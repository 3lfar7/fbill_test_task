from datetime import timedelta
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import redis


class RequestAmountView(APIView):
    def get(self, request, amount):
        client = redis.Redis(**settings.REDIS_CONFIG)
        retry_count = 0
        with client.pipeline() as pipe:
            while True:
                pipe.watch(*['interval:%s' % interval for interval in settings.AMOUNT_LIMITS_CONFIG])
                pipe.multi()
                for interval in sorted(settings.AMOUNT_LIMITS_CONFIG):
                    max_total = settings.AMOUNT_LIMITS_CONFIG[interval]
                    total = client.get('interval:%s' % interval)
                    if total is None:
                        new = True
                        total = 0
                    else:
                        new = False
                        total = int(total)
                    if total + amount <= max_total:
                        pipe.incrby('interval:%s' % interval, amount)
                        if new:
                            pipe.expire('interval:%s' % interval, timedelta(seconds=interval))
                    else:
                        pipe.unwatch()
                        # print({'error': 'amount limit exceeded (%s/%ssec)' % (max_total, interval)})
                        return Response({'error': 'amount limit exceeded (%s/%ssec)' % (max_total, interval)}, status=status.HTTP_400_BAD_REQUEST)
                try:
                    pipe.execute()
                except redis.WatchError:
                    retry_count += 1
                    print('retry_count =', retry_count)
                    if retry_count == settings.MAX_RETRIES:
                        return Response({'error': 'max retries exceeded (%s)' % retry_count}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    break
        # print({'result': 'Ok'})
        return Response({'result': 'Ok'})

from django.conf import settings
from .exceptions import AmountLimitsConfigError


prev_max_total = 0
for interval in sorted(settings.AMOUNT_LIMITS_CONFIG):
    max_total = settings.AMOUNT_LIMITS_CONFIG[interval]
    if max_total < prev_max_total:
        raise AmountLimitsConfigError('Incorrect amount limits configuration %s: %s.' % (interval, max_total))
    prev_max_total = max_total
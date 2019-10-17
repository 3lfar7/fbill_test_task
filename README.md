# 4bill test

fbill_test_task/settings.py - configuration (AMOUNT_LIMITS_CONFIG, MAX_RETRIES, REDIS_CONFIG) is at the end of the file. 

fbill/views.py - RequestAmountView endpoint.


## Deployment without docker:

* systemctl enable redis
* systemctl start redis
* python3 -m venv env
* source env/bin/activate
* pip install -r requirements.txt
* python manage.py runserver 0.0.0.0:8000
* redis-cli -p 6379
* test.sh (parallel requests) or curl http://127.0.0.1:8000/request/100/

## Deployment with docker:
* docker-compose up
* redis-cli -p 8989
* test.sh (parallel requests) or curl http://127.0.0.1:8000/request/100/

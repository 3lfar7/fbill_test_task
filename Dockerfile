FROM python:3.7.4
WORKDIR /fbill_test_task
COPY . /fbill_test_task
RUN pip install -r requirements.txt

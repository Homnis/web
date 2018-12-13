# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task, task
import time
import logging

# pip install django-celery-results
# celery -A mysite worker --loglevel=info
# pip install eventlet
# celery -A mysite worker --loglevel=info -P eventlet
# python manage.py migrate django_celery_results
# 定时任务
# https://www.cnblogs.com/dengshihuang/p/8258621.html

@task
def add():
    print("开发发送…………")
    for i in range(10):
        print(i)
        print("hhhh")
        logging.warning(111111111111)
        time.sleep(1)
    print("结束发送…………")


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)

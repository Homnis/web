from __future__ import absolute_import, unicode_literals
import time,json,utils
from celery import task
from django.conf import settings
from django.core.mail import send_mail


@task
def send_email(uid, username, email):
    # print(token)
    token=utils.md5_by_hmac(str(uid))
    # 发邮件
    subject = '主题信息'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [email]
    print(1)
    html_message = '<h1>%s,信息语句</h1>请点击下面的链接激活您的帐号<br/><a href="http://127.0.0.1:8000/users/active/%s">请点击我</a>' % (
        username, token)
    send_mail(subject, message, sender, receiver, html_message=html_message)
    print('发送成功。。。')

# subject = '主题信息'
# message = ''
# sender = settings.EMAIL_FROM
# receiver = ["675868749@qq.com"]
# print(1)
# send_mail(subject, message, sender, receiver, html_message="<h1>信息语句</h1>")
# print(2)
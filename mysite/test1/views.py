from django.http import HttpResponse
# from django.db import models

import os

from . import models


# 视图函数
def index(request):
    print("首页被访问了……")
    return HttpResponse("<h1>项目首页面</h1><a href='/test1/login'>登录</a><br/><a href='/test1/reg'>注册</a>")

def login(request):
    print("登陆页面被访问了……")
    return HttpResponse("<h1>登录页面</h1><br/>"
                        "<a href='https://news.sina.com.cn/'>新浪新闻</a>"
                        "<br/><a href='https://finance.sina.com.cn/'>新浪财经</a>"
                        "<br/><a href='/test1/myHtml'>myHtml</a>"
                        "<br/><a href='/test1/index'>返回首页</a>")

def reg(request):
    print("注册页面被访问了……")
    # users=models.User.user_manager.create(name="黄焱鑫",gender="男",age=22)
    # users=models.User(name="abc",gender="男",age=1)
    # users.save()
    # print(users)
    return HttpResponse("<h1>注册页面</h1><a href='/test1/index'>返回首页</a>")

def baidu(request):
    # print("注册页面被访问了……")
    return HttpResponse("<a href='http://www.baidu.com'>百度</a>")

def myHtml(request):
    path = os.path.dirname(os.path.abspath(__file__))
    with open(r"{path}\9-21.html".format(path=path), "rb") as f:
        aHtml = f.read().decode('utf-8')
        print(type(aHtml))
    return HttpResponse(aHtml)
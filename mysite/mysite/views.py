from django.http import HttpResponse

# 视图函数
def index(request):
    print("首页被访问了……")
    return HttpResponse("<h1>项目首页面！！！！</h1>")

def login(request):
    print("登陆页面被访问了……")
    return HttpResponse("<h1>登陆页面！！！！</h1>")

def reg(request):
    print("注册页面被访问了……")
    return HttpResponse("<h1>注册页面！！！！</h1>")

def baidu(request):
    # print("注册页面被访问了……")
    return HttpResponse("<a href='http://www.baidu.com'>百度</a>")
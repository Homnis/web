from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
import json

from . import models


# Create your views here.

def home(request):
    # print(request.session["now"])
    # context={request.session.get("now"),}
    return render(request, 'db_static/home.html')


def reg(request):
    # return render(request, 'db_static/reg.html',context_instance=RequestContext(request))
    return render(request, 'db_static/reg.html')


# @csrf_protect
def doReg(request):
    name = request.POST["name"]
    psw = request.POST["psw"]
    age = int(request.POST["age"])
    gender = request.POST["gender"]
    address = request.POST["address"]
    try:
        oldName=models.User.objects.get(name=name)
        return render(request, "db_static/reg_fail.html")
    except:
        if len(address) == 0:
            try:
                user = models.User(name=name, psw=psw, age=age, gender=gender)
                user.save()
                return render(request, "db_static/reg_success.html")
            except:
                return render(request, "db_static/reg_fail.html")
        else:
            try:

                user = models.User(name=name, psw=psw, age=age, gender=gender, address=address)
                user.save()

                return render(request, "db_static/reg_success.html")
            except:
                return render(request, "db_static/reg_fail.html")


def login(request):
    return render(request, 'db_static/login.html')


# @csrf_protect
def doLogin(request):
    name = request.POST["name"]
    psw = request.POST["psw"]
    user = models.User.objects.get(name=name)
    request.session.set_expiry(0)
    if user.psw == psw:
        request.session.clear()
        request.session['now'] = name
        return render(request, 'db_static/login_success.html', )
    else:
        return render(request, 'db_static/login_fail.html')


# 查看当前用户信息
def info(request):
    name = request.session.get("now")
    # print(name)
    # 不存在时返回值是none
    if name != None:
        user = models.User.objects.get(name=name)
        context = {
            "name": user.name,
            "age": user.age,
            "gender": user.gender,
            "address": user.address,
        }
        return render(request, 'db_static/info_show.html', context=context)
    else:
        return render(request, 'db_static/info_fail.html')


# 修改当前用户信息
def changeInfo(request):
    name = request.session.get("now")
    # print(name)
    # 不存在时返回值是none
    if name != None:
        user = models.User.objects.get(name=name)
        context = {
            "name": user.name,
            "age": user.age,
            "gender": user.gender,
            "address": user.address,
        }
        return render(request, 'db_static/change_info.html', context=context)
    else:
        return render(request, 'db_static/info_fail.html')


def doChangeInfo(request):
    name = request.session.get("now")
    changeWhat = request.POST["changeWhat"]
    result = request.POST["result"]
    user = models.User.objects.get(name=name)
    try:
        if changeWhat == "gender":
            user.gender = result
        elif changeWhat == "age":
            user.age = int(result)
        elif changeWhat == "address":
            user.age = result
        user.save()
        return render(request, "db_static/change_info_success.html")
    except:
        return render(request, "db_static/change_info_fail.html")


# 修改当前用户密码
def changePsw(request):
    name = request.session.get("now")
    if name != None:
        return render(request, 'db_static/change_psw.html')
    else:
        return render(request, 'db_static/info_fail.html')


def doChangePsw(request):
    name = request.session.get("now")
    user = models.User.objects.get(name=name)
    psw = request.POST["psw"]
    psw_confirm = request.POST["psw_confirm"]
    if psw != user.psw:
        if psw == psw_confirm:
            return render(request, 'db_static/change_psw_success.html')
        else:
            return render(request, 'db_static/change_psw_fail.html')
    else:
        return render(request, 'db_static/change_psw_fail.html')

# 查看用户列表
def users(request):
    users=models.User.objects.all()
    usersList=[]
    for i in users:
        usersList.append(i.name)
    return render(request,'db_static/users.html',{'List': json.dumps(usersList),})

# 删除当前用户
def delete(request):
    name = request.session.get("now")
    if name != None:
        user = models.User.objects.get(name=name)
        context = {
            "name": user.name,
            "age": user.age,
            "gender": user.gender,
            "address": user.address,
        }
        return render(request, 'db_static/delete.html',context=context)
    else:
        return render(request, 'db_static/info_fail.html')

def doDelete(request):
    name = request.session.get("now")
    if name != None:
        user = models.User.objects.get(name=name)
        user.delete()
        return render(request, 'db_static/delete_success.html')
    else:
        return render(request, 'db_static/info_fail.html')
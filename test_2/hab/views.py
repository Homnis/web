from django.shortcuts import render, redirect
# from django.http import HttpResponseRedirect

from . import models


def index(request):
    # users=request.session.get("loginUser")
    # id=users.id
    # nickname=users.nickname
    # gender=users.gender
    # age=users.age
    # email=users.email
    # context={
    #     "id":id,
    #     "nickname":nickname,
    #     "gender":gender,
    #     "age":age,
    #     "email":email,
    # }
    request.session.set_expiry(0)
    return render(request, "hab/index.html")


def register(request):
    """ 用户注册功能
    """
    if request.method == "GET":
        return render(request, "hab/register.html", {"msg": "请认真填写如下选项"})
    elif request.method == "POST":
        username = request.POST["username"].strip()
        password = request.POST.get("password")
        confirmpwd = request.POST["confirmpwd"]
        nickname = request.POST["nickname"]

        # 数据校验
        if username == "":
            return render(request, "hab/register.html", {"msg": "用户名称不能为空"})
        if len(password) < 3:
            return render(request, "hab/register.html", {"msg": "用户密码长度不能小于3位"})
        if password.strip() != confirmpwd.strip():
            return render(request, "hab/register.html", {"msg": "两次密码不一致"})
        if nickname == "":
            return render(request, "hab/register.html", {"msg": "用户昵称不能为空"})

        # 用户名称不能重复
        try:
            models.User.objects.get(username=username)
            return render(request, "hab/register.html", {"msg": "该用户名称已经存在，请重新输入"})
        except:
            try:
                user = models.User(username=username, password=password, nickname=nickname)
                user.save()
            except:
                return render(request, "hab/register.html", {"msg": "注册失败，请重新注册"})

        return render(request, "hab/login.html", {"msg": "用户注册成功！！，请登录"})


def login(request):
    """ 用户登录功能
    """
    if request.method == "GET":
        return render(request, "hab/login.html", {"msg": "请认真填写如下选项"})
    else:
        # 接受页面的参数
        username = request.POST["username"].strip()
        password = request.POST["password"].strip()

        # 数据校验
        if username == "":
            return render(request, "hab/login.html", {"msg": "用户名称不能为空"})
        if password == "":
            return render(request, "hab/login.html", {"msg": "用户密码不能为空"})

        users = models.User.objects.filter(username=username)
        if len(users) > 0:
            if users[0].password == password:
                # 登录成功，需要保持用户的信息，以表示用户已经登录
                request.session["loginUser"] = users[0]
                # 比如说跳转用户列表页面
                # return HttpResponseRedirect("/hab/user_list/")
                return redirect("/hab/index/")
            else:
                return render(request, "hab/login.html", {"msg": "密码错误！！"})
        else:
            return render(request, "hab/login.html", {"msg": "该用户名不存在！！"})


def logout(request):
    """用户退出"""
    try:
        del request.session["loginUser"]
        return render(request, "hab/login.html", {"msg": "用户退出成功，请重新登录！！"})
    except:
        return render(request, "hab/login.html", {"msg": "用户退出成功，请重新登录！！"})


def user_list(request):
    users = models.User.objects.all()
    return render(request, "hab/user_list.html", {"users": users})


# def user_update(request, changeWhat):
#     request.session["changeWhat"]=changeWhat
#     return render(request, "hab/user_update_wrong.html")
#
#
# def do_update(request):
#     users = models.User.objects.get(username=request.session.get("loginUser").username)
#     changeWhat = request.session.get("changeWhat")
#     nickname = users.nickname
#     age = users.age
#     gender = users.gender
#     email = users.email
#     result=request.POST["result"]
#     if changeWhat=="nickname":
#         users.nickname = result
#         users.age = age
#         users.gender = gender
#         users.email = email
#     elif changeWhat=="age":
#         users.age = int(result)
#         users.gender = gender
#         users.email = email
#         users.nickname=nickname
#     elif changeWhat=="gender":
#         users.gender=result
#         users.email = email
#         users.nickname=nickname
#         users.age=age
#     elif changeWhat=="email":
#         users.nickname = nickname
#         users.age = age
#         users.gender = gender
#         users.email = result
#     users.save()
#     return render(request,"/hab/user_info/")

def user_update(request):
    user = models.User.objects.get(username=request.session.get("loginUser").username)
    return render(request,"hab/user_update.html",context={"users":user})

def do_update(request):
    user = models.User.objects.get(username=request.session.get("loginUser").username)
    nickname = request.POST["nickname"]
    age = request.POST["age"]
    gender = request.POST["gender"]
    email = request.POST["email"]

    user.nickname = nickname
    user.age = age
    user.gender = gender
    user.email = email

    user.save()
    return redirect("/hab/user_info/")

def user_delete(request, user_id):
    user = models.User.objects.get(pk=user_id)
    user.delete()
    return redirect("/hab/user_list/")


def user_info(request):
    return render(request, "hab/user_info.html")


def test(request):
    content = "<h1>这个是内容</h1>"
    users = ["张三", "李四", "王五", "赵六"]
    # users = []
    user = models.User.objects.get(pk=1)
    return render(request, "test.html", {"content": content, "users": users, \
                                         "users": user})

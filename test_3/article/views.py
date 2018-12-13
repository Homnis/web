from io import BytesIO
import logging
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse,JsonResponse
import hmac,json
from django.core.paginator import Paginator
from django.core import serializers
from django.conf import settings
# from django.http import HttpResponseRedirect
# from django.core.urlresolvers import reverse

from . import models, utils, verify,cacheUtil


def index(request):
    logger = logging.getLogger("django")
    logger.info("首页开始加载数据量……")
    # add.delay()
    # 分页功能
    pageNow = int(request.GET.get("pageNow", 1))
    pageSize = settings.PAGE_SIZE
    articles = cacheUtil.getAllArticle()
    request.session.set_expiry(0)
    # 第一个参数是需要分页的数据列表，第二个参数是每页的数量
    paginator = Paginator(articles, pageSize)
    # page需要参数的当前页
    page = paginator.page(pageNow)
    return render(request, "article/index.html", {"page":page})


def register(request):
    """ 用户注册功能
    """
    if request.method == "GET":
        return render(request, "article/register.html", {"msg": "请认真填写如下选项"})
    elif request.method == "POST":
        username = request.POST["username"].strip()
        password = request.POST.get("password")
        confirmpwd = request.POST["confirmpwd"]
        nickname = request.POST["nickname"]
        email = request.POST["email"]
        tel = request.POST["tel"]
        age = int(request.POST["age"])
        gender = request.POST["gender"]
        try:
            avatar = request.FILES["avatar"]
        except:
            avatar = None
        verify_code = request.POST['verify_code'].strip()

        # 数据校验
        if username == "":
            return render(request, "article/register.html", {"msg": "用户名称不能为空"})
        if len(password) < 3:
            return render(request, "article/register.html", {"msg": "用户密码长度不能小于3位"})
        if password.strip() != confirmpwd.strip():
            return render(request, "article/register.html", {"msg": "两次密码不一致"})
        if nickname == "":
            return render(request, "article/register.html", {"msg": "用户昵称不能为空"})
        if age > 200:
            return render(request, "article/register.html", {"msg": "年龄不合理"})
        if gender != "男" and gender != "女":
            return render(request, "article/register.html", {"msg": "性别不合理"})
        if verify_code.upper() != request.session.get("code").upper():
            return render(request, "article/register.html", {"msg": "验证码错误"})

        # 用户名称不能重复
        try:
            models.User.objects.get(username=username)
            return render(request, "article/register.html", {"msg": "该用户名称已经存在，请重新输入"})
        except:
            try:
                password = utils.md5_by_hmac(password)
                # password = hmac.new(password.encode("utf-8"), "password".encode("uft-8"), "MD5")
                if avatar is None:
                    user = models.User(username=username, password=password, nickname=nickname, email=email, tel=tel,
                                       age=age, gender=gender)
                    user.save()
                else:
                    user = models.User(username=username, password=password, nickname=nickname, avatar=avatar,
                                       email=email, tel=tel, age=age, gender=gender)
                    user.save()
            except:
                return render(request, "article/register.html", {"msg": "注册失败，请重新注册"})

        return render(request, "article/login.html", {"msg": "用户注册成功！！，请登录"})


# @utils.create_code
def login(request):
    """ 用户登录功能
    """
    if request.method == "GET":
        return render(request, "article/login.html", {})
    else:
        # 接受页面的参数
        username = request.POST["username"].strip()
        password = request.POST["password"].strip()
        # verify_code = request.POST['verify_code'].strip()
        try:
            request.session.get("display")
            verify_code = request.POST['verify_code'].strip()
        except:
            verify_code = "no verify"
        password = utils.md5_by_hmac(password)
        # 数据校验
        if verify_code == "":
            return render(request, "article/login.html", {"msg": "验证码不能为空"})
        if username == "":
            return render(request, "article/login.html", {"msg": "用户名称不能为空"})
        if password == "":
            return render(request, "article/login.html", {"msg": "用户密码不能为空"})
        users = models.User.objects.filter(username=username)
        # print(verify_code.upper())
        if verify_code == "no verify" or verify_code.upper() == request.session.get("code").upper():
            if len(users) > 0:
                if users[0].password == password:
                    # 登录成功，需要保持用户的信息，以表示用户已经登录
                    request.session["loginUser"] = users[0]
                    request.session["tryTime"] = 0
                    try:
                        del request.session['display']
                    except:
                        pass
                    return redirect(reverse("article:user_list"))
                else:
                    try:
                        # request.session.get("tryTime")
                        request.session["tryTime"] += 1
                    except:
                        request.session["tryTime"] = 0
                    if request.session["tryTime"] > 2:
                        request.session["display"] = 1
                    nowTryTime=3-request.session["tryTime"]
                    if nowTryTime>0:
                        return render(request, "article/login.html", {"msg": "密码错误！！{tryTime}次后将输入验证码".format(tryTime=str(nowTryTime))})
                    else:
                        return render(request, "article/login.html", {"msg": "密码错误！！请输入验证码"})
            else:
                return render(request, "article/login.html", {"msg": "该用户名不存在！！"})
        else:
            return render(request, "article/login.html", {"msg": "验证码错误！！"})


@utils.requirelogin
def logout(request):
    """用户退出"""
    try:
        del request.session["loginUser"]
        return render(request, "article/login.html", {"msg": "用户退出成功，请重新登录！！"})
    except:
        return render(request, "article/login.html", {"msg": "用户退出成功，请重新登录！！"})


@utils.requirelogin
def user_list(request):
    users = models.User.objects.all()
    return render(request, "article/user_list.html", {"users": users})


@utils.requirelogin
def user_update(request):
    if request.method == "GET":
        id = request.GET["id"]
        user = models.User.objects.get(pk=id)
        return render(request, "article/user_update.html", {"users": user})
    else:
        nickname = request.POST["nickname"]
        age = request.POST["age"]
        gender = request.POST["gender"]
        email = request.POST["email"]
        tel = request.POST["tel"]

        user = models.User.objects.get(pk=request.session.get("loginUser").id)
        user.nickname = nickname
        user.age = age
        user.gender = gender
        user.email = email
        user.tel = tel

        user.save()
        request.session["loginUser"] = user
        return redirect(reverse("article:user_info"))


@utils.requirelogin
def user_delete(request):
    user = models.User.objects.get(pk=request.session.get("loginUser").id)
    user.delete()
    # return redirect("/article/user_list/")
    return redirect(reverse("article:user_list"))


def user_info(request):
    user = models.User.objects.get(id=request.session.get("loginUser").id)
    return render(request, "article/user_info.html", {"users": user})


@utils.requirelogin
def article_add(request):
    if request.method == "GET":
        return render(request, "article/article_add.html", {})
    elif request.method == "POST":
        title = request.POST["title"].strip()
        content = request.POST["content"].strip()
        # print(content)
        remark = utils.removeHTMLByRE(content)[:50]
        # print(content)
        author = request.session["loginUser"]

        # 验证
        if title == "":
            return render(request, "article/article_add.html", {"msg": "文字标题不能为空！"})
        if content == "":
            return render(request, "article/article_add.html", {"msg": "文字内容不能为空！"})

        at = models.Article(title=title, content=content, remark=remark, author=author)
        at.save()
        # 更新缓存
        cacheUtil.getAllArticle(ischange=True)
        return JsonResponse({"msg": "文章添加成功", "success": True})
        # return render(request,"article/index.html")

@utils.requirelogin
def article_delete(request, a_id):
    at = models.Article.objects.get(pk=a_id)
    at.delete()
    cacheUtil.getAllArticle(ischange=True)
    return redirect(reverse("article:article_list"))
    # return JsonResponse({"msg": "文章添加成功", "success": True})


@utils.requirelogin
def article_update(request, a_id):
    at = models.Article.objects.get(id=a_id)
    if request.method == "GET":
        return render(request, "article/article_update.html", {"article": at})
    else:
        title = request.POST["title"].strip()
        content = request.POST["content"].strip()
        remark = content[:50]
        # 验证
        if title == "":
            return render(request, "article/article_update.html", {"article": at, "msg": "文字标题不能为空！"})
        if content == "":
            return render(request, "article/article_update.html", {"article": at, "msg": "文字内容不能为空！"})

        at = models.Article.objects.get(pk=a_id)
        at.title = title
        at.content = content
        at.remark = remark
        at.save()
        return redirect(reverse("article:article_detail", kwargs={"a_id": at.id}))


def article_detail(request, a_id):
    at = models.Article.objects.get(pk=a_id)
    return render(request, "article/article_detail.html", {"article": at})


@utils.requirelogin
def article_list(request):
    ats = cacheUtil.getAllArticle()
    # articles=serializers.serialize("json",ats)
    # for i in ats:
    #     print(i.remark)
    return render(request, "article/article_list.html", {"articles": ats})
    # return JsonResponse({"articles": articles, "success": True})

@utils.requirelogin
def psw_update(request):
    if request.method == "POST":
        user = models.User.objects.get(id=request.session["loginUser"].id)
        psw = user.password
        oldPsw = request.POST['oldPsw']
        newPsw = request.POST['newPsw']
        confirmPsw = request.POST["confirmPsw"]
        if newPsw != confirmPsw:
            return render(request, "article/psw_update.html", {"msg": "两次输入的密码不一致！"})
        if oldPsw != psw:
            return render(request, "article/psw_update.html", {"msg": "当前密码错误！"})
        if oldPsw == newPsw:
            return render(request, "article/psw_update.html", {"msg": "与当前密码相同！"})
        user = models.User.objects.get(pk=request.session.get("loginUser").id)
        user.password = newPsw
        # users.nickname=users.nickname
        # users.email=users.email
        # users.gender=users.gender
        # users.age=users.age
        # users.username=users.username
        # users.avatar=users.avatar
        # users.tel=users.tel
        user.save()
        request.session["loginUser"] = user
        return redirect(reverse("article:user_info"))
    else:
        return render(request, "article/psw_update.html")


def upload_avatar(request):
    if request.method == "POST":
        user = models.User.objects.get(id=request.session["loginUser"].id)
        avatar = request.FILES['avatar']
        user.avatar = avatar
        user.save()
        request.session["loginUser"] = user
        return redirect(reverse("article:index"))
    else:
        return render(request, "article/upload_avatar.html")


def code(request):
    filename, code = verify.create_code()
    request.session['code'] = code
    f = BytesIO()
    filename.save(f, "PNG")
    return HttpResponse(f.getvalue(), "image/png")

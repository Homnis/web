import time
from io import BytesIO
import logging

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET, require_safe, require_http_methods
from django.forms.models import model_to_dict
from django.core.serializers import serialize
from django.core.paginator import Paginator
from django.conf import settings

from . import models
from . import utils
from . import cacheUtil
# from .tasks import add

def index(request):
    logger = logging.getLogger("django")
    logger.info("首页开始加载数据量……")
    # add.delay()
    # 分页功能
    pageNow = int(request.GET.get("pageNow", 1))
    pageSize = settings.PAGE_SIZE
    ats = cacheUtil.getAllArticle()
    # 第一个参数是需要分页的数据列表，第二个参数是每页的数量
    paginator = Paginator(ats, pageSize)
    # page需要参数的当前页
    page = paginator.page(pageNow)
    return render(request, "index.html", {"page": page})


def register(request):
    """ 用户注册功能
    """
    if request.method == "GET":
        return render(request, "blog/register.html", {"msg": "请认真填写如下选项"})
    elif request.method == "POST":
        username = request.POST["username"].strip()
        password = request.POST.get("password")
        confirmpwd = request.POST["confirmpwd"]
        nickname = request.POST["nickname"]
        avatar = request.FILES["avatar"]

        # 数据校验
        if username == "":
            return render(request, "blog/register.html", {"msg": "用户名称不能为空"})
        if len(password) < 3:
            return render(request, "blog/register.html", {"msg": "用户密码长度不能小于3位"})
        if password.strip() != confirmpwd.strip():
            return render(request, "blog/register.html", {"msg": "两次密码不一致"})
        if nickname == "":
            return render(request, "blog/register.html", {"msg": "用户昵称不能为空"})

        # 用户名称不能重复
        try:
            models.User.objects.get(username=username)
            return render(request, "blog/register.html", {"msg": "该用户名称已经存在，请重新输入"})
        except:
            try:
                # 进行密码加密
                password = utils.md5_by_hmac(password)
                if avatar is None:
                    user = models.User(username=username, password=password, nickname=nickname)
                    user.save()
                else:
                    user = models.User(username=username, password=password, nickname=nickname, avatar=avatar)
                    user.save()
            except:
                return render(request, "blog/register.html", {"msg": "注册失败，请重新注册"})

        return render(request, "blog/login.html", {"msg": "用户注册成功！！，请登录"})


def login(request):
    """ 用户登录功能
    """
    if request.method == "GET":
        return render(request, "blog/login.html", {"msg": "请认真填写如下选项"})
    else:
        # 接受页面的参数
        username = request.POST["username"].strip()
        password = request.POST["password"].strip()
        code = request.POST["code"].strip()

        # 数据校验
        if code.lower() != request.session["code"].lower():
            return render(request, "blog/login.html", {"msg": "验证码错误！！"})
        if username == "":
            return render(request, "blog/login.html", {"msg": "用户名称不能为空"})
        if password == "":
            return render(request, "blog/login.html", {"msg": "用户密码不能为空"})

        users = models.User.objects.filter(username=username)
        if len(users) > 0:
            # 加密密码
            password = utils.md5_by_hmac(password)
            if users[0].password == password:
                # 登录成功，需要保持用户的信息，以表示用户已经登录
                request.session["loginUser"] = users[0]
                # 比如说跳转用户列表页面
                # return HttpResponseRedirect("/blog/user_list/")
                # return redirect("/blog/user_list/")
                response = redirect(reverse("blog:user_list"))
                response.set_cookie("isLogin", True, max_age=3600*24*14)
                return response
            else:
                return render(request, "blog/login.html", {"msg": "密码错误！！"})
        else:
            return render(request, "blog/login.html", {"msg": "该用户名不存在！！"})


@utils.requirelogin
def logout(request):
    """用户退出"""
    try:
        del request.session["loginUser"]
        return render(request, "blog/login.html", {"msg": "用户退出成功，请重新登录！！"})
    except:
        return render(request, "blog/login.html", {"msg": "用户退出成功，请重新登录！！"})


@utils.requirelogin
def user_list(request):
    users = models.User.objects.all()
    return render(request, "blog/user_list.html", {"users": users})


@utils.requirelogin
def user_update(request):
    if request.method == "GET":
        id = request.GET["id"]
        user  = models.User.objects.get(pk=id)
        return render(request, "blog/user_update.html", {"users": user})
    else:
        id = request.POST["id"]
        nickname = request.POST["nickname"]
        age = request.POST["age"]
        gender = request.POST["gender"]
        email = request.POST["email"]

        user = models.User.objects.get(pk=id)
        user.nickname = nickname
        user.age = age
        user.gender = gender
        user.email = email

        user.save()
        # return redirect("/blog/user_list/")
        # return redirect(reverse("blog:user_list", kwargs={"user_id": 2233}))
        # return redirect(reverse("blog:user_list", args=(1,)))
        return redirect(reverse("blog:user_list"))


@utils.requirelogin
def user_delete(request, user_id):
    user = models.User.objects.get(pk=user_id)
    user.delete()
    # return redirect("/blog/user_list/")
    return redirect(reverse("blog:user_list"))


def user_info(request, u_id):
    user = models.User.objects.get(id=u_id)
    return render(request, "blog/user_info.html", {"users": user})


@utils.requirelogin
# @csrf_exempt
def article_add(request):
    if request.method == "GET":
        return render(request, "blog/article_add.html", {})
    elif request.method == "POST":
        title = request.POST["title"].strip()
        content = request.POST["content"].strip()
        remark = utils.removeHTMLByRE(content)[:50]
        author = request.session["loginUser"]

        # 验证
        if title == "":
            return render(request, "blog/article_add.html", {"msg": "文字标题不能为空！"})
        if content == "":
            return render(request, "blog/article_add.html", {"msg": "文字内容不能为空！"})

        at = models.Article(title=title, content=content, remark=remark, author=author)
        at.save()
        # 更新缓存
        cacheUtil.getAllArticle(ischange=True)
        # return redirect(reverse("blog:article_detail", kwargs={"a_id": at.id}))
        return JsonResponse({"msg": "文章添加成功", "success": True})


@utils.requirelogin
def article_delete(request, a_id):
    at = models.Article.objects.get(pk=a_id)
    at.delete()
    # 更新缓存
    cacheUtil.getAllArticle(ischange=True)
    return redirect(reverse("blog:list_self"))


@utils.requirelogin
def article_update(request, a_id):
    at = models.Article.objects.get(id=a_id)
    if request.method == "GET":
        return render(request, "blog/article_update.html", {"article": at})
    else:
        title = request.POST["title"].strip()
        content = request.POST["content"].strip()
        remark = utils.removeHTMLByRE(content)[:50]
        # 验证
        if title == "":
            return render(request, "blog/article_update.html", {"article": at, "msg": "文字标题不能为空！"})
        if content == "":
            return render(request, "blog/article_update.html", {"article": at, "msg": "文字内容不能为空！"})

        at = models.Article.objects.get(pk=a_id)
        at.title = title
        at.content = content
        at.remark = remark
        at.save()

        # 更新缓存
        cacheUtil.getAllArticle(ischange=True)
        return redirect(reverse("blog:article_detail", kwargs={"a_id": at.id}))


def article_detail(request, a_id):
    at = models.Article.objects.get(pk=a_id)
    return render(request, "blog/article_detail.html", {"article": at})


@utils.requirelogin
def list_self(request):
    # ats = models.Article.objects.filter(author=request.session["loginUser"])
    # return render(request, "blog/list_self.html", {"articles": ats})
    return render(request, "blog/list_self.html", {})


def code(request):
    img, msg = utils.create_code()

    f = BytesIO()
    img.save(f, "PNG")

    # 将验证码的值存储到session
    request.session["code"] = msg

    return HttpResponse(f.getvalue(), "image/png")



# @csrf_exempt # 表示该视图函数忽略csrf验证
# # @require_POST
# # @require_http_methods(["GET","POST"])
# # @require_safe
# @require_GET
# def hello_ajax(request):
#     print("id=", request.POST["id"])
#     return HttpResponse("hello ajax")


# @require_GET
# def hello_ajax_jquery(request):
    # res = {"id": 10}
    # # 如果返回的是字典对象，需要使用JsonResponse
    # return JsonResponse(res)
    # res = "{\"id\": 10}"
    # return HttpResponse(res, "application/json")
    # id = request.GET['id']
    # users = models.User.objects.get(pk=id)
    # model_to_dict 该方法，真能使用在我们model转换为字典对象的时候
    # res = model_to_dict(users)
    # print(res)
    # res = {"users": users}
    # return JsonResponse(res)

    # ats = models.Article.objects.all()
    # # serialize 会根据第一个参数将queryset序列化为一个字符串
    # res = serialize("json", ats)
    # return HttpResponse(res, "application/json")
    #
    # ats = models.Article.objects.values("id", "title","content")
    # return HttpResponse(ats)


@csrf_exempt
@require_POST
def checkusername(request):
    username = request.POST["username"]
    try:
        models.User.objects.get(username=username)
        return JsonResponse({"msg": "对不起，该账户已经存在，请重新注册", "success": False})
    except:
        return JsonResponse({"msg": "恭喜你，该账户可以使用", "success": True})


def test(request):
    response = HttpResponse("hello world")
    response.set_cookie("username", "liujianhong", max_age=3600*24*14)

    return response
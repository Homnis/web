from django.shortcuts import render, redirect
from django.db import transaction
from io import BytesIO
import random,urllib,http.client
from django.http import HttpResponse,JsonResponse
from django.core.paginator import Paginator
from django.core.mail import send_mail

import utils, verify, json
from users import models
from books import models as b_models
from shoppingCar import models as s_models
from users.tasks import send_email


def checktel(request):
    username = request.POST.get("username")
    try:
        models.Passport.objects.get(tel=username)
        return JsonResponse({"success": False, "msg": "用户名已存在"})
    except:
        return JsonResponse({"success": True, "msg": "用户名可用"})

def checkemail(request):
    username = request.POST.get("username")
    try:
        models.Passport.objects.get(email=username)
        return JsonResponse({"success": False, "msg": "用户名已存在"})
    except:
        return JsonResponse({"success": True, "msg": "用户名可用"})


def send_message(request):
    # 请求的路径
    host = "106.ihuyi.com"
    sms_send_uri = "/webservice/sms.php?method=Submit"
    # 用户名是登录ihuyi.com账号名（例如：cf_demo123）
    account = "C48875960"
    # 密码 查看密码请登录用户中心->验证码、通知短信->帐户及签名设置->APIKEY
    password = "b08243961e99bbbe5089ef304e80caed"

    """发送信息的视图函数"""
    # 获取ajax的get方法发送过来的手机号码
    mobile = request.GET.get('mobile')
    # 定义一个字符串,存储生成的6位数验证码
    message_code = ''
    for i in range(6):
        i = random.randint(0, 9)
        message_code += str(i)
    # 拼接成发出的短信
    text = "您的验证码是：" + message_code + "。请不要把验证码泄露给其他人。"
    # 把请求参数编码
    params = urllib.parse.urlencode(
        {'account': account, 'password': password, 'content': text, 'mobile': mobile, 'format': 'json'})
    # 请求头
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    # 通过全局的host去连接服务器
    conn = http.client.HTTPConnection(host, port=80, timeout=30)
    # 向连接后的服务器发送post请求,路径sms_send_uri是全局变量,参数,请求头
    conn.request("POST", sms_send_uri, params, headers)
    # 得到服务器的响应
    response = conn.getresponse()
    # 获取响应的数据
    response_str = response.read()
    # 关闭连接
    conn.close()
    # 把验证码放进session中
    request.session['message_code'] = message_code
    print(eval(response_str.decode()))
    # 使用eval把字符串转为json数据返回
    return JsonResponse(eval(response_str.decode()))

@transaction.atomic
def register_email(request):
    username = request.POST.get("email").strip()
    password = request.POST.get("passwordB").strip()
    re_password = request.POST.get("passwordB2").strip()
    tel = int(request.POST["tel"])
    if username == "":
        return render(request, "users/register.html", {"msg": "用户名称不能为空"})
    if len(password) < 3:
        return render(request, "users/register.html", {"msg": "用户密码长度不能小于3位"})
    if re_password == password:
        if models.Passport.objects.filter(username=username):
            return render(request, "users/register.html", {"msg": "注册失败用户名已存在"})
        else:
            # 保存用户
            s=transaction.savepoint()
            try:
                password = utils.md5_by_hmac(password)
                user = models.Passport(username=username, email=username, password=password, tel=tel)
                user.save()
                """
                    发送激活邮件
                """
                send_email.delay(user.id, username, username)
                transaction.savepoint_commit(s)
            except:
                transaction.rollback(s)
            return render(request, "users/register.html", {"msg": "邮件已发送"})
    else:

        return render(request, "users/register.html", {"msg": "注册失败两次密码不一致"})


# Create your views here.
# 手机注册
@transaction.atomic
def register(request):
    """
    TODO:手机注册
    """
    if request.method == "GET":
        return render(request, "users/register.html", {"msg": "请认真填写如下选项"})
    elif request.method == "POST":
        username = request.POST["phone"].strip()
        password = request.POST["passwordA"]
        re_password = request.POST.get("passwordA2").strip()
        tel_code = request.POST['tel_code'].strip()

        # 数据校验
        if username == "":
            return render(request, "users/register.html", {"msg": "用户名称不能为空"})
        if len(password) < 3:
            return render(request, "users/register.html", {"msg": "用户密码长度不能小于3位"})
        # if password.strip() != confirmpwd.strip():
        #     return render(request, "users/register.html", {"msg": "两次密码不一致"})
        if tel_code.upper() != request.session.get("message_code").upper():
            return render(request, "users/register.html", {"msg": "验证码错误"})

        # 用户名称不能重复
        if re_password == password:
            try:
                models.Passport.objects.get(username=username)
                return render(request, "users/register.html", {"msg": "该用户名称已经存在，请重新输入"})
            except:
                s=transaction.savepoint()
                try:
                    password = utils.md5_by_hmac(password)
                    # print(password)
                    # password = hmac.new(password.encode("utf-8"), "password".encode("uft-8"), "MD5")
                    user = models.Passport(username=username, password=password, tel=username,is_active=True)
                    user.save()
                    transaction.savepoint_commit(s)
                except:
                    transaction.rollback(s)
                    return render(request, "users/register.html", {"msg": "注册失败，请重新注册"})
        else:
            return render(request, "users/register.html", {"msg": "注册失败，两次输入密码不一致"})
        return render(request, "users/login.html", {"msg": "用户注册成功！！，请登录"})


# 激活函数
def active(request, token):
    # print("active")
    print(token)
    try:
        users = models.Passport.objects.all()
        for i in users:
            if utils.md5_by_hmac(str(i.id)) == token:
                i.is_active = 1
                i.save()
        return render(request, "users/login.html", {"msg": "用户激活成功！！，请登录"})
    except Exception as e:
        return HttpResponse("激活失败！请联系服务人员！")


def login(request):
    """ 用户登录功能
    """
    if request.method == "GET":
        return render(request, "users/login.html", {})
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
            return render(request, "users/login.html", {"msg": "验证码不能为空"})
        if username == "":
            return render(request, "users/login.html", {"msg": "用户名称不能为空"})
        if password == "":
            return render(request, "users/login.html", {"msg": "用户密码不能为空"})
        users = models.Passport.objects.filter(username=username)
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
                    # 获得购物车对象
                    user = models.Passport.objects.get(pk=request.session.get("loginUser").id)
                    shopcarts = s_models.ShopCart.objects.filter(user=user)
                    # 购物车中有多少类商品
                    carts_count = len(shopcarts)
                    request.session["carts_count"]=carts_count
                    return redirect("/")
                else:
                    try:
                        # request.session.get("tryTime")
                        request.session["tryTime"] += 1
                    except:
                        request.session["tryTime"] = 0
                    if request.session["tryTime"] > 2:
                        request.session["display"] = 1
                    nowTryTime = 3 - request.session["tryTime"]
                    if nowTryTime > 0:
                        return render(request, "users/login.html",
                                      {"msg": "密码错误！！{tryTime}次后将输入验证码".format(tryTime=str(nowTryTime))})
                    else:
                        return render(request, "users/login.html", {"msg": "密码错误！！请输入验证码"})
            else:
                return render(request, "users/login.html", {"msg": "该用户名不存在！！"})
        else:
            return render(request, "users/login.html", {"msg": "验证码错误！！"})


@utils.requirelogin
def logout(request):
    """用户退出"""
    try:
        del request.session["loginUser"]
        del request.session["carts_count"]
        return render(request, "users/login.html", {"msg": "用户退出成功，请重新登录！！"})
    except:
        return render(request, "users/login.html", {"msg": "用户退出成功，请重新登录！！"})


@utils.requirelogin
def psw_update(request):
    if request.method == "GET":
        return render(request, "users/psw_update.html", {})
    else:
        old_pass = request.POST.get("old_pass").strip()
        new_pass = request.POST.get("new_pass").strip()
        re_pass = request.POST.get("re_pass").strip()
        old_pass = utils.md5_by_hmac(old_pass)
        try:
            user = models.Passport.objects.get(username=request.session.get("loginUser").username, password=old_pass)
            print(user)
            if len(new_pass) > 5 and new_pass == re_pass:
                new_pass = utils.md5_by_hmac(new_pass)
                user.password = new_pass
                print(user)
                user.save()
                return redirect("/users/login/")
            else:
                return render(request, "users/psw_update.html", {"msg": "密码不符合规定！"})

        except:
            return render(request, "users/psw_update.html", {"msg": "旧密码不正确！"})


@utils.requirelogin
def user_update(request):
    if request.method == "GET":
        return render(request, "users/user_update.html", {})
    else:
        username = request.POST.get("username").strip()
        try:
            avatar = request.FILES['avatar']
            print(avatar)
            user = models.Passport.objects.get(id=request.session.get("loginUser").id)
            user.username = username
            user.avatar = avatar
            user.save()
            request.session["loginUser"] = user
            return redirect("books:index")
        except:
            return render(request, "users/user_update.html", {"msg": "修改失败"})


@utils.requirelogin
def manage(request):
    if request.method == "GET":
        return render(request, "users/manage.html")
    if request.session.get('loginUser').is_manager:
        type_id = request.POST['type_id']
        name = request.POST["name"]
        desc = request.POST["desc"]
        price = request.POST["price"]
        stock = request.POST["stock"]
        detail = request.POST["detail"]
        status = request.POST["status"]
        avatar = request.FILES["avatar"]

        book = b_models.Books(name=name, type_id=type_id, desc=desc, price=price, stock=stock,
                              detail=detail, status=status, image=avatar)
        book.save()
        book_img=b_models.BooksImage(image=avatar,books=book)
        book_img.save()
        return render(request, "users/manage.html")
    else:
        return render(request, "users/login.html", {"msg": "不是管理员"})


@utils.requirelogin
def book_list(request):
    if request.session.get('loginUser').is_manager:
        books = b_models.Books.objects.all()
        # 每页显示的条数
        pageSize = 7
        # 获取分页对象
        paginator = Paginator(books, pageSize)
        # 获取分页对象的列表，参数是当前页码
        pageNow = int(request.GET.get("pageNow", 1))
        page = paginator.page(pageNow)

        # 总页数
        num_pages = paginator.num_pages
        # 进行页码控制
        # 1.总页数<5, 显示所有页码
        # 2.当前页是前3页，显示1-5页
        # 3.当前页是后3页，显示后5页 10 9 8 7
        # 4.其他情况，显示当前页前2页，后2页，当前页
        if num_pages < 5:
            pages = range(1, num_pages + 1)
        elif pageNow <= 3:
            pages = range(1, 6)
        elif num_pages - pageNow <= 2:
            pages = range(num_pages - 4, num_pages + 1)
        else:
            pages = range(pageNow - 2, pageNow + 3)
        # print(page.object_list)
        # print(pages)
        # print(page.object_list)
        return render(request, "users/book_list.html",
                      {"page": page, "pageSize": pageSize, "pages": pages, "num_pages": num_pages})
        # return render(request, "users/book_list.html", {"books": books})
    else:
        return render(request, "users/login.html", {"msg": "不是管理员"})


@utils.requirelogin
def book_update(request, id):
    if request.session.get('loginUser').is_manager:
        book = b_models.Books.objects.get(pk=id)
        return render(request, "users/book_update.html", {"book": book})
    else:
        return render(request, "users/login.html", {"msg": "不是管理员"})

@utils.requirelogin
def book_doUpdate(request):
    id = request.POST['id']
    book = b_models.Books.objects.get(pk=id)
    type_id = request.POST['type_id']
    name = request.POST["name"]
    desc = request.POST["desc"]
    price = request.POST["price"]
    stock = request.POST["stock"]
    detail = request.POST["detail"]
    status = request.POST["status"]
    avatar = request.FILES["avatar"]
    book.type_id = type_id
    book.name = name
    book.desc = desc
    book.price = price
    book.stock = stock
    book.detail = detail
    book.status = status
    book.image = avatar
    book.save()
    book_img = b_models.BooksImage(image=avatar, books=book)
    book_img.save()
    books = b_models.Books.objects.all()
    return render(request, "users/book_list.html", {"books": books})

@utils.requirelogin
def book_delete(request, id):
    if request.session.get('loginUser').is_manager:
        book = b_models.Books.objects.get(pk=id)
        book.delete()
        books = b_models.Books.objects.all()
        return render(request, "users/book_list.html", {"books": books})
    else:
        return render(request, "users/login.html", {"msg": "不是管理员"})

@utils.requirelogin
def address(request):
    provinces = models.Provinces.objects.all()
    return render(request,"users/address.html",{"provinces":provinces})

@utils.requirelogin
def regAddress(request):
    province = request.POST.get("province")
    city = request.POST.get("city")
    area = request.POST.get("area")
    desc = request.POST.get("position")
    province = models.Provinces.objects.get(provinceid=province).province
    city = models.Cities.objects.get(cityid=city).city
    area = models.Areas.objects.get(areaid=area).area
    user = models.Passport.objects.get(pk=request.session.get("loginUser").id)
    add = models.Address(passport=user, province=province, city=city, area=area, desc=desc, is_default=True)
    add.save()
    return redirect("/users/addressList/")

@utils.requirelogin
def addressList(request):
    user = models.Passport.objects.get(pk=request.session.get("loginUser").id)
    all_address = models.Address.objects.filter(passport=user)
    address=[]
    for i in all_address:
        address.append(i)
    return render(request,"users/addressList.html",{'address':address})

@utils.requirelogin
def setAddress(request):
    address_id=request.POST["address_id"]
    user = models.Passport.objects.get(pk=request.session.get("loginUser").id)
    former_address = models.Address.objects.get(passport=user, is_default=True)
    former_address.is_default = False
    former_address.save()
    new_address = models.Address.objects.get(pk=address_id)
    new_address.is_default=True
    new_address.save()
    return render(request, "books/index.html")

def getCity(request):
    province = request.POST.get("provinceid")
    cities = models.Cities.objects.all()
    dict = {}
    for i in cities:
        if i.provinceid == province:
            dict[i.cityid] = i.city
    return JsonResponse(dict, content_type="application/json")


def getArea(request):
    city = request.POST.get("cityid")
    areas = models.Areas.objects.all()
    dict = {}
    for i in areas:
        if i.cityid == city:
            dict[i.areaid] = i.area
    return JsonResponse(dict, content_type="application/json")






def agree(request):
    return render(request, "agree.html")


def code(request):
    filename, code = verify.create_code()
    request.session['code'] = code
    f = BytesIO()
    filename.save(f, "PNG")
    return HttpResponse(f.getvalue(), "image/png")

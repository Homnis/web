from django.shortcuts import render
import utils
from users import models as u_models
from order import models as o_models
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.db import transaction


# Create your views here.


@utils.requirelogin
def make_order(request):
    provinces = u_models.Provinces.objects.all()
    try:
        user = u_models.Passport.objects.get(pk=request.session.get("loginUser").id)
        address = u_models.Address.objects.filter(passport=user)
        # print(address)
        content = {"provinces": provinces, "address": address}
    except:
        content = {"provinces": provinces}
    return render(request, "order/make_order.html", content)


@transaction.atomic
@utils.requirelogin
def createAddress(request):
    province = request.POST.get("province")
    city = request.POST.get("city")
    area = request.POST.get("area")
    desc = request.POST.get("position")
    province = u_models.Provinces.objects.get(provinceid=province).province
    city = u_models.Cities.objects.get(cityid=city).city
    area = u_models.Areas.objects.get(areaid=area).area
    user = u_models.Passport.objects.get(pk=request.session.get("loginUser").id)
    s1 = transaction.savepoint()
    # 删除之前的默认
    try:
        former_address = u_models.Address.objects.get(passport=user, is_default=True)
        former_address.is_default = False
        former_address.save()
        transaction.savepoint_commit(s1)
    except:
        transaction.rollback(s1)
    s2 = transaction.savepoint()
    try:
        add = u_models.Address(passport=user, province=province, city=city, area=area, desc=desc, is_default=True)
        add.save()
        transaction.savepoint_commit(s2)
    except:
        transaction.rollback(s2)
    provinces = u_models.Provinces.objects.all()
    address = u_models.Address.objects.filter(passport=user)
    content = {"provinces": provinces, "address": address}
    return render(request, "order/make_order.html", content)


@transaction.atomic
@utils.requirelogin
def success(request):
    # 对数据库进行处理，完成后进入支付成功页面
    #  生成order，对sale进行累加
    #  要接收地址
    user = u_models.Passport.objects.get(pk=request.session.get("loginUser").id)
    address_id = int(request.POST.get("address"))
    print(type(address_id))
    address = u_models.Address.objects.get(pk=address_id)
    shopcarts = request.session.get("shopcarts")
    count = 0
    for i in shopcarts:
        count += i.count
    s1 = transaction.savepoint()
    try:
        order = o_models.OrderInfo(passport=user, addr=address)
        order.save()
        transaction.savepoint_commit(s1)
    except:
        transaction.rollback(s1)
    s2 = transaction.savepoint()
    try:
        for i in shopcarts:
            i.books.sales += i.count
            i.books.save()
            goods = o_models.OrderGoods(goods=i.books, count=i.count, order=order, total_price=i.allTotal)
            goods.save()
            order.total_count += i.count
            order.total_price += goods.total_price
            order.save()
            request.session["carts_count"] = request.session.get("carts_count") - 1
            i.delete()
        transaction.savepoint_commit(s2)
    except:
        transaction.rollback(s2)
    # city = request.POST.get("city")
    return render(request, "order/success.html")


@utils.requirelogin
def order_list(request):
    pageNow = int(request.GET.get("pageNow", 1))
    user = u_models.Passport.objects.get(pk=request.session.get("loginUser").id)
    orders = o_models.OrderInfo.objects.filter(passport=user).order_by("-order_id")
    order_goods = []
    for i in orders:
        goods = o_models.OrderGoods.objects.filter(order=i).order_by("-id")
        order_goods.append(goods)
    # 每页显示的条数
    pageSize = 4
    # 获取分页对象
    paginator = Paginator(order_goods, pageSize)
    # 获取分页对象的列表，参数是当前页码
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
    return render(request, "order/order_list.html",
                  {"page": page, "pageSize": pageSize, "pages": pages, "num_pages": num_pages})


def getCity(request):
    province = request.POST.get("provinceid")
    cities = u_models.Cities.objects.all()
    dict = {}
    for i in cities:
        if i.provinceid == province:
            dict[i.cityid] = i.city
    return JsonResponse(dict, content_type="application/json")


def getArea(request):
    city = request.POST.get("cityid")
    areas = u_models.Areas.objects.all()
    dict = {}
    for i in areas:
        if i.cityid == city:
            dict[i.areaid] = i.area
    return JsonResponse(dict, content_type="application/json")

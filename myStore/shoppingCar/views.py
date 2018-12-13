from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from books import models
from users import models as u_models
import utils
from shoppingCar import models as s_models
from django.http import HttpResponse
from django.db import transaction


# Create your views here.
@transaction.atomic
@utils.requirelogin
def add(request):
    g_id = request.POST.get("g_id")
    count = request.POST.get("count")
    # 获得商品
    goods = models.Books.objects.filter(pk=g_id).first()
    # 算钱
    allTotal = int(goods.price) * int(count)
    # 获得购物车对象
    user = u_models.Passport.objects.get(pk=request.session.get("loginUser").id)
    shopcarts = s_models.ShopCart.objects.filter(user=user)
    # 购物车中有多少类商品
    carts_count = len(shopcarts)
    s=transaction.savepoint()
    try:
        if carts_count == 0:
            shopcart = s_models.ShopCart(books=goods, count=count, allTotal=allTotal, user=user)
            shopcart.save()
            carts_count += 1
        # 获取每一类商品
        for shopcart1 in shopcarts:
            # 商品已存在
            if shopcart1.books == goods:
                shopcart1.allTotal += allTotal
                shopcart1.count += int(count)
                shopcart1.save()
                break
            #     商品之前不存在
            else:
                shopcart = s_models.ShopCart(books=goods, count=count, allTotal=allTotal, user=user)
                shopcart.save()
                carts_count += 1
                break
        transaction.savepoint_commit(s)
    except:
        transaction.rollback(s)
    request.session["carts_count"] = carts_count
    # print(request.session["carts_count"])
    return HttpResponse("success")


@utils.requirelogin
def list(request):
    pageNow = int(request.GET.get("pageNow", 1))
    user = u_models.Passport.objects.get(pk=request.session.get("loginUser").id)
    # 获取用户购物车类的所有项
    shopcarts = s_models.ShopCart.objects.filter(user=user).order_by("-addTime")
    # 每页显示的条数
    pageSize = 4
    # 获取分页对象
    paginator = Paginator(shopcarts, pageSize)
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
    return render(request, "shoppingCar/list.html",
                  {"page": page, "pageSize": pageSize, "pages": pages, "num_pages": num_pages})

@transaction.atomic
@utils.requirelogin
def delete(request):
    sc_id = request.POST.get("sc_id")
    print(sc_id)
    s=transaction.savepoint()
    if sc_id:
        try:
            shopcart = s_models.ShopCart.objects.get(pk=sc_id)
            shopcart.delete()
            transaction.savepoint_commit(s)
        except:
            transaction.rollback(s)
        count=request.session["carts_count"]
        request.session["carts_count"]=count-1
        return HttpResponse("删除成功~")
    else:
        return HttpResponse("删除失败~")

@transaction.atomic
@utils.requirelogin
def confirm(request):
    # print("confirm")
    shopcarts = []
    # print(request.POST)
    s=transaction.savepoint()
    try:
        for key in request.POST:
            print(request.POST[key])
            count=int(request.POST[key])
            shopcart_id = int(key)
            shopcart = s_models.ShopCart.objects.get(pk=shopcart_id)
            shopcart.count=count
            books_id = shopcart.books_id
            books=models.Books.objects.get(pk=books_id)
            # 更新单种商品总价
            shopcart.allTotal = books.price * count
            shopcart.save()
            shopcarts.append(shopcart)
            # number = books.sales + int(request.POST.get(key))
            # books.sales = number
            # books.save()
        transaction.savepoint_commit(s)
    except:
        transaction.rollback(s)
    # print(shopcarts)
    request.session["shopcarts"] = shopcarts
    return HttpResponse("成功".encode("utf-8"))

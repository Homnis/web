from django.shortcuts import render
import utils, verify, logging
from io import BytesIO
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.db import transaction

from books import models
from users import models as u_models
from comments import models as c_models

logger = logging.getLogger('django.request')


# Create your views here.


# 主页

# @cache_page(60 * 15)
def index(request):
    '''显示首页'''

    # 定义模板上下文
    request.session.set_expiry(0)
    context = utils.getIndex()
    # 使用模板
    if 'username' in request.session:
        logger.info(request.session["username"])
    else:
        logger.info('anonymous')
    print(context)
    return render(request, 'books/index.html', context)


def code(request):
    filename, code = verify.create_code()
    request.session['code'] = code
    f = BytesIO()
    filename.save(f, "PNG")
    return HttpResponse(f.getvalue(), "image/png")


def details(request, id):
    book = models.Books.objects.get(pk=id)
    # 所有图片
    goodsImages = models.BooksImage.objects.filter(books=book)
    # 评论
    # comments = c_models.Comments.objects.filter(book=book)
    # 默认图片
    defaultImg = book.image
    provinces = u_models.Provinces.objects.all()
    comments = c_models.Comments.objects.filter(book=book).order_by("-pub_time")
    # 每页显示的条数
    pageSize = 4
    # 获取分页对象
    paginator = Paginator(comments, pageSize)
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
    return render(request, "books/details.html",
                  {"page": page, "pageSize": pageSize, "pages": pages, "num_pages": num_pages, "goods": book,
                   "de_img": defaultImg,"goods_images": goodsImages, "provinces": provinces})


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


def list(request):
    goods = models.Books.objects.all()
    # 评论
    # comments = c_models.Comments.objects.filter(book=book)
    # 每页显示的条数
    pageSize = 10
    # 获取分页对象
    paginator = Paginator(goods, pageSize)
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
    return render(request, "books/list.html",
                  {"page": page, "pageSize": pageSize, "pages": pages, "num_pages": num_pages})
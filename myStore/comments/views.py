from django.shortcuts import render, redirect
from comments import models
from books import models as b_models
from django.db import transaction


# Create your views here.
@transaction.atomic
def add(request):
    '''
    TODO:create comments
    :param request:
    :return:
    '''
    comment = request.POST["comment"]
    user = request.session.get("loginUser")
    goods_id = request.POST["goods"]
    goods = b_models.Books.objects.get(pk=goods_id)
    level = request.POST["level"]
    title = request.POST["title"]
    # print(type(user))
    # print(type(goods))
    # print(comment)
    # print(level)
    # print(title)
    s_id = transaction.savepoint()
    try:
        comments = models.Comments(user=user, book=goods, content=comment, title=title, rating=level)
        comments.save()
        transaction.savepoint_commit(s_id)
    except:
        transaction.rollback(s_id)
    return redirect("/details/{id}/".format(id=goods_id))

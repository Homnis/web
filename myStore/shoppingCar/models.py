from django.db import models
from books.models import Books
from users.models import Passport
# Create your models here.
class ShopCart(models.Model):
    id = models.AutoField(primary_key=True)
    # 商品
    books = models.ForeignKey(Books, on_delete=models.CASCADE, verbose_name="购物车商品")
    # 商品数量
    count = models.IntegerField(verbose_name="商品数量")
    # 商品添加时间
    addTime = models.DateTimeField(auto_now_add=True, verbose_name="商品添加时间")
    # 商品小计金额
    allTotal = models.FloatField(verbose_name="商品小计金额")
    # 购物车所属用户
    user = models.ForeignKey(Passport, on_delete=models.CASCADE, verbose_name="购物车所属用户")
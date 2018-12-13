from django.db import models
from .constant import *
from tinymce.models import HTMLField
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

fs = FileSystemStorage(location=os.path.join(settings.BASE_DIR, 'static'))


# Create your models here.
class Books(models.Model):

    id = models.AutoField(primary_key=True)
    type_id = models.IntegerField(default=NOVEL, verbose_name='商品种类')
    name = models.CharField(max_length=20, verbose_name='商品名称')
    desc = models.CharField(max_length=128, verbose_name='商品简介')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    stock = models.IntegerField(default=1, verbose_name='商品库存')
    sales = models.IntegerField(default=0, verbose_name='商品销量')
    detail = HTMLField(verbose_name='商品详情')
    image = models.ImageField(storage=fs, upload_to='books', verbose_name='商品图片')
    status = models.IntegerField(default=ONLINE, verbose_name='商品状态')

    class Meta:
        db_table = 's_books'


class BooksImage(models.Model):
    id = models.AutoField(primary_key=True)
    # 商品的图片存储路径
    image = models.ImageField(storage=fs, upload_to='books', verbose_name='商品图片')
    # 是否显示这个图片
    status = models.BooleanField(default=False, verbose_name="是否默认显示该图片")
    # 外键， 所属的产品
    books = models.ForeignKey(Books, on_delete=models.CASCADE, verbose_name="所属商品")

    class Meta:
        db_table = 'books_img'

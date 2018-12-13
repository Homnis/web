from django.db import models
from users.models import Passport, Address
from books.models import Books


# Create your models here.


class OrderInfo(models.Model):
    order_id = models.AutoField(max_length=64, primary_key=True, verbose_name='订单编号')
    passport = models.ForeignKey(Passport, verbose_name='下单账户', on_delete=models.CASCADE)
    addr = models.ForeignKey(Address, verbose_name='收货地址', on_delete=models.CASCADE)
    total_count = models.IntegerField(default=0, verbose_name='商品总数')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name='商品总价')
    transit_price = models.DecimalField(max_digits=10, decimal_places=2, default=10,verbose_name='订单运费')

    class Meta:
        db_table = 's_order_info'

class OrderGoods(models.Model):
    id = models.AutoField(max_length=64, primary_key=True, verbose_name='订单中商品编号')
    goods = models.ForeignKey(Books, verbose_name='商品', on_delete=models.CASCADE)
    count = models.IntegerField(default=1, verbose_name='商品总数')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品总价')
    order = models.ForeignKey(OrderInfo, verbose_name='归属订单', on_delete=models.CASCADE)

    class Meta:
        db_table = 'order_goods'

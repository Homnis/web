from django.db import models
from _datetime import datetime


# Create your models here.
class Passport(models.Model):
    '''用户模型类'''
    id = models.AutoField(primary_key=True, verbose_name="用户id")
    username = models.CharField(max_length=20, verbose_name='用户名称')
    password = models.CharField(max_length=40, verbose_name='用户密码')
    email = models.EmailField(default="",verbose_name='用户邮箱')
    tel = models.CharField(max_length=11,default="",verbose_name="电话")
    avatar = models.ImageField(upload_to="static/img/users/", default="", verbose_name="用户头像")
    is_active = models.BooleanField(default=False, verbose_name='激活状态')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    is_manager = models.BooleanField(default=False, verbose_name='管理员')

    class Meta:
        db_table = 'user_account'


class Address(models.Model):
    '''地址模型类'''
    id = models.AutoField(primary_key=True)
    # 收货人
    recv_name = models.CharField(max_length=100, default="", verbose_name="收货人")
    # 收货人的电话号码
    recv_tel = models.CharField(max_length=20, default="", verbose_name="收货人的电话号码")
    # 收货人的省份
    province = models.CharField(max_length=100, default="", verbose_name="收货人的省份")
    # 城市
    city = models.CharField(max_length=100, default="", verbose_name="收货人的城市")
    # 县区
    area = models.CharField(max_length=100, default="", verbose_name="收货人的县区")
    # 街道
    street = models.CharField(max_length=255, default="", verbose_name="收货人的街道")
    # 描述
    desc = models.CharField(max_length=255, default="", verbose_name="详细地址")
    # 是否是默认地址
    is_default = models.BooleanField(default=False, verbose_name="是否是默认地址")
    passport = models.ForeignKey(Passport, verbose_name='账户', on_delete=models.CASCADE, )

    class Meta:
        db_table = 'user_address'


# 建立城市自关联数据库表
class Provinces(models.Model):
    id = models.AutoField(primary_key=True)
    provinceid = models.CharField(max_length=50, verbose_name="省份ID")
    province = models.CharField(max_length=50, verbose_name="省份")

    class Meta:
        db_table = 'province'  # 指定表名称


class Cities(models.Model):
    id = models.AutoField(primary_key=True)
    cityid = models.CharField(max_length=50, verbose_name="城市ID")
    city = models.CharField(max_length=50, verbose_name="城市")
    provinceid = models.CharField(max_length=50, verbose_name="省份ID")

    class Meta:
        db_table = 'cities'  # 指定表名称


class Areas(models.Model):
    id = models.AutoField(primary_key=True)
    areaid = models.CharField(max_length=50, verbose_name="区域ID")
    area = models.CharField(max_length=50, default="", verbose_name="区域")
    cityid = models.CharField(max_length=50, verbose_name="城市ID")

    class Meta:
        db_table = 'areas'  # 指定表名称

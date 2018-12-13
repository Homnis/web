from datetime import datetime

from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="用户id")
    username = models.CharField(max_length=100, unique=True, verbose_name="用户名")
    password = models.CharField(max_length=255, verbose_name="密码")
    nickname = models.CharField(max_length=255, default="普通用户", verbose_name="用户昵称")
    age = models.IntegerField(default=18, verbose_name="年龄")
    gender = models.CharField(max_length=10, default="女", verbose_name="性别")
    email = models.CharField(max_length=255, null=True, blank=True, verbose_name="邮箱")


class Article(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="文章id")
    title = models.CharField(max_length=100, verbose_name="文章标题")
    content = models.TextField(verbose_name="文章内容")
    publishTime = models.DateTimeField(auto_now_add=True)
    modifyTime = models.DateTimeField(auto_now=True)
    # 文章作者，也就是用户对象
    author = models.ForeignKey(User, on_delete=models.CASCADE)

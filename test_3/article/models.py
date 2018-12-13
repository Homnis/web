from datetime import datetime

from django.db import models

from tinymce import models as t_models


class User(models.Model):
    """
        博客用户类
    """
    id = models.AutoField(primary_key=True, verbose_name="用户主键")
    username = models.CharField(max_length=100, unique=True, verbose_name="用户名称")
    password = models.CharField(max_length=255, verbose_name="用户密码")
    nickname = models.CharField(max_length=255, default="普通用户", verbose_name="用户昵称")
    age = models.IntegerField(default=18, verbose_name="用户年龄")
    gender = models.CharField(max_length=10, default="女", verbose_name="用户性别")
    email = models.CharField(max_length=255, null=True, blank=True, verbose_name="用户邮箱")
    avatar = models.ImageField(upload_to="static/img/", default="static/article/img/default.gif", verbose_name="用户头像")
    tel = models.CharField(max_length=50, default="110", verbose_name="用户头像")


class Article(models.Model):
    """ 文章类"""
    id = models.AutoField(primary_key=True, verbose_name="文章主键")
    title = models.CharField(max_length=100, verbose_name="文章标题")
    content = t_models.HTMLField(verbose_name="文章内容")
    remark = models.CharField(max_length=255, default="", verbose_name="文章摘要")
    publishTime = models.DateTimeField(auto_now_add=True, verbose_name="文章发表时间")
    modifyTime = models.DateTimeField(auto_now=True, verbose_name="文章修改时间")
    count = models.IntegerField(default=0, verbose_name="文章点击量")
    # 文章作者，也就是用户对象
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-publishTime"]

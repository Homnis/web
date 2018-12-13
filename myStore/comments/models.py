from django.db import models
from users.models import Passport
from books.models import Books


# Create your models here.
class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    disabled = models.BooleanField(default=False, verbose_name="禁用评论")
    user = models.ForeignKey(Passport, verbose_name="用户", on_delete=models.CASCADE, )
    book = models.ForeignKey(Books, verbose_name="书籍", on_delete=models.CASCADE, )
    content = models.CharField(max_length=1000, verbose_name="评论内容")
    title = models.CharField(max_length=20, verbose_name="评论标题", default="")
    rating = models.IntegerField(default=1, verbose_name="评分")
    # 发表时间
    pub_time = models.DateTimeField(auto_now_add=True, verbose_name="发表时间")

    class Meta:
        db_table = 'comments'

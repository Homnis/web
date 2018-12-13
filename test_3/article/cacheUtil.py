from django.core.cache import cache
from . import models

def getAllArticle(ischange=False):
    print("开始查询数据……")
    ats = cache.get("allArtcles")
    if ats is None or ischange:
        print("缓存中没有数据，需要数据库中获取……")
        ats = models.Article.objects.all().order_by("-publishTime")
        print("从数据库中获取数据成功，保存到缓存中……")
        cache.set("allArtcles", ats)
        # print(ats)
    return ats
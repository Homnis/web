from django.core.cache import cache
from . import models

def getAllArticle(ischange=False):
    ats = cache.get("allArtcles")
    if ats is None or ischange:
        ats = models.Article.objects.all().order_by("-publishTime")
        cache.set("allArtcles", ats)
    return ats
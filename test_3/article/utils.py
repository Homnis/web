from django.shortcuts import render
from io import BytesIO
import hmac,re

from . import verify

"""
工具模块
"""


# 判断用户是否登录
def requirelogin(fn):
    def inner(request, *args, **kwargs):
        if request.session.has_key("loginUser"):
            # 此时用户登录了，正常运行，我们不参与
            return fn(request, *args, **kwargs)
        else:
            return render(request, "article/login.html", {"msg": "你没有登录，该页面需要登录，请先登录！！"})

    return inner


def md5_by_hmac(key):
    md5 = hmac.new(key.encode("utf-8"), "password".encode("utf-8"), "MD5")
    return md5.hexdigest()



def removeHTMLByRE(content):
    """
     使用正则表达式去除字符串中的HTML标签
    :param content: 需要去除HTML的字符串
    :return:  无HTML的字符串
    """
    pattern = r"</?(.*?)>"
    return re.sub(pattern, "", content)
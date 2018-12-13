import hashlib
import hmac
import random
import string
import re
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from django.shortcuts import render
# from mysite import settings
from django.conf import settings

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
            return render(request, "blog/login.html", {"msg": "你没有登录，该页面需要登录，请先登录！！"})
    return inner


def md5_by_hashlib(key):
    """
    使用hashlib模块总md5加密方式加密，盐值是setting文件中的SALT_KEY
    """
    md5 = hashlib.md5(key.encode("utf-8"))
    md5.update(settings.SALT_KEY.encode("utf-8"))
    return md5.hexdigest()


def md5_by_hmac(key):
    md5 = hmac.new(key.encode("utf-8"), settings.SALT_KEY.encode("utf-8"), "MD5")
    return md5.hexdigest()


def getRandomChar(count=4):
    # 生成随机字符串
    # string模块包含各种字符串，以下为小写字母加数字
    ran = string.ascii_lowercase+ string.ascii_uppercase + string.digits
    char = ''
    for i in range(count):
        char += random.choice(ran)
    return char


# 返回一个随机的RGB颜色
def getRandomColor():
    return (random.randint(50,150),random.randint(50,150),random.randint(50,150))


def create_code():
    # 创建图片，模式，大小，背景色
    img = Image.new('RGB', (120,30), (255,255,255))
    #创建画布
    draw = ImageDraw.Draw(img)
    # 设置字体
    font = ImageFont.truetype('arial.ttf', 25)

    code = getRandomChar()
    # 将生成的字符画在画布上
    for t in range(4):
        draw.text((30*t+5,0),code[t],getRandomColor(),font)

    # 生成干扰点 增加识别的难度
    for _ in range(random.randint(0,100)):
        # 位置，颜色
        draw.point((random.randint(0, 120), random.randint(0, 30)), fill=getRandomColor())

    # 使用模糊滤镜使图片模糊
    img = img.filter(ImageFilter.BLUR)
    return img,code


def removeHTMLByRE(content):
    """
     使用正则表达式去除字符串中的HTML标签
    :param content: 需要去除HTML的字符串
    :return:  无HTML的字符串
    """
    pattern = r"</?(.*?)>"
    return re.sub(pattern, "", content)
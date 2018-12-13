from django.shortcuts import render
import hmac, re, hashlib, random, time
from urllib import request, parse
from django.core.cache import cache
from books import models

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
            return render(request, "users/login.html", {"msg": "你没有登录，该页面需要登录，请先登录！！"})

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


"""网易云手机验证码API测试"""


class ServerAPI(object):
    """
     * 参数初始化
     * @param AppKey
     * @param AppSecret
    """

    def __init__(self):
        self.AppKey = ''  # 开发者平台分配的AppKey
        self.AppSecret = ''  # 开发者平台分配的AppSecret,可刷新
        self.CheckSum = ''
        self.CurTime = ''
        self.Nonce = ''  # 随机字符串最大128个字符，也可以小于该数

    def checkSumBuilder(self):
        """
             * API checksum校验生成
             * @param  void
             * @return CheckSum(对象私有属性)
        """
        charHex = '0123456789abcdef'

        for i in range(0, 10):
            index = random.randint(0, 10)
            self.Nonce += charHex[index]

        self.CurTime = int(time.time())  # 当前UTC时间戳，从1970年1月1日0点0 分0 秒开始到现在的秒数(String)
        join_string = self.AppSecret + self.Nonce + str(self.CurTime)

        self.CheckSum = hashlib.sha1(join_string.encode('utf-8')).hexdigest()
        # SHA1(AppSecret + Nonce + CurTime),三个参数拼接的字符串，进行SHA1哈希计算，转化成16进制字符(String，小写)

    def postDataHttps(self, url, data):
        """
             * 使用urllib2发送post请求
             * @param  url     [请求地址]
             * @param  data    [array格式数据]
             * @return 请求返回结果(array)
        """
        self.checkSumBuilder()
        headers = {
            'AppKey': self.AppKey,
            'Nonce': self.Nonce,
            'CurTime': self.CurTime,
            'CheckSum': self.CheckSum,
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        }
        postdata = data

        req = request.Request(url, parse.urlencode(postdata).encode(encoding='UTF8'), headers=headers)
        res_data = request.urlopen(req)
        resp = res_data.read()
        return eval(resp)

    def sendSmsCode(self, mobile, deviceId=''):
        """
             * 发送短信验证码
             * @param  mobile       [目标手机号]
             * @param  deviceId     [目标设备号，可选参数]
             * @return result      [返回python dict 对象]
        """
        url = 'https://api.netease.im/sms/sendcode.action'
        data = dict({
            'mobile': mobile,
            'deviceId': deviceId
        })
        return self.postDataHttps(url, data)


# redis 缓存
def getIndex():
    # 首页图书列表
    sale_list = cache.get("sale_list")
    print("缓存中没有数据，从数据库中查询")
    sale_list = models.Books.objects.all().order_by("-sales")[:5]
    cache.set("sale_list", sale_list, timeout=180)
    context = {
        "sale_list": sale_list,
    }
    return context

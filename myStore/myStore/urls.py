"""bookstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
import xadmin
from xadmin.plugins import xversion
xadmin.autodiscover()
xversion.register_models()

urlpatterns = [
    # url('admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^users/', include('users.urls', namespace='users')),  # 用户模块
    url(r'^tinymce/', include('tinymce.urls')),  # 富文本编辑器
    url(r'^', include('books.urls', namespace='books')),  # 商品模块
    url(r'^shoppingCar/', include('shoppingCar.urls', namespace='shoppingCar')),  # 购物车模块
    url(r'^order/', include('order.urls', namespace='order')),  # 订单模块
    url(r'^comment/', include('comments.urls', namespace='comment')),  # 评论模块
    url(r'^search/', include('haystack.urls')),  # 搜索配置
]

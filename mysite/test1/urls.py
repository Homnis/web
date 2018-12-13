from django.conf.urls import url

from . import views


urlpatterns=[
    url(r'^index/$',views.index,name="index"),
    url(r'^login/$',views.login,name="login"),
    url(r'^reg/$',views.reg,name="reg"),
    url(r'^baidu/$',views.baidu,name="baidu"),
    url(r'^myHtml/$',views.myHtml,name="myHtml")
]
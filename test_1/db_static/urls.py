from django.conf.urls import url
from . import models,views

app_name="db_static"
urlpatterns=[
    url(r'^home/$',views.home,name="home"),
    url(r'^reg/$',views.reg,name="reg"),
    url(r"^doReg/$", views.doReg, name="doReg"),
    url(r'^login/$', views.login, name="login"),
    url(r'^doLogin/$', views.doLogin, name="doLogin"),
    url(r'^info/$', views.info, name="info"),
    url(r'^changeInfo/$',views.changeInfo,name="changeInfo"),
    url(r'^doChangeInfo/$', views.doChangeInfo, name="doChangeInfo"),
    url(r'^changePsw/$',views.changePsw,name="changePsw"),
    url(r'^doChangePsw/$',views.doChangePsw,name="doChangePsw"),
    url(r'^users/$',views.users,name="users"),
    url(r'^delete/$', views.delete, name="delete"),
    url(r'^doDelete/$', views.doDelete, name="doDelete"),
]
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^index/$', views.index, name="index"),
    url(r'^login/$', views.login, name="login"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^user_list/$', views.user_list, name="user_list"),
    url(r'^register/$', views.register, name="register"),
    url(r'^user_update/$', views.user_update, name="user_update"),
    url(r'^do_update/$', views.do_update, name="do_update"),
    url(r'^user_info/$', views.user_info, name="user_info"),
    url(r'^user_delete/$', views.user_delete, name="user_delete"),
    url(r'^test/$', views.test, name="test"),
]
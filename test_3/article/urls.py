from django.conf.urls import url

from . import views

app_name = "article"

urlpatterns = [
    url(r'^index/$', views.index, name="index"),
    url(r'^register/$', views.register, name="register"),
    url(r'^login/$', views.login, name="login"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^psw_update/$', views.psw_update, name="psw_update"),
    url(r'^upload_avatar/$', views.upload_avatar, name="upload_avatar"),

    url(r'^user_list/$', views.user_list, name="user_list"),
    url(r'^user_update/$', views.user_update, name="user_update"),
    url(r'^user_info/$', views.user_info, name="user_info"),
    url(r'^(?P<user_id>\d+)/user_delete/$', views.user_delete, name="user_delete"),

    url(r"^article_add/$", views.article_add, name="article_add"),
    url(r"^article_delete/(?P<a_id>\d+)/$", views.article_delete, name="article_delete"),
    url(r"^article_update/(?P<a_id>\d+)/$", views.article_update, name="article_update"),
    url(r"^article_detail/(?P<a_id>\d+)/$", views.article_detail, name="article_detail"),
    url(r"^article_list/$", views.article_list, name="article_list"),
    url(r"^code/$", views.code, name="code"),
]

from django.conf.urls import url
from users import views

app_name = "users"
urlpatterns = [
    # url(r'^index/$', views.index, name="index"),
    url(r'^register/$', views.register, name="register"),
    url(r'^address/$', views.address, name="address"),
    url(r'^setAddress/$', views.setAddress, name="setAddress"),
    url(r'^addressList/$', views.addressList, name="addressList"),
    url(r'^regAddress/$', views.regAddress, name="regAddress"),
    url(r'^checktel/$', views.checktel, name="checktel"),
    url(r'^checkemail/$', views.checkemail, name="checkemail"),
    url(r'^send_message/$', views.send_message, name="send_message"),
    url(r'^register_email/$', views.register_email, name="register_email"),
    url(r"^active/(?P<token>.*)/$", views.active, name="active"),
    url(r'^login/$', views.login, name="login"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^psw_update/$', views.psw_update, name="psw_update"),
    # url(r'^upload_avatar/$', views.upload_avatar, name="upload_avatar"),
    url(r"^code/$", views.code, name="code"),
    url(r"^agree/$", views.agree, name="agree"),
    url(r'^user_update/$', views.user_update, name="user_update"),
    # url(r'^user_info/$', views.user_info, name="user_info"),
    url(r'^manage/$', views.manage, name="manage"),
    url(r'^book_list/$', views.book_list, name="book_list"),
    url(r'^book_update/(?P<id>\d+)/$', views.book_update, name="book_update"),
    url(r'^book_delete/(?P<id>\d+)/$', views.book_delete, name="book_delete"),
    url(r'^book_doUpdate/$', views.book_doUpdate, name="book_doUpdate"),
    # url(r'^address/$', views.address, name="address"),
]
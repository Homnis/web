from django.conf.urls import url
from . import models,views


urlpatterns=[
    url(r'^index/$',views.index,name="index"),
    url(r'^add/$',views.add,name="add"),
    url(r"^doAdd/$", views.doAdd, name="doAdd"),
    url(r'^showAllToDelete/$',views.showAllToDelete,name="showAllToDelete"),
    url(r'^delete/$',views.delete,name="delete"),
    url(r'^showAllToChange/$',views.showAllToChange,name="showAllToChange"),
    url(r'^showUserToChange/$', views.showUserToChange, name="showUserToChange"),
    url(r'^change/$',views.change,name="change"),
    url(r'^howToSearch/$',views.howToSearch,name="howToSearch"),
    url(r'^search/$',views.search,name="search")
]
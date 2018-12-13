from django.conf.urls import url
from books import views

app_name = "books"
urlpatterns = [
    url(r"^code/$", views.code, name="code"),
    url(r"^list/$", views.list, name="list"),
    url(r"^details/(?P<id>\d+)/$", views.details, name="details"),
    url(r"^getCity/$", views.getCity, name="getCity"),
    url(r"^getArea/$", views.getArea, name="getArea"),
    url(r"^$", views.index, name="index"),
]
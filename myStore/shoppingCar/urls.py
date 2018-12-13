from django.conf.urls import url
from shoppingCar import views

app_name = "shoppingCar"

urlpatterns = [
    url(r'^list/$', views.list, name="list"),
    url(r'^add/$', views.add, name="add"),
    url(r'^delete/$', views.delete, name="delete"),
    url(r'^confirm/$', views.confirm, name="confirm"),

]
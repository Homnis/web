from django.conf.urls import url
from order import views
app_name = "order"
urlpatterns = [
    url(r'^make_order/$', views.make_order, name="make_order"),
    url(r'^order_list/$', views.order_list, name="order_list"),
    url(r'^success/$', views.success, name="success"),
    url(r'^createAddress/$', views.createAddress, name="createAddress"),
]
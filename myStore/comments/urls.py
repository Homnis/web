from django.conf.urls import url
from comments import views
app_name = "comments"
urlpatterns = [
    url(r"^add/$", views.add, name="add"),
]
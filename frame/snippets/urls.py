from django.conf.urls import url
from . import views
app_name = "snippets"
urlpatterns = [
    url(r"^snippets/$", views.snippet_list.as_view(), name="snippet_list"),
    url(r"^snippets(?P<id>\d+)/$", views.snippet_detail, name="snippet_detail"),
]
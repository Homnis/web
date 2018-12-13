from django.contrib import admin

from .models import User
from .models import Article

admin.site.register(User)
admin.site.register(Article)
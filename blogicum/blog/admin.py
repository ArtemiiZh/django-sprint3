from django.contrib import admin

from .models import Category, Location, Post

# Самый простой способ зарегистрировать модели в админке:
admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Post)

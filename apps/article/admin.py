from django.contrib import admin

from article.models import Category, Tag, Post
# Register your models here.


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post)

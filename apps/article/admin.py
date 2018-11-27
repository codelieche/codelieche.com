from django.contrib import admin

from article.models import Category, Tag, Post, Image
# Register your models here.


class CategoryModelAdmin(admin.ModelAdmin):
    """Category Model Admin"""
    list_display = ("id", "slug", "name", "parent")
    list_filter = ("parent",)


class TagModelAdmin(admin.ModelAdmin):
    """Tag Model Admin"""
    list_display = ("id", "slug", "name")


class PostModelAdmin(admin.ModelAdmin):
    """Post Model Admin"""
    list_display = ("id", "category", "title", "author", "time_added", "time_updated")
    list_filter = ("author", "category")


class ImageModelAdmin(admin.ModelAdmin):
    """Image Model Admin"""
    list_display = ("id", "filename", "url", "user", "time_added")
    list_filter = ("user",)


admin.site.register(Category, CategoryModelAdmin)
admin.site.register(Tag, TagModelAdmin)
admin.site.register(Post, PostModelAdmin)
admin.site.register(Image, ImageModelAdmin)

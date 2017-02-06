#coding:utf-8
from django.contrib import admin
from django import forms
from .models import Category, Post, Comment, Tag, Upload
# Register your models here.

class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug']
    list_display_links = ['id', 'slug']
    ordering = ['id']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'title', 'content', 'author', 'status',
                  'top', 'good', 'deleted', 'tags']
        widgets = {
            # 'content': forms.
        }

class PostModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'created', 'status', 'top', 'good']
    # list_display_links = ['title', 'author']
    list_display_links = ['title']
    ordering = ['status', '-created']
    list_filter = ('status', 'author', 'category', 'tags')
    search_fields = ('title', 'content')
    list_editable = ['status']
    date_hierarchy = 'created'
    raw_id_fields = ('author',)

    # 后台增加文章的时候，content_html是不需要的，所以要自定义form
    form = PostForm


    class Media:
        css = {
            'all': (
                # '/static/libs/editor/css/editor.css',
                '/static/css/main.css',
            )
        }

# 评论模型管理
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'created', 'active']
    list_filter = ('active', 'created')
    search_fields = ('content',)

    # class Media :
    #     js = (
    #         '/static/libs/editor/js/editor.js',
    #         '/static/libs/editor/js/marked.js',
    #         '/static/js/admin.js'
    #     )
    #     css = {
    #         'all':(
    #             '/static/libs/editor/css/editor.css',
    #         )
    #     }

# 上传的图片管理模型
class UploadModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'filename', 'created', 'deleted']
    ordering = ['-created']

class TagModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'hot']
    list_display_links = ['id', 'slug']
    # list_editable = ['hot']
    ordering = ['-hot', 'id']

admin.site.register(Category, CategoryModelAdmin)
admin.site.register(Post, PostModelAdmin)
admin.site.register(Comment, CommentModelAdmin)
admin.site.register(Tag, TagModelAdmin)
admin.site.register(Upload, UploadModelAdmin)

# 卸载掉taggit标签的管理
# admin.site.unregister(Taggit_Tag)

#coding=utf-8
from django.conf.urls import url
from . import views

app_name = "article"

urlpatterns = [
    #文章首页
    url(r'^$', views.index, name="index"),
    url(r'category/(?P<category_slug>[\w\d]+)', views.post_category_list,
        name="post_category_list"),
    url(r'^tags/(?P<tag_name>[\w\d\-]+)', views.post_tag_list, name="post_tag_list"),
    url(r'^article/(?P<pk>\d+)$', views.post_detail, name="post_detail"),
    url(r"article/create$", views.create, name="create"),
    url(r"article/save", views.save, name="save"),
    url(r"article/(?P<pk>\d+)/editor$", views.editor, name="editor"),
    url(r"article/upload", views.upload_image, name="upload"),
]
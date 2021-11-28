# -*- coding:utf-8 -*-
from django.urls import path, re_path

from article.views.pages import article
app_name = "article"

urlpatterns = [
    # 前缀：/article/
    re_path(r'^tag/(?P<tag_name>[\w\d\-]+)/(?P<page>\d+)?/?', article.ArticleTagListView.as_view(), name="tag_list"),
    # path('tag/(<str:tag_name>/<int:page>)', article.ArticleTagListView.as_view(), name="tag_list"),
    # 文章详情页
    path('<int:pk>', article.PostDetailView.as_view(), name="detail"),
    # 创建文章
    path("create", article.create, name="create"),
    # 创建文章保存
    path("save", article.save, name="save"),
    # 编辑文章
    path("<int:pk>/editor", article.editor, name="editor"),
    # 上传图片
    path("upload", article.upload_image, name="upload"),

]

# -*- coding:utf-8 -*-
from django.conf.urls import url
from ..views import article
app_name = "article"

urlpatterns = [
    # 标签文章列表页
    url(r'^tag/(?P<tag_name>[\w\d\-]+)/(?P<page>\d+)?/?',
        article.ArticleTagListView.as_view(), name="tag_list"),
    # 文章详情页
    url(r'^(?P<pk>\d+)$', article.PostDetailView.as_view(), name="detail"),
    # 创建文章
    url(r"create$", article.create, name="create"),
    # 创建文章保存
    url(r"save", article.save, name="save"),
    # 编辑文章
    url(r"(?P<pk>\d+)/editor$", article.editor, name="editor"),
    # 上传图片
    url(r"upload", article.upload_image, name="upload"),
]

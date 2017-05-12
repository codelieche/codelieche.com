# -*- coding:utf-8 -*-
from django.conf.urls import url
from ..views import article
app_name = "article"

urlpatterns = [


    url(r'^tag/(?P<tag_name>[\w\d\-]+)', article.post_tag_list, name="tag_list"),
    url(r'^(?P<pk>\d+)$', article.post_detail, name="detail"),
    url(r"create$", article.create, name="create"),
    url(r"save", article.save, name="save"),
    url(r"(?P<pk>\d+)/editor$", article.editor, name="editor"),
    url(r"upload", article.upload_image, name="upload"),
]
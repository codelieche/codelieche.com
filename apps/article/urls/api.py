# -*- coding:utf-8 -*-
from django.conf.urls import url

from article.views import api

app_name = "article"

urlpatterns = [
    url(r'^post/(?P<pk>\d+)$', view=api.post_detail, name="post"),
    url(r'^post/list$', view=api.PostListView.as_view(), name="post_list"),
    url(r'^tag/(?P<pk>\d+)$', view=api.tag_detail, name="tag"),
    url(r'^tag/list$', view=api.TagListView.as_view(), name="tag_list"),
]

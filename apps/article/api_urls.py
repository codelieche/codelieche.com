# -*- coding:utf-8 -*-
from django.conf.urls import url
from . import api_views

app_name = "article"

urlpatterns = [
    url(r'^api/1.0/article/(?P<pk>\d+)$', view=api_views.post_detail, name="api_post"),
    url(r'^api/1.0/tag/(?P<pk>\d+)$', view=api_views.tag_detail, name="api_tag"),
]
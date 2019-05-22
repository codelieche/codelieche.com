# -*- coding:utf-8 -*-
"""
Weibo Api
"""
from django.urls import path, include


urlpatterns = [
    # 前缀：/api/v1/weibo/
    path("weibo/", include(arg=("weibo.urls.api.weibo", "weibo"), namespace="weibo")),
    # 评论
    path("comment/", include(arg=("weibo.urls.api.comment", "weibo"), namespace="comment")),
]

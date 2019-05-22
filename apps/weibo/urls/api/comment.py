# -*- coding:utf-8 -*-
"""
Weibo Api
"""
from django.urls import path

from weibo.views.comment import (
    CommentCreateAPIView,
    CommentListApiView,

)

urlpatterns = [
    # 前缀：/api/v1/weibo/comment/
    path("create", CommentCreateAPIView.as_view(), name="create"),
    path("list", CommentListApiView.as_view(), name="list"),
]

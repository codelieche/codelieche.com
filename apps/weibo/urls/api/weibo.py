# -*- coding:utf-8 -*-
"""
Weibo Api
"""
from django.urls import path

from weibo.views.weibo import (
    WeiboCreateAPIView,
    WeiboListAPIView,
    WeiboDetailApiView

)

urlpatterns = [
    # 前缀：/api/v1/weibo/weibo/
    path("create", WeiboCreateAPIView.as_view(), name="create"),
    path("list", WeiboListAPIView.as_view(), name="list"),
    path("<int:pk>", WeiboDetailApiView.as_view(), name="detail"),
]

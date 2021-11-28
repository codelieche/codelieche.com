# -*- coding:utf-8 -*-
from django.urls import path
from article.views.post import PostListApiView, PostCreateApiView, PostDetailApiView


urlpatterns = [
    # 前缀：/api/v1/article/post/
    path('create', PostCreateApiView.as_view(), name="create"),
    path('list', PostListApiView.as_view(), name="list"),
    path('<int:pk>', PostDetailApiView.as_view(), name="detail"),
]

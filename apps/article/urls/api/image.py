# -*- coding:utf-8 -*-
from django.urls import path
from article.views.image import ImageListApiView, ImageCreateApiView, ImageDetailApiView


urlpatterns = [
    # 前缀：/api/v1/article/image/
    path('create', ImageCreateApiView.as_view(), name="create"),
    path('list', ImageListApiView.as_view(), name="list"),
    path('<int:pk>', ImageDetailApiView.as_view(), name="detail"),
]

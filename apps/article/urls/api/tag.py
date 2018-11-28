# -*- coding:utf-8 -*-
from django.urls import path
from article.views.tag import TagListApiView, TagCreateApiView, TagDetailApiView


urlpatterns = [
    # 前缀：/api/v1/article/tag/
    path('create', TagCreateApiView.as_view(), name="create"),
    path('list', TagListApiView.as_view(), name="list"),
    path('<int:pk>', TagDetailApiView.as_view(), name="detail"),
    path('<str:slug>', TagDetailApiView.as_view(lookup_field="slug"), name="detail02"),
]

# -*- coding:utf-8 -*-
from django.urls import path
from article.views.category import CategoryListApiView, CategoryDetailApiView


urlpatterns = [
    # 前缀：/api/v1/article/category/
    path('list', CategoryListApiView.as_view(), name="list"),
    path('<int:pk>', CategoryDetailApiView.as_view(), name="detail"),
    path('<str:slug>', CategoryDetailApiView.as_view(lookup_field="slug"), name="detail02"),
]

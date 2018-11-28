# -*- coding:utf-8 -*-
from django.urls import path, re_path, include
from article.views.pages.article import IndexPageView

urlpatterns = [
    # 前缀：/
    path("", IndexPageView.as_view(), name="index"),
    re_path(r'^page/(?P<page>\d+)/?$', IndexPageView.as_view(), name="page"),
    # path('page/<int:page>', IndexPageView.as_view(), name="page"),
    path('article/', include(arg=("article.urls.pages.article", "article"), namespace="article")),
    path('category/', include(arg=("article.urls.pages.category", "article"), namespace="category"))
]

# -*- coding:utf-8 -*-
from django.urls import re_path

from article.views.pages.category import ArticleListView
app_name = "article"


urlpatterns = [
    # category list page
    # 前缀：/category/
    re_path(r'^(?P<slug>[\w\d]+)/(?P<page>\d+)?/?$', ArticleListView.as_view(), name="list")
]

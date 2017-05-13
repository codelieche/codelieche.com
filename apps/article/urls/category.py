# -*- coding:utf-8 -*-
from django.conf.urls import url

from ..views import category

urlpatterns = [
    # category list page
    url(r'^(?P<slug>[\w\d]+)/(?P<page>\d+)?/?$',
        category.ArticleListView.as_view(), name="list")
]

# -*- coding:utf-8 -*-
"""
codelieche api相关的路由
"""
from django.conf.urls import url, include

urlpatterns = [
    # article 相关的api
    url(r'^article/', include('article.urls.api', namespace='article')),
]
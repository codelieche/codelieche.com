# -*- coding:utf-8 -*-
from django.urls import path, include

urlpatterns = [
    # 前缀：/api/v1/
    # 用户账号模块api
    path('account/', include(arg=("account.urls.api.main", "account"), namespace="account")),
    # 文章模块api
    path('article/', include(arg=("article.urls.api.main", "article"), namespace="article")),
    # 问卷模块
    path('wenjuan/', include(arg=("wenjuan.urls.api.main", "wenjuan"), namespace="wenjuan")),
]

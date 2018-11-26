# -*- coding:utf-8 -*-
from django.urls import path, include

urlpatterns = [
    # 前缀：/api/v1/
    path('account/', include(arg=("account.urls.api.main", "account"), namespace="account")),
]

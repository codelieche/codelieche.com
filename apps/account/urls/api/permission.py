# -*- coding:utf-8 -*-
from django.urls import path

from account.views.permission import PermissionListApiView, PermissionAllApiView

urlpatterns = [
    # 前缀：/api/v1/account/permission/
    path('list', PermissionListApiView.as_view(), name="list"),
    path('all', PermissionAllApiView.as_view(), name="all"),
]

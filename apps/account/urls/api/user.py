# -*- coding:utf-8 -*-
from django.urls import path

from account.views.user import (
    UserListView,
    UserAllListView,
    UserDetailView
)


urlpatterns = [
    # 前缀：/api/v1/account/user/
    path('list', UserListView.as_view(), name="list"),
    path('all', UserAllListView.as_view(), name="all"),
    path('<int:pk>', UserDetailView.as_view(), name="detail"),
    path('<str:username>', UserDetailView.as_view(lookup_field="username"), name="detail2"),
]

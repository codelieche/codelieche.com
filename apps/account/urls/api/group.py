# -*- coding:utf-8 -*-
from django.urls import path

from account.views.group import (
    GroupListView,
    GroupCreateView,
    GroupDetailView,
    GroupEditorView,
)

urlpatterns = [
    # 前缀：/api/v1/account/group/
    # Group List Api
    path('list', GroupListView.as_view(), name="list"),
    # Group Create Api
    path('create', GroupCreateView.as_view(), name="create"),
    # Group Detail Api: GET and PUT
    path('<int:pk>', GroupDetailView.as_view(), name="detail"),
    # Group Editor Detail Info Api: GET
    path('<int:pk>/editor', GroupEditorView.as_view(), name="editor_info"),
]

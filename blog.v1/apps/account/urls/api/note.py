# -*- coding:utf-8 -*-
from django.urls import path

from account.views.note import (
    NoteCreateApiView,
    NoteListApiView,
    NoteListAllApiView,
    NoteDetailApiView
)


urlpatterns = [
    # 前缀：/ap/v1/account/note/
    path("create", NoteCreateApiView.as_view(), name="create"),
    path("list", NoteListApiView.as_view(), name="list"),
    path("all", NoteListAllApiView.as_view(), name="all"),
    path("<int:pk>", NoteDetailApiView.as_view(), name="detail"),
]

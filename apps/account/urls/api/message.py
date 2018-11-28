# -*- coding:utf-8 -*-
from django.urls import path

from account.views import message

urlpatterns = [
    # 前缀/api/v1/account/message
    path('create', message.MessageCreateView.as_view(), name='create'),
    path('list', message.MessageListView.as_view(), name='list'),
    path('<int:pk>', message.MessageDetailView.as_view(), name='detail')
]

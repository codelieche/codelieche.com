# -*- coding:utf-8 -*-
from django.urls import re_path

from modellog.views import (
    ModelLogsEntryListAPIView,
    ObjectLogsListDetailApiView,
    LogsEntryDetailApiView
)


urlpatterns = [
    # 日志详情
    re_path(r'^(?P<pk>\d+)/?$', LogsEntryDetailApiView.as_view(), name='detail'),
    # 模块日志列表
    re_path(r'^(?P<app>\w+)/(?P<model>\w+)/list/?$',
            ModelLogsEntryListAPIView.as_view(), name="model_logs_list"),
    # 模块中某个对象的日志列表
    re_path(r'^(?P<app>\w+)/(?P<model>\w+)/(?P<pk>\d+)/list/?$',
            ObjectLogsListDetailApiView.as_view(), name='object_logs_list'),
]

# -*- coding:utf-8 -*-
from django.urls import path

from wenjuan.views.report import ReportCreateApiView, ReportDetailApiView


urlpatterns = [
    # 前缀：/api/v1/wenjuan/report/
    path("create", ReportCreateApiView.as_view(), name="create"),
    path("<int:pk>", ReportDetailApiView.as_view(), name="detail"),
]

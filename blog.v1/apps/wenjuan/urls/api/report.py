# -*- coding:utf-8 -*-
from django.urls import path

from wenjuan.views.report import (
    ReportCreateApiView,
    ReportListAPIView,
    ReportListALLApiView,
    ReportDetailApiView,
)


urlpatterns = [
    # 前缀：/api/v1/wenjuan/report/
    path("create", ReportCreateApiView.as_view(), name="create"),
    path("list", ReportListAPIView.as_view(), name="list"),
    path("all", ReportListALLApiView.as_view(), name="all"),
    path("<int:pk>", ReportDetailApiView.as_view(), name="detail"),
]

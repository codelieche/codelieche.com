# -*- coding:utf-8 -*-
from django.urls import path

from wenjuan.views.job import JobListApiView, JobDetailApiView, JobReportsListApiView


urlpatterns = [
    # 前缀：/api/v1/wenjuan/job/
    path("list", JobListApiView.as_view(), name="list"),
    path("<int:pk>", JobDetailApiView.as_view(), name="detail"),
    path("<int:pk>/reports", JobReportsListApiView.as_view(), name="reports"),
    path("<str:name>", JobDetailApiView.as_view(lookup_field="name"), name="detail02"),
]

# -*- coding:utf-8 -*-
from django.urls import path

from question.views.job import JobListApiView, JobDetailApiView


urlpatterns = [
    # 前缀：/api/v1/question/job/
    path("list", JobListApiView.as_view(), name="list"),
    path("<int:pk>", JobDetailApiView.as_view(), name="detail"),
    path("<str:name>", JobDetailApiView.as_view(lookup_field="name"), name="detail02"),
]

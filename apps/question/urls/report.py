# -*- coding:utf-8 -*-
from django.urls import path

from question.views.report import ReportCreateApiView


urlpatterns = [
    # 前缀：/api/v1/question/report/
    path("create", ReportCreateApiView.as_view(), name="create"),
]

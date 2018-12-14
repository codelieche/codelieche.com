# -*- coding:utf-8 -*-
from django.urls import path, include
from wenjuan.views.job import JobListApiView, JobDetailApiView


urlpatterns = [
    # 前缀：/api/v1/wenjuan/
    path("list", JobListApiView.as_view(), name="list"),
    path("<int:pk>", JobDetailApiView.as_view(), name="detail"),
    # 问卷相关api
    path("job/", include(arg=("wenjuan.urls.api.job", "wenjuan"), namespace="job")),
    # 问题相关api
    path("question/", include(arg=("wenjuan.urls.api.question", "wenjuan"), namespace="question")),
    # 问卷回答
    path("report/", include(arg=("wenjuan.urls.api.report", "wenjuan"), namespace="report")),
]

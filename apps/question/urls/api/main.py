# -*- coding:utf-8 -*-
from django.urls import path, include
from question.views.question import QuestionListApiView, QuestionDetailApiView


urlpatterns = [
    # 前缀：/api/v1/question/
    path("list", QuestionListApiView.as_view(), name="list"),
    path("<int:pk>", QuestionDetailApiView.as_view(), name="detail"),
    # 问卷相关api
    path("job/", include(arg=("question.urls.api.job", "question"), namespace="job")),
    # 问题相关api
    path("question/", include(arg=("question.urls.api.question", "question"), namespace="question")),
    # 问卷回答
    path("report/", include(arg=("question.urls.api.report", "question"), namespace="report")),
]

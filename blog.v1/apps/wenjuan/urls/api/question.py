# -*- coding:utf-8 -*-
from django.urls import path
from wenjuan.views.question import QuestionListApiView, QuestionDetailApiView


urlpatterns = [
    # 前缀：/api/v1/wenjuan/question/
    path("list", QuestionListApiView.as_view(), name="list"),
    path("<int:pk>", QuestionDetailApiView.as_view(), name="detail"),
]

# -*- coding:utf-8 -*-
from django.urls import re_path

from question.views.pages.question import QuestionPageView


urlpatterns = [
    # 前缀：/question/
    re_path(".*", QuestionPageView.as_view(), name="questions"),
]

# -*- coding:utf-8 -*-
from django.shortcuts import render

from django.views.generic import View


class QuestionPageView(View):
    """
    Question Page View
    """
    def get(self, request):
        return render(request=request, template_name="question/index.html")

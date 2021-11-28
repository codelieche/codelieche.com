# -*- coding:utf-8 -*-
from django.shortcuts import render

from django.views.generic import View


class WenjuanPageView(View):
    """
    Question Page View
    """
    def get(self, request):
        return render(request=request, template_name="wenjuan/index.html")

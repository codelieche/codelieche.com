# -*- coding:utf-8 -*-
from django.shortcuts import render
# Create your views here.


def page_403(request):
    return render(request, '403.html')


def page_404(request):
    return render(request, '404.html')


def page_500(request):
    return render(request, '500.html')
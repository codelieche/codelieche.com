# -*- coding:utf-8 -*-
"""codelieche URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from codelieche.views.httperror import page_403, page_404, page_500


urlpatterns = [
    path('admin/', admin.site.urls),
    # api v1 url
    path('api/v1/', include(arg=("codelieche.urls.api_v1", "codelieche"), namespace="api")),
]

# 错误页面
handler403 = page_403
handler404 = page_404
handler500 = page_500

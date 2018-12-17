# -*- coding:utf-8 -*-
from django.urls import re_path

from wenjuan.views.pages.wenjuan import WenjuanPageView


urlpatterns = [
    # 前缀：/wenjuan/
    re_path(".*", WenjuanPageView.as_view(), name="wenjuan"),
]

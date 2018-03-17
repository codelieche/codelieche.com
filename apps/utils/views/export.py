# -*- coding:utf-8 -*-
"""
导出数据相关视图
"""
import json

from rest_framework.views import View
from django.http.response import JsonResponse

from utils.tools.exports import get_export_data, test_export


class TestExportDataView(View):
    """测试导出数据"""
    def get(self, request):
        return test_export()

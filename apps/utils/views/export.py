# -*- coding:utf-8 -*-
"""
导出数据相关视图
"""
import json

from rest_framework.views import View
from django.http.response import JsonResponse

from utils.tools.exports import get_export_data, test_export
from utils.mixins import CsrfExemptMixin


class ExportDataView(CsrfExemptMixin, View):
    """
    导出数据
    """
    # 权限控制
    def post(self, request):
        # 暂时设置为导出数据需要是超级管理员才有权限
        user = request.user
        if not user.is_staff:
            if not user.is_superuser:
                content = {"status": False, "message": "需要是管理员才可以访问"}
                return JsonResponse(content)

        if request.META["CONTENT_TYPE"] == "application/json":
            body = json.loads(request.body)
            app = body.get("app")
            model = body.get("model")
            fields = body.get("fields", [])
            filters = body.get("filters", [])
        else:
            app = request.POST.get("app")
            model = request.POST.get("model")
            fields = request.POST.get("fields", [])
            filters = request.POST.get("filters", [])
        # print(app, model, fields, filters)
        if not app or not model:
            content = {
                "status": False,
                "message": "app/model为空",
            }
            return JsonResponse(content, status=400)

        if isinstance(fields, str):
            try:
                fields = json.loads(fields)
            except:
                content = {
                    "status": False,
                    "message": "传入的fields有误"
                }
                return JsonResponse(content, status=400)

        if isinstance(filters, str):
            try:
                filters = json.loads(filters)
            except:
                content = {
                    "status": False,
                    "message": "传入的filters有误"
                }
                return JsonResponse(content, status=400)

        try:
            response = get_export_data(app_label=app, model_name=model,
                                       fields=fields, filters=filters)
            return response
        except Exception as e:
            print(e)
            content = {
                "status": False,
                "message": "导出数据出现错误"
            }
            return JsonResponse(content, status=500)


class TestExportDataView(View):
    """测试导出数据"""
    def get(self, request):
        return test_export()

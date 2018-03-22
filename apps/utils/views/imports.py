# -*- coding:utf-8 -*-
"""
导入数据到Model中
"""
import json

from rest_framework.views import View
from django.http.response import JsonResponse

from utils.tools.imports import imports_excel_data_to_model
from utils.mixins import CsrfExemptMixin


class ImportDataToModelView(CsrfExemptMixin, View):
    """
    导入数据到Model中
    只有超级管理员才有权限
    注意：会创建对象，而且出现异常会继续下一条数据
    """
    def post(self, request):
        # 暂时设置为导入数据需要管理员权限
        user = request.user
        if not user.is_staff:
            if not user.is_superuser:
                content = {"status": False, "message": "需要是管理员才可以访问"}
                return JsonResponse(content)

        # 注意这里导入的fields是个字符串，不是列表
        if request.META["CONTENT_TYPE"] == "application/json":
            body = json.loads(request.body)
            app = body.get("app")
            model = body.get("model")
            fields = body.get("fields", "")
        else:
            app = request.POST.get("app")
            model = request.POST.get("model")
            fields = request.POST.get("fields", "")

        # fields以逗号分割
        fields = fields.split(",")
        excel_file = request.FILES.get("file")

        if not excel_file:
            content = {"status": False, "message": "请传入文件"}
            return JsonResponse(content, status=400)

        if len(fields) < 1:
            content = {"status": False, "message": "传入的fields有误"}
            return JsonResponse(content, status=400)

        # 开始执行导入操作
        result, message = imports_excel_data_to_model(app_label=app, model_name=model,
                                                      fields=fields, excel_file=excel_file)

        content = {
            "status": result,
            "message": message
        }
        return JsonResponse(content)

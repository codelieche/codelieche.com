# -*- coding:utf-8 -*-
from django.conf.urls import url

from utils.views.export import ExportDataView, TestExportDataView
from utils.views.imports import ImportDataToModelView

urlpatterns = [
    # api url前缀：/api/v1/utils/
    # 导出数据
    url(r'^export/data/?$', ExportDataView.as_view(), name="export_data"),
    url(r'^export/test/?$', TestExportDataView.as_view(), name="export_test"),

    # 导入数据
    url(r'^import/data', ImportDataToModelView.as_view(), name="import_data"),

]

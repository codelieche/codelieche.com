# -*- coding:utf-8 -*-
from django.conf.urls import url

from utils.views.export import TestExportDataView

urlpatterns = [
    # api url前缀：/api/v1/utils/

    url(r'^export/test/?$', TestExportDataView.as_view(), name="export_test"),
]

# -*- coding:utf-8 -*-
"""
把QuerySet导出成excel文档
结合Django Rest Framework使用
"""
import time

import xlwt
from django.http import HttpResponse
from utils.tools.export import exports_data_to_excel, get_obj_fields_data


def from_queryset_to_excel_response(queryset, fields, filename=None):
    """
    从queryset中导出excel数据
    :param queryset:
    :param fields:
    :param filename
    :return:
    """
    # 1. 导出的数据放到data中
    data = []
    # fields = ["name": "ID", "field"]
    data_title = []
    for f in fields:
        data_title.append(f["verbose_name"])
    data.append(data_title)

    for model in queryset:
        data_i = get_obj_fields_data(model, fields)
        data.append(data_i)

    # 2. 返回response
    return exports_data_to_excel(data=data, filename=filename)


def from_order_dict_to_excel_response(orderdicts, fields, filename=None):
    data = []
    d_title = []

    for f in fields:
        d_title.append(f["verbose_name"])
    data.append(d_title)

    for d in orderdicts:
        d_i = []
        for f in fields:
            d_i.append(d[f["name"]])
        data.append(d_i)

    # 第1步：先创建个工作簿
    wbook = xlwt.Workbook(encoding="utf-8", style_compression=0)
    # 第2步：添加个工作表
    wsheet = wbook.add_sheet(sheetname="导出数据")

    row = 0
    for line in data:
        colum = 0
        for value in line:
            if value is None:
                value = ""
            wsheet.write(row, colum, str(value))
            colum += 1
        row += 1
    if not filename:
        # 如果没有传文件名，就自动创建个
        filename = "{}.xls".format(time.strftime("%Y%m%d%H%M%S"))

    # 写入到文件
    # wbook.save(filename_or_stream=filename)
    # 写入到Response中

    # 把要导出的内容写入到response中
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    wbook.save(filename_or_stream=response)

    return response


def from_orderdict_queryset_to_excel_response(orderdicts, fields, model, filename=None):
    """
    从queryset中导出excel数据
    :param orderdicts:
    :param fields:
    :param model: Orderdict背后的模型
    :param filename
    :return:
    """
    # 1. 导出的数据放到data中
    data = []
    # fields = ["name": "ID", "field"]
    data_title = []
    for f in fields:
        data_title.append(f["verbose_name"])
    data.append(data_title)

    for i in orderdicts:
        obj_id = i["id"]
        obj = model.objects.filter(id=obj_id).first()
        if obj:
            data_i = get_obj_fields_data(obj, fields)
            data.append(data_i)

    # 2. 返回response
    return exports_data_to_excel(data=data, filename=filename)

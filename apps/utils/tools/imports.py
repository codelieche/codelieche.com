# -*- coding:utf-8 -*-
"""
数据导入功能
"""
import xlrd
from django.apps import apps


def get_imports_model(app_label, model_name):
    """
    得到要导入的Model
    :param app_label: app
    :param model_name: model 注意大小写是不敏感的哦
    :return: app.models.Model
    """
    try:
        model = apps.get_model(app_label=app_label, model_name=model_name)
        return model
    except:
        # 如果填写的信息有误，获取不到Model会报错
        return None


def imports_excel_data_to_model(app_label, model_name, fields, excel_file):
    """
    导入excel数据到Model中
    :param app_label: app
    :param model_name: Model Name
    :param fields: 字段
    :param excel_file: excel文件
    :return:
    """
    # 第1步：先得到Model
    model = get_imports_model(app_label, model_name)
    if not model:
        return False, "获取Model为空"

    # 第2步：开始读取excel的数据
    # excel_file = request.FILES.get("file", None)
    # 读取工作簿
    rbook = xlrd.open_workbook(file_contents=excel_file.read())
    # 读取工作表: 默认读取第一个
    rsheet = rbook.sheet_by_index(0)

    ncols = rsheet.ncols
    nrows = rsheet.nrows
    if ncols != len(fields):
        return False, "传入的fields长度{}与表格列数不匹配{}".format(len(fields), ncols)

    # 第3步：读取每一行，然后写入到Model中
    success = 0
    error = 0
    for row in range(1, nrows):
        # row_values = rsheet.row_values(rowx=row)
        row_values = []
        for i in range(ncols):
            cell_value = rsheet.cell_value(rowx=row, colx=i)
            row_values.append(cell_value)
        obj_dic = dict(zip(fields, row_values))
        # print(obj_dic)
        # print(row_values)
        try:
            model.objects.create(**obj_dic)
            success += 1
        except Exception as e:
            print(str(e))
            error += 1

    return True, "成功{}条，失败{}条".format(success, error)


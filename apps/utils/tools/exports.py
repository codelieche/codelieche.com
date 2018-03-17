# -*- coding:utf-8 -*-
"""
导出Model信息
"""
import time

import xlwt
from django.apps import apps
from django.http import HttpResponse

# 保密字段，这些字段内容不让导出
SECRET_FIELDS = ('admin_pwd', 'password')


def field_can_export(field):
    """
    判断字段是否可以导出
    在SECRET_FIELDS中的字段，都不可以导出
    :param field:
    :return:
    """
    if field in SECRET_FIELDS:
        return False
    else:
        return True


def get_export_model(app_label, model_name):
    """
    获取要导出的Model
    :param app_label: app
    :param model_name: model 注意大小写不敏感哦
    :return: app.models.Model
    """
    try:
        model = apps.get_model(app_label=app_label, model_name=model_name)
        return model
    except Exception:
        # 如果填写的信息有误，获取不到Model会报错
        return None


def get_fields_verbosename(model, fields):
    """
    获取Model的一组字段的名
    :param model: 要查找的Model
    :param fields: 字段列表
    :return: [字段的verbosename]
    """
    # 1. 获取到Model的_meta.fields
    model_fields = model._meta.fields

    # 2. 获取到字段的verbose_name
    fields_names = []
    for field in fields:
        # field是个dict对象
        # 是否找到了这个field
        find_field_flag = False

        # 2-1: 如果field有verbose_name那么就直接使用它
        if "verbose_name" in field:
            fields_names.append(field["verbose_name"])
            find_field_flag = True

        # 要导出的字段可能是个m2m的
        elif "manay" in field and field["many"]:
            # 多对多的，就不取verbose_name了，直接用name这个值
            fields_names.append(field["name"])
        else:
            # 如果field中没verbose_name字段，也不是many
            # 2-2：那么就去模型的fields中一个一个找
            for model_field in model_fields:
                if model_field.name == field["name"]:
                    verbose_name = model_field.verbose_name
                    if verbose_name:
                        # 如果这个字段设置了verbose_name就用它
                        fields_names.append(verbose_name)
                    else:
                        # 没有就直接使用最开始的name
                        fields_names.append(field["name"])
                    # 设置字段找到标志位True，同时跳出循环
                    find_field_flag = True
                    break
            # 2-3：如果字段没找到，需要抛出异常
            if not find_field_flag:
                raise Exception("没有找到{}".format(field["name"]))
        # 3：返回fields_names
        return fields_names


def get_obj_fields_data(obj, fields):
    """
    获取对象各字段的值
    :param obj: Model的实例
    :param fields: 字段列表
    :return:
    """
    # 需要返回的结果
    values = []

    # 对每个字段进行处理
    for field in fields:
        # 第1步：如果这个字段不能导出，那么我们需要给它内容设置为：保密字段
        if not field_can_export(field["name"]):
            values.append("保密字段")
            continue
            # 进入下一个field

        # 不是保密字段，那么就开始取值
        # 第2步：开始取出field的数据
        # 2-1: 得到field的数据，name：字段名称，如果是多对多字段，需要传个many
        name = field["name"]
        many = True if "many" in field and field["many"] else False
        # 如果name中有，那么就显示是多级别的
        # 比如：article.user.username, 文章用户的用户名
        name_split = name.split('.')
        length = len(name_split)

        # 2-2: 得到第一级的值
        value_level_1 = getattr(obj, name_split[0])

        if length > 1:
            # 2-2-1：如果length大于1，就表示这个值需要取几层
            if many:
                # 如果是多值的，那么先取出它的QuerySet, 用.all()即可
                value_level_1_all = value_level_1.all()
            else:
                # 如果不是多值的，那么把她变成列表，方便，后续迭代
                value_level_1_all = [value_level_1]

            # 2-2-2：把值放到一个数组中
            values_list = []
            for obj_i in value_level_1_all:
                v = ""
                # v是最终要得到的值
                for f in name_split[1:]:
                    # f是通过点号分割后的field，比如：article.user.username
                    v = getattr(obj_i, f)
                    # 通过for 渠道最后一层的field value
                values_list.append(v)

            # 2-2-3：把这个值用,连接起来【后续可能要改成可配置，默认用逗号】
            value = ",".join(values_list)
        else:
            # 2-3: 这个filed["name"]通过点分割后长度为1，那么直接取它的值
            # 注意，没有点, 那么就让它都是单值的，many_to_many的，name中请一定配置多级，且name中有点
            value = value_level_1
        # 2-4：把这个字段的value放入到values中
        values.append(value)

    # 第3步: 返回这个对象，这组field的值
    return values


def exports_data_to_excel(data, filename=None):
    """
    导出数据到excel表格中
    :param data: 要导出的数据，包括标题和数据行
    :param filename: 文件名
    :return: response
    """
    # 第1步：先创建一个工作簿
    wbook = xlwt.Workbook(enconding="utf-8", style_compression=0)

    # 第2步：添加个工作表
    wsheet = wbook.add_sheet(sheetname="导出数据")

    # 第3步：开始一行一行的写数据
    row = 0
    for line in data:
        colum = 0
        for value in line:
            wsheet.write(row, colum, str(value))
            # 列自增
            colum += 1
        # 行自增
        row += 1

    # 第4步：写入到文件/response中
    # 4-1: 处理文件名
    if not filename:
        # 如果没有传入文件名，就自动创建个
        filename = "{}.xls".format(time.strftime("%Y%m%d%H%M%S"))
    # 4-2：开始写入
    # 方式1：写入到文件
    # wbook.save(filename_or_stream=filename)

    # 方式2：写入到HttpResponse中
    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = 'attachment; filename="{}"'.format(filename)
    wbook.save(filename_or_stream=response)

    # 第5步：返回响应
    return response


def get_export_data(app_label, model_name, fields, filters=None):
    """
    得到要导出的数据
    :param app_label: app
    :param model_name: model name
    :param fields:  字段列表
    :param filters: 过滤列表
    :return:
    """
    # 第1步：先得到Model
    model = get_export_model(app_label, model_name)
    if not model:
        return False

    # 第2步：开始获取Model的数据
    # 2-1：先获取到满足条件的对象
    objs = model.objects.all()

    # 2-2: 处理fields的verbose_name信息
    fields_verbose_name_list = get_fields_verbosename(model=model, fields=fields)
    # print(fields_verbose_name_list)

    # 2-3: 处理filters信息
    # eg: filters = [{"name": "id", "flag": "__lt", "value": 5}]
    if isinstance(filters, list):
        kwargs = {}
        for _filter in filters:
            filter_name = _filter["name"]
            if "flag" in _filter and _filter["flag"]:
                # 如果这个过滤字段有falg
                filter_name += _filter["flag"]
            # 过滤字段的条件值
            filter_value = _filter["value"]
            # 把这个过滤的字段，加入到kwargs中
            kwargs[filter_value] = filter_value
        # 处理完过滤字段后，重新获取下objs
        objs = objs.filter(**kwargs)

    # 第3步：开始构造要导出的数据
    # 3-1: 第一行就是 导出字段的verbose_name
    data = [fields_verbose_name_list]

    # 3-2: 获取每个要导出的数据
    for obj in objs:
        values = get_obj_fields_data(obj, fields)
        data.append(values)

    # 第4步：把数据写入到excel中
    response = exports_data_to_excel(data=data)

    # 第5步：返回响应
    return response


def test_export():
    """
    测试导出用户信息
    :return:
    """
    app = "account"
    model = "UserProfile"
    fields = [
        {"name": "id"},
        {"name": "username", "verbose_name": "用户名"},
        {"name": "last_login"}
    ]
    filters = [
        {"name": "id", "flag": "__lt", "value": 1}
    ]

    return get_export_data(app, model, fields, filters=filters)

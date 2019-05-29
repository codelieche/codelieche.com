# -*- coding:utf-8 -*-
"""
导出Model信息
待优化的点：加个filter过滤功能
"""
import time

import xlwt
from django.apps import apps
from django.http.response import HttpResponse

SECRET_FIELDS = ["admin_pwd", "password"]


def field_can_export(field):
    """
    判断字段是否可以导出
    :param field:
    :return:
    """
    if field in SECRET_FIELDS:
        return False
    else:
        return True


def get_export_model(app_label, model_name):
    """
    得到要导出的Model
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
    获取字段的名字
    :return:
    """
    # 1. 获取到model的_meta.fields
    model_fields = model._meta.fields

    # 2. 获取到字段的verbose_name
    fields_names = []
    for field in fields:
        find_field_flag = False
        if "verbose_name" in field:
            fields_names.append(field["verbose_name"])
            find_field_flag = True
        elif "manay" in field and field["many"]:
            fields_names.append(field["name"])
            find_field_flag = True
        else:
            for model_field in model_fields:
                if model_field.name == field["name"]:
                    verbose_name = model_field.verbose_name
                    if verbose_name:
                        fields_names.append(verbose_name)
                    else:
                        fields_names.append(field["name"])
                    # 跳出循环
                    find_field_flag = True
                    break
        if not find_field_flag:
            raise Exception("没找到{}".format(field["name"]))
    # 返回fields_names
    return fields_names


def get_obj_fields_data(obj, fields):
    """
    获取对象的各字段的值
    :param obj:
    :param fields:
    :return:
    """
    values = []
    # 对每个字段进行处理
    for field in fields:
        # 第1步：如果这个字段不能导出，那么我们需要给它内容设置为：保密字段
        if not field_can_export(field["name"]):
            values.append("保密字段")
            continue
            # 进入下一个field

        # 第2步：开始取出field的数据
        # 2-1：得到field的数据，name：字段名称，如果是多对多的字段，需要传个manay
        name = field["name"]
        many = True if "many" in field and field["many"] else False
        # 如果name中有.那么就表示是多级别的
        # 比如:article.user.username， 文章用户的用户名
        name_split = name.split('.')
        length = len(name_split)

        # 2-2: 得到第一级的值
        value_levl_1 = getattr(obj, name_split[0])

        if length > 1:
            # 如果length大于1，就表示这个值要取几层
            if many:
                # 如果是多值的，那么先取出它的QuerySet，用.all()即可
                value_levl_1_all = value_levl_1.all()
            else:
                # 不是多值的，那么把它变成列表，方便，后续迭代
                value_levl_1_all = [value_levl_1]

            values_list = []
            for obj_i in value_levl_1_all:
                v = ""
                obj_i_tmp = obj_i
                # v是最终要得到的值
                for f in name_split[1:]:
                    # f是通过点号分割后的field，比如：article.user.username
                    try:
                        v = getattr(obj_i_tmp, f)
                        if v:
                            obj_i_tmp = v
                    except AttributeError:
                        # print(obj_i_tmp, f)
                        try:
                            v = obj_i_tmp.get(f, None)
                            if v:
                                obj_i_tmp = v
                        except Exception:
                            v = "---"
                    # 通过for 取到最后一层的field value
                if v:
                    values_list.append(v)
            # 把这个值用,连接起来【后续可能要改成可配置，默认用逗号】
            if values_list:
                value = ",".join(values_list)
            else:
                value = "---"
        else:
            # 如果，这个field["name"]通过点分割长度为1，那么直接取它的值
            # 注意，没有点，那么就让它都是单值的，many_to_many的，name中请一定配置多级，加个点
            value = value_levl_1
            value = str(value)
        # 把这个这个字段得到的value放入到values中
        values.append(value)

    # 第3步：返回这对象，这组field的值
    return values


def exports_data_to_excel(data, filename=None):
    """
    导出数据到excel表格中
    :param data:
    :param filename: 文件名
    :return: response
    """
    # 第1步：先创建个工作簿
    wbook = xlwt.Workbook(encoding="utf-8", style_compression=0)
    # 第2步：添加个工作表
    wsheet = wbook.add_sheet(sheetname="导出数据")

    row = 0
    for line in data:
        colum = 0
        for value in line:
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


def get_export_data(app_label, model_name, fields, filters=None):
    """
    得到要导出的数据
    :param app_label:
    :param model_name:
    :param fields: 字段列表
    :param filters: 过滤列表
    :return:
    """
    # 第1步：先得到Model
    model = get_export_model(app_label, model_name)
    if not model:
        return False

    # 第2步：开始获取Model的数据
    # 2-1: 先获取到满足条件的对象
    objs = model.objects.all()

    # 2-2：处理fields的verbose_name信息
    fields_verbose_name_list = get_fields_verbosename(model=model, fields=fields)
    # print(fields_verbose_name_list)

    # 2-3: 处理filters信息
    # [{"name": "id", flag: "__lt", value: ""}]
    if isinstance(filters, list):
        kwargs = {}
        for _filter in filters:
            filter_name = _filter["name"]
            if _filter["flag"]:
                filter_name += _filter["flag"]
            filter_value = _filter["value"]
            # 把这个过滤的字段，加入到kwargs中
            kwargs[filter_name] = filter_value
        objs = objs.filter(**kwargs)

    data = [fields_verbose_name_list]

    # 2-3：处理每个对象的数据
    for obj in objs:
        values = get_obj_fields_data(obj, fields)
        # print(values)
        data.append(values)

    # 第3步：把数据写入到excel中
    # print(data)
    response = exports_data_to_excel(data)
    return response


def test_export():
    # 测试导出用户信息
    app = "account"
    model = "UserProfile"
    fields = [
        {"name": "id"},
        {"name": "username", "verbose_name": "用户名"},
        {"name": "nick_name", "verbose_name": "昵称"},
        {"name": "last_login"},
        {"name": "groups.name", "many": True, "verbose_name": "组"},
    ]

    filters = [
        {"name": "id", "flag": "__lt", "value": 15}
    ]

    return get_export_data(app, model, fields, filters)

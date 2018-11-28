# -*- coding:utf-8 -*-
"""
文件上传相关的工具函数
"""
import os
import time
import random

from django.core.files.storage import FileSystemStorage
from django.conf import settings


class ImageStorage(FileSystemStorage):
    """
    图片上传
    图片上传的时候自动修改下文件名字
    """

    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        # 初始化ImageStorage
        super(ImageStorage, self).__init__(location, base_url)

    def _save(self, name, content):
        """
        拓展_save方法
        :param name: 上传的文件名
        :param content: 内容
        :return:
        """
        # 先获取文件的拓展名
        ext = os.path.splitext(name)[1]
        # 文件目录
        d = os.path.dirname(name)
        # 定义文件名：年/月/时分秒随机数
        # filename = time.strftime('%Y%m%d%H%M%S')
        filename = time.strftime('%d%H%M%S')
        # 如果并发人数大，那么这个重命名需要调整
        filename = '{}_{}'.format(filename, random.randint(0, 100))
        # 重写合成文件的名字,注意别漏了ext
        name_new = os.path.join(d, filename + ext)
        # 调用父类的方法
        return super(ImageStorage, self)._save(name=name_new, content=content)


def file_upload_to(instance, filename):
    """
    文件上传相对路径
    :param instance: 实例
    :param filename: 文件名
    :return: 上传的文件路径
    """
    # 传过来的实力，需要有个user_id的值，用户ID
    print(instance.user_id)
    name = 'file/{}/{}_{}'.format(time.strftime('%Y/%m'), instance.user_id, filename)
    return name


# PRIVATE_MEDIA_ROOT = getattr(settings, 'PRIVATE_MEDIA_ROOT',
#                              os.path.join(settings.BASE_DIR, '../private_media'))
# # 判断目录是否存在，如果不存在创建
# if not os.path.exists(PRIVATE_MEDIA_ROOT):
#     os.mkdir(PRIVATE_MEDIA_ROOT)
#
#
# class PrivateFileStorage(FileSystemStorage):
#     """
#     文件上传，不是要用media，使用私有文件系统
#     图片上传的时候自动修改下文件名字
#     """
#
#     def __init__(self, location=PRIVATE_MEDIA_ROOT, base_url='/files'):
#         # 初始化ImageStorage
#         super().__init__(location, base_url)
#
#     def _save(self, name, content):
#         """
#         拓展_save方法
#         :param name: 上传的文件名
#         :param content: 内容
#         :return:
#         """
#         # 先获取文件的拓展名
#         ext = os.path.splitext(name)[1]
#         # 文件目录
#         d = os.path.dirname(name)
#         # 定义文件名：年/月/时分秒随机数
#         # filename = time.strftime('%Y%m%d%H%M%S')
#         filename = time.strftime('%d%H%M%S')
#         # 如果并发人数大，那么这个重命名需要调整
#         filename = '{}_{}'.format(filename, random.randint(0, 100))
#         # 重写合成文件的名字,注意别漏了ext
#         name_new = os.path.join(d, filename + ext)
#         # 调用父类的方法
#         return super()._save(name=name_new, content=content)

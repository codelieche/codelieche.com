# -*- coding:utf-8 -*-
"""
这个文件是，图片上传的时候，自动修改图片的名字
"""
import os
import time
import random

from django.conf import settings
from django.core.files.storage import FileSystemStorage


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
        重写_save方法
        :param name: 上传的文件名
        :param content: 内容
        """
        # 第1步：先获取文件后缀名和文件所在目录
        ext = os.path.splitext(name)[1]
        # 文件目录
        d = os.path.dirname(name)

        # 第2步：定义文件名，年/月/时分秒随机数
        filename = time.strftime('%Y%m%d%H%M%S')
        # 当系统并发人数达，那么这个重命名是需要调整的，名称很可能冲突
        filename = '{}_{}'.format(filename, random.randint(0, 100))
        # 重写合成文件的名字
        name_new = os.path.join(d, filename + ext)

        # 第3步：调用父类的_save方法
        return super(ImageStorage, self)._save(name_new, content)

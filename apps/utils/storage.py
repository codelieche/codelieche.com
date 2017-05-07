# -*- coding:utf-8 -*-
"""
这个文件是，图片上传的时候，自动修改图片的名字
"""
import os
import time
import random

from django.core.files.storage import FileSystemStorage


class ImageStorage(FileSystemStorage):
    from django.conf import settings

    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        # 初始化ImageStorage
        super(ImageStorage, self).__init__(location, base_url)

    def _save(self, name, content):
        """
        重写_save方法
        """
        # 文件后缀名
        ext = os.path.splitext(name)[1]
        # 文件目录
        d = os.path.dirname(name)
        # 定义文件名，年/月/时分秒随机数
        file_name = time.strftime('%Y%m%d%H%M%S')
        file_name += '_%d' % random.randint(0, 100)
        # 重写合成文件的名字
        name = os.path.join(d, file_name + ext)
        # 调用父类的方法
        return super(ImageStorage, self)._save(name, content)


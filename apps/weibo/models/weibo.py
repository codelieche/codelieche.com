# -*- coding:utf-8 -*-
"""
微博相关的 Model
"""
import sys
from io import BytesIO

from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image as PImage, ExifTags

from account.models import User
from utils.store import ImageStorage


class Image(models.Model):
    """
    图片
    """
    user = models.ForeignKey(verbose_name="用户", to=User, on_delete=models.SET_NULL, blank=True, null=True)
    file = models.ImageField(verbose_name="图片", upload_to="weibo/images/%Y/%m", storage=ImageStorage(),
                             help_text="图片路径")
    filename = models.CharField(verbose_name="图片名称", max_length=128, blank=True, null=True)
    # 可能是存储在本地(local)、七牛云(qiniu)、阿里云/AWS对象存储中
    storage = models.CharField(verbose_name="存储", max_length=20, blank=True, default="local")
    url = models.URLField(verbose_name="第三方网址", blank=True, max_length=200, null=True)
    description = models.CharField(verbose_name="描述", blank=True, max_length=256, null=True)

    time_added = models.DateTimeField(verbose_name="添加时间", blank=True, auto_now_add=True)
    is_deleted = models.BooleanField(verbose_name="删除", blank=True, default=False)

    def save(self, *args, **kwargs):
        if not self.id and self.file:
            self.file = self.resize_image(self.file)
        super().save(*args, **kwargs)

    def resize_image(self, image_file):
        """
        对图片大小进行缩放
        :param image_file: 图片对象
        :return:
        """
        if image_file.file.content_type != "image/jpeg" and image_file.size < 600 * 1024:
            return image_file

        if image_file.file.content_type == "image/gif":
            return image_file

        image_tmp = PImage.open(image_file)

        # 方向处理
        try:
            if image_tmp._getexif():
                exif = dict(image_tmp._getexif().items())

                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == "Orientation":
                        break

                if exif[orientation] == 3:
                    image_tmp = image_tmp.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    image_tmp = image_tmp.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    image_tmp = image_tmp.rotate(90, expand=True)
        except Exception as e:
            print(e)

        output_io_stream = BytesIO()
        w, h = image_tmp.size

        scale = 1
        if w > 1600:
            scale = 1600.0 / w
        image_resize = image_tmp.resize((int(w * scale), int(h * scale)))
        image_resize.save(output_io_stream, format='JPEG', quality=80)
        output_io_stream.seek(0)
        image = InMemoryUploadedFile(
            output_io_stream,
            'ImageField',
            "%s.jpg" % image_file.name.split('.')[0],
            'image/jpeg',
            sys.getsizeof(output_io_stream),
            None
        )
        return image

    class Meta:
        verbose_name = "微博图片"
        verbose_name_plural = verbose_name


class Weibo(models.Model):
    """
    微博博文
    """
    user = models.ForeignKey(to=User, verbose_name="用户", on_delete=models.CASCADE)
    content = models.CharField(verbose_name="博文内容", max_length=512, blank=True, null=True)
    # 发微博，有图文、视频、链接分享
    images = models.ManyToManyField(to=Image, blank=True, verbose_name="关联的图片")
    video = models.URLField(verbose_name="视频地址", blank=True, null=True, max_length=200)
    link = models.URLField(verbose_name="分享链接", blank=True, null=True, max_length=200)
    address = models.GenericIPAddressField(verbose_name="IP地址", blank=True, null=True)

    is_public = models.BooleanField(verbose_name="是否公开", blank=True, default=False)
    time_added = models.DateTimeField(verbose_name="添加时间", blank=True, auto_now_add=True)
    is_deleted = models.BooleanField(verbose_name="删除", blank=True, default=False)

    class Meta:
        verbose_name = "微博"
        verbose_name_plural = verbose_name


class Comment(models.Model):
    """
    微博评论
    """
    user = models.ForeignKey(to=User, verbose_name="评论用户",  related_name="weibo_comments",
                             on_delete=models.CASCADE, blank=True, null=True)
    weibo = models.ForeignKey(to=Weibo, on_delete=models.CASCADE, verbose_name="微博")
    content = models.CharField(verbose_name="评论内容", max_length=512)
    address = models.GenericIPAddressField(verbose_name="IP地址", blank=True, null=True)
    time_added = models.DateTimeField(verbose_name="添加时间", blank=True, auto_now_add=True)
    is_deleted = models.BooleanField(verbose_name="删除", blank=True, default=False)

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name

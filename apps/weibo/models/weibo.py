# -*- coding:utf-8 -*-
"""
微博相关的 Model
"""
from django.db import models

from account.models import User
from utils.store import ImageStorage


class Image(models.Model):
    """
    图片
    """
    file = models.ImageField(verbose_name="图片", upload_to="weibo/image/%Y/%m", storage=ImageStorage(),
                             help_text="图片路径")
    filename = models.CharField(verbose_name="图片名称", max_length=100, blank=True, null=True)
    # 可能是存储在本地(local)、七牛云(qiniu)、阿里云/AWS对象存储中
    storage = models.CharField(verbose_name="存储", blank=True, default="local")
    url = models.URLField(verbose_name="第三方网址", blank=True, max_length=200, null=True)
    description = models.CharField(verbose_name="描述", blank=True, max_length=128, null=True)

    time_added = models.DateTimeField(verbose_name="添加时间", blank=True, auto_now_add=True)
    is_deleted = models.BooleanField(verbose_name="删除", blank=True, default=False)

    class Meta:
        verbose_name = "微博图片"
        verbose_name_plural = verbose_name


class Weibo(models.Model):
    """
    微博博文
    """
    user = models.ForeignKey(to=User, verbose_name="用户", on_delete=models.CASCADE)
    content = models.CharField(verbose_name="博文内容", max_length=512)
    # 发微博，有图文、视频、链接分享
    images = models.ForeignKey(to=Image, blank=True)
    video = models.URLField(verbose_name="视频地址", blank=True, null=True, max_length=200)
    link = models.URLField(verbose_name="分享链接", blank=True, null=True, max_length=200)

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
    user = models.ForeignKey(to=User, verbose_name="评论用户", on_delete=models.CASCADE, blank=True, null=True)
    content = models.CharField(verbose_name="评论内容", max_length=512)
    time_added = models.DateTimeField(verbose_name="添加时间", blank=True, auto_now_add=True)
    is_deleted = models.BooleanField(verbose_name="删除", blank=True, default=False)

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name

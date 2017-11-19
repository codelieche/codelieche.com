# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible
# Create your models here.


@python_2_unicode_compatible
class UserData(models.Model):
    """
    用户数据，保存临时文章等
    不同用户有一些临时碎片信息，在不同session中要用到的数据
    """
    TYPE_CHOICE = (
        ('article', "临时文章"),
        ('comment', '临时评论')
    )
    user = models.ForeignKey("UserProfile", related_name="userdatas")
    type = models.CharField(verbose_name="类型", max_length=20, choices=TYPE_CHOICE)
    content = models.TextField(verbose_name="信息内容")
    time_updated = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return "%s -> %s" % (self.user, self.type)


@python_2_unicode_compatible
class UserProfile(AbstractUser):
    """
    自定义的用户Model
    拓展了gender, nike_name, mobile字段
    """
    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女'),
        ('secret', '保密'),
    )

    nike_name = models.CharField(max_length=40, blank=True, verbose_name="昵称")
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES,
                              verbose_name="性别", default="secret")
    mobile = models.CharField(max_length=11, verbose_name="手机号", blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

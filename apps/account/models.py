# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
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
    user = models.ForeignKey(User, related_name="userdatas")
    type = models.CharField(verbose_name="类型", max_length=20, choices=TYPE_CHOICE)
    content = models.TextField(verbose_name="信息内容")
    updated = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return "%s -> %s" % (self.user, self.type)

# -*- coding:utf-8 -*-
from django.contrib import admin
from django.contrib.auth import get_user_model

# Register your models here.


class UserModelAdmin(admin.ModelAdmin):
    """
    用户ModelAdmin
    """
    list_display = ['id', 'username', 'email', 'mobile']
    ordering = ('id',)


User = get_user_model()
admin.site.register(User, UserModelAdmin)

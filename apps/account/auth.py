# -*- coding:utf-8 -*-
"""
自定义用户验证
"""

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model

from .models import UserProfile

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户校验
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 用户有可能传入的是邮箱或者用户名或者手机号
            # 用Q来让查询条件实现或的功能
            if User == UserProfile:
                user = User.objects.get(
                    Q(username=username) | Q(email=username) | Q(mobile=username)
                )
            else:
                # 如果不是account.UserProfile那么就是没有mobile字段的，所以只通过username/email查询用户
                user = User.objects.get(
                    Q(username=username) | Q(email=username)
                )

            # 检查用户的密码
            if user and user.check_password(password):
                return user
            else:
                return None
        except Exception:
            return None

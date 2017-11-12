# -*- coding:utf-8 -*-
"""
自定义用户验证
"""

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model
# 如果知道系统具体使用了哪个User，可以直接导入，也可以使用get_users_model获取
# from django.account.models import User

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 用户有可能传入的是邮箱或者用户名或者手机号
            # 用Q来让查询条件实现或的功能
            user = User.objects.get(
                Q(username=username) | Q(email=username) | Q(mobile=username)
            )
            if user.check_password(password):
                # 如果用户登陆的时候，还没有svn_password，那么给它生成一个
                return user
            else:
                return None
        except Exception:
            return None

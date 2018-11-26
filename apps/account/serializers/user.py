# -*- coding:utf-8 -*-
from rest_framework import serializers

from account.models import User


class UserLoginSerializer(serializers.Serializer):
    """用户登录 Serializer"""
    username = serializers.CharField(max_length=40, required=True)
    password = serializers.CharField(max_length=40, required=True)


class UserSimpleInfoSerializer(serializers.ModelSerializer):
    """
    用户基本信息Model Serializer
    """

    class Meta:
        model = User
        fields = ('id', 'username')


class UserAllListSerializer(serializers.ModelSerializer):
    """
    列出所有用户的信息Model Serializer
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'nick_name', 'mobile', 'qq', 'wechart',
                  'is_superuser', 'is_active', 'last_login', 'is_deleted')


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情/编辑序列化Model
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'nick_name', 'is_active', 'mobile', 'qq', 'wechart',
                  'is_superuser', 'last_login', 'is_deleted')
        read_only_fields = ('id', 'username', 'last_login')

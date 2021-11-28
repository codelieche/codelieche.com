# -*- coding:utf-8 -*-
"""
Django权限
"""
from rest_framework import serializers
from django.contrib.auth.models import Permission


class PermissionInfoSerializer(serializers.ModelSerializer):
    """
    权限信息序列化
    """
    app_model = serializers.SerializerMethodField()

    def get_app_model(self, obj):
        return "{}.{}".format(obj.content_type.app_label, obj.content_type.model)

    class Meta:
        model = Permission
        fields = ("id", "codename", "name", "app_model")

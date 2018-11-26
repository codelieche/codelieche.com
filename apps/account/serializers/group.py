# -*- coding:utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import Group

from account.models import User
from account.serializers.permission import PermissionInfoSerializer


class GroupSerializer(serializers.ModelSerializer):
    """
    账号分组 Model Serializer
    """

    class Meta:
        model = Group
        fields = ('id', 'name', 'user_set', 'permissions')


class GroupInfoSerializer(serializers.ModelSerializer):
    """
    账号分组信息 Model Seriallizer
    """
    user_set = serializers.SlugRelatedField(many=True, read_only=False, slug_field='username',
                                            queryset=User.objects.all())
    permissions = PermissionInfoSerializer(many=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'user_set', "permissions")

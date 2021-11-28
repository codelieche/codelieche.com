# -*- coding:utf-8 -*-
"""
权限相关视图
"""
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import Permission

from account.serializers.permission import PermissionInfoSerializer


class PermissionListApiView(generics.ListAPIView):
    """
    权限列表
    """
    queryset = Permission.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = PermissionInfoSerializer

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ("content_type__app_label", "codename", "name")
    ordering_fields = ("id",)
    ordering = ("id",)


class PermissionAllApiView(generics.ListAPIView):
    """
    所有权限列表api
    """
    queryset = Permission.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = PermissionInfoSerializer
    pagination_class = None

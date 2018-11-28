# -*- coding:utf-8 -*-
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import LogsEntry
from .serializers import LogsEntrySerializer


class LogsEntryDetailApiView(generics.RetrieveAPIView):
    """日志详情API"""
    queryset = LogsEntry.objects.all()
    serializer_class = LogsEntrySerializer
    # 权限控制
    permission_classes = (IsAuthenticated,)


class ModelLogsEntryListAPIView(generics.ListAPIView):
    """
    获取日志列表api
    """
    queryset = LogsEntry.objects.all()
    serializer_class = LogsEntrySerializer
    # 权限控制
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # 第1步：先获取到app和model的字符串
        app = self.kwargs['app']
        model = self.kwargs['model']

        # 第2步：获取到Model的content_type
        content_type = get_object_or_404(ContentType, app_label=app, model=model)

        # 第3步：获取数据
        objects_list = LogsEntry.objects.filter(content_type=content_type).order_by('-time_added')

        # 第4步：返回数据
        return objects_list

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ObjectLogsListDetailApiView(generics.ListAPIView):
    """
    获取model某个对象的历史记录列表
    """
    serializer_class = LogsEntrySerializer
    # 权限控制
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # 第1步：先获取到app和model的字符串，pk
        app = self.kwargs['app']
        model = self.kwargs['model']
        pk = self.kwargs['pk']

        # 第2步：获取到Model的content_type
        content_type = get_object_or_404(ContentType, app_label=app, model=model)

        # 第3步：获取数据
        objects_list = LogsEntry.objects.filter(content_type=content_type,
                                                object_id=pk).order_by('-time_added')

        # 第4步：返回数据
        return objects_list

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

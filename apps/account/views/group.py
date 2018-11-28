# -*- coding:utf-8 -*-
"""
账号分组相关的视图函数
"""
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from account.serializers.group import GroupSerializer, GroupInfoSerializer
from utils.permissions import IsSuperUser
from modellog.mixins import LoggingViewSetMixin


class GroupListView(generics.ListAPIView):
    """
    Group List
    """
    queryset = Group.objects.all()
    serializer_class = GroupInfoSerializer
    permission_classes = (IsAuthenticated,)
    # 不要分页
    pagination_class = None


class GroupCreateView(LoggingViewSetMixin, generics.CreateAPIView):
    """
    Group Create
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsSuperUser,)


class GroupDetailView(LoggingViewSetMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Group Detail
    支持：get、put和Delete
    """
    queryset = Group.objects.all()
    serializer_class = GroupInfoSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        self.serializer_class = GroupSerializer
        self.permission_classes = (IsSuperUser, )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # 如果Group中user_set不为空，就不让删除
        group = get_object_or_404(Group, *args, **kwargs)
        if group.user_set.count() > 0:
            return JsonResponse({"status": "failure", "message": "分组中还有用户，不可删除"})
        return super().destroy(request, *args, **kwargs)


class GroupEditorView(generics.RetrieveAPIView):
    """
    用户分组，获取编辑时候要用到的信息时视图函数
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsSuperUser,)

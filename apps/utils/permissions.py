# -*- coding:utf-8 -*-
"""
DRF权限控制相关的工具类
"""
from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    """需要是超级用户才能操作的权限"""

    def has_object_permission(self, request, view, obj):
        # 关于对象的权限，查看，修改，删除
        # rest_framework.generics.RetrieveUpdateDestroyAPIView
        # 继承 BasePermission 复写这个方法，只有当 has_permission 返回True或者没设置，才会来执行此方法
        return request.user.is_superuser

    def has_permission(self, request, view):
        # 这个是全局的是否有权限
        # 关于权限会先对 has_permission 验证
        # 如果是关于对象的权限，这里返回了True，还需要去 has_object_permission判断一下，是False就直接返回
        return request.user.is_superuser


class IsSuperUserOrReadOnly(permissions.BasePermission):
    """如果不是超级管理员，那么只能对对象进行查看的权限"""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # GET, HEAD, OPTIONS
            # 同时游客不能访问，需要是已登陆的用户
            return request.user and request.user.is_authenticated
        else:
            # 需要是超级用户才可以操作
            return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        # 如果是GET方法，那么可以查看，但是如果是PUT或者DELETE就需要是超级用户
        if request.method in permissions.SAFE_METHODS:
            # GET、HEAD、OPTIONS
            # 同时游客不能访问
            return request.user and request.user.is_authenticated
        else:
            # 需要是超级用户才可以操作
            return request.user.is_superuser

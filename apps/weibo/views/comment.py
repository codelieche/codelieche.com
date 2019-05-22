# -*- coding:utf-8 -*-
"""
Weibo 评论相关
"""
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from weibo.models.weibo import Comment
from weibo.serializers.weibo import CommentModelSerializer


class CommentCreateAPIView(generics.CreateAPIView):
    """
    Comment Create Api View
    """
    queryset = Comment.objects.all()
    serializer_class = CommentModelSerializer


class CommentListApiView(generics.ListAPIView):
    """
    Comment List Api View
    """
    queryset = Comment.objects.filter(is_deleted=False)
    serializer_class = CommentModelSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ("weibo", "user")
    search_fields = ("content", "weibo__content")
    ordering = ("-id", "weibo", "user")


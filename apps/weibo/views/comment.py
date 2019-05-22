# -*- coding:utf-8 -*-
"""
Weibo 评论相关
"""
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.http.response import HttpResponse

from weibo.models.weibo import Comment
from weibo.serializers.weibo import CommentModelSerializer, CommentDetailModelSerializer


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


class CommentDetailAPIView(generics.RetrieveDestroyAPIView):
    """
    Comment Detail API View
    """
    queryset = Comment.objects.all()
    serializer_class = CommentDetailModelSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user == request.user:
            instance.is_deleted = True
            instance.save()
            return HttpResponse(status=204)
        else:
            if request.user.is_superuser:
                instance.is_deleted = True
                instance.save()
                return HttpResponse(status=204)
            else:
                return HttpResponse(status=403)

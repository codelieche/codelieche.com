# -*- coding:utf-8 -*-
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from article.models import Image
from article.serializers.article import ImageModelSerializer


class ImageListApiView(generics.ListAPIView):
    """
    文章图片列表api
    """
    serializer_class = ImageModelSerializer
    queryset = Image.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ("filename", "url")
    ordering_fields = ("id", "time_added")
    ordering = ('id', )


class ImageCreateApiView(generics.CreateAPIView):
    """
    文章图片创建api
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ImageModelSerializer
    queryset = Image.objects.all()


class ImageDetailApiView(generics.RetrieveDestroyAPIView):
    """
    文章图片详情api
    """
    queryset = Image.objects.all()
    serializer_class = ImageModelSerializer

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated and user.has_perm("artcile.delete_image"):
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data="无权限删除", status=status.HTTP_403_FORBIDDEN)

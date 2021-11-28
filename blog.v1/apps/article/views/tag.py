# -*- coding:utf-8 -*-
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


from article.serializers.article import TagModelSerializer
from article.models import Tag


class TagListApiView(generics.ListAPIView):
    """
    标签列表api
    """
    serializer_class = TagModelSerializer
    queryset = Tag.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ("slug", "name")
    ordering_fields = ("id", "tag")
    ordering = ('id', )


class TagCreateApiView(generics.CreateAPIView):
    """
    标签创建api
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = TagModelSerializer
    queryset = Tag.objects.all()


class TagDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    """
    标签详情api
    """
    queryset = Tag.objects.all()
    serializer_class = TagModelSerializer

    def update(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated and user.has_perm("artcile.change_tag"):
            # 调用父类方法
            return super().update(request=request, *args, **kwargs)
        else:
            return Response(data="无权限修改", status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated and user.has_perm("artcile.delete_tag"):
            instance = self.get_object()
            if not instance.is_deleted:
                instance.is_deleted = True
                instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data="无权限删除", status=status.HTTP_403_FORBIDDEN)

# -*- coding:utf-8 -*-
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


from article.serializers.article import CategoryModelSerializer
from article.models import Category


class CategoryListApiView(generics.ListAPIView):
    """
    文章分类列表api
    """
    queryset = Category.objects.all()
    # permission_classes = (IsAuthenticated, )
    serializer_class = CategoryModelSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ("parent", "parent__slug")
    search_fields = ("category", "name")
    ordering_fields = ("id", "level")
    ordering = ("id", )


class CategoryDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    """
    文章分类详情api
    """
    queryset = Category.objects.all()
    # permission_classes = (IsAuthenticated, )
    serializer_class = CategoryModelSerializer

    def update(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated and user.has_perm("artcile.change_category"):
            # 调用父类方法
            return super().update(request=request, *args, **kwargs)
        else:
            return Response(data="无权限修改", status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated and user.has_perm("artcile.delete_category"):
            instance = self.get_object()
            if not instance.is_deleted:
                instance.is_deleted = True
                instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data="无权限删除", status=status.HTTP_403_FORBIDDEN)

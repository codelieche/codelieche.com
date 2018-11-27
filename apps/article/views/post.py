# -*- coding:utf-8 -*-
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


from article.serializers.article import PostModelSerializer
from article.models import Post


class PostCreateApiView(generics.CreateAPIView):
    """
    文章创建API
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = PostModelSerializer


class PostListApiView(generics.ListAPIView):
    """
    文章列表Api
    """
    # permission_classes = (IsAuthenticated,)
    # queryset = Post.published.all()
    serializer_class = PostModelSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ("title", "content", "user__username")
    filter_fields = ("category", "category__slug", "author", "author__username")
    ordering_fields = ("id", "time_added", "time_updated")
    ordering = ('id',)

    def get_queryset(self):
        posts = Post.published.all()

        request = self.request
        # 根据时间过滤: 根据日期区间过滤
        date_time__date__gte = request.data.get("date_time__date__gte")
        date_time__date__lte = request.data.get("date_time__date__lte")
        if date_time__date__gte:
            posts = posts.filter(time_added__date__gte=date_time__date__lte)
        if date_time__date__lte:
            posts = posts.filter(time_added__date__gte=date_time__date__lte)

        return posts


class PostDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    """
    文章详情api
    """
    queryset = Post.published.all()
    serializer_class = PostModelSerializer

    def update(self, request, *args, **kwargs):
        user = self.request.user
        instance = self.get_object()
        if user.is_authenticated and user == instance.user or user.has_perm("artcile.change_post"):
            # 调用父类方法
            return super().update(request=request, *args, **kwargs)
        else:
            return Response(data="无权限修改", status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        instance = self.get_object()
        if user.is_authenticated and user == instance.user or user.has_perm("artcile.delete_post"):
            if not instance.is_deleted:
                instance.is_deleted = True
                instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data="您无权限删除", status=status.HTTP_403_FORBIDDEN)


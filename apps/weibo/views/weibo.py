# -*- coding:utf-8 -*-
"""
Weibo View
"""
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
# from django.db.models import Q
from django.http.response import HttpResponse

from weibo.models.weibo import Weibo
from weibo.serializers.weibo import WeiboModelSerializer


class WeiboCreateAPIView(generics.CreateAPIView):
    """
    Weibo Create API View
    """
    queryset = Weibo.objects.all()
    serializer_class = WeiboModelSerializer
    permission_classes = (IsAuthenticated,)


class WeiboListAPIView(generics.ListAPIView):
    """
    Weibo List API View
    """
    queryset = Weibo.objects.filter(is_deleted=False)
    serializer_class = WeiboModelSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    permission_classes = (IsAuthenticated, )
    filter_fields = ("is_deleted", "user")
    search_fields = ("content",)
    ordering = ("-id", "user")

    # def get_queryset(self):
    #     # 1. get user
    #     request = self.request
    #     user = request.user
    #
    #     # 2. check user permission
    #     if user.is_authenticated:
    #         # 判断用户是否是超级用户
    #         if user.is_superuser:
    #             return Weibo.objects.all()
    #         else:
    #             return Weibo.objects.filter(is_deleted=False).filter(Q(is_public=True) | Q(user=user))
    #     else:
    #         return Weibo.objects.filter(is_public=True, is_deleted=False)


class WeiboDetailApiView(generics.RetrieveDestroyAPIView):
    """
    Weibo Detail Api View
    """
    queryset = Weibo.objects.filter(is_deleted=False)
    serializer_class = WeiboModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        # permission check
        instance = super().get_object()
        user = self.request.user
        if instance.is_public:
            return instance
        else:
            if instance.user == user:
                return instance
            else:
                if user.is_superuser:
                    return instance
                else:
                    return None

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

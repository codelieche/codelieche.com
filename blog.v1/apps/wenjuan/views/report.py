# -*- coding:utf-8 -*-
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.http.response import Http404


from wenjuan.models.question import Report
from wenjuan.serializer.report import (
    ReportModelSerializer,
    ReportListSerializer,
    ReportDetailSerializer
)


class ReportCreateApiView(generics.CreateAPIView):
    """
    问卷回答api
    """
    queryset = Report.objects.all()
    serializer_class = ReportModelSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request=request, *args, **kwargs)


class ReportListAPIView(generics.ListAPIView):
    """
    答卷列表API
    """
    serializer_class = ReportListSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ("job_id", "job", "user")
    search_fields = ("job__title", "user__username", "user__nick_name")
    ordering_fields = ("id", "job")
    ordering = ("-id",)

    def get_queryset(self):
        request = self.request
        user = request.user

        if user.is_authenticated:
            return Report.objects.filter(user=user, is_deleted=False)
        else:
            return None


class ReportListALLApiView(generics.ListAPIView):
    """
    答卷列表API
    """
    serializer_class = ReportListSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    pagination_class = None
    filter_fields = ("job_id", "job", "user")
    search_fields = ("job__title", "user__username", "user__nick_name")
    ordering_fields = ("id", "job")
    ordering = ("-id",)

    def get_queryset(self):
        request = self.request
        user = request.user

        if user.is_authenticated:
            if user.is_superuser:
                return Report.objects.all()
            else:
                return Report.objects.filter(user=user, is_deleted=False)
        else:
            return None


class ReportDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    """
    问卷回答api
    """
    queryset = Report.objects.all()
    serializer_class = ReportDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        # TODO：需要做权限校验
        # 有user的只可看自己的，没user的，可以根据ip来做判断
        instance = self.get_object()

        user = request.user
        if instance.user != user:
            if not user.is_superuser:
                raise Http404()
        return super().retrieve(request=request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        user = request.user
        if not user.has_perm("wenjuan.delete_report"):
            # 判断用户是否自己
            if instance.user != user:
                content = {"status": False, "message": "无权限删除Report"}
                return Response(data=content, content_type="application/json", status=403)
            else:
                # 调用父类的删除方法
                return super().delete(request=request, *args, **kwargs)
        else:
            # 调用父类的删除方法: Model复写了__delete__方法的
            return super().delete(request=request, *args, **kwargs)
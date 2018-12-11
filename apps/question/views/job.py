# -*- coding:utf-8 -*-
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from question.models.question import Job
from question.serializer.question import JobModelSerializer


class JobListApiView(generics.ListAPIView):
    """
    文件列表api
    """
    queryset = Job.objects.all()
    serializer_class = JobModelSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ("title", "description")
    filter_fields = ("is_active", "is_authenticated")
    ordering_fields = ("id", "time_added", "time_start", "time_end")
    ordering = ("-id",)


class JobDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    """
    文件详情api
    """
    queryset = Job.objects.all()
    serializer_class = JobModelSerializer
    permission_classes = (IsAuthenticated,)

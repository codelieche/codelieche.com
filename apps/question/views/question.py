# -*- coding:utf-8 -*-
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from question.models.question import Question
from question.serializer.question import QuestionModelSerializer


class QuestionListApiView(generics.ListAPIView):
    """
    问卷问题列表api
    """
    queryset = Question.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = QuestionModelSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ("category", "job")
    search_fields = ("title", "description")
    ordering_fields = ("id",)
    ordering = ("-id",)


class QuestionDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    """
    问卷详情api
    """
    queryset = Question.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = QuestionModelSerializer

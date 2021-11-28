# -*- coding:utf-8 -*-
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from account.serializers.note import NoteModelSerializer
from account.models import Note


class NoteCreateApiView(generics.CreateAPIView):
    """
    Note Create Api View
    """
    serializer_class = NoteModelSerializer
    queryset = Note.objects.all()
    permission_classes = (IsAuthenticated,)


class NoteListApiView(generics.ListAPIView):
    """
    Note List Api View
    """
    serializer_class = NoteModelSerializer
    queryset = Note.objects.filter(is_deleted=False)
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    search_fields = ("user__username", "content")
    ordering_fields = ("id", "time_added", "user")
    ordering = ("-id",)


class NoteListAllApiView(generics.ListAPIView):
    """
    Note List All Api View
    """
    serializer_class = NoteModelSerializer
    queryset = Note.objects.filter(is_deleted=False)
    pagination_class = None
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    search_fields = ("user__username", "content")
    ordering_fields = ("id", "time_added", "user")
    ordering = ("-id",)


class NoteDetailApiView(generics.RetrieveAPIView):
    """
    Note Detail Api View
    """
    queryset = Note.objects.filter(is_deleted=False)
    serializer_class = NoteModelSerializer
    permission_classes = (IsAuthenticated,)


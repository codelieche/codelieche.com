# -*- coding:utf-8 -*-
from rest_framework import serializers

from .models import LogsEntry


class LogsEntrySerializer(serializers.ModelSerializer):
    """模块日志 序列化模型"""
    user = serializers.CharField(source='user.username', read_only=True)
    action = serializers.CharField(source='get_action_flag_display', read_only=True)
    message = serializers.SerializerMethodField()

    def get_message(self, obj):
        return obj.get_message()

    class Meta:
        model = LogsEntry
        fields = ('id', 'user', 'action_flag', 'action', 'object_id', 'time_added', 'message')

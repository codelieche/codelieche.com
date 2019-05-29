# -*- coding:utf-8 -*-
"""
留言相关
"""
from rest_framework import serializers

from account.models import User
from account.models import Note


class NoteModelSerializer(serializers.ModelSerializer):
    """
    Note Model Serializer
    """

    user = serializers.SlugRelatedField(slug_field="username",
                                        required=False, allow_null=True,
                                        queryset=User.objects.all())

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user

        if user.is_authenticated:
            validated_data["user"] = user
        else:
            validated_data["user"] = None

        # 获取IP
        try:
            ip = request.META['HTTP_X_REAL_IP']
        except KeyError:
            ip = request.META["REMOTE_ADDR"]

        validated_data["address"] = ip

        instance = super().create(validated_data=validated_data)
        return instance

    class Meta:
        model = Note
        fields = ("id", "user", "content", "address", "time_added", "is_deleted")

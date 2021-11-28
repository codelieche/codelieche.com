# -*- coding:utf-8 -*-
"""
用户消息相关的序列化Model
"""
from rest_framework import serializers

from account.models import User, Message, MessageCategory


class MessageSerializer(serializers.ModelSerializer):
    """
    用户消息序列化Model
    """
    user = serializers.SlugRelatedField(read_only=False, slug_field='username',
                                        queryset=User.objects.all())
    scope = serializers.SlugRelatedField(read_only=False, slug_field="category",
                                         queryset=MessageCategory.objects.all(),
                                         required=False)

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['unread'] = True
        validated_data['sender'] = user.username
        category = validated_data.get("category")
        if not category:
            category, created = MessageCategory.objects.get_or_create(category="default")
            validated_data["category"] = category

        return super().create(validated_data)

    class Meta:
        model = Message
        fields = ('id', 'user', 'sender', 'category',
                  'title', 'content', 'link', 'unread', 'time_added')

# -*- coding:utf-8 -*-
from rest_framework import serializers

from wenjuan.models.question import Answer


class AnswerModelSerializer(serializers.ModelSerializer):
    """
    Answer Model Serializer
    """

    class Meta:
        model = Answer
        fields = ("id", "question", "option", "answer")


class AnswerDetailSerializer(serializers.ModelSerializer):
    """
    Answer Detail Serializer
    """
    question = serializers.SlugRelatedField(slug_field="title", read_only=True)
    # question_id = serializers.CharField(source="question_id", read_only=True)

    class Meta:
        model = Answer
        fields = ("id", "question_id", "question", "option", "answer")

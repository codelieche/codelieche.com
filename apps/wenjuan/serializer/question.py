# -*- coding:utf-8 -*-

from rest_framework import serializers

from wenjuan.models.question import Job, Question, Choice, Report
from wenjuan.serializer.answer import AnswerModelSerializer


class ChoiceModelSerializer(serializers.ModelSerializer):
    """
    Choice Model Serializer
    """

    class Meta:
        model = Choice
        fields = ("id", "question", "option", "value")


class QuestionModelSerializer(serializers.ModelSerializer):
    """
    Question Model Serializer
    """

    choices = ChoiceModelSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ("id", "title", "description", "category", "is_unique", "choices")


class JobModelSerializer(serializers.ModelSerializer):
    """
    Job Model Serializer
    """
    questions = QuestionModelSerializer(many=True, read_only=True)

    class Meta:
        model = Job
        fields = ("id", "name", "title", "description",
                  "is_active", "is_authenticated", "questions",
                  "time_start", "time_expired", "time_added")


class ReportModelSerializer(serializers.ModelSerializer):
    """
    Report Model Serializer
    """

    answers = AnswerModelSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Report
        fields = ("id", "ip", "user", "ip", "time_added", "answers")


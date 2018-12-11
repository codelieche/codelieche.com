# -*- coding:utf-8 -*-

from rest_framework import serializers

from question.models.question import Job, Question, Choice, Answer, Report


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
        fields = ("id", "title", "description",
                  "is_active", "is_authenticated", "questions",
                  "time_start", "time_expired", "time_added")


class AnswerModelSerializer(serializers.ModelSerializer):
    """
    Answer Model Serializer
    """

    class Meta:
        model = Answer
        fields = ("id", "question", "option", "answer")


class ReportModelSerializer(serializers.ModelSerializer):
    """
    Report Model Serializer
    """

    answers = AnswerModelSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Report
        fields = ("id", "ip", "user", "ip", "time_added", "answers")


# -*- coding:utf-8 -*-
from django.db import models


class Job(models.Model):
    """
    问卷 Model
    """
    title = models.CharField(verbose_name="标题", max_length=128)
    questions = models.ManyToManyField(verbose_name="问题", to="Question", blank=True)
    time_start = models.DateTimeField(verbose_name="开始时间", blank=True, null=True)
    # 问卷开始时间  过期时间
    time_expired = models.DateTimeField(verbose_name="过期时间", blank=True, null=True)
    description = models.CharField(verbose_name="描述", max_length=512)
    time_added = models.DateTimeField(verbose_name="添加时间", auto_now_add=True, blank=True)
    is_active = models.BooleanField(verbose_name="启用", blank=True, default=True)

    class Meta:
        verbose_name = "问卷"
        verbose_name_plural = verbose_name


class Question(models.Model):
    """
    问题 Model
    """
    CATEGORY_CHOICES = (
        ("text", "文本"),
        ("radio", "单选"),
        ("checkbox", "多选")
    )

    title = models.CharField(verbose_name="问题", max_length=128)
    description = models.CharField(verbose_name="描述", max_length=512, blank=True)
    category = models.CharField(verbose_name="类型", choices=CATEGORY_CHOICES, default="text", blank=True)
    # choices = models.ManyToManyField(to="choices", verbose_name="答案选项", blank=True)

    class Meta:
        verbose_name = "问题"
        verbose_name_plural = verbose_name


class Choice(models.Model):
    """
    答案选项Choice
    """
    question = models.ForeignKey(to="question", verbose_name="问题", related_name="choices")
    option = models.CharField(verbose_name="选项", max_length=1)
    value = models.CharField(verbose_name="选项值", max_length=128)

    class Meta:
        verbose_name = "问题答案选项"
        verbose_name_plural = verbose_name


class Answer(models.Model):
    """
    回答Model
    """
    question = models.ForeignKey(to="question", verbose_name="问题")
    option = models.CharField(verbose_name="回答选项", blank=True, max_length=1, null=True)
    answer = models.CharField(verbose_name="回答", max_length=128)

    class Meta:
        verbose_name = "问题回答"
        verbose_name_plural = verbose_name


class Report(models.Model):
    """
    问卷回答 Model
    """
    job = models.ForeignKey(to="job", verbose_name="问卷")
    ip = models.GenericIPAddressField(verbose_name="回答者IP", blank=True, null=True)
    time_added = models.DateTimeField(verbose_name="添加时间", blank=True, auto_now_add=True)
    answers = models.ManyToManyField(verbose_name="问卷回答", to="answer", blank=True)

    class Meta:
        verbose_name = "问卷回答"
        verbose_name_plural = verbose_name

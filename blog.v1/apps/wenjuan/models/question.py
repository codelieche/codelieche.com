# -*- coding:utf-8 -*-
from django.db import models

from account.models import User


class Job(models.Model):
    """
    问卷 Model
    """
    name = models.SlugField(verbose_name="网址", max_length=40, unique=True)
    title = models.CharField(verbose_name="标题", max_length=128)
    questions = models.ManyToManyField(verbose_name="问题", to="Question", blank=True)
    time_start = models.DateTimeField(verbose_name="开始时间", blank=True, null=True)
    # 问卷开始时间  过期时间
    time_expired = models.DateTimeField(verbose_name="过期时间", blank=True, null=True)
    description = models.CharField(verbose_name="描述", max_length=512)
    time_added = models.DateTimeField(verbose_name="添加时间", auto_now_add=True, blank=True)
    is_active = models.BooleanField(verbose_name="启用", blank=True, default=True)
    # 有些问卷是需要用户登录才可以回答的
    is_authenticated = models.BooleanField(verbose_name="需要用户登录", blank=True, default=True)
    # 添加个帮助链接
    help_title = models.CharField(verbose_name="帮助标题", max_length=128, blank=True, null=True)
    help_url = models.URLField(verbose_name="帮助链接", blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "问卷:Job"
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
    category = models.CharField(verbose_name="类型", choices=CATEGORY_CHOICES, max_length=10,
                                default="text", blank=True)
    # 回答的唯一性，通过在提交的时候做检验
    is_unique = models.BooleanField(verbose_name="回答需要唯一", blank=True, default=False)
    # 每一份问卷的问题，需要个先后顺序，如果不加会按照ID排序
    order = models.IntegerField(verbose_name="排序", blank=True, default=1)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "问题:Question"
        verbose_name_plural = verbose_name
        ordering = ("order", "id")


class Choice(models.Model):
    """
    答案选项Choice
    """
    question = models.ForeignKey(to="question", verbose_name="问题", related_name="choices", on_delete=models.CASCADE)
    option = models.CharField(verbose_name="选项", max_length=1)
    value = models.CharField(verbose_name="选项值", max_length=128)
    order = models.IntegerField(verbose_name="排序", blank=True, default=1)

    def __str__(self):
        return "{}:{}".format(self.question, self.value)

    class Meta:
        verbose_name = "问题答案选项:Question Choices"
        verbose_name_plural = verbose_name
        ordering = ("order", "id")


class Answer(models.Model):
    """
    回答Model
    """
    question = models.ForeignKey(to="question", verbose_name="问题", on_delete=models.CASCADE)
    option = models.CharField(verbose_name="回答选项", blank=True, max_length=1, null=True)
    answer = models.CharField(verbose_name="回答", max_length=128)

    def __str__(self):
        return "问题：(ID:{}):Answer:{}".format(self.question_id, self.answer)

    class Meta:
        verbose_name = "问题回答:Report Question Answer"
        verbose_name_plural = verbose_name


class Report(models.Model):
    """
    问卷回答 Model
    """
    job = models.ForeignKey(to="job", verbose_name="问卷", on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, verbose_name="用户", blank=True, null=True, on_delete=models.SET_NULL)
    ip = models.GenericIPAddressField(verbose_name="回答者IP", blank=True, null=True)
    time_added = models.DateTimeField(verbose_name="添加时间", blank=True, auto_now_add=True)
    answers = models.ManyToManyField(verbose_name="问卷回答", to="answer", blank=True)
    # 是否删除
    is_deleted = models.BooleanField(verbose_name="删除", blank=True, default=False)

    def __str__(self):
        return "Report:{}".format(self.pk)

    def __delete__(self, instance):
        if not self.is_deleted:
            self.is_deleted = True
            self.save()
        else:
            return True

    class Meta:
        verbose_name = "问卷回答:Report"
        verbose_name_plural = verbose_name

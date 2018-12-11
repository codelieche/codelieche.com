from django.contrib import admin

from question.models.question import Job, Question, Choice, Answer, Report

# Register your models here.


class JobModelAdmin(admin.ModelAdmin):
    """
    Job Model Admin
    """
    list_display = ("id", "title", "description", "time_added", "is_active", "is_authenticated")


class QuestionModelAdmin(admin.ModelAdmin):
    """
    Question Model Admin
    """
    list_display = ("id", "title", "description", "category", "is_unique")


class ChoiceModelAdmin(admin.ModelAdmin):
    """
    Choice Model Admin
    """
    list_display = ("id", "question", "option", "value")


class AnswerModelAdmin(admin.ModelAdmin):
    """
    Answer Model Admin
    """
    list_display = ("id", "question", "option", "answer")


class ReportModelAdmin(admin.ModelAdmin):
    """
    Report Model Admin
    """
    list_display = ("id", "job", "user", "ip", "time_added")


admin.site.register(Job, JobModelAdmin)
admin.site.register(Question, QuestionModelAdmin)
admin.site.register(Choice, ChoiceModelAdmin)
admin.site.register(Answer, AnswerModelAdmin)
admin.site.register(Report, ReportModelAdmin)

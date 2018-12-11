from django.contrib import admin

from question.models.question import Job, Question, Choice, Answer, Report

# Register your models here.

admin.site.register(Job)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Answer)
admin.site.register(Report)

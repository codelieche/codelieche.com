# -*- coding:utf-8 -*-
from rest_framework import generics


from question.models.question import Report
from question.serializer.report import ReportModelSerializer


class ReportCreateApiView(generics.CreateAPIView):
    """
    问卷回答api
    """
    queryset = Report.objects.all()
    serializer_class = ReportModelSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request=request, *args, **kwargs)

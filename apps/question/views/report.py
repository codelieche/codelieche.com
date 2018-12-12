# -*- coding:utf-8 -*-
from rest_framework import generics
from rest_framework.response import Response


from question.models.question import Report
from question.serializer.report import ReportModelSerializer, ReportDetailSerializer


class ReportCreateApiView(generics.CreateAPIView):
    """
    问卷回答api
    """
    queryset = Report.objects.all()
    serializer_class = ReportModelSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request=request, *args, **kwargs)


class ReportDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    """
    问卷回答api
    """
    queryset = Report.objects.all()
    serializer_class = ReportDetailSerializer

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if user.has_perm("question.delete_report"):
            # 调用父类的删除方法
            return super().delete(request=request, *args, **kwargs)
        else:
            content = {"status": False, "message": "无权限删除Report"}
            return Response(data=content, content_type="application/json", status=403)

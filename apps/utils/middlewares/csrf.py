# -*- coding:utf-8 -*-
"""
中间件
"""
from django.utils.deprecation import MiddlewareMixin


class ApiDisableCSRF(MiddlewareMixin):
    """API的请求都取消CSRF验证"""

    def is_api_request(self, request):
        """判断是否是qpi的请求"""
        path = request.path.lower()
        return path.startswith('/api/')

    def process_request(self, request):
        if self.is_api_request(request):
            # 给request设置属性，不要检验csrf token
            setattr(request, '_dont_enforce_csrf_checks', True)


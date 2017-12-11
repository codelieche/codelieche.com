# -*- coding:utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class LoginRequiredMixin(object):
    """
    View需要登陆才能访问Mixin
    """

    @method_decorator(login_required(login_url='/account/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class CsrfExemptMixin(object):
    """
    取消CSRF_TOKEN的验证Mixin
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CsrfExemptMixin, self).dispatch(request, *args, **kwargs)

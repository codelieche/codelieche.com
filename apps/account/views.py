# -*- coding:utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View

from .forms import LoginForm
# Create your views here.


class LoginView(View):
    """
    用户登陆
    """
    # print(request.COOKIES)
    # print(request.user) # AnonymousUser
    def get(self, request):
        url = request.get_full_path()
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form, 'url': url})

    def post(self, request):
        url = request.get_full_path()
        form = LoginForm(request.POST)
        if form.is_valid():
            form_cleaned = form.cleaned_data
            user = authenticate(username=form_cleaned['username'],
                                password=form_cleaned['password'])
            if user is not None:
                # 判断用户是否是激活的
                if user.is_active:
                    login(request, user)
                    # return HttpResponse('{sucess:true}')
                    next_url = request.GET.get('next', '/article/create')
                    return HttpResponseRedirect(redirect_to=next_url)
                else:
                    message = "用户非激活状态"
                    return HttpResponse('{sucess:false}')
            else:
                message = "用户名或者密码错误"
        else:
            # 数据清理后，不符合要求
            message = "输入的内容不合法"
        return render(request, 'account/login.html', {'form': form,
                                                      'url': url,
                                                      'msg': message})


def user_logout(request):
    """用户退出"""
    logout(request)
    next_url = request.GET.get('next', '/user/login')
    return HttpResponseRedirect(redirect_to=next_url)


def page_403(request):
    return render(request, '403.html')


def page_404(request):
    return render(request, '404.html')


def page_500(request):
    return render(request, '500.html')
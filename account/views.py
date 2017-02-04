#coding=utf-8
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .forms import LoginForm
# Create your views here.

def user_login(request):
    # print(request.COOKIES)
    # print(request.user) # AnonymousUser
    url = request.get_full_path()
    if request.method == "GET":
        form = LoginForm()
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            form_cleaned = form.cleaned_data
            user = authenticate(username=form_cleaned['username']
                                ,password=form_cleaned['password'])
            if user is not None:
                # 判断用户是否是激活的
                if user.is_active:
                    login(request, user)
                    # return HttpResponse('{sucess:true}')
                    next = request.GET.get('next','/article/create')
                    return HttpResponseRedirect(redirect_to=next)
                else:
                    return HttpResponse('{sucess:false}')
            else :
                return HttpResponse('{error:"用户名或者密码错误"}')
        else:
            # 数据清理后，不符合要求
            return HttpResponse("{sucess:false}")

    return render(request,'account/login.html',{'form':form,'url':url})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(redirect_to="/user/login")
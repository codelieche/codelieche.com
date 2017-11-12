# -*- coding:utf-8 -*-
from django.conf.urls import url
from account.views.user import LoginView, user_logout
# from django.contrib.auth import views as auth_views

app_name = "account"
urlpatterns = [
    url('^login$', LoginView.as_view(), name="login"),
    url('^logout$', user_logout, name='logout'),
]

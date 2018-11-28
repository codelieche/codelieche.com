# -*- coding:utf-8 -*-
from django.urls import path

from account.views.page.user import LoginPageView, user_logout
urlpatterns = [
    # 前缀：/account/
    path('login', LoginPageView.as_view(), name="login"),
    path('logout', user_logout, name="logout"),
]


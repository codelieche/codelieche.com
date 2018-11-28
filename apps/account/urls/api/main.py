# -*- coding:utf-8 -*-
from django.urls import path, include

from account.views.user import LoginView, account_logout

urlpatterns = [
    # 前缀：/api/v1/account/
    path('login', LoginView.as_view(), name="login"),
    path('logout', account_logout, name="logout"),

    # Account Group Api
    path('group/', include(arg=('account.urls.api.group', 'account'), namespace='group')),
    # Account User Api
    path('user/', include(arg=("account.urls.api.user", 'account'), namespace="user")),
    # Account Message Api
    path('message/', include(arg=('account.urls.api.message', 'account'), namespace="message")),
    # 权限
    path('permission/', include(arg=('account.urls.api.permission', 'account'),
                                namespace='permission')),
]

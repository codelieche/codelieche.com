#coding=utf-8
from django.conf.urls import url
from . import views
# from django.contrib.auth import views as auth_views

app_name = "account"
urlpatterns = [
    url('^login$', views.user_login, name="login"),
    # url('^logout$',auth_views.logout,name='logout'),
    url('^logout$', views.user_logout, name='logout'),
]
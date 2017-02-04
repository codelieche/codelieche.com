#coding=utf-8
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="用户名")
    password = forms.CharField(widget=forms.PasswordInput,label="密   码")
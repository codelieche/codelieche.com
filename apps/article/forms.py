# -*- coding:utf-8 -*-
from django import forms


class PostForm(forms.Form):
    """发布文章表单"""
    category = forms.IntegerField(widget=forms.Select, label="分类")
    title = forms.CharField(label="标题", max_length=200)
    content = forms.CharField(label="文章内容", widget=forms.Textarea)
    tags = forms.CharField(label="标签", required=False)
    status = forms.CharField(widget=forms.Select, label="状态")
    created = forms.DateTimeField(label="发布时间", required=False)
    top = forms.BooleanField(widget=forms.CheckboxInput, label="置顶", required=False)
    good = forms.BooleanField(widget=forms.CheckboxInput, label="精华", required=False)
    deleted = forms.BooleanField(widget=forms.CheckboxInput, label="删除", required=False)


class ImageForm(forms.Form):
    """图片上传表单"""
    filename = forms.ImageField(label="上传图片")





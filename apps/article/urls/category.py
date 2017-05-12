# -*- coding:utf-8 -*-
from django.conf.urls import url

from ..views import category

urlpatterns = [
    url(r'(?P<category_slug>[\w\d]+)', category.post_category_list,
        name="list"),
]

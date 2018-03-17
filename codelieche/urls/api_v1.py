# -*- coding:utf-8 -*-
from django.conf.urls import url, include

urlpatterns = [
    # url前缀：/api/v1/

    url(r'^utils/', include("utils.urls.api", "utils"), name="utils"),
]

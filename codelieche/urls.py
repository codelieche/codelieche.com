# -*- coding:utf-8 -*-
"""codelieche URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from django.conf.urls.static import static
from django.conf import settings

from account.views import page_403, page_404, page_500
from article.views.article import IndexPageView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #文章首页
    url(r'^$', IndexPageView.as_view(), name="index"),
    url(r'^page/(?P<page>\d+)/?$', IndexPageView.as_view(), name="page"),
    url(r'^article/', include('article.urls.article', namespace="article")),
    url(r'^category/', include('article.urls.category', namespace="category")),
    url(r'^user/', include('account.urls', namespace="user")),
    # api相关的url
    url(r'^api/1.0/', include('codelieche.api_urls', namespace='api')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# 这里还要添加下/media/xxx.jpg文件的路由，生产环境的时候是用nginx来部署静态文件的。

handler403 = page_403
handler404 = page_404
handler500 = page_500

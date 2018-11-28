# -*- coding:utf-8 -*-
from django.urls import path, include

urlpatterns = [
    # 前缀：/api/v1/article/
    # 文章分类
    path('category/', include(arg=("article.urls.api.category", "article"), namespace="category")),
    # 文章标签
    path('tag/', include(arg=("article.urls.api.tag", "article"), namespace="tag")),
    # 文章api
    path('post/', include(arg=("article.urls.api.post", "article"), namespace="post")),
    # 文章图片api
    path('image/', include(arg=("article.urls.api.image", "article"), namespace="image")),

]

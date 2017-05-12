# -*- coding:utf-8 -*-
from django.shortcuts import get_object_or_404, render

from article.models import Category, Post


def post_category_list(request, category_slug):
    # category = Category.objects.get(slug = category_slug)
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.published.filter(category=category)
    if posts:
        return render(request, "article/list.html", {"category": category, "posts": posts})
    else:
        return render(request, "article/list.html", {"category":category, "posts":[]})
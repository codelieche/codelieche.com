# -*- coding:utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.views.generic import View
from django.core.paginator import Paginator

from article.models import Category, Post


class ArticleListView(View):
    def get(self, request, slug, page=None):

        category = get_object_or_404(Category, slug=slug)
        # 超级用户才可以查看所有文章
        if request.user.is_superuser:
            all_posts = Post.objects.all().filter(category=category)
        else:
            all_posts = Post.published.filter(category=category)

        if page:
            page_num = int(page)
        else:
            page_num = 1

        p = Paginator(all_posts, 10)
        posts = p.page(page_num)
        page_count = p.num_pages

        if page_count <= 3:
            page_num_list = range(1, p.num_pages + 1)
        else:
            start = 1 if (page_num - 3) < 1 else (page_num - 3)
            end = page_count if (start + 6) > page_count else (start + 6)
            if end == page_count:
                start = end - 6 if (end-6) > 1 else 1
            page_num_list = range(start, end + 1)

        content = {
            'posts': posts,
            'category': category,
            'last_page': page_count,
            'page_num_list': page_num_list
        }
        return render(request, 'article/list.html', content)

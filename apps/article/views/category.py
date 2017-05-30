# -*- coding:utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.views.generic import View
from django.core.paginator import Paginator

from article.models import Category, Post
from utils.paginator import get_page_num_list


class ArticleListView(View):
    """
    分类文章列表View
    """
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

        # 获取分页器的页码列表，得到当前页面最近的7个页码列表
        page_num_list = get_page_num_list(page_count, page_num, 7)

        content = {
            'posts': posts,
            'category': category,
            'last_page': page_count,
            'page_num_list': page_num_list
        }
        return render(request, 'article/list.html', content)

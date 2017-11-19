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
        # 第1步：先获取到当前分类
        category = get_object_or_404(Category, slug=slug)

        # 第2步：获取分类的所有文章
        # 博客文章分类，只设置了2级，没有多级的，所以不需要对sub_category再次进行取子集
        sub_categories = category.category_set.all()

        # 超级用户可以查看所有文章【包含删除的】
        if request.user.is_superuser:
            all_posts = Post.objects.filter(category=category)
            # 联合sub_category的文章
            if sub_categories:
                sub_posts = Post.objects.filter(category__in=sub_categories)
                # 文章只能有一个分类，所以不会取到重复对象的
                all_posts = all_posts.union(sub_posts)
        else:
            all_posts = Post.published.filter(category=category)
            # 联合sub_category的文章
            if sub_categories:
                sub_posts = Post.objects.filter(category__in=sub_categories)
                # 文章只能有一个分类，所以不会取到重复对象的
                all_posts = all_posts.union(sub_posts)

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

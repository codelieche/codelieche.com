#coding:utf-8
from django.test import Client, TestCase
from django.urls import reverse

from article.models import Category

from .base import UnitTestBase

class HomePageTest(UnitTestBase):

    def test_home_page_render_home_template(self):
        '''测试首页使用的模版'''
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'article/list.html')

    def test_home_categories_nav(self):
        url = reverse('article:index')
        response = self.client.get(url)
        for category in Category.objects.all():
            self.assertContains(response, category.title)

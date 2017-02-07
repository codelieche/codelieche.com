#coding:utf-8
from django.test import TestCase
from django.contrib.auth.models import User
from article.models import Category, Tag, Post

class UnitTestBase(TestCase):
    '''单元测试基础类'''
    def setUp(self):
        '''初始化数据'''
        self.author = User(username='admin')
        self.author.set_password('admin123456')
        self.author.save()

        self.c1 = Category.objects.create(slug='front', title="前端开发")
        self.c2 = Category.objects.create(slug='backend', title="后端开发")

        self.t1 = Tag.objects.create(slug='python', name='python')

        self.p1 = Post.objects.create(title='python01', content='> python study',
                                 category=self.c1, author=self.author, status='published')
    def tearDown(self):
        pass
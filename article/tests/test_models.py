#coding:utf-8
from django.test import TestCase
from django.contrib.auth.models import User
from article.models import Category, Tag, Post

class CategoryModelTest(TestCase):

    def setUp(self):
        self.author = User(username='admin')
        self.author.set_password('admin123456')
        self.author.save()

        c1 = Category.objects.create(slug='front', title="前端开发")
        c2 = Category.objects.create(slug='backend', title="后端开发")

        t1 = Tag.objects.create(slug='python', name='python')

        p1 = Post.objects.create(title='python01', content='> python study',
                                 category=c1, author=self.author, status='published')
    def tearDown(self):
        pass

    
    def test_create_category(self):
        Category.objects.create(slug='ctest', title='ctest')
        self.assertEqual(Category.objects.count(), 3)


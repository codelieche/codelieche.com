#coding:utf-8
from django.test import TestCase
from django.contrib.auth.models import User
from article.models import Category, Tag, Post

class CategoryModelTest(TestCase):

    def setUp(self):
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

    
    def test_create_category(self):
        Category.objects.create(slug='ctest', title='ctest')
        self.assertEqual(Category.objects.count(), 3)

    def test_category_posts_count(self):
        Post.objects.create(title='python02', content='> python study2',
                            category=self.c1, author=self.author, status='published')
        self.assertEqual(self.c1.posts.count(), 2)

    def test_category_slug_is_unique(self):
        with self.assertRaises(Exception):
            Category.objects.create(slug='duplicate', title="重复分类")
            Category.objects.create(slug='duplicate', title="重复分类2")

    def test_category_title_is_unique(self):
        with self.assertRaises(Exception):
            Category.objects.create(slug='duplicate1', title="重复分类")
            Category.objects.create(slug='duplicate2', title="重复分类")



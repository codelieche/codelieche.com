# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-04 11:44
from __future__ import unicode_literals

import article.libs.storage
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=10, unique=True, verbose_name='分类网址')),
                ('title', models.CharField(max_length=40, unique=True, verbose_name='分类名称')),
            ],
            options={
                'verbose_name': '分类',
                'verbose_name_plural': '分类列表',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='评论内容')),
                ('name', models.CharField(default='匿名用户', max_length=40, verbose_name='用户名')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='评论时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('active', models.BooleanField(default=True, verbose_name='激活')),
            ],
            options={
                'verbose_name': '评论',
                'verbose_name_plural': '评论列表',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='标题')),
                ('content', models.TextField(verbose_name='文章内容')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('status', models.CharField(choices=[('published', '发布'), ('draft', '草稿')], default='published', max_length=10, verbose_name='状态')),
                ('top', models.BooleanField(default=False, verbose_name='置顶')),
                ('good', models.BooleanField(default=False, verbose_name='精华')),
                ('deleted', models.BooleanField(default=False, verbose_name='删除')),
                ('visit_count', models.IntegerField(default=0, verbose_name='访问量')),
                ('reply_count', models.IntegerField(default=0, verbose_name='回复数')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to=settings.AUTH_USER_MODEL, verbose_name='作者')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='article.Category', verbose_name='分类')),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章列表',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=15, verbose_name='网址')),
                ('name', models.CharField(max_length=30, verbose_name='名称')),
                ('hot', models.BooleanField(default=False, verbose_name='热门')),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签列表',
            },
        ),
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.ImageField(storage=article.libs.storage.ImageStorage(), upload_to='img/%Y/%m', verbose_name='图片')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='上传时间')),
                ('qiniu_url', models.CharField(blank=True, max_length=200, verbose_name='七牛Url')),
                ('deleted', models.BooleanField(default=False, verbose_name='删除')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '上传的图片',
                'verbose_name_plural': '上传的图片列表',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(related_name='articles', to='article.Tag', verbose_name='标签'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='article.Post', verbose_name='文章'),
        ),
    ]

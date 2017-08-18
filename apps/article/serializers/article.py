# -*- coding:utf-8 -*-
from rest_framework import serializers

from article.models import Post, Tag


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'content', 'created']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'hot']
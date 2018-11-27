# -*- coding:utf-8 -*-
from rest_framework import serializers

from article.models import Category, Post, Tag


class CategoryParentModelSerializer(serializers.ModelSerializer):
    """
    文章分类Model Serializer
    """

    class Meta:
        model = Category
        fields = ["id", "slug", "name", "parent"]


class CategorySubModelSerializer(serializers.ModelSerializer):
    """
    文章分类Model Serializer
    """

    class Meta:
        model = Category
        fields = ["id", "slug", "name", "parent"]


class CategoryModelSerializer(serializers.ModelSerializer):
    """
    文章分类Model Serializer
    """
    parent = CategoryParentModelSerializer()
    subs = CategorySubModelSerializer(many=True)

    class Meta:
        model = Category
        fields = ["id", "slug", "name", "parent", "subs"]


class TagModelSerializer(serializers.ModelSerializer):
    """文章标签Model Serializer"""

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'is_hot']


class PostModelSerializer(serializers.ModelSerializer):
    """文章Model Serializer"""
    category = serializers.SlugRelatedField(slug_field="slug", queryset=Category.objects.all())
    tags = serializers.SlugRelatedField(many=True, slug_field="slug", queryset=Tag.objects.all())

    class Meta:
        model = Post
        fields = ['id', "category", 'title', 'author', 'content', 'time_added', 'tags']

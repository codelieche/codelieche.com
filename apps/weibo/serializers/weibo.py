# -*- coding:utf-8 -*-
"""
weibo serializer
"""
from rest_framework import serializers

from account.models import User
from weibo.models.weibo import Image, Weibo, Comment


class ImageModelSerializer(serializers.ModelSerializer):
    """
    Image Model Serializer
    """

    user = serializers.SlugRelatedField(required=False, slug_field="username", read_only=False,
                                        queryset=User.objects.all())

    class Meta:
        model = Image
        fields = ("id", "user", "file", "filename", "storage", "url", "description")


class ImageInfoModelSerializer(serializers.ModelSerializer):
    """
    Image Model Serializer
    """

    class Meta:
        model = Image
        fields = ("id", "file", "filename", "storage", "url")


class CommentModelSerializer(serializers.ModelSerializer):
    """
    Webibo Comment Model Serializer
    """

    user = serializers.SlugRelatedField(slug_field="username", required=False, read_only=False,
                                        queryset=User.objects.all())

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user

        if user.is_authenticated:
            validated_data["user"] = user
        else:
            validated_data["user"] = None

        # 获取IP
        try:
            ip = request.META['HTTP_X_REAL_IP']
        except KeyError:
            ip = request.META["REMOTE_ADDR"]

        validated_data["address"] = ip

        instance = super().create(validated_data=validated_data)
        return instance

    class Meta:
        model = Comment
        fields = ("id", "user", "weibo", "content", "time_added", "address", "is_deleted")


class WeiboModelSerializer(serializers.ModelSerializer):
    """
    Weibo Model Serializer
    """
    user = serializers.SlugRelatedField(required=False, slug_field="username",
                                        read_only=False, queryset=User.objects.all())
    files = serializers.ListField(
        child=serializers.ImageField(
            allow_empty_file=False, use_url=False, max_length=1024000),
        allow_null=True,
        allow_empty=True
    )

    images = ImageInfoModelSerializer(required=False, many=True, read_only=True)
    comments = CommentModelSerializer(required=False, many=True, read_only=True,
                                      source="comment_set")

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user

        if user.is_authenticated:
            validated_data["user"] = user
        else:
            validated_data["user"] = None

        # 获取IP
        try:
            ip = request.META['HTTP_X_REAL_IP']
        except KeyError:
            ip = request.META["REMOTE_ADDR"]

        validated_data["address"] = ip

        # 根据传递的files获取到images
        files = validated_data.pop("files")

        # print(files)
        # for file_i in request.FILES["files"]:
        images = []
        for file_i in files:
            # 创建图片Model
            # print(file_i)
            info = {
                "filename": file_i.name,
                "user": user,
            }
            image_i = Image.objects.create(file=file_i, **info)
            images.append(image_i)
        validated_data["images"] = images
        instance = super().create(validated_data=validated_data)
        return instance

    class Meta:
        model = Weibo
        fields = ("id", "user", "content", "images", "video", "link", "address",
                  # "is_public", "time_added", "is_deleted",
                  "is_public", "time_added", "is_deleted", "files", "comments"
                  )


class WeiboSimpleModelSerializer(serializers.ModelSerializer):
    """
    Weibo Simple Model Serializer
    """
    user = serializers.SlugRelatedField(slug_field="username", required=False, read_only=True)
    images = ImageInfoModelSerializer(required=False, many=True, read_only=True)

    class Meta:
        model = Weibo
        fields = ("id", "user", "content", "images", "video", "link",
                  "is_public", "time_added", "is_deleted")


class CommentDetailModelSerializer(serializers.ModelSerializer):
    """
    Comment Detail Model Serializer
    """

    user = serializers.SlugRelatedField(slug_field="username", required=False, read_only=True)
    weibo = WeiboSimpleModelSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "weibo", "user", "content", "address", "time_added")



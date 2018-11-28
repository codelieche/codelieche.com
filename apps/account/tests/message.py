# -*- coding:utf-8 -*-
from django.test import TestCase

from account.models import UserProfile, MessageCategory, Message


class MessageCreateTestCase(TestCase):
    def setUp(self):
        # 准备测试用户
        user, created = UserProfile.objects.get_or_create(username="codelieche", email="test@codelieche.com")
        self.user = user
        # 准备消息
        category, created = MessageCategory.objects.get_or_create(category="default")
        Message.objects.create(user=user, title="测试消息", content="消息内容", category=category)

    def test_message_count(self):
        queryset = Message.objects.filter(user=self.user)
        # for i in queryset:
        #     print(i)
        self.assertGreaterEqual(queryset.count(), 1)

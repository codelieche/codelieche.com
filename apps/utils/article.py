# -*- coding:utf-8 -*-
from datetime import datetime, date
from random import randint
from article.models import Post


def create_article_id(created=None):
    '''根据created参数，创建一个数字id,有可能重复，需要自己判断下'''
    if not created:
        created = datetime.now()

    # 计算与2013-2-10相差天数
    # print(created,type(created))
    date_now = created.date()
    date_start = date(2013, 2, 10)
    days = (date_now - date_start).days

    num = randint(0, 100)
    article_id = "%d%s" % (days, str(num).zfill(2))

    article_id = int(article_id)
    if article_id < 0:
        article_id = abs(article_id)
    return article_id


def get_article_id(created=None):
    """
    获取文章pk，也就是主键id
    """
    count = 1
    article_id = 0
    while count > 0:
        article_id = create_article_id(created)
        count = Post.objects.filter(pk=article_id).count()
    article_id = int(article_id)
    if article_id < 0:
        article_id = abs(article_id)
    return article_id


def get_now():
    '''格式化now时间'''
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

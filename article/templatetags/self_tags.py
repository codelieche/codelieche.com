#coding=utf-8
from django import template
from django.db.models import Count
import markdown2
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter

from ..models import Category, Comment, Post, Tag

register = template.Library()
from datetime import datetime

# 自定义过滤器
# @register.filter(name="markdown", is_safe = True)
@register.filter(name="markdown")
@stringfilter
def markdown(value):
    # extras_flags = ['cuddled-lists','footnotes','code-friendly','fenced-code-blocks','footnotes']
    # value = value.replace('```','\n```')
    extras_flags = ['tables','cuddled-lists','footnotes','code-friendly','fenced-code-blocks','tag-friendly','pyshell','markdown-in-html']
    # html = markdown2.markdown(text=value, extras= extras_flags)
    html = mark_safe(markdown2.markdown(text=value, extras= extras_flags))
    return html



# 自定义模版标签
@register.assignment_tag()
def get_all_article_categories():
    '''
    获取文章分类列表
    '''
    return Category.objects.all()

@register.assignment_tag()
def get_all_article_tags():
    '''
    获取文章的所有标签
    :return: 返回所有文章的标签
    '''
    return Tag.objects.all()
@register.assignment_tag()
def get_hot_article_tags():
    '''
    获取文章的所有标签
    :return: 返回所有文章的标签
    '''
    return Tag.objects.filter(hot=True)

@register.inclusion_tag('article/latest_posts.html')
def get_latest_posts(count=5):
    '''
    获取最新的帖子
    :param count: 需要返回的文章数
    :return: 返回的是渲染好的html代码
    @register.inclusion_tag('article/latest_posts.html')
    '''
    latest_posts = Post.published.order_by('-created')[:count]
    return {'latest_posts':latest_posts}

@register.assignment_tag(name="get_most_polular_posts")
def get_most_popular_posts(count=5):
    '''
    返回最受欢迎的帖子，暂时是按照访问量，后续改成评论数
    :param count: 返回的数量
    :return: 返回的是一个数组，可以在模版中用for标签使用
    '''
    most_popular_posts = Post.published.order_by('-visit_count')[:count]
    return most_popular_posts

#获取相似的帖子
@register.assignment_tag()
def get_similar_posts(post,count=5):
    post_tags_ids = post.tags.values_list('id', flat=True)
    if not post_tags_ids: return None #如果没标签就返回空
    #获取与post相同标签的文章，然后排除自己
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('id'))\
                                    .order_by('-same_tags','-created')[:count]
    return similar_posts

@register.assignment_tag()
def get_now():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S" )

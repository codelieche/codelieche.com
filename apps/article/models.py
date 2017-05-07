# -*- coding:utf-8 -*-
# from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from utils.storage import ImageStorage


# Create your models here.

# 文章分类
@python_2_unicode_compatible
class Category(models.Model):
    slug = models.SlugField(max_length=10, verbose_name="分类网址", unique=True)
    title = models.CharField(max_length=40, verbose_name="分类名称", unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = "分类列表"


# 创建标签类
@python_2_unicode_compatible
class Tag(models.Model):
    slug = models.SlugField(max_length=15, verbose_name="网址", blank=True)
    name = models.CharField(max_length=30, verbose_name="名称")
    hot = models.BooleanField(default=False, verbose_name="热门")

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签列表"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        '''自动创建标签，slug设置为一个数字'''
        if not self.slug:
            self.slug = Tag.objects.count()
        super(Tag, self).save(*args, **kwargs)

    @staticmethod
    def get_or_create(name):
        # 根据传递的name  获取tag对象，或者创建对象,并返回创建的对象
        # 这个方法，在create,editor的时候 都要用到
        t = Tag.objects.filter(name__iexact=name)
        if t:
            return t[0]
        else:
            tag = Tag(name=name)
            tag.save()
            return tag

    def get_absolute_url(self):
        """tag的绝对路径"""
        return reverse('post_tag_list', args=[self.name])


# 自定义文章的manager
class PostPublishedManager(models.Manager):
    def get_queryset(self):
        return super(PostPublishedManager,self).get_queryset().filter(status='published',deleted=False)


# 文章模型
@python_2_unicode_compatible
class Post(models.Model):
    """
    文章有两种状态：published(发布),draft(草稿)
    title(标题),content(内容),author(作者),category(分类),created(创建时间),updated(更新时间)
    top(置顶),good(精华),deleted(删除)
    visit_count(阅读量),reply_count(回复数)
    管理器有：objects(所有文章包括草稿),published(所有是发布状态的文章)
    标签：用到了django-taggit来管理标签，
    文章访问的时候需要增加一次visit_count，对象save的时候需要添加update_fields参数.
    ```
    p1 = Post.objects.get(pk=1)
    p1.visit_count += 1
    p1.save(update_fields=['visit_count'])
    ```
    """
    # 文章有草稿、发布、两种状态
    STATUS_CHOICES = (
        ("published", "发布"),
        ("draft", "草稿")
    )
    # 文章标题
    title = models.CharField(max_length=200, verbose_name="标题")
    # 文章内容 markdown
    content = models.TextField(verbose_name="文章内容")
    # 文章内容 html
    # content_html = models.TextField(verbose_name="文章内容html",blank=True)
    # 文章作者
    author = models.ForeignKey(User, related_name='articles', verbose_name="作者")
    # 文章分类
    category = models.ForeignKey(Category, related_name="posts", verbose_name="分类")
    # related_name 是可以让 category对象.posts获取所有的帖子

    # 创建时间
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    # 更新时间
    updated = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    # 帖子状态 发布/草稿
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default='published', verbose_name="状态")

    # 帖子是否置顶
    top = models.BooleanField(default=False, verbose_name="置顶")
    # 帖子是否精华
    good = models.BooleanField(default=False, verbose_name="精华")
    # 帖子是否删除
    deleted = models.BooleanField(default=False, verbose_name="删除")

    # 帖子访问统计
    visit_count = models.IntegerField(default=0, verbose_name="访问量")
    # 帖子回复数
    reply_count = models.IntegerField(default=0, verbose_name="回复数")

    # 管理器 mannager， 默认只有objects
    objects = models.Manager() # 默认的manager
    published = PostPublishedManager() # 自定义的manager

    # 文章的标签，依赖django-taggit库
    # tags = TaggableManager() # Post.tags.all() / pObj.tags.all()
    # tags = TaggableManager(through=TaggedItem) # Post.tags.all() / pObj.tags.all()
    tags = models.ManyToManyField(to=Tag, related_name='articles', verbose_name="标签")
    #获取打了标签的对象  t1.taggit_taggeditem_items.all() t1是Taggit的Tag对象
    # 用了自定义的TaggedItem,设置related_name为articles，
    # 那么通过：t1.articles.all()可以获取所有打了t1标签的文章对象的pk
    # 通过标签slug获取Post：posts = Post.published.filter(tags__slug__in=[tag_slug])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """获取文章的绝对路径"""
        return reverse('article:post_detail', kwargs={'pk': self.pk})

    # model元数据
    class Meta:
        # 排序
        ordering = ('-created',)
        verbose_name = "文章"
        verbose_name_plural = "文章列表"


# 文章评论
@python_2_unicode_compatible
class Comment(models.Model):
    # user = models.ForeignKey(User,related_name='comments',verbose_name="用户")
    # 是哪条文章的评论
    post = models.ForeignKey(Post, related_name="comments", verbose_name="文章")
    # 评论内容
    content = models.TextField(verbose_name="评论内容")
    name = models.CharField(verbose_name="用户名", max_length=40, default="匿名用户")

    # 评论时间
    created = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")
    # 更新时间
    updated = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    # 评论是否可以查看，是否是激活的
    active = models.BooleanField(default=True, verbose_name="激活")

    class Meta:
        ordering = ('-created',)
        verbose_name = "评论"
        verbose_name_plural = "评论列表"

    def __str__(self):
        return "评论 {} ".format(self.content)


@python_2_unicode_compatible
class Upload(models.Model):
    user = models.ForeignKey(User, related_name='images', verbose_name="用户")
    filename = models.ImageField(upload_to="img/%Y/%m", storage=ImageStorage(), verbose_name="图片")
    created = models.DateTimeField(auto_now_add=True, verbose_name="上传时间")
    qiniu_url = models.CharField(verbose_name="七牛Url", blank=True, max_length=200)
    deleted = models.BooleanField(default=False, verbose_name="删除")

    def __str__(self):
        return str(self.filename)

    class Meta:
        verbose_name = "上传的图片"
        verbose_name_plural = "上传的图片列表"






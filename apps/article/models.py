# -*- coding:utf-8 -*-
# from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.encoding import python_2_unicode_compatible

from utils.storage import ImageStorage
# Create your models here.


User = get_user_model()


@python_2_unicode_compatible
class Category(models.Model):
    """
    文章分类 Model
    """
    slug = models.SlugField(max_length=10, verbose_name="分类网址",
                            unique=True, help_text="文章分类网址")
    name = models.CharField(max_length=40, verbose_name="分类名称",
                            unique=True, help_text="文章分类名称")
    parent = models.ForeignKey(to="self", verbose_name="父级目录", blank=True, null=True,
                               help_text="父级目录")
    level = models.IntegerField(blank=True, default=1, verbose_name="目录级别", help_text="目录级别")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # 目录有级别的，每次分类的保存，自动计算level值
        level = 1
        parent = self.parent
        while parent:
            parent = parent.parent
            level += 1
        self.level = level
        super(Category, self).save(force_insert=force_insert, force_update=force_update,
                                   using=using, update_fields=update_fields)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "文章分类"
        verbose_name_plural = "文章分类列表"


@python_2_unicode_compatible
class Tag(models.Model):
    """
    文章标签 Model
    """
    slug = models.SlugField(max_length=15, verbose_name="网址", blank=True,
                            help_text="标签网址")
    name = models.CharField(max_length=30, verbose_name="标签名", help_text="标签名称")
    is_hot = models.BooleanField(default=False, verbose_name="热门", help_text="是否是热门标签")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        对象保存，如果标签的slg为空，给它赋值个数字
        """
        if not self.slug:
            self.slug = Tag.objects.count()
        super(Tag, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签列表"

    def get_absolute_url(self):
        """tag的绝对路径"""
        return reverse('post_tag_list', args=[self.name])


class PostPublishedManager(models.Manager):
    """
    自定义文章的manager
    获取状态是published的文章，且未删除
    """
    def get_queryset(self):
        return super(PostPublishedManager, self).get_queryset().filter(status='published',
                                                                       deleted=False)


@python_2_unicode_compatible
class Post(models.Model):
    """
    文章Model
    文章有两种状态：published(发布), draft(草稿)
    字段说明：
        1. title：标题
        2. content：文章内容
        3. author：文章作者
        4. category：文章分类
        5. time_created：创建时间
        6. time_updated：更新时间
        7. is_top: 是否置顶
        8. is_good: 是否精华
        9. deleted: 已删除
        10. visit_count: 阅读量
        11. reply_count: 评论回复数
    管理器：
        1. objects：所有文章包含草稿
        2. published：所有是发布状态的文章
    标签：多对多关系
    说明：修改文章访问量的时候，save要传递update_fields参数。
    ```
    p1 = Post.objects.get(pk=1)
    p1.visit_count += 1
    p1.save(update_fields=['vist_count'])
    ```
    """
    # 文章有草稿、发布两种状态，通过`p.get_status_display()`可以得到中文的状态
    STATUS_CHOICES = (
        ('published', '发布'),
        ('draft', '草稿')
    )
    title = models.CharField(max_length=128, verbose_name="标题", help_text="文章标题")
    content = models.TextField(verbose_name="文章内容", help_text="文章内容")
    # 关于related默认是：appname_set，很多时候推荐使用默认的
    author = models.ForeignKey(to=User, related_name='articles', verbose_name="作者",
                               help_text="文章作者")
    category = models.ForeignKey(to=Category, verbose_name="分类", help_text="文章分类")

    time_added = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", blank=True,
                                      help_text="文章创建时间")
    time_updated = models.DateTimeField(auto_now=True, verbose_name="更新时间", blank=True,
                                        help_text="更新文章时间")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published',
                              blank=True, verbose_name="状态",
                              help_text="文章状态(draft/published)")

    is_top = models.BooleanField(verbose_name="置顶", default=False, blank=True,
                                 help_text="文章置顶")
    is_good = models.BooleanField(verbose_name="精华", default=False, blank=True,
                                  help_text="精华文章")
    deleted = models.BooleanField(verbose_name="已删除", default=False, blank=True,
                                  help_text="文章已删除")

    visit_count = models.IntegerField(verbose_name="阅读量", default=0, blank=True,
                                      help_text="文章阅读数")
    reply_count = models.IntegerField(verbose_name="回复数", default=0, blank=True,
                                      help_text="文章回复数")

    # 管理器，默认只有objects，自己加了published
    objects = models.Manager()
    # 注意是PostPublishedManager的实例哦
    published = PostPublishedManager()

    tags = models.ManyToManyField(to=Tag, related_name='articles', verbose_name="标签",
                                  help_text="文章标签")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """获取文章的绝对路径"""
        return reverse('article:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ('-time_added', )
        verbose_name = '文章'
        verbose_name_plural = '文章列表'


@python_2_unicode_compatible
class Comment(models.Model):
    """
    文章评论
    """
    post = models.ForeignKey(to=Post, related_name="comments", verbose_name="文章",
                             help_text="评论文章")
    content = models.CharField(max_length=512, verbose_name="评论内容", help_text="评论内容")
    user = models.ForeignKey(to=User, verbose_name="用户", blank=True, help_text="用户")
    ip = models.GenericIPAddressField(verbose_name="用户IP", blank=True, null=True,
                                      help_text="评论者IP地址")
    time_added = models.DateTimeField(auto_now_add=True, verbose_name="评论时间", blank=True)
    time_updated = models.DateTimeField(auto_now=True, verbose_name="评论更新时间", blank=True)
    deleted = models.BooleanField(verbose_name="删除评论", blank=True, default=False,
                                  help_text="删除评论")

    def __str__(self):
        return "评论{}({})".format(self.pk, self.user)

    class Meta:
        ordering = ('-time_added',)
        verbose_name = "评论"
        verbose_name_plural = "评论列表"


@python_2_unicode_compatible
class Image(models.Model):
    """
    文章图片Model
    """
    user = models.ForeignKey(to=User, related_name="article_images", verbose_name="上传者",
                             blank=True, help_text="用户")
    filename = models.CharField(max_length=100, verbose_name="图片名", blank=True,
                                help_text="图片名称")
    url = models.ImageField(upload_to="img/article/%Y/%m", storage=ImageStorage(),
                            verbose_name="图片", help_text="图片路径")
    time_added = models.DateTimeField(verbose_name="上传时间", auto_now_add=True, blank=True,
                                      help_text="上传时间")
    deleted = models.BooleanField(verbose_name="删除", blank=True, default=False,
                                  help_text="删除图片")

    def __str__(self):
        return "image:{}".format(self.filename)

    class Meta:
        verbose_name = "图片"
        verbose_name_plural = "图片列表"

from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from utils.store import ImageStorage

# Create your models here.

User = get_user_model()


class Category(models.Model):
    """
    文章分类Model
    """
    slug = models.SlugField(max_length=10, verbose_name="分类网址", unique=True, help_text="文章分类网址")
    name = models.CharField(max_length=40, verbose_name="分类名称", unique=True, help_text="文章分类名称")
    parent = models.ForeignKey(to="self", verbose_name="父级分类", blank=True, null=True, help_text="父级分类",
                               related_name="subs", on_delete=models.CASCADE)
    level = models.SmallIntegerField(blank=True, default=1, verbose_name="分类级别", help_text="分类级别")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # 分类有级别的，每次分类保存的时候，自动计算level值
        level = 1
        parent = self.parent
        while parent:
            parent = parent.parent
            level += 1
        self.level = level
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "文章分类"
        verbose_name_plural = verbose_name


class Tag(models.Model):
    """
    文章标签Model
    """
    slug = models.SlugField(max_length=15, verbose_name="网址", blank=True, help_text="标签网址")
    name = models.CharField(max_length=30, verbose_name="标签名", help_text="标签名称")
    is_hot = models.BooleanField(default=False, verbose_name="热门", help_text="是否是热门标签")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # 对象保存，如果标签的slug为空，就给它个数字
        if not self.slug:
            self.slug = Tag.objects.count()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Tag对象的绝对路径"""
        return reverse('pages:article:detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name


class PostPublishedManager(models.Manager):
    """
    自定义文章的Manager
    获取状态是published的文章，且未删除
    """
    def get_queryset(self):
        return super().get_queryset().filter(status="published", is_deleted=False)


class Post(models.Model):
    """
    文章Model
    文章有两种状态：published(发布)，draft(草稿)
    字段说明：
        1. title: 标题
        2. content：文章内容
        3. author：文章作者
        4. category：文章分类
        5. time_created: 创建时间
        6. time_updated: 更新时间
        7. is_top: 是否制定
        8. is_good: 是否精华
        9. is_deleted: 是否删除
        10. visit_count: 阅读数
        11. reply_count: 评论回复数
    管理器：
        1. objects: 所有文章【默认】
        2. published: 所有是发布状态的文章【自定义】
    标签：多对多关系
    说明：修改文章访问量的时候，save要传update_fields参数
    ```
    p1 = Post.objects.get(pk=1)
    p1.visit_count += 1
    p1.save(update_fields=['visit_count']
    ```
    """
    # 文章有草稿、发布两种状态，通过`p.get_status_display()`可以得到中文的状态
    STATUS_CHOICES = (
        ('published', '发布'),
        ('draft', '草稿')
    )
    title = models.CharField(max_length=128, verbose_name="标题", help_text="文章标题")
    content = models.TextField(verbose_name="文章内容", help_text="文章内容")
    # 关于related_name默认是：appname_set,很多时候推荐使用默认的:比如：u.post_set.all()
    author = models.ForeignKey(to=User, related_name='articles', verbose_name="作者", help_text='文章作者',
                               on_delete=models.CASCADE)
    category = models.ForeignKey(to=Category, verbose_name="分类", help_text="文章分类", on_delete=models.CASCADE)

    time_added = models.DateTimeField(verbose_name="创建时间", auto_now_add=True, blank=True, help_text="文章创建时间")
    time_updated = models.DateTimeField(verbose_name="更新时间", auto_now=True, blank=True, help_text="文章更新时间")
    status = models.CharField(verbose_name="状态", max_length=10, choices=STATUS_CHOICES, default='published',
                              blank=True, help_text="文章状态(draft/published)")
    tags = models.ManyToManyField(to=Tag, related_name="articles", verbose_name="标签", help_text="文章标签")

    is_top = models.BooleanField(verbose_name="置顶", default=False, blank=True, help_text="文章置顶")
    is_good = models.BooleanField(verbose_name="精华", default=False, blank=True, help_text="精华文章")
    is_deleted = models.BooleanField(verbose_name="已删除", default=False, blank=True, help_text="文章已删除")
    visit_count = models.IntegerField(verbose_name="阅读量", default=0, blank=True, help_text="文章阅读数")
    reply_count = models.IntegerField(verbose_name="回复数", default=0, blank=True, help_text="文章回复数")

    # 管理器，默认只有objects，自己加了published
    objects = models.Manager()
    # 注意PostPublishedManager的实例哦
    published = PostPublishedManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """获取文章的绝对路径"""
        return reverse('pages:article:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ('-time_added',)
        verbose_name = "文章"
        verbose_name_plural = verbose_name


class Comment(models.Model):
    """
    文章评论
    """
    post = models.ForeignKey(to=Post, related_name="comments", verbose_name="文章", help_text="评论文章",
                             on_delete=models.CASCADE)
    content = models.CharField(verbose_name="评论内容", max_length=512, help_text="评论内容")
    user = models.ForeignKey(verbose_name="用户", to=User, help_text="评论用户", blank=True, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(verbose_name="用户IP", help_text="评论者IP地址", blank=True, null=True)
    time_added = models.DateTimeField(verbose_name="添加时间", auto_now_add=True, blank=True)
    time_updated = models.DateTimeField(verbose_name="更新时间", auto_now=True, blank=True)
    is_deleted = models.BooleanField(verbose_name="删除", blank=True, default=False, help_text="删除评论")

    def __str__(self):
        return "评论{}({})".format(self.pk, self.user)

    class Meta:
        ordering = ("-time_added",)
        verbose_name = "文章评论"
        verbose_name_plural = verbose_name


class Image(models.Model):
    """
    文章图片Model
    """
    user = models.ForeignKey(verbose_name="上传者", to=User, related_name="article_images", null=True,
                             blank=True, help_text="上传者", on_delete=models.SET_NULL)
    filename = models.CharField(verbose_name="图片名", max_length=100, blank=True, help_text="图片名称")
    url = models.ImageField(verbose_name="图片", upload_to="img/article/%Y/%m", storage=ImageStorage(),
                            help_text="图片路径")
    time_added = models.DateTimeField(verbose_name="上传时间", auto_now_add=True, blank=True, help_text="上传时间")
    is_deleted = models.BooleanField(verbose_name="删除", blank=True, default=False, help_text="删除图片")

    def __str__(self):
        return "Image:{}".format(self.filename)

    class Meta:
        verbose_name = "图片"
        verbose_name_plural = verbose_name


class UserData(models.Model):
    """
    用户数据，保存临时文章等
    不同用户有一些临时碎片信息，在不同session中要用到的数据
    """
    TYPE_CHOICE = (
        ('article', "临时文章"),
        ('comment', '临时评论')
    )
    user = models.ForeignKey(to=User, related_name="userdatas", on_delete=models.CASCADE)
    type = models.CharField(verbose_name="类型", max_length=20, choices=TYPE_CHOICE)
    content = models.TextField(verbose_name="信息内容")
    time_updated = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return "%s -> %s" % (self.user, self.type)

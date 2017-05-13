# -*- coding:utf-8 -*-
import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.core.paginator import Paginator

from account.models import UserData
from utils.article import get_article_id
from article.forms import PostForm, ImageForm
from article.models import Category, Post, Tag, Upload
# Create your views here.


class IndexPageView(View):
    def get(self, request, page=0):
        # 超级用户才可以查看所有文章
        if request.user.is_superuser:
            all_posts = Post.objects.all()
        else:
            all_posts = Post.published.all()

        if page:
            page_num = int(page)
        else:
            page_num = 1

        p = Paginator(all_posts, 10)
        posts = p.page(page_num)
        page_count = p.num_pages

        if page_count <= 7:
            page_num_list = range(1, p.num_pages + 1)
        else:
            start = 1 if (page_num - 3) < 1 else (page_num - 3)
            end = page_count if (start + 6) > page_count else (start + 6)
            page_num_list = range(start, end + 1)

        content = {
            'posts': posts,
            'last_page': page_count,
            'page_num_list': page_num_list
        }
        return render(request, 'article/page.html', content)


class ArticleTagListView(View):
    def get(self, request, tag_name, page=0):
        # 先取出tag
        tag = get_object_or_404(Tag, slug=tag_name)
        # print(tag)
        # 超级用户才可以查看所有文章
        if request.user.is_superuser:
            all_posts = tag.articles.all()
        else:
            all_posts = tag.articles.all().filter(status='published')
        if page:
            page_num = int(page)
        else:
            page_num = 1

        # 分页
        p = Paginator(all_posts, 10)
        posts = p.page(page_num)
        # 总共页数
        page_count = p.num_pages

        # 生成页列表
        if page_num < 7:
            page_num_list = range(1, p.num_pages + 1)
        else:
            start = 1 if (page_num - 3) < 1 else (page_num - 3)
            end = page_count if (start + 6) > page_count else (start + 6)
            page_num_list = range(start, end + 1)

        # 渲染主体内容
        content = {
            'tag': tag,
            'posts': posts,
            'last_page': page_count,
            'page_num_list': page_num_list
        }

        # posts = Post.published.filter(tags__name__in=[tag_name])
        return render(request, "article/list_tag.html", content)


class PostDetailView(View):
    """
    文章详情页View
    每次访问都需要增加以下阅读量，visit_count
    更新阅读量的时候，要传递update_fields=['visit_count']
    默认Model.save方法的参数update_fields=None,不传值，同时会修改掉updated字段的数据
    """
    def get(self, request, pk):
        # 根据pk获取到文章
        post = get_object_or_404(Post, pk=pk)
        # 阅读次数+1
        post.visit_count += 1
        post.save(update_fields=['visit_count'])

        # 根据状态判断是草稿还是已发布
        if post.author == request.user:
            if post.status == 'draft':
                pre_title = "【草稿】"
                post.title = pre_title + post.title
            elif post.deleted:
                pre_title = "【删除】"
                post.title = pre_title + post.title
        else:
            if post.status == 'draft' or post.delete:
                raise Http404
        return render(request, 'article/detail.html', {"post": post})


@login_required(login_url="/user/login")
def create(request):
    ud = None
    # 从UserData中获取type为article的数据
    try:
        # ud = UserData.objects.get(type="article",user=request.user)
        ud = request.user.userdatas.get(type="article")
    except ObjectDoesNotExist:
        # article的数据还不存在，那么就创建一个吧
        ud = UserData(user=request.user, type="article", content="")
    # ud.content中的false,true没有加双引号的，所以这里定义一下，false，true
    false = False
    true = True
    if ud.content:
        post = json.loads(ud.content)
    else:
        # 当post创建了之后，UserData.content的内容变成空了
        post = {}
    # 也可以用 post = dict(eval(ud.content)) 但是能不用eval就不要用eval

    categories = Category.objects.all()

    if request.method == "POST":
        # print(request.POST)
        form = PostForm(request.POST)
        # 获取了提交过来的form数据后 验证是否正确，以及获取cleaned_data
        # print(form)
        if form.is_valid():
            form = form.cleaned_data
            category = Category.objects.get(pk=form['category'])
            title = form['title']
            content = form['content']
            status = form['status']
            tags = form['tags']
            if tags.find('，') > 0:
                tags = tags.replace("，", ",")
            top = form['top']
            good = form['good']
            deleted = form['deleted']
            created = form['created']
            post_pk = get_article_id(created)
            # print(category,title,content,status,tags)
            post = Post(pk=post_pk, category=category, title=title, content=content,
                        status=status, author=request.user,
                        top=top, good=good, deleted=deleted)

            # print(post.tags)
            post.save()
            post.created = created
            post.save(update_fields=['created'])
            # 文章保存后，要对 UserData中的article的内容清空
            ud.content = ""
            ud.save()
            if tags:#如果有值则添加tag
                for tag in tags.split(','):
                    if not tag: continue #如果tag为空就跳过一下
                    # get_or_create是Tag的静态方法
                    tag = Tag.get_or_create(name=tag.strip())  # 必须加strip，去除首位空格
                    post.tags.add(tag)
            if post.deleted:
                return HttpResponseRedirect(redirect_to="/")
            else:
                # return HttpResponseRedirect(redirect_to="/article/%s" % post.pk)
                return redirect(post)

        # 如果表单没有验证成功，就重新进入编辑页面
        return HttpResponseRedirect(redirect_to="/article/create")

    else:
        return render(request, "article/create.html", {"post":post, "categories":categories})


@login_required(login_url="/user/login")
def editor(request, pk=None):
    '''文章编辑view'''
    categories = Category.objects.all()
    # 得到 编辑的文章对象
    post = Post.objects.get(pk=pk)
    # print(post.author == request.user)
    # print(post.author)
    if request.method == "POST":
        # print(request.POST)
        form = PostForm(request.POST)
        # 获取了提交过来的form数据后 验证是否正确，以及获取cleaned_data
        # print(form)
        if form.is_valid() and post.author == request.user:
            form = form.cleaned_data
            category = Category.objects.get(pk=form['category'])
            title = form['title']
            content = form['content']
            status = form['status']
            tags = form['tags']
            if tags.find('，') > 0:
                tags = tags.replace("，", ",")
            top = form['top']
            good = form['good']
            deleted = form['deleted']
            # print(category,title,content,status,tags,deleted)
            # 修改post对象的 分类，标题，内容，状态，author，top，good信息
            post.category = category
            post.title = title
            post.content = content
            post.status = status
            post.top = top
            post.good = good
            post.deleted = deleted
            # print(post.tags.all())
            post.save()
            if tags:  # 如果有值则添加tag
                for tag in tags.split(','):
                    if not tag: continue  # 如果tag为空就跳过一下
                    # get_or_create是Tag的静态方法
                    tag = Tag.get_or_create(name=tag.strip())  # 必须加strip，去除首位空格
                    post.tags.add(tag)
            if deleted:
                return HttpResponseRedirect("/")
        # return HttpResponseRedirect(redirect_to="/article/%s" % post.pk)
        return redirect(post)
    else:
        form = PostForm()
    return render(request, "article/editor.html", {"post": post, "categories": categories})


@login_required(login_url="/user/login")
def save(request):
    '''创建文章中途保存'''
    # 从UserData中获取type为article的数据
    try:
        # ud = UserData.objects.get(type="article",user=request.user)
        ud = request.user.userdatas.get(type="article")
    except ObjectDoesNotExist:
        # article的数据还不存在，那么就创建一个吧
        ud = UserData()
    post = Post()
    if request.method == "POST":
        # print(request.POST)
        form = PostForm(request.POST)
        # 获取了提交过来的form数据后 验证是否正确，以及获取cleaned_data
        # print(form) #还没cleaned_data是些html标签
        if form.is_valid():
            form = form.cleaned_data
            # 把form转成dict，再用json.dumps成字符串，方便在create中转成字典
            ud.content = json.dumps(dict(form))
            # print(json.dumps(dict(form)))
            # print(form)
            ud.user = request.user
            ud.save()
            return HttpResponse(json.dumps({"sucess":True}), content_type="application/json")
        return HttpResponse(json.dumps({"sucess": False}),
                            content_type="application/json")
    else:
        # /article/save 只能是POST访问
        return HttpResponse(status=404)


@login_required(login_url="/user/login")
def upload_image(request):
    '''上传图片'''
    if request.method == "GET":
        form = ImageForm()
    else:
        form = ImageForm(request.POST, request.FILES)
        # file = request.FILES['filename']
        # print(dir(request.FILES['filename']))
        # print(file.size)
        if form.is_valid():
            image = Upload(filename=form.cleaned_data['filename'],
                           user=request.user)
            image.save()
            response_data = {
                'success': 'true',
                'url': '/media/%s' % image,
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'success': 'false'}, status=400)
    return render(request, "article/upload_image.html", {'form': form})

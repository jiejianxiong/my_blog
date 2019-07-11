from django.shortcuts import render,redirect

from .models import ArticlePost
from django.http import HttpResponse
from .forms import ArticlePostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import markdown
from django.core.paginator import Paginator

# 视图函数
def article_list(request):
    # 取出所有博客文章
    article_list = ArticlePost.objects.all()

    # 每页显示6篇文章
    paginator = Paginator(article_list,9)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象对应的页码内容返回给articles
    articles = paginator.get_page(page)

    # 需要传递给模板的对象
    context = {'articles':articles}
    # 载入模板，并返回context对象
    return render(request,'article/list.html',context)

# 文章详情
def article_detail(request,id):
    # 取出相应文章
    article = ArticlePost.objects.get(id=id)

    # 浏览量 +1
    article.total_views += 1
    article.save(update_fields=['total_views'])

    # 将markdown语法渲染成html样式
    article.body = markdown.markdown(article.body,
                                     extensions=[
                                         # 包含 缩写、表格等常用扩展
                                         'markdown.extensions.extra',
                                         # 语法高亮扩展
                                         'markdown.extensions.codehilite',
                                     ])
    # 需要传递给模板的对象
    context = { 'article':article }
    # 载入模板 返回context对象
    return render(request,'article/detail.html',context)

# 写文章的视图
@login_required(login_url='/userprofile/login/')
def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=request.user.id)
            # 指定数据库中id = 1的用户为作者
            # 如果曾经删过数据库的话，可能会找不到id=1的作者
            # 重新创建新用户，传入用户id=1
            # 将新文章保存到数据库中
            new_article.save()
            # 返回文章列表
            return redirect("article:article_list")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写")

    # 如果用户请求数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文
        context = {'article_post_form':article_post_form}
        # 返回模板
        return render(request,'article/create.html',context)

# 删除文章
@login_required(login_url='/userprofile/login/')
def article_delete(request,id):
    # 根据id获取需要删除的文章
    article = ArticlePost.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse('抱歉，您无权删除这篇文章，详情请联系站长')
    # 调用.delete方法删除文章
    article.delete()
    # 完成删除后返回文章列表
    return redirect("article:article_list")

# 修改文章
@login_required(login_url='/userprofile/login/')
def article_update(request,id):
    """
    更新文章的视图函数
    通过post方法提交表单，更新title，body字段
    get方法进入初始表单页面
    :param request:
    :param id: 文章的id
    :return:
    """
    # 获取需要修改的文章对象
    article = ArticlePost.objects.get(id=id)

    # 过滤非作者的用户
    if request.user != article.author:
        return HttpResponse('抱歉，你无权修改这篇博客!')
    # 判断用户是否为post提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的title,body 数据并保存
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            # 完成后返回到修改后的文章中，需传入文章的 id 值
            return redirect("article:article_detail",id=id)
        # 如果数据不合法 返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写")

    # 如果是get请求
    else:
        # 创建表单实例
        article_post_form = ArticlePostForm()
        # # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = {'article':article,'article_post_form':article_post_form}
        # 将响应返回到模板中
        return render(request,'article/update.html',context)








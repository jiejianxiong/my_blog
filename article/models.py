from django.db import models

from django.contrib.auth.models import User

from django.utils import timezone

# 博客文章数据模型
class ArticlePost(models.Model):
    # 文章作者
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    # 文章标题
    title = models.CharField(max_length=100)
    # 文章正文
    body = models.TextField()
    # 文章创建时间
    created = models.DateTimeField(default=timezone.now)
    # 文章修改时间
    updated = models.DateTimeField(auto_now=True)
    # 浏览量
    total_views = models.PositiveIntegerField(default=0)

    # 内部类，用于给model定义元数据
    class Meta:
        # 指定模型返回的数据排列顺序，倒叙
        ordering = ('-created',)

    def __str__(self):
        return self.title


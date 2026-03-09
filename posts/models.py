from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings


class Post(models.Model):
    """笔记/帖子模型"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    image = models.ImageField(upload_to='posts/', blank=True, null=True, verbose_name='封面图片')
    tags = models.CharField(max_length=500, blank=True, verbose_name='标签（用逗号分隔）')
    likes_count = models.PositiveIntegerField(default=0, verbose_name='点赞数')
    comments_count = models.PositiveIntegerField(default=0, verbose_name='评论数')
    collects_count = models.PositiveIntegerField(default=0, verbose_name='收藏数')
    views_count = models.PositiveIntegerField(default=0, verbose_name='浏览数')
    is_public = models.BooleanField(default=True, verbose_name='公开')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '笔记'
        verbose_name_plural = '笔记'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})
    
    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]


class Like(models.Model):
    """点赞"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'post')
        verbose_name = '点赞'
        verbose_name_plural = '点赞'
    
    def __str__(self):
        return f'{self.user.username} 赞了 {self.post.title}'


class Collect(models.Model):
    """收藏"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collects')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='collects')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'post')
        verbose_name = '收藏'
        verbose_name_plural = '收藏'
    
    def __str__(self):
        return f'{self.user.username} 收藏了 {self.post.title}'


class Comment(models.Model):
    """评论"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(verbose_name='评论内容')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    likes_count = models.PositiveIntegerField(default=0, verbose_name='点赞数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.author.username} 的评论'


class CommentLike(models.Model):
    """评论点赞"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_likes')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'comment')
        verbose_name = '评论点赞'
        verbose_name_plural = '评论点赞'

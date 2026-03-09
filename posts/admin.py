from django.contrib import admin
from .models import Post, Like, Collect, Comment, CommentLike


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'likes_count', 'comments_count', 'collects_count', 'views_count', 'created_at']
    list_filter = ['created_at', 'is_public']
    search_fields = ['title', 'content', 'tags']
    readonly_fields = ['likes_count', 'comments_count', 'collects_count', 'views_count']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'content', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content']


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'comment', 'created_at']
    list_filter = ['created_at']

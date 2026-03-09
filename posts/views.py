from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Like, Collect, Comment, CommentLike
from accounts.models import Follow


def home(request):
    """首页 - 推荐流"""
    # 获取关注的用户的帖子 + 热门帖子
    if request.user.is_authenticated:
        # 获取关注用户的帖子
        following_ids = request.user.following.values_list('following_id', flat=True)
        posts = Post.objects.filter(
            Q(author_id__in=following_ids) | Q(is_public=True),
            author=request.user
        ).distinct().order_by('-created_at')
    else:
        posts = Post.objects.filter(is_public=True).order_by('-created_at')
    
    # 分页
    paginator = Paginator(posts, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # 检查用户是否点赞/收藏
    if request.user.is_authenticated:
        liked_posts = set(request.user.likes.values_list('post_id', flat=True))
        collected_posts = set(request.user.collects.values_list('post_id', flat=True))
    else:
        liked_posts = set()
        collected_posts = set()
    
    context = {
        'page_obj': page_obj,
        'liked_posts': liked_posts,
        'collected_posts': collected_posts,
    }
    return render(request, 'posts/home.html', context)


@login_required
def create_post(request):
    """发布笔记"""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        tags = request.POST.get('tags', '')
        image = request.FILES.get('image')
        
        post = Post.objects.create(
            author=request.user,
            title=title,
            content=content,
            tags=tags,
            image=image
        )
        
        # 更新用户帖子数
        request.user.profile.posts_count += 1
        request.user.profile.save()
        
        messages.success(request, '笔记发布成功！')
        return redirect('home')
    
    return render(request, 'posts/create.html')


def post_detail(request, pk):
    """笔记详情"""
    post = get_object_or_404(Post, pk=pk)
    
    # 增加浏览数
    post.views_count += 1
    post.save()
    
    # 获取评论
    comments = post.comments.filter(parent=None).order_by('-created_at')
    
    # 检查点赞/收藏状态
    is_liked = False
    is_collected = False
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(user=request.user, post=post).exists()
        is_collected = Collect.objects.filter(user=request.user, post=post).exists()
    
    context = {
        'post': post,
        'comments': comments,
        'is_liked': is_liked,
        'is_collected': is_collected,
    }
    return render(request, 'posts/detail.html', context)


@login_required
@require_POST
def like_post(request, pk):
    """点赞/取消点赞"""
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        like.delete()
        is_liked = False
        post.likes_count = max(0, post.likes_count - 1)
    else:
        is_liked = True
        post.likes_count += 1
    
    post.save()
    
    return JsonResponse({
        'is_liked': is_liked,
        'likes_count': post.likes_count
    })


@login_required
@require_POST
def collect_post(request, pk):
    """收藏/取消收藏"""
    post = get_object_or_404(Post, pk=pk)
    collect, created = Collect.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        collect.delete()
        is_collected = False
        post.collects_count = max(0, post.collects_count - 1)
    else:
        is_collected = True
        post.collects_count += 1
    
    post.save()
    
    return JsonResponse({
        'is_collected': is_collected,
        'collects_count': post.collects_count
    })


@login_required
@require_POST
def comment_post(request, pk):
    """发表评论"""
    post = get_object_or_404(Post, pk=pk)
    content = request.POST.get('content')
    parent_id = request.POST.get('parent_id')
    
    if not content.strip():
        return JsonResponse({'error': '评论内容不能为空'}, status=400)
    
    parent = None
    if parent_id:
        parent = get_object_or_404(Comment, pk=parent_id)
    
    comment = Comment.objects.create(
        post=post,
        author=request.user,
        content=content,
        parent=parent
    )
    
    # 更新评论数
    post.comments_count += 1
    post.save()
    
    return JsonResponse({
        'id': comment.id,
        'author': comment.author.username,
        'content': comment.content,
        'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M'),
    })


@login_required
@require_POST
def like_comment(request, pk):
    """点赞评论"""
    comment = get_object_or_404(Comment, pk=pk)
    like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)
    
    if not created:
        like.delete()
        is_liked = False
        comment.likes_count = max(0, comment.likes_count - 1)
    else:
        is_liked = True
        comment.likes_count += 1
    
    comment.save()
    
    return JsonResponse({
        'is_liked': is_liked,
        'likes_count': comment.likes_count
    })


def search(request):
    """搜索"""
    query = request.GET.get('q', '')
    
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(tags__icontains=query),
            is_public=True
        ).order_by('-created_at')
    else:
        posts = Post.objects.none()
    
    paginator = Paginator(posts, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'query': query,
        'page_obj': page_obj,
    }
    return render(request, 'posts/search.html', context)


@login_required
def my_collects(request):
    """我的收藏"""
    collects = Collect.objects.filter(user=request.user).order_by('-created_at')
    posts = [c.post for c in collects]
    
    paginator = Paginator(posts, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/collects.html', context)

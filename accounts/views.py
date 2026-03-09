from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Profile, Follow


def user_login(request):
    """用户登录"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, '用户名或密码错误')
    return render(request, 'accounts/login.html')


def user_register(request):
    """用户注册"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, '两次密码不一致')
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, '用户名已存在')
            return redirect('register')
        
        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        return redirect('home')
    
    return render(request, 'accounts/register.html')


def user_logout(request):
    """用户登出"""
    logout(request)
    return redirect('home')


@login_required
def user_profile(request, username):
    """用户个人主页"""
    user = get_object_or_404(User, username=username)
    profile = user.profile
    
    # 获取用户的帖子
    from posts.models import Post
    posts = Post.objects.filter(author=user).order_by('-created_at')[:20]
    
    # 检查是否已关注
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(
            follower=request.user, 
            following=user
        ).exists()
    
    context = {
        'profile_user': user,
        'profile': profile,
        'posts': posts,
        'is_following': is_following,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
@require_POST
def follow_user(request, user_id):
    """关注/取消关注用户"""
    target_user = get_object_or_404(User, id=user_id)
    
    if target_user == request.user:
        return JsonResponse({'error': '不能关注自己'}, status=400)
    
    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=target_user
    )
    
    if not created:
        follow.delete()
        is_following = False
    else:
        is_following = True
    
    # 更新粉丝数
    profile = target_user.profile
    profile.followers_count = target_user.followers.count()
    profile.save()
    
    # 更新关注数
    request.user.profile.following_count = request.user.following.count()
    request.user.profile.save()
    
    return JsonResponse({
        'is_following': is_following,
        'followers_count': profile.followers_count
    })


def user_settings(request):
    """用户设置"""
    if request.method == 'POST':
        profile = request.user.profile
        profile.bio = request.POST.get('bio', '')
        profile.location = request.POST.get('location', '')
        profile.website = request.POST.get('website', '')
        profile.gender = request.POST.get('gender', 'other')
        
        if request.FILES.get('avatar'):
            profile.avatar = request.FILES.get('avatar')
        
        profile.save()
        messages.success(request, '设置已保存')
        return redirect('settings')
    
    return render(request, 'accounts/settings.html')

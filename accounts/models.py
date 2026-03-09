from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """用户资料扩展"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', blank=True)
    bio = models.CharField(max_length=200, blank=True, verbose_name='个人简介')
    gender = models.CharField(max_length=10, choices=[
        ('male', '男'),
        ('female', '女'),
        ('other', '其他')
    ], default='other', verbose_name='性别')
    birthday = models.DateField(null=True, blank=True, verbose_name='生日')
    location = models.CharField(max_length=100, blank=True, verbose_name='所在地')
    website = models.URLField(blank=True, verbose_name='个人网站')
    followers_count = models.PositiveIntegerField(default=0, verbose_name='粉丝数')
    following_count = models.PositiveIntegerField(default=0, verbose_name='关注数')
    posts_count = models.PositiveIntegerField(default=0, verbose_name='笔记数')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'
    
    def __str__(self):
        return f'{self.user.username} 的资料'


class Follow(models.Model):
    """关注关系"""
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'following')
        verbose_name = '关注'
        verbose_name_plural = '关注'
    
    def __str__(self):
        return f'{self.follower.username} 关注了 {self.following.username}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """创建用户时自动创建资料"""
    if created:
        Profile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """保存用户时自动保存资料"""
    if hasattr(instance, 'profile'):
        instance.profile.save()

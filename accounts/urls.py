from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/<str:username>/', views.user_profile, name='profile'),
    path('follow/<int:user_id>/', views.follow_user, name='follow'),
    path('settings/', views.user_settings, name='settings'),
]

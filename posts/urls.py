from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_post, name='create_post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('post/<int:pk>/collect/', views.collect_post, name='collect_post'),
    path('post/<int:pk>/comment/', views.comment_post, name='comment_post'),
    path('comment/<int:pk>/like/', views.like_comment, name='like_comment'),
    path('search/', views.search, name='search'),
    path('collects/', views.my_collects, name='my_collects'),
]

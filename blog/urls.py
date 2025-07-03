from django.urls import path
from . import views
from .views import CustomLoginView, custom_logout_view, chat_users_view

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:pk>/like/', views.post_like, name='post_like'),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('search/', views.search_posts, name='search_posts'),
    path('accounts/register/', views.register, name='register'),
    path('profile/<str:username>/', views.profile_view, name='profile_view'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('follow/<str:username>/', views.follow_toggle_view, name='follow_toggle'),
    path('bookmark/<int:pk>/', views.bookmark_toggle_view, name='bookmark_toggle'),
    path('react/<int:pk>/<str:reaction_type>/', views.react_view, name='react_post'),
    path('tag/<str:tag_name>/', views.posts_by_tag, name='posts_by_tag'),
    path('hero-preview/', views.hero_preview, name='hero_preview'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', views.custom_logout_view, name='logout'),
    path('chat/', views.chat_list, name='chat_list'),
    path('chat/<str:username>/', views.chat_detail, name='chat_detail'),
    


]

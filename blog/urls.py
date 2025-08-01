from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blog_list', views.blog_list, name='blog_list'),
    path('post/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create/', views.create_blog_post, name='create_blog'),
    path('my-posts/', views.user_blog_list, name='user_blog_list'),
    path('post/edit/<int:pk>/', views.edit_blog, name='edit_blog'),
    path('post/delete/<int:pk>/', views.delete_blog, name='delete_blog'),
]

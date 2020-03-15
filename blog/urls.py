from django.urls import path
from . import views

urlpatterns = [
    path('post/<slug>/', views.blog_detail, name='blog-detail'),
    path('search/', views.blog_search, name='blog-search'),
    path('create/', views.blog_create, name='blog-create'),
    path('update/<slug>/', views.blog_update, name='blog-update'),
    path('delete/<slug>/', views.blog_delete, name='blog-delete'),
    path('articles/', views.ArticleList.as_view(), name='blog-articles'),
]

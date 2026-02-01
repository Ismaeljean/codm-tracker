from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.blog_view, name='blog'),
    path('<slug:slug>/', views.article_detail, name='article_detail'),
]

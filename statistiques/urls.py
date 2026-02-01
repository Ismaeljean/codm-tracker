from django.urls import path
from . import views

app_name = 'statistiques'

urlpatterns = [
    path('', views.stats_view, name='stats'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('classements/', views.classements_view, name='classements'),
    path('add/', views.add_stats_view, name='add_stats'),
]

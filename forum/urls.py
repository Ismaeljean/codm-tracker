from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.index_forum, name='index'),
    path('communaute/<slug:slug>/', views.communaute_detail, name='communaute'),
    path('communaute/<slug:slug>/rejoindre/', views.rejoindre_communaute, name='rejoindre'),
    path('communaute/<slug:slug>/quitter/', views.quitter_communaute, name='quitter'),
    path('communaute/<slug:slug>/creer-post/', views.creer_post, name='creer_post'),
    path('communaute/<slug:slug>/post/<slug:post_slug>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/commenter/', views.commenter_post, name='commenter_post'),
    path('commentaire/<int:commentaire_id>/like/', views.like_commentaire, name='like_commentaire'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/<int:notification_id>/marquer-lue/', views.marquer_notification_lue, name='marquer_notification_lue'),
    path('notifications/marquer-toutes-lues/', views.marquer_toutes_lues, name='marquer_toutes_lues'),
]

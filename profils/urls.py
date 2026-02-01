from django.urls import path
from . import views

app_name = 'profils'

urlpatterns = [
    path('', views.profil_view, name='profil'),
    path('create/', views.create_profil_view, name='create_profil'),
    path('edit/', views.edit_profil_view, name='edit_profil'),
]

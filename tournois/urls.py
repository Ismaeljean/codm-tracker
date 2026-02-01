from django.urls import path
from . import views

app_name = 'tournois'

urlpatterns = [
    path('', views.tournaments_view, name='tournaments'),
    path('register/<int:tournoi_id>/', views.register_tournament_view, name='register'),
    path('check/<int:tournoi_id>/', views.check_registration_view, name='check_registration'),
]

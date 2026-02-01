from django.urls import path
from . import views

app_name = 'equipements'

urlpatterns = [
    path('', views.loadouts_view, name='loadouts'),
    path('add/', views.add_loadout_view, name='add_loadout'),
    path('delete/<int:loadout_id>/', views.delete_loadout_view, name='delete_loadout'),
]

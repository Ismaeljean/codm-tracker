# CODMTracker/urls.py
# URL configuration for CODMTracker project.

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_view, name='index'),
    path('a-propos/', views.a_propos_view, name='a_propos'),
    path('utilisateurs/', include('utilisateurs.urls')),
    path('articles/', include('articles.urls')),
    path('statistiques/', include('statistiques.urls')),
    path('tournois/', include('tournois.urls')),
    path('equipements/', include('equipements.urls')),
    path('profils/', include('profils.urls')),
    path('boutique/', include('boutique.urls')),
    path('forum/', include('forum.urls')),
]

# Gestion des erreurs personnalisées
handler404 = 'CODMTracker.views.handler404'
handler500 = 'CODMTracker.views.handler500'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else None)

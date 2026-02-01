from django.shortcuts import render

def index_view(request):
    """Vue pour la page d'accueil"""
    return render(request, 'index.html')

def a_propos_view(request):
    """Vue pour la page À propos"""
    return render(request, 'a_propos.html')

# Gestionnaires d'erreurs personnalisés
def handler404(request, exception):
    """Gestionnaire personnalisé pour les erreurs 404"""
    return render(request, '404.html', status=404)

def handler500(request):
    """Gestionnaire personnalisé pour les erreurs 500"""
    return render(request, '500.html', status=500)
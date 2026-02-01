from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ProfilJoueur
from boutique.models import Commande

@login_required
def create_profil_view(request):
    """Vue pour créer le profil joueur après inscription"""
    # Vérifier si le profil existe déjà
    if ProfilJoueur.objects.filter(utilisateur=request.user).exists():
        return redirect('profils:profil')
    
    if request.method == 'POST':
        uid_codm = request.POST.get('uid_codm', '').strip()
        avatar_file = request.FILES.get('avatar')
        bio = request.POST.get('bio', '').strip()
        niveau = request.POST.get('niveau', '1')
        rang_mj = request.POST.get('rang_mj', '').strip()
        rang_br = request.POST.get('rang_br', '').strip()
        
        # Validations
        if not rang_mj or not rang_br:
            messages.error(request, "Les rangs Multijoueur et Battle Royale sont obligatoires.")
            return render(request, 'profils/create_profil.html')
        
        try:
            niveau = int(niveau)
            if niveau < 1 or niveau > 400:
                messages.error(request, "Le niveau doit être entre 1 et 400.")
                return render(request, 'profils/create_profil.html')
        except ValueError:
            messages.error(request, "Le niveau doit être un nombre.")
            return render(request, 'profils/create_profil.html')
        
        # Créer le profil
        try:
            profil = ProfilJoueur.objects.create(
                utilisateur=request.user,
                uid_codm=uid_codm if uid_codm else None,
                avatar=avatar_file if avatar_file else None,
                bio=bio,
                niveau=niveau,
                rang_mj=rang_mj,
                rang_br=rang_br,
            )
            messages.success(request, "Profil créé avec succès ! Bienvenue sur CODM Tracker !")
            return redirect('profils:profil')
        except Exception as e:
            messages.error(request, f"Une erreur est survenue : {str(e)}")
            return render(request, 'profils/create_profil.html')
    
    return render(request, 'profils/create_profil.html')

@login_required
def profil_view(request):
    """Vue pour la page du profil utilisateur"""
    try:
        profil = ProfilJoueur.objects.get(utilisateur=request.user)
        # Récupérer les commandes récentes de la boutique
        commandes_recentes = Commande.objects.filter(utilisateur=request.user).order_by('-date_commande')[:5]
        return render(request, 'profils/profil.html', {
            'profil': profil,
            'commandes_recentes': commandes_recentes
        })
    except ProfilJoueur.DoesNotExist:
        return redirect('profils:create_profil')

@login_required
def edit_profil_view(request):
    """Vue pour modifier le profil joueur"""
    try:
        profil = ProfilJoueur.objects.get(utilisateur=request.user)
    except ProfilJoueur.DoesNotExist:
        return redirect('profils:create_profil')
    
    if request.method == 'POST':
        profil.uid_codm = request.POST.get('uid_codm', '').strip() or None
        profil.bio = request.POST.get('bio', '').strip()
        
        # Gestion de l'upload d'image
        avatar_file = request.FILES.get('avatar')
        if avatar_file:
            profil.avatar = avatar_file
        
        # Validation du niveau
        try:
            niveau = int(request.POST.get('niveau', profil.niveau))
            if niveau < 1 or niveau > 400:
                messages.error(request, "Le niveau doit être entre 1 et 400.")
                return render(request, 'profils/edit_profil.html', {'profil': profil})
            profil.niveau = niveau
        except ValueError:
            messages.error(request, "Le niveau doit être un nombre.")
            return render(request, 'profils/edit_profil.html', {'profil': profil})
        
        profil.rang_mj = request.POST.get('rang_mj', profil.rang_mj)
        profil.rang_br = request.POST.get('rang_br', profil.rang_br)
        profil.save()
        
        messages.success(request, "Profil mis à jour avec succès !")
        return redirect('profils:profil')
    
    return render(request, 'profils/edit_profil.html', {'profil': profil})

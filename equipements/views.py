from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import json
from .models import Equipement
from profils.models import ProfilJoueur

@login_required
def loadouts_view(request):
    """Vue pour la page des loadouts/équipements"""
    try:
        profil = ProfilJoueur.objects.get(utilisateur=request.user)
        equipements = Equipement.objects.filter(profil=profil).order_by('-cree_le')
        return render(request, 'equipements/loadouts.html', {'equipements': equipements, 'profil': profil})
    except ProfilJoueur.DoesNotExist:
        return render(request, 'equipements/loadouts.html', {'error': 'Veuillez créer votre profil joueur d\'abord'})

@login_required
def add_loadout_view(request):
    """Vue pour ajouter un loadout (AJAX)"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=405)
    
    try:
        profil = ProfilJoueur.objects.get(utilisateur=request.user)
    except ProfilJoueur.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Veuillez créer votre profil d\'abord'}, status=400)
    
    arme = request.POST.get('arme', '').strip()
    accessoires_str = request.POST.get('accessoires', '{}')
    sensibilite_str = request.POST.get('sensibilite', '{}')
    
    if not arme:
        return JsonResponse({'success': False, 'error': 'Le nom de l\'arme est obligatoire'}, status=400)
    
    try:
        accessoires = json.loads(accessoires_str) if accessoires_str else {}
        sensibilite = json.loads(sensibilite_str) if sensibilite_str else {}
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Format JSON invalide pour accessoires ou sensibilité'}, status=400)
    
    equipement = Equipement.objects.create(
        profil=profil,
        arme=arme,
        accessoires=accessoires,
        sensibilite=sensibilite
    )
    
    return JsonResponse({
        'success': True,
        'message': 'Loadout ajouté avec succès !',
        'id': equipement.id
    })

@login_required
def delete_loadout_view(request, loadout_id):
    """Vue pour supprimer un loadout"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=405)
    
    try:
        profil = ProfilJoueur.objects.get(utilisateur=request.user)
        equipement = Equipement.objects.get(id=loadout_id, profil=profil)
        equipement.delete()
        return JsonResponse({'success': True, 'message': 'Loadout supprimé avec succès !'})
    except Equipement.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Loadout non trouvé'}, status=404)
    except ProfilJoueur.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Profil non trouvé'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

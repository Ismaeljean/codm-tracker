from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import StatistiquesJoueur
from profils.models import ProfilJoueur
from tournois.models import Tournoi, ParticipantTournoi

def stats_view(request):
    """Vue pour la page des statistiques"""
    if request.user.is_authenticated:
        try:
            profil = ProfilJoueur.objects.get(utilisateur=request.user)
            stats = StatistiquesJoueur.objects.filter(profil=profil)
            return render(request, 'statistiques/stats.html', {'stats': stats, 'profil': profil})
        except ProfilJoueur.DoesNotExist:
            pass
    return render(request, 'statistiques/stats.html')

def leaderboard_view(request):
    """Vue pour le classement"""
    stats_mj = StatistiquesJoueur.objects.filter(mode='MJ').order_by('-ratio_kd')[:100]
    stats_br = StatistiquesJoueur.objects.filter(mode='BR').order_by('-ratio_kd')[:100]
    return render(request, 'statistiques/leaderboard.html', {
        'stats_mj': stats_mj,
        'stats_br': stats_br
    })

def classements_view(request):
    """Vue pour les classements des tournois (présents et finis)"""
    now = timezone.now()
    
    # Tournois terminés (date_fin < now)
    tournois_termines = Tournoi.objects.filter(
        date_fin__lt=now
    ).order_by('-date_fin')
    
    # Tournois en cours (date_debut <= now <= date_fin)
    tournois_en_cours = Tournoi.objects.filter(
        date_debut__lte=now,
        date_fin__gte=now
    ).order_by('-date_debut')
    
    # Préparer les données pour chaque tournoi
    tournois_data = []
    
    # Traiter les tournois terminés
    for tournoi in tournois_termines:
        participants = ParticipantTournoi.objects.filter(tournoi=tournoi, paiement_effectue=True)
        
        # Grouper par équipe si nécessaire
        classement = []
        if tournoi.mode == 'MJ' or (tournoi.mode == 'BR' and tournoi.type_tournoi in ['duo', 'escouade']):
            # Mode équipe : grouper par équipe
            equipes_vues = set()
            for participant in participants.select_related('profil__utilisateur', 'equipe'):
                if participant.equipe:
                    if participant.equipe.id not in equipes_vues:
                        equipes_vues.add(participant.equipe.id)
                        membres = ParticipantTournoi.objects.filter(equipe=participant.equipe).select_related('profil__utilisateur')
                        classement.append({
                            'type': 'equipe',
                            'equipe': participant.equipe,
                            'membres': membres,
                            'code': participant.equipe.code_invitation
                        })
        else:
            # Mode solo : liste des participants individuels
            for participant in participants.select_related('profil__utilisateur'):
                classement.append({
                    'type': 'solo',
                    'participant': participant
                })
        
        tournois_data.append({
            'tournoi': tournoi,
            'classement': classement,
            'nb_participants': participants.count(),
            'est_termine': True,
            'est_en_cours': False
        })
    
    # Ajouter les tournois en cours (sans classement final)
    for tournoi in tournois_en_cours:
        participants = ParticipantTournoi.objects.filter(tournoi=tournoi, paiement_effectue=True)
        tournois_data.append({
            'tournoi': tournoi,
            'classement': [],
            'nb_participants': participants.count(),
            'est_termine': False,
            'est_en_cours': True
        })
    
    # Trier par date (les plus récents en premier)
    tournois_data.sort(key=lambda x: x['tournoi'].date_fin, reverse=True)
    
    return render(request, 'statistiques/classements.html', {
        'tournois_data': tournois_data
    })

@login_required
def add_stats_view(request):
    """Vue pour ajouter/modifier des statistiques (AJAX)"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=405)
    
    try:
        profil = ProfilJoueur.objects.get(utilisateur=request.user)
    except ProfilJoueur.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Veuillez créer votre profil d\'abord'}, status=400)
    
    try:
        mode = request.POST.get('mode')
        ratio_kd = float(request.POST.get('ratio_kd', 0))
        victoires = int(request.POST.get('victoires', 0))
        matchs = int(request.POST.get('matchs', 0))
        top10 = int(request.POST.get('top10', 0))
        
        if mode not in ['MJ', 'BR']:
            return JsonResponse({'success': False, 'error': 'Mode invalide'}, status=400)
        
        if matchs <= 0:
            return JsonResponse({'success': False, 'error': 'Le nombre de parties doit être supérieur à 0'}, status=400)
        
        # Vérifier si des stats existent déjà pour ce mode
        stats_existantes = StatistiquesJoueur.objects.filter(profil=profil, mode=mode).first()
        
        if stats_existantes:
            # Mettre à jour les stats existantes
            stats_existantes.ratio_kd = ratio_kd
            stats_existantes.victoires = victoires
            stats_existantes.matchs = matchs
            if mode == 'BR':
                stats_existantes.top10 = top10
            stats_existantes.save()
            message = "Statistiques mises à jour avec succès !"
        else:
            # Créer de nouvelles stats
            StatistiquesJoueur.objects.create(
                profil=profil,
                mode=mode,
                ratio_kd=ratio_kd,
                victoires=victoires,
                matchs=matchs,
                top10=top10 if mode == 'BR' else 0
            )
            message = "Statistiques ajoutées avec succès !"
        
        return JsonResponse({'success': True, 'message': message})
    except ValueError as e:
        return JsonResponse({'success': False, 'error': 'Valeurs invalides. Vérifiez vos données.'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

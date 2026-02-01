from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from decimal import Decimal
import secrets
from .models import Tournoi, ParticipantTournoi, EquipeTournoi
from profils.models import ProfilJoueur

def tournaments_view(request):
    """Vue pour la page des tournois avec distinction en cours/à venir (automatique via dates)"""
    now = timezone.now()
    
    # Tournois en cours (date_debut <= now <= date_fin) - AUTOMATIQUE
    tournois_en_cours = Tournoi.objects.filter(
        date_debut__lte=now,
        date_fin__gte=now
    ).order_by('-date_debut')
    
    # Tournois à venir (date_debut > now) - AUTOMATIQUE
    tournois_a_venir = Tournoi.objects.filter(
        date_debut__gt=now
    ).order_by('date_debut')
    
    # Tournois passés (date_fin < now) - AUTOMATIQUE
    tournois_passes = Tournoi.objects.filter(
        date_fin__lt=now
    ).order_by('-date_fin')[:5]
    
    # Vérifier les inscriptions de l'utilisateur avec détails
    user_registrations = {}
    if request.user.is_authenticated:
        try:
            profil = ProfilJoueur.objects.get(utilisateur=request.user)
            all_tournois = list(tournois_en_cours) + list(tournois_a_venir) + list(tournois_passes)
            for tournoi in all_tournois:
                participant = ParticipantTournoi.objects.filter(tournoi=tournoi, profil=profil).first()
                if participant:
                    equipe_info = None
                    if participant.equipe:
                        equipe_info = {
                            'code': participant.equipe.code_invitation,
                            'is_createur': participant.equipe.createur == profil,
                            'nb_membres': participant.equipe.get_nb_membres(),
                            'nb_requis': participant.equipe.get_nb_membres_requis(),
                            'complete': participant.equipe.complete,
                            'membres': [
                                {
                                    'nom': m.profil.utilisateur.nom,
                                    'prenom': m.profil.utilisateur.prenom,
                                    'email': m.profil.utilisateur.email,
                                    'is_me': m.profil == profil,
                                    'is_createur': m.profil == participant.equipe.createur
                                }
                                for m in participant.equipe.membres.all()
                            ]
                        }
                    user_registrations[tournoi.id] = {
                        'is_registered': True,
                        'equipe': equipe_info
                    }
        except ProfilJoueur.DoesNotExist:
            pass
    
    # Calculer les prix par personne pour chaque tournoi
    for tournoi in list(tournois_en_cours) + list(tournois_a_venir) + list(tournois_passes):
        prix_total = float(tournoi.prix_participation) if tournoi.prix_participation else 0.0
        
        if tournoi.mode == 'MJ':
            # Multijoueur : toujours divisé par 5
            tournoi.prix_par_personne = prix_total / 5 if prix_total > 0 else 0.0
            tournoi.nb_joueurs_requis = 5
        elif tournoi.mode == 'BR':
            # Battle Royale : selon le type
            if tournoi.type_tournoi == 'duo':
                tournoi.prix_par_personne = prix_total / 2 if prix_total > 0 else 0.0
                tournoi.nb_joueurs_requis = 2
            elif tournoi.type_tournoi == 'escouade':
                tournoi.prix_par_personne = prix_total / 4 if prix_total > 0 else 0.0
                tournoi.nb_joueurs_requis = 4
            else:  # solo ou None
                tournoi.prix_par_personne = prix_total
                tournoi.nb_joueurs_requis = 1
        else:
            tournoi.prix_par_personne = prix_total
            tournoi.nb_joueurs_requis = 1
    
    # Vérifier s'il existe des équipes pour chaque tournoi (pour afficher le champ code)
    for tournoi in list(tournois_en_cours) + list(tournois_a_venir):
        if tournoi.nb_joueurs_requis > 1:
            tournoi.has_equipes = EquipeTournoi.objects.filter(tournoi=tournoi, complete=False).exists()
        else:
            tournoi.has_equipes = False
    
    return render(request, 'tournois/tournaments.html', {
        'tournois_en_cours': tournois_en_cours,
        'tournois_a_venir': tournois_a_venir,
        'tournois_passes': tournois_passes,
        'user_registrations': user_registrations,
    })

def generate_invitation_code():
    """Génère un code d'invitation unique"""
    while True:
        code = secrets.token_urlsafe(8).upper()[:8]
        if not EquipeTournoi.objects.filter(code_invitation=code).exists():
            return code

@login_required
def register_tournament_view(request, tournoi_id):
    """Vue pour s'inscrire à un tournoi avec paiement (gère solo/duo/escouade/MJ)"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=405)
    
    try:
        tournoi = get_object_or_404(Tournoi, id=tournoi_id)
        profil = ProfilJoueur.objects.get(utilisateur=request.user)
        
        # Vérifier si déjà inscrit
        if ParticipantTournoi.objects.filter(tournoi=tournoi, profil=profil).exists():
            return JsonResponse({'success': False, 'error': 'Vous êtes déjà inscrit à ce tournoi'}, status=400)
        
        # Vérifier les dates
        now = timezone.now()
        if tournoi.date_fin < now:
            return JsonResponse({'success': False, 'error': 'Ce tournoi est terminé'}, status=400)
        
        payment_method = request.POST.get('payment_method')
        code_invitation = request.POST.get('code_invitation', '').strip().upper()
        action = request.POST.get('action', 'create')  # 'create' ou 'join'
        
        if not payment_method:
            return JsonResponse({'success': False, 'error': 'Méthode de paiement requise'}, status=400)
        
        # DÉTERMINER LE NOMBRE DE JOUEURS REQUIS
        if tournoi.mode == 'MJ':
            nb_joueurs_requis = 5
        elif tournoi.mode == 'BR':
            if tournoi.type_tournoi == 'duo':
                nb_joueurs_requis = 2
            elif tournoi.type_tournoi == 'escouade':
                nb_joueurs_requis = 4
            else:  # solo
                nb_joueurs_requis = 1
        else:
            nb_joueurs_requis = 1
        
        # GESTION SELON LE NOMBRE DE JOUEURS
        if nb_joueurs_requis == 1:
            # SOLO : Paiement normal, pas d'équipe
            prix_a_payer = tournoi.prix_participation
            payment_success = True  # À remplacer par la vraie logique de paiement
            
            if payment_success:
                ParticipantTournoi.objects.create(
                    tournoi=tournoi,
                    profil=profil,
                    paiement_effectue=True
                )
                return JsonResponse({
                    'success': True,
                    'message': f'Inscription réussie au tournoi "{tournoi.titre}" !'
                })
        
        else:
            # ÉQUIPE (Duo, Escouade ou Multijoueur) : Gestion d'équipe
            if action == 'create':
                # Créer une nouvelle équipe
                code = generate_invitation_code()
                equipe = EquipeTournoi.objects.create(
                    tournoi=tournoi,
                    createur=profil,
                    code_invitation=code
                )
                prix_a_payer = tournoi.prix_participation / nb_joueurs_requis
                payment_success = True  # À remplacer par la vraie logique de paiement
                
                if payment_success:
                    ParticipantTournoi.objects.create(
                        tournoi=tournoi,
                        profil=profil,
                        equipe=equipe,
                        paiement_effectue=True
                    )
                    return JsonResponse({
                        'success': True,
                        'message': f'Équipe créée ! Code d\'invitation: {code}. Partagez ce code avec vos coéquipiers.',
                        'code_invitation': code,
                        'equipe_id': equipe.id
                    })
            
            elif action == 'join':
                # Rejoindre une équipe existante
                if not code_invitation:
                    return JsonResponse({'success': False, 'error': 'Code d\'invitation requis'}, status=400)
                
                try:
                    # VÉRIFIER que le code correspond au bon tournoi (IMPORTANT)
                    equipe = EquipeTournoi.objects.get(
                        tournoi=tournoi,  # Le code doit correspondre à CE tournoi spécifique
                        code_invitation=code_invitation.upper()
                    )
                    
                    # Vérifier si l'équipe est complète
                    if equipe.complete:
                        return JsonResponse({'success': False, 'error': 'Cette équipe est déjà complète'}, status=400)
                    
                    # Vérifier le nombre de membres
                    nb_membres = equipe.get_nb_membres()
                    nb_requis = equipe.get_nb_membres_requis()
                    
                    if nb_membres >= nb_requis:
                        equipe.complete = True
                        equipe.save()
                        return JsonResponse({'success': False, 'error': 'Cette équipe est complète'}, status=400)
                    
                    # Calculer le prix à payer (prix par personne)
                    prix_a_payer = equipe.get_prix_par_personne()
                    
                    # SIMULATION DE PAIEMENT
                    payment_success = True  # À remplacer par la vraie logique de paiement
                    # Ici vous pouvez ajouter la logique de paiement réelle (Orange Money, MTN, etc.)
                    
                    if payment_success:
                        ParticipantTournoi.objects.create(
                            tournoi=tournoi,
                            profil=profil,
                            equipe=equipe,
                            paiement_effectue=True
                        )
                        
                        # Vérifier si l'équipe est maintenant complète
                        nb_membres_apres = equipe.get_nb_membres()
                        if nb_membres_apres >= nb_requis:
                            equipe.complete = True
                            equipe.save()
                        
                        return JsonResponse({
                            'success': True,
                            'message': f'Vous avez rejoint l\'équipe {code_invitation.upper()} ! Paiement effectué avec succès.'
                        })
                    else:
                        return JsonResponse({'success': False, 'error': 'Le paiement a échoué'}, status=400)
                
                except EquipeTournoi.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Code d\'invitation invalide ou ne correspond pas à ce tournoi'}, status=400)
        
        return JsonResponse({'success': False, 'error': 'Le paiement a échoué'}, status=400)
            
    except ProfilJoueur.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Veuillez créer votre profil d\'abord'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
def check_registration_view(request, tournoi_id):
    """Vérifier si l'utilisateur est inscrit au tournoi et retourner les détails"""
    try:
        tournoi = get_object_or_404(Tournoi, id=tournoi_id)
        profil = ProfilJoueur.objects.get(utilisateur=request.user)
        participant = ParticipantTournoi.objects.filter(tournoi=tournoi, profil=profil).first()
        
        if participant:
            equipe_info = None
            if participant.equipe:
                equipe_info = {
                    'code': participant.equipe.code_invitation,
                    'is_createur': participant.equipe.createur == profil,
                    'nb_membres': participant.equipe.get_nb_membres(),
                    'nb_requis': participant.equipe.get_nb_membres_requis(),
                    'complete': participant.equipe.complete,
                    'membres': [
                        {
                            'nom': m.profil.utilisateur.nom,
                            'prenom': m.profil.utilisateur.prenom,
                            'email': m.profil.utilisateur.email,
                            'is_me': m.profil == profil
                        }
                        for m in participant.equipe.membres.all()
                    ]
                }
            
            return JsonResponse({
                'is_registered': True,
                'equipe': equipe_info
            })
        return JsonResponse({'is_registered': False})
    except ProfilJoueur.DoesNotExist:
        return JsonResponse({'is_registered': False})
    except Exception as e:
        return JsonResponse({'is_registered': False, 'error': str(e)})

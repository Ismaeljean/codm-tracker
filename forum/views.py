from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.utils import timezone
from django.utils.text import slugify
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from .models import Communaute, MembreCommunaute, Post, LikePost, Commentaire, LikeCommentaire, Notification


def creer_notification(utilisateur, type_notif, titre, message, lien=None, post=None, commentaire=None):
    """Fonction utilitaire pour créer une notification"""
    Notification.objects.create(
        utilisateur=utilisateur,
        type_notification=type_notif,
        titre=titre,
        message=message,
        lien=lien,
        post=post,
        commentaire=commentaire
    )


def creer_notification_match(utilisateur, gagne=True, details=None):
    """Fonction utilitaire pour créer une notification de match"""
    if gagne:
        creer_notification(
            utilisateur=utilisateur,
            type_notif='match_gagne',
            titre='🎉 Tu as gagné un match !',
            message=f'Félicitations ! Tu as remporté un match.{" " + details if details else ""}',
            lien=None
        )
    else:
        creer_notification(
            utilisateur=utilisateur,
            type_notif='match_perdu',
            titre='Match terminé',
            message=f'Tu as perdu un match.{" " + details if details else "Continue à t\'entraîner !"}',
            lien=None
        )


def index_forum(request):
    """Page d'accueil du forum - Liste des communautés"""
    communautes = Communaute.objects.filter(est_active=True).annotate(
        posts_count=Count('posts', filter=Q(posts__est_actif=True))
    ).order_by('nom')
    
    context = {
        'communautes': communautes,
    }
    return render(request, 'forum/index.html', context)


def communaute_detail(request, slug):
    """Page d'une communauté - Liste des posts"""
    communaute = get_object_or_404(Communaute, slug=slug, est_active=True)
    
    # Vérifier si l'utilisateur est membre
    est_membre = False
    if request.user.is_authenticated:
        est_membre = MembreCommunaute.objects.filter(
            communaute=communaute,
            utilisateur=request.user
        ).exists()
    
    # Récupérer les posts (épinglés en premier)
    posts = Post.objects.filter(
        communaute=communaute,
        est_actif=True
    ).select_related('auteur', 'communaute').annotate(
        commentaires_count=Count('commentaires', filter=Q(commentaires__est_actif=True))
    ).order_by('-est_epingle', '-date_creation')
    
    # Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)
    
    context = {
        'communaute': communaute,
        'posts': posts_page,
        'est_membre': est_membre,
    }
    return render(request, 'forum/communaute.html', context)


@login_required
def rejoindre_communaute(request, slug):
    """Rejoindre une communauté"""
    communaute = get_object_or_404(Communaute, slug=slug, est_active=True)
    
    membre, created = MembreCommunaute.objects.get_or_create(
        communaute=communaute,
        utilisateur=request.user
    )
    
    if created:
        communaute.update_stats()
        messages.success(request, f"Vous avez rejoint la communauté {communaute.nom} !")
    else:
        messages.info(request, f"Vous êtes déjà membre de {communaute.nom}.")
    
    return redirect('forum:communaute', slug=slug)


@login_required
def quitter_communaute(request, slug):
    """Quitter une communauté"""
    communaute = get_object_or_404(Communaute, slug=slug)
    
    MembreCommunaute.objects.filter(
        communaute=communaute,
        utilisateur=request.user
    ).delete()
    
    communaute.update_stats()
    messages.success(request, f"Vous avez quitté la communauté {communaute.nom}.")
    
    return redirect('forum:communaute', slug=slug)


@login_required
def creer_post(request, slug):
    """Créer un nouveau post"""
    communaute = get_object_or_404(Communaute, slug=slug, est_active=True)
    
    # Vérifier si l'utilisateur est membre
    est_membre = MembreCommunaute.objects.filter(
        communaute=communaute,
        utilisateur=request.user
    ).exists()
    
    if not est_membre:
        messages.error(request, "Vous devez rejoindre la communauté pour créer un post.")
        return redirect('forum:communaute', slug=slug)
    
    if request.method == 'POST':
        titre = request.POST.get('titre', '').strip()
        contenu = request.POST.get('contenu', '').strip()
        type_post = request.POST.get('type_post', 'texte')
        image = request.FILES.get('image')
        lien_url = request.POST.get('lien_url', '').strip()
        
        if not titre or not contenu:
            messages.error(request, "Le titre et le contenu sont obligatoires.")
            return render(request, 'forum/creer_post.html', {'communaute': communaute})
        
        post = Post.objects.create(
            communaute=communaute,
            auteur=request.user,
            titre=titre,
            contenu=contenu,
            type_post=type_post,
            image=image if image else None,
            lien_url=lien_url if lien_url else None
        )
        
        # Notifier les membres de la communauté (sauf l'auteur)
        membres = MembreCommunaute.objects.filter(communaute=communaute).exclude(utilisateur=request.user)
        lien_post = request.build_absolute_uri(reverse('forum:post_detail', args=[communaute.slug, post.slug]))
        
        for membre in membres:
            creer_notification(
                utilisateur=membre.utilisateur,
                type_notif='nouveau_post_communaute',
                titre=f'Nouveau post dans {communaute.nom}',
                message=f'{request.user.nom} {request.user.prenom} a créé un nouveau post: "{titre}"',
                lien=lien_post,
                post=post
            )
        
        messages.success(request, "Post créé avec succès !")
        return redirect('forum:post_detail', slug=communaute.slug, post_slug=post.slug)
    
    context = {
        'communaute': communaute,
    }
    return render(request, 'forum/creer_post.html', context)


def post_detail(request, slug, post_slug):
    """Page détail d'un post avec commentaires"""
    communaute = get_object_or_404(Communaute, slug=slug, est_active=True)
    post = get_object_or_404(Post, slug=post_slug, communaute=communaute, est_actif=True)
    
    # Vérifier si l'utilisateur a liké le post
    a_like = False
    if request.user.is_authenticated:
        a_like = LikePost.objects.filter(post=post, utilisateur=request.user).exists()
    
    # Récupérer les commentaires (sans réponses pour l'instant)
    commentaires = Commentaire.objects.filter(
        post=post,
        est_actif=True,
        parent__isnull=True  # Seulement les commentaires de premier niveau
    ).select_related('auteur').prefetch_related('likes_commentaire__utilisateur').order_by('date_creation')
    
    # Vérifier quels commentaires sont likés par l'utilisateur
    commentaires_likes = set()
    if request.user.is_authenticated:
        likes = LikeCommentaire.objects.filter(
            commentaire__in=commentaires,
            utilisateur=request.user
        ).values_list('commentaire_id', flat=True)
        commentaires_likes = set(likes)
    
    # Pagination des commentaires
    paginator = Paginator(commentaires, 20)
    page_number = request.GET.get('page')
    commentaires_page = paginator.get_page(page_number)
    
    context = {
        'communaute': communaute,
        'post': post,
        'commentaires': commentaires_page,
        'a_like': a_like,
        'commentaires_likes': commentaires_likes,
    }
    return render(request, 'forum/post_detail.html', context)


@login_required
@require_http_methods(["POST"])
def like_post(request, post_id):
    """Like/Unlike un post (AJAX)"""
    post = get_object_or_404(Post, id=post_id, est_actif=True)
    
    like, created = LikePost.objects.get_or_create(
        post=post,
        utilisateur=request.user
    )
    
    if created:
        action = 'liked'
        # Notifier l'auteur du post (sauf si c'est lui qui a liké)
        if post.auteur != request.user:
            lien_post = request.build_absolute_uri(reverse('forum:post_detail', args=[post.communaute.slug, post.slug]))
            creer_notification(
                utilisateur=post.auteur,
                type_notif='like_post',
                titre='Quelqu\'un a aimé votre post',
                message=f'{request.user.nom} {request.user.prenom} a aimé votre post "{post.titre}"',
                lien=lien_post,
                post=post
            )
    else:
        like.delete()
        action = 'unliked'
    
    # Recharger le post pour avoir le bon nombre de likes
    post.refresh_from_db()
    
    return JsonResponse({
        'success': True,
        'action': action,
        'likes_count': post.nombre_likes
    })


@login_required
def commenter_post(request, post_id):
    """Commenter un post"""
    post = get_object_or_404(Post, id=post_id, est_actif=True)
    
    if request.method == 'POST':
        contenu = request.POST.get('contenu', '').strip()
        parent_id = request.POST.get('parent_id')
        
        if not contenu:
            messages.error(request, "Le commentaire ne peut pas être vide.")
            return redirect('forum:post_detail', slug=post.communaute.slug, post_slug=post.slug)
        
        parent = None
        if parent_id:
            try:
                parent = Commentaire.objects.get(id=parent_id, post=post, est_actif=True)
            except Commentaire.DoesNotExist:
                pass
        
        commentaire = Commentaire.objects.create(
            post=post,
            auteur=request.user,
            contenu=contenu,
            parent=parent
        )
        
        # Notifications
        lien_post = request.build_absolute_uri(reverse('forum:post_detail', args=[post.communaute.slug, post.slug]))
        
        if parent:
            # Réponse à un commentaire - notifier l'auteur du commentaire parent
            if parent.auteur != request.user:
                creer_notification(
                    utilisateur=parent.auteur,
                    type_notif='reponse_commentaire',
                    titre='Réponse à votre commentaire',
                    message=f'{request.user.nom} {request.user.prenom} a répondu à votre commentaire',
                    lien=lien_post,
                    post=post,
                    commentaire=commentaire
                )
        else:
            # Nouveau commentaire - notifier l'auteur du post
            if post.auteur != request.user:
                creer_notification(
                    utilisateur=post.auteur,
                    type_notif='nouveau_commentaire',
                    titre='Nouveau commentaire sur votre post',
                    message=f'{request.user.nom} {request.user.prenom} a commenté votre post "{post.titre}"',
                    lien=lien_post,
                    post=post,
                    commentaire=commentaire
                )
        
        messages.success(request, "Commentaire ajouté avec succès !")
        return redirect('forum:post_detail', slug=post.communaute.slug, post_slug=post.slug)
    
    return redirect('forum:post_detail', slug=post.communaute.slug, post_slug=post.slug)


@login_required
@require_http_methods(["POST"])
def like_commentaire(request, commentaire_id):
    """Like/Unlike un commentaire (AJAX)"""
    commentaire = get_object_or_404(Commentaire, id=commentaire_id, est_actif=True)
    
    like, created = LikeCommentaire.objects.get_or_create(
        commentaire=commentaire,
        utilisateur=request.user
    )
    
    if created:
        action = 'liked'
        # Notifier l'auteur du commentaire (sauf si c'est lui qui a liké)
        if commentaire.auteur != request.user:
            lien_post = request.build_absolute_uri(reverse('forum:post_detail', args=[commentaire.post.communaute.slug, commentaire.post.slug]))
            creer_notification(
                utilisateur=commentaire.auteur,
                type_notif='like_commentaire',
                titre='Quelqu\'un a aimé votre commentaire',
                message=f'{request.user.nom} {request.user.prenom} a aimé votre commentaire',
                lien=lien_post,
                post=commentaire.post,
                commentaire=commentaire
            )
    else:
        like.delete()
        action = 'unliked'
    
    # Recharger le commentaire pour avoir le bon nombre de likes
    commentaire.refresh_from_db()
    
    return JsonResponse({
        'success': True,
        'action': action,
        'likes_count': commentaire.nombre_likes
    })


@login_required
def notifications_view(request):
    """Vue pour afficher les notifications de l'utilisateur"""
    notifications = Notification.objects.filter(utilisateur=request.user).order_by('-date_creation')
    non_lues = notifications.filter(lu=False).count()
    
    # Pagination
    paginator = Paginator(notifications, 20)
    page_number = request.GET.get('page')
    notifications_page = paginator.get_page(page_number)
    
    return render(request, 'forum/notifications.html', {
        'notifications': notifications_page,
        'non_lues': non_lues,
    })


@login_required
@require_http_methods(["POST"])
def marquer_notification_lue(request, notification_id):
    """Marquer une notification comme lue (AJAX)"""
    notification = get_object_or_404(Notification, id=notification_id, utilisateur=request.user)
    notification.marquer_comme_lu()
    
    return JsonResponse({'success': True})


@login_required
@require_http_methods(["POST"])
def marquer_toutes_lues(request):
    """Marquer toutes les notifications comme lues"""
    Notification.objects.filter(utilisateur=request.user, lu=False).update(lu=True)
    return JsonResponse({'success': True})

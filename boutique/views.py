
# Create your views here.
# commande/views.py
"""
Vues de l'application commande

Organisation (ordre logique):
- Section "Pages publiques" (accueil avec onglets, fiche produit)
- Section "Panier / Commande" (ajout, affichage, validation)
- Section "Auth/UI simples" (login, signup, confirmation)
- Section "Administration" (liste produits admin)

Chaque vue indique:
- Rôle
- Où utilisée (URL + template)
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpRequest, JsonResponse
from django.db.models import Sum
from django.core.paginator import Paginator
from django.utils import timezone
import uuid
from django.urls import reverse
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
import json
import hmac
import hashlib
import os

from .models import Produit, Categorie, Panier, PanierProduit, Commande, Paiement
from .utils.paystack import initialize_payment, verify_payment
from decimal import Decimal

# Clé secrète Paystack (disponible partout dans views.py)
PAYSTACK_MODE = os.getenv('PAYSTACK_MODE', 'test').lower()
PAYSTACK_SECRET_KEY = (
    os.getenv('PAYSTACK_LIVE_SECRET_KEY')
    if PAYSTACK_MODE == 'live'
    else os.getenv('PAYSTACK_TEST_SECRET_KEY')
)


def custom_404(request, exception):
    return render(request, "404.html", status=404)

# --- Helpers ---
def get_cart_count(user):
    """Calcule le nombre total d'articles dans le panier en cours de l'utilisateur."""
    if user.is_authenticated:
        panier = Panier.objects.filter(utilisateur=user, statut='en_cours').first()
        if panier:
            return panier.panierproduit_set.aggregate(Sum('quantite'))['quantite__sum'] or 0
    return 0


def liste_produits(request: HttpRequest):
    """
    Accueil: affiche uniquement les catégories avec pagination.
    - URL: path('', views.liste_produits, name='index')
    - Template: commande/index.html
    """

    # Ajoute un ordre stable (ex: par nom, ou par ID)
    categories_list = Categorie.objects.all().order_by('nom')  # ou 'id', ou 'date_creation'
    paginator = Paginator(categories_list, 6)
    page_number = request.GET.get('page')
    categories = paginator.get_page(page_number)
    
    return render(
        request,
        'boutique/index.html',
        {
            'categories': categories,
            'cart_count': get_cart_count(request.user),
        },
    )

def liste_produits_par_categorie(request: HttpRequest, categorie_id: int):
    """
    Page catégorie: liste des produits avec pagination.
    - URL: path('categorie/<int:categorie_id>/', ...)
    - Template: boutique/categorie.html
    """
    categorie = get_object_or_404(Categorie, id=categorie_id)
    produits_qs = Produit.objects.filter(is_active=True, categorie=categorie).order_by('nom')
    
    # Pagination
    paginator = Paginator(produits_qs, 12)  # 12 produits par page
    page_number = request.GET.get('page', 1)
    produits = paginator.get_page(page_number)
    
    return render(
        request,
        'boutique/categorie.html',
        {
            'categorie': categorie,
            'produits': produits,
            'cart_count': get_cart_count(request.user),
        },
    )

def produit_detail(request, produit_id: int):
    """
    Fiche produit.
    - Rôle: afficher le produit, prix (avec réduction si disponible), proposer ajout panier
    - URL: path('produit/<int:produit_id>/', views.produit_detail, name='produit')
    - Template: boutique/produit.html
    """
    produit = get_object_or_404(Produit, id=produit_id, is_active=True)

    # Calculs pour la promo (si applicable)
    promo_data = None
    if produit.est_en_promotion and produit.prix_reduit and produit.prix_reduit < produit.prix:
        economie = produit.prix - produit.prix_reduit
        pourcentage = round((economie / produit.prix) * 100) if produit.prix > 0 else 0
        promo_data = {
            'prix_reduit': produit.prix_reduit,
            'prix_normal': produit.prix,
            'economie': economie,
            'pourcentage': pourcentage,
        }

    context = {
        'produit': produit,
        'promo_data': promo_data,  # ← on passe un dict prêt à l'emploi
        'cart_count': get_cart_count(request.user),
    }
    return render(request, 'boutique/produit.html', context)

def redirect_produit_index_html(request: HttpRequest):
    """
    Sécurité/Compat: si une ancienne URL /produit/index.html est appelée, on redirige vers l'accueil.
    - Non utilisé normalement (routes actuelles n'emploient plus index.html)
    """
    return redirect('boutique:index')


@login_required(login_url='utilisateurs:login')
def ajouter_au_panier(request, produit_id):
    """
    Ajouter un produit au panier de l'utilisateur connecté.
    - Rôle: créer/mettre à jour la ligne panier (PanierProduit) avec quantité
    - URL: path('ajouter/<int:produit_id>/', views.ajouter_au_panier, name='ajouter_au_panier')
    - Redirige: boutique:panier
    """
    produit = get_object_or_404(Produit, id=produit_id, is_active=True)
    panier, created = Panier.objects.get_or_create(
        utilisateur=request.user,
        statut='en_cours',
        defaults={'statut': 'en_cours'}
    )
    try:
        quantite = int(request.POST.get('quantite', 1))
    except (TypeError, ValueError):
        messages.error(request, "Quantité invalide.")
        return redirect('boutique:index')
    
    if quantite < 1:
        messages.error(request, "Quantité invalide.")
        return redirect('boutique:index')
    
    if produit.stock < quantite:
        messages.error(request, "Stock insuffisant.")
        return redirect('boutique:index')

    panier_produit, created = PanierProduit.objects.get_or_create(
        panier=panier,
        produit=produit,
        defaults={'quantite': quantite}
    )
    if not created:
        panier_produit.quantite += quantite
        panier_produit.save()
    
    messages.success(request, f"{produit.nom} ajouté au panier.")
    return redirect('boutique:panier')

@login_required(login_url='utilisateurs:login')
def voir_panier(request):
    panier, created = Panier.objects.get_or_create(
        utilisateur=request.user,
        statut='en_cours',
        defaults={'statut': 'en_cours'}
    )
    items_qs = panier.panierproduit_set.select_related('produit').all()
    items = []
    total_produits = 0
    for item in items_qs:
        unit_price = item.prix_unitaire
        line_total = item.total_ligne
        total_produits += line_total
        items.append({
            'id': item.id,
            'produit': item.produit,
            'quantite': item.quantite,
            'unit_price': unit_price,
            'line_total': line_total,
        })

    # Simulation de la logique de Commande.appliquer_frais_livraison()
    commandes_precedentes = Commande.objects.filter(
        utilisateur=request.user,
        statut__in=['payee', 'valide', 'livre']
    ).exists()

    frais_livraison = Decimal('0.00') if not commandes_precedentes else Decimal('1000.00')
    total_avec_livraison = total_produits + frais_livraison
    est_premier_achat = not commandes_precedentes

    return render(request, 'boutique/panier.html', {
        'panier': panier,
        'panier_produits': items,
        'total': total_produits,
        'frais_livraison': frais_livraison,
        'total_avec_livraison': total_avec_livraison,
        'est_premier_achat': est_premier_achat,
        'cart_count': get_cart_count(request.user)
    })


@login_required(login_url='utilisateurs:login')
def mettre_a_jour_ligne_panier(request: HttpRequest, item_id: int):
    """
    Met à jour la quantité d'une ligne du panier en cours (POST uniquement).
    - URL: path('panier/update/<int:item_id>/', views.mettre_a_jour_ligne_panier, name='maj_ligne_panier')
    - Redirige: boutique:panier
    """
    if request.method != 'POST':
        return redirect('boutique:panier')
    item = get_object_or_404(PanierProduit, id=item_id, panier__utilisateur=request.user, panier__statut='en_cours')
    try:
        quantite = int(request.POST.get('quantite', item.quantite))
    except (TypeError, ValueError):
        messages.error(request, "Quantité invalide.")
        return redirect('boutique:panier')
    if quantite < 1:
        messages.error(request, "Quantité minimum: 1")
        return redirect('boutique:panier')
    if item.produit.stock < quantite:
        messages.error(request, f"Stock insuffisant. Stock disponible: {item.produit.stock}")
        return redirect('boutique:panier')
    item.quantite = quantite
    item.save()
    messages.success(request, "Quantité mise à jour.")
    return redirect('boutique:panier')

@login_required(login_url='utilisateurs:login')
def supprimer_ligne_panier(request: HttpRequest, item_id: int):
    """
    Supprime une ligne du panier en cours (POST uniquement).
    - URL: path('panier/remove/<int:item_id>/', views.supprimer_ligne_panier, name='supprimer_ligne_panier')
    - Redirige: boutique:panier
    """
    if request.method != 'POST':
        return redirect('boutique:panier')
    item = get_object_or_404(PanierProduit, id=item_id, panier__utilisateur=request.user, panier__statut='en_cours')
    item.delete()
    messages.success(request, "Article supprimé du panier.")
    return redirect('boutique:panier')





@login_required(login_url='utilisateurs:login')
def passer_commande(request):
    """
    Passer une commande.
    - Livraison gratuite pour le premier achat réussi (payé/validé/livré)
    - Sinon, frais de livraison fixes (1000 XOF ici)
    """
    if request.method != 'POST':
        return redirect('boutique:panier')

    panier = Panier.objects.filter(
        utilisateur=request.user,
        statut='en_cours'
    ).first()

    if not panier or not panier.panierproduit_set.exists():
        messages.error(request, "Votre panier est vide.")
        return redirect('boutique:panier')

    adresse = request.POST.get('adresse_livraison', '').strip()
    if not adresse:
        messages.error(request, "Adresse de livraison obligatoire.")
        return redirect('boutique:panier')

    # Total produits
    total_produits = sum(
        item.total_ligne
        for item in panier.panierproduit_set.all()
    )

    try:
        with transaction.atomic():
            # 1️⃣ Créer la commande (sans toucher au panier)
            commande = Commande.objects.create(
                utilisateur=request.user,
                panier=panier,
                total=total_produits,
                adresse_livraison=adresse,
                mode_paiement='paystack',
                statut='en_attente_paiement'
            )

            total_final = commande.total_avec_livraison

            # 2️⃣ Créer le paiement
            reference = f"CODM-TRACKER-{uuid.uuid4().hex[:15].upper()}"

            paiement = Paiement.objects.create(
                commande=commande,
                reference_paystack=reference,
                montant=total_final,
                statut='en_attente',
                mode_paiement='paystack'
            )

            email = request.user.email or "client@codmtracker.ci"
            callback_url = request.build_absolute_uri(
                reverse('boutique:paystack_callback')
            )

            auth_url, ref_paystack = initialize_payment(
                email=email,
                amount_xof=Decimal(str(total_final)),
                reference=reference,
                callback_url=callback_url,
                metadata={"commande_id": commande.id},
                channels=["mobile_money", "card", "bank_transfer", "ussd"]
            )

            if not auth_url:
                raise Exception("Initialisation paiement échouée")

            if ref_paystack:
                paiement.reference_paystack = ref_paystack
                paiement.save(update_fields=['reference_paystack'])

            # 3️⃣ Redirection vers Paystack
            return redirect(auth_url)

    except Exception as e:
        messages.error(request, "Erreur lors de la préparation du paiement.")
        return redirect('boutique:panier')


def paystack_callback(request):
    """
    Callback navigateur Paystack (après paiement).
    - Vérifie le paiement via l’API Paystack
    - Valide la commande UNE SEULE FOIS
    - Protège contre les doubles traitements
    """

    ref = request.GET.get('reference') or request.GET.get('trxref')
    if not ref:
        messages.error(request, "Paiement annulé ou référence manquante.")
        return redirect('boutique:panier')

    # 1️⃣ Vérification Paystack
    success, data = verify_payment(ref)
    if not success:
        messages.error(request, "Paiement non confirmé.")
        return redirect('boutique:panier')

    # Sécurité : Paystack doit confirmer SUCCESS
    if data.get("status") != "success":
        messages.error(request, "Paiement échoué.")
        return redirect('boutique:panier')

    try:
        paiement = Paiement.objects.select_related(
            'commande', 'commande__panier'
        ).get(reference_paystack=ref)
    except Paiement.DoesNotExist:
        messages.error(request, "Paiement introuvable.")
        return redirect('boutique:panier')

    # 2️⃣ Si déjà traité → on affiche simplement la confirmation
    if paiement.statut == 'payee':
        return render(request, 'boutique/confirmation.html', {
            'commande': paiement.commande
        })

    # 3️⃣ Traitement atomique (une seule fois)
    try:
        with transaction.atomic():
            # Verrouillage des produits
            for item in paiement.commande.panier.panierproduit_set.select_for_update():
                if item.produit.stock < item.quantite:
                    raise Exception(f"Stock insuffisant pour {item.produit.nom}")

                item.produit.stock -= item.quantite
                item.produit.save(update_fields=['stock'])

            # Marquer paiement + commande
            paiement.marquer_comme_paye()

    except Exception:
        messages.error(request, "Erreur lors de la validation de la commande.")
        return redirect('boutique:panier')

    # 4️⃣ Confirmation utilisateur
    messages.success(
        request,
        f"Paiement réussi ! Commande {paiement.commande.numero_commande}"
    )

    return render(request, 'boutique/confirmation.html', {
        'commande': paiement.commande
    })



@csrf_exempt
def paystack_webhook(request):
    """
    Webhook de Paystack.
    - Rôle: Traiter les événements de Paystack.
    - URL: path('paystack/webhook/', views.paystack_webhook, name='paystack_webhook')
    - Template: commande/paystack_webhook.html
    """
    if request.method != "POST":
        return JsonResponse({"status": "invalid method"}, status=405)

    signature = request.headers.get("x-paystack-signature")
    if not signature:
        return JsonResponse({"status": "missing signature"}, status=400)

    computed_signature = hmac.new(
        PAYSTACK_SECRET_KEY.encode(),
        request.body,
        hashlib.sha512
    ).hexdigest()

    if computed_signature != signature:
        return JsonResponse({"status": "invalid signature"}, status=400)

    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"status": "invalid json"}, status=400)

    if payload.get("event") == "charge.success":
        ref = payload["data"]["reference"]

        try:
            paiement = Paiement.objects.select_related('commande').get(
                reference_paystack=ref,
                statut='en_attente'
            )

            with transaction.atomic():
                for item in paiement.commande.panier.panierproduit_set.select_for_update():
                    if item.produit.stock < item.quantite:
                        raise Exception("Stock insuffisant")
                    item.produit.stock -= item.quantite
                    item.produit.save()

                paiement.marquer_comme_paye()


        except Paiement.DoesNotExist:
            pass

    return JsonResponse({"status": "ok"})





# --- Profil utilisateur boutique ---
@login_required(login_url='utilisateurs:login')
def profil(request):
    """
    Page de profil utilisateur pour la boutique.
    - Rôle: Afficher les commandes de l'utilisateur connecté.
    - URL: path('profil/', views.profil, name='profil')
    - Template: boutique/profil.html
    """
    # Récupérer les commandes de l'utilisateur
    commandes = Commande.objects.filter(utilisateur=request.user).order_by('-date_commande')[:5]
    
    context = {
        'user': request.user,
        'commandes_recentes': commandes,
        'cart_count': get_cart_count(request.user),
    }
    return render(request, 'boutique/profil.html', context)
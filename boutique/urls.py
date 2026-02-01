from django.urls import path
from . import views

app_name = 'boutique'

urlpatterns = [
    # Pages publiques
    path('', views.liste_produits, name='index'),
    path('categorie/<int:categorie_id>/', views.liste_produits_par_categorie, name='categorie'),
    path('produit/<int:produit_id>/', views.produit_detail, name='produit'),
    
    # Panier
    path('panier/', views.voir_panier, name='panier'),
    path('ajouter/<int:produit_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('panier/update/<int:item_id>/', views.mettre_a_jour_ligne_panier, name='maj_ligne_panier'),
    path('panier/remove/<int:item_id>/', views.supprimer_ligne_panier, name='supprimer_ligne_panier'),
    
    # Commande et paiement
    path('commande/', views.passer_commande, name='passer_commande'),
    path('paystack/callback/', views.paystack_callback, name='paystack_callback'),
    path('paystack/webhook/', views.paystack_webhook, name='paystack_webhook'),
    
    # Profil
    path('profil/', views.profil, name='profil'),
]
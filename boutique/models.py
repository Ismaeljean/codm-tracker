# boutique/models.py
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from decimal import Decimal

# Utilisateur
from utilisateurs.models import Utilisateur


class Categorie(models.Model):
    """Catégorie de produits.

    - nom: libellé de la catégorie
    - image: image téléversée (affichage dans les listes)
    """
    nom = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.nom

class Produit(models.Model):
    """Produit vendable.

    - prix: prix normal en XOF
    - prix_reduit: prix réduit (optionnel, pour promotions)
    - image: photo du produit (optionnelle)
    - categorie: lien vers Categorie
    """
    
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Prix normal en XOF")
    prix_reduit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Prix réduit (optionnel, pour promotions)")
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='produits/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.RESTRICT)

    def __str__(self):
        return self.nom
    
    @property
    def prix_actuel(self):
        """Retourne le prix réduit s'il existe, sinon le prix normal"""
        return self.prix_reduit if self.prix_reduit else self.prix
    
    @property
    def est_en_promotion(self):
        """Vérifie si le produit est en promotion"""
        return self.prix_reduit is not None and self.prix_reduit < self.prix


class Panier(models.Model):
    """Panier d'un utilisateur.

    - statut: en_cours | valide
    - un seul panier en cours par utilisateur
    """
    STATUT_CHOICES = (
        ('en_cours', 'En cours'),
        ('valide', 'Validé'),
    )
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_cours')
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Panier de {self.utilisateur.nom} ({self.statut})"

class PanierProduit(models.Model):
    """Ligne de panier."""
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.RESTRICT)
    quantite = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantite} x {self.produit.nom}"
    
    @property
    def prix_unitaire(self):
        """Retourne le prix unitaire du produit (prix réduit si disponible)"""
        return self.produit.prix_actuel
    
    @property
    def total_ligne(self):
        """Retourne le total de la ligne (quantité * prix unitaire)"""
        return self.quantite * self.prix_unitaire


class Commande(models.Model):
    """Commande issue d'un panier validé.

    - numero_commande: identifiant lisible unique (généré au save)
    - adresse_livraison: texte fourni à la validation
    - mode_paiement: ex: mobile_money, paystack
    """
    STATUT_CHOICES = (
        ('en_attente_paiement', 'En attente de paiement'),
        ('en_attente', 'En attente'),
        ('payee', 'Payée'),
        ('valide', 'Validé'),
        ('livre', 'Livré'),
        ('annulee', 'Annulée'),
        ('echec', 'Échec'),
    )
    
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.RESTRICT)
    panier = models.ForeignKey(Panier, on_delete=models.RESTRICT)
    total = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total des produits uniquement")
    date_commande = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente_paiement')
    adresse_livraison = models.TextField()
    mode_paiement = models.CharField(max_length=50)
    numero_commande = models.CharField(max_length=150, unique=True, db_index=True, blank=True)
    
    # Nouveaux champs pour la livraison
    frais_livraison = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_avec_livraison = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Commande {self.numero_commande or self.id} de {self.utilisateur}"

    def save(self, *args, **kwargs):
        # Générer le numéro de commande si nécessaire
        if not self.numero_commande:
            now = timezone.localtime(timezone.now())
            date_str = now.strftime('%Y%m%d')
            time_str = now.strftime('%H%M%S')
            start_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)
            count_today = Commande.objects.filter(date_commande__range=(start_day, end_day)).count() + 1
            user_slug = slugify(self.utilisateur.nom)[:30] or 'client'
            self.numero_commande = f"CMD-{user_slug}-{date_str}{time_str}-{count_today}"

        # Appliquer les frais de livraison (avant sauvegarde finale)
        self.appliquer_frais_livraison()

        # Calculer le total final
        self.total_avec_livraison = self.total + self.frais_livraison

        super().save(*args, **kwargs)

    def appliquer_frais_livraison(self):
        """Livraison gratuite pour le premier achat réussi."""
        commandes_precedentes = Commande.objects.filter(
            utilisateur=self.utilisateur,
            statut__in=['payee', 'valide', 'livre']
        ).exclude(pk=self.pk if self.pk else None)

        if commandes_precedentes.exists():
            self.frais_livraison = Decimal('1000.00')  # Tarif normal
        else:
            self.frais_livraison = Decimal('0.00')   # Premier achat → gratuit

    @property
    def est_premier_achat(self):
        """Utile pour l'affichage dans les templates."""
        return not Commande.objects.filter(
            utilisateur=self.utilisateur,
            statut__in=['payee', 'valide', 'livre']
        ).exclude(pk=self.pk if self.pk else None).exists()

    @property
    def paiement(self):
        return self.paiements.first()

    @property
    def est_payee(self):
        paiement = self.paiement
        return paiement is not None and paiement.statut == 'payee'


class Paiement(models.Model):
    """Paiement associé à une commande.

    - reference_paystack: référence de transaction Paystack
    - montant: montant payé
    - statut: statut du paiement
    - date_paiement: date de paiement effectif
    """
    STATUT_CHOICES = (
        ('en_attente', 'En attente'), # paiement créé, mais pas encore payé
        ('payee', 'Payée'), # paiement payé, mais pas encore validé
        ('echec', 'Échec'), # paiement échoué
        ('annule', 'Annulé'), # paiement annulé
    )
    
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='paiements')
    reference_paystack = models.CharField(max_length=200, unique=True, db_index=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    mode_paiement = models.CharField(max_length=50, default='paystack')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_paiement = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True, help_text="Données supplémentaires de Paystack")

    class Meta:
        ordering = ['-date_creation']
        verbose_name = 'Paiement'
        verbose_name_plural = 'Paiements'

    def __str__(self):
        return f"Paiement {self.reference_paystack} - {self.get_statut_display()} - {self.montant} XOF"

    def marquer_comme_paye(self):
        if self.statut == 'payee':
            return

        self.statut = 'payee'
        self.date_paiement = timezone.now()
        self.save(update_fields=['statut', 'date_paiement'])

        commande = self.commande
        commande.statut = 'payee'
        commande.save(update_fields=['statut'])

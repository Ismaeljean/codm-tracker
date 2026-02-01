from django.db import models
from profils.models import ProfilJoueur

# Create your models here.
class Tournoi(models.Model):
    MODE_CHOICES = [("MJ", "Multijoueur"), ("BR", "Battle Royale")]
    TYPE_CHOICES = [
        ("solo", "Solo"),
        ("duo", "Duo"),
        ("escouade", "Escouade"),
    ]

    titre = models.CharField(max_length=150)
    description = models.TextField()
    mode = models.CharField(max_length=2, choices=MODE_CHOICES)
    type_tournoi = models.CharField(max_length=10, choices=TYPE_CHOICES, default="solo", blank=True, null=True, help_text="Type de tournoi (Solo, Duo ou Escouade) - Uniquement pour Battle Royale. Multijoueur = 5 joueurs obligatoire")
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    recompense = models.CharField(max_length=100)
    image = models.ImageField(upload_to='tournois/', blank=True, null=True, help_text="Image du tournoi")
    prix_participation = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Prix total de participation en FCFA")

    def __str__(self):
        return f"{self.titre} - {self.get_mode_display()}"

    class Meta:
        verbose_name = "Tournoi"
        verbose_name_plural = "Tournois"
        ordering = ['-date_debut']


class EquipeTournoi(models.Model):
    """Modèle pour gérer les équipes de tournoi (duo/escouade)"""
    tournoi = models.ForeignKey(Tournoi, on_delete=models.CASCADE, related_name='equipes')
    code_invitation = models.CharField(max_length=20, unique=True, help_text="Code unique pour rejoindre l'équipe")
    createur = models.ForeignKey(ProfilJoueur, on_delete=models.CASCADE, related_name='equipes_creees')
    cree_le = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, help_text="True si l'équipe est complète")
    
    def __str__(self):
        return f"Équipe {self.code_invitation} - {self.tournoi.titre}"
    
    def get_nb_membres(self):
        """Retourne le nombre de membres dans l'équipe"""
        return self.membres.count()
    
    def get_nb_membres_requis(self):
        """Retourne le nombre de membres requis selon le mode et type de tournoi"""
        if self.tournoi.mode == 'MJ':
            # Multijoueur : toujours 5 joueurs
            return 5
        elif self.tournoi.mode == 'BR':
            # Battle Royale : selon le type
            if self.tournoi.type_tournoi == 'duo':
                return 2
            elif self.tournoi.type_tournoi == 'escouade':
                return 4
            else:  # solo
                return 1
        return 1
    
    def get_prix_par_personne(self):
        """Retourne le prix par personne"""
        nb_membres = self.get_nb_membres_requis()
        if nb_membres > 0:
            return self.tournoi.prix_participation / nb_membres
        return self.tournoi.prix_participation
    
    class Meta:
        verbose_name = "Équipe Tournoi"
        verbose_name_plural = "Équipes Tournois"


class ParticipantTournoi(models.Model):
    tournoi = models.ForeignKey(Tournoi, on_delete=models.CASCADE, related_name='participants')
    profil = models.ForeignKey(ProfilJoueur, on_delete=models.CASCADE, related_name='participations')
    equipe = models.ForeignKey(EquipeTournoi, on_delete=models.CASCADE, null=True, blank=True, related_name='membres')
    rejoint_le = models.DateTimeField(auto_now_add=True)
    paiement_effectue = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.profil.utilisateur.nom} {self.profil.utilisateur.prenom} - {self.tournoi.titre}"

    class Meta:
        verbose_name = "Participant Tournoi"
        verbose_name_plural = "Participants Tournois"
        unique_together = ['tournoi', 'profil']

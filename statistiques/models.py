from django.db import models
from profils.models import ProfilJoueur

# Modèle pour les statistiques joueur
class StatistiquesJoueur(models.Model):
    MODE_CHOICES = [
        ("MJ", "Multijoueur"),
        ("BR", "Battle Royale")
    ]

    profil = models.ForeignKey(ProfilJoueur, on_delete=models.CASCADE)
    mode = models.CharField(max_length=2, choices=MODE_CHOICES)
    ratio_kd = models.FloatField()
    victoires = models.IntegerField()
    matchs = models.IntegerField()
    top10 = models.IntegerField(default=0)
    mis_a_jour_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.profil.utilisateur.nom} {self.profil.utilisateur.prenom} - {self.mode}"
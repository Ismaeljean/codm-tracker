from django.db import models
from profils.models import ProfilJoueur

# Modèle pour les équipements
class Equipement(models.Model):
    profil = models.ForeignKey(ProfilJoueur, on_delete=models.CASCADE)
    arme = models.CharField(max_length=100)
    accessoires = models.JSONField()
    sensibilite = models.JSONField()
    cree_le = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profil.utilisateur.nom} {self.profil.utilisateur.prenom} - {self.arme}"
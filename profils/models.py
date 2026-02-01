from django.db import models
from utilisateurs.models import Utilisateur

# Modèle pour le profil joueur
class ProfilJoueur(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    uid_codm = models.CharField(max_length=50, blank=True, null=True)
    avatar = models.ImageField(upload_to='profils/avatars/', blank=True, null=True, help_text="Image de profil")
    bio = models.TextField(blank=True)
    niveau = models.IntegerField(default=1)
    rang_mj = models.CharField(max_length=50)
    rang_br = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.utilisateur.nom} {self.utilisateur.prenom} - Profil"

    class Meta:
        verbose_name = "Profil Joueur"
        verbose_name_plural = "Profils Joueurs"

    
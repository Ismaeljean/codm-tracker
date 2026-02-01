from django.db import models
from django.utils import timezone
from utilisateurs.models import Utilisateur


class Communaute(models.Model):
    """Communauté (catégorie) du forum - Niveau 1"""
    nom = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    icone = models.CharField(max_length=50, default='fas fa-comments', help_text="Classe FontAwesome pour l'icône")
    couleur = models.CharField(max_length=20, default='#FF1A1A', help_text="Couleur hexadécimale")
    date_creation = models.DateTimeField(auto_now_add=True)
    est_active = models.BooleanField(default=True)
    
    # Statistiques
    nombre_posts = models.PositiveIntegerField(default=0)
    nombre_membres = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = "Communauté"
        verbose_name_plural = "Communautés"
        ordering = ['nom']
    
    def __str__(self):
        return self.nom
    
    def update_stats(self):
        """Met à jour les statistiques de la communauté"""
        self.nombre_posts = self.posts.filter(est_actif=True).count()
        self.nombre_membres = self.membres.count()
        self.save(update_fields=['nombre_posts', 'nombre_membres'])


class MembreCommunaute(models.Model):
    """Membres d'une communauté"""
    communaute = models.ForeignKey(Communaute, on_delete=models.CASCADE, related_name='membres')
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    date_join = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['communaute', 'utilisateur']
        verbose_name = "Membre"
        verbose_name_plural = "Membres"
    
    def __str__(self):
        return f"{self.utilisateur.nom} - {self.communaute.nom}"


class Post(models.Model):
    """Post dans une communauté - Niveau 2"""
    TYPE_POST_CHOICES = (
        ('texte', 'Post Texte'),
        ('image', 'Post Image'),
        ('lien', 'Post Lien'),
    )
    
    communaute = models.ForeignKey(Communaute, on_delete=models.CASCADE, related_name='posts')
    auteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='posts')
    titre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    contenu = models.TextField()
    type_post = models.CharField(max_length=10, choices=TYPE_POST_CHOICES, default='texte')
    image = models.ImageField(upload_to='forum/posts/', blank=True, null=True)
    lien_url = models.URLField(blank=True, null=True, help_text="URL si type_post = 'lien'")
    
    # Statistiques
    nombre_likes = models.PositiveIntegerField(default=0)
    nombre_commentaires = models.PositiveIntegerField(default=0)
    
    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    est_actif = models.BooleanField(default=True)
    est_epingle = models.BooleanField(default=False, help_text="Post épinglé en haut de la communauté")
    
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['-est_epingle', '-date_creation']
        indexes = [
            models.Index(fields=['communaute', '-date_creation']),
            models.Index(fields=['auteur', '-date_creation']),
        ]
    
    def __str__(self):
        return f"{self.titre} - {self.communaute.nom}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.titre)
            # Assurer l'unicité
            base_slug = self.slug
            counter = 1
            while Post.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
        # Mettre à jour les stats de la communauté
        self.communaute.update_stats()
    
    def update_comment_count(self):
        """Met à jour le nombre de commentaires"""
        self.nombre_commentaires = self.commentaires.filter(est_actif=True).count()
        self.save(update_fields=['nombre_commentaires'])


class LikePost(models.Model):
    """Like/Upvote sur un post"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes_post')
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['post', 'utilisateur']
        verbose_name = "Like Post"
        verbose_name_plural = "Likes Posts"
    
    def __str__(self):
        return f"{self.utilisateur.nom} aime {self.post.titre}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Mettre à jour le nombre de likes du post
        self.post.nombre_likes = self.post.likes_post.count()
        self.post.save(update_fields=['nombre_likes'])
    
    def delete(self, *args, **kwargs):
        post = self.post
        super().delete(*args, **kwargs)
        # Mettre à jour le nombre de likes du post
        post.nombre_likes = post.likes_post.count()
        post.save(update_fields=['nombre_likes'])


class Commentaire(models.Model):
    """Commentaire sous un post - Niveau 3"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='commentaires')
    auteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='commentaires')
    contenu = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='reponses', help_text="Commentaire parent pour les réponses")
    
    # Statistiques
    nombre_likes = models.PositiveIntegerField(default=0)
    
    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    est_actif = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
        ordering = ['date_creation']
        indexes = [
            models.Index(fields=['post', 'date_creation']),
        ]
    
    def __str__(self):
        return f"Commentaire de {self.auteur.nom} sur {self.post.titre}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Mettre à jour le nombre de commentaires du post
        self.post.update_comment_count()
    
    def delete(self, *args, **kwargs):
        post = self.post
        super().delete(*args, **kwargs)
        # Mettre à jour le nombre de commentaires du post
        post.update_comment_count()


class LikeCommentaire(models.Model):
    """Like sur un commentaire"""
    commentaire = models.ForeignKey(Commentaire, on_delete=models.CASCADE, related_name='likes_commentaire')
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['commentaire', 'utilisateur']
        verbose_name = "Like Commentaire"
        verbose_name_plural = "Likes Commentaires"
    
    def __str__(self):
        return f"{self.utilisateur.nom} aime le commentaire de {self.commentaire.auteur.nom}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Mettre à jour le nombre de likes du commentaire
        self.commentaire.nombre_likes = self.commentaire.likes_commentaire.count()
        self.commentaire.save(update_fields=['nombre_likes'])
    
    def delete(self, *args, **kwargs):
        commentaire = self.commentaire
        super().delete(*args, **kwargs)
        # Mettre à jour le nombre de likes du commentaire
        commentaire.nombre_likes = commentaire.likes_commentaire.count()
        commentaire.save(update_fields=['nombre_likes'])


class Notification(models.Model):
    """Système de notifications pour le forum"""
    TYPE_NOTIFICATION_CHOICES = (
        ('nouveau_commentaire', 'Nouveau commentaire sur votre post'),
        ('reponse_commentaire', 'Réponse à votre commentaire'),
        ('like_post', 'Quelqu\'un a aimé votre post'),
        ('like_commentaire', 'Quelqu\'un a aimé votre commentaire'),
        ('nouveau_post_communaute', 'Nouveau post dans votre communauté'),
        ('match_gagne', 'Tu as gagné un match !'),
        ('match_perdu', 'Tu as perdu un match'),
        ('tournoi_gagne', 'Tu as gagné un tournoi !'),
        ('nouveau_membre', 'Nouveau membre dans votre communauté'),
    )
    
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='notifications')
    type_notification = models.CharField(max_length=30, choices=TYPE_NOTIFICATION_CHOICES)
    titre = models.CharField(max_length=200)
    message = models.TextField()
    lien = models.URLField(blank=True, null=True, help_text="Lien vers la page concernée")
    
    # Relations optionnelles
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    commentaire = models.ForeignKey(Commentaire, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    
    # Statut
    lu = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-date_creation']
        indexes = [
            models.Index(fields=['utilisateur', '-date_creation', 'lu']),
        ]
    
    def __str__(self):
        return f"{self.titre} - {self.utilisateur.nom}"
    
    def marquer_comme_lu(self):
        """Marque la notification comme lue"""
        self.lu = True
        self.save(update_fields=['lu'])

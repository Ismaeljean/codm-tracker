from django.db import models
from utilisateurs.models import Utilisateur

# Create your models here.
class Article(models.Model):
    LAYOUT_CHOICES = (
        ('standard', 'Standard (Texte + Images alternées)'),
        ('image_gauche', 'Image à gauche, Texte à droite'),
        ('image_droite', 'Texte à gauche, Image à droite'),
        ('image_centree', 'Image centrée avec texte'),
        ('texte_seul', 'Texte seul'),
    )
    
    titre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    contenu = models.TextField(help_text="Introduction de l'article")
    resume = models.TextField(max_length=300, blank=True, help_text="Résumé court de l'article (affiché dans la liste)")
    image = models.ImageField(upload_to='articles/', blank=True, null=True, help_text="Image principale de l'article (pour la liste)")
    auteur = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True)
    layout = models.CharField(max_length=20, choices=LAYOUT_CHOICES, default='standard', help_text="Layout principal de l'article")
    publie = models.BooleanField(default=False)
    cree_le = models.DateTimeField(auto_now_add=True)
    modifie_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['-cree_le']


class ArticleImage(models.Model):
    """Images supplémentaires pour un article"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='articles/images/', help_text="Image pour l'article")
    legende = models.CharField(max_length=200, blank=True, help_text="Légende de l'image")
    ordre = models.PositiveIntegerField(default=0, help_text="Ordre d'affichage (0 = premier)")
    date_ajout = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Image d'article"
        verbose_name_plural = "Images d'articles"
        ordering = ['ordre', 'date_ajout']
    
    def __str__(self):
        return f"Image {self.ordre} - {self.article.titre}"


class ArticleBlock(models.Model):
    """Blocs de contenu structurés pour un article"""
    TYPE_BLOCK_CHOICES = (
        ('texte', 'Bloc de texte'),
        ('titre', 'Titre/Sous-titre'),
        ('image', 'Image'),
        ('liste', 'Liste à puces'),
        ('citation', 'Citation'),
        ('code', 'Code/Commande'),
        ('video', 'Vidéo (iframe)'),
    )
    
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='blocks')
    type_block = models.CharField(max_length=20, choices=TYPE_BLOCK_CHOICES, default='texte')
    contenu = models.TextField(help_text="Contenu du bloc (texte, HTML, URL vidéo, etc.)")
    image = models.ForeignKey(ArticleImage, on_delete=models.SET_NULL, null=True, blank=True, help_text="Image associée (si type = image)")
    ordre = models.PositiveIntegerField(default=0, help_text="Ordre d'affichage (0 = premier)")
    alignement = models.CharField(max_length=20, choices=[
        ('gauche', 'Gauche'),
        ('droite', 'Droite'),
        ('centre', 'Centre'),
        ('pleine_largeur', 'Pleine largeur'),
    ], default='pleine_largeur', help_text="Alignement du bloc")
    date_ajout = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Bloc d'article"
        verbose_name_plural = "Blocs d'articles"
        ordering = ['ordre', 'date_ajout']
    
    def __str__(self):
        return f"{self.get_type_block_display()} - {self.article.titre}"

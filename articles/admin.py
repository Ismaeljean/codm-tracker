from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Article, ArticleImage, ArticleBlock


class ArticleImageInline(admin.TabularInline):
    """Inline pour gérer les images d'un article"""
    model = ArticleImage
    extra = 1
    fields = ('image', 'legende', 'ordre')
    ordering = ('ordre',)
    verbose_name = "Image supplémentaire"
    verbose_name_plural = "Images supplémentaires"
    
    def get_extra(self, request, obj=None, **kwargs):
        """Affiche 3 lignes vides si l'article est nouveau, 1 sinon"""
        if obj is None:
            return 3
        return 1


class ArticleBlockInline(admin.TabularInline):
    """Inline pour gérer les blocs de contenu d'un article"""
    model = ArticleBlock
    extra = 2
    fields = ('type_block', 'contenu', 'image', 'alignement', 'ordre')
    ordering = ('ordre',)
    verbose_name = "Bloc de contenu"
    verbose_name_plural = "Blocs de contenu"
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        # Limiter les images disponibles à celles de l'article
        if obj:
            formset.form.base_fields['image'].queryset = ArticleImage.objects.filter(article=obj)
        else:
            # Si l'article n'existe pas encore, désactiver le champ image
            formset.form.base_fields['image'].queryset = ArticleImage.objects.none()
            formset.form.base_fields['image'].help_text = "Enregistrez d'abord l'article et ajoutez des images, puis revenez ici."
        return formset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Configuration admin sophistiquée pour le modèle Article"""
    list_display = ('titre', 'auteur', 'layout', 'image_preview', 'publie', 'nb_images', 'nb_blocks', 'cree_le', 'modifie_le')
    list_filter = ('publie', 'layout', 'cree_le', 'modifie_le')
    search_fields = ('titre', 'contenu', 'resume', 'auteur__nom', 'auteur__prenom', 'auteur__email')
    prepopulated_fields = {'slug': ('titre',)}
    readonly_fields = ('cree_le', 'modifie_le', 'image_preview', 'stats_display')
    date_hierarchy = 'cree_le'
    inlines = [ArticleImageInline, ArticleBlockInline]
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('titre', 'slug', 'auteur', 'layout'),
            'description': 'Remplissez les informations de base de l\'article. Le slug sera généré automatiquement à partir du titre.'
        }),
        ('Contenu principal', {
            'fields': ('resume', 'image', 'image_preview', 'contenu'),
            'description': '<strong>Image principale :</strong> Image affichée sur la page de liste des blogs.<br>'
                          '<strong>Résumé :</strong> Texte court affiché sous l\'image dans la liste (max 300 caractères).<br>'
                          '<strong>Contenu :</strong> Texte optionnel. Pour un blog sophistiqué, utilisez plutôt les "Blocs de contenu" ci-dessous.'
        }),
        ('Images supplémentaires et Blocs de contenu', {
            'fields': (),
            'description': '<div style="background: #e7f3ff; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #007cba;">'
                          '<h4 style="margin-top: 0; color: #007cba;">📝 Guide de création d\'un blog professionnel</h4>'
                          '<p><strong>Étape 1 :</strong> Enregistrez d\'abord l\'article avec le titre, résumé et image principale.</p>'
                          '<p><strong>Étape 2 :</strong> Ajoutez des images supplémentaires dans la section "Images d\'articles" ci-dessous.</p>'
                          '<p><strong>Étape 3 :</strong> Créez des blocs de contenu dans la section "Blocs de contenu" pour structurer votre article :</p>'
                          '<ul style="margin-left: 20px;">'
                          '<li><strong>Paragraphe de Texte :</strong> Pour du texte simple</li>'
                          '<li><strong>Titre de Section :</strong> Pour les sous-titres</li>'
                          '<li><strong>Image :</strong> Choisissez une image ajoutée à l\'étape 2, puis l\'alignement (gauche, droite, centre, pleine largeur)</li>'
                          '<li><strong>Liste :</strong> Utilisez du HTML (&lt;ul&gt;&lt;li&gt;...&lt;/li&gt;&lt;/ul&gt; ou &lt;ol&gt;...&lt;/ol&gt;)</li>'
                          '<li><strong>Citation :</strong> Pour mettre en valeur une citation</li>'
                          '<li><strong>Bloc de Code :</strong> Pour afficher du code</li>'
                          '<li><strong>Vidéo :</strong> Collez l\'URL d\'intégration YouTube/Vimeo</li>'
                          '</ul>'
                          '<p><strong>💡 Astuce :</strong> Utilisez l\'ordre pour contrôler l\'affichage des blocs (0 = premier).</p>'
                          '</div>',
            'classes': ('collapse',)
        }),
        ('Publication', {
            'fields': ('publie', 'cree_le', 'modifie_le')
        }),
        ('Statistiques', {
            'fields': ('stats_display',),
            'classes': ('collapse',)
        }),
    )
    
    list_editable = ('publie',)
    
    def image_preview(self, obj):
        """Affiche un aperçu de l'image principale"""
        if obj and obj.pk and obj.image:
            return format_html(
                '<img src="{}" style="max-height: 150px; max-width: 200px; object-fit: cover; border-radius: 8px; border: 2px solid #ddd;"/>',
                obj.image.url
            )
        return mark_safe('<span style="color: #999;">Aucune image (enregistrez d\'abord l\'article)</span>')
    image_preview.short_description = 'Aperçu image principale'
    
    def nb_images(self, obj):
        """Affiche le nombre d'images supplémentaires"""
        if not obj or not obj.pk:
            return mark_safe('<span style="color: #999;">-</span>')
        count = obj.images.count()
        if count > 0:
            return format_html('<span style="color: #28a745; font-weight: bold;">{} image(s)</span>', count)
        return mark_safe('<span style="color: #999;">0</span>')
    nb_images.short_description = 'Images'
    
    def nb_blocks(self, obj):
        """Affiche le nombre de blocs de contenu"""
        if not obj or not obj.pk:
            return mark_safe('<span style="color: #999;">-</span>')
        count = obj.blocks.count()
        if count > 0:
            return format_html('<span style="color: #007cba; font-weight: bold;">{} bloc(s)</span>', count)
        return mark_safe('<span style="color: #999;">0</span>')
    nb_blocks.short_description = 'Blocs'
    
    def stats_display(self, obj):
        """Affiche les statistiques de l'article"""
        if not obj or not obj.pk:
            return mark_safe('<div style="padding: 15px; background: #f8f9fa; border-radius: 8px; color: #999;">Enregistrez d\'abord l\'article pour voir les statistiques</div>')
        
        nb_images = obj.images.count()
        nb_blocks = obj.blocks.count()
        
        return format_html(
            '<div style="padding: 15px; background: #f8f9fa; border-radius: 8px;">'
            '<p><strong>Images supplémentaires:</strong> {}</p>'
            '<p><strong>Blocs de contenu:</strong> {}</p>'
            '</div>',
            nb_images,
            nb_blocks
        )
    stats_display.short_description = 'Statistiques'


@admin.register(ArticleImage)
class ArticleImageAdmin(admin.ModelAdmin):
    """Configuration admin pour les images d'articles"""
    list_display = ('article', 'image_preview', 'legende', 'ordre', 'date_ajout')
    list_filter = ('date_ajout', 'article')
    search_fields = ('article__titre', 'legende')
    ordering = ('article', 'ordre', 'date_ajout')
    readonly_fields = ('date_ajout', 'image_preview')
    
    def image_preview(self, obj):
        """Affiche un aperçu de l'image"""
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 150px; object-fit: cover; border-radius: 8px; border: 2px solid #ddd;"/>',
                obj.image.url
            )
        return "Aucune image"
    image_preview.short_description = 'Aperçu'


@admin.register(ArticleBlock)
class ArticleBlockAdmin(admin.ModelAdmin):
    """Configuration admin pour les blocs de contenu"""
    list_display = ('article', 'type_block', 'contenu_preview', 'alignement', 'ordre', 'date_ajout')
    list_filter = ('type_block', 'alignement', 'date_ajout', 'article')
    search_fields = ('article__titre', 'contenu')
    ordering = ('article', 'ordre', 'date_ajout')
    readonly_fields = ('date_ajout',)
    
    def contenu_preview(self, obj):
        """Affiche un aperçu du contenu"""
        if obj and obj.contenu:
            preview = obj.contenu[:100]
            if len(obj.contenu) > 100:
                preview += '...'
            return format_html('<span style="color: #333;">{}</span>', preview)
        return "-"
    contenu_preview.short_description = 'Aperçu contenu'

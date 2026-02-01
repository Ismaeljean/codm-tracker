from django.contrib import admin
from django.utils.html import format_html
from .models import Communaute, MembreCommunaute, Post, LikePost, Commentaire, LikeCommentaire, Notification


@admin.register(Communaute)
class CommunauteAdmin(admin.ModelAdmin):
    list_display = ['nom', 'slug', 'nombre_posts', 'nombre_membres', 'est_active', 'date_creation']
    list_filter = ['est_active', 'date_creation']
    search_fields = ['nom', 'description']
    prepopulated_fields = {'slug': ('nom',)}
    readonly_fields = ['nombre_posts', 'nombre_membres', 'date_creation']


@admin.register(MembreCommunaute)
class MembreCommunauteAdmin(admin.ModelAdmin):
    list_display = ['utilisateur', 'communaute', 'date_join']
    list_filter = ['communaute', 'date_join']
    search_fields = ['utilisateur__nom', 'utilisateur__prenom', 'communaute__nom']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['titre', 'communaute', 'auteur', 'type_post', 'nombre_likes', 'nombre_commentaires', 'est_epingle', 'est_actif', 'date_creation']
    list_filter = ['communaute', 'type_post', 'est_actif', 'est_epingle', 'date_creation']
    search_fields = ['titre', 'contenu', 'auteur__nom', 'auteur__prenom']
    prepopulated_fields = {'slug': ('titre',)}
    readonly_fields = ['nombre_likes', 'nombre_commentaires', 'date_creation', 'date_modification']
    date_hierarchy = 'date_creation'


@admin.register(LikePost)
class LikePostAdmin(admin.ModelAdmin):
    list_display = ['utilisateur', 'post', 'date_creation']
    list_filter = ['date_creation']
    search_fields = ['utilisateur__nom', 'post__titre']


@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ['auteur', 'post', 'parent', 'nombre_likes', 'est_actif', 'date_creation']
    list_filter = ['est_actif', 'date_creation']
    search_fields = ['contenu', 'auteur__nom', 'post__titre']
    readonly_fields = ['nombre_likes', 'date_creation', 'date_modification']


@admin.register(LikeCommentaire)
class LikeCommentaireAdmin(admin.ModelAdmin):
    list_display = ['utilisateur', 'commentaire', 'date_creation']
    list_filter = ['date_creation']
    search_fields = ['utilisateur__nom']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['utilisateur', 'type_notification', 'titre', 'lu', 'date_creation', 'status_color']
    list_filter = ['type_notification', 'lu', 'date_creation']
    search_fields = ['utilisateur__nom', 'utilisateur__prenom', 'titre', 'message']
    readonly_fields = ['date_creation']
    date_hierarchy = 'date_creation'
    list_editable = ['lu']
    
    fieldsets = (
        ('Destinataire', {
            'fields': ('utilisateur',)
        }),
        ('Notification', {
            'fields': ('type_notification', 'titre', 'message', 'lien')
        }),
        ('Relations', {
            'fields': ('post', 'commentaire'),
            'classes': ('collapse',)
        }),
        ('Statut', {
            'fields': ('lu', 'date_creation')
        }),
    )
    
    def status_color(self, obj):
        """Affiche le statut avec une couleur"""
        if obj.lu:
            return format_html('<span style="color: #28a745; font-weight: bold;">✓ Lu</span>')
        return format_html('<span style="color: #ff1a1a; font-weight: bold;">● Non lu</span>')
    status_color.short_description = 'Statut'
    
    actions = ['marquer_comme_lu', 'marquer_comme_non_lu']
    
    def marquer_comme_lu(self, request, queryset):
        updated = queryset.update(lu=True)
        self.message_user(request, f'{updated} notification(s) marquée(s) comme lue(s).')
    marquer_comme_lu.short_description = 'Marquer comme lues'
    
    def marquer_comme_non_lu(self, request, queryset):
        updated = queryset.update(lu=False)
        self.message_user(request, f'{updated} notification(s) marquée(s) comme non lue(s).')
    marquer_comme_non_lu.short_description = 'Marquer comme non lues'

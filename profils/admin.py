from django.contrib import admin
from .models import ProfilJoueur


@admin.register(ProfilJoueur)
class ProfilJoueurAdmin(admin.ModelAdmin):
    """Configuration admin pour le modèle ProfilJoueur"""
    list_display = ('get_nom_complet', 'uid_codm', 'niveau', 'rang_mj', 'rang_br', 'get_email')
    list_filter = ('niveau', 'rang_mj', 'rang_br')
    search_fields = ('utilisateur__nom', 'utilisateur__prenom', 'utilisateur__email', 'uid_codm')
    readonly_fields = ('utilisateur',)
    fieldsets = (
        ('Utilisateur', {
            'fields': ('utilisateur',)
        }),
        ('Informations CODM', {
            'fields': ('uid_codm', 'niveau', 'rang_mj', 'rang_br')
        }),
        ('Profil', {
            'fields': ('avatar', 'bio')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Rendre l'utilisateur en lecture seule lors de l'édition"""
        if obj:  # Si on édite un objet existant
            return self.readonly_fields + ('utilisateur',)
        return self.readonly_fields
    
    def get_nom_complet(self, obj):
        """Affiche le nom complet de l'utilisateur"""
        return f"{obj.utilisateur.nom} {obj.utilisateur.prenom}"
    get_nom_complet.short_description = 'Nom complet'
    get_nom_complet.admin_order_field = 'utilisateur__nom'
    
    def get_email(self, obj):
        """Affiche l'email de l'utilisateur"""
        return obj.utilisateur.email
    get_email.short_description = 'Email'
    get_email.admin_order_field = 'utilisateur__email'

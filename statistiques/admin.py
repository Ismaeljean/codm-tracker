from django.contrib import admin
from .models import StatistiquesJoueur


@admin.register(StatistiquesJoueur)
class StatistiquesJoueurAdmin(admin.ModelAdmin):
    """Configuration admin pour le modèle StatistiquesJoueur"""
    list_display = ('get_nom_complet', 'mode', 'ratio_kd', 'victoires', 'matchs', 'top10', 'mis_a_jour_le')
    list_filter = ('mode', 'mis_a_jour_le')
    search_fields = ('profil__utilisateur__nom', 'profil__utilisateur__prenom', 'profil__utilisateur__email')
    readonly_fields = ('mis_a_jour_le',)
    date_hierarchy = 'mis_a_jour_le'
    
    fieldsets = (
        ('Joueur', {
            'fields': ('profil',)
        }),
        ('Statistiques', {
            'fields': ('mode', 'ratio_kd', 'victoires', 'matchs', 'top10')
        }),
        ('Dates', {
            'fields': ('mis_a_jour_le',)
        }),
    )
    
    def get_nom_complet(self, obj):
        """Affiche le nom complet du joueur"""
        return f"{obj.profil.utilisateur.nom} {obj.profil.utilisateur.prenom}"
    get_nom_complet.short_description = 'Joueur'
    get_nom_complet.admin_order_field = 'profil__utilisateur__nom'

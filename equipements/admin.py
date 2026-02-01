from django.contrib import admin
from django.utils.html import format_html
import json
from .models import Equipement


@admin.register(Equipement)
class EquipementAdmin(admin.ModelAdmin):
    """Configuration admin pour le modèle Equipement"""
    list_display = ('get_nom_complet', 'arme', 'get_accessoires_summary', 'cree_le')
    list_filter = ('cree_le',)
    search_fields = ('arme', 'profil__utilisateur__nom', 'profil__utilisateur__prenom', 'profil__utilisateur__email')
    readonly_fields = ('cree_le', 'accessoires_display', 'sensibilite_display')
    date_hierarchy = 'cree_le'
    
    fieldsets = (
        ('Joueur', {
            'fields': ('profil',)
        }),
        ('Arme', {
            'fields': ('arme',)
        }),
        ('Accessoires', {
            'fields': ('accessoires', 'accessoires_display')
        }),
        ('Sensibilités', {
            'fields': ('sensibilite', 'sensibilite_display')
        }),
        ('Date', {
            'fields': ('cree_le',)
        }),
    )
    
    def get_nom_complet(self, obj):
        """Affiche le nom complet du joueur"""
        return f"{obj.profil.utilisateur.nom} {obj.profil.utilisateur.prenom}"
    get_nom_complet.short_description = 'Joueur'
    get_nom_complet.admin_order_field = 'profil__utilisateur__nom'
    
    def get_accessoires_summary(self, obj):
        """Affiche un résumé des accessoires"""
        if obj.accessoires:
            count = sum(1 for v in obj.accessoires.values() if v)
            return f"{count} accessoire(s)"
        return "Aucun"
    get_accessoires_summary.short_description = 'Accessoires'
    
    def accessoires_display(self, obj):
        """Affiche les accessoires de manière formatée"""
        if not obj.accessoires:
            return "Aucun accessoire"
        
        html = "<ul style='margin: 0; padding-left: 20px;'>"
        for key, value in obj.accessoires.items():
            if value:
                html += f"<li><strong>{key.capitalize()}:</strong> {value}</li>"
        html += "</ul>"
        return format_html(html)
    accessoires_display.short_description = 'Détails des accessoires'
    
    def sensibilite_display(self, obj):
        """Affiche les sensibilités de manière formatée"""
        if not obj.sensibilite:
            return "Aucune sensibilité"
        
        html = "<ul style='margin: 0; padding-left: 20px;'>"
        for key, value in obj.sensibilite.items():
            if value:
                html += f"<li><strong>{key.capitalize()}:</strong> {value}</li>"
        html += "</ul>"
        return format_html(html)
    sensibilite_display.short_description = 'Détails des sensibilités'

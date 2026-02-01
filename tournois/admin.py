from django.contrib import admin
from django import forms
from .models import Tournoi, ParticipantTournoi, EquipeTournoi


class ParticipantTournoiInline(admin.TabularInline):
    """Inline pour afficher les participants dans l'admin du tournoi"""
    model = ParticipantTournoi
    extra = 0
    readonly_fields = ('rejoint_le',)
    fields = ('profil', 'rejoint_le')


class TournoiAdminForm(forms.ModelForm):
    """Formulaire personnalisé pour gérer type_tournoi selon le mode"""
    class Meta:
        model = Tournoi
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si c'est un objet existant avec mode MJ, masquer type_tournoi
        if self.instance and self.instance.pk and self.instance.mode == 'MJ':
            self.fields['type_tournoi'].widget = forms.HiddenInput()
            self.fields['type_tournoi'].required = False


@admin.register(Tournoi)
class TournoiAdmin(admin.ModelAdmin):
    """Configuration admin pour le modèle Tournoi"""
    form = TournoiAdminForm
    list_display = ('titre', 'mode', 'get_type_display', 'date_debut', 'date_fin', 'prix_participation', 'recompense', 'get_nb_participants')
    list_filter = ('mode', 'type_tournoi', 'date_debut', 'date_fin')
    search_fields = ('titre', 'description', 'recompense')
    date_hierarchy = 'date_debut'
    inlines = [ParticipantTournoiInline]
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('titre', 'description', 'mode', 'image')
        }),
        ('Type de Tournoi (Battle Royale uniquement)', {
            'fields': ('type_tournoi',),
            'description': 'Le type de tournoi (Solo/Duo/Escouade) s\'applique uniquement au mode Battle Royale. Pour Multijoueur, l\'équipe est toujours de 5 joueurs.',
            'classes': ('collapse',),
        }),
        ('Dates', {
            'fields': ('date_debut', 'date_fin')
        }),
        ('Participation', {
            'fields': ('prix_participation',)
        }),
        ('Récompense', {
            'fields': ('recompense',)
        }),
    )
    
    def get_nb_participants(self, obj):
        """Affiche le nombre de participants"""
        count = obj.participants.count()
        return f"{count} participant(s)"
    get_nb_participants.short_description = 'Participants'
    
    def get_type_display(self, obj):
        """Affiche le type de tournoi selon le mode"""
        if obj.mode == 'MJ':
            return '5 Joueurs (MJ)'
        elif obj.mode == 'BR' and obj.type_tournoi:
            return obj.get_type_tournoi_display()
        return '-'
    get_type_display.short_description = 'Type'
    
    class Media:
        js = ('admin/js/tournoi_admin.js',)


@admin.register(EquipeTournoi)
class EquipeTournoiAdmin(admin.ModelAdmin):
    """Configuration admin pour le modèle EquipeTournoi"""
    list_display = ('code_invitation', 'tournoi', 'get_nom_createur', 'get_nb_membres', 'complete', 'cree_le')
    list_filter = ('tournoi', 'complete', 'cree_le')
    search_fields = ('code_invitation', 'tournoi__titre', 'createur__utilisateur__nom', 'createur__utilisateur__prenom')
    readonly_fields = ('code_invitation', 'cree_le', 'get_nb_membres_display')
    date_hierarchy = 'cree_le'
    
    def get_nom_createur(self, obj):
        """Affiche le nom du créateur"""
        return f"{obj.createur.utilisateur.nom} {obj.createur.utilisateur.prenom}"
    get_nom_createur.short_description = 'Créateur'
    
    def get_nb_membres(self, obj):
        """Affiche le nombre de membres"""
        return f"{obj.get_nb_membres()}/{obj.get_nb_membres_requis()}"
    get_nb_membres.short_description = 'Membres'
    
    def get_nb_membres_display(self, obj):
        """Affiche le nombre de membres (readonly)"""
        return f"{obj.get_nb_membres()}/{obj.get_nb_membres_requis()}"
    get_nb_membres_display.short_description = 'Membres'


@admin.register(ParticipantTournoi)
class ParticipantTournoiAdmin(admin.ModelAdmin):
    """Configuration admin pour le modèle ParticipantTournoi"""
    list_display = ('get_nom_complet', 'tournoi', 'equipe', 'paiement_effectue', 'rejoint_le')
    list_filter = ('tournoi', 'equipe', 'paiement_effectue', 'rejoint_le')
    search_fields = ('profil__utilisateur__nom', 'profil__utilisateur__prenom', 'tournoi__titre', 'equipe__code_invitation')
    readonly_fields = ('rejoint_le',)
    date_hierarchy = 'rejoint_le'
    
    def get_nom_complet(self, obj):
        """Affiche le nom complet du participant"""
        return f"{obj.profil.utilisateur.nom} {obj.profil.utilisateur.prenom}"
    get_nom_complet.short_description = 'Participant'
    get_nom_complet.admin_order_field = 'profil__utilisateur__nom'

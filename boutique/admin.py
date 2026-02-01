from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse
from .models import Categorie, Produit, Panier, PanierProduit, Commande, Paiement



@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'image_preview', 'produits_count']
    search_fields = ['nom']
    ordering = ['nom']
    fields = ['nom', 'image']
    
    def image_preview(self, obj):
        if obj and obj.image:
            return format_html('<img src="{}" style="height:50px; width:50px; object-fit:cover; border-radius:8px; border: 2px solid #ddd;"/>', obj.image.url)
        return mark_safe('<div style="height:50px; width:50px; background:#f8f9fa; border:2px dashed #dee2e6; border-radius:8px; display:flex; align-items:center; justify-content:center; color:#6c757d;">📦</div>')
    image_preview.short_description = 'Image'
    
    def produits_count(self, obj):
        count = obj.produit_set.count()
        return format_html('<span style="color: #007cba; font-weight: bold;">{} produits</span>', count)
    produits_count.short_description = 'Nombre de produits'


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'nom', 'categorie', 'prix_display', 'prix_reduit_display', 'stock', 'is_active', 'status_color']
    list_filter = ['categorie', 'is_active']
    search_fields = ['nom', 'description']
    ordering = ['nom']
    list_editable = ['stock', 'is_active']
    readonly_fields = ['image_preview']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'description', 'categorie', 'image_preview', 'image')
        }),
        ('Prix', {
            'fields': ('prix', 'prix_reduit')
        }),
        ('Stock et statut', {
            'fields': ('stock', 'is_active')
        })
    )
    
    def image_preview(self, obj):
        if obj and obj.pk and obj.image:
            return format_html('<img src="{}" style="height:60px; width:60px; object-fit:cover; border-radius:8px; border: 2px solid #ddd;"/>', obj.image.url)
        return mark_safe('<div style="height:60px; width:60px; background:#f8f9fa; border:2px dashed #dee2e6; border-radius:8px; display:flex; align-items:center; justify-content:center; color:#6c757d; font-size:24px;">📦</div>')
    image_preview.short_description = 'Aperçu'
    
    def prix_display(self, obj):
        prix = f"{obj.prix:.0f}"
        return format_html('<span style="color: #28a745; font-weight: bold;">{} XOF</span>', prix)
    prix_display.short_description = 'Prix'
    
    def prix_reduit_display(self, obj):
        if obj.prix_reduit:
            prix = f"{obj.prix_reduit:.0f}"
            return format_html('<span style="color: #dc3545; font-weight: bold; text-decoration: line-through;">{} XOF</span>', prix)
        return format_html('<span style="color: #6c757d;">-</span>')
    prix_reduit_display.short_description = 'Prix Réduit'
    
    def status_color(self, obj):
        if obj.stock <= 0:
            return format_html('<span style="color: red; font-weight: bold;">Rupture de stock</span>')
        elif obj.stock <= 10:
            return format_html('<span style="color: orange; font-weight: bold;">Stock faible</span>')
        else:
            return format_html('<span style="color: green; font-weight: bold;">En stock</span>')
    status_color.short_description = 'Statut du stock'
    
    actions = ['activate_products', 'deactivate_products', 'restock_products']
    
    def activate_products(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} produits activés avec succès.')
    activate_products.short_description = 'Activer les produits sélectionnés'
    
    def deactivate_products(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} produits désactivés avec succès.')
    deactivate_products.short_description = 'Désactiver les produits sélectionnés'
    
    def restock_products(self, request, queryset):
        updated = queryset.update(stock=100)
        self.message_user(request, f'{updated} produits remis en stock (100 unités).')
    restock_products.short_description = 'Remettre en stock (100 unités)'


class PanierProduitInline(admin.TabularInline):
    model = PanierProduit
    extra = 0
    readonly_fields = ['produit', 'quantite', 'prix_unitaire', 'total_ligne', 'image_preview']
    fields = ['image_preview', 'produit', 'quantite', 'prix_unitaire', 'total_ligne']
    
    def image_preview(self, obj):
        if obj and obj.produit and obj.produit.image:
            return format_html('<img src="{}" style="height:40px; width:40px; object-fit:cover; border-radius:4px;"/>', obj.produit.image.url)
        return format_html('<div style="height:40px; width:40px; background:#f8f9fa; border:1px dashed #dee2e6; border-radius:4px; display:flex; align-items:center; justify-content:center; color:#6c757d; font-size:16px;">📦</div>')
    image_preview.short_description = 'Image'
    
    def prix_unitaire(self, obj):
        if obj and obj.produit:
            prix = obj.prix_unitaire
            return format_html('<span style="color: #007cba; font-weight: bold;">{} XOF</span>', f"{prix:.0f}")
        return '-'
    prix_unitaire.short_description = 'Prix unitaire'
    
    def total_ligne(self, obj):
        if obj and obj.produit:
            total = obj.total_ligne
            return format_html('<span style="color: #28a745; font-weight: bold;">{} XOF</span>', f"{total:.0f}")
        return '-'
    total_ligne.short_description = 'Total ligne'


@admin.register(Panier)
class PanierAdmin(admin.ModelAdmin):
    list_display = ['id', 'utilisateur', 'statut', 'total_calculated', 'date_creation', 'items_count']
    list_filter = ['statut', 'date_creation']
    search_fields = ['utilisateur__nom', 'utilisateur__email']
    ordering = ['-date_creation']
    readonly_fields = ['date_creation', 'total_calculated']
    inlines = [PanierProduitInline]
    
    def total_calculated(self, obj):
        total = sum(
            item.quantite * (item.produit.prix_gros if item.type_commande == 'gros' else item.produit.prix_detail)
            for item in obj.panierproduit_set.all()
        )
        return format_html('<span style="color: #007cba; font-weight: bold;">{} XOF</span>', f"{total:.0f}")
    total_calculated.short_description = 'Total calculé'
    
    def items_count(self, obj):
        count = obj.panierproduit_set.count()
        return format_html('<span style="color: #007cba;">{} articles</span>', count)
    items_count.short_description = 'Articles'


@admin.register(PanierProduit)
class PanierProduitAdmin(admin.ModelAdmin):
    list_display = ['id', 'panier', 'produit', 'quantite', 'prix_unitaire', 'total_ligne']
    search_fields = ['produit__nom', 'panier__utilisateur__nom']
    ordering = ['-id']
    
    def prix_unitaire(self, obj):
        prix = obj.prix_unitaire
        return format_html('{} XOF', f"{prix:.0f}")
    prix_unitaire.short_description = 'Prix unitaire'
    
    def total_ligne(self, obj):
        total = obj.total_ligne
        return format_html('<span style="color: #007cba; font-weight: bold;">{} XOF</span>', f"{total:.0f}")
    total_ligne.short_description = 'Total ligne'


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ['id', 'utilisateur', 'total', 'statut', 'date_commande', 'mode_paiement', 'status_color']
    list_filter = ['statut', 'mode_paiement', 'date_commande']
    search_fields = ['utilisateur__nom', 'utilisateur__email', 'id']
    ordering = ['-date_commande']
    readonly_fields = ['date_commande', 'produits_details']
    
    fieldsets = (
        ('Informations de la commande', {
            'fields': ('utilisateur', 'panier', 'total', 'statut')
        }),
        ('Produits commandés', {
            'fields': ('produits_details',),
            'classes': ('wide',)
        }),
        ('Livraison et paiement', {
            'fields': ('adresse_livraison', 'mode_paiement')
        }),
        ('Dates', {
            'fields': ('date_commande',),
            'classes': ('collapse',)
        })
    )
    
    def produits_details(self, obj):
        """Affiche les détails des produits de la commande"""
        if not obj or not obj.panier:
            return format_html('<p style="color: #6c757d;">Aucun produit dans cette commande.</p>')
        
        produits = obj.panier.panierproduit_set.select_related('produit').all()
        if not produits:
            return format_html('<p style="color: #6c757d;">Aucun produit dans cette commande.</p>')
        
        html = '<div style="overflow-x: auto;">'
        html += '<table style="width: 100%; border-collapse: collapse; margin: 10px 0;">'
        html += '<thead>'
        html += '<tr style="background-color: #f8f9fa; border: 1px solid #dee2e6;">'
        html += '<th style="padding: 8px; border: 1px solid #dee2e6; text-align: left;">Image</th>'
        html += '<th style="padding: 8px; border: 1px solid #dee2e6; text-align: left;">Produit</th>'
        html += '<th style="padding: 8px; border: 1px solid #dee2e6; text-align: center;">Quantité</th>'
        html += '<th style="padding: 8px; border: 1px solid #dee2e6; text-align: right;">Prix unitaire</th>'
        html += '<th style="padding: 8px; border: 1px solid #dee2e6; text-align: right;">Total ligne</th>'
        html += '</tr>'
        html += '</thead>'
        html += '<tbody>'
        
        for item in produits:
            prix = item.prix_unitaire
            total_ligne = item.total_ligne
            
            html += '<tr style="border: 1px solid #dee2e6;">'
            
            # Image
            if item.produit.image:
                html += f'<td style="padding: 8px; border: 1px solid #dee2e6; text-align: center;">'
                html += f'<img src="{item.produit.image.url}" style="height: 50px; width: 50px; object-fit: cover; border-radius: 6px; border: 1px solid #ddd;"/>'
                html += '</td>'
            else:
                html += '<td style="padding: 8px; border: 1px solid #dee2e6; text-align: center;">'
                html += '<div style="height: 50px; width: 50px; background: #f8f9fa; border: 1px dashed #dee2e6; border-radius: 6px; display: flex; align-items: center; justify-content: center; color: #6c757d; font-size: 20px;">📦</div>'
                html += '</td>'
            
            # Nom du produit
            html += f'<td style="padding: 8px; border: 1px solid #dee2e6;"><strong>{item.produit.nom}</strong></td>'
            
            # Quantité
            html += f'<td style="padding: 8px; border: 1px solid #dee2e6; text-align: center;"><span style="background: #e3f2fd; color: #1976d2; padding: 4px 8px; border-radius: 4px; font-weight: bold;">{item.quantite}</span></td>'
            
            # Prix unitaire
            html += f'<td style="padding: 8px; border: 1px solid #dee2e6; text-align: right;">'
            html += f'<span style="color: #007cba; font-weight: bold;">{prix:.0f} XOF</span>'
            html += '</td>'
            
            # Total ligne
            html += f'<td style="padding: 8px; border: 1px solid #dee2e6; text-align: right;">'
            html += f'<span style="color: #28a745; font-weight: bold;">{total_ligne:.0f} XOF</span>'
            html += '</td>'
            
            html += '</tr>'
        
        html += '</tbody>'
        html += '</table>'
        html += '</div>'
        
        return format_html(html)
    produits_details.short_description = 'Détails des produits'
    
    def status_color(self, obj):
        colors = {
            'en_attente': 'orange',
            'valide': 'green',
            'livre': 'blue'
        }
        color = colors.get(obj.statut, 'gray')
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, obj.get_statut_display())
    status_color.short_description = 'Statut'
    
    actions = ['mark_as_validated', 'mark_as_delivered']
    
    def mark_as_validated(self, request, queryset):
        updated = queryset.update(statut='valide')
        self.message_user(request, f'{updated} commandes validées avec succès.')
    mark_as_validated.short_description = 'Marquer comme validées'
    
    def mark_as_delivered(self, request, queryset):
        updated = queryset.update(statut='livre')
        self.message_user(request, f'{updated} commandes marquées comme livrées.')
    mark_as_delivered.short_description = 'Marquer comme livrées'


@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ['id', 'commande', 'reference_paystack', 'montant', 'statut', 'mode_paiement', 'date_creation', 'date_paiement', 'status_color']
    list_filter = ['statut', 'mode_paiement', 'date_creation']
    search_fields = ['reference_paystack', 'commande__numero_commande', 'commande__utilisateur__nom', 'commande__utilisateur__email']
    ordering = ['-date_creation']
    readonly_fields = ['date_creation', 'date_paiement', 'metadata_display']
    
    fieldsets = (
        ('Informations du paiement', {
            'fields': ('commande', 'reference_paystack', 'montant', 'statut', 'mode_paiement')
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_paiement'),
            'classes': ('collapse',)
        }),
        ('Métadonnées Paystack', {
            'fields': ('metadata_display',),
            'classes': ('collapse',)
        })
    )
    
    def metadata_display(self, obj):
        """Affiche les métadonnées Paystack de manière lisible"""
        if obj.metadata:
            import json
            return format_html('<pre style="background: #f8f9fa; padding: 10px; border-radius: 4px; overflow-x: auto;">{}</pre>', 
                             json.dumps(obj.metadata, indent=2, ensure_ascii=False))
        return format_html('<p style="color: #6c757d;">Aucune métadonnée disponible.</p>')
    metadata_display.short_description = 'Métadonnées Paystack'
    
    def status_color(self, obj):
        colors = {
            'en_attente': 'orange',
            'payee': 'green',
            'echec': 'red',
            'annule': 'gray'
        }
        color = colors.get(obj.statut, 'gray')
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, obj.get_statut_display())
    status_color.short_description = 'Statut'
    
    actions = ['mark_as_paid', 'mark_as_failed']
    
    def mark_as_paid(self, request, queryset):
        for paiement in queryset:
            paiement.marquer_comme_paye()
        self.message_user(request, f'{queryset.count()} paiements marqués comme payés.')
    mark_as_paid.short_description = 'Marquer comme payés'
    
    def mark_as_failed(self, request, queryset):
        updated = queryset.update(statut='echec')
        self.message_user(request, f'{updated} paiements marqués comme échecs.')
    mark_as_failed.short_description = 'Marquer comme échecs'


# Personnalisation de l'interface admin
admin.site.site_header = "CODM Tracker - Administration"
admin.site.site_title = "CODM Tracker Admin"
admin.site.index_title = "Tableau de bord CODM Tracker"

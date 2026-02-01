"""
Script pour créer un article de type GUIDE avec images alternées (gauche/droite)
Usage: python manage.py create_guide_article
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from articles.models import Article, ArticleBlock
from utilisateurs.models import Utilisateur


class Command(BaseCommand):
    help = 'Crée un article de type GUIDE avec images alternées gauche/droite'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            default=None,
            help='Email de l\'utilisateur qui sera l\'auteur',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Création d\'un article GUIDE avec images alternées...\n'))

        # Récupérer l'auteur
        email = options.get('email')
        if email:
            try:
                auteur = Utilisateur.objects.get(email=email)
            except Utilisateur.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'❌ Utilisateur avec email {email} non trouvé'))
                return
        else:
            auteur = Utilisateur.objects.filter(is_superuser=True).first()
            if not auteur:
                auteur = Utilisateur.objects.first()
            if not auteur:
                self.stdout.write(self.style.ERROR('❌ Aucun utilisateur trouvé.'))
                return

        self.stdout.write(f'📝 Auteur: {auteur.nom} {auteur.prenom} ({auteur.email})\n')

        # Créer l'article
        titre = "Guide Complet : Maîtriser les Armes Assault Rifle dans CODM"
        slug = slugify(titre)
        base_slug = slug
        counter = 1
        while Article.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        article = Article.objects.create(
            titre=titre,
            slug=slug,
            resume="Apprenez à maîtriser les meilleures armes AR de Call of Duty Mobile. Guide détaillé avec configurations, stratégies et conseils de pros.",
            auteur=auteur,
            layout='standard',
            publie=True,
            contenu="",
        )

        self.stdout.write(self.style.SUCCESS(f'✅ Article créé: "{article.titre}" (ID: {article.pk})\n'))

        # Blocs avec images alternées
        blocs_data = [
            {
                'type_block': 'titre',
                'contenu': 'Introduction aux Assault Rifles',
                'ordre': 0,
            },
            {
                'type_block': 'texte',
                'contenu': 'Les Assault Rifles (AR) sont les armes les plus polyvalentes de Call of Duty Mobile. '
                          'Dans ce guide complet, nous allons explorer les meilleures AR, leurs configurations optimales, '
                          'et les stratégies pour les dominer sur le champ de bataille.',
                'ordre': 1,
            },
            {
                'type_block': 'image',
                'contenu': '',
                'ordre': 2,
                'alignement': 'pleine_largeur',
                'note': 'Image principale des AR (pleine largeur)',
            },
            {
                'type_block': 'titre',
                'contenu': 'AK-47 : La Légende',
                'ordre': 3,
            },
            {
                'type_block': 'image',
                'contenu': '',
                'ordre': 4,
                'alignement': 'gauche',
                'note': 'Screenshot AK-47 (gauche)',
            },
            {
                'type_block': 'texte',
                'contenu': 'L\'AK-47 reste l\'une des armes les plus populaires et efficaces de CODM. '
                          'Avec un excellent équilibre entre dégâts et précision, elle convient à tous les styles de jeu. '
                          'Sa cadence de tir modérée permet un contrôle optimal, même à longue distance.',
                'ordre': 5,
            },
            {
                'type_block': 'liste',
                'contenu': '<ul><li><strong>Dégâts:</strong> Très élevés</li><li><strong>Portée:</strong> Excellente</li><li><strong>Contrôle:</strong> Moyen</li><li><strong>Cadence:</strong> Modérée</li><li><strong>Meilleur pour:</strong> Combat à moyenne/longue portée</li></ul>',
                'ordre': 6,
            },
            {
                'type_block': 'titre',
                'contenu': 'M4 : Polyvalence Parfaite',
                'ordre': 7,
            },
            {
                'type_block': 'image',
                'contenu': '',
                'ordre': 8,
                'alignement': 'droite',
                'note': 'Screenshot M4 (droite)',
            },
            {
                'type_block': 'texte',
                'contenu': 'La M4 est l\'arme de référence pour les joueurs qui recherchent la polyvalence. '
                          'Avec une cadence de tir élevée et un contrôle remarquable, elle excelle dans tous les types de combat. '
                          'Parfaite pour les débutants comme pour les joueurs expérimentés.',
                'ordre': 9,
            },
            {
                'type_block': 'liste',
                'contenu': '<ul><li><strong>Dégâts:</strong> Moyens</li><li><strong>Portée:</strong> Bonne</li><li><strong>Contrôle:</strong> Excellent</li><li><strong>Cadence:</strong> Élevée</li><li><strong>Meilleur pour:</strong> Combat polyvalent à toutes distances</li></ul>',
                'ordre': 10,
            },
            {
                'type_block': 'titre',
                'contenu': 'ICR-1 : Précision Létale',
                'ordre': 11,
            },
            {
                'type_block': 'image',
                'contenu': '',
                'ordre': 12,
                'alignement': 'gauche',
                'note': 'Screenshot ICR-1 (gauche)',
            },
            {
                'type_block': 'texte',
                'contenu': 'L\'ICR-1 est l\'arme de choix pour les snipers qui préfèrent les AR. '
                          'Avec un recul minimal et une précision exceptionnelle, elle permet d\'éliminer les ennemis '
                          'à longue distance avec une facilité déconcertante.',
                'ordre': 13,
            },
            {
                'type_block': 'liste',
                'contenu': '<ul><li><strong>Dégâts:</strong> Élevés</li><li><strong>Portée:</strong> Exceptionnelle</li><li><strong>Contrôle:</strong> Parfait</li><li><strong>Cadence:</strong> Modérée</li><li><strong>Meilleur pour:</strong> Combat à longue portée et précision</li></ul>',
                'ordre': 14,
            },
            {
                'type_block': 'titre',
                'contenu': 'Configurations Recommandées',
                'ordre': 15,
            },
            {
                'type_block': 'texte',
                'contenu': 'Voici les meilleures configurations pour chaque arme :',
                'ordre': 16,
            },
            {
                'type_block': 'titre',
                'contenu': 'AK-47 - Build Agressif',
                'ordre': 17,
            },
            {
                'type_block': 'code',
                'contenu': 'Accessoires:\n- Canon: Canon court\n- Crosse: Crosse de combat\n- Poignée: Poignée avant tactique\n- Chargeur: Chargeur rapide étendu\n- Optique: Point rouge',
                'ordre': 18,
            },
            {
                'type_block': 'citation',
                'contenu': 'Cette configuration maximise la mobilité et la cadence de tir, parfaite pour le combat rapproché.',
                'ordre': 19,
            },
            {
                'type_block': 'titre',
                'contenu': 'M4 - Build Équilibré',
                'ordre': 20,
            },
            {
                'type_block': 'code',
                'contenu': 'Accessoires:\n- Canon: Canon de précision\n- Crosse: Crosse de tireur d\'élite\n- Poignée: Poignée avant\n- Chargeur: Chargeur étendu\n- Optique: Lunette x3',
                'ordre': 21,
            },
            {
                'type_block': 'titre',
                'contenu': 'Stratégies de Combat',
                'ordre': 22,
            },
            {
                'type_block': 'texte',
                'contenu': 'Pour maîtriser les AR, suivez ces stratégies éprouvées :',
                'ordre': 23,
            },
            {
                'type_block': 'liste',
                'contenu': '<ol><li><strong>Positionnement:</strong> Utilisez la couverture et les angles pour maximiser votre avantage</li><li><strong>Contrôle du recul:</strong> Apprenez les patterns de recul de chaque arme</li><li><strong>Gestion des munitions:</strong> Surveillez votre chargeur et rechargez au bon moment</li><li><strong>Adaptation:</strong> Changez de configuration selon la carte et le mode de jeu</li><li><strong>Pratique:</strong> Entraînez-vous régulièrement en mode entraînement</li></ol>',
                'ordre': 24,
            },
            {
                'type_block': 'image',
                'contenu': '',
                'ordre': 25,
                'alignement': 'centre',
                'note': 'Image de comparaison des AR (centre)',
            },
            {
                'type_block': 'titre',
                'contenu': 'Conclusion',
                'ordre': 26,
            },
            {
                'type_block': 'texte',
                'contenu': 'Chaque AR a ses forces et ses faiblesses. La clé du succès réside dans la compréhension '
                          'de chaque arme et l\'adaptation à votre style de jeu. Expérimentez avec différentes configurations '
                          'et trouvez celle qui vous convient le mieux.',
                'ordre': 27,
            },
            {
                'type_block': 'citation',
                'contenu': 'Rappelez-vous : une bonne arme ne fait pas un bon joueur, mais un bon joueur sait tirer le meilleur parti de chaque arme.',
                'ordre': 28,
            },
        ]

        # Créer les blocs
        for bloc_data in blocs_data:
            bloc = ArticleBlock.objects.create(
                article=article,
                type_block=bloc_data['type_block'],
                contenu=bloc_data['contenu'],
                ordre=bloc_data['ordre'],
                alignement=bloc_data.get('alignement', 'pleine_largeur'),
            )
            message = f'  ✓ Bloc créé: {bloc.get_type_block_display()} (ordre: {bloc.ordre})'
            if bloc_data.get('note'):
                message += f' - {bloc_data["note"]}'
            self.stdout.write(message)

        self.stdout.write(self.style.SUCCESS(f'\n✅ {len(blocs_data)} blocs créés avec succès!\n'))
        self.stdout.write(self.style.WARNING('📸 N\'oubliez pas d\'ajouter les images dans l\'admin Django!\n'))
        self.stdout.write(self.style.SUCCESS('🎉 Article GUIDE créé!\n'))
        self.stdout.write(f'🔗 URL: http://127.0.0.1:8000/blog/{article.slug}/\n')
        self.stdout.write(f'✏️  Admin: http://127.0.0.1:8000/admin/articles/article/{article.pk}/change/\n')

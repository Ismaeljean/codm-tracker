"""
Script pour créer un article de type TUTORIEL ÉTAPE PAR ÉTAPE avec images alternées
Usage: python manage.py create_tutorial_article
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from articles.models import Article, ArticleBlock
from utilisateurs.models import Utilisateur


class Command(BaseCommand):
    help = 'Crée un article de type TUTORIEL avec images alternées et étapes détaillées'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            default=None,
            help='Email de l\'utilisateur qui sera l\'auteur',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Création d\'un article TUTORIEL étape par étape...\n'))

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
        titre = "Tutoriel : Comment Créer le Loadout Parfait pour Ranked"
        slug = slugify(titre)
        base_slug = slug
        counter = 1
        while Article.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        article = Article.objects.create(
            titre=titre,
            slug=slug,
            resume="Apprenez à créer des loadouts optimaux pour le mode Ranked. Guide étape par étape avec exemples concrets et conseils de pros.",
            auteur=auteur,
            layout='standard',
            publie=True,
            contenu="",
        )

        self.stdout.write(self.style.SUCCESS(f'✅ Article créé: "{article.titre}" (ID: {article.pk})\n'))

        # Blocs de tutoriel avec images alternées
        blocs_data = [
            {
                'type_block': 'titre',
                'contenu': 'Introduction',
                'ordre': 0,
            },
            {
                'type_block': 'texte',
                'contenu': 'Créer le loadout parfait pour le mode Ranked nécessite une compréhension approfondie '
                          'des mécaniques du jeu, des armes, et des stratégies. Ce tutoriel vous guidera étape par étape '
                          'pour construire des loadouts qui vous donneront un avantage compétitif.',
                'ordre': 1,
            },
            {
                'type_block': 'image',
                'contenu': '',
                'ordre': 2,
                'alignement': 'pleine_largeur',
                'note': 'Image d\'introduction - Écran de création de loadout (pleine largeur)',
            },
            {
                'type_block': 'titre',
                'contenu': 'Étape 1 : Choisir l\'Arme Principale',
                'ordre': 3,
            },
            {
                'type_block': 'texte',
                'contenu': 'La première étape consiste à sélectionner votre arme principale. '
                          'Pour le mode Ranked, privilégiez les armes polyvalentes et fiables.',
                'ordre': 4,
            },
            {
                'type_block': 'image',
                'contenu': '',
                'ordre': 5,
                'alignement': 'gauche',
                'note': 'Screenshot sélection arme (gauche)',
            },
            {
                'type_block': 'liste',
                'contenu': '<ol><li>Analysez la carte et le mode de jeu</li><li>Choisissez une arme adaptée à votre style</li><li>Vérifiez les statistiques (dégâts, portée, contrôle)</li><li>Testez l\'arme en mode entraînement</li></ol>',
                'ordre': 6,
            },
            {
                'type_block': 'citation',
                'contenu': 'Astuce : Les armes polyvalentes comme la M4 ou l\'AK-47 sont souvent les meilleurs choix pour débuter.',
                'ordre': 7,
            },
            {
                'type_block': 'titre',
                'contenu': 'Étape 2 : Configurer les Accessoires',
                'ordre': 8,
            },
            {
                'type_block': 'texte',
                'contenu': 'Les accessoires peuvent faire toute la différence. Chaque slot doit être optimisé '
                          'pour maximiser les performances de votre arme selon votre style de jeu.',
                'ordre': 9,
            },
            {
                'type_block': 'image',
                'contenu': '',
                'ordre': 10,
                'alignement': 'droite',
                'note': 'Screenshot configuration accessoires (droite)',
            },
            {
                'type_block': 'titre',
                'contenu': 'Configuration Agressive',
                'ordre': 11,
            },
            {
                'type_block': 'code',
                'contenu': 'Canon: Canon court\nCrosse: Crosse de combat\nPoignée: Poignée avant tactique\nChargeur: Chargeur rapide étendu\nOptique: Point rouge',
                'ordre': 12,
            },
            {
                'type_block': 'texte',
                'contenu': 'Cette configuration maximise la mobilité et la cadence de tir, parfaite pour les joueurs agressifs.',
                'ordre': 13,
            },
            {
                'type_block': 'titre',
                'contenu': 'Configuration Défensive',
                'ordre': 14,
            },
            {
                'type_block': 'code',
                'contenu': 'Canon: Canon de précision\nCrosse: Crosse de tireur d\'élite\nPoignée: Poignée avant\nChargeur: Chargeur étendu\nOptique: Lunette x3',
                'ordre': 15,
            },
            {
                'type_block': 'texte',
                'contenu': 'Cette configuration privilégie la précision et la portée, idéale pour le combat à distance.',
                'ordre': 16,
            },
            {
                'type_block': 'titre',
                'contenu': 'Étape 3 : Sélectionner l\'Arme Secondaire',
                'ordre': 17,
            },
            {
                'type_block': 'image',
                'contenu': '',
                'ordre': 18,
                'alignement': 'gauche',
                'note': 'Screenshot arme secondaire (gauche)',
            },
            {
                'type_block': 'texte',
                'contenu': 'L\'arme secondaire doit compléter votre arme principale. '
                          'Si vous utilisez un sniper, choisissez un pistolet ou un SMG pour le combat rapproché.',
                'ordre': 19,
            },
            {
                'type_block': 'liste',
                'contenu': '<ul><li><strong>Pour AR/SMG:</strong> Pistolet ou SMG secondaire</li><li><strong>Pour Sniper:</strong> Pistolet ou SMG</li><li><strong>Pour Shotgun:</strong> AR ou SMG</li><li><strong>Pour LMG:</strong> Pistolet ou SMG</li></ul>',
                'ordre': 20,
            },
            {
                'type_block': 'titre',
                'contenu': 'Étape 4 : Choisir les Perks',
                'ordre': 21,
            },
            {
                'type_block': 'image',
                'contenu': '',
                'ordre': 22,
                'alignement': 'droite',
                'note': 'Screenshot sélection perks (droite)',
            },
            {
                'type_block': 'texte',
                'contenu': 'Les perks peuvent changer complètement votre style de jeu. '
                          'Voici les meilleures combinaisons pour le Ranked :',
                'ordre': 23,
            },
            {
                'type_block': 'titre',
                'contenu': 'Perks Recommandés',
                'ordre': 24,
            },
            {
                'type_block': 'liste',
                'contenu': '<ul><li><strong>Perk 1 (Rouge):</strong> Agile, Lightweight, ou Vulture</li><li><strong>Perk 2 (Vert):</strong> Ghost, Hardline, ou Tracker</li><li><strong>Perk 3 (Bleu):</strong> Dead Silence, Alert, ou High Alert</li></ul>',
                'ordre': 25,
            },
            {
                'type_block': 'titre',
                'contenu': 'Étape 5 : Configurer l\'Équipement',
                'ordre': 26,
            },
            {
                'type_block': 'texte',
                'contenu': 'L\'équipement tactique et létal doivent être choisis en fonction de votre stratégie.',
                'ordre': 27,
            },
            {
                'type_block': 'image',
                'contenu': '',
                'ordre': 28,
                'alignement': 'centre',
                'note': 'Screenshot équipements (centre)',
            },
            {
                'type_block': 'liste',
                'contenu': '<ul><li><strong>Équipement Létal:</strong> Grenade à fragmentation, C4, ou Claymore</li><li><strong>Équipement Tactique:</strong> Grenade flash, Fumigène, ou Stim</li></ul>',
                'ordre': 29,
            },
            {
                'type_block': 'titre',
                'contenu': 'Étape 6 : Tester et Ajuster',
                'ordre': 30,
            },
            {
                'type_block': 'texte',
                'contenu': 'Une fois votre loadout créé, testez-le en conditions réelles et ajustez selon vos besoins.',
                'ordre': 31,
            },
            {
                'type_block': 'liste',
                'contenu': '<ol><li>Testez en mode entraînement pour comprendre le comportement</li><li>Jouez quelques parties en mode public</li><li>Analysez vos performances</li><li>Ajustez les accessoires si nécessaire</li><li>Répétez jusqu\'à trouver la configuration optimale</li></ol>',
                'ordre': 32,
            },
            {
                'type_block': 'titre',
                'contenu': 'Exemples de Loadouts Complets',
                'ordre': 33,
            },
            {
                'type_block': 'image',
                'contenu': '',
                'ordre': 34,
                'alignement': 'pleine_largeur',
                'note': 'Screenshots de loadouts complets (pleine largeur)',
            },
            {
                'type_block': 'titre',
                'contenu': 'Loadout Agressif Complet',
                'ordre': 35,
            },
            {
                'type_block': 'code',
                'contenu': 'Arme principale: AK-47\nAccessoires: Canon court, Crosse de combat, Poignée avant tactique, Chargeur rapide étendu, Point rouge\nArme secondaire: J358\nPerks: Agile, Ghost, Dead Silence\nÉquipement: Grenade à fragmentation, Grenade flash',
                'ordre': 36,
            },
            {
                'type_block': 'titre',
                'contenu': 'Loadout Défensif Complet',
                'ordre': 37,
            },
            {
                'type_block': 'code',
                'contenu': 'Arme principale: M4\nAccessoires: Canon de précision, Crosse de tireur d\'élite, Poignée avant, Chargeur étendu, Lunette x3\nArme secondaire: SMRS\nPerks: Vulture, Tracker, Alert\nÉquipement: Claymore, Fumigène',
                'ordre': 38,
            },
            {
                'type_block': 'titre',
                'contenu': 'Conseils Finaux',
                'ordre': 39,
            },
            {
                'type_block': 'liste',
                'contenu': '<ul><li>Adaptez votre loadout selon la carte et le mode de jeu</li><li>N\'ayez pas peur d\'expérimenter</li><li>Observez les loadouts des meilleurs joueurs</li><li>Pratiquez régulièrement</li><li>Gardez plusieurs loadouts prêts pour différentes situations</li></ul>',
                'ordre': 40,
            },
            {
                'type_block': 'citation',
                'contenu': 'Rappelez-vous : le meilleur loadout est celui qui correspond à votre style de jeu et dans lequel vous êtes à l\'aise.',
                'ordre': 41,
            },
            {
                'type_block': 'titre',
                'contenu': 'Conclusion',
                'ordre': 42,
            },
            {
                'type_block': 'texte',
                'contenu': 'Créer le loadout parfait demande du temps et de la pratique. '
                          'Suivez ces étapes, expérimentez, et vous trouverez la configuration qui vous convient. '
                          'N\'oubliez pas que le meilleur loadout est celui avec lequel vous êtes performant.',
                'ordre': 43,
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
        self.stdout.write(self.style.SUCCESS('🎉 Article TUTORIEL créé!\n'))
        self.stdout.write(f'🔗 URL: http://127.0.0.1:8000/blog/{article.slug}/\n')
        self.stdout.write(f'✏️  Admin: http://127.0.0.1:8000/admin/articles/article/{article.pk}/change/\n')

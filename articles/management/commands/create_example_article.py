"""
Script pour créer un article de blog complet et professionnel
Usage: python manage.py create_example_article
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from articles.models import Article, ArticleImage, ArticleBlock
from utilisateurs.models import Utilisateur


class Command(BaseCommand):
    help = 'Crée un article de blog complet et professionnel avec images et blocs de contenu'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            default=None,
            help='Email de l\'utilisateur qui sera l\'auteur (si non fourni, prend le premier superuser)',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Création d\'un article de blog professionnel...\n'))

        # Récupérer l'auteur
        email = options.get('email')
        if email:
            try:
                auteur = Utilisateur.objects.get(email=email)
            except Utilisateur.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'❌ Utilisateur avec email {email} non trouvé'))
                return
        else:
            # Prendre le premier superuser ou le premier utilisateur
            auteur = Utilisateur.objects.filter(is_superuser=True).first()
            if not auteur:
                auteur = Utilisateur.objects.first()
            if not auteur:
                self.stdout.write(self.style.ERROR('❌ Aucun utilisateur trouvé. Créez d\'abord un utilisateur.'))
                return

        self.stdout.write(f'📝 Auteur: {auteur.nom} {auteur.prenom} ({auteur.email})\n')

        # Créer l'article principal
        titre = "Top 5 Loadouts Sniper pour Call of Duty Mobile"
        slug = slugify(titre)
        
        # S'assurer que le slug est unique
        base_slug = slug
        counter = 1
        while Article.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        article = Article.objects.create(
            titre=titre,
            slug=slug,
            resume="Découvrez les meilleurs loadouts pour devenir un sniper redoutable dans CODM. Guide complet avec armes, accessoires et stratégies.",
            auteur=auteur,
            layout='standard',
            publie=True,
            contenu="",  # On utilise les blocs à la place
        )

        self.stdout.write(self.style.SUCCESS(f'✅ Article créé: "{article.titre}" (ID: {article.pk})\n'))

        # Note: Pour les images, on ne peut pas créer de fichiers réels dans un script
        # L'utilisateur devra les ajouter manuellement via l'admin
        # Mais on crée les références pour les blocs

        self.stdout.write('📸 Note: Les images devront être ajoutées manuellement via l\'admin Django.\n')
        self.stdout.write('   Pour chaque image mentionnée ci-dessous, ajoutez-la dans "Images d\'articles"\n')
        self.stdout.write('   puis modifiez les blocs pour les associer.\n\n')

        # Créer les blocs de contenu dans l'ordre
        blocs_data = [
            {
                'type_block': 'titre',
                'contenu': 'Introduction',
                'ordre': 0,
            },
            {
                'type_block': 'texte',
                'contenu': 'Le sniper est l\'une des classes les plus redoutées dans Call of Duty Mobile. '
                          'Avec la bonne configuration, vous pouvez dominer le champ de bataille depuis une position sécurisée. '
                          'Dans ce guide complet, nous allons explorer les 5 meilleurs loadouts sniper pour différents styles de jeu.',
                'ordre': 1,
            },
            {
                'type_block': 'titre',
                'contenu': 'Loadout #1 : Sniper Rapide et Mobile',
                'ordre': 2,
            },
            {
                'type_block': 'texte',
                'contenu': 'Ce loadout est parfait pour les joueurs qui aiment bouger rapidement tout en gardant une précision mortelle.',
                'ordre': 3,
            },
            {
                'type_block': 'image',
                'contenu': '',
                'ordre': 4,  # Image entre le texte et la liste
                'alignement': 'centre',
                'note': 'Ajouter une image du loadout #1 ici',
            },
            {
                'type_block': 'liste',
                'contenu': '<ul><li><strong>Arme principale:</strong> DL Q33</li><li><strong>Accessoires:</strong> Silencieux, Poignée avant, Chargeur rapide</li><li><strong>Arme secondaire:</strong> J358</li><li><strong>Équipement:</strong> Grenade flash</li><li><strong>Perks:</strong> Agile, Ghost, Dead Silence</li></ul>',
                'ordre': 5,
            },
            {
                'type_block': 'citation',
                'contenu': '"La vitesse tue, mais la précision tue encore plus vite." - Proverbe de sniper',
                'ordre': 6,
            },
            {
                'type_block': 'titre',
                'contenu': 'Loadout #2 : Sniper de Camping',
                'ordre': 7,
            },
            {
                'type_block': 'texte',
                'contenu': 'Pour ceux qui préfèrent une approche plus défensive, ce loadout maximise la portée et la stabilité.',
                'ordre': 8,
            },
            {
                'type_block': 'image',
                'contenu': '',
                'ordre': 9,  # Image entre le texte et la liste
                'alignement': 'droite',
                'note': 'Ajouter une image du loadout #2 ici',
            },
            {
                'type_block': 'liste',
                'contenu': '<ul><li><strong>Arme principale:</strong> Arctic .50</li><li><strong>Accessoires:</strong> Lunette x6, Bipied, Chargeur étendu</li><li><strong>Arme secondaire:</strong> SMRS</li><li><strong>Équipement:</strong> Piège à mine</li><li><strong>Perks:</strong> Vulture, Tracker, Alert</li></ul>',
                'ordre': 10,
            },
            {
                'type_block': 'titre',
                'contenu': 'Loadout #3 : Sniper Agressif',
                'ordre': 11,
            },
            {
                'type_block': 'texte',
                'contenu': 'Un loadout pour les snipers qui n\'ont pas peur de se rapprocher de l\'action et de prendre des risques.',
                'ordre': 12,
            },
            {
                'type_block': 'image',
                'contenu': '',
                'ordre': 13,  # Image entre le texte et la liste
                'alignement': 'gauche',
                'note': 'Ajouter une image du loadout #3 ici',
            },
            {
                'type_block': 'liste',
                'contenu': '<ol><li><strong>Arme principale:</strong> Locus</li><li><strong>Accessoires:</strong> Canon court, Poignée avant, Laser tactique</li><li><strong>Arme secondaire:</strong> FHJ-18</li><li><strong>Équipement:</strong> Grenade à fragmentation</li><li><strong>Perks:</strong> Lightweight, Hardline, High Alert</li></ol>',
                'ordre': 14,
            },
            {
                'type_block': 'titre',
                'contenu': 'Conseils de Stratégie',
                'ordre': 15,
            },
            {
                'type_block': 'texte',
                'contenu': 'Voici quelques conseils essentiels pour maîtriser l\'art du sniper dans CODM:',
                'ordre': 16,
            },
            {
                'type_block': 'liste',
                'contenu': '<ul><li>Toujours changer de position après quelques kills pour éviter d\'être repéré</li><li>Utilisez le scope uniquement quand nécessaire pour garder une vision périphérique</li><li>Apprenez les points de spawn et les routes communes des ennemis</li><li>Communiquez avec votre équipe pour coordonner les attaques</li><li>Pratiquez le quick-scope en mode entraînement</li></ul>',
                'ordre': 17,
            },
            {
                'type_block': 'titre',
                'contenu': 'Exemple de Code de Configuration',
                'ordre': 18,
            },
            {
                'type_block': 'code',
                'contenu': '// Configuration recommandée pour DL Q33\nSensibilité Scope: 45\nSensibilité ADS: 50\nFOV: 90\nMode de tir: Tactique',
                'ordre': 19,
            },
            {
                'type_block': 'titre',
                'contenu': 'Vidéo Tutoriel',
                'ordre': 20,
            },
            {
                'type_block': 'texte',
                'contenu': 'Regardez cette vidéo pour voir ces loadouts en action:',
                'ordre': 21,
            },
            {
                'type_block': 'video',
                'contenu': 'https://www.youtube.com/embed/dQw4w9WgXcQ',  # URL d'exemple, à remplacer
                'ordre': 22,
            },
            {
                'type_block': 'titre',
                'contenu': 'Conclusion',
                'ordre': 23,
            },
            {
                'type_block': 'texte',
                'contenu': 'Chaque loadout a ses avantages et convient à différents styles de jeu. '
                          'N\'hésitez pas à expérimenter et à adapter ces configurations à votre façon de jouer. '
                          'La clé du succès réside dans la pratique constante et l\'adaptation à chaque situation de combat.',
                'ordre': 24,
            },
            {
                'type_block': 'citation',
                'contenu': 'Rappelez-vous: un bon sniper ne tire pas seulement, il observe, analyse et choisit le bon moment.',
                'ordre': 25,
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

        self.stdout.write(self.style.SUCCESS(f'\n✅ {len(blocs_data)} blocs de contenu créés avec succès!\n'))

        # Instructions pour les images
        self.stdout.write(self.style.WARNING('📸 INSTRUCTIONS POUR LES IMAGES:\n'))
        self.stdout.write('1. Allez dans l\'admin Django: /admin/articles/article/\n')
        self.stdout.write(f'2. Cliquez sur l\'article "{article.titre}"\n')
        self.stdout.write('3. Dans la section "Images d\'articles", ajoutez au moins 3 images:\n')
        self.stdout.write('   - Image 1: Screenshot du loadout #1 (Ordre: 0)\n')
        self.stdout.write('   - Image 2: Screenshot du loadout #2 (Ordre: 1)\n')
        self.stdout.write('   - Image 3: Screenshot du loadout #3 (Ordre: 2)\n')
        self.stdout.write('4. Ensuite, modifiez les blocs de type "Image" (ordre 4, 9, 13) pour associer les images:\n')
        self.stdout.write('   - Trouvez les blocs de type "Image" dans "Blocs de contenu"\n')
        self.stdout.write('   - Sélectionnez l\'image correspondante dans le champ "Image"\n')
        self.stdout.write('   - L\'alignement est déjà configuré (Centre, Droite, Gauche)\n')
        self.stdout.write('5. N\'oubliez pas de mettre à jour l\'URL de la vidéo dans le bloc vidéo\n\n')

        self.stdout.write(self.style.SUCCESS('🎉 Article créé avec succès!\n'))
        self.stdout.write(f'🔗 URL de l\'article: http://127.0.0.1:8000/blog/{article.slug}/\n')
        self.stdout.write(f'✏️  Modifier dans l\'admin: http://127.0.0.1:8000/admin/articles/article/{article.pk}/change/\n')

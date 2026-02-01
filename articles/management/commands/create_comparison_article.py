"""
Script pour créer un article de type COMPARAISON avec images alternées
Usage: python manage.py create_comparison_article
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from articles.models import Article, ArticleBlock
from utilisateurs.models import Utilisateur


class Command(BaseCommand):
    help = 'Crée un article de type COMPARAISON avec images alternées'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            default=None,
            help='Email de l\'utilisateur qui sera l\'auteur',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Création d\'un article COMPARAISON...\n'))

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
        titre = "Comparaison : DL Q33 vs Arctic .50 - Quel Sniper Choisir ?"
        slug = slugify(titre)
        base_slug = slug
        counter = 1
        while Article.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        article = Article.objects.create(
            titre=titre,
            slug=slug,
            resume="Comparaison détaillée entre les deux snipers les plus populaires de CODM. Découvrez lequel choisir selon votre style de jeu.",
            auteur=auteur,
            layout='standard',
            publie=True,
            contenu="",
        )

        self.stdout.write(self.style.SUCCESS(f'✅ Article créé: "{article.titre}" (ID: {article.pk})\n'))

        # Blocs de comparaison avec images alternées
        blocs_data = [
            {
                'type_block': 'titre',
                'contenu': 'Introduction',
                'ordre': 0,
            },
            {
                'type_block': 'texte',
                'contenu': 'Le choix entre le DL Q33 et l\'Arctic .50 est l\'un des dilemmes les plus fréquents '
                          'chez les joueurs de CODM. Ces deux snipers sont excellents, mais chacun a ses spécificités. '
                          'Dans cette comparaison approfondie, nous allons analyser leurs forces, faiblesses et cas d\'usage.',
                'ordre': 1,
            },
            {
                'type_block': 'image',
                'contenu': '',
                'ordre': 2,
                'alignement': 'pleine_largeur',
                'note': 'Image de comparaison côte à côte (pleine largeur)',
            },
            {
                'type_block': 'titre',
                'contenu': 'DL Q33 : Le Rapide et Précis',
                'ordre': 3,
            },
            {
                'type_block': 'image',
                'contenu': '',
                'ordre': 4,
                'alignement': 'gauche',
                'note': 'Screenshot DL Q33 (gauche)',
            },
            {
                'type_block': 'texte',
                'contenu': 'Le DL Q33 est réputé pour sa vitesse de manipulation et sa précision. '
                          'C\'est l\'arme de choix pour les joueurs agressifs qui aiment bouger rapidement '
                          'et prendre des risques. Sa cadence de tir est supérieure à celle de l\'Arctic .50, '
                          'ce qui permet de tirer plusieurs coups rapidement.',
                'ordre': 5,
            },
            {
                'type_block': 'titre',
                'contenu': 'Avantages du DL Q33',
                'ordre': 6,
            },
            {
                'type_block': 'liste',
                'contenu': '<ul><li>✅ Cadence de tir plus rapide</li><li>✅ Temps de rechargement plus court</li><li>✅ Mobilité supérieure</li><li>✅ Idéal pour le quick-scope</li><li>✅ Meilleur pour le combat rapproché</li></ul>',
                'ordre': 7,
            },
            {
                'type_block': 'titre',
                'contenu': 'Inconvénients du DL Q33',
                'ordre': 8,
            },
            {
                'type_block': 'liste',
                'contenu': '<ul><li>❌ Dégâts légèrement inférieurs</li><li>❌ Portée effective plus courte</li><li>❌ Recul plus difficile à contrôler</li><li>❌ Moins efficace à très longue distance</li></ul>',
                'ordre': 9,
            },
            {
                'type_block': 'titre',
                'contenu': 'Arctic .50 : Le Puissant et Stable',
                'ordre': 10,
            },
            {
                'type_block': 'image',
                'contenu': '',
                'ordre': 11,
                'alignement': 'droite',
                'note': 'Screenshot Arctic .50 (droite)',
            },
            {
                'type_block': 'texte',
                'contenu': 'L\'Arctic .50 est le sniper de référence pour ceux qui privilégient la puissance brute '
                          'et la stabilité. Avec des dégâts dévastateurs et un recul bien contrôlé, il excelle dans '
                          'les combats à longue distance. C\'est l\'arme parfaite pour les snipers défensifs qui '
                          'préfèrent prendre leur temps.',
                'ordre': 12,
            },
            {
                'type_block': 'titre',
                'contenu': 'Avantages de l\'Arctic .50',
                'ordre': 13,
            },
            {
                'type_block': 'liste',
                'contenu': '<ul><li>✅ Dégâts supérieurs (one-shot kill garanti)</li><li>✅ Portée exceptionnelle</li><li>✅ Recul très contrôlable</li><li>✅ Idéal pour le camping</li><li>✅ Meilleur pour le combat à longue distance</li></ul>',
                'ordre': 14,
            },
            {
                'type_block': 'titre',
                'contenu': 'Inconvénients de l\'Arctic .50',
                'ordre': 15,
            },
            {
                'type_block': 'liste',
                'contenu': '<ul><li>❌ Cadence de tir plus lente</li><li>❌ Temps de rechargement plus long</li><li>❌ Mobilité réduite</li><li>❌ Moins adapté au combat rapproché</li><li>❌ Nécessite plus de précision</li></ul>',
                'ordre': 16,
            },
            {
                'type_block': 'titre',
                'contenu': 'Comparaison Directe',
                'ordre': 17,
            },
            {
                'type_block': 'image',
                'contenu': '',
                'ordre': 18,
                'alignement': 'centre',
                'note': 'Tableau de comparaison (centre)',
            },
            {
                'type_block': 'titre',
                'contenu': 'Tableau Comparatif',
                'ordre': 19,
            },
            {
                'type_block': 'liste',
                'contenu': '<ul><li><strong>Dégâts:</strong> Arctic .50 (10/10) vs DL Q33 (9/10)</li><li><strong>Portée:</strong> Arctic .50 (10/10) vs DL Q33 (8/10)</li><li><strong>Cadence:</strong> DL Q33 (9/10) vs Arctic .50 (6/10)</li><li><strong>Contrôle:</strong> Arctic .50 (9/10) vs DL Q33 (7/10)</li><li><strong>Mobilité:</strong> DL Q33 (9/10) vs Arctic .50 (6/10)</li></ul>',
                'ordre': 20,
            },
            {
                'type_block': 'titre',
                'contenu': 'Quand Choisir le DL Q33 ?',
                'ordre': 21,
            },
            {
                'type_block': 'texte',
                'contenu': 'Le DL Q33 est parfait si vous :',
                'ordre': 22,
            },
            {
                'type_block': 'liste',
                'contenu': '<ul><li>Préférez un style de jeu agressif et mobile</li><li>Aimez le quick-scope et les combats rapprochés</li><li>Jouez sur des cartes avec beaucoup de couverture</li><li>Voulez une arme polyvalente</li><li>Êtes à l\'aise avec le contrôle du recul</li></ul>',
                'ordre': 23,
            },
            {
                'type_block': 'titre',
                'contenu': 'Quand Choisir l\'Arctic .50 ?',
                'ordre': 24,
            },
            {
                'type_block': 'texte',
                'contenu': 'L\'Arctic .50 est idéal si vous :',
                'ordre': 25,
            },
            {
                'type_block': 'liste',
                'contenu': '<ul><li>Préférez un style de jeu défensif et patient</li><li>Excellente dans les combats à longue distance</li><li>Jouez sur des cartes ouvertes</li><li>Voulez maximiser les one-shot kills</li><li>Cherchez la stabilité et la précision</li></ul>',
                'ordre': 26,
            },
            {
                'type_block': 'titre',
                'contenu': 'Verdict Final',
                'ordre': 27,
            },
            {
                'type_block': 'texte',
                'contenu': 'Les deux snipers sont excellents, mais pour des raisons différentes. '
                          'Le DL Q33 excelle dans la mobilité et la polyvalence, tandis que l\'Arctic .50 '
                          'domine en puissance et en précision. Le choix dépend entièrement de votre style de jeu.',
                'ordre': 28,
            },
            {
                'type_block': 'citation',
                'contenu': 'Conseil d\'expert : Maîtrisez les deux armes et adaptez votre choix selon la carte et le mode de jeu.',
                'ordre': 29,
            },
            {
                'type_block': 'video',
                'contenu': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
                'ordre': 30,
                'note': 'Vidéo de comparaison (URL à remplacer)',
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
        self.stdout.write(self.style.SUCCESS('🎉 Article COMPARAISON créé!\n'))
        self.stdout.write(f'🔗 URL: http://127.0.0.1:8000/blog/{article.slug}/\n')
        self.stdout.write(f'✏️  Admin: http://127.0.0.1:8000/admin/articles/article/{article.pk}/change/\n')

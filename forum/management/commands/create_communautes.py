from django.core.management.base import BaseCommand
from forum.models import Communaute
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Crée les communautés par défaut du forum'

    def handle(self, *args, **options):
        communautes_data = [
            {
                'nom': 'Sniper CODM',
                'description': 'Communauté dédiée aux snipers dans Call of Duty Mobile. Partagez vos meilleurs moments, vos builds et vos astuces.',
                'icone': 'fas fa-crosshairs',
                'couleur': '#FF1A1A',
            },
            {
                'nom': 'AR / SMG',
                'description': 'Tout sur les fusils d\'assaut et les mitraillettes. Builds, sensibilités, et stratégies pour dominer avec ces armes.',
                'icone': 'fas fa-gun',
                'couleur': '#FF6600',
            },
            {
                'nom': 'Tournois & compétitions',
                'description': 'Discussions sur les tournois, les compétitions et l\'esport CODM. Résultats, analyses et stratégies compétitives.',
                'icone': 'fas fa-trophy',
                'couleur': '#FFD700',
            },
            {
                'nom': 'Loadouts & sensibilité',
                'description': 'Partagez vos loadouts, configurations de sensibilité et optimisez votre gameplay pour être au top.',
                'icone': 'fas fa-cog',
                'couleur': '#00CCFF',
            },
            {
                'nom': 'Mobile & performances',
                'description': 'Optimisation des performances sur mobile, paramètres graphiques, FPS, et astuces pour améliorer votre expérience.',
                'icone': 'fas fa-mobile-alt',
                'couleur': '#00FF00',
            },
            {
                'nom': 'Général CODM',
                'description': 'Discussions générales sur Call of Duty Mobile. Actualités, débats, questions et tout ce qui concerne CODM.',
                'icone': 'fas fa-comments',
                'couleur': '#CC00FF',
            },
        ]

        created_count = 0
        for data in communautes_data:
            slug = slugify(data['nom'])
            communaute, created = Communaute.objects.get_or_create(
                slug=slug,
                defaults={
                    'nom': data['nom'],
                    'description': data['description'],
                    'icone': data['icone'],
                    'couleur': data['couleur'],
                    'est_active': True,
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Communauté créée: {communaute.nom}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'→ Communauté déjà existante: {communaute.nom}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n{created_count} communauté(s) créée(s) avec succès!')
        )

import os
import django
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CODMTracker.settings")
django.setup()

# Exemple : créer des articles par défaut
try:
    call_command('create_communautes')
    call_command('create_example_article')
    call_command('create_guide_article')  
    call_command('create_comparison_article')  
    call_command('create_tutorial_article')  
    print("✅ Commandes custom exécutées")
except Exception as e:
    print("Erreur lors de l'exécution des commandes custom :", e)

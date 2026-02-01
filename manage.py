#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CODMTracker.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Création automatique du superuser si variable CREATE_SUPERUSER=1
    if os.environ.get("CREATE_SUPERUSER") == "1":
        try:
            import create_superuser
        except Exception as e:
            print("Erreur lors de la création du superuser :", e)

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

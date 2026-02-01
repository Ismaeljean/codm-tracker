#!/usr/bin/env bash
set -o errexit

echo "📦 Installation des dépendances"
pip install -r requirements.txt

echo "🗃 Collectstatic"
python manage.py collectstatic --noinput

echo "🛠 Migrations"
python manage.py migrate

echo "👤 Création superuser"
python manage.py shell -c "import create_superuser"

echo "📝 Commandes custom"
python manage.py shell -c "import run_commands"

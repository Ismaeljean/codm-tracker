# 📝 Scripts de Création d'Articles de Blog

Ce dossier contient plusieurs scripts pour créer automatiquement des articles de blog avec différentes structures et layouts.

## 🚀 Scripts Disponibles

### 1. `create_example_article.py` - Article Exemple Complet
**Type** : Article général avec tous les types de blocs

**Structure** :
- Images : Centre, Droite, Gauche
- Contenu varié : Titres, textes, listes, citations, code, vidéo
- **26 blocs** au total

**Usage** :
```bash
python manage.py create_example_article
python manage.py create_example_article --email votre@email.com
```

**Idéal pour** : Démonstration complète de toutes les fonctionnalités

---

### 2. `create_guide_article.py` - Guide avec Images Alternées
**Type** : Guide détaillé avec images alternées gauche/droite

**Structure** :
- Images alternées : Gauche → Droite → Gauche
- Comparaisons d'armes avec images côte à côte
- **29 blocs** au total

**Caractéristiques** :
- Images à gauche avec texte à droite
- Images à droite avec texte à gauche
- Images pleine largeur pour les sections importantes
- Images centrées pour les comparaisons

**Usage** :
```bash
python manage.py create_guide_article
python manage.py create_guide_article --email votre@email.com
```

**Idéal pour** : Guides d'armes, guides de gameplay, articles comparatifs

---

### 3. `create_comparison_article.py` - Article de Comparaison
**Type** : Comparaison détaillée avec images alternées

**Structure** :
- Comparaison côte à côte avec images alternées
- Avantages/Inconvénients pour chaque option
- Tableaux comparatifs
- **31 blocs** au total

**Caractéristiques** :
- Images alternées pour chaque option comparée
- Listes avec ✅ et ❌ pour avantages/inconvénients
- Tableau de comparaison visuel
- Section "Verdict Final"

**Usage** :
```bash
python manage.py create_comparison_article
python manage.py create_comparison_article --email votre@email.com
```

**Idéal pour** : Comparaisons d'armes, équipements, stratégies

---

### 4. `create_tutorial_article.py` - Tutoriel Étape par Étape
**Type** : Tutoriel détaillé avec images pour chaque étape

**Structure** :
- Étapes numérotées avec images
- Images alternées pour chaque étape
- Exemples de code/configuration
- **44 blocs** au total

**Caractéristiques** :
- Images pour chaque étape importante
- Alternance gauche/droite pour varier la présentation
- Listes numérotées pour les étapes
- Exemples concrets de configurations

**Usage** :
```bash
python manage.py create_tutorial_article
python manage.py create_tutorial_article --email votre@email.com
```

**Idéal pour** : Tutoriels, guides étape par étape, walkthroughs

---

## 📋 Utilisation Générale

### Commande de Base
Tous les scripts suivent le même format :
```bash
python manage.py [nom_du_script]
```

### Spécifier un Auteur
Pour créer un article avec un auteur spécifique :
```bash
python manage.py [nom_du_script] --email votre@email.com
```

Si aucun email n'est fourni, le script utilisera :
1. Le premier superuser trouvé
2. Sinon, le premier utilisateur trouvé

### Après la Création

1. **Ajouter les Images** :
   - Allez dans l'admin Django : `/admin/articles/article/`
   - Cliquez sur l'article créé
   - Dans "Images d'articles", ajoutez les images nécessaires
   - Associez-les aux blocs de type "Image"

2. **Personnaliser le Contenu** :
   - Modifiez les textes selon vos besoins
   - Ajustez les ordres si nécessaire
   - Ajoutez ou supprimez des blocs

3. **Mettre à Jour la Vidéo** :
   - Trouvez le bloc de type "Vidéo"
   - Remplacez l'URL d'exemple par une vraie URL YouTube/Vimeo

---

## 🎨 Modèles de Layout Disponibles

### Images Alternées (Gauche/Droite)
Les scripts utilisent différents alignements pour créer un effet visuel dynamique :

- **Gauche** : Image à gauche, texte à droite
- **Droite** : Image à droite, texte à gauche
- **Centre** : Image centrée avec texte autour
- **Pleine largeur** : Image sur toute la largeur

### Exemples de Structures

#### Structure Guide (create_guide_article.py)
```
Titre → Texte → Image (pleine largeur)
Titre → Image (gauche) → Texte → Liste
Titre → Image (droite) → Texte → Liste
Titre → Image (gauche) → Texte → Liste
```

#### Structure Comparaison (create_comparison_article.py)
```
Introduction → Image (pleine largeur)
Option A → Image (gauche) → Texte → Avantages → Inconvénients
Option B → Image (droite) → Texte → Avantages → Inconvénients
Comparaison → Tableau → Verdict
```

#### Structure Tutoriel (create_tutorial_article.py)
```
Introduction → Image (pleine largeur)
Étape 1 → Texte → Image (gauche) → Liste
Étape 2 → Texte → Image (droite) → Code
Étape 3 → Texte → Image (gauche) → Liste
...
Conclusion
```

---

## 💡 Conseils d'Utilisation

### Pour Créer Plusieurs Articles
Exécutez les scripts dans l'ordre pour avoir une variété d'articles :
```bash
python manage.py create_example_article
python manage.py create_guide_article
python manage.py create_comparison_article
python manage.py create_tutorial_article
```

### Personnalisation
Après création, vous pouvez :
- Modifier les titres et contenus
- Réorganiser les blocs (changer les ordres)
- Ajouter ou supprimer des blocs
- Changer les alignements des images

### Réutilisation
Vous pouvez utiliser ces scripts comme base et les modifier pour créer vos propres structures d'articles.

---

## 📸 Images Requises

Chaque script nécessite différentes images. Voici un récapitulatif :

### create_example_article.py
- 3 images minimum (loadouts)

### create_guide_article.py
- 4 images minimum :
  - Image principale AR (pleine largeur)
  - Screenshot AK-47 (gauche)
  - Screenshot M4 (droite)
  - Screenshot ICR-1 (gauche)
  - Image comparaison (centre)

### create_comparison_article.py
- 4 images minimum :
  - Image comparaison côte à côte (pleine largeur)
  - Screenshot DL Q33 (gauche)
  - Screenshot Arctic .50 (droite)
  - Tableau comparaison (centre)

### create_tutorial_article.py
- 6 images minimum :
  - Image introduction (pleine largeur)
  - Screenshot sélection arme (gauche)
  - Screenshot accessoires (droite)
  - Screenshot arme secondaire (gauche)
  - Screenshot perks (droite)
  - Screenshot équipements (centre)
  - Screenshots loadouts complets (pleine largeur)

---

## 🔧 Dépannage

**Erreur** : "Aucun utilisateur trouvé"
- **Solution** : Créez d'abord un utilisateur ou utilisez `--email` avec un utilisateur existant

**Erreur** : "Article with this slug already exists"
- **Solution** : Le script gère automatiquement les slugs en doublon en ajoutant un numéro

**Les images ne s'affichent pas**
- **Solution** : Assurez-vous d'avoir ajouté les images dans "Images d'articles" et de les avoir associées aux blocs

---

**Bon blogging ! 🚀**

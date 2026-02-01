# 📝 Guide de Création d'un Blog Professionnel - CODM Tracker

## Vue d'ensemble

Le système de blog permet de créer des articles sophistiqués avec des images multiples, des blocs de contenu structurés, et un contrôle total sur la mise en page. Ce guide vous accompagne étape par étape pour créer des articles de qualité professionnelle.

## 🚀 Méthode Rapide : Script Automatique

Pour créer rapidement un article complet avec tous les blocs de contenu, utilisez la commande Django :

```bash
python manage.py create_example_article
```

Cette commande crée automatiquement :
- Un article avec titre, résumé et structure complète
- 26 blocs de contenu (titres, textes, listes, citations, code, vidéo)
- 3 emplacements pour images avec alignements différents
- Un exemple complet de blog professionnel

**Ensuite**, il vous suffit d'ajouter les images dans l'admin Django et de personnaliser le contenu.

## 🎯 Processus de Création (Étape par Étape)

### Étape 1 : Créer l'Article de Base

1. Allez dans **Admin Django** → **Articles** → **Articles** → **Ajouter un article**
2. Remplissez les champs obligatoires :
   - **Titre** : Le titre de votre article (ex: "Meilleurs Loadouts pour Sniper")
   - **Auteur** : Sélectionnez votre utilisateur
   - **Layout** : Choisissez le style d'affichage
     - `Standard` : Image en haut, texte en dessous
     - `Alternatif` : Image/Texte alternés
     - `Pleine largeur` : Contenu sans sidebar
   - **Résumé** : Texte court (max 300 caractères) affiché dans la liste des blogs
   - **Image principale** : Image affichée sur la page de liste des blogs
   - **Contenu** : (Optionnel) Texte simple. Pour un blog sophistiqué, utilisez plutôt les blocs ci-dessous.

3. **⚠️ IMPORTANT** : Cliquez sur **"Enregistrer"** ou **"Enregistrer et continuer l'édition"** avant de continuer !

### Étape 2 : Ajouter des Images Supplémentaires

Une fois l'article enregistré, vous verrez deux sections en bas de la page :

#### Section "Images d'articles"

1. Cliquez sur **"Ajouter une autre Image d'article"**
2. Pour chaque image :
   - **Image** : Uploadez votre image
   - **Légende** : (Optionnel) Texte affiché sous l'image
   - **Ordre** : Numéro d'ordre (0 = première image, 1 = deuxième, etc.)

3. Répétez pour toutes les images que vous voulez utiliser dans votre article

**💡 Astuce** : Vous pouvez ajouter autant d'images que vous voulez (5, 10, 20+). Elles seront disponibles pour les blocs de contenu.

### Étape 3 : Créer les Blocs de Contenu

C'est ici que la magie opère ! Les blocs permettent de structurer votre article de manière professionnelle.

#### Section "Blocs de contenu"

Cliquez sur **"Ajouter un autre Bloc de contenu"** et choisissez le type :

#### 📝 Types de Blocs Disponibles :

1. **Paragraphe de Texte**
   - **Type block** : Sélectionnez "Paragraphe de Texte"
   - **Contenu** : Écrivez votre texte (supporte les retours à la ligne)
   - **Ordre** : Position dans l'article (0 = premier bloc)

2. **Titre de Section**
   - **Type block** : Sélectionnez "Titre de Section"
   - **Contenu** : Votre titre (ex: "Les Meilleurs Armes")
   - **Ordre** : Position du titre

3. **Image (avec alignement)**
   - **Type block** : Sélectionnez "Image"
   - **Image** : Choisissez une image que vous avez ajoutée à l'Étape 2
   - **Alignement** : 
     - `Gauche` : Image à gauche, texte à droite
     - `Droite` : Image à droite, texte à gauche
     - `Centre` : Image centrée
     - `Pleine largeur` : Image sur toute la largeur
   - **Ordre** : Position dans l'article

4. **Liste (HTML)**
   - **Type block** : Sélectionnez "Liste"
   - **Contenu** : Utilisez du HTML. **⚠️ IMPORTANT** : Le HTML sera rendu tel quel, utilisez `|safe` dans le template.
     ```html
     <ul>
       <li>Premier élément</li>
       <li>Deuxième élément</li>
       <li>Troisième élément</li>
     </ul>
     ```
     Ou pour une liste numérotée :
     ```html
     <ol>
       <li>Premier point</li>
       <li>Deuxième point</li>
     </ol>
     ```
   - **💡 Astuce** : Vous pouvez utiliser `<strong>`, `<em>`, `<a href="">` dans les éléments de liste pour enrichir le contenu.

5. **Citation**
   - **Type block** : Sélectionnez "Citation"
   - **Contenu** : Votre citation (ex: "Le meilleur sniper est celui qui attend le bon moment")
   - **Ordre** : Position

6. **Bloc de Code**
   - **Type block** : Sélectionnez "Bloc de Code"
   - **Contenu** : Votre code (sera affiché dans un bloc formaté)
   - **Ordre** : Position

7. **Vidéo (YouTube/Vimeo)**
   - **Type block** : Sélectionnez "Vidéo"
   - **Contenu** : URL d'intégration de la vidéo
     - Pour YouTube : `https://www.youtube.com/embed/VIDEO_ID`
     - Pour Vimeo : `https://player.vimeo.com/video/VIDEO_ID`
   - **Ordre** : Position

### Étape 4 : Organiser l'Ordre

L'ordre des blocs détermine leur affichage dans l'article :
- **0** = Premier élément
- **1** = Deuxième élément
- **2** = Troisième élément
- etc.

**💡 Exemple d'ordre pour un article :**
```
Ordre 0 : Titre de Section "Introduction"
Ordre 1 : Paragraphe de Texte (texte d'introduction)
Ordre 2 : Image (alignement: Pleine largeur)
Ordre 3 : Titre de Section "Les Meilleurs Loadouts"
Ordre 4 : Liste (HTML avec les loadouts)
Ordre 5 : Image (alignement: Droite)
Ordre 6 : Paragraphe de Texte (explication)
Ordre 7 : Citation
Ordre 8 : Vidéo
```

### Étape 5 : Publier

1. Vérifiez que **"Publié"** est coché
2. Cliquez sur **"Enregistrer"**
2. Votre article apparaîtra sur la page `/blog/`

## 📋 Exemple Complet de Création

### Scénario : Article "Top 5 Sniper Loadouts"

1. **Créer l'article** :
   - Titre : "Top 5 Sniper Loadouts pour CODM"
   - Résumé : "Découvrez les meilleurs loadouts pour devenir un sniper redoutable"
   - Image principale : Image d'un sniper
   - Enregistrer

2. **Ajouter 3 images** :
   - Image 1 : Screenshot loadout 1 (Ordre: 0)
   - Image 2 : Screenshot loadout 2 (Ordre: 1)
   - Image 3 : Screenshot loadout 3 (Ordre: 2)

3. **Créer les blocs** :
   - **Bloc 0** : Titre de Section "Introduction"
   - **Bloc 1** : Paragraphe de Texte "Dans ce guide..."
   - **Bloc 2** : Image (Image 1, Alignement: Centre)
   - **Bloc 3** : Titre de Section "Loadout #1 : Sniper Rapide"
   - **Bloc 4** : Liste HTML avec les armes et accessoires
   - **Bloc 5** : Paragraphe de Texte "Ce loadout est parfait pour..."
   - **Bloc 6** : Image (Image 2, Alignement: Droite)
   - **Bloc 7** : Citation "La vitesse tue"
   - **Bloc 8** : Vidéo YouTube
   - **Bloc 9** : Titre de Section "Conclusion"
   - **Bloc 10** : Paragraphe de Texte final

4. **Publier** et c'est prêt ! 


## ⚠️ Points Importants

- **Toujours enregistrer l'article avant d'ajouter des images/blocs** : C'est essentiel car les relations entre les modèles nécessitent que l'article existe en base de données.
- **L'ordre des blocs est crucial** : utilisez des numéros séquentiels (0, 1, 2, 3...). Les blocs sont affichés dans l'ordre croissant.
- **Pour les images dans les blocs** : vous devez d'abord les ajouter dans "Images d'articles", puis les sélectionner dans les blocs de type "Image".
- **Le contenu principal** est optionnel si vous utilisez des blocs. Si vous utilisez des blocs, vous pouvez laisser le champ "Contenu" vide.
- **Le résumé** est obligatoire pour l'affichage dans la liste des blogs. Il doit faire maximum 300 caractères.
- **Le slug** est généré automatiquement à partir du titre, mais vous pouvez le modifier manuellement si nécessaire.
- **Les listes HTML** : Utilisez `<ul>` pour les listes à puces et `<ol>` pour les listes numérotées. Le HTML sera rendu correctement grâce au filtre `|safe`.

## 🎨 Conseils de Design et Bonnes Pratiques

### Images
- **Qualité** : Utilisez des images de bonne qualité (minimum 800px de largeur, format JPG ou PNG)
- **Taille** : Optimisez vos images avant l'upload (max 2MB recommandé) pour un chargement rapide
- **Alignement** : Variez les alignements (gauche, droite, centre, pleine largeur) pour créer un effet visuel dynamique
- **Légendes** : Ajoutez des légendes descriptives à vos images pour améliorer l'accessibilité et le SEO

### Structure du Contenu
- **Titres de section** : Utilisez régulièrement des titres de section pour structurer votre article et faciliter la lecture
- **Variété** : Variez les types de blocs (texte, image, liste, citation) pour maintenir l'attention du lecteur
- **Espacement** : Laissez de l'espace entre les sections (utilisez des ordres espacés si nécessaire)
- **Citations** : Utilisez des citations pour mettre en valeur des points importants ou des témoignages

### Listes
- **Listes à puces** (`<ul>`) : Pour les éléments sans ordre particulier (ex: liste d'armes, accessoires)
- **Listes numérotées** (`<ol>`) : Pour les étapes, classements, ou éléments ordonnés (ex: Top 5, étapes d'un processus)
- **Formatage** : Utilisez `<strong>` pour mettre en gras les mots-clés dans vos listes

### Vidéos
- **URL d'intégration** : Utilisez toujours l'URL d'intégration (embed), pas l'URL normale
  - YouTube : `https://www.youtube.com/embed/VIDEO_ID`
  - Vimeo : `https://player.vimeo.com/video/VIDEO_ID`
- **Position** : Placez les vidéos après une introduction ou une explication pour un meilleur contexte

### SEO et Accessibilité
- **Résumé accrocheur** : Rédigez un résumé qui donne envie de lire l'article
- **Titres descriptifs** : Utilisez des titres clairs et descriptifs pour chaque section
- **Alt text** : Les légendes d'images servent aussi d'alternative textuelle

## 🔧 Dépannage

### Problèmes Courants

**Problème** : Je ne peux pas sélectionner d'image dans un bloc
- **Cause** : L'article n'a pas été enregistré ou aucune image n'a été ajoutée
- **Solution** : 
  1. Assurez-vous d'avoir cliqué sur "Enregistrer" après avoir créé l'article
  2. Ajoutez des images dans la section "Images d'articles"
  3. Rechargez la page de modification de l'article
  4. Les images devraient maintenant apparaître dans le menu déroulant des blocs

**Problème** : Les blocs ne s'affichent pas dans le bon ordre
- **Cause** : Les numéros d'ordre ne sont pas séquentiels ou contiennent des doublons
- **Solution** : 
  1. Vérifiez que les numéros d'ordre sont séquentiels (0, 1, 2, 3...)
  2. Évitez les sauts (ex: 0, 1, 5, 6) - utilisez des numéros consécutifs
  3. Les blocs sont triés par ordre croissant automatiquement

**Problème** : La vidéo ne s'affiche pas
- **Cause** : URL incorrecte ou non valide
- **Solution** : 
  1. Utilisez l'URL d'intégration (embed), pas l'URL normale de la vidéo
  2. Pour YouTube : Récupérez l'ID de la vidéo et utilisez `https://www.youtube.com/embed/VIDEO_ID`
  3. Vérifiez que l'URL commence bien par `https://`

**Problème** : Le HTML des listes s'affiche en texte brut
- **Cause** : Le filtre `|safe` n'est pas appliqué dans le template
- **Solution** : C'est normal, le système utilise déjà `|safe` automatiquement. Si le problème persiste, vérifiez que vous utilisez bien le type de bloc "Liste"

**Problème** : L'image principale ne s'affiche pas dans la liste des blogs
- **Cause** : Aucune image principale n'a été uploadée
- **Solution** : 
  1. Allez dans l'admin Django
  2. Modifiez l'article
  3. Uploadez une image dans le champ "Image principale"
  4. Enregistrez

**Problème** : Le slug généré automatiquement contient des caractères étranges
- **Cause** : Le titre contient des caractères spéciaux non supportés
- **Solution** : 
  1. Modifiez manuellement le slug dans l'admin
  2. Utilisez uniquement des lettres minuscules, chiffres et tirets
  3. Exemple : "Top 5 Loadouts!" devient "top-5-loadouts"

## 📚 Exemples de Structures d'Articles

### Structure Type : Guide/Tutoriel
```
0. Titre : Introduction
1. Texte : Présentation du sujet
2. Image : (Pleine largeur) - Image d'illustration
3. Titre : Étape 1
4. Texte : Explication de l'étape
5. Liste : Points clés
6. Image : (Droite) - Screenshot
7. Titre : Étape 2
8. Texte : Explication
9. Code : Exemple de code
10. Citation : Conseil important
11. Titre : Conclusion
12. Texte : Résumé final
```

### Structure Type : Top 5 / Classement
```
0. Titre : Introduction
1. Texte : Présentation du classement
2. Titre : #5 - Premier élément
3. Image : (Centre) - Image de l'élément
4. Liste : Caractéristiques
5. Texte : Description
6. Titre : #4 - Deuxième élément
7. Image : (Gauche) - Image
8. Liste : Caractéristiques
9. Texte : Description
... (répéter pour chaque élément)
N. Titre : Conclusion
N+1. Citation : Message final
```

### Structure Type : Comparaison
```
0. Titre : Introduction
1. Texte : Contexte de la comparaison
2. Titre : Option A
3. Image : (Droite) - Screenshot option A
4. Liste : Avantages
5. Liste : Inconvénients
6. Titre : Option B
7. Image : (Gauche) - Screenshot option B
8. Liste : Avantages
9. Liste : Inconvénients
10. Titre : Comparaison
11. Texte : Analyse comparative
12. Vidéo : Démonstration
13. Titre : Recommandation
14. Texte : Conclusion
```

## 🎯 Checklist Avant Publication

Avant de publier votre article, vérifiez :

- [ ] Le titre est clair et accrocheur
- [ ] Le résumé est complet et fait moins de 300 caractères
- [ ] L'image principale est uploadée et de bonne qualité
- [ ] Tous les blocs sont dans le bon ordre (0, 1, 2, 3...)
- [ ] Les images supplémentaires sont ajoutées et associées aux blocs
- [ ] Les listes HTML sont correctement formatées (`<ul>` ou `<ol>`)
- [ ] Les citations sont pertinentes et bien placées
- [ ] L'URL de la vidéo est correcte (format embed)
- [ ] Le contenu est relu et sans fautes
- [ ] L'article est coché comme "Publié"
- [ ] Le slug est correct et SEO-friendly

## 💡 Astuces Avancées

### Réutiliser des Structures
Une fois que vous avez créé un article avec une structure qui fonctionne bien, vous pouvez :
1. Noter l'ordre et les types de blocs utilisés
2. Réutiliser cette structure pour d'autres articles similaires
3. Utiliser le script `create_example_article.py` comme base et le modifier

### Optimisation des Images
- **Compression** : Utilisez des outils comme TinyPNG ou ImageOptim avant l'upload
- **Formats** : JPG pour les photos, PNG pour les screenshots avec texte
- **Dimensions** : 1200px de largeur maximum pour un bon équilibre qualité/taille

### Workflow Recommandé
1. **Planification** : Écrivez d'abord le plan de votre article (titres, structure)
2. **Création** : Créez l'article de base dans l'admin
3. **Images** : Préparez et uploadez toutes les images nécessaires
4. **Blocs** : Créez les blocs dans l'ordre prévu
5. **Révision** : Relisez et ajustez l'ordre si nécessaire
6. **Publication** : Vérifiez la checklist et publiez

---

**Bon blogging ! 🚀**

*Pour toute question ou problème, consultez la section Dépannage ci-dessus ou contactez l'administrateur.*

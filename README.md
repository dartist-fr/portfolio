# dartist. — Portfolio photographique

Portfolio photographique de **dartist.** : séries consacrées au sport, aux événements, aux voyages et aux instants du quotidien.

🌐 **Site en ligne :** https://dartist-fr.github.io/portfolio/  
📷 **Instagram :** [@dartist_photography](https://www.instagram.com/dartist_photography/)  
💻 **Dépôt GitHub :** https://github.com/dartist-fr/portfolio

## Fonctionnalités

- Albums et sous-albums organisés à partir des dossiers de photos.
- Page d’accueil avec image principale configurable et présentation des séries.
- Pages de séries avec photographie principale et galerie.
- Visionneuse pour consulter les images.
- Recherche de séries et navigation entre albums.
- Interface responsive et thème clair/sombre.
- Carrousel de séries cliquable, utilisable à la souris ou au doigt.
- Descriptions facultatives par album ou sous-série.
- Métadonnées facultatives pour afficher le lieu, la date et le contexte d’une photo.
- Ordre des photos existantes conservé lors de la génération du manifeste ; les nouvelles images sont ajoutées à la fin.
- Couvertures conservées tant que le fichier choisi existe toujours.

## Organisation du dépôt

- `index.html` : application du portfolio.
- `images/` : photographies classées par séries et sous-séries.
- `images-manifest.json` : données utilisées par le site.
- `scripts/generate-portfolio.py` : génération du manifeste à partir des dossiers d’images.
- `scripts/convert-jpg-to-webp.py` : conversion automatisée des JPG/JPEG en WebP.
- `scripts/validate-portfolio.py` : contrôles du contenu et du manifeste.
- `tests/` : tests de stabilité et de validation.
- `docs/README-AUTOMATISATION.md` : guide pour ajouter des photos et comprendre l’automatisation.
- `.github/workflows/` : workflows de génération, de vérification et de régression navigateur.

## Ajouter des photos ou une série

1. Ajoute les images dans le dossier correspondant sous `images/`, ou crée un nouveau dossier pour une série.
2. Envoie les modifications sur la branche `main`.
3. Le workflow **Actualiser le portfolio** convertit les fichiers JPG/JPEG en WebP, puis régénère `images-manifest.json`.
4. Vérifie l’exécution dans l’onglet [Actions](https://github.com/dartist-fr/portfolio/actions).
5. Après le déploiement GitHub Pages, contrôle la série sur le site.

Les dossiers et sous-dossiers servent à construire la hiérarchie des albums. Les fichiers README et `.gitkeep` ne sont pas des photos.

## Ordre des photos et couvertures

Le manifeste existant est utilisé comme référence pour conserver l’ordre des photos encore présentes. Les images nouvellement découvertes sont ajoutées à la fin, dans un ordre déterministe. Une couverture déjà choisie est conservée tant que son fichier existe toujours dans l’album ou ses sous-dossiers. Si elle a été supprimée, une nouvelle couverture est choisie à partir des images disponibles.

Pour cette raison, il n’est normalement pas nécessaire de modifier manuellement le manifeste après chaque ajout de photo. Le guide [Automatisation du portfolio](docs/README-AUTOMATISATION.md) détaille le comportement du générateur.

## Personnaliser le contenu du manifeste

Le fichier `images-manifest.json` contient notamment :

- `hero.image` et `hero.position` : image principale de la page d’accueil et position de cadrage ;
- `albums` : séries principales ;
- `children` : sous-séries ;
- `titre`, `sujet`, `cover` et `photos` : informations d’un album ;
- `description` : texte facultatif d’un album ;
- `photoMetadata` : informations facultatives associées aux chemins exacts des images, lorsque cette propriété est utilisée par la version du site.

Exemple de métadonnées facultatives :

```json
{
  "photoMetadata": {
    "images/Voyages/Londres/photo.webp": {
      "lieu": "Londres, Royaume-Uni",
      "date": "Avril 2025",
      "contexte": "Photographie de voyage"
    }
  },
  "albums": []
}
```

Cet extrait illustre la structure : ne remplace pas les albums existants par un tableau vide. Ajoute uniquement les propriétés souhaitées au manifeste réel et conserve les chemins exacts des fichiers.

## Publication et contrôles

Le site est publié avec **GitHub Pages**. Les workflows du dépôt vérifient le manifeste, les images référencées, certains aspects du HTML/JavaScript et la stabilité de l’ordre des photos. Consulte l’onglet [Actions](https://github.com/dartist-fr/portfolio/actions) pour connaître le résultat des contrôles.

Si une modification n’apparaît pas immédiatement, attends la fin du déploiement puis actualise la page. Le navigateur peut conserver certaines ressources en cache.

---

*Des instants vécus, des images à revivre.*

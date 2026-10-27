# dartist. — Portfolio photographique

Portfolio de **dartist.**, photographe depuis 2022. Le site rassemble des séries consacrées au sport, aux événements, aux voyages et aux instants du quotidien.

🌐 **Site en ligne :** https://dartist-fr.github.io/portfolio
📷 **Instagram :** [@dartist_photography](https://www.instagram.com/dartist_photography/)  
💻 **Dépôt GitHub :** https://github.com/dartist-fr/portfolio

---

## Fonctionnalités

- **Galerie organisée en albums et sous-albums** pour parcourir les différentes séries.
- **Affichage des photos** dans une visionneuse.
- **Recherche de séries** depuis la page d’accueil.
- **Interface responsive**, adaptée aux ordinateurs, tablettes et téléphones.
- **Thème clair ou sombre**.
- **Carrousel de séries** avec défilement automatique et navigation à la souris ou au doigt.
- **Favicon personnalisé** aux couleurs de dartist.
- **Métadonnées facultatives** pour afficher le lieu, la date et le contexte d’une photo.

## Organisation du contenu

Les albums et les photos sont pilotés par le fichier `images-manifest.json`. Il décrit la structure des albums et les chemins vers les images utilisées par le site.

Pour ajouter ou réorganiser des séries, modifie le manifeste en respectant sa structure JSON et les chemins des fichiers présents dans le dépôt. Vérifie ensuite le site après la publication par GitHub Pages.

> Les chemins des images dans le manifeste doivent correspondre exactement aux noms et à l’emplacement des fichiers, y compris les majuscules, minuscules et extensions.

## Ajouter des informations aux photos (facultatif)

Le portfolio fonctionne sans métadonnées. Pour afficher un lieu, une date ou un contexte dans la légende de la visionneuse, ajoute une propriété `photoMetadata` à la racine de `images-manifest.json`.

Exemple :

```json
{
  "photoMetadata": {
    "images/Voyages/Londres/Bentley London.jpg": {
      "lieu": "Londres, Royaume-Uni",
      "date": "Avril 2025",
      "contexte": "Photographie de voyage"
    }
  },
  "albums": []
}
```

**Important :** cet exemple illustre uniquement la structure. Dans le fichier réel, conserve le tableau `albums` déjà présent et ajoute `photoMetadata` à côté, sans remplacer le contenu existant. Les champs `lieu`, `date` et `contexte` sont facultatifs. Chaque clé de `photoMetadata` doit correspondre au chemin exact d’une image.

## Publication

Le site est publié avec **GitHub Pages**. Les modifications envoyées sur la branche publiée sont déployées automatiquement après le délai de mise à jour de GitHub Pages.

Si une modification n’apparaît pas tout de suite, attends quelques instants puis actualise la page. Le navigateur peut conserver certaines ressources en cache.

---

*Des instants vécus, des images à revivre.*

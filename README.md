# dartist — Portfolio photographique

Portfolio photographique de **dartist**, consacré à la photographie de voyage, de sport et d’événementiel.

Le site présente les photos sous forme de séries et de sous-séries, avec une page d’accueil illustrée, un affichage des photos en grand format et un thème clair/sombre.

## Fonctionnalités

- Galerie organisée en séries et sous-séries.
- Affichage d’une couverture et des photos de chaque série.
- Visionneuse plein écran (lightbox) pour agrandir les clichés.
- Thème clair/sombre, avec prise en compte du thème de l’appareil.
- Mise en page adaptée aux ordinateurs et aux mobiles.
- Chargement des séries depuis le fichier images-manifest.json, séparément du code de la page.

## Structure du projet

    /
    ├── index.html
    ├── images-manifest.json
    ├── images/
    │   ├── France/
    │   ├── Red Bull/
    │   ├── Sports/
    │   └── Voyages/
    └── README.md

Les dossiers présentés ci-dessus correspondent aux séries actuellement référencées dans le manifeste. Le dossier images/ contient les fichiers photo utilisés par le site.

- **index.html** : structure, styles et logique d’affichage du portfolio.
- **images-manifest.json** : données des séries, titres, sujets, couvertures et chemins des photos.
- **images/** : photographies référencées par le manifeste.
- **README.md** : documentation du projet.

## Lancer le site en local

Le site charge le manifeste avec fetch(). Il doit donc être servi par un petit serveur HTTP plutôt qu’ouvert directement en file://.

Avec Python installé, ouvre un terminal à la racine du projet et lance :

    python -m http.server 8000

Puis ouvre [http://localhost:8000](http://localhost:8000) dans ton navigateur.

Pour arrêter le serveur, utilise Ctrl+C dans le terminal.

## Ajouter des photos ou créer une série

1. Ajoute les photos dans le dossier images/, en organisant les fichiers dans des sous-dossiers si nécessaire.
2. Ouvre images-manifest.json.
3. Ajoute ou modifie une entrée dans albums en respectant la structure JSON existante.
4. Renseigne le titre (titre), le sujet (sujet), la couverture (cover) et la liste des fichiers (photos). Pour une série contenant des sous-séries, utilise children, comme dans les exemples existants.
5. Vérifie que chaque chemin correspond exactement au nom et à l’emplacement du fichier.
6. Enregistre le JSON et recharge le site pour vérifier l’affichage.

Exemple de série simple :

    {
      "titre": "Nouvelle série",
      "sujet": "Photographie · Exemple",
      "cover": "images/Nouvelle serie/couverture.webp",
      "photos": [
        "images/Nouvelle serie/couverture.webp",
        "images/Nouvelle serie/photo-02.webp"
      ]
    }

Les chemins de fichiers doivent être relatifs à la racine du site. Dans le JSON, utilise des / comme séparateurs. Si un nom de fichier contient des espaces ou des caractères spéciaux, encode-les dans les chemins d’URL (par exemple, un espace peut être écrit %20). Le manifeste doit rester un JSON valide.

### Photo de couverture de l’accueil

L’image de fond de la section d’accueil est définie dans la propriété hero.image de images-manifest.json. La propriété facultative hero.position permet d’ajuster le cadrage, par exemple "center 45%".

## Publier les modifications

Après avoir ajouté les photos et mis à jour le manifeste, envoie les modifications au dépôt GitHub. Si le dépôt est publié avec GitHub Pages, vérifie que la source de publication est configurée sur la branche et le dossier contenant index.html.

Le site récupère le manifeste à chaque chargement et demande une version sans cache pour celui-ci. En revanche, les fichiers doivent bien avoir été envoyés sur la branche publiée pour apparaître sur le site.

## Technologies

- HTML
- CSS
- JavaScript natif
- JSON pour les données de la galerie

Les polices Fraunces et Inter sont chargées depuis Google Fonts.

## Contact

- **E-mail :** [dartist.photography@gmail.com](mailto:dartist.photography@gmail.com)
- **Instagram :** [@dartist_photography](https://www.instagram.com/dartist_photography/)

---

© dartist — Photographie.

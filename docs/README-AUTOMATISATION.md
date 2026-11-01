# Portfolio — guide d’automatisation des séries

Les albums et sous-albums du portfolio sont générés à partir de l’arborescence du dossier `images/`. Le fichier `images-manifest.json` est construit automatiquement par GitHub Actions.

## Ajouter une série ou des photos

1. Ouvre le dossier `images/` dans le dépôt.
2. Pour une nouvelle série, crée un dossier. Pour une sous-série, crée un dossier à l’intérieur de la série correspondante.
3. Ajoute les photos dans le bon dossier. Les extensions prises en charge par le générateur sont JPG, JPEG, PNG, WebP, AVIF et GIF.
4. Envoie les changements sur `main`.
5. Le workflow **Actualiser le portfolio** se déclenche : il convertit les JPG/JPEG en WebP, génère le manifeste et pousse les changements si nécessaire.
6. Consulte l’onglet [Actions](https://github.com/dartist-fr/portfolio/actions) pour vérifier que le workflow s’est terminé correctement.

Les fichiers `README.md` et `.gitkeep` ne sont pas interprétés comme des images. Les dossiers vides ne créent pas de galerie visible.

## Comportement de génération

Le script `scripts/generate-portfolio.py` applique les règles suivantes :

- Les dossiers de premier niveau sous `images/` deviennent les albums principaux.
- Les sous-dossiers deviennent des sous-séries ; la structure peut être imbriquée.
- Les extensions JPG, JPEG, PNG, WebP, AVIF et GIF sont reconnues.
- Lorsqu’un JPG/JPEG possède un WebP correspondant portant le même nom de base, le JPG/JPEG n’est pas ajouté une seconde fois au manifeste.
- Les photos déjà présentes dans le manifeste et toujours disponibles conservent leur ordre.
- Les nouvelles photos sont ajoutées à la fin, avec un tri déterministe.
- Une couverture existante est conservée tant que le fichier correspondant existe encore dans l’album ou ses descendants.
- Si la couverture précédente a disparu, le générateur choisit une couverture parmi les photos disponibles ; pour un album sans photo directe, il peut reprendre la couverture d’une sous-série.
- L’image principale de la page d’accueil (`hero`) et sa position sont conservées lors de la génération si elles existent déjà dans le manifeste.

**Important :** le générateur ne remplace pas systématiquement les couvertures par la première image alphabétique. Il préserve les choix déjà enregistrés. Il n’est donc pas nécessaire de réordonner manuellement les photos après chaque ajout.

## Conversion JPG/JPEG vers WebP

Le workflow installe Pillow puis exécute `scripts/convert-jpg-to-webp.py` avant la génération du manifeste. Les fichiers originaux JPG/JPEG sont conservés par le script de conversion ; les versions WebP sont utilisées pour éviter les doublons dans la galerie lorsque le nom de base correspond.

La conversion ne doit pas être confondue avec une recompression à chaque affichage : elle est réalisée dans le workflow de dépôt, pas à chaque visite du portfolio.

## Actualisation manuelle

Si nécessaire, ouvre l’onglet **Actions** du dépôt, sélectionne **Actualiser le portfolio**, puis utilise **Run workflow**.

Le workflow automatique se déclenche aussi lors d’un push sur `main` qui modifie `images/**`, le générateur, le convertisseur ou le workflow lui-même.

## Fichiers concernés

- `scripts/generate-portfolio.py` : parcourt les dossiers, conserve l’ordre historique et génère les données JSON.
- `scripts/convert-jpg-to-webp.py` : convertit les images JPG/JPEG en WebP.
- `scripts/validate-portfolio.py` : contrôle le contenu et les références du manifeste.
- `tests/test_manifest_order.py` : vérifie la stabilité de l’ordre.
- `.github/workflows/portfolio-auto.yml` : conversion et génération automatiques.
- `.github/workflows/portfolio-checks.yml` : validations sur les pushes, pull requests et lancements manuels.
- `.github/workflows/browser-regression.yml` : workflow de régression navigateur.
- `images-manifest.json` : données consommées par la page du portfolio.

## En cas d’échec

1. Ouvre l’exécution en échec dans [Actions](https://github.com/dartist-fr/portfolio/actions).
2. Lis la première étape rouge et son journal.
3. Vérifie les noms et extensions des fichiers, ainsi que les références de couverture.
4. Corrige les fichiers concernés puis relance le workflow.

Le générateur annule la génération si le manifeste existant est illisible ou si des images référencées sont manquantes : cette protection évite de remplacer silencieusement des choix de galerie par un manifeste incomplet.

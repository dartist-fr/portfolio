# Automatisation du portfolio

## Génération du manifeste photo

Le script `scripts/generate-portfolio.py` génère `images-manifest.json` à partir des dossiers d'images présents dans `images/`.

Le workflow GitHub Actions `.github/workflows/portfolio-auto.yml` se lance :
- lors d'un push sur `main` qui modifie `images/**`, le script ou le workflow ;
- manuellement depuis l'onglet **Actions**, avec **Actualiser le portfolio** puis **Run workflow**.

Si le manifeste change, GitHub Actions le commit et le pousse sur `main`. Le workflow demande la permission `contents: write`.

## Vérifier l'exécution

Consultez l'onglet [Actions](https://github.com/dartist-fr/portfolio/actions) et ouvrez l'exécution la plus récente pour voir son résultat et ses journaux.

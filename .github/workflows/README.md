# Workflows GitHub Actions du portfolio

Ce dossier contient les automatisations de génération, de contrôle et de régression du portfolio.

## Actualiser le manifeste photo

Workflow : `portfolio-auto.yml` — **Actualiser le portfolio**.

Déclencheurs :
- push sur `main) qui modifie `images/**`, le générateur, le convertisseur JPG/WebP ou le workflow ;
- lancement manuel depuis l’onglet **Actions**.

Étapes principales :
1. récupère le dépôt ;
2. installe Python et Pillow ;
3. convertit les JPG/JPEG en WebP ;
4. exécute `scripts/generate-portfolio.py` ;
5. commit et pousse les changements d’images/manifeste si nécessaire.

Le workflow utilise la permission `contents: write` pour pouvoir enregistrer les fichiers générés. Il ne crée pas de commit si le portfolio est déjà à jour.

## Vérifier le portfolio

Workflow : `portfolio-checks.yml` — **Vérifier le portfolio**.

Déclencheurs :
- push sur les branches ;
- pull request ;
- lancement manuel.

Il exécute notamment :
- le test de stabilité de l’ordre des photos ;
- la validation du manifeste et des images référencées ;
- une vérification du HTML et du JavaScript intégré.

Cette vérification ne remplace pas un test visuel complet sur tous les navigateurs et appareils.

## Régression navigateur

Workflow : `browser-regression.yml`.

Il complète les contrôles automatisés par une vérification de régression navigateur. Consulte les étapes du workflow et les journaux de l’exécution pour connaître précisément les tests exécutés par la version actuelle.

## Consulter les résultats

Ouvre l’onglet [Actions du dépôt](https://github.com/dartist-fr/portfolio/actions), puis sélectionne le workflow et l’exécution souhaités. En cas d’échec, commence par lire le journal de la première étape en erreur.

Pour les règles de génération des albums, de conservation des couvertures et de conversion des photos, consulte [docs/README-AUTOMATISATION.md](../../docs/README-AUTOMATISATION.md).

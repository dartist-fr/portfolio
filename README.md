# dartist. — Photographie

Bienvenue sur mon portfolio photo ! 📸

Je partage ici mes photos de voyages, de sport et des moments capturés au fil de mes sorties.

🌐 **Voir le portfolio :** https://dartist-fr.github.io/

📷 **Instagram :** [@dartist_photography](https://www.instagram.com/dartist_photography/)

---

*Merci d’être passé !*

## Ajouter des informations aux photos (facultatif)

Le portfolio continue de fonctionner sans métadonnées. Pour afficher un lieu, une date ou un contexte dans la légende de la visionneuse, ajoute une propriété `photoMetadata` à la racine de `images-manifest.json`. Chaque clé correspond au chemin d'une image :

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

Garde la propriété `albums` existante et ajoute simplement `photoMetadata` à côté d'elle : **ne remplace pas tout le manifeste par cet exemple**. Les champs `lieu`, `date` et `contexte` sont tous facultatifs. Les chemins doivent correspondre à ceux des photos dans le manifeste.


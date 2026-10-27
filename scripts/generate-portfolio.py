#!/usr/bin/env python3
"""Construit images-manifest.json en conservant les couvertures déjà choisies."""
import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
IMAGE_ROOT = ROOT / "images"
OUTPUT = ROOT / "images-manifest.json"
EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".avif", ".gif"}
SUBJECTS = {
    "voyages": "Voyage · Photographie",
    "france": "France · Photographie",
    "red bull": "Sport · Événementiel",
    "sports": "Sport · Photographie",
    "sport": "Sport · Photographie",
    "evenementiel": "Événementiel · Photographie",
    "sports-mecaniques": "Sport mécanique · Photographie",
}


def label(folder_name):
    return folder_name.replace("-", " ").replace("_", " ").strip().title()


def image_url(path):
    return "/".join(quote(part) for part in path.relative_to(ROOT).parts)


def build(folder, root_label=None, previous=None):
    previous = previous or {}
    children = []
    previous_children = {
        child.get("titre"): child
        for child in previous.get("children", [])
        if isinstance(child, dict)
    }
    child_dirs = sorted(
        (p for p in folder.iterdir() if p.is_dir()),
        key=lambda p: p.name.casefold()
    )
    for child_dir in child_dirs:
        children.append(build(
            child_dir,
            root_label or folder.name,
            previous_children.get(label(child_dir.name))
        ))

    photos = sorted(
        (p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in EXTENSIONS),
        key=lambda p: p.name.casefold()
    )
    photo_urls = [image_url(p) for p in photos]

    # Toutes les images de ce dossier et de ses sous-dossiers restent candidates
    # pour la couverture d'un album parent.
    descendant_urls = set(photo_urls)
    for child in children:
        descendant_urls.update(child.get("_all_photo_urls", []))

    old_cover = previous.get("cover")
    if old_cover and old_cover in descendant_urls:
        # Ne change pas la couverture si le fichier existe toujours.
        cover = old_cover
    elif photo_urls:
        # Nouvel album, ou ancienne couverture supprimée : première image triée.
        cover = photo_urls[0]
    else:
        cover = next((c.get("cover") for c in children if c.get("cover")), "")

    top_name = root_label or folder.name
    subject = SUBJECTS.get(top_name.casefold(), "Photographie")
    item = {
        "titre": label(folder.name),
        "sujet": subject,
        "cover": cover,
        "photos": photo_urls,
    }
    if children:
        item["children"] = children
    item["_all_photo_urls"] = descendant_urls
    return item


def clean_internal_fields(item):
    item.pop("_all_photo_urls", None)
    for child in item.get("children", []):
        clean_internal_fields(child)


def count_photos(item):
    return len(item.get("photos", [])) + sum(count_photos(c) for c in item.get("children", []))


def main():
    if not IMAGE_ROOT.exists():
        raise SystemExit(f"Dossier introuvable : {IMAGE_ROOT}")

    previous_manifest = {}
    if OUTPUT.exists():
        try:
            previous_manifest = json.loads(OUTPUT.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            raise SystemExit("images-manifest.json est illisible : génération annulée pour protéger les couvertures.")

    previous_albums = {
        album.get("titre"): album
        for album in previous_manifest.get("albums", [])
        if isinstance(album, dict)
    }

    series = [
        build(folder, folder.name, previous_albums.get(label(folder.name)))
        for folder in sorted(
            (p for p in IMAGE_ROOT.iterdir() if p.is_dir()),
            key=lambda p: p.name.casefold()
        )
    ]
    for item in series:
        clean_internal_fields(item)

    manifest = {
        "hero": previous_manifest.get("hero", {
            "image": "images/Capture d'écran 2024-02-28 155431.png",
            "position": "center 45%",
        }),
        "albums": series,
    }
    OUTPUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    photo_count = sum(count_photos(s) for s in series)
    print(f"Manifeste généré : {len(series)} séries principales, {photo_count} photos.")
    print("Couvertures conservées tant que les fichiers correspondants existent.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Contrôles de cohérence du portfolio avant publication."""
import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "images-manifest.json"
HTML = ROOT / "index.html"


class MarkupChecks(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.duplicates, self.resources = set(), [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            if attrs["id"] in self.ids:
                self.duplicates.append(attrs["id"])
            self.ids.add(attrs["id"])
        for key in ("src", "href"):
            value = attrs.get(key, "")
            if value and "${" not in value and not value.startswith(("http://", "https://", "mailto:", "#", "?", "data:", "javascript:")):
                self.resources.append((tag, key, value))


def fail(errors):
    for error in errors:
        print(f"ERREUR: {error}", file=sys.stderr)
    raise SystemExit(1)


def local_file(value):
    path = unquote(value).split("?", 1)[0].split("#", 1)[0]
    return not path or Path(path).as_posix() in ("", ".") or (ROOT / path).is_file()


def main():
    errors = []
    if not HTML.is_file() or not MANIFEST.is_file():
        fail(["index.html ou images-manifest.json introuvable"])
    parser = MarkupChecks()
    parser.feed(HTML.read_text(encoding="utf-8"))
    if parser.duplicates:
        errors.append("IDs HTML dupliqués: " + ", ".join(sorted(set(parser.duplicates))))
    for tag, attr, value in parser.resources:
        if not local_file(value):
            errors.append(f"Ressource locale absente ({tag} {attr}): {value}")
    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        fail([f"images-manifest.json invalide: {exc}"])
    albums = manifest.get("albums")
    if not isinstance(albums, list):
        fail(["Le champ albums doit être une liste"])
    seen_titles = set()

    def check_album(album, trail, top=False):
        if not isinstance(album, dict):
            errors.append(f"{trail}: album non valide")
            return
        title = album.get("titre")
        if not isinstance(title, str) or not title.strip():
            errors.append(f"{trail}: titre absent ou vide")
            title = "?"
        if top:
            if title.casefold() in seen_titles:
                errors.append(f"Album principal dupliqué: {title}")
            seen_titles.add(title.casefold())
        photos = album.get("photos", [])
        if not isinstance(photos, list):
            errors.append(f"{title}: photos doit être une liste")
            photos = []
        values = ([("cover", album.get("cover"))] if album.get("cover") else []) + [(f"photos[{i}]", p) for i, p in enumerate(photos)]
        for label, value in values:
            if not isinstance(value, str) or not value:
                errors.append(f"{title}.{label}: chemin vide ou invalide")
            elif not local_file(value):
                errors.append(f"{title}.{label}: fichier absent: {value}")
        children = album.get("children", [])
        if not isinstance(children, list):
            errors.append(f"{title}: children doit être une liste")
        else:
            for child in children:
                check_album(child, trail + "/" + str(child.get("titre", "?")) if isinstance(child, dict) else trail + "/?")
    for album in albums:
        check_album(album, "albums", True)
    hero = manifest.get("hero", {})
    if not isinstance(hero, dict):
        errors.append("hero doit être un objet")
    elif hero.get("image") and not local_file(hero["image"]):
        errors.append(f"Image hero absente: {hero['image']}")
    if errors:
        fail(errors)
    print(f"OK: HTML analysé, {len(albums)} albums principaux et chemins d'images valides.")


if __name__ == "__main__":
    main()

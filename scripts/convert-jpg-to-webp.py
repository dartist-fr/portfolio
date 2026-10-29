#!/usr/bin/env python3
"""Convertit les JPG en WebP sans supprimer les originaux et actualise le manifeste."""
import json
from pathlib import Path
from urllib.parse import quote, unquote
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
IMAGE_ROOT = ROOT / "images"
MANIFEST = ROOT / "images-manifest.json"


def replace_path(value):
    decoded = unquote(value)
    if decoded.lower().endswith((".jpg", ".jpeg")):
        candidate = str(Path(decoded).with_suffix(".webp")).replace("\\", "/")
        if (ROOT / candidate).is_file():
            return quote(candidate, safe="/")
    return value


def walk_manifest(item):
    if not isinstance(item, dict):
        return
    for key in ("cover", "image"):
        if isinstance(item.get(key), str):
            item[key] = replace_path(item[key])
    if isinstance(item.get("photos"), list):
        item["photos"] = [replace_path(p) if isinstance(p, str) else p for p in item["photos"]]
    for child in item.get("children", []):
        walk_manifest(child)


def main():
    if not IMAGE_ROOT.is_dir() or not MANIFEST.is_file():
        raise SystemExit("Dossier images ou manifeste introuvable.")
    converted, failed = [], []
    for source in sorted(IMAGE_ROOT.rglob("*")):
        if not source.is_file() or source.suffix.lower() != ".jpg":
            continue
        target = source.with_suffix(".webp")
        if target.is_file() and target.stat().st_size:
            continue
        temp = target.with_name(target.name + ".tmp.webp")
        try:
            with Image.open(source) as image:
                if image.mode not in ("RGB", "RGBA"):
                    image = image.convert("RGBA" if "transparency" in image.info else "RGB")
                image.save(temp, "WEBP", quality=88, method=6)
            with Image.open(temp) as check:
                check.verify()
            if not temp.stat().st_size:
                raise RuntimeError("fichier WebP vide")
            temp.replace(target)
            converted.append((source.relative_to(ROOT).as_posix(), target.relative_to(ROOT).as_posix()))
        except Exception as exc:
            temp.unlink(missing_ok=True)
            failed.append((source, exc))
    try:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise SystemExit(f"Manifeste illisible, aucune mise à jour effectuée : {exc}") from exc
    for album in data.get("albums", []):
        walk_manifest(album)
    if isinstance(data.get("hero"), dict):
        walk_manifest(data["hero"])
    temp_manifest = MANIFEST.with_suffix(".json.tmp")
    temp_manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    json.loads(temp_manifest.read_text(encoding="utf-8"))
    temp_manifest.replace(MANIFEST)
    print(f"Images WebP créées : {len(converted)}. Les JPG originaux sont conservés.")
    for old, new in converted:
        print(f"{old} -> {new}")
    if failed:
        for path, error in failed:
            print(f"ÉCHEC : {path}: {error}")
        raise SystemExit(f"{len(failed)} conversion(s) ont échoué; les originaux sont conservés.")


if __name__ == "__main__":
    main()

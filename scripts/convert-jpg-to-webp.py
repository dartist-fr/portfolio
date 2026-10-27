#!/usr/bin/env python3
"""Convertit les images .jpg en .webp et met à jour les chemins du manifeste."""
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
IMAGE_ROOT = ROOT / "images"
MANIFEST = ROOT / "images-manifest.json"


def main():
    converted = []
    failed = []

    for source in sorted(IMAGE_ROOT.rglob("*")):
        if not source.is_file() or source.suffix.lower() != ".jpg":
            continue

        target = source.with_suffix(".webp")
        try:
            with Image.open(source) as image:
                # Conversion en RGB/RGBA pour assurer une sortie WebP valide.
                if image.mode not in ("RGB", "RGBA"):
                    image = image.convert("RGBA" if "transparency" in image.info else "RGB")
                image.save(target, "WEBP", quality=88, method=6)
            if not target.exists() or target.stat().st_size == 0:
                raise RuntimeError("fichier WebP vide")
            source.unlink()
            converted.append((source.relative_to(ROOT).as_posix(), target.relative_to(ROOT).as_posix()))
        except Exception as exc:
            if target.exists():
                target.unlink()
            failed.append((source, exc))

    if MANIFEST.exists() and converted:
        text = MANIFEST.read_text(encoding="utf-8")
        for old, new in converted:
            text = text.replace(old, new)
            text = text.replace(old.replace(" ", "%20"), new.replace(" ", "%20"))
        MANIFEST.write_text(text, encoding="utf-8")

    print(f"Images JPG converties en WebP : {len(converted)}")
    for old, new in converted:
        print(f"{old} -> {new}")
    if failed:
        for path, error in failed:
            print(f"ÉCHEC : {path}: {error}")
        raise SystemExit(f"{len(failed)} conversion(s) ont échoué; les fichiers sources concernés ont été conservés.")


if __name__ == "__main__":
    main()

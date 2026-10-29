#!/usr/bin/env python3
"""Génère des versions légères des photos (vignettes + grand format) dans images-opt/
et écrit images-opt/sizes.json (largeur/hauteur de chaque photo) pour éviter les sauts de mise en page.
Les originaux dans images/ ne sont jamais modifiés."""
import json
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "images"
OUT = ROOT / "images-opt"
EXT = {".webp", ".jpg", ".jpeg", ".png"}
SIZES = {"s": (800, 78), "m": (2000, 80)}  # nom: (largeur max, qualité)

Image.MAX_IMAGE_PIXELS = None
OUT.mkdir(exist_ok=True)
sizes = {}

for src in sorted(SRC.rglob("*")):
    if not src.is_file() or src.suffix.lower() not in EXT:
        continue
    rel = src.relative_to(ROOT).as_posix()          # ex. images/Red Bull/DSCF8807.webp
    stem = src.relative_to(SRC).with_suffix("")      # ex. Red Bull/DSCF8807
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)
        sizes[rel] = [im.width, im.height]
        for key, (maxw, quality) in SIZES.items():
            dest = OUT / key / stem.with_suffix(".webp")
            if dest.exists() and dest.stat().st_mtime >= src.stat().st_mtime:
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            w = min(maxw, im.width)
            h = round(im.height * w / im.width)
            out = im.convert("RGB").resize((w, h), Image.LANCZOS)
            out.save(dest, "WEBP", quality=quality, method=6)
            print("✓", dest.relative_to(ROOT))

(OUT / "sizes.json").write_text(json.dumps(sizes, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"{len(sizes)} photos indexées.")

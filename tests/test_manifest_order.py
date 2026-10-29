#!/usr/bin/env python3
"""Tests unitaires de stabilité de l’ordre des photos."""
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "generate_portfolio", ROOT / "scripts" / "generate-portfolio.py"
)
GENERATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GENERATOR)


class StablePhotoOrderTests(unittest.TestCase):
    def test_existing_photos_keep_their_order_and_new_photos_are_appended(self):
        previous = ["images/album/photo-z.webp", "images/album/photo-a.webp"]
        discovered = [
            "images/album/photo-new-b.webp",
            "images/album/photo-a.webp",
            "images/album/photo-new-a.webp",
            "images/album/photo-z.webp",
        ]
        self.assertEqual(
            GENERATOR.stable_photo_order(discovered, previous),
            [
                "images/album/photo-z.webp",
                "images/album/photo-a.webp",
                "images/album/photo-new-a.webp",
                "images/album/photo-new-b.webp",
            ],
        )

    def test_deleted_photos_are_removed_without_reordering_remaining_photos(self):
        previous = ["photo-c.webp", "photo-b.webp", "photo-a.webp"]
        discovered = ["photo-a.webp", "photo-new.webp", "photo-c.webp"]
        self.assertEqual(
            GENERATOR.stable_photo_order(discovered, previous),
            ["photo-c.webp", "photo-a.webp", "photo-new.webp"],
        )

    def test_first_generation_is_deterministic(self):
        discovered = ["z.webp", "B.webp", "a.webp"]
        self.assertEqual(
            GENERATOR.stable_photo_order(discovered, []),
            ["a.webp", "B.webp", "z.webp"],
        )


if __name__ == "__main__":
    unittest.main()

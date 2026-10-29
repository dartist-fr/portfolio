import os
import time
import unittest
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright


BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:8000/").rstrip("/") + "/"
LIVE_MODE = "dartist-fr.github.io" in BASE_URL


class PortfolioBrowserRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()
        cls.context = cls.browser.new_context(
            viewport={"width": 1365, "height": 900},
            device_scale_factor=1,
            has_touch=True,
            is_mobile=False,
        )

    @classmethod
    def tearDownClass(cls):
        cls.context.close()
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.page = self.context.new_page()
        self.errors = []
        self.page.on("pageerror", lambda error: self.errors.append(str(error)))
        # GitHub Pages may take a short time to publish a new commit.
        last_error = None
        for attempt in range(8 if LIVE_MODE else 1):
            try:
                response = self.page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30000)
                if response and response.status < 400:
                    break
                last_error = f"HTTP {response.status if response else 'no response'}"
            except Exception as exc:
                last_error = str(exc)
            if attempt < 7:
                time.sleep(8)
        else:
            self.fail(f"Portfolio inaccessible at {BASE_URL}: {last_error}")
        self.page.locator("#albums-view .album-card").first.wait_for(timeout=30000)
        self.page.wait_for_function(
            "() => window.portfolioData ? true : document.querySelectorAll('#albums-view .album-card').length > 0",
            timeout=10000,
        )

    def tearDown(self):
        self.page.close()

    def test_homepage_manifest_and_album_cards(self):
        self.assertIn("dartist", self.page.title().lower())
        self.assertGreater(self.page.locator("#albums-view .album-card").count(), 0)
        manifest_url = urljoin(BASE_URL, "images-manifest.json")
        response = self.page.request.get(manifest_url)
        self.assertEqual(response.status, 200, f"Manifest HTTP status: {response.status}")
        manifest = response.json()
        self.assertIsInstance(manifest.get("albums"), list)
        self.assertGreater(len(manifest["albums"]), 0)
        self.assertEqual(self.errors, [], f"JavaScript errors: {self.errors}")

    def test_search_filters_series_and_recovers(self):
        search = self.page.locator("#series-search")
        search.fill("Rome")
        self.assertGreater(self.page.locator("#albums-view .album-card").count(), 0)
        self.assertTrue(
            any("rome" in text.lower() for text in self.page.locator("#albums-view .album-title").all_text_contents()),
            "La recherche Rome doit afficher une série correspondante.",
        )
        search.fill("une-serie-qui-nexiste-pas-qa")
        self.assertTrue(self.page.get_by_text("Aucune série ne correspond à votre recherche.").is_visible())
        search.fill("")
        self.assertGreater(self.page.locator("#albums-view .album-card").count(), 0)

    def test_theme_toggle_and_system_default_override(self):
        root = self.page.locator("html")
        before = root.get_attribute("data-theme")
        self.page.locator("#theme-toggle").click()
        after = root.get_attribute("data-theme")
        self.assertIn(after, ("light", "dark"))
        self.assertNotEqual(before, after, "Le bouton doit réellement changer le thème.")
        expected_label = "Activer le thème clair" if after == "dark" else "Activer le thème sombre"
        self.assertEqual(self.page.locator("#theme-toggle").get_attribute("aria-label"), expected_label)

    def test_lightbox_keyboard_navigation_and_close(self):
        self.page.goto(urljoin(BASE_URL, "?album=Divers"), wait_until="domcontentloaded")
        self.page.locator("#photo-view").wait_for(state="visible", timeout=15000)
        trigger = self.page.locator(".featured-photo").first
        if trigger.count() == 0:
            trigger = self.page.locator(".photo-item").first
        trigger.wait_for(state="visible", timeout=15000)
        trigger.click()
        lightbox = self.page.locator("#lightbox")
        lightbox.wait_for(state="visible")
        self.assertIn("open", lightbox.get_attribute("class") or "")
        initial_counter = self.page.locator("#lightbox-counter").inner_text()
        self.page.keyboard.press("ArrowRight")
        self.assertNotEqual(
            self.page.locator("#lightbox-counter").inner_text(),
            initial_counter,
            "Flèche droite doit afficher la photo suivante.",
        )
        self.page.keyboard.press("ArrowLeft")
        self.assertEqual(self.page.locator("#lightbox-counter").inner_text(), initial_counter)
        self.page.keyboard.press("Escape")
        self.assertNotIn("open", lightbox.get_attribute("class") or "")

    def test_lightbox_outside_click_closes(self):
        self.page.goto(urljoin(BASE_URL, "?album=Divers"), wait_until="domcontentloaded")
        self.page.locator("#photo-view").wait_for(state="visible", timeout=15000)
        self.page.locator(".featured-photo").first.click()
        lightbox = self.page.locator("#lightbox")
        lightbox.wait_for(state="visible")
        lightbox.click(position={"x": 8, "y": 8})
        self.assertNotIn("open", lightbox.get_attribute("class") or "")

    def test_mobile_layout_and_touch_swipe(self):
        self.page.set_viewport_size({"width": 390, "height": 844})
        self.page.goto(urljoin(BASE_URL, "?album=Divers"), wait_until="domcontentloaded")
        self.page.locator("#photo-view").wait_for(state="visible", timeout=15000)
        self.assertLessEqual(
            self.page.evaluate("document.documentElement.scrollWidth"),
            self.page.evaluate("window.innerWidth") + 1,
            "La page mobile ne doit pas créer de débordement horizontal global.",
        )
        self.page.locator(".featured-photo").first.click()
        lightbox = self.page.locator("#lightbox")
        lightbox.wait_for(state="visible")
        counter = self.page.locator("#lightbox-counter")
        before = counter.inner_text()
        # Synthetic touch events exercise the same registered listeners in headless CI.
        self.page.evaluate("""() => {
          const target = document.getElementById('lightbox');
          const send = (type, x, y) => {
            const event = new Event(type, { bubbles: true, cancelable: true });
            Object.defineProperty(event, 'changedTouches', { value: [{ clientX: x, clientY: y }] });
            target.dispatchEvent(event);
          };
          send('touchstart', 300, 400);
          send('touchend', 220, 402);
        }""")
        self.assertNotEqual(counter.inner_text(), before, "Un balayage horizontal doit changer de photo.")
        self.page.keyboard.press("Escape")
        self.assertNotIn("open", lightbox.get_attribute("class") or "")


if __name__ == "__main__":
    unittest.main(verbosity=2)

"""Tests for website build (PL/EN pages, hreflang, sitemap)."""

from __future__ import annotations

import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]


class BuildWebsiteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.run(
            [sys.executable, str(_REPO / "tool" / "build_website.py")],
            check=True,
            cwd=_REPO,
        )

    def test_generates_eight_html_pages(self) -> None:
        expected = [
            "index.html",
            "o-nas.html",
            "polityka-prywatnosci.html",
            "regulamin.html",
            "en/index.html",
            "en/about.html",
            "en/privacy-policy.html",
            "en/terms-of-service.html",
        ]
        for rel in expected:
            self.assertTrue((_REPO / rel).is_file(), rel)

    def test_home_has_hreflang_pair(self) -> None:
        html = (_REPO / "index.html").read_text(encoding="utf-8")
        self.assertIn('hreflang="pl"', html)
        self.assertIn('hreflang="en"', html)
        self.assertIn("https://arngcor.pl/en/", html)

    def test_en_home_has_lang_switcher(self) -> None:
        html = (_REPO / "en/index.html").read_text(encoding="utf-8")
        self.assertIn('lang="en"', html)
        self.assertIn('data-lang="pl"', html)
        self.assertIn('data-lang="en"', html)
        self.assertIn("/js/i18n.js", html)
        self.assertIn("/images/app-home-en.png", html)

    def test_home_uses_app_favicon(self) -> None:
        html = (_REPO / "index.html").read_text(encoding="utf-8")
        self.assertIn('/images/favicon-32x32.png', html)
        self.assertIn('/images/apple-touch-icon.png', html)
        self.assertNotIn('rel="icon" href="/images/app-home.png"', html)

    def test_pl_home_uses_pl_mock(self) -> None:
        html = (_REPO / "index.html").read_text(encoding="utf-8")
        self.assertIn("/images/app-home.png", html)
        self.assertNotIn("/images/app-home-en.png", html)

    def test_sitemap_has_eight_urls(self) -> None:
        root = ET.fromstring((_REPO / "sitemap.xml").read_text(encoding="utf-8"))
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locs = [el.text for el in root.findall("sm:url/sm:loc", ns)]
        self.assertEqual(len(locs), 8)
        self.assertIn("https://arngcor.pl/en/about.html", locs)


if __name__ == "__main__":
    unittest.main()

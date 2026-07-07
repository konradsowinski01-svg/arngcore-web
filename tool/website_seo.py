"""Wspólne meta tagi SEO, Open Graph i JSON-LD dla strony arngcor.pl (PL + EN)."""

from __future__ import annotations

import html
import json
from datetime import date
from pathlib import Path

BASE_URL = "https://arngcor.pl"
SITE_NAME = "ARNGCOR"
ORG_NAME = "SovinSky Studio"
CONTACT_EMAIL = "kontakt@arngcor.pl"
OG_IMAGE = f"{BASE_URL}/images/app-home.png"
OG_IMAGE_WIDTH = 499
OG_IMAGE_HEIGHT = 1024
THEME_COLOR = "#1a1512"

# Pary stron PL (root) ↔ EN (/en/).
PAGE_REGISTRY: list[dict[str, str | float]] = [
    {
        "id": "home",
        "pl_path": "",
        "pl_file": "index.html",
        "en_path": "en/",
        "en_file": "en/index.html",
        "changefreq": "weekly",
        "priority": "1.0",
    },
    {
        "id": "about",
        "pl_path": "o-nas.html",
        "pl_file": "o-nas.html",
        "en_path": "en/about.html",
        "en_file": "en/about.html",
        "changefreq": "monthly",
        "priority": "0.8",
    },
    {
        "id": "privacy",
        "pl_path": "polityka-prywatnosci.html",
        "pl_file": "polityka-prywatnosci.html",
        "en_path": "en/privacy-policy.html",
        "en_file": "en/privacy-policy.html",
        "changefreq": "yearly",
        "priority": "0.3",
    },
    {
        "id": "terms",
        "pl_path": "regulamin.html",
        "pl_file": "regulamin.html",
        "en_path": "en/terms-of-service.html",
        "en_file": "en/terms-of-service.html",
        "changefreq": "yearly",
        "priority": "0.3",
    },
]


def _page_entry(page_id: str) -> dict[str, str | float]:
    for entry in PAGE_REGISTRY:
        if entry["id"] == page_id:
            return entry
    raise KeyError(page_id)


def canonical_url(path: str) -> str:
    if not path:
        return f"{BASE_URL}/"
    return f"{BASE_URL}/{path}"


def alternate_urls(page_id: str) -> dict[str, str]:
    entry = _page_entry(page_id)
    return {
        "pl": canonical_url(str(entry["pl_path"])),
        "en": canonical_url(str(entry["en_path"])),
    }


def seo_head(
    *,
    title: str,
    description: str,
    page_id: str,
    locale: str,
    og_type: str = "website",
    json_ld: object | None = None,
    include_fonts: bool = True,
    keywords: str | None = None,
) -> str:
    """Fragment <head> od meta description do końca JSON-LD."""
    entry = _page_entry(page_id)
    path = str(entry["pl_path"] if locale == "pl" else entry["en_path"])
    url = canonical_url(path)
    alts = alternate_urls(page_id)
    safe_desc = html.escape(description, quote=True)
    safe_title = html.escape(title, quote=True)
    html_lang = "pl" if locale == "pl" else "en"
    og_locale = "pl_PL" if locale == "pl" else "en_US"
    og_alt = (
        "Ekran aplikacji mobilnej ARNGCOR"
        if locale == "pl"
        else "ARNGCOR mobile app screen"
    )

    kw = keywords or (
        "ARNGCOR, aplikacja mobilność, rozciąganie, joga, wyzwanie mostek, "
        "wyzwanie szpagat, aplikacja iOS, SovinSky Studio"
        if locale == "pl"
        else "ARNGCOR, mobility app, stretching, yoga, wheel challenge, "
        "front split challenge, iOS app, SovinSky Studio"
    )

    fonts = ""
    if include_fonts:
        fonts = """
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">"""

    json_ld_block = ""
    if json_ld is not None:
        payload = json.dumps(json_ld, ensure_ascii=False, separators=(",", ":"))
        json_ld_block = f"""
  <script type="application/ld+json">{payload}</script>"""

    return f"""  <meta name="description" content="{safe_desc}">
  <meta name="keywords" content="{html.escape(kw, quote=True)}">
  <meta name="author" content="{ORG_NAME}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <meta name="theme-color" content="{THEME_COLOR}">
  <link rel="canonical" href="{url}">
  <link rel="alternate" hreflang="pl" href="{alts['pl']}">
  <link rel="alternate" hreflang="en" href="{alts['en']}">
  <link rel="alternate" hreflang="x-default" href="{alts['en']}">
  <link rel="icon" href="/images/app-home.png" type="image/png">
  <link rel="apple-touch-icon" href="/images/app-home.png">
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta property="og:locale" content="{og_locale}">
  <meta property="og:title" content="{safe_title}">
  <meta property="og:description" content="{safe_desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta property="og:image:width" content="{OG_IMAGE_WIDTH}">
  <meta property="og:image:height" content="{OG_IMAGE_HEIGHT}">
  <meta property="og:image:alt" content="{html.escape(og_alt, quote=True)}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{safe_title}">
  <meta name="twitter:description" content="{safe_desc}">
  <meta name="twitter:image" content="{OG_IMAGE}">{fonts}{json_ld_block}
"""


def home_json_ld(locale: str, description: str) -> dict:
    in_lang = "pl-PL" if locale == "pl" else "en-US"
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": f"{BASE_URL}/#organization",
                "name": ORG_NAME,
                "url": BASE_URL,
                "email": CONTACT_EMAIL,
                "logo": OG_IMAGE,
            },
            {
                "@type": "WebSite",
                "@id": f"{BASE_URL}/#website",
                "url": BASE_URL,
                "name": SITE_NAME,
                "description": description,
                "inLanguage": in_lang,
                "publisher": {"@id": f"{BASE_URL}/#organization"},
            },
            {
                "@type": "SoftwareApplication",
                "@id": f"{BASE_URL}/#app",
                "name": SITE_NAME,
                "applicationCategory": "HealthApplication",
                "operatingSystem": "iOS",
                "description": description,
                "url": BASE_URL,
                "image": OG_IMAGE,
                "offers": {
                    "@type": "Offer",
                    "price": "0",
                    "priceCurrency": "PLN",
                    "availability": "https://schema.org/PreOrder",
                },
                "publisher": {"@id": f"{BASE_URL}/#organization"},
            },
        ],
    }


def about_json_ld(locale: str, *, name: str, description: str) -> dict:
    path = "o-nas.html" if locale == "pl" else "en/about.html"
    return {
        "@context": "https://schema.org",
        "@type": "AboutPage",
        "name": name,
        "url": canonical_url(path),
        "description": description,
        "inLanguage": "pl-PL" if locale == "pl" else "en-US",
        "isPartOf": {"@type": "WebSite", "name": SITE_NAME, "url": BASE_URL},
        "about": {"@type": "Organization", "name": ORG_NAME, "email": CONTACT_EMAIL},
    }


def web_page_json_ld(*, name: str, page_id: str, locale: str, description: str) -> dict:
    entry = _page_entry(page_id)
    path = str(entry["pl_path"] if locale == "pl" else entry["en_path"])
    return {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": name,
        "url": canonical_url(path),
        "description": description,
        "inLanguage": "pl-PL" if locale == "pl" else "en-US",
        "isPartOf": {"@type": "WebSite", "name": SITE_NAME, "url": BASE_URL},
    }


def write_robots_txt(website_dir: Path) -> None:
    content = f"""User-agent: *
Allow: /

Sitemap: {BASE_URL}/sitemap.xml
"""
    (website_dir / "robots.txt").write_text(content, encoding="utf-8")


def write_sitemap_xml(website_dir: Path) -> None:
    today = date.today().isoformat()
    urls: list[str] = []
    for page in PAGE_REGISTRY:
        for locale_key in ("pl_path", "en_path"):
            path = str(page[locale_key])
            file_key = "pl_file" if locale_key == "pl_path" else "en_file"
            file_path = website_dir / str(page[file_key])
            lastmod = today
            if file_path.is_file():
                mtime = date.fromtimestamp(file_path.stat().st_mtime).isoformat()
                lastmod = mtime
            loc = canonical_url(path)
            urls.append(
                "  <url>\n"
                f"    <loc>{loc}</loc>\n"
                f"    <lastmod>{lastmod}</lastmod>\n"
                f"    <changefreq>{page['changefreq']}</changefreq>\n"
                f"    <priority>{page['priority']}</priority>\n"
                "  </url>"
            )

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )
    (website_dir / "sitemap.xml").write_text(xml, encoding="utf-8")

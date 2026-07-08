#!/usr/bin/env python3
"""Generuje strony PL/EN, robots.txt i sitemap.xml w katalogu głównym repo."""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

_TOOL = Path(__file__).resolve().parent
if str(_TOOL) not in sys.path:
    sys.path.insert(0, str(_TOOL))

from jinja2 import Environment, FileSystemLoader, select_autoescape

from website_seo import (  # noqa: E402
    CONTACT_EMAIL,
    about_json_ld,
    home_json_ld,
    seo_head,
    web_page_json_ld,
    write_robots_txt,
    write_site_webmanifest,
    write_sitemap_xml,
)

_REPO = Path(__file__).resolve().parents[1]
_LEGAL = _REPO / "assets" / "legal"
_WEBSITE = _REPO
_I18N = _REPO / "i18n"
_TEMPLATES = _REPO / "templates"

_PAGE_URLS = {
    "pl": {
        "home": "index.html",
        "about": "o-nas.html",
        "privacy": "polityka-prywatnosci.html",
        "terms": "regulamin.html",
    },
    "en": {
        "home": "index.html",
        "about": "about.html",
        "privacy": "privacy-policy.html",
        "terms": "terms-of-service.html",
    },
}

_OUTPUT = {
    "pl": {
        "home": _WEBSITE / "index.html",
        "about": _WEBSITE / "o-nas.html",
        "privacy": _WEBSITE / "polityka-prywatnosci.html",
        "terms": _WEBSITE / "regulamin.html",
    },
    "en": {
        "home": _WEBSITE / "en" / "index.html",
        "about": _WEBSITE / "en" / "about.html",
        "privacy": _WEBSITE / "en" / "privacy-policy.html",
        "terms": _WEBSITE / "en" / "terms-of-service.html",
    },
}

_LEGAL_FILES = {
    "pl": {
        "privacy": _LEGAL / "privacy_policy_pl.txt",
        "terms": _LEGAL / "terms_of_service_pl.txt",
    },
    "en": {
        "privacy": _LEGAL / "privacy_policy_en.txt",
        "terms": _LEGAL / "terms_of_service_en.txt",
    },
}


def _load_i18n(locale: str) -> dict:
    path = _I18N / f"{locale}.json"
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def _txt_to_body(raw: str) -> str:
    raw = raw.replace("LEGAL_CONTACT_EMAIL", CONTACT_EMAIL)
    lines = raw.splitlines()
    parts: list[str] = []
    in_table = False
    table_rows: list[str] = []

    def flush_table() -> None:
        nonlocal in_table, table_rows
        if not table_rows:
            return
        parts.append('<table class="legal-table">')
        for i, row in enumerate(table_rows):
            cells = [c.strip() for c in row.split("|")]
            tag = "th" if i == 0 else "td"
            parts.append(
                "<tr>"
                + "".join(f"<{tag}>{html.escape(c)}</{tag}>" for c in cells)
                + "</tr>"
            )
        parts.append("</table>")
        table_rows = []
        in_table = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("|") and "|" in stripped[1:]:
            in_table = True
            table_rows.append(stripped.strip("|"))
            continue
        if in_table:
            flush_table()
        if not stripped:
            parts.append("")
            continue
        if stripped.startswith("http://") or stripped.startswith("https://"):
            parts.append(
                f'<p><a href="{html.escape(stripped)}" rel="noopener">'
                f"{html.escape(stripped)}</a></p>"
            )
            continue
        if re.match(r"^\d+\.\s", stripped) and len(stripped) < 120 and stripped.count(".") == 1:
            flush_table()
            parts.append(f"<h2>{html.escape(stripped)}</h2>")
            continue
        if re.match(r"^\d+\.\d+\.", stripped):
            flush_table()
            parts.append(f"<h3>{html.escape(stripped)}</h3>")
            continue
        if stripped.startswith("- "):
            parts.append(f"<li>{html.escape(stripped[2:])}</li>")
            continue
        parts.append(f"<p>{html.escape(stripped)}</p>")

    flush_table()
    body = "\n".join(parts)
    body = re.sub(
        r"(<li>.*?</li>\n?)+",
        lambda m: "<ul>\n" + m.group(0) + "</ul>\n",
        body,
    )
    return body


def _jinja_env() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(_TEMPLATES)),
        autoescape=select_autoescape(["html", "xml"]),
    )


def _render_page(
    env: Environment,
    *,
    template_name: str,
    locale: str,
    t: dict,
    active: str,
    page_title: str,
    seo_block: str,
    extra: dict | None = None,
) -> str:
    ctx = {
        "t": t,
        "urls": _PAGE_URLS[locale],
        "active": active,
        "page_title": page_title,
        "seo_head": seo_block,
    }
    if extra:
        ctx.update(extra)
    return env.get_template(template_name).render(**ctx)


def main() -> None:
    env = _jinja_env()
    written: list[str] = []

    for locale in ("pl", "en"):
        t = _load_i18n(locale)

        home_meta = t["meta"]["home"]
        home_desc = t["json_ld"]["home_description"]
        home_seo = seo_head(
            title=home_meta["title"],
            description=home_meta["description"],
            page_id="home",
            locale=locale,
            json_ld=home_json_ld(locale, home_desc),
        )
        home_html = _render_page(
            env,
            template_name="home.html.j2",
            locale=locale,
            t=t,
            active="home",
            page_title=home_meta["title"],
            seo_block=home_seo,
        )
        out_home = _OUTPUT[locale]["home"]
        out_home.parent.mkdir(parents=True, exist_ok=True)
        out_home.write_text(home_html + "\n", encoding="utf-8")
        written.append(str(out_home.relative_to(_REPO)))

        about_meta = t["meta"]["about"]
        about_seo = seo_head(
            title=about_meta["title"],
            description=about_meta["description"],
            page_id="about",
            locale=locale,
            json_ld=about_json_ld(
                locale,
                name=t["json_ld"]["about_name"],
                description=t["json_ld"]["about_description"],
            ),
        )
        about_html = _render_page(
            env,
            template_name="about.html.j2",
            locale=locale,
            t=t,
            active="about",
            page_title=about_meta["title"],
            seo_block=about_seo,
        )
        out_about = _OUTPUT[locale]["about"]
        out_about.write_text(about_html + "\n", encoding="utf-8")
        written.append(str(out_about.relative_to(_REPO)))

        for legal_key in ("privacy", "terms"):
            legal_meta = t["meta"][legal_key]
            legal_raw = _LEGAL_FILES[locale][legal_key].read_text(encoding="utf-8")
            legal_body = _txt_to_body(legal_raw)
            legal_seo = seo_head(
                title=legal_meta["title"],
                description=legal_meta["description"],
                page_id=legal_key,
                locale=locale,
                include_fonts=False,
                json_ld=web_page_json_ld(
                    name=legal_meta["title"],
                    page_id=legal_key,
                    locale=locale,
                    description=legal_meta["description"],
                ),
            )
            legal_html = _render_page(
                env,
                template_name="legal.html.j2",
                locale=locale,
                t=t,
                active=legal_key,
                page_title=legal_meta["title"],
                seo_block=legal_seo,
                extra={"legal_body": legal_body},
            )
            out_legal = _OUTPUT[locale][legal_key]
            out_legal.write_text(legal_html + "\n", encoding="utf-8")
            written.append(str(out_legal.relative_to(_REPO)))

    write_robots_txt(_WEBSITE)
    write_site_webmanifest(_WEBSITE)
    write_sitemap_xml(_WEBSITE)
    written.extend(["robots.txt", "site.webmanifest", "sitemap.xml"])

    print("Zapisano:")
    for path in written:
        print(f"  {path}")


if __name__ == "__main__":
    main()

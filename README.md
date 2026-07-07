# arngcore-web

Publiczna strona [arngcor.pl](https://arngcor.pl) - landing PL/EN, O nas, polityka prywatności, regulamin.

**To jest jedyne repo strony WWW.** Kod aplikacji Flutter jest w osobnym repo `arngcor`.

## Struktura

```
index.html, o-nas.html, en/...     - wygenerowane HTML (GitHub Pages serwuje z root)
i18n/pl.json, i18n/en.json         - copy marketingowe (źródło prawdy)
templates/*.html.j2                - szablony Jinja2
assets/legal/*_pl.txt, *_en.txt    - dokumenty prawne (źródło dla stron HTML)
css/, js/, images/                 - statyczne assety
tool/build_website.py              - generator stron
robots.txt, sitemap.xml, CNAME     - SEO + domena
```

## Edycja i deploy

```bash
pip install -r tool/requirements-website.txt   # jednorazowo
python3 tool/build_website.py
python3 -m unittest test/build_website_test.py
git add -A && git commit && git push
```

Push na `main` = strona live na `arngcor.pl` (GitHub Pages).

- Copy landing + O nas: `i18n/pl.json` / `i18n/en.json`, potem build.
- Dokumenty prawne na stronie: `assets/legal/*.txt`, potem build.

Szczegóły DNS, OAuth, Search Console: [docs/WEBSITE_DEPLOY.md](docs/WEBSITE_DEPLOY.md).

## Spójność z aplikacją

Treści prawnych w aplikacji (in-app) trzymamy w `arngcor/assets/legal/`. Po zmianie polityki lub regulaminu zaktualizuj **oba** miejsca (app + to repo), żeby tekst na stronie i w aplikacji był zgodny.

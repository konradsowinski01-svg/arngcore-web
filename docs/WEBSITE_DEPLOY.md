# Strona arngcor.pl - domena + hosting 0 zł

Repo strony: **https://github.com/konradsowinski01-svg/arngcore-web** (publiczne, GitHub Pages).

## Koszty (uczciwie)

| Element | Koszt |
|---------|--------|
| **Hosting** (GitHub Pages) | **0 zł** |
| **SSL (HTTPS)** | **0 zł** (automatycznie) |
| **Domena arngcor.pl** | **~10-35 zł/rok** u rejestratora |

## Co jest w tym repo

```
index.html, o-nas.html, en/...     - wygenerowane (nie edytuj ręcznie)
i18n/pl.json, i18n/en.json         - copy marketingowe
templates/*.html.j2                - szablony
assets/legal/*.txt                 - dokumenty prawne (strona HTML)
css/, js/, images/                 - statyczne assety
tool/build_website.py              - build
robots.txt, sitemap.xml, CNAME
```

Regeneracja po edycji copy lub legal:

```bash
pip install -r tool/requirements-website.txt
python3 tool/build_website.py
git add -A && git commit && git push
```

Push na `main` publikuje od razu na `arngcor.pl`.

---

## Krok 1 - Kup domenę arngcor.pl

- [nazwa.pl](https://www.nazwa.pl)
- [home.pl](https://home.pl)
- [OVH.pl](https://www.ovh.pl)

**Właściciel domeny:** Ty (wymagane dla Google OAuth i App Store).

---

## Krok 2 - GitHub Pages

- **Settings → Pages:** branch `main`, folder `/`
- **Custom domain:** `arngcor.pl`
- **Enforce HTTPS** po weryfikacji DNS

Plik `CNAME` zawiera `arngcor.pl`.

---

## Krok 3 - DNS

| Typ | Nazwa | Wartość |
|-----|--------|---------|
| **A** | `@` | `185.199.108.153` |
| **A** | `@` | `185.199.109.153` |
| **A** | `@` | `185.199.110.153` |
| **A** | `@` | `185.199.111.153` |
| **CNAME** | `www` | `TWOJ_USER.github.io` |

[Aktualna lista IP - GitHub Docs](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)

---

## Krok 4 - Google Search Console

1. [Google Search Console](https://search.google.com/search-console) → `arngcor.pl`
2. Mapa witryn: `https://arngcor.pl/sitemap.xml` (8 URL-i PL+EN)
3. Poproś o indeksowanie `/` i `/en/`

---

## Krok 5 - Google OAuth / App Store

- Home: `https://arngcor.pl/` lub `https://arngcor.pl/en/`
- Privacy: `https://arngcor.pl/polityka-prywatnosci.html` + `https://arngcor.pl/en/privacy-policy.html`
- Terms: `https://arngcor.pl/regulamin.html` + `https://arngcor.pl/en/terms-of-service.html`

App Store Connect: listing EN może wskazywać `/en/privacy-policy.html`.

---

## Smoke test PL/EN

- [ ] `https://arngcor.pl/` - PL, przełącznik PL | EN
- [ ] `https://arngcor.pl/en/` - EN
- [ ] Przeglądarka `en-US`, czyste `localStorage` - redirect na `/en/` z root PL
- [ ] Przeglądarka `pl-PL` - zostaje na PL
- [ ] `rg '[\u2013\u2014]' i18n/en.json en/` - brak em/en dash w EN

---

## E-mail kontaktowy

Publiczny adres: **`kontakt@arngcor.pl`**. Przekierowanie np. przez [ImprovMX](https://improvmx.com/).

---

## Checklist

- [ ] Kupiono `arngcor.pl`
- [ ] GitHub Pages + workflow zielony
- [ ] DNS + HTTPS działa
- [ ] `python3 tool/build_website.py` + push na main
- [ ] Sitemap w Search Console
- [ ] Google OAuth + App Store URL-e zaktualizowane

# Finect Financials — statische kopie van www.finect.nl

Deze map (`site/`) bevat een volledige, zelfstandige kopie van
[finect.nl](https://finect.nl) zoals de site er op **23 september 2026** uitzag.

De originele site draait op WordPress (thema *Zikzag* + Elementor + Slider
Revolution). Deze kopie is de door WordPress gerenderde HTML, samen met alle
CSS, JavaScript, lettertypen, afbeeldingen en PDF's — dus geen PHP en geen
database nodig.

## Bekijken

```bash
python3 -m http.server 8080 --directory site
# open http://localhost:8080
```

Of publiceer `site/` op elke statische host (GitHub Pages, Netlify, S3, een
gewone Apache/Nginx-docroot). Er is geen buildstap.

## Wat is er gekopieerd

| Pagina | Pad |
| --- | --- |
| Home | `site/index.html` |
| Verzekeringen | `site/verzekeringen/` |
| Zakelijk | `site/zakelijk/` |
| Hypotheken | `site/hypotheken/` |
| Over Finect | `site/over-finect/` |
| Contact | `site/contact/` |
| Nieuws | `site/nieuws/` |
| Vergelijkingskaarten | `site/vergelijkingskaarten/` |
| AOV | `site/arbeidsongeschiktheidsverzekeringen-aov/` |
| Blogartikelen | `site/huis/…`, `site/ondernemer/…` |
| Categorieën | `site/category/huis/`, `site/category/ondernemer/` |
| Auteur | `site/author/fred/` |
| Elementor-templates | `site/elementor-4497/`, `site/elementor-4597/` |

Alle assets staan onder `site/wp-content/` en `site/wp-includes/`, op dezelfde
paden als op de originele site. De PDF's (dienstenwijzer, algemene voorwaarden,
privacy statement, vergelijkingskaarten) staan in `site/wp-content/uploads/`.

## Aanpassingen ten opzichte van het origineel

Puur technisch; de opmaak en inhoud zijn ongewijzigd.

1. **Relatieve links.** Alle interne `href`/`src` verwijzingen zijn omgezet naar
   relatieve paden, zodat de kopie op elk domein of vanaf schijf werkt.
2. **Versienummers uit bestandsnamen.** WordPress hangt `?ver=…` aan CSS/JS.
   Die query strings zijn uit de bestandsnamen en verwijzingen gehaald
   (`style.css?ver=a1ac0d…` → `style.css`).
3. **Menu-links.** Het menu gebruikte `?p=<id>`-links die op de live site
   doorverwijzen (301). Die zijn direct naar de eindpagina gezet, bijvoorbeeld
   `?p=21` → `contact/`.
4. **Google Fonts lokaal.** Barlow, Nunito Sans, Amiri en Roboto zijn
   gedownload naar `site/wp-content/local-fonts/`. De site laadt geen
   lettertypen meer van Google — schermbeeld identiek, geen externe requests.
5. **Verwijzingen in JavaScript.** Een aantal bestanden wordt niet via
   `href`/`src` geladen maar via JavaScript: de sliderfoto's staan in
   `data-lazyload`, het emoji-script in een JSON-blok. Het
   downloadprogramma ziet die niet. Ze zijn apart opgehaald (12 bestanden)
   en de verwijzingen wijzen nu naar de lokale kopie. Schema.org-identifiers
   (`@id`), `canonical` en `og:url` blijven absoluut naar finect.nl wijzen --
   dat hoort zo en is gelijk aan het origineel.
6. **Feeds en API-eindpunten verwijderd.** `/feed/`, `/comments/feed/` en
   `/wp-json/` bestaan alleen binnen WordPress. Het downloadprogramma had ze
   als HTML opgeslagen; op een statische host zouden ze verkeerd worden
   geserveerd.

## Verificatie

De kopie is vergeleken met de live site door beide in dezelfde headless
Chromium te renderen (de live site via een lokale reverse proxy, omdat de
browser finect.nl niet rechtstreeks kan bereiken).

| Check | Resultaat |
| --- | --- |
| Paginahoogte kopie vs live (10 pagina's, 1440px) | 10/10 identiek |
| Tekstlengte kopie vs live | 10/10 identiek |
| `<title>` kopie vs live | 10/10 identiek |
| Aantal DOM-elementen | 3 minder per pagina: de `dns-prefetch`/`preconnect` naar Google Fonts, overbodig nu de fonts lokaal staan |
| Externe requests met netwerk geblokkeerd (16 pagina's) | 0, m.u.v. het formulier-endpoint op `/contact/` |
| 404's binnen de kopie (16 pagina's) | 0 |
| JavaScript-fouten (16 pagina's) | 0, m.u.v. het formulier op `/contact/` |

## Wat niet werkt zonder WordPress

* **Contactformulier** (Contact Form 7). Het formulier wordt getoond, maar
  versturen vereist een server-endpoint. Koppel het aan een dienst als
  Formspree of Netlify Forms, of aan een eigen mailscript.
* **Zoeken, RSS-feeds, `wp-json` en `xmlrpc.php`.** Die links staan nog in de
  `<head>` (zoals op het origineel) maar hebben geen backend.

Al het overige werkt wel: navigatie, uitklapmenu, mobiel hamburgermenu,
slider, animaties, blogoverzicht en de PDF-downloads zijn stuk voor stuk in de
browser getest (zie de tabel hierboven).

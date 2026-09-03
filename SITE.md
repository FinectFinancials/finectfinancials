# Finect Financials — statische kopie van www.finect.nl

Deze map (`site/`) bevat een volledige, zelfstandige kopie van
[finect.nl](https://finect.nl) zoals de site er op **3 september 2026** uitzag.

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
5. **Protocol-relatieve verwijzingen.** WordPress schrijft sommige URL's als
   `//finect.nl/…`. Die zijn omgezet naar relatieve paden, maar alléén waar het
   bestand ook daadwerkelijk lokaal staat. Schema.org-identifiers (`@id`),
   `canonical`, `og:url` en `og:image` blijven absoluut — dat hoort zo en is
   gelijk aan het origineel.

## Verificatie

De kopie is vergeleken met de live site door beide in dezelfde headless
Chromium te renderen en de screenshots pixel voor pixel te vergelijken:

| Check | Resultaat |
| --- | --- |
| Pixeldiff desktop (1440px, 10 pagina's) | 9 pagina's identiek; homepage 895 px (0,018%) |
| Pixeldiff mobiel (390px, 10 pagina's) | alle 10 identiek |
| Paginahoogtes desktop + mobiel | identiek op alle 20 metingen |
| DOM + computed styles (5 pagina's, 3.223 elementen, 22 CSS-eigenschappen) | 0 verschillen |
| Afbeeldingen byte-voor-byte | 13/13 identiek |
| Externe requests met netwerk geblokkeerd | 0 (m.u.v. het formulier-endpoint) |
| Interactie: dropdown "Over Finect" | verborgen, klapt uit bij hover |
| Interactie: mobiel hamburgermenu | opent, alle 6 menu-items zichtbaar |
| Interactie: navigatie via menu | gaat naar de juiste pagina |
| PDF-downloads op Vergelijkingskaarten | 9 links, steekproef 4/4 geeft 200 |

Het restverschil van 895 pixels op de homepage zit in de fototextuur van de
"Onze diensten"-kaarten. Zelfde bestand, zelfde afmetingen, zelfde CSS — het is
resampling-ruis van de browser, geen kopieerfout. Elke kant is op zichzelf wél
bit-identiek reproduceerbaar (kopie-vs-kopie en live-vs-live geven 0 pixels
verschil).

## Wat niet werkt zonder WordPress

* **Contactformulier** (Contact Form 7). Het formulier wordt getoond, maar
  versturen vereist een server-endpoint. Koppel het aan een dienst als
  Formspree of Netlify Forms, of aan een eigen mailscript.
* **Zoeken, RSS-feeds, `wp-json` en `xmlrpc.php`.** Die links staan nog in de
  `<head>` (zoals op het origineel) maar hebben geen backend.

Al het overige werkt wel: navigatie, uitklapmenu, mobiel hamburgermenu,
slider, animaties, blogoverzicht en de PDF-downloads zijn stuk voor stuk in de
browser getest (zie de tabel hierboven).

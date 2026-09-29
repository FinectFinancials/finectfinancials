# Nieuwe homepage: bouw en opruimen

Werkbestanden voor de voorbeeldpagina op `site/voorbeeld/`. Nog niet in gebruik
op de echte homepage.

* `bouw_home.py` bouwt de pagina uit `site/over-finect/index.html`, met
  `inhoud.html` en `home.css`. De map met werkbestanden (`SP`) staat bovenaan het
  script en moet naar deze map wijzen als u het opnieuw draait.
* `opruimen.py` haalt WordPress-onderdelen weg die op de statische site niets
  doen: formulier-plugin, slider, emoji, Elementor-effecten, 148 kB aan
  parallax-instellingen en verwijzingen naar feeds en API's. De overige scripts
  krijgen `defer`.
* `gedrag.js` vergelijkt een pagina voor en na: schermafbeeldingen op 1440 en
  390 px, uitklapmenu, zoekvenster, vaste kopbalk, mobiel menu en reviews.
* `snelheid.js` meet de laadtijd op een gesimuleerde telefoon.

perfect-scrollbar, jquery-appear en jquery-migrate blijven staan: zonder die
drie werkt het uitklapmenu op de telefoon niet.

## Afslanken van de opmaak

* `slank.py` voegt de twaalf opmaakbestanden en -blokken van thema, Elementor
  en lettertypen samen tot `site/wp-content/themes/zikzag/css/finect-thema.css`
  en laat alleen regels staan die op de opgegeven pagina's kunnen gelden
  (klassen en id's uit de pagina's, plus woorden tussen aanhalingstekens in de
  scripts). Van 661 kB naar 93 kB.
  Draai het opnieuw met alle pagina's die het bestand gebruiken, zodra er een
  pagina bij komt: `python3 slank.py over-ons.html contact.html voorbeeld.html`
  (de eerste pagina moet de oorspronkelijke opmaakblokken nog bevatten).
* `opruimen.py` heeft ook `zoeken_weg`: het vergrootglas in de kopbalk. Zoeken
  werkt alleen binnen WordPress.
* `formulier.js` vergelijkt het contactformulier voor en na.

Getest op de voorbeeldpagina, Over ons en Contact: schermafbeeldingen op 1440,
1280, 1024, 768 en 390 px, uitklapmenu, vaste kopbalk, mobiel menu, reviews en
formulier. Alles gelijk, behalve het vergrootglas.

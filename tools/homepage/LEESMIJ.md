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

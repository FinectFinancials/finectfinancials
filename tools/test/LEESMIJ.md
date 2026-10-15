# Testscripts

Draaien tegen een lokale server: `cd site && python3 -m http.server 8099`.

- `foto.js <pad> <naam>`: schermafbeeldingen op 1440 en 390 pixels, met js-fouten, kapotte bestanden en horizontale overloop.
- `axe.js <pad>`: toegankelijkheidscontrole. Zet eerst `axe.min.js` ernaast:
  `curl -o axe.min.js https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.2/axe.min.js`
- `snel.js <pad>`: laadtijd op een trage mobiele verbinding (FCP, LCP, kB).
- `hypcheck.js`: klikt de hypotheekcheck op /voorbeeld/hypotheken/ door en controleert links en ankers.
- `startcheck.js [pad]`: rekent de rekenhulp op Eerste huis kopen door met vaste gevallen, en controleert de partnervraag, het toetsenbord, ankers en links.
- `elfoto.js <pad> <selector> <breedte> <naam>`: schermafbeelding van één element, bijvoorbeeld een rekenhulp.

Nodig voor de bouwscripts: `pip install tinycss2 beautifulsoup4 lxml pillow`.
De bouwscripts verwachten de werkmap uit `tools/` (zie de paden bovenin elk script).
Voor `tools/hypotheken/bouw_start.py` horen `start.html` en `start.css` in de werkmap in `hypstart/`, naast `hyp/hyp.css`.

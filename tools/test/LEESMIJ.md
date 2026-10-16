# Testscripts

Draaien tegen een lokale server: `cd site && python3 -m http.server 8099`.

- `foto.js <pad> <naam>`: schermafbeeldingen op 1440 en 390 pixels, met js-fouten, kapotte bestanden en horizontale overloop.
- `axe.js <pad>`: toegankelijkheidscontrole. Zet eerst `axe.min.js` ernaast:
  `curl -o axe.min.js https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.2/axe.min.js`
- `snel.js <pad>`: laadtijd op een trage mobiele verbinding (FCP, LCP, kB).
- `hypcheck.js`: klikt de hypotheekcheck op /voorbeeld/hypotheken/ door en controleert links en ankers.
- `startcheck.js [pad]`: rekent de rekenhulp op Eerste huis kopen door met vaste gevallen, en controleert de partnervraag, het toetsenbord, ankers en links.
- `subcheck.js [voorbeeld/]`: rekent de rekenhulpen op Oversluiten, Volgend huis kopen en Zzp door, en controleert de check op Hypotheken en alle links en ankers op de vijf hypotheekpagina's.
- `elfoto.js <pad> <selector> <breedte> <naam>`: schermafbeelding van één element, bijvoorbeeld een rekenhulp.

Nodig voor de bouwscripts: `pip install tinycss2 beautifulsoup4 lxml pillow`.
De bouwscripts verwachten de werkmap uit `tools/` (zie de paden bovenin elk script).
Voor `tools/hypotheken/bouw_hypsub.py` horen de subpagina's (`start.html`, `volgend.html`, `oversluiten.html`, `zzp.html`) en `sub.css` in de werkmap in `hypsub/`; `bouw_hyp.py`, `inhoud.html`, `hyp.css` en `menu_hyp.py` in `hyp/`.
Let op: `inhoud.html` van Hypotheken linkt naar de subpagina's. Bouw de hoofdpagina dus pas live samen met `bouw_hypsub.py live`, en zet dan met `menu_hyp.py` de uitklaplijst op alle pagina's.

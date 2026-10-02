# -*- coding: utf-8 -*-
"""Stap 1: de oude WordPress-pagina's technisch opruimen, zonder de inhoud te veranderen.

Per pagina:
  - WordPress-restjes, slider, emoji, contactformulier en Elementor-scripts weg (opruimen.py)
  - de scripts van Revolution Slider weg (er staat op geen enkele pagina een slider)
  - de zoekknop weg, inzoomen weer toegestaan, links met een slash
  - het logo van 452 kB vervangen door hetzelfde logo op de juiste maat, met alt-tekst
  - alt-tekst bij de logo's van CFP en Wft in de voettekst
  - de losse opmaakbestanden vervangen door finect-thema-oud.css: dezelfde aanpak als finect-thema.css
    van de nieuwe pagina's, maar een eigen bestand, zodat de nieuwe pagina's pixel voor pixel gelijk blijven
    (maken: slank.py met UIT=finect-thema-oud.css en schoon/over-finect.html + alle oude pagina's)
Extra:
  - elementor-4497 (oude 'Particuliere verzekeringen') verwijst door naar /verzekeringen/
  - auteurs- en categoriepagina's: noindex, follow (dunne overzichtspagina's)
  - de twee artikelen krijgen een omschrijving voor Google

Gebruik:
  python3 opruim_oud.py voorbeeld hypotheken zakelijk   -> site/voorbeeld/<pad>/index.html
  python3 opruim_oud.py live                            -> alle oude pagina's op hun eigen plek
"""
import glob, html, io, os, re, sys

HOME = os.path.dirname(os.path.abspath(__file__)) + '/'
sys.path.insert(0, HOME)
from opruimen import opruimen, zoeken_weg, kleine_punten, links_en_voettekst, weg  # noqa: E402
from slank import pagina_aanpassen  # noqa: E402

NIEUW = ('index.html', 'verzekeringen/', 'voorbeeld/')
OMSCHRIJVING = {
    'huis/woonhuis-en-energielabel/':
        'Wat betekent het energielabel voor de waarde van uw woning en hoeveel u kunt lenen? '
        'Fred Koeling van Finect Financials in Apeldoorn legt het uit.',
    'ondernemer/het-betaalbaar-houden-van-de-arbeidsongeschiktheidsverzekering-aov/':
        'Tips om uw arbeidsongeschiktheidsverzekering (AOV) betaalbaar te houden: verzekerd bedrag, '
        'eigen risico en sluimerdekking. Advies van Finect Financials.',
}
NOINDEX = ('author/', 'category/')
DOORVERWIJZEN = {'elementor-4497/': 'verzekeringen/'}


def oude_paginas():
    uit = []
    for p in glob.glob('site/**/index.html', recursive=True):
        r = p[len('site/'):]
        if r.startswith(NIEUW):
            continue
        uit.append(r[:-len('index.html')])
    return sorted(uit)


def schoon(t, pad):
    d = '../' * pad.count('/')
    t, _ = opruimen(t)
    for p in (r"<link rel='stylesheet' id='rs-plugin-settings-css'[^>]*/>\n?",
              r'<script[^>]*id="tp-tools-js"[^>]*></script>\n?',
              r'<script[^>]*id="revmin-js"[^>]*></script>\n?'):
        t, k = weg(t, p)
        assert k in (0, 1), (pad, p)   # bij Over ons en Contact was de slider al weg
    t, n = zoeken_weg(t)
    assert n == 3, (pad, n)
    t = kleine_punten(t)
    t, _ = links_en_voettekst(t)
    # logo: het bestand van 1181 bij 658 pixels (452 kB) werd op 60 pixels hoog getoond
    t, n = re.subn(r'src="((?:\.\./)*)wp-content/uploads/2020/04/logofinect\.png" alt=""  style="height:(\d+)px;"',
                   r'src="\1wp-content/uploads/finect/finect-logo.png" alt="Finect Financials" width="323" height="180" '
                   r'style="height:\2px;width:auto;"', t)
    t, m = re.subn(r'src="((?:\.\./)*)wp-content/uploads/2020/04/finect-financials-logo-retina\.png" alt=""  style="height:(\d+)px;"',
                   r'src="\1wp-content/uploads/2020/04/finect-financials-logo-retina.png" alt="Finect Financials" width="186" '
                   r'height="100" style="height:\2px;width:auto;"', t)
    assert (n, m) in ((3, 1), (0, 0)), (pad, n, m)
    t = re.sub(r'(src="(?:\.\./)*wp-content/uploads/2022/04/cfp_0\.png" class="[^"]*") alt=""', r'\1 alt="Certified Financial Planner"', t)
    t = re.sub(r'(src="(?:\.\./)*wp-content/uploads/2022/04/OIP-1\.jpg" class="[^"]*") alt=""', r'\1 alt="Wft vakbekwaamheid"', t)
    # eigen lichte opmaakbestand voor de oude pagina's; finect-thema.css van de nieuwe pagina's blijft ongemoeid
    t = pagina_aanpassen(t, d)
    t, k = re.subn(r"id='finect-thema-css' href='((?:\.\./)*)wp-content/themes/zikzag/css/finect-thema\.css'",
                   r"id='finect-thema-oud-css' href='\1wp-content/themes/zikzag/css/finect-thema-oud.css'", t)
    assert k == 1, pad
    # omschrijving voor Google
    if pad in OMSCHRIJVING and '<meta name="description"' not in t:
        t = t.replace('</title>', '</title>\n<meta name="description" content="' + html.escape(OMSCHRIJVING[pad]) + '" />', 1)
    # dunne overzichtspagina's niet in Google, links wel volgen
    if pad.startswith(NOINDEX):
        t, k = re.subn(r"<meta name='robots' content='[^']*' />", "<meta name='robots' content='noindex, follow' />", t)
        assert k == 1, pad
    # oude dubbele pagina: doorsturen naar de nieuwe
    if pad in DOORVERWIJZEN:
        doel = DOORVERWIJZEN[pad]
        t, k = re.subn(r"<meta name='robots' content='[^']*' />", "<meta name='robots' content='noindex, follow' />", t)
        assert k == 1
        t, k = re.subn(r'<link rel="canonical" href="[^"]*" />', '<link rel="canonical" href="https://finect.nl/' + doel + '" />', t)
        assert k == 1
        t = t.replace('<head>', '<head>\n<meta http-equiv="refresh" content="0; url=' + d + doel + '">', 1)
    return t


def voorbeeld(t, pad):
    """zelfde pagina, maar onder /voorbeeld/: een map dieper, niet in Google, met de balk onderin"""
    t = t.replace('../', '../../')
    t = re.sub(r'\s*<link rel="canonical" href="[^"]*" />', '', t, count=1)
    t = re.sub(r"<meta name='robots' content='[^']*' />", "<meta name='robots' content='noindex, nofollow' />", t, count=1)
    t = t.replace('<title>', '<title>VOORBEELD | ', 1)
    banier = ('<div id="fxBanier" style="position:fixed;left:0;right:0;bottom:0;z-index:99999;background:#b5004a;color:#fff;'
              'font-family:Barlow,Arial,sans-serif;font-size:14px;line-height:1.45;padding:10px 16px;text-align:center;">'
              'Voorbeeld: dezelfde pagina, technisch opgeschoond en sneller. Deze pagina staat niet in Google.</div>\n')
    return t.replace('</body>', banier + '</body>', 1)


if __name__ == '__main__':
    modus = sys.argv[1]
    paden = [p.strip('/') + '/' for p in sys.argv[2:]] or oude_paginas()
    for pad in paden:
        bron = 'site/' + pad + 'index.html'
        t = io.open(bron, encoding='utf-8').read()
        assert 'finect-thema.css' not in t, ('al opgeschoond', pad)
        nieuw = schoon(t, pad)
        if modus == 'voorbeeld':
            doel = 'site/voorbeeld/' + pad + 'index.html'
            nieuw = voorbeeld(nieuw, pad)
        else:
            doel = bron
        os.makedirs(os.path.dirname(doel), exist_ok=True)
        io.open(doel, 'w', encoding='utf-8').write(nieuw)
        print('%-90s %4d -> %4d kB' % (doel, len(t.encode()) // 1024, len(nieuw.encode()) // 1024))

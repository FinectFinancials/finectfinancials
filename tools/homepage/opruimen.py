# -*- coding: utf-8 -*-
"""Haalt WordPress-onderdelen weg die op de statische site niets doen.

Gebruik: python3 opruimen.py BRON DOEL [groep ...]
Zonder groepen worden alle groepen toegepast.
"""
import io, re, sys

def weg(t, patroon, n=None, flags=re.S):
    t2, k = re.subn(patroon, '', t, flags=flags)
    if n is not None:
        assert k == n, (k, n, patroon[:70])
    return t2, k

def tag_link(id_):   # <link ... id='x' ...>
    return r"<link rel='stylesheet' id='" + re.escape(id_) + r"'[^>]*/>\n?"

def script_src(id_):
    return r'<script id="' + re.escape(id_) + r'" src="[^"]*"></script>\n?'

def script_inline(id_):
    return r'<script id="' + re.escape(id_) + r'"[^>]*>.*?</script>\n?'

def style_inline(id_):
    return r'<style id="' + re.escape(id_) + r'"[^>]*>.*?</style>\n?'

GROEPEN = {
    # verwijzingen naar WordPress-adressen die op de statische site niet bestaan
    'kop': [
        r'<link rel="alternate" type="application/rss\+xml"[^>]*/>\n?',
        r'<link rel="alternate" title="oEmbed[^>]*/>\n?',
        r'<link rel="https://api\.w\.org/"[^>]*/>',
        r'<link rel="alternate" title="JSON" type="application/json"[^>]*/>',
        r'<link rel="EditURI"[^>]*/>',
        r'<meta name="generator"[^>]*/>\n?',
    ],
    # stijlen voor WordPress-blokken, emoji en de oude slider
    'wpstijl': [
        style_inline('wp-img-auto-sizes-contain-inline-css'),
        style_inline('wp-emoji-styles-inline-css'),
        style_inline('wp-block-library-inline-css'),
        style_inline('classic-theme-styles-inline-css'),
        style_inline('global-styles-inline-css'),
        style_inline('rs-plugin-settings-inline-css'),
    ],
    # het contactformulier van WordPress; er staat geen formulier op deze pagina
    'formulier': [
        tag_link('contact-form-7-css'),
        script_src('swv-js'),
        script_inline('contact-form-7-js-extra'),
        script_src('contact-form-7-js'),
    ],
    # slider, emoji en lege scripts
    'slider': [
        r'<script>function setREVStartSize\(e\)\{.*?</script>\n?',
        r'<script id="wp-emoji-settings" type="application/json">.*?</script>\n?',
        r'<script type="module">\s*/\*! This file is auto-generated \*/.*?</script>\n?',
        r'<script id="wgl_custom_footer_js">\s*</script>\n?',
    ],
    # lettertypen werden vier keer aangeroepen; één keer is genoeg
    'fonts': [
        r'<link rel="preload" as="style" href="\.\./wp-content/local-fonts/gfonts-2\.css" />',
        r'<link rel="stylesheet" href="\.\./wp-content/local-fonts/gfonts-2\.css" media="print" onload="this\.media=\'all\'">',
        r'<noscript><link rel="stylesheet" href="\.\./wp-content/local-fonts/gfonts-2\.css" /></noscript>',
    ],
    # Elementor-onderdelen voor effecten die hier niet gebruikt worden
    'elementor': [
        tag_link('swiper-css'),
        tag_link('e-animations-css'),
        tag_link('elementor-icons-css'),
        script_inline('wgl-parallax-js-extra'),
        script_src('wgl-parallax-js'),
        script_src('wgl-column-js'),
        script_src('wgl-elementor-extensions-widgets-js'),
        script_src('elementor-webpack-runtime-js'),
        script_src('elementor-frontend-modules-js'),
        script_src('elementor-waypoints-js'),
        script_inline('jquery-ui-core-js-before'),
        script_src('jquery-ui-core-js'),
        script_src('swiper-js'),
        script_src('share-link-js'),
        script_src('elementor-dialog-js'),
        script_inline('elementor-frontend-js-before'),
        script_src('elementor-frontend-js'),
        script_src('preloaded-modules-js'),
    ],
    # let op: perfect-scrollbar, jquery-appear en jquery-migrate blijven staan;
    # zonder die drie werkt het uitklapmenu op de telefoon niet meer
}

def div_weg(t, begin):
    """haalt elke <div> weg die begint met `begin`, inclusief alles wat erin staat"""
    n = 0
    while True:
        a = t.find(begin)
        if a < 0:
            return t, n
        diep, i = 0, a
        for m in re.finditer(r'<div\b|</div>', t[a:]):
            diep += 1 if m.group(0) == '<div' else -1
            if diep == 0:
                i = a + m.end()
                break
        assert diep == 0, 'div niet gesloten'
        t = t[:a] + t[i:]
        n += 1


def zoeken_weg(t):
    # zoeken werkt alleen binnen WordPress; op de statische site kwam een
    # bezoeker gewoon op de homepage uit
    t, n = div_weg(t, '<div class="header_search search_alt"')
    return t, n


def kleine_punten(t):
    """drie kleine verbeteringen uit de SEO-analyse"""
    # 1. inzoomen weer toestaan (het thema blokkeerde het met maximum-scale=1)
    oud = '<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">'
    assert t.count(oud) == 1
    t = t.replace(oud, '<meta name="viewport" content="width=device-width, initial-scale=1">')
    # 2. postcode overal op dezelfde manier, zoals bij de KvK: met spatie
    t = t.replace('7317AH Apeldoorn', '7317 AH Apeldoorn')
    # 3. het telefoonnummer in de voettekst is geen kopje; zelfde uiterlijk als eerst
    oud = '<h3 class="wgl-infobox_title">+31 6 30 67 97 90</h3>'
    if oud in t:
        t = t.replace(oud, '<p class="wgl-infobox_title fx-voet-tel">+31 6 30 67 97 90</p>')
        t = t.replace('</head>', '<style id="fx-voet-css">.wgl-infobox .fx-voet-tel{display:block;'
                      'font-family:Barlow,Arial,sans-serif;font-size:24px;font-weight:400;line-height:1.4;'
                      'letter-spacing:-.5px;color:#fff;margin:0 0 4px;padding:0;}</style>\n</head>', 1)
    return t


def opruimen(t, groepen=None, uitstellen=True):
    verslag = {}
    for g in (groepen or GROEPEN):
        for p in GROEPEN[g]:
            t, k = weg(t, p)
            verslag[p[:60]] = k
    if uitstellen:
        # de overgebleven scripts pas na het tekenen van de pagina uitvoeren;
        # defer houdt de volgorde gelijk, dus jQuery blijft als eerste
        t, k = re.subn(r'<script id="([^"]+)" src="([^"]+)"></script>',
                       r'<script id="\1" src="\2" defer></script>', t)
        verslag['defer'] = k
    return t, verslag

if __name__ == '__main__':
    bron, doel = sys.argv[1], sys.argv[2]
    groepen = sys.argv[3:] or None
    t = io.open(bron, encoding='utf-8').read()
    t2, v = opruimen(t, groepen)
    for p, k in v.items():
        if k != 1: print('  let op:', k, 'x', p)
    io.open(doel, 'w', encoding='utf-8').write(t2)
    print(f'{len(t)} -> {len(t2)} tekens')

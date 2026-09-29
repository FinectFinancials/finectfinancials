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

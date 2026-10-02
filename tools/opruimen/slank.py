# -*- coding: utf-8 -*-
"""Voegt de opmaak van thema, Elementor en lettertypen samen tot één bestand
en laat alleen de regels staan die op de opgegeven pagina's kunnen gelden.

Een regel blijft staan als elke klasse en elk id in de selector ergens in de
pagina's of in de scripts voorkomt, en elke elementnaam echt op een pagina
staat. Dat is ruim genomen: bij twijfel blijft een regel staan.

Gebruik: python3 slank.py pagina.html [pagina.html ...]
Schrijft site/wp-content/themes/zikzag/css/finect-thema.css
"""
import io, os, re, sys
import tinycss2
from bs4 import BeautifulSoup

SITE = 'site'
UIT = os.path.join(SITE, 'wp-content/themes/zikzag/css/finect-thema.css')

# in deze volgorde stonden ze in de pagina; de volgorde bepaalt welke regel wint
BRONNEN = [
    ('link', 'wp-content/themes/zikzag/style.css@ver=e4a7e9cec77071ae7a53fbce4b4e64aa.css'),
    ('link', 'wp-content/themes/zikzag/fonts/flaticon/flaticon.css@ver=e4a7e9cec77071ae7a53fbce4b4e64aa.css'),
    ('link', 'wp-content/themes/zikzag/css/main.css@ver=e4a7e9cec77071ae7a53fbce4b4e64aa.css'),
    ('style', 'zikzag-main-inline-css'),
    ('link', 'wp-content/plugins/elementor/assets/css/frontend-legacy.min.css@ver=3.11.3.css'),
    ('link', 'wp-content/plugins/elementor/assets/css/frontend.min.css@ver=3.11.3.css'),
    ('style', 'elementor-frontend-inline-css'),
    ('link', 'wp-content/uploads/elementor/css/post-1.css@ver=1678278600.css'),
    ('link', 'wp-content/uploads/elementor/css/global.css@ver=1678278601.css'),
    ('link', 'wp-content/uploads/elementor/css/post-3272.css@ver=1678282298.css'),
    ('link', 'wp-content/uploads/elementor/css/post-475.css@ver=1733826303.css'),
    ('link', 'wp-content/local-fonts/gfonts-2.css'),
    ('style', 'wp-custom-css'),
    ('style', 'zikzag_set-dynamic-css'),
]
SCRIPTS = [
    'wp-includes/js/jquery/jquery.min.js@ver=3.7.1',
    'wp-content/themes/zikzag/js/theme-addons.js@ver=1.2.2',
    'wp-content/themes/zikzag/js/theme.js@ver=1.2.2',
    'wp-content/themes/zikzag/js/perfect-scrollbar.min.js@ver=1.0.0',
    'wp-content/themes/zikzag/js/jquery.appear.js@ver=1.0.0',
]


def inline_style(html, id_):
    m = re.search(r'<style id="' + re.escape(id_) + r'"[^>]*>(.*?)</style>', html, re.S)
    assert m, id_
    return m.group(1)


def urls_herschrijven(css, bronmap):
    """url(...) in een bronbestand laten wijzen vanaf de plek van het nieuwe bestand."""
    uitmap = os.path.dirname(UIT)
    def fix(m):
        q, u = m.group(1), m.group(2).strip()
        if re.match(r'(data:|https?:|//|#)', u):
            return m.group(0)
        pad, _, rest = u.partition('?')
        pad, _, frag = pad.partition('#')
        doel = os.path.normpath(os.path.join(bronmap, pad))
        nieuw = os.path.relpath(doel, uitmap).replace(os.sep, '/')
        if frag:
            nieuw += '#' + frag
        return 'url(' + q + nieuw + q + ')'
    return re.sub(r'url\(\s*([\'"]?)([^\'")]+)\1\s*\)', fix, css)


def tokens_verzamelen(paginas):
    """klassen en id's uit de pagina's, plus alle woorden tussen aanhalingstekens
    in de scripts (daar zitten de klassen die scripts later toevoegen)"""
    woorden, tags = set(), {'html', 'body', '*'}
    for p in paginas:
        t = io.open(p, encoding='utf-8').read()
        soep = BeautifulSoup(t, 'lxml')
        for el in soep.find_all(True):
            tags.add(el.name.lower())
            woorden.update(el.get('class', []))
            if el.get('id'):
                woorden.add(el['id'])
        for sc in soep.find_all('script'):
            woorden |= set(re.findall(r'[A-Za-z0-9_-]+', sc.get_text()))
    for s in SCRIPTS:
        js = io.open(os.path.join(SITE, s), encoding='utf-8', errors='ignore').read()
        for lit in re.findall(r'"([^"\n]*)"|\'([^\'\n]*)\'', js):
            woorden |= set(re.findall(r'[A-Za-z0-9_-]+', lit[0] or lit[1]))
    # elementen die scripts of de browser zelf kunnen toevoegen
    tags |= {'svg', 'path', 'iframe', 'img', 'span', 'div', 'a', 'input', 'button', 'ul', 'li'}
    return woorden, tags


def selector_nodig(sel, woorden, tags):
    if '\\' in sel:
        return True
    s = sel
    # :not(...) en soortgelijke hoeven niet op de pagina te staan
    for _ in range(3):
        s = re.sub(r':(not|is|where|has|matches|-webkit-any|-moz-any)\([^()]*\)', '', s)
    s = re.sub(r'\[[^\]]*\]', '', s)           # attribuutselectors: ruim nemen
    s = re.sub(r'::?[a-zA-Z-]+(\([^()]*\))?', '', s)  # :hover, ::before, :nth-child(2)
    for k in re.findall(r'\.([A-Za-z0-9_-]+)', s):
        if k not in woorden:
            return False
    for i in re.findall(r'#([A-Za-z0-9_-]+)', s):
        if i not in woorden:
            return False
    zonder = re.sub(r'[.#][A-Za-z0-9_-]+', ' ', s)
    for tag in re.findall(r'(?<![A-Za-z0-9_-])([A-Za-z][A-Za-z0-9-]*)', zonder):
        if tag.lower() not in tags:
            return False
    return True


def kort(s):
    s = re.sub(r'\s+', ' ', s).strip()
    s = re.sub(r'\s*([{};,>])\s*', r'\1', s)
    return s


def regels_filteren(regels, woorden, tags, stats):
    uit = []
    for r in regels:
        if r.type == 'qualified-rule':
            prelude = tinycss2.serialize(r.prelude).strip()
            stats['regels'] += 1
            if prelude.startswith(('from', 'to')) or re.match(r'^[\d.]+%', prelude):
                uit.append(prelude + '{' + tinycss2.serialize(r.content) + '}')
                continue
            delen = [d.strip() for d in split_selectors(prelude)]
            bewaard = [d for d in delen if selector_nodig(d, woorden, tags)]
            if bewaard:
                stats['bewaard'] += 1
                uit.append(','.join(bewaard) + '{' + tinycss2.serialize(r.content) + '}')
        elif r.type == 'at-rule':
            naam = r.lower_at_keyword
            prelude = tinycss2.serialize(r.prelude).strip()
            if naam in ('media', 'supports', 'document', '-moz-document'):
                binnen = tinycss2.parse_rule_list(r.content, skip_comments=True, skip_whitespace=True)
                inhoud = regels_filteren(binnen, woorden, tags, stats)
                if inhoud:
                    uit.append('@' + naam + ' ' + prelude + '{' + ''.join(inhoud) + '}')
            elif naam == 'charset':
                continue
            else:  # font-face, keyframes, import: eerst bewaren, straks schiften
                uit.append('@' + naam + (' ' + prelude if prelude else '') +
                           ('{' + tinycss2.serialize(r.content) + '}' if r.content is not None else ';'))
    return uit


def split_selectors(prelude):
    delen, diep, huidig = [], 0, ''
    for ch in prelude:
        if ch in '([':
            diep += 1
        elif ch in ')]':
            diep -= 1
        if ch == ',' and diep == 0:
            delen.append(huidig); huidig = ''
        else:
            huidig += ch
    delen.append(huidig)
    return delen


def ongebruikte_at_regels(css):
    """keyframes en font-face die nergens meer genoemd worden, weghalen"""
    for _ in range(2):
        rest = re.sub(r'@(-webkit-|-moz-|-o-)?keyframes\s+[^{]+\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}', '', css)
        rest = re.sub(r'@font-face\{[^{}]*\}', '', rest)
        def kf(m):
            naam = m.group(2).strip().strip('"\'')
            return m.group(0) if re.search(r'(?<![A-Za-z0-9_-])' + re.escape(naam) + r'(?![A-Za-z0-9_-])', rest) else ''
        css = re.sub(r'@(-webkit-|-moz-|-o-)?keyframes\s+([^{]+)\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}', kf, css)
        def ff(m):
            fam = re.search(r'font-family:\s*([^;}]+)', m.group(0))
            if not fam:
                return m.group(0)
            naam = fam.group(1).strip().strip('"\'')
            return m.group(0) if naam.lower() in rest.lower() else ''
        css = re.sub(r'@font-face\{[^{}]*\}', ff, css)
    return css


def main(paginas):
    woorden, tags = tokens_verzamelen(paginas)
    eerste = io.open(paginas[0], encoding='utf-8').read()
    stukken, voor_totaal = [], 0
    stats = {'regels': 0, 'bewaard': 0}
    for soort, bron in BRONNEN:
        if soort == 'link':
            css = io.open(os.path.join(SITE, bron), encoding='utf-8').read()
            css = urls_herschrijven(css, os.path.dirname(os.path.join(SITE, bron)))
        else:
            css = inline_style(eerste, bron)
            # inline opmaak stond in de pagina zelf, die een map diep staat
            css = urls_herschrijven(css, os.path.join(SITE, 'voorbeeld'))
        voor_totaal += len(css)
        regels = tinycss2.parse_stylesheet(css, skip_comments=True, skip_whitespace=True)
        stukken.append('/* ' + bron.split('/')[-1].split('@')[0] + ' */\n' +
                       ''.join(kort(x) for x in regels_filteren(regels, woorden, tags, stats)))
    css = ongebruikte_at_regels('\n'.join(stukken))
    os.makedirs(os.path.dirname(UIT), exist_ok=True)
    io.open(UIT, 'w', encoding='utf-8').write(css + '\n')
    print(f'{voor_totaal} -> {len(css)} tekens, {stats["bewaard"]} van {stats["regels"]} regels bewaard')


def pagina_aanpassen(html, diepte='../'):
    """de losse opmaakbestanden en blokken vervangen door het ene nieuwe bestand"""
    eerste = None
    for soort, bron in BRONNEN:
        if soort == 'link':
            pat = r"<link rel='stylesheet' id='[^']*' href='" + re.escape(diepte + bron) + r"' media='all' />\n?"
            if bron.endswith('gfonts-2.css'):
                pat = r"<link rel='stylesheet' id='google-fonts-1-css' href='" + re.escape(diepte + bron) + r"' media='all' />\n?"
        else:
            pat = r'<style id="' + re.escape(bron) + r'"[^>]*>.*?</style>\n?'
        m = re.search(pat, html, re.S)
        assert m, bron
        if eerste is None:
            eerste = m.start()
        html = html[:m.start()] + html[m.end():]
    nieuw = ("<link rel='stylesheet' id='finect-thema-css' href='" + diepte +
             "wp-content/themes/zikzag/css/finect-thema.css' media='all' />\n")
    return html[:eerste] + nieuw + html[eerste:]


if __name__ == '__main__':
    main(sys.argv[1:])

# -*- coding: utf-8 -*-
"""Bouwt de pagina Zakelijk en de subpagina's (gemaakt op basis van bouw_verz.py).

Gebruik:
  python3 bouw_zak.py voorbeeld   -> site/voorbeeld/zakelijk/... en site/voorbeeld/arbeidsongeschiktheidsverzekeringen-aov/
  python3 bouw_zak.py live        -> site/zakelijk/... en site/arbeidsongeschiktheidsverzekeringen-aov/

Basis is Over ons, net als de homepage: dezelfde kop, voettekst en opmaak.
Alle paden in de bron en in de inhoud gaan uit van een pagina die één map diep
staat (../). Voor dieper liggende pagina's worden ze aan het eind omgezet.
"""
import io, re, json, html, os, sys

HOME = '/tmp/claude-0/-home-user-finectfinancials/eb3bde67-f228-5f8e-b9ee-dcd3a00cb56a/scratchpad/home/'
SP = HOME + 'zak/'
VERZ = HOME + 'verz/'
sys.path.insert(0, HOME)
from opruimen import opruimen, zoeken_weg, kleine_punten, links_en_voettekst
from slank import pagina_aanpassen

MODUS = sys.argv[1] if len(sys.argv) > 1 else 'voorbeeld'
VOORBEELD = MODUS == 'voorbeeld'
BASIS = 'https://finect.nl/'
SRC = 'tools/basis/over-finect.html'   # vaste bouwbasis: Over ons zoals die was vóór het opschonen (stap 1)
GOOGLE = 'https://maps.app.goo.gl/CUqTeR8SEaGoE9rx9'

# ---------- iconen ----------
def svg(paden, maat=26, dikte=1.7):
    return (f'<svg width="{maat}" height="{maat}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="{dikte}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" '
            f'focusable="false">{paden}</svg>')
TEL = ('<path d="M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3.1 19.5 19.5 0 01-6-6A19.8 19.8 0 012.1 4.2 '
       '2 2 0 014.1 2h3a2 2 0 012 1.7c.1.9.4 1.8.7 2.7a2 2 0 01-.5 2.1L8.1 9.9a16 16 0 006 6l1.4-1.2a2 2 0 '
       '012.1-.5c.9.3 1.8.6 2.7.7a2 2 0 011.7 2z"/>')
ICONEN = {
    'ICO_SCHILD': svg('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>'),
    'ICO_CHECK': svg('<path d="M16 4h2a2 2 0 012 2v14a2 2 0 01-2 2H6a2 2 0 01-2-2V6a2 2 0 012-2h2"/>'
                     '<rect x="8" y="2" width="8" height="4" rx="1"/><path d="M9 14l2 2 4-4"/>'),
    'ICO_HUIS': svg('<path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><path d="M9 22V12h6v10"/>'),
    'ICO_VERGELIJK': svg('<path d="M12 3v18M5 7h14"/><path d="M5 7l-3 6a3 3 0 006 0z"/><path d="M19 7l-3 6a3 3 0 006 0z"/>'
                         '<path d="M8 21h8"/>'),
    'ICO_AUTO': svg('<path d="M5 17H3v-5l2-5h14l2 5v5h-2"/><path d="M3 12h18"/><circle cx="7.5" cy="17" r="2"/>'
                    '<circle cx="16.5" cy="17" r="2"/><path d="M9.5 17h5"/>'),
    'ICO_LEVEN': svg('<path d="M20.8 4.6a5.5 5.5 0 00-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 00-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 000-7.8z"/>'),
    'ICO_TEL26': svg(TEL),
    'ICO_HART': svg('<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>'),
    'ICO_BANK': svg('<path d="M20 10V7a2 2 0 00-2-2H6a2 2 0 00-2 2v3"/><path d="M2 12a2 2 0 014 0v3h12v-3a2 2 0 014 0v5H2z"/><path d="M5 17v2M19 17v2"/>'),
    'ICO_VLIEG': svg('<path d="M17.8 19.2L16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/>'),
    'ICO_BLOEM': svg('<circle cx="12" cy="9" r="3"/><path d="M12 2a3 3 0 010 4M12 16a3 3 0 010-4M5 9a3 3 0 014 0M19 9a3 3 0 00-4 0M12 12v10M8 18c2 0 4 1 4 4M16 18c-2 0-4 1-4 4"/>'),
    'ICO_GEBOUW': svg('<rect x="4" y="2" width="16" height="20" rx="1"/><path d="M9 22v-4h6v4M8 6h.01M12 6h.01M16 6h.01M8 10h.01M12 10h.01M16 10h.01M8 14h.01M12 14h.01M16 14h.01"/>'),
    'ICO_SLEUTEL': svg('<circle cx="7.5" cy="15.5" r="4.5"/><path d="M10.7 12.3L21 2M16 7l3 3M18 5l2 2"/>'),
    'ICO_GEZIN': svg('<path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/>'),
    'ICO_KOFFER': svg('<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v16"/>'),
    'ICO_TEL': svg(TEL, 20, 1.8),
    'ICO_MAIL': svg('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>', 20, 1.8),
    'ICO_PIN': svg('<path d="M21 10c0 6-9 12-9 12s-9-6-9-12a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/>', 20, 1.8),
    'ICO_WINKEL': svg('<path d="M3 9l1.5-5h15L21 9"/><path d="M3 9h18v1.5a3 3 0 01-6 0 3 3 0 01-6 0 3 3 0 01-6 0z"/><path d="M5 13v8h14v-8"/><path d="M10 21v-5h4v5"/>'),
    'ICO_BUS': svg('<path d="M2 17V7a2 2 0 012-2h11l5 5v7h-2"/><path d="M15 5v5h5"/><circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/><path d="M9 17h6"/>'),
    'ICO_GEREEDSCHAP': svg('<path d="M14.7 6.3a4 4 0 00-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 005.4-5.4l-2.5 2.5-2.4-.6-.6-2.4z"/>'),
    'ICO_EURO': svg('<path d="M18 7a7 7 0 100 10"/><path d="M4 10h10M4 14h10"/>'),
    'ICO_LAPTOP': svg('<rect x="4" y="4" width="16" height="11" rx="2"/><path d="M2 19h20"/>'),
    'ICO_SCHILD20': svg('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>', 20, 1.8),
    'ICO_KAART': svg('<path d="M1 6v16l7-4 8 4 7-4V2l-7 4-8-4-7 4z"/><path d="M8 2v16M16 6v16"/>', 20, 1.8),
}

# ---------- de pagina's ----------
BEELD = 'wp-content/uploads/finect/zak-held.jpg'
BEELD_M = 'wp-content/uploads/finect/zak-held-mobiel.jpg'
F = 'wp-content/uploads/finect/'
PAGINAS = [
    dict(pad='zakelijk/', bron='inhoud.html', held=True,
         titel='Zakelijke verzekeringen Apeldoorn | Finect Financials',
         beschr="Zakelijke verzekeringen voor ondernemers, zzp'ers en VvE's in Apeldoorn: aansprakelijkheid, AOV, "
                "bedrijfspand en bedrijfsauto. Eén vaste adviseur.",
         naam='Zakelijk', dienst='Verzekeringsadvies voor ondernemers', vragen=8),
    dict(pad='zakelijk/bedrijfsaansprakelijkheidsverzekering/', bron='avb.html', menu='Bedrijfsaansprakelijkheid',
         titel='Bedrijfsaansprakelijkheidsverzekering | Finect Apeldoorn',
         beschr="Wat dekt een bedrijfsaansprakelijkheidsverzekering (AVB), en wanneer heeft u ook beroepsaansprakelijkheid "
                "nodig? Uitleg en onafhankelijk advies in Apeldoorn.",
         naam='Bedrijfsaansprakelijkheid', dienst='Advies over bedrijfsaansprakelijkheidsverzekering', vragen=7, beeld=F + 'zak-avb.jpg'),
    dict(pad='arbeidsongeschiktheidsverzekeringen-aov/', bron='aov.html', menu='AOV voor ondernemers',
         titel="AOV voor zzp'ers en ondernemers | Finect Apeldoorn",
         beschr="Wat als u als ondernemer niet meer kunt werken? Uitleg over de AOV, wachttijd, verzekerd bedrag en de "
                "komende verplichte basisverzekering. Advies in Apeldoorn.",
         naam='AOV', dienst='Advies over arbeidsongeschiktheidsverzekering', vragen=7, beeld=F + 'zak-aov.jpg'),
    dict(pad='zakelijk/bedrijfspand-en-inventaris/', bron='pand.html', menu='Bedrijfspand en inventaris',
         titel='Bedrijfspand en inventaris verzekeren | Finect Apeldoorn',
         beschr="Uw bedrijfspand, inventaris, voorraad en inkomsten bij stilstand goed verzekerd. Uitleg over opstal, "
                "inventaris en bedrijfsschade, met advies in Apeldoorn.",
         naam='Bedrijfspand en inventaris', dienst='Advies over bedrijfspand, inventaris en bedrijfsschade', vragen=7, beeld=F + 'zak-pand.jpg'),
    dict(pad='zakelijk/bedrijfsautoverzekering/', bron='auto.html', menu='Bedrijfsauto en bestelbus',
         titel='Bedrijfsautoverzekering en bestelbus | Finect Apeldoorn',
         beschr="Een auto van de zaak, een bestelbus of een wagenpark verzekeren? Uitleg over dekking, gereedschap in "
                "de bus en een wagenparkpolis. Advies in Apeldoorn.",
         naam='Bedrijfsauto', dienst='Advies over bedrijfsautoverzekering', vragen=7, beeld=F + 'zak-auto.jpg'),
    dict(pad='zakelijk/vve-verzekering/', bron='vve.html', menu='VvE-verzekering',
         titel='VvE-verzekering in Apeldoorn: opstal en aansprakelijkheid',
         beschr="Welke verzekeringen heeft een VvE nodig? Opstal, aansprakelijkheid en bestuurders verzekerd, met "
                "een checklist voor het bestuur. Advies in Apeldoorn.",
         naam='VvE-verzekering', dienst='Advies over VvE-verzekeringen', vragen=7, beeld=F + 'de-pencil-apeldoorn.jpg'),
]
HOOFD = PAGINAS[0]

def schoon(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', s))).replace('\xad', '').strip()


def bouw(pg):
    t = io.open(SRC, encoding='utf-8').read()

    def vervang(oud, nieuw, n=1):
        nonlocal t
        assert t.count(oud) == n, (t.count(oud), oud[:80])
        t = t.replace(oud, nieuw)

    url = BASIS + pg['pad']
    inhoud = io.open(SP + pg['bron'], encoding='utf-8').read()
    # vaste balk onderin op mobiel: bellen en polischeck (op de polischeckpagina zelf: mailen)
    tweede = '<a href="mailto:info@finect.nl">{ICO_MAIL}Mail mij</a>'
    inhoud += ('\n  <div class="fx-verz__balk" role="region" aria-label="Direct contact">'
               '<a href="tel:+31630679790">{ICO_TEL}Bel mij</a>' + tweede + '</div>\n')
    for k, v in ICONEN.items():
        inhoud = inhoud.replace('{' + k + '}', v)
    assert not re.search(r'\{[A-Z][A-Z_0-9]*\}', inhoud), ('niet alle iconen ingevuld', pg['bron'])

    css = io.open(HOME + 'home.css', encoding='utf-8').read()
    css = css.replace('{BEELD}', '../' + BEELD).replace('{BEELD_MOBIEL}', '../' + BEELD_M)
    css = css.replace('{BEELD_DIENST}', '../wp-content/uploads/finect/diensten-handtekening.jpg')
    css += '\n' + io.open(VERZ + 'verz.css', encoding='utf-8').read()
    css += '\n' + io.open(SP + 'zak.css', encoding='utf-8').read()

    # ----- kop -----
    t = re.sub(r'<title>.*?</title>', '<title>' + html.escape(pg['titel'], quote=False) + '</title>', t, count=1, flags=re.S)
    t = re.sub(r'<meta name="description" content="[^"]*" />',
               '<meta name="description" content="' + html.escape(pg['beschr'], quote=True) + '" />', t, count=1)
    vervang('<link rel="canonical" href="https://finect.nl/over-finect/" />', '<link rel="canonical" href="' + url + '" />')
    t = re.sub(r'<meta property="og:title" content="[^"]*" />',
               '<meta property="og:title" content="' + html.escape(pg['titel'], quote=True) + '" />', t, count=1)
    t = re.sub(r'<meta property="og:description" content="[^"]*" />',
               '<meta property="og:description" content="' + html.escape(pg['beschr'], quote=True) + '" />', t, count=1)
    vervang('<meta property="og:url" content="https://finect.nl/over-finect/" />',
            '<meta property="og:url" content="' + url + '" />\n'
            '\t<meta property="og:image" content="' + BASIS + pg.get('beeld', BEELD) + '" />\n'
            '\t<meta property="og:image:width" content="1920" />\n'
            '\t<meta property="og:image:height" content="1080" />')
    t = re.sub(r'\s*<meta property="article:modified_time" content="[^"]*" />', '', t, count=1)

    # ----- gestructureerde data -----
    kruimels = [("Home", BASIS), ("Zakelijk", BASIS + HOOFD['pad'])]
    if pg is not HOOFD:
        kruimels.append((pg['naam'], url))
    graaf = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": pg['titel'], "description": pg['beschr'],
         "isPartOf": {"@id": BASIS + "#website"}, "about": {"@id": url + "#dienst"},
         "breadcrumb": {"@id": url + "#kruimelpad"}, "inLanguage": "nl-NL"},
        {"@type": "BreadcrumbList", "@id": url + "#kruimelpad", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(kruimels)]},
        {"@type": "Service", "@id": url + "#dienst", "name": pg['dienst'], "serviceType": "Verzekeringsadvies voor bedrijven",
         "provider": {"@id": BASIS + "#organisatie"}, "url": url,
         "areaServed": [{"@type": "City", "name": c} for c in
                        ["Apeldoorn", "Ugchelen", "Beekbergen", "Loenen", "Klarenbeek", "Twello", "Vaassen"]]}]}
    t = re.sub(r'(<script type="application/ld\+json" class="yoast-schema-graph">).*?(</script>)',
               lambda m: m.group(1) + json.dumps(graaf, ensure_ascii=False, separators=(',', ':')) + m.group(2),
               t, count=1, flags=re.S)
    m = re.search(r'(<script type="application/ld\+json" id="fx-bedrijfsgegevens">)(.*?)(</script>)', t, re.S)
    org = json.loads(m.group(2))
    org["hasMap"] = "https://www.google.com/maps?cid=9247328396419147947"
    # het Google Bedrijfsprofiel als officieel profiel van het bedrijf
    if org["hasMap"] not in org.setdefault("sameAs", []):
        org["sameAs"].append(org["hasMap"])
    org["geo"] = {"@type": "GeoCoordinates", "latitude": 52.2186011, "longitude": 5.9704508}
    t = t[:m.start(2)] + json.dumps(org, ensure_ascii=False, separators=(',', ':')) + t[m.end(2):]
    t = re.sub(r'\s*<script type="application/ld\+json" id="fx-persoon">.*?</script>', '', t, count=1, flags=re.S)
    vragen = [{"@type": "Question", "name": schoon(v.group(1)),
               "acceptedAnswer": {"@type": "Answer", "text": schoon(v.group(2))}}
              for v in re.finditer(r'<details[^>]*>\s*<summary><h3>(.*?)</h3></summary>\s*<p>(.*?)</p>\s*</details>', inhoud, re.S)]
    assert len(vragen) == pg['vragen'], (pg['bron'], len(vragen))
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "@id": url + "#vragen", "mainEntity": vragen}
    t = re.sub(r'(<script type="application/ld\+json" id="fx-vragen">).*?(</script>)',
               lambda m: m.group(1) + json.dumps(faq, ensure_ascii=False, separators=(',', ':')) + m.group(2),
               t, count=1, flags=re.S)

    # ----- opmaak -----
    voorladen = ''
    if pg.get('beeld') and 'fx-verz__kop--foto' in inhoud:
        # de kopfoto van een subpagina is het grootste element bovenaan: vooraf laden
        m_beeld = pg['beeld'].replace('.jpg', '-mobiel.jpg')
        voorladen = ('<link rel="preload" as="image" href="../' + pg['beeld'] + '" media="(min-width: 769px)" fetchpriority="high">\n'
                     '<link rel="preload" as="image" href="../' + m_beeld + '" media="(max-width: 768px)" fetchpriority="high">\n')
    if pg.get('held'):
        voorladen = ('<link rel="preload" as="image" href="../' + BEELD + '" media="(min-width: 769px)" fetchpriority="high">\n'
                     '<link rel="preload" as="image" href="../' + BEELD_M + '" media="(max-width: 768px)" fetchpriority="high">\n')
    vervang('</head>', voorladen + css + '\n</head>')

    # ----- lichaam -----
    a = t.find('<div class="page-header'); b = t.find('<main id="main"')
    assert 0 < a < b
    t = t[:a] + t[b:]
    a = t.find('<div class="fx-ct">'); eind = t.find('</main>', a); b = t.rfind('</div>', a, eind)
    assert 0 < a < b < eind
    t = t[:a] + '<div class="fx-ct">\n' + inhoud + '\n</div>' + t[b + len('</div>'):]

    # menu: Zakelijk is de huidige pagina; de uitklaplijst van Verzekeringen komt uit de basis en blijft staan
    t = t.replace('current-menu-item page_item page-item-31 current_page_item ', '')
    assert t.count('<a href=".">') == 4
    t = t.replace('<a href=".">', '<a href="../over-finect">')
    subs = [p for p in PAGINAS if p is not HOOFD]
    items = ''.join('\t<li class="menu-item menu-item-type-post_type menu-item-object-page%s menu-item-fz%d">'
                    '<a href="../%s"><span><span class="item_text">%s</span></span><span class="menu-item_plus"></span></a></li>'
                    % (' current-menu-item current_page_item' if p is pg else '', i, p['pad'], p['menu'])
                    for i, p in enumerate(subs, 1))
    t, n = re.subn(r'(<li (?:id="menu-item-3875" )?class="menu-item menu-item-type-post_type menu-item-object-page)'
                   r'( menu-item-3875"><a href="[^"]*"><span><span class="item_text">Zakelijk</span></span><span class="menu-item_plus"></span></a>)</li>',
                   lambda m: m.group(1) + ' menu-item-has-children current-menu-item' + (' current-menu-ancestor current-menu-parent' if pg is not HOOFD else ' current_page_item')
                   + m.group(2) + '<ul class="sub-menu">' + items + '</ul>\n</li>', t)
    assert n == 4, n

    # restanten van Over ons (pagina 31): nu die van Zakelijk (pagina 3873)
    vervang('finect.nl%252Fover-finect%252F', 'finect.nl%252Fzakelijk%252F', 2)
    vervang('href="../wp-json/wp/v2/pages/31"', 'href="../wp-json/wp/v2/pages/3873"')
    t, n = re.subn(r"<link rel='stylesheet' id='elementor-post-31-css' [^>]*/>\n", '', t)
    assert n == 1
    vervang('page-id-31 ', 'page-id-3873 ')
    vervang('elementor-page-31"', 'elementor-page-3873"')

    if VOORBEELD:
        t = re.sub(r'\s*<link rel="canonical" href="[^"]*" />', '', t, count=1)
        t = t.replace('<head>', '<head>\n<meta name="robots" content="noindex, nofollow">', 1)
        t = t.replace('<title>', '<title>VOORBEELD | ', 1)
        banier = ('<div id="fxBanier" style="position:fixed;left:0;right:0;bottom:0;z-index:99999;background:#b5004a;'
                  'color:#fff;font-family:Barlow,Arial,sans-serif;font-size:14px;line-height:1.45;'
                  'padding:10px 16px;text-align:center;">Voorbeeld van de nieuwe pagina ' + html.escape(pg['naam']) +
                  '. Deze pagina staat niet in Google en hoort nog niet bij de website.</div>\n'
                  '<script>(function(){var b=document.getElementById("fxBanier"),r=document.documentElement;'
                  'function z(){r.style.setProperty("--fx-onder",b.offsetHeight+"px");}z();addEventListener("resize",z);})();</script>\n')
        t = t.replace('</body>', banier + '</body>', 1)

    t, _ = opruimen(t)
    t, n = zoeken_weg(t); assert n == 3
    t = pagina_aanpassen(t)
    t = kleine_punten(t)
    t, _ = links_en_voettekst(t)

    # ----- paden: de voorbeelden staan onder /voorbeeld/, en subpagina's liggen dieper -----
    pad = pg['pad']
    if VOORBEELD:
        for p in ('zakelijk/', 'arbeidsongeschiktheidsverzekeringen-aov/'):
            t = t.replace('"../' + p, '"../voorbeeld/' + p).replace("'../" + p, "'../voorbeeld/" + p)
        pad = 'voorbeeld/' + pad
    diepte = pad.count('/')
    if diepte != 1:
        t = t.replace('../', '../' * diepte)
    dst = 'site/' + pad + 'index.html'
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    io.open(dst, 'w', encoding='utf-8').write(t)
    h1 = re.findall(r'<h1[^>]*>(.*?)</h1>', t)
    woorden = len(schoon(inhoud).split())
    print(f"{dst}: titel {len(pg['titel'])} tekens, beschrijving {len(pg['beschr'])}, h1 {h1}, ~{woorden} woorden")


for pg in PAGINAS:
    if os.path.exists(SP + pg['bron']):
        bouw(pg)
    else:
        print('nog geen inhoud voor', pg['pad'])

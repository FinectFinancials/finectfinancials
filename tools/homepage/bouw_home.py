# -*- coding: utf-8 -*-
"""Bouwt de nieuwe homepage als voorbeeldpagina op /voorbeeld/.

Basis is Over ons: dezelfde kop, voettekst, opmaak en scripts. Alleen de
inhoud, de kopgegevens en de gestructureerde data worden vervangen.
"""
import io, re, json, html, os, sys

SP = '/tmp/claude-0/-home-user-finectfinancials/eb3bde67-f228-5f8e-b9ee-dcd3a00cb56a/scratchpad/home/'
SRC = 'site/over-finect/index.html'
DST = sys.argv[1] if len(sys.argv) > 1 else 'site/voorbeeld/index.html'
VOORBEELD = '/voorbeeld/' in DST

TITEL = 'Verzekeringen en hypotheek in Apeldoorn | Finect Financials'
BESCHR = ('Onafhankelijk verzekeringsadvies in Apeldoorn, voor thuis en voor uw bedrijf. '
          'Ook voor uw hypotheek. Eén vaste adviseur, het eerste gesprek is gratis.')
BASIS = 'https://finect.nl/'
P = '../'   # de voorbeeldpagina staat een map diep, net als Over ons
BEELD = 'wp-content/uploads/finect/de-pencil-apeldoorn.jpg'
BEELD_M = 'wp-content/uploads/finect/de-pencil-apeldoorn-mobiel.jpg'

t = io.open(SRC, encoding='utf-8').read()

def vervang(oud, nieuw, n=1):
    global t
    assert t.count(oud) == n, (t.count(oud), oud[:80])
    t = t.replace(oud, nieuw)

# ---------- iconen ----------
def svg(paden, maat=26, dikte=1.7):
    return (f'<svg width="{maat}" height="{maat}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="{dikte}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" '
            f'focusable="false">{paden}</svg>')
TEL = ('<path d="M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3.1 19.5 19.5 0 01-6-6A19.8 19.8 0 012.1 4.2 '
       '2 2 0 014.1 2h3a2 2 0 012 1.7c.1.9.4 1.8.7 2.7a2 2 0 01-.5 2.1L8.1 9.9a16 16 0 006 6l1.4-1.2a2 2 0 '
       '012.1-.5c.9.3 1.8.6 2.7.7a2 2 0 011.7 2z"/>')
ICONEN = {
    'PIJL': svg('<path d="M5 12h14M13 6l6 6-6 6"/>', 22, 1.8),
    'ICO_SCHILD': svg('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>'),
    'ICO_KOFFER': svg('<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v16"/>'),
    'ICO_HART': svg('<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>'),
    'ICO_CHECK': svg('<path d="M16 4h2a2 2 0 012 2v14a2 2 0 01-2 2H6a2 2 0 01-2-2V6a2 2 0 012-2h2"/>'
                     '<rect x="8" y="2" width="8" height="4" rx="1"/><path d="M9 14l2 2 4-4"/>'),
    'ICO_HUIS': svg('<path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><path d="M9 22V12h6v10"/>'),
    'ICO_TAART': svg('<path d="M21.21 15.89A10 10 0 118 2.83"/><path d="M22 12A10 10 0 0012 2v10z"/>'),
    'ICO_TEL': svg(TEL, 20, 1.8),
    'ICO_MAIL': svg('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>', 20, 1.8),
    'ICO_PIN': svg('<path d="M21 10c0 6-9 12-9 12s-9-6-9-12a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/>', 20, 1.8),
    'ICO_KAART': svg('<path d="M1 6v16l7-4 8 4 7-4V2l-7 4-8-4-7 4z"/><path d="M8 2v16M16 6v16"/>', 20, 1.8),
}

inhoud = io.open(SP + 'inhoud.html', encoding='utf-8').read()
for k, v in ICONEN.items():
    inhoud = inhoud.replace('{' + k + '}', v)
assert not re.search(r'\{[A-Z_]+\}', inhoud), 'niet alle iconen ingevuld'

css = io.open(SP + 'home.css', encoding='utf-8').read()
css = css.replace('{BEELD}', P + BEELD).replace('{BEELD_MOBIEL}', P + BEELD_M)
css = css.replace('{BEELD_DIENST}', P + 'wp-content/uploads/finect/diensten-handtekening.jpg')

# ---------- kop: titel, beschrijving, canonical, deelinformatie ----------
t = re.sub(r'<title>.*?</title>', '<title>' + TITEL + '</title>', t, count=1, flags=re.S)
t = re.sub(r'<meta name="description" content="[^"]*" />',
           '<meta name="description" content="' + html.escape(BESCHR, quote=True) + '" />', t, count=1)
vervang('<link rel="canonical" href="https://finect.nl/over-finect/" />',
        '<link rel="canonical" href="' + BASIS + '" />')
vervang('<meta property="og:type" content="article" />', '<meta property="og:type" content="website" />')
t = re.sub(r'<meta property="og:title" content="[^"]*" />',
           '<meta property="og:title" content="' + TITEL + '" />', t, count=1)
t = re.sub(r'<meta property="og:description" content="[^"]*" />',
           '<meta property="og:description" content="' + html.escape(BESCHR, quote=True) + '" />', t, count=1)
vervang('<meta property="og:url" content="https://finect.nl/over-finect/" />',
        '<meta property="og:url" content="' + BASIS + '" />\n'
        '\t<meta property="og:image" content="' + BASIS + BEELD + '" />\n'
        '\t<meta property="og:image:width" content="1920" />\n'
        '\t<meta property="og:image:height" content="1080" />')
t = re.sub(r'\s*<meta property="article:modified_time" content="[^"]*" />', '', t, count=1)

# ---------- gestructureerde data ----------
graaf = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebSite", "@id": BASIS + "#website", "url": BASIS, "name": "Finect Financials",
     "alternateName": "Finect", "inLanguage": "nl-NL", "publisher": {"@id": BASIS + "#organisatie"}},
    {"@type": "WebPage", "@id": BASIS + "#webpage", "url": BASIS, "name": TITEL, "description": BESCHR,
     "isPartOf": {"@id": BASIS + "#website"}, "about": {"@id": BASIS + "#organisatie"},
     "primaryImageOfPage": {"@type": "ImageObject", "url": BASIS + BEELD, "width": 1920, "height": 1080},
     "inLanguage": "nl-NL"}]}
t = re.sub(r'(<script type="application/ld\+json" class="yoast-schema-graph">).*?(</script>)',
           lambda m: m.group(1) + json.dumps(graaf, ensure_ascii=False, separators=(',', ':')) + m.group(2),
           t, count=1, flags=re.S)

# organisatie: dezelfde als op contact en Over ons, plus de diensten
m = re.search(r'(<script type="application/ld\+json" id="fx-bedrijfsgegevens">)(.*?)(</script>)', t, re.S)
org = json.loads(m.group(2))
# Google Bedrijfsprofiel en de plek van het kantoor op de kaart
org["hasMap"] = "https://www.google.com/maps?cid=9247328396419147947"
org["geo"] = {"@type": "GeoCoordinates", "latitude": 52.2186011, "longitude": 5.9704508}
org["hasOfferCatalog"] = {"@type": "OfferCatalog", "name": "Diensten van Finect Financials", "itemListElement": [
    {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "url": BASIS + u}} for n, u in [
        ("Particuliere verzekeringen", "verzekeringen/"),
        ("Zakelijke verzekeringen", "zakelijk/"),
        ("Arbeidsongeschiktheidsverzekering voor zzp'ers", "arbeidsongeschiktheidsverzekeringen-aov/"),
        ("Polischeck", "contact/"),
        ("Hypotheekadvies", "hypotheken/"),
        ("Financiële planning", "contact/")]]}
t = t[:m.start(2)] + json.dumps(org, ensure_ascii=False, separators=(',', ':')) + t[m.end(2):]

# de persoon hoort bij Over ons
t = re.sub(r'\s*<script type="application/ld\+json" id="fx-persoon">.*?</script>', '', t, count=1, flags=re.S)

# veelgestelde vragen: uit de zichtbare tekst, zodat die twee nooit uit elkaar lopen
def schoon(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', s))).strip()
vragen = []
for vm in re.finditer(r'<details[^>]*>\s*<summary><h3>(.*?)</h3></summary>\s*<p>(.*?)</p>\s*</details>', inhoud, re.S):
    vragen.append({"@type": "Question", "name": schoon(vm.group(1)),
                   "acceptedAnswer": {"@type": "Answer", "text": schoon(vm.group(2))}})
assert len(vragen) == 5, len(vragen)
faq = {"@context": "https://schema.org", "@type": "FAQPage", "@id": BASIS + "#vragen", "mainEntity": vragen}
t = re.sub(r'(<script type="application/ld\+json" id="fx-vragen">).*?(</script>)',
           lambda m: m.group(1) + json.dumps(faq, ensure_ascii=False, separators=(',', ':')) + m.group(2),
           t, count=1, flags=re.S)

# ---------- opmaak en vooraf laden van de openingsfoto ----------
voorladen = ('<link rel="preload" as="image" href="' + P + BEELD + '" media="(min-width: 769px)" fetchpriority="high">\n'
             '<link rel="preload" as="image" href="' + P + BEELD_M + '" media="(max-width: 768px)" fetchpriority="high">\n')
vervang('</head>', voorladen + css + '\n</head>')

# ---------- lichaam ----------
# de fotostrook met breadcrumbs van Over ons vervalt; het openingsbeeld staat in de inhoud
a = t.find('<div class="page-header')
b = t.find('<main id="main"')
assert 0 < a < b, (a, b)
t = t[:a] + t[b:]

a = t.find('<div class="fx-ct">')
eind_main = t.find('</main>', a)
b = t.rfind('</div>', a, eind_main)
assert 0 < a < b < eind_main
t = t[:a] + '<div class="fx-ct">\n' + inhoud + '\n</div>' + t[b + len('</div>'):]

# menu: Home is nu de huidige pagina, Over Finect wijst weer naar zijn eigen pagina
t = t.replace('current-menu-item page_item page-item-31 current_page_item ', '')
n_zelf = t.count('<a href=".">')
assert n_zelf == 4, n_zelf
t = t.replace('<a href=".">', '<a href="' + P + 'over-finect">')
t, n = re.subn(r'menu-item-home menu-item-3514', 'menu-item-home current-menu-item current_page_item menu-item-3514', t)
assert n >= 1

# restanten van Over ons (pagina 31) in de kop en de body: nu die van de homepage (pagina 3326)
vervang('finect.nl%252Fover-finect%252F', 'finect.nl%252F', 2)
vervang('href="../wp-json/wp/v2/pages/31"', 'href="../wp-json/wp/v2/pages/3326"')
# de Elementor opmaak van Over ons geldt alleen voor elementen die hier niet meer staan
t, n = re.subn(r"<link rel='stylesheet' id='elementor-post-31-css' [^>]*/>\n", '', t)
assert n == 1, n
vervang('class="wp-singular page-template-default page page-id-31 wp-theme-zikzag elementor-default '
        'elementor-kit-1 elementor-page elementor-page-31"',
        'class="home wp-singular page-template-default page page-id-3326 wp-theme-zikzag elementor-default '
        'elementor-kit-1 elementor-page elementor-page-3326"')

# ---------- alleen voor de voorbeeldpagina ----------
if VOORBEELD:
    t = re.sub(r'\s*<link rel="canonical" href="[^"]*" />', '', t, count=1)
    t = t.replace('<head>', '<head>\n<meta name="robots" content="noindex, nofollow">', 1)
    t = t.replace('<title>', '<title>VOORBEELD homepage | ', 1)
    banier = ('<div style="position:fixed;left:0;right:0;bottom:0;z-index:99999;background:#b5004a;'
              'color:#fff;font-family:Barlow,Arial,sans-serif;font-size:14px;line-height:1.45;'
              'padding:10px 16px;text-align:center;">Voorbeeld van de nieuwe homepage. '
              'Deze pagina staat niet in Google en hoort nog niet bij de website.</div>\n')
    t = t.replace('</body>', banier + '</body>', 1)

# ---------- oude WordPress-onderdelen weg (zie opruimen.py) ----------
sys.path.insert(0, SP)
from opruimen import opruimen, zoeken_weg
from slank import pagina_aanpassen
t, _ = opruimen(t)
t, n = zoeken_weg(t)
assert n == 3, n
# één afgeslankt opmaakbestand in plaats van twaalf losse (zie slank.py)
t = pagina_aanpassen(t)

os.makedirs(os.path.dirname(DST), exist_ok=True)
io.open(DST, 'w', encoding='utf-8').write(t)
print('geschreven:', DST, len(t), 'tekens')
print('titel      :', re.findall(r'<title>(.*?)</title>', t)[0], len(TITEL), 'tekens')
print('beschrijving:', len(BESCHR), 'tekens')
print('h1         :', re.findall(r'<h1[^>]*>(.*?)</h1>', t))

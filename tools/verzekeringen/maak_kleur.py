# -*- coding: utf-8 -*-
"""Proefversie van de hoofdpagina Verzekeringen met een groenblauwe steunkleur en zonder wegwijzer.
Kopieert site/voorbeeld/verzekeringen/index.html naar site/voorbeeld/verzekeringen-kleur/index.html
(zelfde diepte, dus alle paden blijven kloppen), voegt kleur.css toe, haalt de wegwijzer weg
en zet de bruikbare zinnen daaruit als extra vragen onderaan (ook in de gestructureerde gegevens)."""
import io, os, re, json

SP = os.path.dirname(os.path.abspath(__file__)) + '/'
BRON = 'site/voorbeeld/verzekeringen/index.html'
DOEL = 'site/voorbeeld/verzekeringen-kleur/index.html'

EXTRA_VRAGEN = [
    ('Welke verzekeringen zijn belangrijk voor een gezin?',
     'Een aansprakelijkheidsverzekering voor het hele gezin. Heeft u samen een hypotheek, dan is een '
     'overlijdensrisicoverzekering verstandig. Kijk ook of uw reisverzekering alle gezinsleden dekt, ook als de kinderen ouder worden.'),
    ('Wat moet ik zelf verzekeren als ik een appartement heb?',
     'Het gebouw verzekert de VvE meestal met een opstalverzekering voor het hele complex. U heeft zelf een inboedelverzekering '
     'en een aansprakelijkheidsverzekering nodig. Heeft u uw keuken of badkamer vernieuwd? Kijk dan of die verbetering onder de '
     'polis van de VvE valt, of dat u hem zelf moet meeverzekeren.'),
    ('Welke verzekeringen zijn belangrijk voor een zzp\'er?',
     'Een oplossing voor uw inkomen als u niet kunt werken, en een bedrijfsaansprakelijkheidsverzekering als u schade bij klanten '
     'kunt veroorzaken. Uw aansprakelijkheidsverzekering voor particulieren dekt namelijk geen schade die u tijdens uw werk veroorzaakt.'),
]

t = io.open(BRON, encoding='utf-8').read()

# kleuren
css = io.open(SP + 'kleur.css', encoding='utf-8').read()
assert t.count('</head>') == 1
t = t.replace('</head>', css + '</head>', 1)

# wegwijzer weg
a = t.index('  <!-- wegwijzer -->')
b = t.index('  <!-- pakket en polischeck -->')
t = t[:a] + t[b:]

# extra vragen achter de laatste vraag
a = t.index('  <!-- vragen -->')
b = t.index('  <!-- contact -->', a)
blok = t[a:b]
laatste = blok.rindex('</details>') + len('</details>')
nieuw = ''.join('\n      <details>\n        <summary><h3>%s</h3></summary>\n        <p>%s</p>\n      </details>'
                % (v.replace("'", '&#039;'), u) for v, u in EXTRA_VRAGEN)
blok = blok[:laatste] + nieuw + blok[laatste:]
t = t[:a] + blok + t[b:]

# gestructureerde gegevens bijwerken
m = re.search(r'(<script type="application/ld\+json" id="fx-vragen">)(.*?)(</script>)', t, re.S)
faq = json.loads(m.group(2))
for v, u in EXTRA_VRAGEN:
    faq['mainEntity'].append({"@type": "Question", "name": v, "acceptedAnswer": {"@type": "Answer", "text": u}})
t = t[:m.start(2)] + json.dumps(faq, ensure_ascii=False, separators=(',', ':')) + t[m.end(2):]
zichtbaar = len(re.findall(r'<summary><h3>', t))
assert zichtbaar == len(faq['mainEntity']), (zichtbaar, len(faq['mainEntity']))

# voorbeeldbalk en titel
oud = 'Voorbeeld van de nieuwe pagina Verzekeringen.'
assert t.count(oud) == 1
t = t.replace(oud, 'Proef met een extra steunkleur (groen) en zonder wegwijzer op de pagina Verzekeringen.')
t = t.replace('<title>VOORBEELD | ', '<title>VOORBEELD KLEUR | ', 1)

os.makedirs(os.path.dirname(DOEL), exist_ok=True)
io.open(DOEL, 'w', encoding='utf-8').write(t)
print('geschreven', DOEL, '| vragen:', zichtbaar)

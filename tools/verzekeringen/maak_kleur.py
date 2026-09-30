# -*- coding: utf-8 -*-
"""Proefversie van de hoofdpagina Verzekeringen met een groenblauwe steunkleur.
Kopieert site/voorbeeld/verzekeringen/index.html naar site/voorbeeld/verzekeringen-kleur/index.html
(zelfde diepte, dus alle paden blijven kloppen) en voegt kleur.css toe."""
import io, os

SP = os.path.dirname(os.path.abspath(__file__)) + '/'
BRON = 'site/voorbeeld/verzekeringen/index.html'
DOEL = 'site/voorbeeld/verzekeringen-kleur/index.html'

t = io.open(BRON, encoding='utf-8').read()
css = io.open(SP + 'kleur.css', encoding='utf-8').read()
assert t.count('</head>') == 1
t = t.replace('</head>', css + '</head>', 1)
oud = 'Voorbeeld van de nieuwe pagina Verzekeringen.'
assert t.count(oud) == 1
t = t.replace(oud, 'Proef met een extra steunkleur (groen) op de pagina Verzekeringen.')
t = t.replace('<title>VOORBEELD | ', '<title>VOORBEELD KLEUR | ', 1)
os.makedirs(os.path.dirname(DOEL), exist_ok=True)
io.open(DOEL, 'w', encoding='utf-8').write(t)
print('geschreven', DOEL)

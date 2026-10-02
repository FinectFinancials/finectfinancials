# -*- coding: utf-8 -*-
"""Zet onder 'Zakelijk' in het menu een uitklaplijst met de vijf zakelijke subpagina's.
Gebruik: python3 menu_zak.py site/index.html [meer bestanden...]
Werkt op elke pagina met het gewone menu; slaat pagina's over die de lijst al hebben (zoals de zakelijke pagina's zelf).
De links wijzen naar de echte subpagina's, relatief vanaf de pagina. Draai dit ook na het opnieuw bouwen
van de homepage of de verzekeringspagina's (net als menu_alle.py voor Verzekeringen)."""
import io, os, re, sys

SUBS = [('zakelijk/bedrijfsaansprakelijkheidsverzekering/', 'Bedrijfsaansprakelijkheid'),
        ('arbeidsongeschiktheidsverzekeringen-aov/', 'AOV voor ondernemers'),
        ('zakelijk/bedrijfspand-en-inventaris/', 'Bedrijfspand en inventaris'),
        ('zakelijk/bedrijfsautoverzekering/', 'Bedrijfsauto en bestelbus'),
        ('zakelijk/vve-verzekering/', 'VvE-verzekering')]
PATROON = re.compile(r'(<li (?:id="menu-item-3875" )?class="menu-item menu-item-type-post_type menu-item-object-page)'
                     r'([^"]*"><a href="[^"]*"><span><span class="item_text">Zakelijk</span></span>'
                     r'<span class="menu-item_plus"></span></a>)</li>')


def zet_menu(pad):
    t = io.open(pad, encoding='utf-8').read()
    if 'menu-item-fz1' in t:
        return 'al aanwezig'
    terug = os.path.relpath('site', os.path.dirname(pad)).replace(os.sep, '/') + '/'
    if terug == './':
        terug = ''
    items = ''.join('\t<li class="menu-item menu-item-type-post_type menu-item-object-page menu-item-fz%d">'
                    '<a href="%s%s"><span><span class="item_text">%s</span></span>'
                    '<span class="menu-item_plus"></span></a></li>' % (i, terug, s, n)
                    for i, (s, n) in enumerate(SUBS, 1))
    t, n = PATROON.subn(lambda m: m.group(1) + ' menu-item-has-children' + m.group(2) +
                        '<ul class="sub-menu">' + items + '</ul>\n</li>', t)
    assert n == 4, (pad, n)
    io.open(pad, 'w', encoding='utf-8').write(t)
    return 'aangepast'


if __name__ == '__main__':
    for p in sys.argv[1:]:
        print(p, zet_menu(p))

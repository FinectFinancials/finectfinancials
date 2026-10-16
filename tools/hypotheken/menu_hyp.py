# -*- coding: utf-8 -*-
"""Zet onder 'Hypotheken' in het menu een uitklaplijst met de hypotheek-subpagina's.
Gebruik: python3 menu_hyp.py site/index.html [meer bestanden...]
Werkt op elke pagina met het gewone menu; slaat pagina's over die de lijst al hebben.
De links zijn relatief vanaf de pagina. Met voorbeeld=True wijzen ze naar /voorbeeld/hypotheken/...
Draai dit ook na het opnieuw bouwen van andere pagina's (net als menu_zak.py voor Zakelijk)."""
import io, os, re, sys

SUBS = [('hypotheken/eerste-huis-kopen/', 'Eerste huis kopen'),
        ('hypotheken/volgend-huis-kopen/', 'Volgend huis kopen'),
        ('hypotheken/oversluiten/', 'Hypotheek oversluiten'),
        ('hypotheken/zzp-en-ondernemers/', "Voor zzp'ers en ondernemers")]
PATROON = re.compile(r'(<li (?:id="menu-item-3877" )?class="menu-item menu-item-type-post_type menu-item-object-page)'
                     r'([^"]*"><a href="[^"]*"><span><span class="item_text">Hypotheken</span></span>'
                     r'<span class="menu-item_plus"></span></a>)</li>')


def zet_menu(pad, voorbeeld=False, huidig=None):
    t = io.open(pad, encoding='utf-8').read()
    if 'menu-item-fh1' in t:
        return 'al aanwezig'
    terug = os.path.relpath('site', os.path.dirname(pad)).replace(os.sep, '/') + '/'
    if terug == './':
        terug = ''
    if voorbeeld:
        terug += 'voorbeeld/'
    items = ''.join('\t<li class="menu-item menu-item-type-post_type menu-item-object-page%s menu-item-fh%d">'
                    '<a href="%s%s"><span><span class="item_text">%s</span></span>'
                    '<span class="menu-item_plus"></span></a></li>'
                    % (' current-menu-item current_page_item' if s == huidig else '', i, terug, s, n)
                    for i, (s, n) in enumerate(SUBS, 1))
    t, n = PATROON.subn(lambda m: m.group(1) + ' menu-item-has-children' + m.group(2) +
                        '<ul class="sub-menu">' + items + '</ul>\n</li>', t)
    assert n == 4, (pad, n)
    io.open(pad, 'w', encoding='utf-8').write(t)
    return 'aangepast'


if __name__ == '__main__':
    for p in sys.argv[1:]:
        print(p, zet_menu(p))

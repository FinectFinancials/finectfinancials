# -*- coding: utf-8 -*-
"""Zet onder 'Verzekeringen' in het menu een uitklaplijst met de vier subpagina's.
Gebruik: python3 menu_alle.py site/voorbeeld/index.html [meer bestanden...]
Werkt op elke pagina met het gewone menu; slaat pagina's over die de lijst al hebben.
De links wijzen naar de echte subpagina's onder /verzekeringen/, relatief vanaf de pagina."""
import io, os, re, sys

SUBS = [('woonverzekering', 'Woonverzekering'), ('aansprakelijkheidsverzekering', 'Aansprakelijkheid'),
        ('autoverzekering', 'Autoverzekering'), ('polischeck', 'Polischeck')]
PATROON = re.compile(r'(<li (?:id="menu-item-3876" )?class="menu-item menu-item-type-post_type menu-item-object-page)'
                     r'([^"]*"><a href="[^"]*"><span><span class="item_text">Verzekeringen</span></span>'
                     r'<span class="menu-item_plus"></span></a>)</li>')


def zet_menu(pad):
    t = io.open(pad, encoding='utf-8').read()
    if 'menu-item-fx1' in t:
        return 'al aanwezig'
    terug = os.path.relpath('site', os.path.dirname(pad)).replace(os.sep, '/')
    items = ''.join('\t<li class="menu-item menu-item-type-post_type menu-item-object-page menu-item-fx%d">'
                    '<a href="%s/verzekeringen/%s/"><span><span class="item_text">%s</span></span>'
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

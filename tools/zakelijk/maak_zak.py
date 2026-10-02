# -*- coding: utf-8 -*-
"""Maakt de inhoud van de vijf subpagina's onder Zakelijk.
Gebruikt de bouwstenen uit ../verz/sub_extra.py (duo, vinkjes, schade, werkwijze, review, wie, rij, CIJFERS, CHIP)."""
import io, os, sys
HIER = os.path.dirname(os.path.abspath(__file__)) + '/'
sys.path.insert(0, os.path.join(HIER, '..', 'verz'))
from sub_extra import (duo, vinkjes, schade, werkwijze, review, wie, rij, CIJFERS, CHIP, KNOPPEN,  # noqa: E402
                       REVIEW_FLEUR, REVIEW_TONY, REVIEW_KYRA, REVIEW_MARCEL)

STERREN = ('<a class="fx-verz__sterren" href="https://maps.app.goo.gl/CUqTeR8SEaGoE9rx9" target="_blank" rel="noopener">'
           '<span class="fx-verz__sterrij" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</span>'
           '<b>5,0</b><span>uit 16 Google reviews</span></a>')

ANDERE = [('Bedrijfsaansprakelijkheid', '../zakelijk/bedrijfsaansprakelijkheidsverzekering/'),
          ('AOV', '../arbeidsongeschiktheidsverzekeringen-aov/'),
          ('Bedrijfspand en inventaris', '../zakelijk/bedrijfspand-en-inventaris/'),
          ('Bedrijfsauto', '../zakelijk/bedrijfsautoverzekering/'),
          ('VvE-verzekering', '../zakelijk/vve-verzekering/'),
          ('Alle zakelijke verzekeringen', '../zakelijk/')]
FOTO = {'Bedrijfsaansprakelijkheid': 'zak-avb', 'AOV': 'zak-aov', 'Bedrijfspand en inventaris': 'zak-pand',
        'Bedrijfsauto': 'zak-auto', 'VvE-verzekering': 'de-pencil-apeldoorn'}
UITLEG = {'Bedrijfsaansprakelijkheid': ('{ICO_SCHILD}', 'Voor schade die u of uw personeel bij klanten of anderen veroorzaakt.'),
          'AOV': ('{ICO_HART}', 'Voor uw inkomen als u als ondernemer langere tijd niet kunt werken.'),
          'Bedrijfspand en inventaris': ('{ICO_WINKEL}', 'Uw pand, inrichting, voorraad en inkomsten bij stilstand.'),
          'Bedrijfsauto': ('{ICO_BUS}', 'Auto van de zaak, bestelbus of wagenpark, en het gereedschap erin.'),
          'VvE-verzekering': ('{ICO_GEBOUW}', 'Opstal, aansprakelijkheid en het bestuur van uw VvE verzekerd.')}


REVIEW_MARITA = ('Zowel voor mijn privé situatie als risico&rsquo;s als ondernemer goed objectief advies van Finect/Fred gekregen.', 'MT', 'Marita T.')
REVIEW_LARS = ('Ik ben zeer tevreden over de service van Finect. Fred is deskundig, meedenkend en weet zaken helder uit te leggen. Wat het extra prettig maakt, is dat hij goed bereikbaar is en snel reageert op vragen. Een betrouwbare adviseur waar je op kunt rekenen!', 'LS', 'Lars S.')
REVIEW_ROB = ('Ik ben bij Finect terechtgekomen voor mijn autoverzekering en ik ben zelden zo goed geholpen als hier. Geen standaard verkooppraatjes, maar oprechte interesse in wat ik nodig had en wat het beste bij mijn situatie paste.', 'R', 'Rob')
ONDERNEMER = 'Ondernemer &middot; Google, 5 sterren'
BRON = {'Kyra D.': ONDERNEMER, 'Marita T.': ONDERNEMER}


def reviews(kop, intro, lijst):
    """klantervaringen als carrousel (zelfde opmaak en script als op de hoofdpagina's)"""
    fig = ''.join('''
          <figure class="fx-ct__quote%s">
            <blockquote>&ldquo;%s&rdquo;</blockquote>
            <figcaption><span class="fx-ct__ini">%s</span><span class="fx-ct__wie"><b>%s</b>%s</span></figcaption>
          </figure>''' % (' is-on' if i == 0 else '', c, ini, n, BRON.get(n, 'Google, 5 sterren')) for i, (c, ini, n) in enumerate(lijst))
    return '''  <!-- klantervaringen -->
  <div class="fx-ct__band--navy" id="ervaringen"><div class="fx-ct__wrap"><section class="fx-ct__sec">
    <div class="fx-ct__rev">
      <div>
        <p class="fx-ct__sub">Klantervaringen</p>
        <h2>%s</h2>
        <p>%s</p>
        <div class="fx-ct__score">
          <span class="fx-ct__sterren" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
          <span class="fx-ct__cijfer">5,0</span>
          <span class="fx-ct__bron">uit 16 beoordelingen op Google</span>
        </div>
        <div class="fx-ct__btns">
          <a class="fx-ct__btn fx-ct__btn--o fx-home__google" href="https://maps.app.goo.gl/CUqTeR8SEaGoE9rx9" target="_blank" rel="noopener">Lees alle reviews op Google</a>
        </div>
      </div>
      <div>
        <div class="fx-ct__stage" id="fxCtStage">%s
        </div>
        <ul class="fx-ct__dots" id="fxCtDots"></ul>
      </div>
    </div>
  </section></div></div>

''' % (kop, intro, fig)


def kort(punten):
    return ('      <div class="fx-verz__kort"><h2>In het kort</h2><ul class="fx-verz__lijst">' +
            ''.join(f'<li>{p}</li>' for p in punten) + '</ul></div>\n')


def welniet(wel, niet, welkop='Wel verzekerd', nietkop='Niet verzekerd'):
    w = ''.join(f'<li>{x}</li>' for x in wel); n = ''.join(f'<li>{x}</li>' for x in niet)
    return (f'<div class="fx-verz__welniet"><div><span class="fx-verz__lijstkop">{welkop}</span><ul class="fx-verz__lijst">{w}</ul></div>'
            f'<div><span class="fx-verz__lijstkop fx-verz__lijstkop--let">{nietkop}</span><ul class="fx-verz__lijst fx-verz__lijst--niet">{n}</ul></div></div>')


def pagina(naam, kruimel, sub, h1, lead, tekst, vragen, vragenkop, hulp, hulpkop, hoe, eigen, knop2):
    andere = ''.join(f'<li><a href="{u}">{n}</a></li>' for n, u in ANDERE if n != naam)
    gerel = ''.join(f'<div class="fx-verz__pkaart fx-verz__pkaart--link"><span class="fx-ct__ico">{UITLEG[n][0]}</span><h3>{n}</h3>'
                    f'<p>{UITLEG[n][1]}</p><a class="fx-verz__pmeer" href="{u}">Lees verder</a></div>'
                    for n, u in ANDERE if n != naam and n in UITLEG)
    vr = ''.join(f'''
      <details{' open' if i == 0 else ''}>
        <summary><h3>{v}</h3></summary>
        <p>{a}</p>
      </details>''' for i, (v, a) in enumerate(vragen))
    if eigen.get('licht'):
        kop_open = '<section class="fx-verz__kop fx-verz__kop--licht"><div class="fx-ct__wrap fx-verz__kopgrid"><div>'
        kop_dicht = (f'</div>\n    <div class="fx-verz__kopfoto"><img src="../wp-content/uploads/finect/{FOTO[naam]}-mobiel.jpg" '
                     f'alt="" width="780" height="1219" fetchpriority="high" decoding="async"></div>\n  </div></section>')
    else:
        kop_open = (f'<section class="fx-verz__kop fx-verz__kop--foto" style="--kop:url(../wp-content/uploads/finect/{FOTO[naam]}.jpg);'
                    f'--kop-m:url(../wp-content/uploads/finect/{FOTO[naam]}-mobiel.jpg)"><div class="fx-ct__wrap">')
        kop_dicht = '</div></section>'
    return f'''<div class="fx-verz fx-zak">

  <!-- kop -->
  {kop_open}
    <p class="fx-verz__kruimel"><a href="../">Home</a> &rsaquo; <a href="../zakelijk/">Zakelijk</a> &rsaquo; {kruimel}</p>
    {CHIP}
    <p class="fx-ct__sub">{sub}</p>
    <h1>{h1}</h1>
    <p class="fx-ct__lead">{lead}</p>
    <div class="fx-ct__btns">
      <a class="fx-ct__btn fx-ct__btn--m" href="tel:+31630679790">Bel 06 30 67 97 90</a>
      <a class="fx-ct__btn fx-ct__btn--o" href="{knop2[1]}">{knop2[0]}</a>
    </div>
    {STERREN}
    <p class="fx-verz__heldlink"><a href="#hulp">{hulpkop}</a></p>
  {kop_dicht}

{CIJFERS}{hulp}
  <!-- tekst -->
  <div class="fx-ct__wrap"><section class="fx-ct__sec fx-verz__artikel">
    <div class="fx-verz__tekst">
{tekst}
    </div>
    <div class="fx-verz__zij">
      <div class="fx-verz__zijkaart fx-verz__zijkaart--navy">
        <h2>Liever even overleggen?</h2>
        <p>{eigen['zij']}</p>
        <div class="fx-ct__btns"><a class="fx-ct__btn fx-ct__btn--m" href="tel:+31630679790">Bel 06 30 67 97 90</a></div>
        <p style="margin:14px 0 0;"><a class="fx-verz__licht" href="mailto:info@finect.nl">info@finect.nl</a></p>
      </div>
      <div class="fx-verz__zijkaart">
        <h2>Meer voor ondernemers</h2>
        <ul>{andere}</ul>
      </div>
    </div>
  </section></div>

{hoe}{eigen['schade']}{eigen['werk']}{eigen['review']}{eigen['wie']}  <!-- ook interessant -->
  <div class="fx-ct__wrap"><section class="fx-ct__sec fx-verz__andere">
    <p class="fx-ct__sub">Ook interessant</p>
    <h2 style="margin-bottom:28px;">Andere zakelijke verzekeringen</h2>
    <div class="fx-verz__gerelateerd">{gerel}</div>
  </section></div>

  <!-- vragen -->
  <div class="fx-ct__band"><div class="fx-ct__wrap"><section class="fx-ct__sec fx-ct__faq">
    <div>
      <p class="fx-ct__sub">Vragen</p>
      <h2>{vragenkop}</h2>
      <p>{eigen['vragenintro']}</p>
      <p style="margin-top:22px;"><a class="fx-ct__btn fx-ct__btn--o" href="../contact/">Plan een gesprek</a></p>
    </div>
    <div>{vr}
    </div>
  </section></div></div>

  <!-- contact -->
  <div class="fx-ct__wrap"><section class="fx-ct__sec fx-ct__hero">
    <div>
      <p class="fx-ct__sub">Contact</p>
      <h2>{eigen['contact'][0]}</h2>
      <p class="fx-ct__lead">{eigen['contact'][1]}</p>
      <div class="fx-ct__btns">
        <a class="fx-ct__btn fx-ct__btn--m" href="tel:+31630679790">Bel 06 30 67 97 90</a>
        <a class="fx-ct__btn fx-ct__btn--o" href="../contact/">Naar contact</a>
      </div>
    </div>
    <ul class="fx-home__gegevens">
      <li><span class="fx-home__rond">{{ICO_TEL}}</span><span><b><a href="tel:+31630679790">06 30 67 97 90</a></b><span>Maandag t/m vrijdag 09:00 tot 17:30</span></span></li>
      <li><span class="fx-home__rond">{{ICO_MAIL}}</span><span><b><a href="mailto:info@finect.nl">info@finect.nl</a></b><span>Antwoord binnen één werkdag</span></span></li>
      <li><span class="fx-home__rond">{{ICO_PIN}}</span><span><b>Kantoor</b><span>Vlijtseweg 16, 7317 AH Apeldoorn</span></span></li>
      <li><span class="fx-home__rond">{{ICO_KAART}}</span><span><b>Werkgebied</b><span>Apeldoorn, Ugchelen, Beekbergen, Loenen, Klarenbeek, Twello, Vaassen en omgeving</span></span></li>
      <li><span class="fx-home__rond">{{ICO_SCHILD20}}</span><span><b>Geregistreerd</b><span>AFM 12047700, Kifid 300.017906, KvK 62201735</span></span></li>
    </ul>
  </section></div>

</div>
'''


def scenario_blok(sub, kop, intro, kaarten, voet):
    """kaarten om open te klikken (zelfde opmaak als 'Verzekerd of niet?' bij aansprakelijkheid)"""
    return ('''  <!-- hulpmiddel -->
  <div class="fx-ct__wrap"><section class="fx-ct__sec fx-verz__checksec" id="hulp">
    <div class="fx-verz__checkkaart fx-verz__checkkaart--breed">
      <div class="fx-verz__checkintro">
        <p class="fx-ct__sub">%s</p>
        <h2>%s</h2>
        <p>%s</p>
      </div>
      <div class="fx-verz__scen">''' % (sub, kop, intro) + ''.join('''
        <details class="fx-verz__scenario">
          <summary><span class="fx-verz__scenvraag">%s</span><span class="fx-verz__scenknop">Bekijk het antwoord</span></summary>
          <p><b class="fx-verz__oordeel fx-verz__oordeel--%s">%s</b>%s</p>
        </details>''' % k for k in kaarten) + '''
      </div>
      <p class="fx-verz__scenvoet">%s</p>
    </div>
  </section></div>

''' % voet)


def advieslijst(sub, kop, intro, punten, vraagkop, items, knop):
    """vinkjes; per aangevinkt punt verschijnt een advies in de lijst"""
    pl = ''.join('<li>%s</li>' % p for p in punten)
    it = ''.join('<label><input type="checkbox" name="advies" data-advies="%s"><span>%s</span></label>' % (a.replace('"', '&quot;'), t)
                 for t, a in items)
    return '''  <!-- hulpmiddel -->
  <div class="fx-ct__wrap"><section class="fx-ct__sec fx-verz__checksec" id="hulp">
    <div class="fx-verz__checkkaart">
      <div class="fx-verz__checkintro">
        <p class="fx-ct__sub">%s</p>
        <h2>%s</h2>
        <p>%s</p>
        <ul class="fx-verz__checkpunten">%s</ul>
      </div>
      <div class="fx-verz__checkvak">
        <noscript><p class="fx-verz__checkgeenjs">Dit hulpmiddel werkt met JavaScript. Bel mij gerust op <a href="tel:+31630679790">06 30 67 97 90</a>, dan lopen we het samen door.</p></noscript>
        <div class="fx-verz__hulp" id="fxAdvies" hidden>
          <fieldset class="fx-verz__vraag fx-verz__vraag--vink">
            <legend>%s</legend>
            %s
          </fieldset>
          <div class="fx-verz__hulpuit" id="fxAdviesUit" aria-live="polite"><p>Vink aan wat voor uw bedrijf geldt. Dan ziet u hier welke verzekeringen ik met u zou bekijken.</p></div>
          %s
        </div>
      </div>
    </div>
    <script>
    (function(){
      var h=document.getElementById('fxAdvies'), u=document.getElementById('fxAdviesUit'); if(!h||!u) return;
      h.hidden=false; var leeg=u.innerHTML, bx=[].slice.call(h.querySelectorAll('input[type=checkbox]'));
      function toon(){ var a=bx.filter(function(b){return b.checked;});
        if(!a.length){ u.innerHTML=leeg; u.classList.remove('is-uit'); return; }
        u.innerHTML='<span class="fx-verz__lijstkop">Dit zou ik met u bekijken</span><ul class="fx-verz__lijst">'+
          a.map(function(b){return '<li>'+b.getAttribute('data-advies')+'</li>';}).join('')+'</ul>';
        u.classList.add('is-uit'); }
      bx.forEach(function(b){ b.addEventListener('change',toon); });
    })();
    </script>
  </section></div>

''' % (sub, kop, intro, pl, vraagkop, it, KNOPPEN.format(u=knop[1], t=knop[0]))


# ================================================================ bedrijfsaansprakelijkheid
AVB_HULP = scenario_blok(
    'Test uzelf', 'Bedrijfs- of beroepsaansprakelijkheid?',
    'Zes situaties uit de praktijk van ondernemers. Welke verzekering betaalt? Denk eerst zelf na en bekijk dan het antwoord.',
    [('Een schilder stoot bij een klant thuis een dure vaas om.', 'wel', 'Bedrijfsaansprakelijkheid',
      'Schade aan spullen van een ander, veroorzaakt tijdens uw werk. Dat is precies waarvoor een AVB bedoeld is.'),
     ('Een klant struikelt in uw werkplaats over een snoer en breekt zijn pols.', 'wel', 'Bedrijfsaansprakelijkheid',
      'Letsel bij een ander valt ook onder de AVB, net als de kosten die daaruit volgen, zoals een behandeling of gemist inkomen.'),
     ('Een adviseur maakt een rekenfout, waardoor de klant geld misloopt.', 'let', 'Beroepsaansprakelijkheid',
      'Er is niets kapot en niemand gewond, maar de klant lijdt financiële schade door een fout in uw werk. Daarvoor is een beroepsaansprakelijkheidsverzekering.'),
     ('Een installateur sluit een leiding verkeerd aan en er ontstaat waterschade.', 'wel', 'Meestal bedrijfsaansprakelijkheid',
      'De waterschade bij de klant valt meestal onder de AVB. Het opnieuw aansluiten van de leiding, dus het herstel van uw eigen werk, betaalt u zelf.'),
     ('U werkt met een machine van uw opdrachtgever en die gaat kapot.', 'let', 'Alleen met opzichtdekking',
      'Spullen die u in uw zorg heeft, heten zaken in opzicht. Veel polissen sluiten die uit, of verzekeren ze maar tot een beperkt bedrag. Soms kunt u het bijverzekeren.'),
     ('U levert een opdracht te laat op en uw klant mist daardoor omzet.', 'niet', 'Meestal niet verzekerd',
      'Te laat of niet leveren is een ondernemersrisico. Dat valt meestal buiten zowel de AVB als de beroepsaansprakelijkheidsverzekering.')],
    'Dit geldt in de meeste gevallen. De precieze dekking verschilt per verzekeraar en per branche. Twijfelt u over uw eigen polis? <a href="tel:+31630679790">Bel mij</a>, dan kijk ik het na.')

AVB_TEKST = kort(['De AVB betaalt schade die u of uw personeel bij een ander veroorzaakt: aan spullen of aan personen.',
                  'Een fout in uw advies of ontwerp valt daar niet onder. Daarvoor is een beroepsaansprakelijkheidsverzekering.',
                  'Uw particuliere aansprakelijkheidsverzekering dekt geen schade die u tijdens uw werk veroorzaakt.']) + '''      <h2>Wat is een bedrijfsaansprakelijkheidsverzekering?</h2>
      <p>Als ondernemer bent u aansprakelijk voor schade die u, uw personeel of uw producten bij anderen veroorzaken. Een bedrijfsaansprakelijkheidsverzekering, kortweg AVB, betaalt die schade. Het gaat om twee soorten schade: schade aan spullen van een ander, en letsel bij een ander. Ook de kosten van een advocaat om een onterechte claim af te wijzen zitten er meestal in.</p>
      <p>Uw particuliere <a href="../verzekeringen/aansprakelijkheidsverzekering/">aansprakelijkheidsverzekering</a> helpt u hier niet. Die sluit schade tijdens uw werk juist uit. Ook als zzp'er heeft u dus een aparte verzekering nodig.</p>

      <h2>Wat is wel en niet verzekerd?</h2>
''' + welniet(
        ['Schade aan spullen of gebouwen van klanten en anderen', 'Letsel bij klanten, bezoekers of voorbijgangers',
         'Letsel van uw eigen personeel tijdens het werk (werkgeversaansprakelijkheid)', 'Schade door een product dat u levert of maakt',
         'Kosten van verweer tegen een claim'],
        ['Financiële schade door een fout in uw advies of ontwerp', 'Het herstel van uw eigen werk', 'Schade die u met opzet veroorzaakt',
         'Te laat of niet leveren', 'Boetes en schade aan uw eigen spullen'], nietkop='Meestal niet verzekerd') + '''
      <h2>Bedrijfs- of beroepsaansprakelijkheid?</h2>
      <p>Het verschil zit in het soort schade. De bedrijfsaansprakelijkheidsverzekering is er voor schade die u kunt zien: iets gaat kapot of iemand raakt gewond. De beroepsaansprakelijkheidsverzekering is er voor financiële schade door een fout in uw vak, zoals een verkeerd advies, een rekenfout of een gebrekkig ontwerp.</p>
      <table class="fx-verz__tabel">
        <thead><tr><td></td><th>Bedrijfs&shy;aansprakelijkheid (AVB)</th><th>Beroeps&shy;aansprakelijkheid (BAV)</th></tr></thead>
        <tbody>
          <tr><th>Soort schade</th><td>Schade aan spullen en letsel bij anderen</td><td>Financiële schade door een fout in uw werk</td></tr>
          <tr><th>Voorbeeld</th><td>Een schilder beschadigt de vloer van een klant</td><td>Een adviseur geeft een advies dat de klant geld kost</td></tr>
          <tr><th>Voor wie</th><td>Bijna elke ondernemer, zeker bij klanten op locatie</td><td>Adviseurs, ontwerpers, ICT, zorg en andere kenniswerkers</td></tr>
        </tbody>
      </table>
      <p>Veel ondernemers hebben er één nodig, sommigen allebei. Een interieurontwerper die ook zelf meubels plaatst, kan zowel een kras in een vloer als een fout in een ontwerp maken.</p>

      <h2>Waar moet u op letten?</h2>
      <h3>Het verzekerde bedrag</h3>
      <p>Verzekerde bedragen van 1,25 of 2,5 miljoen euro per aanspraak zijn gebruikelijk. Werkt u voor grotere opdrachtgevers, dan eisen die soms een hoger bedrag. Kijk dus ook in uw contracten.</p>
      <h3>Opzicht: spullen die u onder u heeft</h3>
      <p>Werkt u met machines, gereedschap of materiaal van uw opdrachtgever? Dan zijn die vaak niet of maar beperkt verzekerd. Bij veel verzekeraars kunt u een opzichtdekking bijsluiten.</p>
      <h3>De juiste omschrijving van uw werk</h3>
      <p>De verzekeraar gaat uit van de werkzaamheden die op de polis staan. Doet u inmiddels meer of ander werk dan toen u de verzekering afsloot? Laat het aanpassen, anders kunt u bij schade voor een verrassing komen te staan.</p>
      <h3>Eigen risico</h3>
      <p>Een hoger eigen risico maakt de premie lager. Kies een bedrag dat u bij een kleine schade zonder moeite zelf kunt betalen.</p>'''

AVB_VR = [
    ('Is een bedrijfsaansprakelijkheidsverzekering verplicht?',
     'Niet volgens de wet. Wel vragen veel opdrachtgevers, brancheverenigingen en verhuurders erom. En zonder verzekering betaalt u een claim uit eigen zak, wat voor een kleine onderneming het einde kan betekenen.'),
    ("Heb ik als zzp'er zonder personeel een AVB nodig?",
     'Meestal wel. Ook als u alleen werkt, kunt u schade bij klanten of anderen veroorzaken. Uw particuliere aansprakelijkheidsverzekering dekt geen schade tijdens uw werk.'),
    ('Wat is het verschil tussen een AVB en een BAV?',
     'De AVB is voor schade aan spullen en letsel bij anderen. De BAV, de beroepsaansprakelijkheidsverzekering, is voor financiële schade door een fout in uw werk, zoals een verkeerd advies of een rekenfout.'),
    ('Is schade aan mijn eigen werk verzekerd?',
     'Nee. Het opnieuw doen of herstellen van uw eigen werk betaalt u zelf. Wel kan de schade die daaruit volgt bij de klant verzekerd zijn, zoals waterschade na een verkeerd aangesloten leiding.'),
    ('Is mijn personeel ook verzekerd?',
     'Ja. Schade die uw medewerkers tijdens hun werk bij anderen veroorzaken, valt onder de AVB. Ook uw aansprakelijkheid als werkgever, bijvoorbeeld bij letsel van een medewerker tijdens het werk, zit er meestal in.'),
    ('Geldt de verzekering ook als ik in het buitenland werk?',
     'Dat verschilt per polis. Vaak geldt de dekking in Europa, maar werk in de Verenigde Staten of Canada is meestal uitgesloten of alleen tegen een hogere premie te verzekeren.'),
    ('Wat kost een bedrijfsaansprakelijkheidsverzekering?',
     'Dat hangt af van uw branche, de omvang van uw bedrijf, het verzekerde bedrag en het eigen risico. Een bouwbedrijf betaalt meer dan een tekstschrijver. Ik vraag offertes op bij verschillende verzekeraars en zet ze voor u naast elkaar.'),
]

AVB_EIGEN = dict(
    schade=schade('Een claim van een klant?',
        'Een klant stelt u aansprakelijk voor schade. Zo pakt u het goed aan:',
        ['Erken niet zelf schriftelijk dat u aansprakelijk bent. Dat beoordeelt de verzekeraar.',
         'Leg vast wat er is gebeurd, met foto\'s, datum en namen van betrokkenen.',
         'Bewaar de aansprakelijkstelling, offertes en facturen.',
         'Bel mij voordat u iets toezegt of betaalt.'],
        'Ik meld de schade bij de verzekeraar en denk met u mee over hoe u uw klant op de hoogte houdt. Zo blijft de relatie met uw klant zo goed mogelijk.'),
    werk=werkwijze('Zo regel ik uw aansprakelijkheid', 'Van de eerste kennismaking tot de jaren daarna. Het eerste gesprek kost u niets.',
        [('Kennismaken op uw bedrijf', 'Ik wil zien wat u doet, waar u werkt en voor wie. Dat bepaalt welke risico\'s er zijn.'),
         ('Risico\'s op een rij', 'We kijken samen of u een AVB, een BAV of allebei nodig heeft, en welk verzekerd bedrag past.'),
         ('Vergelijken en advies', 'Ik vraag offertes op en let op opzicht, uitsluitingen en eigen risico.'),
         ('Regelen en bijhouden', 'Groeit uw bedrijf of verandert uw werk, dan passen we de polis aan.')]),
    review=reviews('Wat ondernemers zeggen', 'Een vaste adviseur die meedenkt, ook als uw bedrijf verandert.', [REVIEW_MARITA, REVIEW_KYRA, REVIEW_TONY]),
    wie=wie('Uw adviseur voor ondernemers',
        'Mijn naam is Fred Koeling. Ik help ondernemers en zzp\'ers in Apeldoorn en omgeving met hun zakelijke verzekeringen, en kijk daarbij ook naar uw privésituatie.',
        'Ik werk sinds 2015 als zelfstandig adviseur, met ruim 22 jaar ervaring. Ik weet dus uit eigen ervaring hoe het is om een bedrijf te runnen.',
        'Een goede polis past bij wat u echt doet, niet bij wat er ooit op papier stond.'),
    zij='Twijfelt u of u een AVB, een BAV of allebei nodig heeft? Bel of mail mij. Het eerste gesprek is gratis.',
    vragenintro='Nog een vraag over aansprakelijkheid voor uw bedrijf? Bel gerust, daar hoeft u geen afspraak voor te maken.',
    contact=('Uw aansprakelijkheid goed geregeld?', 'Ik kom bij u langs op uw bedrijf in Apeldoorn en omgeving. Dan zie ik meteen wat u doet en welke risico\'s erbij horen.'))

AVB_DUO = duo('dienst-zakelijk.jpg', 'Ondernemer en medewerker overleggen in een magazijn', 1261, 840,
    'Mijn aanpak', 'Hoe ik u help',
    '      <p>Een aansprakelijkheidsverzekering is pas goed als de omschrijving klopt met wat u echt doet. Daar begin ik dus mee.</p>',
    ['Ik kijk welke werkzaamheden u doet, en of die goed op de polis staan.',
     'Ik zoek uit of u naast een AVB ook een BAV nodig heeft.',
     'Ik let op opzicht, werken in het buitenland en eisen van uw opdrachtgevers.',
     'Bij een claim help ik u, en houd ik het contact met de verzekeraar.'],
    ('Vraag een zakelijke polischeck aan', '../zakelijk/#polischeck'))

# ================================================================ AOV
AOV_HULP = '''  <!-- hulpmiddel -->
  <div class="fx-ct__wrap"><section class="fx-ct__sec fx-verz__checksec" id="hulp">
    <div class="fx-verz__checkkaart">
      <div class="fx-verz__checkintro">
        <p class="fx-ct__sub">Rekenhulp</p>
        <h2>Hoe lang kunt u zonder inkomen?</h2>
        <p>De wachttijd is de periode waarin u nog geen uitkering krijgt. Hoe langer die is, hoe lager de premie. Maar u moet die periode wel zelf kunnen overbruggen.</p>
        <ul class="fx-verz__checkpunten"><li>Twee schuifjes</li><li>Direct antwoord</li><li>Niets invullen</li></ul>
      </div>
      <div class="fx-verz__checkvak">
        <noscript><p class="fx-verz__checkgeenjs">Deze rekenhulp werkt met JavaScript. Bel mij gerust op <a href="tel:+31630679790">06 30 67 97 90</a>, dan rekenen we het samen uit.</p></noscript>
        <div class="fx-verz__hulp" id="fxReken" hidden>
          <div class="fx-zak__schuif">
            <label for="fxLasten">Uw vaste lasten per maand, zakelijk en privé</label>
            <output id="fxLastenUit" for="fxLasten">&euro;&nbsp;2.500</output>
            <input type="range" id="fxLasten" min="500" max="8000" step="100" value="2500">
          </div>
          <div class="fx-zak__schuif">
            <label for="fxBuffer">Uw spaargeld of buffer</label>
            <output id="fxBufferUit" for="fxBuffer">&euro;&nbsp;10.000</output>
            <input type="range" id="fxBuffer" min="0" max="100000" step="1000" value="10000">
          </div>
          <div class="fx-verz__hulpuit is-uit" id="fxRekenUit" aria-live="polite"></div>
          <p class="fx-verz__klein">Dit is een vuistregel, geen advies. Ook uw partner, uw inkomen en de premie spelen mee.</p>
          ''' + KNOPPEN.format(u='tel:+31630679790', t='Reken het met mij door') + '''
        </div>
      </div>
    </div>
    <script>
    (function(){
      var h=document.getElementById('fxReken'); if(!h) return; h.hidden=false;
      var l=document.getElementById('fxLasten'), b=document.getElementById('fxBuffer'), u=document.getElementById('fxRekenUit');
      function eur(x){return '\\u20ac\\u00a0'+Math.round(x).toString().replace(/\\B(?=(\\d{3})+(?!\\d))/g,'.');}
      function reken(){
        var maanden=b.value/l.value, w, r;
        [l,b].forEach(function(x){x.style.setProperty('--p',((x.value-x.min)/(x.max-x.min)*100)+'%');});
        document.getElementById('fxLastenUit').textContent=eur(l.value);
        document.getElementById('fxBufferUit').textContent=eur(b.value);
        if(maanden>=12){w='een jaar'; r='U kunt een jaar of langer zonder inkomen. Een lange wachttijd scheelt flink in premie.';}
        else if(maanden>=3){w='90 dagen'; r='U kunt een paar maanden overbruggen. Een wachttijd van drie maanden is voor veel ondernemers een goede balans.';}
        else if(maanden>=1){w='30 dagen'; r='Uw buffer is beperkt. Een korte wachttijd geeft u meer zekerheid, al is de premie dan hoger.';}
        else {w='14 dagen of korter'; r='U heeft weinig buffer. Kies een korte wachttijd en bouw als het kan een buffer op.';}
        var m=Math.floor(maanden*10)/10;
        u.innerHTML='<p><span class="fx-verz__lijstkop">Uw buffer is genoeg voor ongeveer</span><b class="fx-verz__dekking">'+(m<1?'minder dan een maand':(m.toString().replace('.',',')+' maanden'))+'</b>'+
          r+' Een wachttijd van <b>'+w+'</b> past daarbij.</p>';
      }
      l.addEventListener('input',reken); b.addEventListener('input',reken); reken();
    })();
    </script>
  </section></div>

'''

AOV_TEKST = kort(['Een AOV keert uit als u als ondernemer door ziekte of een ongeval niet kunt werken.',
                  'U kiest zelf het verzekerde bedrag, de wachttijd en tot welke leeftijd u verzekerd bent.',
                  'Er komt een verplichte basisverzekering voor zelfstandigen, maar naar verwachting niet voor 2030.']) + '''      <h2>Waarom een AOV?</h2>
      <p>Werknemers krijgen bij ziekte loon doorbetaald en kunnen daarna terugvallen op een uitkering. Als zelfstandig ondernemer heeft u dat niet. Kunt u door ziekte of een ongeval niet werken, dan stopt uw inkomen. Uw vaste lasten, zoals uw hypotheek en de kosten van uw bedrijf, lopen wel door.</p>
      <p>Een arbeidsongeschiktheidsverzekering, kortweg AOV, vult dat gat. U ontvangt een maandelijkse uitkering zolang u niet of maar deels kunt werken, tot de eindleeftijd die u kiest.</p>

      <h2>De keuzes die de premie bepalen</h2>
      <h3>Het verzekerde bedrag</h3>
      <p>U verzekert een bedrag per jaar, meestal tot ongeveer 80 procent van uw gemiddelde winst. Kijk vooral naar wat u nodig heeft om uw vaste lasten te betalen.</p>
      <h3>De wachttijd</h3>
      <p>Dit is de periode waarin u nog geen uitkering krijgt, vaak 14 dagen, een maand, drie maanden of een jaar. Hoe langer de wachttijd, hoe lager de premie. Met de rekenhulp hierboven ziet u welke wachttijd bij uw buffer past.</p>
      <h3>Wanneer bent u arbeidsongeschikt?</h3>
      <p>Dit is de belangrijkste keuze en het meest onderschatte verschil tussen polissen.</p>
      <ul>
        <li><b>Beroepsarbeidsongeschiktheid:</b> u krijgt een uitkering als u uw eigen beroep niet meer kunt doen. Dit is de ruimste en duurste dekking.</li>
        <li><b>Passende arbeid:</b> u krijgt geen uitkering als u nog ander werk kunt doen dat past bij uw opleiding en ervaring.</li>
        <li><b>Gangbare arbeid:</b> u krijgt alleen een uitkering als u vrijwel geen enkel werk meer kunt doen. Goedkoper, maar veel beperkter.</li>
      </ul>
      <h3>De eindleeftijd</h3>
      <p>Tot welke leeftijd loopt de verzekering? Een eindleeftijd tot uw AOW-leeftijd geeft de meeste zekerheid. Een lagere eindleeftijd maakt de premie lager.</p>

      <h2>De verplichte basisverzekering voor zelfstandigen</h2>
      <p>De overheid werkt aan een verplichte basisverzekering arbeidsongeschiktheid voor zelfstandigen, de BAZ. Het wetsvoorstel is in maart 2026 ingediend. De invoering wordt niet voor 2030 verwacht. De BAZ keert straks pas uit na twee jaar ziekte, en dan hooguit op het niveau van het minimumloon. Wilt u meer zekerheid, of eerder verzekerd zijn, dan blijft een eigen AOV nodig. Ik houd de ontwikkelingen voor u in de gaten.</p>

      <h2>Alternatieven</h2>
      <p>Een AOV is niet de enige oplossing. Een broodfonds, waarin ondernemers elkaar bij ziekte tijdelijk ondersteunen, keert maximaal twee jaar uit. Een eigen buffer helpt vooral bij kortere uitval. Soms is een combinatie het beste. Ik zet de mogelijkheden eerlijk voor u naast elkaar.</p>'''

AOV_VR = [
    ("Is een AOV verplicht voor zzp'ers?",
     'Nu nog niet. Er komt naar verwachting een verplichte basisverzekering voor zelfstandigen, de BAZ. Het wetsvoorstel is in maart 2026 ingediend en invoering wordt niet voor 2030 verwacht.'),
    ('Is de premie van een AOV aftrekbaar?',
     'Ja, de premie is aftrekbaar van uw inkomen in box 1. Daar staat tegenover dat een uitkering belast is. Uw boekhouder kan dit voor uw situatie bevestigen.'),
    ('Wat is een wachttijd?',
     'De wachttijd, ook wel eigenrisicoperiode, is de periode waarin u nog geen uitkering krijgt. Vaak kiest u tussen 14 dagen, een maand, drie maanden of een jaar. Hoe langer de wachttijd, hoe lager de premie.'),
    ('Kan ik een AOV afsluiten als ik niet helemaal gezond ben?',
     'Meestal wel, maar de verzekeraar kan dan een uitsluiting maken, bijvoorbeeld voor rugklachten, of een hogere premie vragen. Vul de gezondheidsverklaring altijd eerlijk in. Ik help u daarbij en kijk welke verzekeraar het beste bij uw situatie past.'),
    ('Wat is het verschil tussen beroeps- en gangbare arbeidsongeschiktheid?',
     'Bij beroepsarbeidsongeschiktheid krijgt u een uitkering als u uw eigen vak niet meer kunt doen. Bij gangbare arbeid alleen als u vrijwel geen enkel werk meer kunt doen. Het eerste is ruimer en duurder.'),
    ('Wat is een broodfonds?',
     'Een broodfonds is een groep ondernemers die elkaar bij ziekte maandelijks een schenking geven, maximaal twee jaar lang. Het is betaalbaar en persoonlijk, maar het dekt geen lange uitval. Daarom combineren sommige ondernemers het met een AOV met een lange wachttijd.'),
    ('Kan ik mijn AOV aanpassen als mijn inkomen verandert?',
     'Ja. Verdient u meer of minder dan toen u de verzekering afsloot, dan kunt u het verzekerde bedrag aanpassen. Bij sommige verzekeraars kunt u de dekking ook tijdelijk verlagen als het even tegenzit.'),
]

AOV_EIGEN = dict(
    licht=True,
    schade=schade('Ziek en kunt u niet werken?',
        'Meld het op tijd, dan voorkomt u gedoe met uw uitkering:',
        ['Meld uw arbeidsongeschiktheid zo snel mogelijk bij de verzekeraar. Een te late melding kan uw uitkering vertragen.',
         'Ga naar uw huisarts of specialist en bewaar de verslagen.',
         'Houd bij welk werk u nog wel kunt doen, en hoeveel uur.',
         'Bel mij, dan help ik u door de stappen heen.'],
        'Bij een uitkering komt veel kijken: een medisch onderzoek, gesprekken met een arbeidsdeskundige en uw boekhouding. Ik blijf in die periode uw aanspreekpunt.'),
    werk=werkwijze('Zo regel ik uw AOV', 'Een AOV sluit u voor lange tijd af. Daarom neem ik er de tijd voor. Het eerste gesprek kost u niets.',
        [('Kennismaken', 'U vertelt over uw werk, uw inkomen en uw vaste lasten, zakelijk en privé.'),
         ('Rekenen', 'We bepalen samen welk bedrag, welke wachttijd en welke eindleeftijd bij u passen.'),
         ('Vergelijken en advies', 'Ik vergelijk verzekeraars op voorwaarden en premie, en kijk ook naar een broodfonds of een combinatie.'),
         ('Regelen en bijhouden', 'Ik help bij de gezondheidsverklaring en kijk elk jaar of de dekking nog past bij uw inkomen.')]),
    review=reviews('Klanten over mijn advies', 'Bij een AOV draait het om vertrouwen en goede uitleg. Dat is wat klanten noemen.', [REVIEW_LARS, REVIEW_MARITA, REVIEW_FLEUR]),
    wie=wie('Advies dat verder kijkt dan de polis',
        'Mijn naam is Fred Koeling. Als Certified Financial Planner kijk ik bij een AOV niet alleen naar de premie, maar naar uw hele financiële situatie.',
        'Zo houd ik rekening met uw hypotheek, uw pensioen en uw buffer. Ik werk sinds 2015 als zelfstandig adviseur.',
        'Een goede AOV is er niet voor nu, maar voor de dag dat u hem nodig heeft.'),
    zij='Twijfelt u over de hoogte van uw dekking of de wachttijd? Bel of mail mij. Het eerste gesprek is gratis.',
    vragenintro='Nog een vraag over uw AOV? Bel gerust, daar hoeft u geen afspraak voor te maken.',
    contact=('Uw inkomen goed beschermd?', 'Ik kom bij u langs op uw bedrijf of thuis in Apeldoorn en omgeving, of we spreken online af.'))

AOV_DUO = duo('dienst-aov.jpg', 'Ambachtsman aan het werk in zijn werkplaats', 1260, 840,
    'Mijn aanpak', 'Hoe ik u help',
    '      <p>AOV-polissen verschillen sterk in hun voorwaarden. Het verschil merkt u pas als u ziek wordt. Daarom lees ik de kleine letters voor u.</p>',
    ['Ik reken uit welk bedrag u echt nodig heeft, zakelijk en privé.',
     'Ik let op de definitie van arbeidsongeschiktheid en op uitsluitingen.',
     'Ik zet een AOV, een broodfonds en een combinatie eerlijk naast elkaar.',
     'Ik help u bij de gezondheidsverklaring, zodat die volledig en juist is.'],
    ('Plan een gratis gesprek', '../contact/'))

# ================================================================ bedrijfspand en inventaris
PAND_HULP = advieslijst(
    'Snelle check', 'Wat moet u verzekeren?',
    'Elk bedrijf is anders. Vink aan wat bij uw bedrijf hoort. Dan ziet u welke verzekeringen ik met u zou bekijken.',
    ['Zeven punten', 'Direct een lijst', 'Niets invullen'],
    'Wat geldt voor uw bedrijf?',
    [('Ik heb een eigen bedrijfspand', '<b>Opstalverzekering</b> voor het pand zelf, op basis van de herbouwwaarde.'),
     ('Ik huur een pand en heb het zelf verbouwd', '<b>Huurdersbelang</b> voor uw verbouwing aan het gehuurde pand.'),
     ('Ik heb machines, computers of inrichting', '<b>Inventarisverzekering</b> voor alles wat u gebruikt om uw werk te doen.'),
     ('Ik heb voorraad of spullen van klanten', '<b>Goederenverzekering</b> voor uw voorraad, en eventueel voor spullen van klanten.'),
     ('Mijn bedrijf ligt stil als het pand onbruikbaar is', '<b>Bedrijfsschadeverzekering</b> voor doorlopende kosten en gemiste winst.'),
     ('Ik heb grote ruiten of lichtreclame', '<b>Glas en lichtreclame</b>, als dat nog niet in uw polis zit.'),
     ('Ik werk met klantgegevens of een webshop', '<b>Cyberverzekering</b> voor hulp en schade na een hack of datalek.')],
    ('Vraag een zakelijke polischeck aan', '../zakelijk/#polischeck'))

PAND_TEKST = kort(['De opstalverzekering is voor het gebouw, de inventarisverzekering voor alles erin.',
                   'Een bedrijfsschadeverzekering vergoedt doorlopende kosten en gemiste winst als uw bedrijf stilligt.',
                   'Werkt u vanuit huis? Dan zijn uw zakelijke spullen vaak maar beperkt verzekerd op uw inboedelverzekering.']) + '''      <h2>Drie verzekeringen die bij elkaar horen</h2>
      <p>Bij een brand, een storm of een inbraak in uw bedrijf gaat het om drie soorten schade: aan het gebouw, aan wat erin staat en aan uw inkomsten zolang u niet kunt werken. Voor elk daarvan is een eigen verzekering. Samen zorgen ze ervoor dat u na een grote schade weer verder kunt.</p>
      <table class="fx-verz__tabel">
        <thead><tr><td></td><th>Wat is verzekerd</th><th>Voor wie</th></tr></thead>
        <tbody>
          <tr><th>Opstal (bedrijfspand)</th><td>Het gebouw zelf, met vaste onderdelen zoals installaties en de pui</td><td>Eigenaren van een bedrijfspand</td></tr>
          <tr><th>Inventaris en goederen</th><td>Inrichting, machines, computers, gereedschap en voorraad</td><td>Elke ondernemer met spullen, ook huurders</td></tr>
          <tr><th>Bedrijfsschade</th><td>Doorlopende kosten en gemiste winst na een verzekerde schade</td><td>Ondernemers die afhankelijk zijn van hun pand of machines</td></tr>
        </tbody>
      </table>

      <h2>Opstal: uw bedrijfspand</h2>
      <p>De opstalverzekering vergoedt schade aan het pand zelf, bijvoorbeeld na brand, storm of waterschade. Het verzekerde bedrag is de herbouwwaarde: wat het kost om het pand opnieuw te bouwen. Heeft u een zakelijke hypotheek, dan vraagt de geldverstrekker bijna altijd om deze verzekering. Laat de herbouwwaarde eens in de paar jaar nakijken, zeker na een verbouwing.</p>

      <h2>Inventaris en goederen</h2>
      <p>Onder inventaris valt alles wat u gebruikt om uw werk te doen: inrichting, machines, computers en gereedschap. Goederen zijn uw voorraad, en soms ook spullen van klanten die bij u liggen. Huurt u een pand en heeft u het zelf verbouwd, bijvoorbeeld met een nieuwe vloer of een keuken? Dat heet huurdersbelang en kunt u meeverzekeren.</p>
      <p>Werkt u vanuit huis? Dan zijn uw laptop, gereedschap of voorraad vaak maar beperkt verzekerd op uw particuliere <a href="../verzekeringen/woonverzekering/">inboedelverzekering</a>. Kijk na wat er in de voorwaarden staat over zakelijke spullen.</p>

      <h2>Bedrijfsschade: als uw bedrijf stilligt</h2>
      <p>Na een brand duurt het vaak maanden voordat u weer volledig aan het werk bent. In die tijd lopen uw huur, salarissen en leningen gewoon door, terwijl uw omzet wegvalt. Een bedrijfsschadeverzekering vergoedt die doorlopende kosten en de winst die u misloopt. Voorwaarde is wel dat de stilstand komt door een schade die zelf verzekerd is, zoals brand of storm.</p>

      <h2>Waar moet u op letten?</h2>
      <h3>Onderverzekering</h3>
      <p>Is het verzekerde bedrag lager dan de werkelijke waarde, dan krijgt u bij schade maar een deel vergoed. Groeit uw bedrijf, schaft u nieuwe machines aan of heeft u meer voorraad? Laat de bedragen dan aanpassen.</p>
      <h3>Beveiliging</h3>
      <p>Verzekeraars stellen vaak eisen aan sloten en alarm, zeker bij een winkel of een werkplaats met waardevolle spullen. Voldoet u daar niet aan, dan kan een inbraak niet of maar deels vergoed worden.</p>
      <h3>De uitkeringstermijn bij bedrijfsschade</h3>
      <p>Hoe lang vergoedt de verzekeraar uw kosten en gemiste winst? Vaak is dat een jaar. Zou het herstel bij u langer duren, bijvoorbeeld omdat u speciale machines heeft, kies dan een langere termijn.</p>'''

PAND_VR = [
    ('Wat is het verschil tussen inventaris en goederen?',
     'Inventaris is wat u gebruikt om uw werk te doen, zoals inrichting, machines en computers. Goederen zijn uw voorraad: wat u verkoopt of verwerkt. Beide kunt u op één polis verzekeren.'),
    ('Heb ik als huurder van een bedrijfspand een opstalverzekering nodig?',
     'Meestal niet, die sluit de eigenaar af. Wel heeft u een inventarisverzekering nodig, en eventueel een verzekering voor huurdersbelang als u het pand zelf heeft verbouwd. Kijk ook in uw huurcontract wat er van u verwacht wordt.'),
    ('Wat vergoedt een bedrijfsschadeverzekering?',
     'Doorlopende kosten, zoals huur, salarissen en rente, en de winst die u misloopt doordat uw bedrijf stilligt. Voorwaarde is dat de stilstand komt door een verzekerde schade, zoals brand.'),
    ('Zijn mijn zakelijke spullen thuis verzekerd?',
     'Op uw particuliere inboedelverzekering vaak maar beperkt, en soms helemaal niet. Werkt u vanuit huis met dure apparatuur of voorraad, dan is een aparte inventarisverzekering verstandig.'),
    ('Is mijn gereedschap ook verzekerd als het in de bus ligt?',
     'Op een inventarisverzekering vaak niet of maar beperkt. Voor gereedschap en materiaal onderweg is een eigen vervoer- of gereedschapsverzekering. Zie ook de pagina over de <a href="../zakelijk/bedrijfsautoverzekering/">bedrijfsauto</a>.'),
    ('Hoe bepaal ik de waarde van mijn inventaris?',
     'Ga uit van wat het kost om alles nieuw te kopen, niet van de boekwaarde. Een lijst met uw belangrijkste spullen en aankoopbedragen helpt. Ik loop die graag met u door.'),
    ('Is een cyberverzekering nodig voor een klein bedrijf?',
     'Werkt u met klantgegevens, een webshop of online betalingen, dan is het het overwegen waard. Een cyberverzekering helpt bij een hack of datalek, met de kosten van herstel en hulp van specialisten.'),
]

PAND_EIGEN = dict(
    schade=schade('Brand, storm of inbraak in uw bedrijf?',
        'Na een grote schade telt elke dag. Dit kunt u meteen doen:',
        ['Zorg eerst voor de veiligheid van uzelf, uw personeel en uw klanten.',
         'Beperk de schade als dat veilig kan, en doe bij inbraak aangifte bij de politie.',
         'Maak foto\'s en bewaar kapotte spullen, facturen en uw voorraadlijst.',
         'Bel mij zo snel mogelijk, ook buiten kantoortijd via de voicemail.'],
        'Bij een grote schade stuurt de verzekeraar vaak een expert. Ik help u bij dat contact, en kijk mee of de vergoeding voor gebouw, inventaris en bedrijfsschade klopt.'),
    werk=werkwijze('Zo regel ik uw bedrijfspand en inventaris', 'Van de eerste kennismaking tot de jaren daarna. Het eerste gesprek kost u niets.',
        [('Kennismaken op uw bedrijf', 'Ik kom kijken: uw pand, uw inrichting, uw voorraad en hoe uw bedrijf draait.'),
         ('Waarden bepalen', 'We bepalen samen de herbouwwaarde, de waarde van uw inventaris en hoe lang herstel zou duren.'),
         ('Vergelijken en advies', 'Ik vergelijk verzekeraars op dekking, beveiligingseisen en premie.'),
         ('Regelen en bijhouden', 'Groeit uw bedrijf, dan passen we de verzekerde bedragen aan.')]),
    review=reviews('Ondernemers over mijn advies', 'Een vaste adviseur die meedenkt en bereikbaar blijft, ook na het afsluiten.', [REVIEW_KYRA, REVIEW_LARS, REVIEW_MARITA]),
    wie=wie('Een adviseur die uw bedrijf kent',
        'Mijn naam is Fred Koeling. Ik kom graag bij u langs, want een bedrijf leer ik pas echt kennen als ik er rondloop.',
        'Ik werk sinds 2015 als zelfstandig adviseur, met ruim 22 jaar ervaring, voor ondernemers in Apeldoorn en omgeving.',
        'Na een brand wilt u maar één ding: zo snel mogelijk weer open. Daar richt ik uw verzekeringen op in.'),
    zij='Twijfelt u of uw pand, inventaris of voorraad goed verzekerd is? Bel of mail mij. Het eerste gesprek is gratis.',
    vragenintro='Nog een vraag over uw bedrijfspand of inventaris? Bel gerust, daar hoeft u geen afspraak voor te maken.',
    contact=('Uw bedrijf goed verzekerd?', 'Ik kom bij u langs op uw bedrijf in Apeldoorn en omgeving. Dan zie ik meteen wat er verzekerd moet worden.'))

PAND_DUO = duo('diensten-handtekening.jpg', 'Ondertekening van een verzekeringspolis', 1024, 683,
    'Mijn aanpak', 'Hoe ik u help',
    '      <p>De meeste schade aan bedrijven is goed verzekerd, tot blijkt dat de bedragen niet meer kloppen. Daarom begin ik bij de waarde van wat u heeft.</p>',
    ['Ik loop met u door uw pand en bepaal wat er verzekerd moet worden.',
     'Ik controleer de verzekerde bedragen, zodat u niet onderverzekerd bent.',
     'Ik let op beveiligingseisen en de uitkeringstermijn bij bedrijfsschade.',
     'Bij schade help ik u, en kijk ik mee of de vergoeding klopt.'],
    ('Vraag een zakelijke polischeck aan', '../zakelijk/#polischeck'))

# ================================================================ bedrijfsauto
AUTO_HULP = '''  <!-- hulpmiddel -->
  <div class="fx-ct__wrap"><section class="fx-ct__sec fx-verz__checksec" id="hulp">
    <div class="fx-verz__checkkaart">
      <div class="fx-verz__checkintro">
        <p class="fx-ct__sub">Voertuigwijzer</p>
        <h2>Wat heeft u nodig voor uw auto of bus?</h2>
        <p>Drie vragen over hoe u rijdt. Dan ziet u welke verzekeringen ik met u zou bekijken.</p>
        <ul class="fx-verz__checkpunten"><li>Drie vragen</li><li>Direct antwoord</li><li>Niets invullen</li></ul>
      </div>
      <div class="fx-verz__checkvak">
        <noscript><p class="fx-verz__checkgeenjs">Dit hulpmiddel werkt met JavaScript. Bel mij gerust op <a href="tel:+31630679790">06 30 67 97 90</a>, dan lopen we het samen door.</p></noscript>
        <form class="fx-verz__hulp" id="fxVoertuig" hidden>
          ''' + rij('voertuig', 'Waar rijdt u mee?', [('auto', 'Een personenauto'), ('bus', 'Een bestelbus'), ('meer', 'Meerdere voertuigen')]) + '''
          ''' + rij('naam', 'Op wiens naam staat het voertuig?', [('zaak', 'Op naam van de zaak'), ('prive', 'Privé, maar ik rijd ook zakelijk')]) + '''
          ''' + rij('lading', 'Vervoert u gereedschap of goederen?', [('ja', 'Ja'), ('nee', 'Nee')]) + '''
          <div class="fx-verz__hulpuit" id="fxVoertuigUit" aria-live="polite"><p>Beantwoord de drie vragen, dan ziet u hier wat ik met u zou bekijken.</p></div>
          ''' + KNOPPEN.format(u='tel:+31630679790', t='Bespreek het met mij') + '''
        </form>
      </div>
    </div>
    <script>
    (function(){
      var f=document.getElementById('fxVoertuig'), u=document.getElementById('fxVoertuigUit'); if(!f||!u) return;
      f.hidden=false; f.addEventListener('submit',function(e){e.preventDefault();});
      function w(n){var r=f.querySelector('input[name='+n+']:checked'); return r?r.value:'';}
      f.addEventListener('change',function(){
        var v=w('voertuig'), n=w('naam'), l=w('lading'); if(!v||!n||!l) return;
        var p=[];
        if(v==='meer') p.push('<b>Wagenparkverzekering:</b> al uw voertuigen op één polis, vaak met korting en één aanspreekpunt bij schade.');
        else if(v==='bus') p.push('<b>Bestelautoverzekering:</b> WA is verplicht, en afhankelijk van de leeftijd en waarde van de bus beperkt casco of allrisk.');
        else p.push('<b>Zakelijke autoverzekering:</b> WA is verplicht, en afhankelijk van de leeftijd en waarde van de auto beperkt casco of allrisk.');
        if(n==='prive') p.push('<b>Zakelijk gebruik doorgeven:</b> op een particuliere polis is zakelijk rijden niet altijd verzekerd. Controleer wat er op uw polis staat.');
        if(l==='ja') p.push('<b>Eigen vervoer- of gereedschapsverzekering:</b> gereedschap en goederen in uw auto of bus vallen meestal niet onder de autoverzekering.');
        p.push('<b>Schadeverzekering inzittenden:</b> voor letsel en schade van u en uw passagiers, ook als u zelf de schade veroorzaakt.');
        u.innerHTML='<span class="fx-verz__lijstkop">Dit zou ik met u bekijken</span><ul class="fx-verz__lijst">'+p.map(function(x){return '<li>'+x+'</li>';}).join('')+'</ul>';
        u.classList.add('is-uit');
      });
    })();
    </script>
  </section></div>

'''

AUTO_TEKST = kort(['Voor een auto of bus van de zaak heeft u een zakelijke autoverzekering nodig. WA is wettelijk verplicht.',
                   'Gereedschap en goederen in de bus zijn meestal niet verzekerd op de autoverzekering.',
                   'Heeft u meerdere voertuigen, dan is een wagenparkpolis vaak voordeliger en overzichtelijker.']) + '''      <h2>Welke verzekering heeft u nodig?</h2>
      <p>Staat een auto of bestelbus op naam van uw bedrijf, dan verzekert u die met een zakelijke autoverzekering. Net als bij een privéauto is WA wettelijk verplicht. Daarnaast kiest u voor beperkt casco of allrisk, afhankelijk van de leeftijd en de waarde van het voertuig.</p>
      <table class="fx-verz__tabel">
        <thead><tr><th>Dekking</th><th>Wat is verzekerd</th><th>Past vaak bij</th></tr></thead>
        <tbody>
          <tr><th>WA</th><td>Schade die u met uw auto of bus bij een ander veroorzaakt. Wettelijk verplicht.</td><td>Oudere voertuigen met een lage dagwaarde</td></tr>
          <tr><th>WA en beperkt casco</th><td>WA, plus schade aan uw eigen voertuig door onder meer diefstal, brand, storm en ruitschade.</td><td>Voertuigen van gemiddelde leeftijd</td></tr>
          <tr><th>Allrisk</th><td>WA en beperkt casco, plus schade die u zelf aan uw voertuig veroorzaakt.</td><td>Nieuwe voertuigen en voertuigen met lease of financiering</td></tr>
        </tbody>
      </table>
      <p>De keuze werkt hetzelfde als bij een <a href="../verzekeringen/autoverzekering/">particuliere autoverzekering</a>. Het verschil zit in de extra's die voor ondernemers belangrijk zijn.</p>

      <h2>Gereedschap en goederen in de bus</h2>
      <p>Dit is het punt dat het vaakst misgaat. De autoverzekering dekt de bus, maar meestal niet wat erin ligt. Wordt er 's nachts ingebroken en is uw gereedschap weg, dan betaalt de autoverzekering dat in de regel niet. Daarvoor is een eigen vervoer- of gereedschapsverzekering, of bij sommige verzekeraars een aanvullende dekking op de autopolis. Let op de eisen die verzekeraars stellen, bijvoorbeeld aan extra sloten of aan waar de bus 's nachts staat.</p>

      <h2>Een privéauto zakelijk gebruiken</h2>
      <p>Rijdt u met uw privéauto naar klanten? Dan staat de auto op uw naam en is een particuliere verzekering vaak voldoende. Controleer wel of zakelijk gebruik op uw polis staat, want niet elke verzekeraar dekt dat zonder meer. Een vergeten wijziging kan bij schade vervelende gevolgen hebben.</p>

      <h2>Meerdere voertuigen: een wagenparkpolis</h2>
      <p>Heeft uw bedrijf meerdere auto's of bussen, dan kunt u ze vaak samen verzekeren op één wagenparkpolis. Dat is overzichtelijker, en vaak voordeliger. Afhankelijk van de verzekeraar kan dat vanaf ongeveer drie tot vijf voertuigen. De premie hangt dan af van de schades van het hele wagenpark, niet van één bestuurder.</p>

      <h2>Schadevrije jaren</h2>
      <p>Bij een nieuwe zakelijke polis vraagt de verzekeraar naar uw schadeverleden. Of u schadevrije jaren van privé naar zakelijk kunt meenemen, verschilt per verzekeraar. Dat zoek ik voor u uit.</p>'''

AUTO_VR = [
    ('Is een zakelijke autoverzekering verplicht?',
     'WA is wettelijk verplicht voor elk voertuig met een Nederlands kenteken, ook als het op naam van uw bedrijf staat. Beperkt casco en allrisk zijn een eigen keuze, al eist een leasemaatschappij of financier vaak allrisk.'),
    ('Is mijn gereedschap in de bus verzekerd?',
     'Meestal niet op de autoverzekering. Daarvoor is een eigen vervoer- of gereedschapsverzekering, of soms een aanvullende dekking op de autopolis. Verzekeraars stellen vaak eisen aan sloten en aan waar de bus staat, zeker voor diefstal uit de bus.'),
    ('Kan ik met mijn privéauto zakelijk rijden?',
     'Ja, maar controleer of zakelijk gebruik op uw polis staat. Niet elke particuliere polis dekt dat zonder meer.'),
    ('Wat is een wagenparkpolis?',
     'Eén polis voor alle auto\'s en bussen van uw bedrijf. Dat is overzichtelijker en vaak voordeliger. Afhankelijk van de verzekeraar kan het vanaf ongeveer drie tot vijf voertuigen.'),
    ('Kan ik mijn schadevrije jaren meenemen naar een zakelijke polis?',
     'Dat verschilt per verzekeraar. Soms kan het, soms bouwt u op de zakelijke polis opnieuw op. Ik zoek uit wat voor u het gunstigst is.'),
    ('Wie mag er in de bedrijfsauto rijden?',
     'Meestal mag iedereen met een geldig rijbewijs en toestemming van het bedrijf rijden. Voor jonge bestuurders geldt vaak een hoger eigen risico. Geef het door als er vaak wisselende bestuurders zijn.'),
    ('Is een inzittendenverzekering nodig?',
     'Het is verstandig. Een schadeverzekering inzittenden vergoedt letsel en schade van u en uw passagiers, ook als u zelf de schade veroorzaakt. Vooral als u met collega\'s of personeel rijdt.'),
]

AUTO_EIGEN = dict(
    licht=True,
    schade=schade('Schade met uw bedrijfsauto?',
        'Een aanrijding of inbraak in de bus is vervelend en kost tijd. Zo pakt u het aan:',
        ['Zorg eerst voor uw veiligheid. Zet de alarmlichten aan en trek een veiligheidshesje aan.',
         'Vul samen met de tegenpartij het Europees schadeformulier in, op papier of in een app.',
         'Is er ingebroken in de bus? Doe aangifte en maak een lijst van wat er weg is.',
         'Bel mij, dan regel ik de melding en kijk ik mee naar vervangend vervoer.'],
        'Kunt u na een ongeval niet verder rijden? Bel dan eerst de hulpdienst van uw verzekeraar, als u hulpverlening op uw polis heeft. Het nummer staat op uw verzekeringsbewijs. Daarna help ik u verder.'),
    werk=werkwijze('Zo regel ik uw bedrijfsauto', 'Van de eerste kennismaking tot de jaren daarna. Het eerste gesprek kost u niets.',
        [('Kennismaken', 'U vertelt welke voertuigen u heeft, wie erin rijdt en wat er meestal in ligt.'),
         ('Dekking kiezen', 'We kijken per voertuig naar leeftijd en waarde, en of een wagenparkpolis voordeliger is.'),
         ('Vergelijken en advies', 'Ik vergelijk verzekeraars op premie, eigen risico en de eisen voor gereedschap in de bus.'),
         ('Regelen en bijhouden', 'Koopt u een nieuw voertuig, dan regel ik het meteen, ook de overstap van uw schadevrije jaren.')]),
    review=reviews('Hulp bij schade', 'Juist bij schade aan een bedrijfsvoertuig wilt u snel en goed geholpen worden.', [REVIEW_TONY, REVIEW_ROB, REVIEW_KYRA]),
    wie=wie('Eén aanspreekpunt voor al uw voertuigen',
        'Mijn naam is Fred Koeling. Bij schade aan een bedrijfsauto wilt u niet in een keuzemenu hangen, maar iemand spreken die u kent.',
        'Ik werk sinds 2015 als zelfstandig adviseur, voor ondernemers in Apeldoorn en omgeving.',
        'Een stilstaande bus kost u geld. Daarom regel ik het bij schade zo snel mogelijk.'),
    zij='Twijfelt u welke dekking past bij uw auto, bus of wagenpark? Bel of mail mij. Het eerste gesprek is gratis.',
    vragenintro='Nog een vraag over uw bedrijfsauto of bus? Bel gerust, daar hoeft u geen afspraak voor te maken.',
    contact=('Uw bedrijfsauto goed verzekerd?', 'Stuur mij het kenteken en uw huidige polis, dan zoek ik uit wat het beste past. Ik kom ook graag langs op uw bedrijf.'))

AUTO_DUO = duo('verz-auto-sleutel.jpg', 'Autosleutel in de hand met de auto op de achtergrond', 1260, 840,
    'Mijn aanpak', 'Hoe ik u help',
    '      <p>Bij een bedrijfsauto gaat het niet alleen om het voertuig, maar ook om wat erin ligt en wie erin rijdt.</p>',
    ['Ik kies per voertuig de dekking die past bij leeftijd en waarde.',
     'Ik zorg dat uw gereedschap en goederen onderweg verzekerd zijn.',
     'Ik bereken of een wagenparkpolis voor u voordeliger is.',
     'Bij schade regel ik de melding, zodat u snel weer kunt rijden.'],
    ('Vraag een zakelijke polischeck aan', '../zakelijk/#polischeck'))

# ================================================================ VvE
VVE_HULP = vinkjes(
    'Checklist voor het bestuur', 'Is uw VvE goed verzekerd?',
    'Als bestuur bent u verantwoordelijk voor de verzekeringen van de VvE. Vink aan wat voor uw VvE geldt.',
    ['Zes punten', 'Direct antwoord', 'Niets invullen'],
    'Wat geldt voor uw VvE?',
    ['De VvE heeft een opstalverzekering voor het hele gebouw',
     'De herbouwwaarde is de afgelopen jaren nog getaxeerd',
     'De VvE heeft een aansprakelijkheidsverzekering',
     'Het bestuur is verzekerd voor bestuurdersaansprakelijkheid',
     'De eigenaren weten wat de VvE verzekert en wat zij zelf moeten regelen',
     'De polis is de afgelopen drie jaar vergeleken met andere verzekeraars'],
    [(0, 0, 'Vink aan wat voor uw VvE geldt. U ziet direct of er iets te verbeteren valt.'),
     (1, 3, '<b>Tijd voor een check.</b> Er zijn een paar belangrijke punten open. Ontbreekt de opstal- of aansprakelijkheidsverzekering, of klopt de herbouwwaarde niet, dan kan dat het bestuur en de eigenaren veel geld kosten.'),
     (4, 5, '<b>Bijna goed geregeld.</b> Een paar punten zijn het nalopen waard. Vaak is er ook premie te besparen door de polis eens te vergelijken.'),
     (6, 6, '<b>Goed geregeld.</b> Uw VvE heeft de basis op orde. Laat de herbouwwaarde wel eens in de paar jaar opnieuw bepalen.')],
    ('Laat de polis van uw VvE nakijken', 'tel:+31630679790'))

VVE_STREN = """    <script>
    (function(){
      /* ontbreekt de opstal- of de aansprakelijkheidsverzekering, dan blijft de uitslag 'tijd voor een check' */
      var h=document.getElementById('fxHulp'), u=document.getElementById('fxHulpUit'); if(!h||!u) return;
      var bx=[].slice.call(h.querySelectorAll('input[type=checkbox]')), ps=[].slice.call(u.querySelectorAll('[data-min]'));
      function streng(){ var n=bx.filter(function(b){return b.checked;}).length;
        if(n>=4&&(!bx[0].checked||!bx[2].checked)) ps.forEach(function(p){ p.hidden=p.getAttribute('data-min')!=='1'; }); }
      bx.forEach(function(b){ b.addEventListener('change',streng); });
    })();
    </script>
"""
assert VVE_HULP.count('    </script>\n  </section></div>') == 1
VVE_HULP = VVE_HULP.replace('    </script>\n  </section></div>', '    </script>\n' + VVE_STREN + '  </section></div>')

VVE_TEKST = kort(['Bijna elke VvE moet volgens het splitsingsreglement het gebouw verzekeren met een opstalverzekering.',
                  'Een aansprakelijkheidsverzekering is verplicht als het reglement dat voorschrijft, zoals bij het modelreglement van 1983 en later.',
                  'Eigenaren verzekeren zelf hun inboedel, en vaak ook hun eigen verbeteringen aan het appartement.']) + '''      <h2>Welke verzekeringen heeft een VvE nodig?</h2>
      <p>Een Vereniging van Eigenaren beheert het gebouw namens alle eigenaren. Het bestuur moet ervoor zorgen dat het gebouw en de VvE goed verzekerd zijn. Wat precies verplicht is, staat in de splitsingsakte en het splitsingsreglement van uw VvE.</p>
      <table class="fx-verz__tabel">
        <thead><tr><td></td><th>Wat is verzekerd</th><th>Verplicht?</th></tr></thead>
        <tbody>
          <tr><th>Opstal</th><td>Het hele gebouw, inclusief gemeenschappelijke ruimtes en vaste onderdelen</td><td>Ja, volgens bijna elk splitsingsreglement</td></tr>
          <tr><th>Aansprakelijkheid</th><td>Schade die het gebouw of de VvE bij anderen veroorzaakt</td><td>Ja, bij het modelreglement van 1983 en later</td></tr>
          <tr><th>Bestuurders&shy;aansprakelijkheid</th><td>Persoonlijke aansprakelijkheid van bestuursleden</td><td>Nee, maar wel verstandig</td></tr>
          <tr><th>Rechtsbijstand</th><td>Hulp bij een conflict, bijvoorbeeld met een aannemer</td><td>Nee</td></tr>
        </tbody>
      </table>

      <h2>De opstalverzekering van de VvE</h2>
      <p>De opstalverzekering dekt schade aan het gebouw, bijvoorbeeld door brand, storm of een lekkage. Het verzekerde bedrag is de herbouwwaarde van het hele complex. Laat die eens in de paar jaar opnieuw taxeren. Bouwkosten stijgen, en een te laag bedrag betekent dat u bij een grote schade niet alles vergoed krijgt. Dan moeten de eigenaren het verschil samen betalen.</p>

      <h2>Aansprakelijkheid van de VvE</h2>
      <p>Valt er een dakpan op een geparkeerde auto, of glijdt een bezoeker uit in een glad trappenhuis? Dan kan de VvE aansprakelijk zijn. De aansprakelijkheidsverzekering van de VvE dekt die schade. Bij de meeste VvE's schrijft het reglement deze verzekering voor.</p>

      <h2>Bestuurdersaansprakelijkheid</h2>
      <p>Bestuursleden van een VvE zijn vaak vrijwilligers. Toch kunnen zij persoonlijk aansprakelijk worden gesteld, bijvoorbeeld als een verplichte verzekering ontbreekt of als onderhoud te lang is uitgesteld. Een bestuurdersaansprakelijkheidsverzekering beschermt hen daartegen. Dat maakt het ook makkelijker om nieuwe bestuursleden te vinden.</p>

      <h2>Wat regelen de eigenaren zelf?</h2>
      <p>Elke eigenaar verzekert zelf de eigen <a href="../verzekeringen/woonverzekering/">inboedel</a> en een eigen aansprakelijkheidsverzekering. Heeft een eigenaar het appartement verbeterd, bijvoorbeeld met een nieuwe keuken of badkamer, dan valt dat niet altijd onder de opstalverzekering van de VvE. Dat kan de eigenaar dan zelf meeverzekeren. Het helpt als het bestuur dit duidelijk aan alle eigenaren uitlegt.</p>'''

VVE_VR = [
    ('Is een opstalverzekering verplicht voor een VvE?',
     'Bijna altijd wel. Het splitsingsreglement schrijft voor dat de VvE het gebouw verzekert. Kijk in uw eigen splitsingsakte en reglement wat er precies staat.'),
    ('Is een aansprakelijkheidsverzekering verplicht voor een VvE?',
     'Als uw splitsingsreglement verwijst naar het modelreglement van 1983 of later, dan wel. Dat is bij de meeste VvE\'s het geval.'),
    ('Hoe vaak moet de herbouwwaarde worden getaxeerd?',
     'Er is geen vaste regel, maar eens in de paar jaar is verstandig. Bouwkosten stijgen, en met een te laag verzekerd bedrag krijgt de VvE bij een grote schade niet alles vergoed.'),
    ('Is mijn nieuwe keuken verzekerd via de VvE?',
     'Niet altijd. De opstalverzekering van de VvE gaat meestal uit van de oorspronkelijke staat van het appartement. Verbeteringen die u zelf heeft laten aanbrengen, kunt u zelf meeverzekeren.'),
    ('Wat is een bestuurdersaansprakelijkheidsverzekering?',
     'Een verzekering die bestuursleden beschermt als zij persoonlijk aansprakelijk worden gesteld voor hun beslissingen als bestuur. Zeker bij een VvE met vrijwilligers in het bestuur is dat verstandig.'),
    ('Helpt u ook kleine VvE\'s?',
     'Ja. Ook een VvE met een paar appartementen moet het gebouw goed verzekeren. Juist bij kleine VvE\'s ontbreekt het vaak aan een actuele herbouwwaarde of een aansprakelijkheidsverzekering.'),
    ('Kan de VvE besparen op de premie?',
     'Vaak wel. Een polis die al jaren loopt, is niet altijd meer scherp geprijsd. Ik vergelijk de dekking en premie van uw VvE met wat er nu te krijgen is, zonder dat de dekking erop achteruitgaat.'),
]

VVE_EIGEN = dict(
    schade=schade('Schade aan het gebouw?',
        'Een lekkage of stormschade raakt vaak meerdere eigenaren tegelijk. Zo pakt het bestuur het aan:',
        ['Beperk de schade als dat veilig kan, bijvoorbeeld door de hoofdkraan af te sluiten of een dak tijdelijk af te dekken.',
         'Maak foto\'s van de schade, ook bij de appartementen die het raakt.',
         'Laat eigenaren hun eigen schade aan inboedel bij hun eigen verzekeraar melden.',
         'Bel mij, dan meld ik de schade aan het gebouw en houd ik het overzicht.'],
        'Bij schade aan een gebouw lopen de verzekeringen van de VvE en van de eigenaren door elkaar. Ik help het bestuur om te bepalen wat bij wie hoort.'),
    werk=werkwijze('Zo regel ik de verzekeringen van uw VvE', 'Van het eerste gesprek met het bestuur tot de jaren daarna. Het eerste gesprek kost u niets.',
        [('Kennismaken met het bestuur', 'Ik lees de splitsingsakte en het reglement, en kom naar het gebouw kijken.'),
         ('Dekking op een rij', 'Ik kijk wat verplicht is, wat er al geregeld is en of de herbouwwaarde nog klopt.'),
         ('Vergelijken en advies', 'Ik vergelijk verzekeraars en leg het voorstel zo uit dat het bestuur het in de vergadering kan voorleggen.'),
         ('Regelen en bijhouden', 'Ik regel de polissen en blijf aanspreekpunt bij schade, ook als het bestuur wisselt.')]),
    review=reviews('Een VvE in de praktijk', 'Na het uitzoeken had deze VvE een completere verzekering, en betaalde ze minder.', [REVIEW_MARCEL, REVIEW_LARS, REVIEW_FLEUR]),
    wie=wie('Een vaste adviseur voor uw VvE',
        'Mijn naam is Fred Koeling. Een VvE-bestuur wisselt nogal eens. Ik blijf, en ken uw gebouw en uw polissen.',
        'Ik werk sinds 2015 als zelfstandig adviseur voor particulieren, ondernemers en VvE\'s in Apeldoorn en omgeving.',
        'Een goede VvE-verzekering voorkomt dat eigenaren na een schade onverwacht moeten bijbetalen.'),
    zij='Twijfelt het bestuur of de VvE goed verzekerd is? Bel of mail mij. Het eerste gesprek is gratis.',
    vragenintro='Nog een vraag over de verzekeringen van uw VvE? Bel gerust, daar hoeft u geen afspraak voor te maken.',
    contact=('De polis van uw VvE laten nakijken?', 'Ik kom graag naar uw gebouw in Apeldoorn en omgeving, of spreek met het bestuur af op een moment dat het uitkomt.'))

VVE_DUO = duo('sleutels-nieuwe-woning.jpg', 'Sleutels in de voordeur van een woning', 1100, 733,
    'Mijn aanpak', 'Hoe ik u help',
    '      <p>Voor een VvE-bestuur zijn verzekeringen vaak een lastig onderwerp. Ik maak het overzichtelijk, zodat u het in de vergadering goed kunt uitleggen.</p>',
    ['Ik lees de splitsingsakte en het reglement, en kijk wat verplicht is.',
     'Ik controleer of de herbouwwaarde nog klopt.',
     'Ik vergelijk de polis van de VvE met wat er nu te krijgen is.',
     'Ik maak een overzicht voor de eigenaren: wat regelt de VvE, en wat zij zelf.'],
    ('Bel mij voor een gesprek', 'tel:+31630679790'))

BESTANDEN = {
    'avb.html': pagina('Bedrijfsaansprakelijkheid', 'Bedrijfsaansprakelijkheid', 'Aansprakelijkheid',
        'Bedrijfs&shy;aansprakelijkheids&shy;verzekering (AVB)',
        'Een kras in de vloer van een klant of een bezoeker die struikelt: als ondernemer bent u er aansprakelijk voor. Ik leg uit wat een AVB dekt, en wanneer u ook beroepsaansprakelijkheid nodig heeft.',
        AVB_TEKST, AVB_VR, 'Vragen over bedrijfs&shy;aansprakelijkheid', AVB_HULP, 'Test uzelf: bedrijfs- of beroepsaansprakelijkheid?',
        AVB_DUO, AVB_EIGEN, ('Doe de bedrijfscheck', '../zakelijk/#check')),
    'aov.html': pagina('AOV', 'Arbeidsongeschiktheid (AOV)', 'Inkomen',
        "Arbeids&shy;ongeschiktheids&shy;verzekering voor zzp'ers en ondernemers",
        'Als ondernemer stopt uw inkomen als u niet kunt werken, maar uw vaste lasten lopen door. Ik help u een AOV te kiezen die past bij uw inkomen, uw buffer en uw vak.',
        AOV_TEKST, AOV_VR, 'Vragen over de AOV', AOV_HULP, 'Reken uit: hoe lang kunt u zonder inkomen?',
        AOV_DUO, AOV_EIGEN, ('Plan een gratis gesprek', '../contact/')),
    'pand.html': pagina('Bedrijfspand en inventaris', 'Bedrijfspand en inventaris', 'Pand en spullen',
        'Bedrijfspand, inventaris en bedrijfsschade verzekeren',
        'Brand, storm of inbraak kan uw bedrijf stilleggen. Ik zorg dat uw pand, inrichting en voorraad goed verzekerd zijn, en dat u na een schade weer verder kunt.',
        PAND_TEKST, PAND_VR, 'Vragen over pand en inventaris', PAND_HULP, 'Doe de snelle check: wat moet u verzekeren?',
        PAND_DUO, PAND_EIGEN, ('Doe de bedrijfscheck', '../zakelijk/#check')),
    'auto.html': pagina('Bedrijfsauto', 'Bedrijfsauto en bestelbus', 'Vervoer',
        'Bedrijfsauto, bestelbus en wagenpark verzekeren',
        'Een auto van de zaak, een bestelbus vol gereedschap of een heel wagenpark. Ik zorg dat uw voertuigen en wat erin ligt goed verzekerd zijn.',
        AUTO_TEKST, AUTO_VR, 'Vragen over de bedrijfsauto', AUTO_HULP, 'Voertuigwijzer: wat heeft u nodig?',
        AUTO_DUO, AUTO_EIGEN, ('Doe de bedrijfscheck', '../zakelijk/#check')),
    'vve.html': pagina('VvE-verzekering', 'VvE-verzekering', 'VvE',
        'VvE-verzekering: opstal, aansprakelijkheid en bestuur',
        'Als VvE-bestuur bent u verantwoordelijk voor de verzekeringen van het gebouw. Ik zoek uit wat verplicht is, controleer de herbouwwaarde en vergelijk de premie.',
        VVE_TEKST, VVE_VR, 'Vragen over de VvE-verzekering', VVE_HULP, 'Checklist voor het bestuur: is uw VvE goed verzekerd?',
        VVE_DUO, VVE_EIGEN, ('Mail mij uw polis', 'mailto:info@finect.nl?subject=Polischeck%20VvE')),
}

if __name__ == '__main__':
    for naam, inhoud in BESTANDEN.items():
        io.open(HIER + naam, 'w', encoding='utf-8').write(inhoud)
        print('geschreven', naam, len(inhoud) // 1024, 'kB')

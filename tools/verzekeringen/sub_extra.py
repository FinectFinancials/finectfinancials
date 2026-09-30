# -*- coding: utf-8 -*-
"""Extra onderdelen voor de subpagina's: hulpmiddel per onderwerp, 'hoe ik u help' met foto,
en blokken die de subpagina's delen met de hoofdpagina (cijfers, schade, werkwijze, reviews, uw adviseur)."""
import io, os, re

SP = os.path.dirname(os.path.abspath(__file__)) + '/'
HUB = io.open(SP + 'inhoud.html', encoding='utf-8').read()


def hub_blok(naam):
    """Een blok uit de hoofdpagina, van <!-- naam --> tot het volgende commentaar."""
    a = HUB.index('  <!-- ' + naam + ' -->')
    b = HUB.index('  <!-- ', a + 10)
    return HUB[a:b].rstrip() + '\n\n'


CIJFERS = '  <div class="fx-ct__wrap">\n    ' + re.search(r'<ul class="fx-verz__cijfers">.*?</ul>', HUB, re.S).group(0) + '\n  </div>\n\n'
SCHADE = hub_blok('schade')
WERKWIJZE = hub_blok('werkwijze')
REVIEWS = hub_blok('klantervaringen')
WIE = hub_blok('uw adviseur')
CHIP = re.search(r'<div class="fx-verz__adviseur">.*?</div>', HUB).group(0)

KNOPPEN = ('<div class="fx-ct__btns"><a class="fx-ct__btn fx-ct__btn--m" href="tel:+31630679790">Bel 06 30 67 97 90</a>'
           '<a class="fx-ct__btn fx-ct__btn--o" href="{u}">{t}</a></div>')


def duo(foto, alt, br, ho, sub, kop, tekst, punten, knop):
    li = ''.join('<li>%s</li>' % p for p in punten)
    return '''  <!-- hoe ik u help -->
  <div class="fx-ct__band"><div class="fx-ct__wrap"><section class="fx-ct__sec fx-verz__duo fx-verz__hulpduo">
    <div class="fx-verz__pakfoto"><img src="../wp-content/uploads/finect/%s" alt="%s" width="%d" height="%d" loading="lazy" decoding="async"></div>
    <div>
      <p class="fx-ct__sub">%s</p>
      <h2>%s</h2>
%s
      <ul class="fx-verz__lijst fx-verz__lijst--ruim">%s</ul>
      %s
    </div>
  </section></div></div>

''' % (foto, alt, br, ho, sub, kop, tekst, li, KNOPPEN.format(u=knop[1], t=knop[0]))


def vinkjes(sub, kop, intro, punten, vragen_kop, items, uitslagen, knop):
    """Hulpmiddel met vinkjes: hoe meer er voor u geldt, hoe duidelijker het advies."""
    pl = ''.join('<li>%s</li>' % p for p in punten)
    it = ''.join('<label><input type="checkbox" name="vink" value="%d"><span>%s</span></label>' % (i, x) for i, x in enumerate(items))
    ui = ''.join('<p data-min="%d" data-max="%d"%s>%s</p>' % (a, b, '' if a == 0 else ' hidden', t) for a, b, t in uitslagen)
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
        <div class="fx-verz__hulp" id="fxHulp" hidden>
          <fieldset class="fx-verz__vraag fx-verz__vraag--vink">
            <legend>%s</legend>
            %s
          </fieldset>
          <div class="fx-verz__hulpuit" id="fxHulpUit" aria-live="polite">%s</div>
          %s
        </div>
      </div>
    </div>
    <script>
    (function(){
      var h=document.getElementById('fxHulp'), u=document.getElementById('fxHulpUit'); if(!h||!u) return;
      h.hidden=false;
      var bx=[].slice.call(h.querySelectorAll('input[type=checkbox]')), ps=[].slice.call(u.querySelectorAll('[data-min]'));
      function tel(){ var n=bx.filter(function(b){return b.checked;}).length;
        ps.forEach(function(p){ p.hidden=!(n>=+p.getAttribute('data-min')&&n<=+p.getAttribute('data-max')); });
        u.classList.toggle('is-uit', n>0); }
      bx.forEach(function(b){ b.addEventListener('change',tel); }); tel();
    })();
    </script>
  </section></div>

''' % (sub, kop, intro, pl, vragen_kop, it, ui, KNOPPEN.format(u=knop[1], t=knop[0]))


# ---------------------------------------------------------------- woonverzekering
HULP_WOON = vinkjes(
    'Snelle check', 'Klopt uw woonverzekering nog?',
    'Een verzekerd bedrag dat niet meer klopt, merkt u pas bij schade. Vink aan wat de afgelopen jaren voor u is veranderd.',
    ['Zes vragen', 'Direct antwoord', 'Niets invullen'],
    'Wat is er de afgelopen jaren gebeurd?',
    ['Ik heb verbouwd of een uitbouw laten maken',
     'Er is een nieuwe keuken of badkamer geplaatst',
     'Ik heb zonnepanelen, een laadpaal of een warmtepomp',
     'Ik heb dure spullen gekocht, zoals een e-bike, sieraden of apparatuur',
     'Ik weet niet welk bedrag er op mijn polis staat',
     'Mijn polis is ouder dan vijf jaar'],
    [(0, 0, 'Vink aan wat voor u geldt. U ziet direct of het slim is om uw woonverzekering te laten nakijken.'),
     (1, 2, '<b>Laat uw verzekerde bedrag nakijken.</b> Er is iets veranderd aan uw huis of uw spullen. Dan klopt het bedrag op uw polis misschien niet meer, en bij schade krijgt u dan maar een deel vergoed.'),
     (3, 99, '<b>Grote kans dat uw polis niet meer klopt.</b> Er is veel veranderd sinds u de verzekering afsloot. Een polischeck laat zien of u onderverzekerd bent, en of het voordeliger kan.')],
    ('Vraag een polischeck aan', '../verzekeringen/polischeck/'))

DUO_WOON = duo('verzekeringen-woonhuis.jpg', 'Karakteristiek woonhuis aan het water', 1920, 1080,
    'Mijn aanpak', 'Hoe ik u help',
    '      <p>Ik vergelijk de woonverzekeringen van verschillende verzekeraars en kijk verder dan de premie. U hoort wat u echt nodig heeft, en wat niet.</p>',
    ['Ik vergelijk dekking, eigen risico en premie voor u.',
     'Ik kijk of het verzekerde bedrag past bij uw huis en uw spullen.',
     'Ik kijk of een pakket met uw andere verzekeringen voordeliger is.',
     'Bij schade belt u mij, en ik help u verder.'],
    ('Vraag een polischeck aan', '../verzekeringen/polischeck/'))

# ---------------------------------------------------------------- aansprakelijkheid
SCEN = [
    ('Uw zoon van negen fietst tegen een geparkeerde auto.', 'wel', 'Meestal verzekerd',
     'Kinderen onder de 14 zijn wettelijk niet zelf aansprakelijk, maar dan bent u dat als ouder. Veel verzekeraars vergoeden de schade dan.'),
    ('Uw hond bijt de broek van een voorbijganger kapot.', 'wel', 'Meestal verzekerd',
     'Als eigenaar bent u aansprakelijk voor schade door uw huisdier. Die schade valt meestal onder uw aansprakelijkheidsverzekering.'),
    ('U laat de geleende laptop van een vriend vallen.', 'let', 'Vaak beperkt verzekerd',
     'Schade aan geleende of gehuurde spullen is bij veel verzekeraars beperkt of uitgesloten. Hier verschillen polissen echt.'),
    ('Uw wasmachine lekt en de benedenburen krijgen waterschade.', 'wel', 'Meestal verzekerd',
     'De schade bij de buren valt meestal onder uw aansprakelijkheidsverzekering. De schade in uw eigen huis loopt via uw woonverzekering.'),
    ('U stoot uw eigen televisie van de kast.', 'niet', 'Niet via deze verzekering',
     'Deze verzekering is voor schade bij een ander. Schade aan uw eigen spullen kan onder een uitgebreide inboedelverzekering vallen.'),
    ('Als zzp\'er beschadigt u de vloer bij een klant.', 'niet', 'Niet via deze verzekering',
     'Schade tijdens uw werk valt niet onder de verzekering voor particulieren. Daarvoor is een bedrijfsaansprakelijkheidsverzekering.'),
]
HULP_AVP = '''  <!-- hulpmiddel -->
  <div class="fx-ct__wrap"><section class="fx-ct__sec fx-verz__checksec" id="hulp">
    <div class="fx-verz__checkkaart fx-verz__checkkaart--breed">
      <div class="fx-verz__checkintro">
        <p class="fx-ct__sub">Test uzelf</p>
        <h2>Verzekerd of niet?</h2>
        <p>Zes situaties uit het dagelijks leven. Denk eerst zelf na en bekijk dan het antwoord.</p>
      </div>
      <div class="fx-verz__scen">''' + ''.join('''
        <details class="fx-verz__scenario">
          <summary><span class="fx-verz__scenvraag">%s</span><span class="fx-verz__scenknop">Bekijk het antwoord</span></summary>
          <p><b class="fx-verz__oordeel fx-verz__oordeel--%s">%s</b>%s</p>
        </details>''' % (v, k, o, u) for v, k, o, u in SCEN) + '''
      </div>
      <p class="fx-verz__scenvoet">Dit geldt in de meeste gevallen. De precieze dekking verschilt per verzekeraar. Twijfelt u over uw eigen polis? <a href="tel:+31630679790">Bel mij</a>, dan kijk ik het na.</p>
    </div>
  </section></div>

'''

DUO_AVP = duo('verz-avp-hond.jpg', 'Stel wandelt met hun hond door een park in de herfst', 1120, 747,
    'Mijn aanpak', 'Hoe ik u help',
    '      <p>Aansprakelijkheidsverzekeringen lijken op elkaar, maar de verschillen zitten in de details. Juist die zet ik voor u op een rij.</p>',
    ['Ik kijk of de dekking past bij uw gezin, ook bij kinderen op kamers.',
     'Ik let op geleende en gehuurde spullen, en op huisdieren.',
     'Ik kijk of de verzekering voordeliger is in een pakket met uw <a href="../verzekeringen/woonverzekering/">woonverzekering</a>.',
     'Bij schade belt u mij, en ik help u verder.'],
    ('Vraag een polischeck aan', '../verzekeringen/polischeck/'))

# ---------------------------------------------------------------- autoverzekering
def rij(naam, legend, opties):
    return ('<fieldset class="fx-verz__vraag fx-verz__vraag--rij"><legend>%s</legend>' % legend +
            ''.join('<label><input type="radio" name="%s" value="%s"><span>%s</span></label>' % (naam, w, t) for w, t in opties) +
            '</fieldset>')

HULP_AUTO = '''  <!-- hulpmiddel -->
  <div class="fx-ct__wrap"><section class="fx-ct__sec fx-verz__checksec" id="hulp">
    <div class="fx-verz__checkkaart">
      <div class="fx-verz__checkintro">
        <p class="fx-ct__sub">Dekkingswijzer</p>
        <h2>Welke dekking past bij uw auto?</h2>
        <p>Beantwoord drie vragen en zie welke dekking waarschijnlijk het best past. Zo weet u of u niet te veel of te weinig verzekerd bent.</p>
        <ul class="fx-verz__checkpunten"><li>Drie vragen</li><li>Direct antwoord</li><li>Niets invullen</li></ul>
      </div>
      <div class="fx-verz__checkvak">
        <noscript><p class="fx-verz__checkgeenjs">Dit hulpmiddel werkt met JavaScript. Bel mij gerust op <a href="tel:+31630679790">06 30 67 97 90</a>, dan lopen we het samen door.</p></noscript>
        <form class="fx-verz__hulp" id="fxDekking" hidden>
          ''' + rij('leeftijd', 'Hoe oud is uw auto?', [('nieuw', 'Jonger dan 4 jaar'), ('midden', '4 tot 8 jaar'), ('oud', '8 jaar of ouder')]) + '''
          ''' + rij('waarde', 'Wat is uw auto ongeveer waard?', [('laag', 'Minder dan &euro;&nbsp;5.000'), ('midden', '&euro;&nbsp;5.000 tot &euro;&nbsp;15.000'), ('hoog', 'Meer dan &euro;&nbsp;15.000')]) + '''
          ''' + rij('financiering', 'Heeft u de auto gefinancierd of in private lease?', [('ja', 'Ja'), ('nee', 'Nee')]) + '''
          <div class="fx-verz__hulpuit" id="fxDekkingUit" aria-live="polite"><p>Beantwoord de drie vragen, dan ziet u hier welke dekking waarschijnlijk past.</p></div>
          ''' + KNOPPEN.format(u='../verzekeringen/polischeck/', t='Vraag een polischeck aan') + '''
        </form>
      </div>
    </div>
    <script>
    (function(){
      var f=document.getElementById('fxDekking'), u=document.getElementById('fxDekkingUit'); if(!f||!u) return;
      f.hidden=false;
      f.addEventListener('submit',function(e){e.preventDefault();});
      function w(n){var r=f.querySelector('input[name='+n+']:checked'); return r?r.value:'';}
      f.addEventListener('change',function(){
        var l=w('leeftijd'), v=w('waarde'), fi=w('financiering'); if(!l||!v||!fi) return;
        var d, r;
        if(fi==='ja'){d='Allrisk'; r='Bij een financiering of private lease is allrisk meestal verplicht. Kijk wel goed naar het eigen risico.';}
        else if(v==='laag'){d='WA, eventueel met beperkt casco'; r='Bij een auto van minder dan 5.000 euro is de extra premie voor allrisk vaak hoger dan wat u ooit vergoed krijgt. Met beperkt casco bent u wel verzekerd voor onder meer diefstal, brand, storm en ruitschade.';}
        else if(l==='nieuw'){d='Allrisk'; r='Uw auto is nog jong en veel waard. Met allrisk is ook schade verzekerd die u zelf veroorzaakt, zoals een aanrijding of een kras bij het parkeren.';}
        else if(l==='midden'&&v==='hoog'){d='Allrisk of beperkt casco'; r='Dit is een twijfelgeval. Het hangt af van de premie en van of u een schade zelf zou kunnen betalen. Dat reken ik graag met u door.';}
        else {d='WA met beperkt casco'; r='Voor een auto van deze leeftijd en waarde is beperkt casco vaak de beste balans tussen premie en dekking.';}
        u.innerHTML='<p><span class="fx-verz__lijstkop">Waarschijnlijk past</span><b class="fx-verz__dekking">'+d+'</b>'+r+'</p><p class="fx-verz__klein">Dit is een vuistregel, geen advies. Ook uw schadevrije jaren en het eigen risico tellen mee.</p>';
        u.classList.add('is-uit');
      });
    })();
    </script>
  </section></div>

'''

DUO_AUTO = duo('verz-auto-sleutel.jpg', 'Autosleutel in de hand met de auto op de achtergrond', 1260, 840,
    'Mijn aanpak', 'Hoe ik u help',
    '      <p>Ik vergelijk autoverzekeringen van verschillende verzekeraars en let op meer dan alleen de premie.</p>',
    ['Ik kijk welke dekking past bij de leeftijd en de waarde van uw auto.',
     'Ik let op het eigen risico en de voorwaarden, zoals de regeling voor nieuwe auto\'s.',
     'Ik kijk of de verzekering voordeliger is in een pakket met uw andere verzekeringen.',
     'Heeft u schade, dan belt u mij en kijk ik mee wat er moet gebeuren.'],
    ('Vraag een polischeck aan', '../verzekeringen/polischeck/'))

# ---------------------------------------------------------------- polischeck
HULP_CHECK = vinkjes(
    'Snelle check', 'Is het tijd voor een polischeck?',
    'Bij elke grote verandering in uw leven is het slim om naar uw verzekeringen te kijken. Vink aan wat voor u geldt.',
    ['Acht vragen', 'Direct antwoord', 'Niets invullen'],
    'Wat is er de afgelopen jaren veranderd?',
    ['Ik ben verhuisd of heb een huis gekocht',
     'Ik heb verbouwd of verduurzaamd',
     'Ik ben gaan samenwonen of getrouwd',
     'Ik heb kinderen gekregen',
     'Ik heb een andere auto',
     'Ik ben zelfstandig ondernemer geworden',
     'Ik ben met pensioen gegaan',
     'Ik heb al jaren niet naar mijn verzekeringen gekeken'],
    [(0, 0, 'Vink aan wat voor u geldt. U ziet direct of een polischeck zinvol is.'),
     (1, 1, '<b>Een goed moment om te kijken.</b> Eén verandering kan al gevolgen hebben voor uw dekking. Een korte check geeft u zekerheid.'),
     (2, 99, '<b>Tijd voor een polischeck.</b> Er is genoeg veranderd om uw verzekeringen eens goed na te lopen. Grote kans dat er iets te verbeteren valt.')],
    ('Stuur uw polissen', 'mailto:info@finect.nl'))

DUO_CHECK = duo('dienst-inzicht.jpg', 'Overzicht van verzekeringen en kosten op papier', 1145, 840,
    'Wat u krijgt', 'Een helder overzicht',
    '      <p>Na de polischeck weet u precies hoe u ervoor staat. U krijgt van mij een overzicht in gewone taal, zonder verzekeringsjargon.</p>',
    ['Welke verzekeringen u heeft en wat ze dekken.',
     'Waar u te veel of dubbel verzekerd bent.',
     'Waar u te weinig verzekerd bent.',
     'Wat ik zou aanpassen, en wat dat u oplevert.'],
    ('Stuur uw polissen', 'mailto:info@finect.nl'))

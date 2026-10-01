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

# in de hulpmiddelen en bij 'hoe ik u help' alleen de vervolgstap; bellen kan via de kop, de zijkaart, contact en de balk
KNOPPEN = '<div class="fx-ct__btns"><a class="fx-ct__btn fx-ct__btn--m" href="{u}">{t}</a></div>'


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


# ================================================================ ronde 7: eigen blokken per onderwerp


def schade(kop, intro, punten, rechts):
    li = ''.join('<li>%s</li>' % p for p in punten)
    return '''  <!-- schade -->
  <div class="fx-ct__band--navy"><div class="fx-ct__wrap"><section class="fx-ct__sec fx-home__schade">
    <div>
      <p class="fx-ct__sub">Schade</p>
      <h2>%s</h2>
      <p>%s</p>
      <ul class="fx-verz__schadelijst">%s</ul>
    </div>
    <div class="fx-home__schade-bel">
      <p class="fx-verz__schadetel">Bel mij op <a href="tel:+31630679790">06 30 67 97 90</a></p>
      <p>%s</p>
      <p><a class="fx-verz__licht" href="../vergelijkingskaarten/">Bekijk de vergelijkingskaarten</a></p>
    </div>
  </section></div></div>

''' % (kop, intro, li, rechts)


def werkwijze(kop, intro, stappen):
    li = ''.join('<li><b>%s</b><span>%s</span></li>' % s for s in stappen)
    return '''  <!-- werkwijze -->
  <div class="fx-ct__wrap"><section class="fx-ct__sec fx-home__werk">
    <p class="fx-ct__sub">Werkwijze</p>
    <h2>%s</h2>
    <p style="margin-bottom:38px;max-width:66ch;">%s</p>
    <ol class="fx-ct__stap fx-ct__stap--breed">%s</ol>
  </section></div>

''' % (kop, intro, li)


def review(kop, intro, citaat, ini, naam, bron='Google, 5 sterren'):
    return '''  <!-- klantervaring -->
  <div class="fx-ct__band--navy" id="ervaringen"><div class="fx-ct__wrap"><section class="fx-ct__sec">
    <div class="fx-ct__rev">
      <div>
        <p class="fx-ct__sub">Klantervaring</p>
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
        <div class="fx-ct__stage">
          <figure class="fx-ct__quote is-on">
            <blockquote>&ldquo;%s&rdquo;</blockquote>
            <figcaption><span class="fx-ct__ini">%s</span><span class="fx-ct__wie"><b>%s</b>%s</span></figcaption>
          </figure>
        </div>
      </div>
    </div>
  </section></div></div>

''' % (kop, intro, citaat, ini, naam, bron)


def wie(kop, lead, tekst, citaat):
    return '''  <!-- uw adviseur -->
  <div class="fx-ct__wrap"><section class="fx-ct__sec fx-verz__wie">
    <div class="fx-verz__wiefoto"><img src="../wp-content/uploads/2025/07/DSCF4417.jpg" alt="Fred Koeling, onafhankelijk verzekeringsadviseur in Apeldoorn" width="482" height="640" loading="lazy" decoding="async"></div>
    <div>
      <p class="fx-ct__sub">Uw adviseur</p>
      <h2>%s</h2>
      <p class="fx-ct__lead">%s</p>
      <p>%s</p>
      <blockquote class="fx-verz__citaat">&ldquo;%s&rdquo;</blockquote>
      <div class="fx-ct__btns"><a class="fx-ct__btn fx-ct__btn--o" href="../over-finect/">Lees meer over mij</a></div>
    </div>
  </section></div>

''' % (kop, lead, tekst, citaat)


REVIEW_FLEUR = ('Onlangs heeft Finect Financials mij geholpen met het regelen van mijn hypotheek en mijn huis- en autoverzekering, en ik ben echt ontzettend blij met hoe dat is gegaan. Fred neemt ruim de tijd om alles uit te leggen, denkt echt met je mee en zoekt actief naar de beste oplossingen voor jouw situatie.', 'FS', 'Fleur S.')
REVIEW_TONY = ('Fred heeft mij en mijn ouders heel goed geholpen met de schadeafhandeling van de zakelijke bus. Heel vriendelijk en zeer behulpzaam.', 'TP', 'Tony P.')
REVIEW_KYRA = ('Fred heeft verstand van zaken, houdt contact met je en denkt echt met je mee. Heel blij mee!', 'KD', 'Kyra D.')
REVIEW_MARCEL = ('Fred heeft de verzekeringen voor onze VVE uitgezocht, we hebben nu een completere verzekering dan we hadden, voor minder geld, top!', 'MG', 'Marcel de G.')

WERK_TEKST = 'Ik werk sinds 2015 als zelfstandig adviseur, met ruim 22 jaar ervaring in het vak.'

EIGEN = {
    'Woonverzekering': dict(
        schade=schade('Schade aan uw huis of spullen?',
            'Een lekkage, stormschade of inbraak komt altijd onverwacht. Dit kunt u meteen doen:',
            ['Beperk de schade als dat veilig kan. Sluit bij een lekkage de hoofdkraan af, en dek na storm een kapot raam of dak tijdelijk af.',
             'Doe bij inbraak of diefstal altijd aangifte bij de politie.',
             'Maak foto\'s van de schade en bewaar kapotte spullen en bonnen.',
             'Laat grote reparaties pas uitvoeren als de verzekeraar akkoord is. Een noodreparatie mag meteen.'],
            'Bij een grote schade, zoals brand of een flinke lekkage, stuurt de verzekeraar vaak een schade-expert. Ik help u bij dat contact en kijk mee of de vergoeding klopt.'),
        werk=werkwijze('Zo regel ik uw woonverzekering', 'Van de eerste vraag tot de jaren daarna. Het eerste gesprek kost u niets.',
            [('Kennismaken', 'We bespreken uw woning, wat erin staat en of u huurt of een eigen huis heeft.'),
             ('Waarde bepalen', 'We bepalen samen de herbouwwaarde en de waarde van uw inboedel, zodat u niet onderverzekerd bent.'),
             ('Vergelijken en advies', 'U krijgt de keuzes op een rij, met dekking, eigen risico en premie.'),
             ('Regelen en bijhouden', 'Ik regel de aanvraag. Na een verbouwing kijken we samen of het bedrag nog klopt.')]),
        review=review('Klanten over mijn advies', 'Een woonverzekering regelt u niet elk jaar. Des te fijner als iemand de tijd neemt om het goed uit te leggen.', *REVIEW_FLEUR),
        wie=wie('Uw adviseur voor wonen en verzekeren',
            'Mijn naam is Fred Koeling. Omdat ik ook hypotheken adviseer, kijk ik bij uw woonverzekering naar het geheel: uw huis, uw hypotheek en wat erin staat.',
            WERK_TEKST + ' Als Certified Financial Planner kijk ik verder dan één polis.',
            'Een goed verzekerd huis begint met het juiste bedrag op de polis.'),
        zij='Twijfelt u over het verzekerde bedrag van uw huis? Bel of mail mij. Het eerste gesprek is gratis.',
        contact=('Uw woonverzekering laten nakijken?', 'Ik kom bij u thuis in Apeldoorn en omgeving, dan zie ik de woning meteen. Liever online? Dat kan ook.')),
    'Aansprakelijkheidsverzekering': dict(
        schade=schade('Schade veroorzaakt bij een ander?',
            'Een ongelukje is zo gebeurd. Zo pakt u het goed aan:',
            ['Geef niet zelf schriftelijk toe dat u aansprakelijk bent. Dat beoordeelt de verzekeraar.',
             'Wissel gegevens uit met de ander en schrijf op wat er is gebeurd.',
             'Maak foto\'s van de schade en vraag de ander om een offerte of de rekening van de reparatie.',
             'Bel mij voordat u iets toezegt of betaalt.'],
            'Wordt u per brief of mail aansprakelijk gesteld? Stuur die door naar mij. Dan kijk ik mee voordat u reageert.'),
        werk=werkwijze('Zo regel ik uw aansprakelijkheids&shy;verzekering', 'Het is een eenvoudige verzekering, maar de details maken het verschil. Het eerste gesprek kost u niets.',
            [('Kennismaken', 'We bespreken wie er bij u wonen, en of er huisdieren of kinderen op kamers zijn.'),
             ('Uitzoeken', 'Ik kijk welke polissen passen, met aandacht voor geleende spullen en het eigen risico.'),
             ('Advies', 'U hoort welke verzekering ik aanraad en waarom. Vaak kan het voordelig in een pakket.'),
             ('Regelen en bijhouden', 'Ik regel de aanvraag. Verandert uw gezin, dan passen we de dekking aan.')]),
        review=review('Wat klanten van mij vinden', 'Klanten waarderen vooral dat ik meedenk en bereikbaar blijf, ook lang na het afsluiten.', *REVIEW_KYRA),
        wie=wie('Persoonlijk advies voor uw gezin',
            'Mijn naam is Fred Koeling. Ik kijk niet alleen naar de premie, maar naar uw gezin: kinderen, huisdieren en wat u leent of huurt.',
            WERK_TEKST + ' U heeft bij mij één vast aanspreekpunt.',
            'Een lage premie, maar een groot risico. Deze verzekering raad ik bijna iedereen aan.'),
        zij='Twijfelt u of uw gezin goed verzekerd is? Bel of mail mij. Het eerste gesprek is gratis.',
        contact=('Goed verzekerd voor schade bij een ander?', 'Bel of mail mij. Ik kom bij u thuis in Apeldoorn en omgeving, of we spreken online af.')),
    'Autoverzekering': dict(
        schade=schade('Een aanrijding gehad?',
            'Na een aanrijding is het vaak even schrikken. Met deze stappen maakt u het uzelf makkelijker:',
            ['Zorg eerst voor uw veiligheid en die van anderen. Zet de alarmlichten aan en trek een veiligheidshesje aan als u dat heeft.',
             'Vul samen met de tegenpartij het Europees schadeformulier in, op papier of in een app. Teken alleen als u het eens bent met wat er staat.',
             'Maak foto\'s van beide auto\'s, de kentekens en de situatie op de weg.',
             'Noteer de namen en telefoonnummers van getuigen.'],
            'Staat u stil langs de weg? Bel dan eerst de hulpdienst van uw verzekeraar. Het nummer staat op uw verzekeringsbewijs of in de app. Daarna help ik u verder.'),
        werk=werkwijze('Zo regel ik uw autoverzekering', 'Van de eerste vraag tot de jaren daarna. Het eerste gesprek kost u niets.',
            [('Kennismaken', 'U vertelt over uw auto, hoeveel u rijdt en wie er nog meer in rijdt.'),
             ('Dekking kiezen', 'We kijken naar de leeftijd en de waarde van de auto, en welk risico u zelf kunt dragen.'),
             ('Vergelijken en advies', 'Ik vergelijk verzekeraars op premie, eigen risico en voorwaarden.'),
             ('Regelen en bijhouden', 'Ik regel de overstap met uw schadevrije jaren. Na een paar jaar kijken we of een lichtere dekking kan.')]),
        review=review('Hulp bij schade', 'Juist bij schade merkt u het verschil van een vaste adviseur die u kent.', *REVIEW_TONY),
        wie=wie('Een vaste adviseur, ook na een aanrijding',
            'Mijn naam is Fred Koeling. Bij schade aan uw auto wilt u één persoon die u kent en die meedenkt. Dat ben ik.',
            WERK_TEKST + ' Ik kom bij u langs in Apeldoorn en omgeving.',
            'Allrisk is niet altijd nodig. Ik reken het eerlijk voor u door.'),
        zij='Twijfelt u tussen beperkt casco en allrisk? Bel of mail mij. Het eerste gesprek is gratis.',
        contact=('Advies over uw autoverzekering?', 'Stuur mij uw kenteken en uw huidige polis, dan zoek ik uit welke dekking het best past. Ik kom ook graag bij u langs in Apeldoorn en omgeving.')),
    'Polischeck': dict(
        schade='', werk='',
        review=review('Een polischeck in de praktijk', 'Na een check had deze VvE een betere dekking, en betaalde ze minder.', *REVIEW_MARCEL),
        wie=wie('Wie kijkt uw polissen na?',
            'Mijn naam is Fred Koeling. Ik ben Certified Financial Planner en werk sinds 2015 als zelfstandig adviseur.',
            'Met ruim 22 jaar ervaring weet ik waar polissen van elkaar verschillen, en waar het vaak misgaat.',
            'Ik adviseer alleen wat u echt iets oplevert.'),
        zij='Vragen over de polischeck? Bel of mail mij. Het eerste gesprek is gratis.',
        contact=('Een polischeck aanvragen?', 'Mail uw polissen naar <a href="mailto:info@finect.nl">info@finect.nl</a> of bel mij. Ik kom ook bij u langs in Apeldoorn en omgeving om ze samen door te nemen.')),
}


# ================================================================ ronde 10: eigen opbouw voor Woonverzekering
HUIS_ITEMS = [
    ('dak', 35, 29.5, 'opstal', 'Opstal', 'Dak en dakpannen',
     'Waait er bij een storm een stuk dak weg, of lekt het daarna? Dan valt de schade onder de woonhuisverzekering.'),
    ('zon', 70, 29, 'opstal', 'Opstal', 'Zonnepanelen',
     'Zonnepanelen op uw eigen dak horen meestal bij het huis en vallen onder de woonhuisverzekering. Geef ze wel door, zodat het verzekerde bedrag klopt.'),
    ('raam', 55.8, 54.5, 'opstal', 'Opstal', 'Ramen en glas',
     'Glas hoort bij het huis. Bij veel woonhuisverzekeringen is glasschade standaard verzekerd, bij andere kunt u het erbij nemen.'),
    ('cv', 45.8, 53.4, 'opstal', 'Opstal', 'Cv-ketel en leidingen',
     'De cv-ketel en de leidingen zitten vast aan het huis. Springt er een leiding, dan valt de schade aan het huis onder de woonhuisverzekering en de schade aan uw spullen onder de inboedelverzekering.'),
    ('keuken', 30, 73, 'opstal', 'Opstal', 'Keuken',
     'Een ingebouwde keuken hoort bij het huis, net als de badkamer. Huurt u en heeft u zelf een keuken laten plaatsen? Dan verzekert u die als huurdersbelang op uw inboedelverzekering.'),
    ('vloer', 62, 86, 'beide', 'Het hangt ervan af', 'Vloer',
     'Bent u eigenaar, dan valt een vaste vloer meestal onder de woonhuisverzekering. Heeft u als huurder zelf een vloer gelegd, dan valt die als huurdersbelang onder de inboedelverzekering.'),
    ('tv', 53, 68, 'inboedel', 'Inboedel', 'Televisie en laptop',
     'Apparatuur is inboedel. Valt de laptop van tafel, dan is dat alleen verzekerd met een uitgebreide dekking die ook een ongelukje vergoedt.'),
    ('bank', 71.7, 68, 'inboedel', 'Inboedel', 'Bank en meubels',
     'Alles wat u meeneemt als u verhuist, is inboedel. Uw meubels vallen dus onder de inboedelverzekering.'),
]

HUIS_SVG = '''<svg viewBox="0 0 600 440" role="img" aria-labelledby="huisTitel"><title id="huisTitel">Doorsnede van een woning met dak, zonnepanelen, keuken, cv-ketel, vloer, televisie en bank</title>
  <rect x="0" y="0" width="600" height="440" rx="24" fill="#ecf6f3"/>
  <g fill="#fff"><ellipse cx="92" cy="78" rx="38" ry="20"/><ellipse cx="124" cy="66" rx="30" ry="22"/><ellipse cx="150" cy="82" rx="28" ry="16"/></g>
  <rect x="0" y="392" width="600" height="48" fill="#cfe8e0"/>
  <rect x="540" y="330" width="9" height="64" fill="#6b4f3a"/><circle cx="544" cy="312" r="36" fill="#12705f"/><circle cx="526" cy="326" r="22" fill="#0d5a4c"/>
  <rect x="392" y="84" width="30" height="64" fill="#8f0a45"/>
  <rect x="110" y="180" width="380" height="214" fill="#fff" stroke="#14212b" stroke-width="3"/>
  <rect x="113" y="183" width="374" height="206" fill="#fdf4f8"/>
  <polygon points="88,188 300,56 512,188" fill="#b5004a"/><polygon points="88,188 300,56 512,188" fill="none" stroke="#8f0a45" stroke-width="3" stroke-linejoin="round"/>
  <g transform="translate(372 96) rotate(31.6)" fill="#1f3342" stroke="#cfe8e0" stroke-width="1.2">
    <rect x="0" y="0" width="38" height="24"/><rect x="40" y="0" width="38" height="24"/><rect x="0" y="26" width="38" height="24"/><rect x="40" y="26" width="38" height="24"/>
    <path d="M19 0v24M59 0v24M19 26v24M59 26v24" fill="none"/></g>
  <rect x="113" y="350" width="374" height="39" fill="#e9d6c3"/>
  <path d="M143 350v39M173 350v39M203 350v39M233 350v39M263 350v39M293 350v39M323 350v39M353 350v39M383 350v39M413 350v39M443 350v39M473 350v39" stroke="#d8bfa6" stroke-width="2"/>
  <rect x="253" y="183" width="6" height="140" fill="#14212b" opacity=".12"/>
  <rect x="125" y="205" width="112" height="38" rx="3" fill="#14212b" opacity=".88"/>
  <rect x="122" y="294" width="118" height="8" rx="2" fill="#8a939a"/><rect x="125" y="302" width="112" height="48" fill="#14212b"/>
  <path d="M162 302v48M199 302v48" stroke="#33424d" stroke-width="2"/><rect x="140" y="288" width="26" height="6" rx="2" fill="#33424d"/><path d="M210 294v-16h10" fill="none" stroke="#8a939a" stroke-width="3"/>
  <rect x="300" y="208" width="72" height="62" fill="#cfe8e0" stroke="#14212b" stroke-width="3"/><path d="M336 208v62M300 239h72" stroke="#14212b" stroke-width="3"/>
  <rect x="262" y="214" width="26" height="42" rx="3" fill="#fff" stroke="#14212b" stroke-width="2"/><circle cx="275" cy="244" r="3" fill="#12705f"/>
  <path d="M268 256v94M282 256v94" stroke="#8a939a" stroke-width="3"/>
  <rect x="290" y="324" width="56" height="26" rx="2" fill="#8a939a"/><rect x="292" y="282" width="52" height="36" rx="3" fill="#14212b"/><rect x="314" y="318" width="8" height="6" fill="#14212b"/>
  <rect x="362" y="290" width="112" height="28" rx="9" fill="#0d5a4c"/><rect x="362" y="312" width="112" height="28" rx="6" fill="#12705f"/>
  <rect x="354" y="304" width="16" height="36" rx="6" fill="#0d5a4c"/><rect x="466" y="304" width="16" height="36" rx="6" fill="#0d5a4c"/>
  <path d="M368 340v8M468 340v8" stroke="#14212b" stroke-width="4"/>
</svg>'''

HUIS = '''  <!-- opstal of inboedel -->
  <div class="fx-ct__wrap"><section class="fx-ct__sec fx-verz__huis" id="opstal-inboedel">
    <div class="fx-home__kop">
      <p class="fx-ct__sub">Opstal of inboedel?</p>
      <h2>Wat valt onder welke verzekering?</h2>
      <p>Klik op de plusjes in het huis. Zo ziet u in één oogopslag wat bij het huis hoort, en wat bij uw spullen.</p>
    </div>
    <div class="fx-verz__huisgrid">
      <div class="fx-verz__huisbeeld">
        ''' + HUIS_SVG + '''
        ''' + ''.join('<button type="button" class="fx-verz__hs" data-id="%s" style="left:%s%%;top:%s%%" aria-pressed="false" aria-controls="hs-%s"><span aria-hidden="true">+</span><span class="fx-verz__vh">%s</span></button>'
                      % (i, x, y, i, t) for i, x, y, s, l, t, u in HUIS_ITEMS) + '''
      </div>
      <div class="fx-verz__huisinfo">
        <ul class="fx-verz__huislijst" aria-live="polite">''' + ''.join('''
          <li id="hs-%s" data-soort="%s"><span class="fx-verz__soort fx-verz__soort--%s">%s</span><b>%s</b><p>%s</p></li>'''
                                                                         % (i, s, s, l, t, u) for i, x, y, s, l, t, u in HUIS_ITEMS) + '''
        </ul>
        <ul class="fx-verz__legenda" aria-hidden="true"><li><i class="fx-verz__stip--opstal"></i>Opstal: het huis zelf</li><li><i class="fx-verz__stip--inboedel"></i>Inboedel: uw spullen</li></ul>
      </div>
    </div>
    <script>
    (function(){
      var s=document.getElementById('opstal-inboedel'); if(!s) return;
      s.classList.add('is-js');
      var kn=[].slice.call(s.querySelectorAll('.fx-verz__hs')), it=[].slice.call(s.querySelectorAll('.fx-verz__huislijst li'));
      function kies(id){
        kn.forEach(function(b){var a=b.getAttribute('data-id')===id; b.setAttribute('aria-pressed',a?'true':'false'); b.classList.toggle('is-aan',a);});
        it.forEach(function(l){l.hidden=l.id!=='hs-'+id;});
      }
      kn.forEach(function(b){ b.addEventListener('click',function(){kies(b.getAttribute('data-id'));}); });
      kies('dak');
    })();
    </script>
  </section></div>

'''
EIGEN['Woonverzekering']['licht'] = True
EIGEN['Woonverzekering']['extra'] = HUIS

# -*- coding: utf-8 -*-
"""Maakt de inhoud van de vier subpagina's onder Verzekeringen, in één vaste opbouw."""
import io, sys
sys.path.insert(0, '/tmp/claude-0/-home-user-finectfinancials/eb3bde67-f228-5f8e-b9ee-dcd3a00cb56a/scratchpad/home/verz/')
from sub_extra import *

SP = '/tmp/claude-0/-home-user-finectfinancials/eb3bde67-f228-5f8e-b9ee-dcd3a00cb56a/scratchpad/home/verz/'

ANDERE = [('Woonverzekering', '../verzekeringen/woonverzekering/'),
          ('Aansprakelijkheidsverzekering', '../verzekeringen/aansprakelijkheidsverzekering/'),
          ('Autoverzekering', '../verzekeringen/autoverzekering/'),
          ('Polischeck', '../verzekeringen/polischeck/'),
          ('Alle verzekeringen', '../verzekeringen/')]


FOTO = {'Woonverzekering': 'verz-woon', 'Aansprakelijkheidsverzekering': 'verz-avp',
        'Autoverzekering': 'verz-auto', 'Polischeck': 'verz-polischeck'}
UITLEG = {'Woonverzekering': ('{ICO_HUIS}', 'Opstal en inboedel: uw huis en alles wat erin staat.'),
          'Aansprakelijkheidsverzekering': ('{ICO_SCHILD}', 'Voor schade die u of uw gezin bij een ander veroorzaakt.'),
          'Autoverzekering': ('{ICO_AUTO}', 'WA, beperkt casco of allrisk: welke dekking past bij uw auto?'),
          'Polischeck': ('{ICO_CHECK}', 'Uw verzekeringen nagekeken: te veel, te weinig of goed.')}


def welniet(wel, niet, welkop='Wel verzekerd', nietkop='Niet verzekerd'):
    w = ''.join(f'<li>{x}</li>' for x in wel); n = ''.join(f'<li>{x}</li>' for x in niet)
    return (f'<div class="fx-verz__welniet"><div><span class="fx-verz__lijstkop">{welkop}</span><ul class="fx-verz__lijst">{w}</ul></div>'
            f'<div><span class="fx-verz__lijstkop fx-verz__lijstkop--let">{nietkop}</span><ul class="fx-verz__lijst fx-verz__lijst--niet">{n}</ul></div></div>')


def kort(punten):
    return ('      <div class="fx-verz__kort"><h2>In het kort</h2><ul class="fx-verz__lijst">' +
            ''.join(f'<li>{p}</li>' for p in punten) + '</ul></div>\n')


def pagina(naam, sub, h1, lead, tekst, vragen, hulp, hulpkop, hoe, knop2=('Vraag een polischeck aan', '../verzekeringen/polischeck/'), schade=True):
    andere = ''.join(f'<li><a href="{u}">{n}</a></li>' for n, u in ANDERE if n != naam)
    gerel = ''.join(f'<div class="fx-verz__pkaart fx-verz__pkaart--link"><span class="fx-ct__ico">{UITLEG[n][0]}</span><h3>{n.replace("heidsverzekering","heids&shy;verzekering")}</h3>'
                    f'<p>{UITLEG[n][1]}</p><a class="fx-verz__pmeer" href="{u}">Lees verder</a></div>'
                    for n, u in ANDERE if n != naam and n in UITLEG)
    vr = ''.join(f'''
      <details{' open' if i == 0 else ''}>
        <summary><h3>{v}</h3></summary>
        <p>{a}</p>
      </details>''' for i, (v, a) in enumerate(vragen))
    return f'''<div class="fx-verz">

  <!-- kop -->
  <section class="fx-verz__kop fx-verz__kop--foto" style="--kop:url(../wp-content/uploads/finect/{FOTO[naam]}.jpg);--kop-m:url(../wp-content/uploads/finect/{FOTO[naam]}-mobiel.jpg)"><div class="fx-ct__wrap">
    <p class="fx-verz__kruimel"><a href="../">Home</a> &rsaquo; <a href="../verzekeringen/">Verzekeringen</a> &rsaquo; {naam}</p>
    {CHIP}
    <p class="fx-ct__sub">{sub}</p>
    <h1>{h1}</h1>
    <p class="fx-ct__lead">{lead}</p>
    <div class="fx-ct__btns">
      <a class="fx-ct__btn fx-ct__btn--m" href="tel:+31630679790">Bel 06 30 67 97 90</a>
      <a class="fx-ct__btn fx-ct__btn--o" href="{knop2[1]}">{knop2[0]}</a>
    </div>
    <p class="fx-verz__heldlink"><a href="#hulp">{hulpkop}</a></p>
  </div></section>

{CIJFERS}
  <!-- tekst -->
  <div class="fx-ct__wrap"><section class="fx-ct__sec fx-verz__artikel">
    <div class="fx-verz__tekst">
{tekst}
    </div>
    <div class="fx-verz__zij">
      <div class="fx-verz__zijkaart fx-verz__zijkaart--navy">
        <h2>Liever even overleggen?</h2>
        <p>{EIGEN[naam]['zij']}</p>
        <div class="fx-ct__btns"><a class="fx-ct__btn fx-ct__btn--m" href="tel:+31630679790">Bel 06 30 67 97 90</a></div>
        <p style="margin:14px 0 0;"><a class="fx-verz__licht" href="mailto:info@finect.nl">info@finect.nl</a></p>
      </div>
      <div class="fx-verz__zijkaart">
        <h2>Meer over verzekeringen</h2>
        <ul>{andere}</ul>
      </div>
    </div>
  </section></div>

{hulp}{hoe}{EIGEN[naam]['schade']}{EIGEN[naam]['werk']}{EIGEN[naam]['review']}{EIGEN[naam]['wie']}  <!-- ook interessant -->
  <div class="fx-ct__wrap"><section class="fx-ct__sec fx-verz__andere">
    <p class="fx-ct__sub">Ook interessant</p>
    <h2 style="margin-bottom:28px;">Andere verzekeringen</h2>
    <div class="fx-verz__gerelateerd">{gerel}</div>
  </section></div>

  <!-- vragen -->
  <div class="fx-ct__band"><div class="fx-ct__wrap"><section class="fx-ct__sec fx-ct__faq">
    <div>
      <p class="fx-ct__sub">Vragen</p>
      <h2>Vragen over {(naam[0].lower() + naam[1:]).replace('heidsverzekering','heids&shy;verzekering')}</h2>
      <p>Nog een vraag over uw {naam.lower().replace('polischeck','verzekeringen').replace('heidsverzekering','heids&shy;verzekering')}? Bel gerust, daar hoeft u geen afspraak voor te maken.</p>
      <p style="margin-top:22px;"><a class="fx-ct__btn fx-ct__btn--o" href="../contact/">Plan een gesprek</a></p>
    </div>
    <div>{vr}
    </div>
  </section></div></div>

  <!-- contact -->
  <div class="fx-ct__wrap"><section class="fx-ct__sec fx-ct__hero">
    <div>
      <p class="fx-ct__sub">Contact</p>
      <h2>{EIGEN[naam]['contact'][0]}</h2>
      <p class="fx-ct__lead">{EIGEN[naam]['contact'][1]}</p>
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
    </ul>
  </section></div>

</div>
'''


KORT_WOON = kort(['De woonhuisverzekering is voor het huis zelf, de inboedelverzekering voor wat erin staat.',
                  'Huurt u? Dan heeft u alleen een inboedelverzekering nodig.',
                  'Laat na een verbouwing het verzekerde bedrag nakijken, anders bent u misschien onderverzekerd.'])
KORT_AVP = kort(['Voor schade die u of uw gezin per ongeluk bij een ander veroorzaakt.',
                 'Een lage premie voor een risico dat groot kan zijn.',
                 'Let op bij geleende spullen en bij schade tijdens uw werk.'])
KORT_AUTO = kort(['WA is wettelijk verplicht.',
                  'Bij een nieuwe, dure auto is allrisk meestal verstandig.',
                  'Uw schadevrije jaren neemt u mee als u overstapt.'])
KORT_CHECK = kort(['Ik kijk naar dekking, verzekerde bedragen, eigen risico en premie.',
                   'U krijgt mijn advies zonder verplichting.',
                   'Een foto of scan van uw polissen is genoeg.'])
WELNIET_WOON = welniet(
    ['Brand, blikseminslag en ontploffing', 'Storm', 'Inbraak en diefstal',
     'Water dat plotseling uit een leiding of apparaat stroomt'],
    ['Slijtage en achterstallig onderhoud', 'Schade door grondwater', 'Overstroming door een dijkdoorbraak',
     'Schade die met opzet is veroorzaakt'], nietkop='Meestal niet verzekerd')

# ------------------------------------------------------------------ woonverzekering
WOON = KORT_WOON + '''      <h2>Twee verzekeringen voor uw woning</h2>
      <p>Een woonverzekering bestaat meestal uit twee delen: de woonhuisverzekering en de inboedelverzekering. Veel verzekeraars bieden ze samen aan, maar het blijven twee dekkingen met elk een eigen verzekerd bedrag.</p>
      <table class="fx-verz__tabel">
        <thead><tr><td></td><th>Woonhuisverzekering (opstal)</th><th>Inboedelverzekering</th></tr></thead>
        <tbody>
          <tr><th>Wat is verzekerd</th><td>Het huis zelf: muren, dak, vloeren, ramen en vaste onderdelen zoals keuken en badkamer</td><td>Wat u bij een verhuizing meeneemt, zoals meubels, kleding en apparatuur</td></tr>
          <tr><th>Voor wie</th><td>Huiseigenaren</td><td>Huurders en huiseigenaren</td></tr>
          <tr><th>Verzekerd bedrag</th><td>De herbouwwaarde van het huis</td><td>De waarde van uw spullen</td></tr>
        </tbody>
      </table>

      <h2>Wat dekt een woonhuisverzekering?</h2>
      <p>De woonhuisverzekering, ook wel opstalverzekering, vergoedt schade aan het huis zelf. Denk aan schade door brand, storm, inbraak of water dat plotseling uit een leiding stroomt. Vaste onderdelen zoals de keuken, de badkamer en de cv-ketel vallen er meestal ook onder.</p>
      <p>Het verzekerde bedrag is de herbouwwaarde: wat het kost om uw huis opnieuw op te bouwen. Dat is iets anders dan de WOZ-waarde of de verkoopprijs, want de grond telt niet mee.</p>
      <p>Heeft u een hypotheek? Dan vraagt de geldverstrekker bijna altijd om een woonhuisverzekering.</p>

      <h2>Wat dekt een inboedelverzekering?</h2>
      <p>De inboedelverzekering vergoedt schade aan of verlies van uw spullen in huis, bijvoorbeeld door brand, inbraak of waterschade. Vaak kunt u kiezen tussen een basisdekking en een uitgebreide dekking die ook een ongelukje dekt, zoals koffie over de laptop.</p>
      <p>Let op bij sieraden, computers en andere kostbaarheden. Daarvoor gelden vaak maximale bedragen. Heeft u veel waardevolle spullen, dan kan een aparte dekking verstandig zijn.</p>

      <h2>Wat is wel en niet verzekerd?</h2>
      <p>De precieze dekking verschilt per verzekeraar en per polis. Dit geldt in de meeste gevallen:</p>
''' + WELNIET_WOON + '''
      <h2>Onderverzekering voorkomen</h2>
      <p>U bent onderverzekerd als het verzekerde bedrag lager is dan de werkelijke waarde. Bij schade krijgt u dan maar een deel vergoed. Veel verzekeraars bieden een garantie tegen onderverzekering als u de waarde bepaalt met hun rekenhulp. Laat het verzekerde bedrag in elk geval nakijken:</p>
      <ul>
        <li>na een verbouwing, een uitbouw of een nieuwe keuken;</li>
        <li>na grote aankopen voor in huis;</li>
        <li>als u lang niet naar uw polis heeft gekeken.</li>
      </ul>

      <h2>Huurt u een woning?</h2>
      <p>Dan heeft u geen woonhuisverzekering nodig, want het gebouw verzekert de verhuurder. Een inboedelverzekering wel. Heeft u zelf iets aan de woning verbeterd, zoals een nieuwe keuken of vloer? Dan kunt u dat vaak meeverzekeren op uw inboedelverzekering. Dat heet huurdersbelang.</p>'''

WOON_VR = [
    ('Is een woonhuisverzekering verplicht?',
     'Niet volgens de wet. Heeft u een hypotheek, dan vraagt de geldverstrekker er wel bijna altijd om.'),
    ('Wat is het verschil tussen herbouwwaarde en WOZ-waarde?',
     'De herbouwwaarde is wat het kost om uw huis opnieuw op te bouwen. De WOZ-waarde is de marktwaarde die de gemeente vaststelt, inclusief de grond. Voor uw woonhuisverzekering telt de herbouwwaarde.'),
    ('Is glas verzekerd?',
     'Bij veel woonhuisverzekeringen kunt u glas meeverzekeren, en soms zit het er standaard in. Dat verschilt per verzekeraar.'),
    ('Moet ik een verbouwing doorgeven?',
     'Dat is verstandig. Een verbouwing verhoogt vaak de herbouwwaarde. Geeft u het niet door, dan loopt u het risico onderverzekerd te zijn.'),
    ('Kan ik opstal en inboedel bij verschillende verzekeraars hebben?',
     'Dat kan. Het heeft wel voordelen om ze bij dezelfde verzekeraar te hebben. Bij schade aan zowel het huis als uw spullen, bijvoorbeeld na een brand, heeft u dan één aanspreekpunt.'),
    ('Wat is huurdersbelang?',
     'Huurdersbelang zijn verbeteringen die u als huurder zelf aan de woning heeft laten aanbrengen, zoals een nieuwe keuken, vloer of schuur. U kunt die vaak meeverzekeren op uw inboedelverzekering.'),
    ('Zijn zonnepanelen verzekerd?',
     'Zonnepanelen op uw eigen dak vallen meestal onder de woonhuisverzekering, omdat ze vast aan het huis zitten. Geef ze wel door, zodat het verzekerde bedrag klopt. Huurt u de panelen, dan ligt het anders.'),
]

# ------------------------------------------------------------------ aansprakelijkheid
AVP = KORT_AVP + '''      <h2>Wat is een aansprakelijkheidsverzekering?</h2>
      <p>Veroorzaakt u schade bij een ander, dan bent u daar volgens de wet vaak aansprakelijk voor. De aansprakelijkheidsverzekering voor particulieren, ook wel AVP genoemd, betaalt die schade. Het gaat om schade aan spullen van een ander en om letselschade.</p>
      <p>De premie is laag, maar een schade kan groot zijn. Daarom raad ik bijna iedereen aan om deze verzekering te hebben.</p>
      <h2>Wat is wel en niet verzekerd?</h2>
''' + welniet(
    ['U stoot bij vrienden een dure vaas om.', 'Uw kind fietst tegen een geparkeerde auto.', 'Uw hond bijt een voorbijganger.',
     'U laat per ongeluk een lekkage ontstaan die schade geeft bij de benedenburen.'],
    ['Schade aan uw eigen spullen. Daarvoor is de <a href="../verzekeringen/woonverzekering/">inboedelverzekering</a>.',
     'Schade die u met opzet veroorzaakt.',
     'Schade met een auto, motor of scooter. Daarvoor is de <a href="../verzekeringen/autoverzekering/">autoverzekering</a>.',
     'Schade tijdens uw werk. Bent u ondernemer, dan is daarvoor een <a href="../zakelijk/">bedrijfs&shy;aansprakelijkheids&shy;verzekering</a>.'],
    welkop='Wel verzekerd, bijvoorbeeld') + '''

      <h2>Waar moet u op letten?</h2>
      <h3>Alleenstaand of gezin</h3>
      <p>Een gezinsdekking geldt voor iedereen die bij u woont, zoals uw partner en kinderen. Een kind dat op kamers woont, is vaak nog meeverzekerd. Dat verschilt per verzekeraar.</p>
      <h3>Geleende en gehuurde spullen</h3>
      <p>Schade aan spullen die u leent of huurt, zoals een geleende laptop of een vakantiehuis, is niet altijd of maar beperkt verzekerd. Verzekeraars gaan hier verschillend mee om. Dit is een van de punten waarop polissen echt verschillen.</p>
      <h3>Kinderen jonger dan 14 jaar</h3>
      <p>Kinderen onder de 14 zijn volgens de wet niet zelf aansprakelijk. Veel verzekeringen vergoeden de schade dan toch als u dat wilt, zodat u de verhouding met de buren of vrienden goed houdt.</p>
      <h3>Verzekerd bedrag en eigen risico</h3>
      <p>Het verzekerde bedrag is meestal minimaal een miljoen euro per gebeurtenis. Kijk ook naar het eigen risico, zeker bij schade door kinderen.</p>'''

AVP_VR = [
    ('Is een aansprakelijkheidsverzekering verplicht?',
     'Nee, voor particulieren niet. Ik raad hem wel bijna iedereen aan, omdat de premie laag is en een schade hoog kan oplopen.'),
    ('Is schade door mijn hond verzekerd?',
     'Schade die uw huisdier bij een ander veroorzaakt, is meestal verzekerd via uw aansprakelijkheidsverzekering. Voor sommige dieren, zoals paarden, gelden vaak andere regels.'),
    ('Ben ik verzekerd als ik iets leen?',
     'Niet altijd. Schade aan geleende of gehuurde spullen is bij veel verzekeraars beperkt of uitgesloten. Ik kijk graag met u hoe dat bij uw polis zit.'),
    ('Geldt de verzekering ook in het buitenland?',
     'Bij de meeste verzekeraars wel. De aansprakelijkheidsverzekering voor particulieren geldt meestal wereldwijd.'),
    ('Ben ik als zzp\'er verzekerd tijdens mijn werk?',
     'Nee. Schade die u tijdens uw werk veroorzaakt, valt niet onder de aansprakelijkheidsverzekering voor particulieren. Daarvoor is een bedrijfsaansprakelijkheidsverzekering.'),
    ('Is mijn kind op kamers nog meeverzekerd?',
     'Vaak wel, zolang uw kind studeert en niet samenwoont of getrouwd is. De voorwaarden verschillen per verzekeraar. Het is goed om dit na te kijken.'),
    ('Wat is het verschil tussen een gezinsdekking en een alleenstaandendekking?',
     'Een alleenstaandendekking geldt alleen voor u. Een gezinsdekking geldt voor iedereen die bij u woont, zoals uw partner en kinderen. Gaat u samenwonen of krijgt u kinderen, pas uw verzekering dan aan.'),
]

# ------------------------------------------------------------------ autoverzekering
AUTO = KORT_AUTO + '''      <h2>De drie dekkingen</h2>
      <table class="fx-verz__tabel">
        <thead><tr><th>Dekking</th><th>Wat is verzekerd</th><th>Past vaak bij</th></tr></thead>
        <tbody>
          <tr><th>WA</th><td>Schade die u met uw auto bij een ander veroorzaakt. Wettelijk verplicht.</td><td>Oudere auto's met een lage dagwaarde</td></tr>
          <tr><th>WA en beperkt casco</th><td>WA, plus schade aan uw eigen auto door onder meer diefstal, brand, storm, ruitschade en een aanrijding met loslopende dieren.</td><td>Auto's van gemiddelde leeftijd</td></tr>
          <tr><th>Allrisk</th><td>WA en beperkt casco, plus schade aan uw eigen auto die u zelf veroorzaakt, zoals een aanrijding of een kras bij het parkeren.</td><td>Nieuwe en jonge auto's, en auto's met een financiering</td></tr>
        </tbody>
      </table>

      <h2>Welke dekking kiest u?</h2>
      <p>De leeftijd en de waarde van uw auto zijn een goede vuistregel. Hoe nieuwer en duurder de auto, hoe eerder allrisk loont. Bij een oudere auto kan de extra premie voor allrisk hoger zijn dan wat u ooit vergoed krijgt. Ik reken het met u door.</p>

      <h2>Schadevrije jaren en bonus-malus</h2>
      <p>Voor elk jaar zonder schade krijgt u korting. Claimt u een schade, dan zakt u een aantal treden op de bonus-malusladder en betaalt u meer premie. Bij een kleine schade kan het daarom voordeliger zijn om die zelf te betalen. Ik help u die afweging te maken.</p>

      <h2>Aanvullende dekkingen</h2>
      <ul>
        <li>Pechhulp in Nederland of in Europa.</li>
        <li>Een verzekering voor inzittenden, voor letsel of schade van u en uw passagiers.</li>
        <li>Rechtsbijstand voor het verkeer, bijvoorbeeld als de tegenpartij de schade niet wil betalen.</li>
        <li>Vervangend vervoer na een schade.</li>
      </ul>
      <p>Niet alles is voor iedereen nodig. Heeft u al pechhulp via een lidmaatschap? Dan hoeft u het niet dubbel te verzekeren.</p>'''

AUTO_VR = [
    ('Is een autoverzekering verplicht?',
     'Ja. Een WA-verzekering is wettelijk verplicht voor elke auto met een Nederlands kenteken, ook als u er niet mee rijdt. Alleen als het kenteken geschorst is, hoeft het niet.'),
    ('Wat is het verschil tussen dagwaarde en aanschafwaarde?',
     'De dagwaarde is wat uw auto op dit moment waard is. Veel allriskverzekeringen vergoeden in de eerste jaren de aanschafwaarde of werken met een vaste waarderegeling. Hoe lang dat geldt, verschilt per verzekeraar.'),
    ('Wat gebeurt er met mijn schadevrije jaren als ik overstap?',
     'Die neemt u mee. Schadevrije jaren worden centraal geregistreerd, zodat uw nieuwe verzekeraar ze kan overnemen.'),
    ('Is ruitschade verzekerd?',
     'Bij beperkt casco en allrisk meestal wel. Laat u de ruit herstellen bij een bedrijf waar de verzekeraar mee samenwerkt, dan geldt vaak geen of een laag eigen risico.'),
    ('Mag iemand anders in mijn auto rijden?',
     'Meestal wel. Rijdt er regelmatig iemand anders in uw auto, zoals uw partner of een kind, geef dat dan door. Voor jonge bestuurders geldt vaak een hoger eigen risico.'),
    ('Wanneer is allrisk niet meer nodig?',
     'Daar is geen vaste leeftijd voor. Kijk naar de waarde van de auto en de premie. Is de extra premie voor allrisk in een paar jaar hoger dan wat de auto nog waard is, dan is beperkt casco vaak genoeg.'),
    ('Ben ik in het buitenland verzekerd?',
     'In de landen op uw internationale verzekeringsbewijs, vroeger de groene kaart, bent u in elk geval voor WA verzekerd. Daar staan de meeste Europese landen op. Of casco en pechhulp ook in het buitenland gelden, verschilt per polis.'),
]

# ------------------------------------------------------------------ polischeck
CHECK = KORT_CHECK + '''      <h2>Waarom een polischeck?</h2>
      <p>Verzekeringen sluit u vaak af op een moment dat er iets verandert, zoals bij het kopen van een huis. Daarna kijkt bijna niemand er nog naar, terwijl uw situatie wel verandert. Het gevolg is dat u dubbel verzekerd bent, onderverzekerd, of meer premie betaalt dan nodig.</p>
      <h3>Wat ik vaak tegenkom</h3>
      <ul>
        <li>Een verzekerd bedrag voor het huis dat na een verbouwing niet is aangepast.</li>
        <li>Dubbele dekking, bijvoorbeeld een annulerings- of rechtsbijstandverzekering die al in een andere polis zit.</li>
        <li>Allrisk op een auto waarvoor een lichtere dekking volstaat.</li>
        <li>Een aansprakelijkheidsverzekering voor een alleenstaande, terwijl er inmiddels een gezin is.</li>
        <li>Losse polissen die samen in een pakket voordeliger zijn.</li>
      </ul>

      <h2>Hoe werkt het?</h2>
      <ol class="fx-ct__stap">
        <li><b>U stuurt uw polissen</b><span>De polisbladen of een overzicht van uw verzekeringen, bijvoorbeeld uit de app van uw verzekeraar.</span></li>
        <li><b>Ik zoek het uit</b><span>Ik kijk naar dekking, verzekerde bedragen, eigen risico en premie, en vergelijk dat met wat er nu te krijgen is.</span></li>
        <li><b>We bespreken het</b><span>Bij u thuis, op kantoor of online. U hoort wat ik zou aanpassen en waarom.</span></li>
        <li><b>U beslist</b><span>Wilt u iets veranderen, dan regel ik het, ook het opzeggen van de oude polis.</span></li>
      </ol>

      <h2>Wat heb ik van u nodig?</h2>
      <ul>
        <li>De polisbladen van uw verzekeringen, of het overzicht uit de app of de website van uw verzekeraar.</li>
        <li>Het bouwjaar en de grootte van uw huis, en of u heeft verbouwd.</li>
        <li>Het merk, het type en het bouwjaar van uw auto.</li>
        <li>Of er iets gaat veranderen, zoals verhuizen, samenwonen of met pensioen gaan.</li>
      </ul>

      <h2>Wanneer is een polischeck zinvol?</h2>
      <p>Bij elke grote verandering: verhuizen, verbouwen, samenwonen, gezinsuitbreiding, een nieuwe auto, zelfstandig ondernemer worden of met pensioen gaan. Verandert er niets, dan is eens in de paar jaar een goede gewoonte.</p>
      <p>Wilt u een polischeck? Mail uw polissen naar <a href="mailto:info@finect.nl">info@finect.nl</a> of bel mij op <a href="tel:+31630679790">06 30 67 97 90</a>.</p>'''

CHECK_VR = [
    ('Moet ik na de polischeck overstappen?',
     'Nee. U krijgt mijn advies en beslist zelf. Is er niets te verbeteren, dan zeg ik dat eerlijk.'),
    ('Kan ik mijn verzekeringen tussentijds opzeggen?',
     'Bij de meeste particuliere schadeverzekeringen kunt u na het eerste contractjaar per maand opzeggen. Als u overstapt, regel ik het zo dat u niet onverzekerd raakt.'),
    ('Doet u ook een polischeck voor ondernemers?',
     'Ja. Voor ondernemers kijk ik ook naar bedrijfsaansprakelijkheid, gebouw en inventaris, bedrijfsschade en het wagenpark.'),
    ('Hoe lever ik mijn polissen aan?',
     'Per mail naar info@finect.nl, of ik neem ze mee als ik bij u langskom. Een foto met uw telefoon volstaat.'),
    ('Wat als ik dubbel verzekerd ben?',
     'Dan zoek ik uit welke verzekering u het beste kunt houden en regel ik het opzeggen van de andere. Soms lijkt iets dubbel, maar is het dat niet helemaal. Ook dat zoek ik voor u uit.'),
    ('Kijkt u ook naar verzekeringen via mijn werkgever?',
     'Ja, als u die meestuurt. Denk aan een arbeidsongeschiktheidsverzekering of een collectieve korting. Zo voorkomt u dat u iets dubbel verzekert.'),
]

BESTANDEN = {
    'woonverzekering.html': pagina(
        'Woonverzekering', 'Wonen', 'Woonverzekering: opstal en inboedel',
        'Uw huis en alles wat erin staat, goed verzekerd. Ik leg uit wat een woonhuis- en een inboedelverzekering dekken, en zoek de dekking die bij uw woning past.',
        WOON, WOON_VR, HULP_WOON, 'Doe de snelle check: klopt uw woonverzekering nog?', DUO_WOON),
    'aansprakelijkheid.html': pagina(
        'Aansprakelijkheidsverzekering', 'Persoonlijk', 'Aansprakelijkheids&shy;verzekering voor particulieren',
        'Een ongelukje zit in een klein hoekje. Met een aansprakelijkheidsverzekering bent u verzekerd als u of uw gezin per ongeluk schade veroorzaakt bij een ander.',
        AVP, AVP_VR, HULP_AVP, 'Test uzelf: verzekerd of niet?', DUO_AVP),
    'autoverzekering.html': pagina(
        'Autoverzekering', 'Onderweg', 'Autoverzekering: WA, beperkt casco of allrisk?',
        'Welke dekking past bij uw auto? Ik zet de verschillen op een rij en vergelijk premie, eigen risico en voorwaarden voor u.',
        AUTO, AUTO_VR, HULP_AUTO, 'Welke dekking past bij uw auto? Zie het in drie vragen', DUO_AUTO),
    'polischeck.html': pagina(
        'Polischeck', 'Polischeck', 'Polischeck: weet hoe u ervoor staat',
        'Ik loop uw bestaande verzekeringen na en zeg wat er te veel is, wat er te weinig is en wat er goed staat. Vaak levert dat premie op. Klopt alles al, dan hoort u dat ook.',
        CHECK, CHECK_VR, HULP_CHECK, 'Doe de snelle check: is het tijd voor een polischeck?', DUO_CHECK,
        knop2=('Stuur uw polissen', 'mailto:info@finect.nl'), schade=False),
}
for naam, inhoud in BESTANDEN.items():
    io.open(SP + naam, 'w', encoding='utf-8').write(inhoud)
    print('geschreven', naam)

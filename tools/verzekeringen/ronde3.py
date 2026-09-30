import io,re
t=io.open('inhoud.html',encoding='utf-8').read()
def r(a,b,n=1):
    global t
    assert t.count(a)==n,(t.count(a),a[:70]); t=t.replace(a,b)

# A. adviseur in het openingsbeeld
r('''        <p class="fx-ct__sub">Verzekeringen in Apeldoorn en omgeving</p>''',
'''        <div class="fx-verz__adviseur"><img src="../wp-content/uploads/2025/07/DSCF4417.jpg" alt="" width="56" height="56" decoding="async"><span><b>Fred Koeling</b>Uw vaste adviseur, Certified Financial Planner</span></div>
        <p class="fx-ct__sub">Verzekeringen in Apeldoorn en omgeving</p>''')

# B. cijferbalk in plaats van de vertrouwensregel
i=t.index('    <ul class="fx-verz__vertrouwen">'); j=t.index('    </ul>',i)+len('    </ul>')
t=t[:i]+'''    <ul class="fx-verz__cijfers">
      <li><b>5,0</b><span>uit 16 beoordelingen op <a href="https://maps.app.goo.gl/CUqTeR8SEaGoE9rx9" target="_blank" rel="noopener">Google</a></span></li>
      <li><b>22+</b><span>jaar ervaring in het vak</span></li>
      <li><b>2015</b><span>onafhankelijk sinds</span></li>
      <li><b>1</b><span>vaste adviseur, ook bij schade</span></li>
    </ul>'''+t[j:]

# C. icoon per verzekering
ico={'Woonhuisverzekering (opstal)':'ICO_HUIS','Inboedelverzekering':'ICO_BANK','Aansprakelijkheids&shy;verzekering (AVP)':'ICO_SCHILD',
     'Rechtsbijstandverzekering':'ICO_VERGELIJK','Autoverzekering':'ICO_AUTO','Reisverzekering':'ICO_VLIEG',
     'Overlijdensrisicoverzekering':'ICO_LEVEN','Uitvaartverzekering':'ICO_BLOEM',"Arbeids&shy;ongeschiktheids&shy;verzekering voor zzp'ers":'ICO_HART'}
for naam,ic in ico.items():
    a='<h4>%s</h4>'%naam
    assert t.count(a)==1,naam
    t=t.replace(a,'<span class="fx-verz__pico">{%s}</span><h4>%s</h4>'%(ic,naam))

# D. actueel bij wonen
a='''        <div class="fx-verz__producten">
          <div class="fx-verz__pkaart fx-verz__pkaart--link"><span class="fx-verz__pico">{ICO_HUIS}</span>'''
assert t.count(a)==1
i=t.index(a); j=t.index('        </div>\n      </div>',i)
t=t[:j]+'''        </div>
        <p class="fx-verz__tip"><b>Zonnepanelen, een laadpaal of een warmtepomp?</b> Uw huis verandert mee met de tijd. Laat nakijken of die nieuwe onderdelen goed verzekerd zijn, en of het verzekerde bedrag nog klopt.</p>
'''+t[j+len('        </div>\n'):]

# E. extra situatie: appartement
tabs_eind='</button></div>\n'
i=t.index('<div class="fx-verz__tabs"'); j=t.index(tabs_eind,i)
t=t[:j]+'</button><button class="fx-verz__tab" type="button" role="tab" id="wg-tab-4" aria-controls="wg-4" aria-selected="false" tabindex="-1">{ICO_GEBOUW}Appartement'+t[j:]
a='''      <div class="fx-verz__paneel" role="tabpanel" id="wg-3" aria-labelledby="wg-tab-3">'''
i=t.index(a); j=t.index('      </div>\n    </div>\n    <script>',i)
t=t[:j]+'''      </div>
      <div class="fx-verz__paneel" role="tabpanel" id="wg-4" aria-labelledby="wg-tab-4">
        <h3>U heeft een appartement</h3>
        <div class="fx-verz__paneelgrid">
          <div><span class="fx-verz__lijstkop">Belangrijk</span><ul class="fx-verz__lijst"><li>Een inboedelverzekering en een aansprakelijkheidsverzekering.</li><li>Het gebouw zelf verzekert de VvE meestal met een opstalverzekering voor het hele complex.</li></ul></div>
          <div><span class="fx-verz__lijstkop fx-verz__lijstkop--let">Let op</span><ul class="fx-verz__lijst fx-verz__lijst--let"><li>Heeft u uw keuken of badkamer vernieuwd? Kijk dan of die verbetering onder de polis van de VvE valt, of dat u hem zelf moet meeverzekeren.</li></ul></div>
        </div>
'''+t[j:]

# F. blok Uw adviseur, na de klantervaringen
r('''  <!-- vragen -->''','''  <!-- uw adviseur -->
  <div class="fx-ct__wrap"><section class="fx-ct__sec fx-verz__wie">
    <div class="fx-verz__wiefoto"><img src="../wp-content/uploads/2025/07/DSCF4417.jpg" alt="Fred Koeling, onafhankelijk verzekeringsadviseur in Apeldoorn" width="482" height="640" loading="lazy" decoding="async"></div>
    <div>
      <p class="fx-ct__sub">Uw adviseur</p>
      <h2>U spreekt steeds mij</h2>
      <p class="fx-ct__lead">Mijn naam is Fred Koeling. Ik regel verzekeringen voor particulieren en ondernemers in Apeldoorn en omgeving, en ik blijf daarna uw aanspreekpunt.</p>
      <p>Ik werk sinds 2015 als zelfstandig adviseur, met ruim 22 jaar ervaring in het vak. Als Certified Financial Planner kijk ik niet alleen naar losse polissen, maar naar het geheel: uw huis, uw inkomen en uw gezin.</p>
      <blockquote class="fx-verz__citaat">&ldquo;Ik zeg het ook als u iets niet nodig heeft.&rdquo;</blockquote>
      <div class="fx-ct__btns"><a class="fx-ct__btn fx-ct__btn--m" href="tel:+31630679790">Bel 06 30 67 97 90</a><a class="fx-ct__btn fx-ct__btn--o" href="../over-finect/">Lees meer over mij</a></div>
    </div>
  </section></div>

  <!-- vragen -->''')

# G. pakketblok met foto
r('''    <div>
      <p class="fx-ct__sub">Pakketpolis</p>''','''    <div>
      <div class="fx-verz__pakfoto"><img src="../wp-content/uploads/finect/dienst-hypotheek.jpg" alt="" width="1259" height="840" loading="lazy" decoding="async"></div>
      <p class="fx-ct__sub">Pakketpolis</p>''')
io.open('inhoud.html','w',encoding='utf-8').write(t); print('ok')

import io,re
t=io.open('inhoud.html',encoding='utf-8').read()
def tussen(a,b):
    i=t.index(a); j=t.index(b,i); return i,j
i,j=tussen('        <ul class="fx-home__feiten">','      </div>\n    </div>\n  </section>')
t=t[:i]+t[j:]
snel='''
  <!-- snelkeuze -->
  <div class="fx-ct__wrap">
    <nav class="fx-verz__snel" aria-label="Snel naar">
      <a class="fx-verz__snelkaart" href="../verzekeringen/woonverzekering/"><span class="fx-ct__ico">{ICO_HUIS}</span><b>Woonverzekering</b><span class="fx-verz__sneltekst">Opstal en inboedel</span><i>Meer weten</i></a>
      <a class="fx-verz__snelkaart" href="../verzekeringen/aansprakelijkheidsverzekering/"><span class="fx-ct__ico">{ICO_SCHILD}</span><b>Aansprakelijkheid</b><span class="fx-verz__sneltekst">Voor u en uw gezin</span><i>Meer weten</i></a>
      <a class="fx-verz__snelkaart" href="../verzekeringen/autoverzekering/"><span class="fx-ct__ico">{ICO_AUTO}</span><b>Autoverzekering</b><span class="fx-verz__sneltekst">WA, beperkt casco, allrisk</span><i>Meer weten</i></a>
      <a class="fx-verz__snelkaart" href="../verzekeringen/polischeck/"><span class="fx-ct__ico">{ICO_CHECK}</span><b>Polischeck</b><span class="fx-verz__sneltekst">Weet hoe u ervoor staat</span><i>Meer weten</i></a>
    </nav>
    <ul class="fx-verz__vertrouwen">
      <li><span><span class="fx-ct__sterren" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</span> 5,0 uit 16 beoordelingen op <a href="https://maps.app.goo.gl/CUqTeR8SEaGoE9rx9" target="_blank" rel="noopener">Google</a></span></li>
      <li>Onafhankelijk sinds 2015</li>
      <li>Certified Financial Planner</li>
      <li>AFM-vergunning 12047700</li>
    </ul>
  </div>
'''
t=t.replace('  <!-- waarom via een adviseur -->', snel+'\n  <!-- waarom via een adviseur -->',1)

i=t.index('    <div class="fx-verz__groepen">'); j=t.index('    <p class="fx-verz__zakelijk">')
blok=t[i:j]
groepen=re.findall(r'<div class="fx-verz__groep">\s*<div class="fx-verz__groepkop">(.*?)</div>(.*?)\n      </div>\n(?=      <div class="fx-verz__groep">|    </div>)',blok,re.S)
assert len(groepen)==4,len(groepen)
nieuw=''
for kop,prod in groepen:
    kaarten=''
    for pm in re.finditer(r'<div class="fx-verz__product">\s*<h4>(.*?)</h4>\s*<p>(.*?)</p>\s*</div>',prod,re.S):
        h4,p=pm.group(1),pm.group(2)
        link=re.match(r'<a href="([^"]+)">(.*?)</a>',h4)
        m2=re.search(r'\s*<a href="([^"]+)">([^<]+)</a>$',p)
        if link:
            naam=link.group(2); href=link.group(1)
            kaarten+='          <div class="fx-verz__pkaart fx-verz__pkaart--link"><h4>%s</h4><p>%s</p><a class="fx-verz__pmeer" href="%s">Meer over de %s</a></div>\n'%(naam,p,href,naam.split(' (')[0].lower())
        elif m2:
            kaarten+='          <div class="fx-verz__pkaart fx-verz__pkaart--link"><h4>%s</h4><p>%s</p><a class="fx-verz__pmeer" href="%s">%s</a></div>\n'%(h4,p[:m2.start()],m2.group(1),m2.group(2))
        else:
            kaarten+='          <div class="fx-verz__pkaart"><h4>%s</h4><p>%s</p></div>\n'%(h4,p)
    nieuw+='      <div class="fx-verz__groeprij">\n        <div class="fx-verz__groepkop">%s</div>\n        <div class="fx-verz__producten">\n%s        </div>\n      </div>\n'%(kop,kaarten)
t=t[:i]+'    <div class="fx-verz__overzicht">\n'+nieuw+'    </div>\n'+t[j:]

i=t.index('    <div class="fx-verz__wegwijzer">'); j=t.index('  </section></div>',i)
sits=re.findall(r'<h3>(.*?)</h3>\s*<p><span class="fx-verz__label">Belangrijk</span>(.*?)</p>\s*<p><span class="fx-verz__label fx-verz__label--let">Let op</span>(.*?)</p>',t[i:j],re.S)
assert len(sits)==4
korte=['Huurder','Eigen huis','Gezin',"Zzp'er"]
iconen=['{ICO_SLEUTEL}','{ICO_HUIS}','{ICO_GEZIN}','{ICO_KOFFER}']
tabs=''
for n in range(4):
    sel='true' if n==0 else 'false'
    ti='' if n==0 else ' tabindex="-1"'
    tabs+='<button class="fx-verz__tab" type="button" role="tab" id="wg-tab-%d" aria-controls="wg-%d" aria-selected="%s"%s>%s%s</button>'%(n,n,sel,ti,iconen[n],korte[n])
def zinnen(s):
    return [z.strip() for z in re.split(r'(?<=\.)\s+',s.strip()) if z.strip()]
panelen=''
for n,(h,bel,let) in enumerate(sits):
    b=''.join('<li>%s</li>'%z for z in zinnen(bel)); l=''.join('<li>%s</li>'%z for z in zinnen(let))
    panelen+='''      <div class="fx-verz__paneel" role="tabpanel" id="wg-%d" aria-labelledby="wg-tab-%d">
        <h3>%s</h3>
        <div class="fx-verz__paneelgrid">
          <div><span class="fx-verz__lijstkop">Belangrijk</span><ul class="fx-verz__lijst">%s</ul></div>
          <div><span class="fx-verz__lijstkop fx-verz__lijstkop--let">Let op</span><ul class="fx-verz__lijst fx-verz__lijst--let">%s</ul></div>
        </div>
      </div>
'''%(n,n,h,b,l)
weg='''    <div class="fx-verz__wegwijzer2" id="wegwijzer">
      <div class="fx-verz__tabs" role="tablist" aria-label="Kies uw situatie" hidden>'''+tabs+'''</div>
'''+panelen+'''    </div>
    <script>
    (function(){
      var w=document.getElementById('wegwijzer'); if(!w) return;
      var lijst=w.querySelector('[role=tablist]'), tabs=[].slice.call(w.querySelectorAll('[role=tab]')), pan=[].slice.call(w.querySelectorAll('[role=tabpanel]'));
      lijst.hidden=false; w.classList.add('fx-verz--tabs');
      function kies(i,focus){tabs.forEach(function(t,n){t.setAttribute('aria-selected',n===i?'true':'false');t.tabIndex=n===i?0:-1;pan[n].hidden=n!==i;}); if(focus) tabs[i].focus();}
      tabs.forEach(function(t,n){t.addEventListener('click',function(){kies(n);});
        t.addEventListener('keydown',function(e){var k=e.key; if(k==='ArrowRight'||k==='ArrowLeft'){e.preventDefault();kies((n+(k==='ArrowRight'?1:tabs.length-1))%tabs.length,true);}});});
      kies(0);
    })();
    </script>
'''
t=t[:i]+weg+t[j:]
io.open('inhoud.html','w',encoding='utf-8').write(t); print('ok', len(t))

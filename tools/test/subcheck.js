// rekent de rekenhulpen op de hypotheek-subpagina's door en controleert links en ankers op alle vijf de pagina's
const {chromium}=require('/opt/node22/lib/node_modules/playwright/index.js');
const B='http://127.0.0.1:8099/'+(process.argv[2]||'voorbeeld/')+'hypotheken/';
(async()=>{const b=await chromium.launch(); const pg=await b.newPage({viewport:{width:390,height:900}}); const fout=[];
 pg.on('pageerror',e=>fout.push('js '+e.message));
 const zet=async(id,v)=>pg.$eval(id,(e,v)=>{e.value=v;e.dispatchEvent(new Event('input',{bubbles:true}));},String(v));
 const uit=async id=>pg.$eval(id,e=>e.innerText.replace(/\s+/g,' '));
 function kijk(naam,t,moet,nietMoet=[]){const mis=moet.filter(v=>!t.includes(v)), teveel=nietMoet.filter(v=>t.includes(v));
  console.log(mis.length||teveel.length?'FOUT':'ok  ',naam,(mis.length?'| mist: '+mis.join(', '):'')+(teveel.length?' | onterecht: '+teveel.join(', '):''),mis.length||teveel.length?'| '+t:'');}
 // oversluiten
 await pg.goto(B+'oversluiten/',{waitUntil:'networkidle'});
 await zet('#fxSchuld',300000); await zet('#fxRente',4.5);
 kijk('oversluiten kort',await uit('#fxOverUit'),['€ 1.125','€ 125 per maand','binnen een jaar af','lagere risicoklasse','386.000','10 tot 20 procent']);
 await pg.check('input[name=eind][value=mid]'); kijk('oversluiten mid',await uit('#fxOverUit'),['1 tot 5 jaar','boeterente']);
 await pg.check('input[name=eind][value=lang]'); await pg.check('input[name=nhg][value=ja]');
 kijk('oversluiten lang nhg',await uit('#fxOverUit'),['meer dan 5 jaar','zonder risico-opslag'],['lagere risicoklasse']);
 await pg.check('input[name=nhg][value=nee]'); await pg.check('input[name=waarde][value=nee]');
 kijk('oversluiten waarde nee',await uit('#fxOverUit'),['Boetevrij'],['lagere risicoklasse','risico-opslag']);
 // volgend huis
 await pg.goto(B+'volgend-huis-kopen/',{waitUntil:'networkidle'});
 await zet('#fxVerkoop',450000); await zet('#fxHyp',250000); await zet('#fxKosten',6000); await zet('#fxNieuw',550000);
 kijk('volgend normaal',await uit('#fxVolgUit'),['€ 194.000','€ 356.000','Bijleenregeling','drie jaar','overbruggingskrediet'],['genoeg voor de hele koopsom']);
 await zet('#fxVerkoop',300000); await zet('#fxHyp',320000);
 kijk('volgend restschuld',await uit('#fxVolgUit'),['Geen','€ 26.000','schuld over']);
 await zet('#fxVerkoop',900000); await zet('#fxHyp',100000); await zet('#fxKosten',10000); await zet('#fxNieuw',500000);
 kijk('volgend genoeg',await uit('#fxVolgUit'),['€ 790.000','€ 0','genoeg voor de hele koopsom']);
 // zzp
 await pg.goto(B+'zzp-en-ondernemers/',{waitUntil:'networkidle'});
 kijk('zzp leeg',await uit('#fxOndUit'),['Beantwoord de vier vragen']);
 for (const [n,v] of [['duur','kort'],['vorm','ez'],['trend','lager'],['loon','ja']]) await pg.check(`input[name=${n}][value=${v}]`);
 kijk('zzp kort',await uit('#fxOndUit'),['Korter dan een jaar','loondienst kan nu al','lagere bedrag','eenmanszaak','prognose','KvK']);
 for (const [n,v] of [['duur','lang'],['vorm','bv'],['trend','hoger'],['loon','nee']]) await pg.check(`input[name=${n}][value=${v}]`);
 kijk('zzp bv lang',await uit('#fxOndUit'),['3 jaar of langer','dga','gemiddelde'],['prognose','loondienst kan nu al']);
 await pg.check('input[name=vorm][value=vof]'); kijk('zzp vof',await uit('#fxOndUit'),['vof of maatschap']);
 // hoofdpagina: check met link naar de subpagina
 await pg.goto(B,{waitUntil:'networkidle'});
 for (const v of ['starter','zzp','alleen','orient']){ await pg.click(`input[value=${v}] + span`); await pg.waitForTimeout(400); }
 const ul=await pg.$eval('#fxUitslag',e=>({t:e.innerText,h:[...e.querySelectorAll('a.fx-hyp__meer')].map(a=>a.getAttribute('href'))}));
 kijk('hoofdpagina check',ul.t+' '+ul.h.join(' '),['Alles over uw eerste huis kopen',"zzp'ers en ondernemers",'eerste-huis-kopen/','zzp-en-ondernemers/','intentieverklaring'].slice(0,4));
 // links en ankers op alle pagina's
 const gezien=new Set();
 for (const s of ['','eerste-huis-kopen/','volgend-huis-kopen/','oversluiten/','zzp-en-ondernemers/']){
  await pg.goto(B+s,{waitUntil:'networkidle'});
  for (const h of await pg.$$eval('a[href^="#"]',a=>a.map(x=>x.getAttribute('href')))) if(h.length>1 && !(await pg.$(h))) fout.push(s+' anker mist '+h);
  for (const h of await pg.$$eval('a[href]',a=>a.map(x=>x.href).filter(x=>x.startsWith('http://127.0.0.1')))){
   const u=h.split('#')[0]; if(gezien.has(u)) continue; gezien.add(u);
   const r=await pg.request.get(u); if(r.status()!==200) fout.push('kapot '+u+' '+r.status());
   const a=h.split('#')[1]; if(a){ const p2=await b.newPage(); await p2.goto(u); if(!(await p2.$('#'+a))) fout.push('anker mist '+h); await p2.close(); } }
 }
 console.log('links gecontroleerd:',gezien.size); console.log(fout.length?fout:'geen fouten'); await b.close();})();

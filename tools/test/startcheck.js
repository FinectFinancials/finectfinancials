// klikt de rekenhulp op /voorbeeld/hypotheken/eerste-huis-kopen/ door en controleert de uitkomsten
const {chromium}=require('/opt/node22/lib/node_modules/playwright/index.js');
const pad=process.argv[2]||'voorbeeld/hypotheken/eerste-huis-kopen/';
(async()=>{const b=await chromium.launch(); const pg=await b.newPage({viewport:{width:390,height:900}}); const fout=[];
 pg.on('pageerror',e=>fout.push('js '+e.message));
 await pg.goto('http://127.0.0.1:8099/'+pad,{waitUntil:'networkidle'});
 async function zet(koop,jaar,samen,u,p){
  await pg.$eval('#fxKoop',(e,v)=>{e.value=v;e.dispatchEvent(new Event('input',{bubbles:true}));},String(koop));
  for (const [n,v] of [['jaar',jaar],['samen',samen],['leeftijd',u]]) await pg.check(`input[name=${n}][value="${v}"]`);
  if(p) await pg.check(`input[name=partner][value="${p}"]`);
  return pg.$eval('#fxStartUit',e=>e.innerText.replace(/\s+/g,' '));
 }
 const gevallen=[
  [[350000,'2026','alleen','jong'],['U betaalt niets','scheelt u € 7.000','onder de NHG-grens']],
  [[560000,'2026','alleen','jong'],['€ 11.200','boven de grens van € 555.000','zonder NHG']],
  [[560000,'2027','alleen','jong'],['U betaalt niets','scheelt u € 11.200','eind 2026 bekend']],
  [[400000,'2026','samen','jong','oud'],['€ 4.000','helft','bespaart € 4.000']],
  [[400000,'2026','samen','jong','jong'],['U betaalt niets','scheelt u € 8.000']],
  [[400000,'2026','alleen','oud'],['€ 8.000','tot 35 jaar']],
  [[480000,'2026','alleen','jong'],['€ 498.200','kan NHG dus nog']],
 ];
 for (const [inv,verwacht] of gevallen){ const t=await zet(...inv); const mis=verwacht.filter(v=>!t.includes(v));
  console.log(mis.length?'FOUT':'ok  ',inv.join(' '),mis.length?'| mist: '+mis.join(', ')+' | '+t:''); }
 // partnervraag alleen zichtbaar bij samen
 await pg.check('input[name=samen][value=alleen]'); const verborgen=await pg.$eval('#fxPartner',e=>e.hidden);
 await pg.check('input[name=samen][value=samen]'); const zicht=await pg.$eval('#fxPartner',e=>!e.hidden);
 console.log('partnervraag', verborgen&&zicht?'ok':'FOUT');
 // toetsenbord: schuif met pijltjes
 await pg.focus('#fxKoop'); const voor=await pg.$eval('#fxKoopUit',e=>e.textContent); await pg.keyboard.press('ArrowRight');
 const na=await pg.$eval('#fxKoopUit',e=>e.textContent); console.log('toetsenbord', voor!==na?'ok':'FOUT', voor,'->',na, await pg.$eval('#fxKoop',e=>e.getAttribute('aria-valuetext')));
 // ankers en links
 for (const h of await pg.$$eval('a[href^="#"]',a=>a.map(x=>x.getAttribute('href')))) if(h.length>1 && !(await pg.$(h))) fout.push('anker mist '+h);
 for (const h of [...new Set(await pg.$$eval('a[href]',a=>a.map(x=>x.href).filter(x=>x.startsWith('http://127.0.0.1'))))]){
  const r=await pg.request.get(h.split('#')[0]); if(r.status()!==200) fout.push('kapot '+h+' '+r.status()); }
 await pg.$eval('#hulp',e=>e.scrollIntoView()); await pg.screenshot({path:'startcheck-390.png'});
 console.log(fout.length?fout:'geen fouten'); await b.close();})();

const {chromium}=require('/opt/node22/lib/node_modules/playwright/index.js');
const B='http://127.0.0.1:8099/voorbeeld/hypotheken/';
(async()=>{const b=await chromium.launch(); const fout=[];
 for (const w of [1440,390]){ const pg=await b.newPage({viewport:{width:w,height:900}}); pg.on('pageerror',e=>fout.push(w+' js '+e.message));
  await pg.goto(B,{waitUntil:'networkidle'});
  async function kies(n,v){ await pg.locator(`input[name=${n}][value=${v}]`).locator('xpath=..').click(); await pg.waitForTimeout(260); }
  async function uit(){ return pg.evaluate(()=>({zicht:!document.getElementById('fxUitslag').hidden,focus:document.activeElement.id,
    stappen:[...document.querySelectorAll('[data-lijst=stappen] li')].map(l=>l.textContent.slice(0,55)),
    nodig:[...document.querySelectorAll('[data-lijst=nodig] li')].map(l=>l.textContent.slice(0,55)),
    letop:[...document.querySelectorAll('[data-lijst=letop] p')].map(l=>l.textContent.slice(0,70))})); }
  const nr=()=>pg.textContent('.fx-verz__stapnr');
  await kies('situatie','starter'); console.log(w,'na starter:',await nr());
  await kies('inkomen','vast'); await kies('samen','samen');
  await pg.click('.fx-verz__terug'); console.log(w,'terug:',await nr()); await kies('samen','samen');
  await kies('wanneer','nu'); if(w===1440) console.log('starter/vast/samen/nu',JSON.stringify(await uit(),null,1));
  await pg.click('.fx-verz__opnieuw'); console.log(w,'opnieuw:',await nr());
  await kies('situatie','over'); console.log(w,'na over:',await nr()); await kies('inkomen','zzp'); console.log(w,'na zzp:',await nr());
  await kies('wanneer','maanden'); const r2=await uit(); console.log(w,'over/zzp: stappen',r2.stappen.length,'nodig',r2.nodig.length,'letop',JSON.stringify(r2.letop));
  await pg.click('.fx-verz__opnieuw');
  await kies('situatie','uit'); await kies('inkomen','pensioen'); await kies('wanneer','orient'); const r3=await uit(); console.log(w,'uit/pensioen/orient letop',JSON.stringify(r3.letop),'nodig',JSON.stringify(r3.nodig));
  await pg.click('.fx-verz__opnieuw');
  await kies('situatie','verb'); await kies('inkomen','flex'); await kies('wanneer','maanden'); const r4=await uit(); console.log(w,'verb/flex letop',JSON.stringify(r4.letop));
  // toetsenbord
  await pg.click('.fx-verz__opnieuw'); await pg.focus('input[name=situatie][value=starter]'); await pg.keyboard.press('Space'); await pg.keyboard.press('ArrowDown'); await pg.waitForTimeout(300);
  const k1=await nr(); await pg.keyboard.press('Enter'); await pg.waitForTimeout(200);
  console.log(w,'toetsenbord: bleef op',k1,'na Enter',await nr(),'gekozen',await pg.evaluate(()=>document.querySelector('input[name=situatie]:checked').value));
  // snelkeuze-anker
  await pg.goto(B,{waitUntil:'networkidle'}); await pg.click('.fx-verz__snelkaart[href="#oversluiten"]'); await pg.waitForTimeout(700);
  console.log(w,'anker oversluiten top:',await pg.evaluate(()=>Math.round(document.getElementById('oversluiten').getBoundingClientRect().top)));
  if(w===390){ const balk=await pg.evaluate(()=>{const e=document.querySelector('.fx-verz__balk');const r=e.getBoundingClientRect();return {disp:getComputedStyle(e).display,bottom:Math.round(r.bottom),ban:Math.round(document.getElementById('fxBanier').getBoundingClientRect().top)};}); console.log('balk',JSON.stringify(balk)); }
  // links
  if(w===1440){ const gezien={}; for(const h of await pg.$$eval('a[href]',a=>a.map(x=>x.href).filter(u=>u.startsWith('http://127.0.0.1')))){ const u=h.split('#')[0]; if(gezien[u])continue; gezien[u]=1; const x=await pg.request.get(u); if(x.status()!==200) fout.push('kapot '+u); }
    for (const a of await pg.$$eval('a[href^="#"]',a=>a.map(x=>x.getAttribute('href')))) if(a.length>1&&!(await pg.$(a))) fout.push('anker mist '+a);
    console.log('links gecontroleerd',Object.keys(gezien).length,'menu Zakelijk items',await pg.$$eval('.menu-item-3875 .sub-menu a',a=>a.length)); }
  await pg.close(); }
 console.log(fout.length?fout:'geen fouten'); await b.close();})();

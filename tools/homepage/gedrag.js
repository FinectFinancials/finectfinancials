// test gedrag en uiterlijk van een pagina; schrijft hashes en afbeeldingen per toestand
const {chromium}=require('/opt/node22/lib/node_modules/playwright/index.js');
const crypto=require('crypto');
const pad=process.argv[2], naam=process.argv[3];
const SP='/tmp/claude-0/-home-user-finectfinancials/eb3bde67-f228-5f8e-b9ee-dcd3a00cb56a/scratchpad/home/gedrag/';
require('fs').mkdirSync(SP,{recursive:true});
const h=b=>crypto.createHash('md5').update(b).digest('hex').slice(0,10);
(async()=>{
  const b=await chromium.launch();
  const uit={};
  async function pagina(w,hgt){
    const ctx=await b.newContext({viewport:{width:w,height:hgt}, hasTouch:w<800, isMobile:w<800});
    const pg=await ctx.newPage(); const fout=[]; let n=0, bytes=0;
    pg.on('pageerror',e=>fout.push('js: '+e.message));
    pg.on('console',m=>{ if(m.type()==='error') fout.push('console: '+m.text()); });
    pg.on('requestfailed',r=>fout.push('mislukt: '+r.url()));
    pg.on('response',async r=>{ n++; if(r.status()>=400) fout.push(r.status()+' '+r.url()); try{ const bb=await r.body(); bytes+=bb.length;}catch(e){} });
    await pg.goto('http://127.0.0.1:8099/'+pad,{waitUntil:'networkidle'});
    return {ctx,pg,fout,tel:()=>({n,bytes})};
  }
  async function shot(pg,key,opts={}){ const buf=await pg.screenshot(opts); require('fs').writeFileSync(SP+naam+'-'+key+'.png',buf); uit[key]=h(buf); }
  // desktop
  let {ctx,pg,fout,tel}=await pagina(1440,900);
  await pg.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=600){scrollTo(0,y);await new Promise(r=>setTimeout(r,50));}scrollTo(0,0);});
  await pg.waitForLoadState('networkidle'); await pg.waitForTimeout(500);
  uit.verzoeken=tel();
  await shot(pg,'d-vol',{fullPage:true});
  await pg.hover('.wgl-theme-header .menu-item-has-children > a'); await pg.waitForTimeout(700);
  await shot(pg,'d-submenu',{clip:{x:0,y:0,width:1440,height:450}});
  await pg.mouse.move(5,600); await pg.waitForTimeout(600);
  await pg.goto('http://127.0.0.1:8099/'+pad,{waitUntil:'networkidle'});
  await pg.mouse.wheel(0,1500); await pg.waitForTimeout(1200);
  uit['d-sticky-zichtbaar']=await pg.evaluate(()=>{const s=document.querySelector('.wgl-sticky-header');const r=s.getBoundingClientRect();return getComputedStyle(s).visibility+' top='+Math.round(r.top)+' h='+Math.round(r.height)+' cls='+s.className;});
  await shot(pg,'d-sticky',{clip:{x:0,y:0,width:1440,height:200}});
  uit.fouten_d=fout.slice(); await ctx.close();
  // mobiel
  ({ctx,pg,fout,tel}=await pagina(390,844));
  await pg.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=600){scrollTo(0,y);await new Promise(r=>setTimeout(r,50));}scrollTo(0,0);});
  await pg.waitForLoadState('networkidle'); await pg.waitForTimeout(500);
  await shot(pg,'m-vol',{fullPage:true});
  await pg.click('.wgl-mobile-header .mobile-hamburger-toggle'); await pg.waitForTimeout(1000);
  await shot(pg,'m-menu');
  const sub=await pg.$('.mobile_nav_wrapper .menu-item-has-children .button_switcher, .wgl-menu_outer .menu-item-has-children .button_switcher');
  if(sub){ await sub.click(); await pg.waitForTimeout(800); await shot(pg,'m-submenu'); } else uit['m-submenu']='geen knop';
  await pg.goto('http://127.0.0.1:8099/'+pad,{waitUntil:'networkidle'});
  const zk=pg.locator('.header_search-button:visible').first();
  if(await zk.count()){ await zk.click(); await pg.waitForTimeout(900); await shot(pg,'m-zoek'); } else uit['m-zoek']='geen zichtbare knop';
  await pg.goto('http://127.0.0.1:8099/'+pad,{waitUntil:'networkidle'});
  await pg.evaluate(()=>scrollTo(0,1500)); await pg.waitForTimeout(1200);
  await shot(pg,'m-scroll');
  // reviews
  await pg.evaluate(()=>{const d=document.querySelector('#fxCtDots'); if(d) d.scrollIntoView({block:'center'});}); await pg.waitForTimeout(300);
  const dots=await pg.$$('#fxCtDots button, #fxCtDots li'); if(dots[2]){await dots[2].click(); await pg.waitForTimeout(900);}
  uit['m-review-actief']=await pg.evaluate(()=>[...document.querySelectorAll('.fx-ct__quote')].findIndex(q=>q.classList.contains('is-on')));
  uit.fouten_m=fout.slice(); await ctx.close();
  // tussenmaten: tablet en kleine laptop
  for (const w of [1280,1024,768]) {
    ({ctx,pg,fout,tel}=await pagina(w,900));
    await pg.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=600){scrollTo(0,y);await new Promise(r=>setTimeout(r,50));}scrollTo(0,0);});
    await pg.waitForLoadState('networkidle'); await pg.waitForTimeout(500);
    await shot(pg,'w'+w,{fullPage:true});
    if (fout.length) uit['fouten_'+w]=fout.slice();
    await ctx.close();
  }
  await b.close();
  console.log(JSON.stringify(uit,null,1));
})();

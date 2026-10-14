// schermafbeeldingen op 1440 en 390, met foutcontrole en overloop
const {chromium}=require('/opt/node22/lib/node_modules/playwright/index.js');
const pad=process.argv[2], naam=process.argv[3];
(async()=>{const b=await chromium.launch();
 for (const w of [1440,390]){const pg=await b.newPage({viewport:{width:w,height:900}}); const fout=[];
  pg.on('pageerror',e=>fout.push('js: '+e.message)); pg.on('response',r=>{if(r.status()>=400)fout.push(r.status()+' '+r.url());});
  pg.on('requestfailed',r=>fout.push('mislukt '+r.url()));
  await pg.goto('http://127.0.0.1:8099/'+pad,{waitUntil:'networkidle'});
  await pg.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=600){scrollTo(0,y);await new Promise(r=>setTimeout(r,50));}scrollTo(0,0);});
  await pg.waitForLoadState('networkidle'); await pg.waitForTimeout(300);
  await pg.addStyleTag({content:'#fxBanier,.fx-verz__balk{display:none!important}'});
  await pg.screenshot({fullPage:true,path:naam+'-'+w+'.png'});
  const info=await pg.evaluate(()=>({h:document.body.scrollHeight,over:document.documentElement.scrollWidth-innerWidth}));
  console.log(w,JSON.stringify(info),fout.length?fout.join(' | '):'geen fouten'); await pg.close();}
 await b.close();})();

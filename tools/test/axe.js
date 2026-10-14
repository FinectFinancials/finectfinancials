const {chromium}=require('/opt/node22/lib/node_modules/playwright/index.js');
const fs=require('fs'); const axe=fs.readFileSync(__dirname+'/axe.min.js','utf8');
(async()=>{const b=await chromium.launch();
 for (const w of [1440,390]){const pg=await b.newPage({viewport:{width:w,height:900}});
  await pg.goto('http://127.0.0.1:8099/'+process.argv[2],{waitUntil:'networkidle'});
  await pg.addScriptTag({content:axe});
  const r=await pg.evaluate(async()=>{const x=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','best-practice']}});
    return x.violations.map(v=>v.id+' ('+v.impact+') '+v.nodes.length+'x: '+v.nodes.slice(0,3).map(n=>n.target.join(' ')).join(' ; '));});
  console.log('===',w); r.filter(l=>!/fxBanier|landmark-unique|region/.test(l)).forEach(l=>console.log(l)); await pg.close();}
 await b.close();})();

// schermafbeelding van één element: node elfoto.js <pad> <selector> <breedte> <naam>
const {chromium}=require('/opt/node22/lib/node_modules/playwright/index.js');
(async()=>{const b=await chromium.launch(); const pg=await b.newPage({viewport:{width:+process.argv[4],height:900}});
 await pg.goto('http://127.0.0.1:8099/'+process.argv[2],{waitUntil:'networkidle'});
 await pg.addStyleTag({content:'#fxBanier,.fx-verz__balk{display:none!important}'});
 await (await pg.$(process.argv[3])).screenshot({path:process.argv[5]}); await b.close();})();

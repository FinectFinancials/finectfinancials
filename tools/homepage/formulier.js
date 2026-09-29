// verstuurt het contactformulier leeg en maakt een foto van de foutmeldingen,
// daarna focus op een veld en hover op de knop
const {chromium}=require('/opt/node22/lib/node_modules/playwright/index.js');
const crypto=require('crypto');
(async()=>{
  const b=await chromium.launch();
  for (const pad of process.argv.slice(2)) {
    const uit=[];
    for (const w of [1440,390]) {
      const pg=await b.newPage({viewport:{width:w,height:900}});
      await pg.goto('http://127.0.0.1:8099/'+pad,{waitUntil:'networkidle'});
      const f=pg.locator('#fxForm');
      await f.scrollIntoViewIfNeeded();
      await f.locator('[type=submit], button').last().click(); await pg.waitForTimeout(500);
      uit.push(crypto.createHash('md5').update(await f.screenshot()).digest('hex').slice(0,10));
      await f.locator('input, textarea').first().focus(); await pg.waitForTimeout(300);
      uit.push(crypto.createHash('md5').update(await f.screenshot()).digest('hex').slice(0,10));
      await f.locator('[type=submit], button').last().hover(); await pg.waitForTimeout(400);
      uit.push(crypto.createHash('md5').update(await f.screenshot()).digest('hex').slice(0,10));
      await pg.close();
    }
    console.log(pad, uit.join(' '));
  }
  await b.close();
})();

// meet laadtijd op een gesimuleerde telefoon (trage 4G, 4x tragere processor)
const {chromium}=require('/opt/node22/lib/node_modules/playwright/index.js');
(async()=>{
  const b=await chromium.launch();
  const res={};
  for (const pad of (process.argv.slice(2).length?process.argv.slice(2):['_orig/','_schoon/'])) {
    res[pad]=[];
    for (let i=0;i<5;i++){
      const ctx=await b.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
      const pg=await ctx.newPage();
      const cdp=await ctx.newCDPSession(pg);
      await cdp.send('Network.enable');
      await cdp.send('Network.emulateNetworkConditions',{offline:false,latency:150,downloadThroughput:1.6*1024*1024/8,uploadThroughput:750*1024/8});
      await cdp.send('Emulation.setCPUThrottlingRate',{rate:4});
      await pg.addInitScript(()=>{window.__lcp=0;new PerformanceObserver(l=>{for(const e of l.getEntries())window.__lcp=e.startTime;}).observe({type:'largest-contentful-paint',buffered:true});});
      await pg.goto('http://127.0.0.1:8099/'+pad,{waitUntil:'load'});
      await pg.waitForTimeout(1500);
      const m=await pg.evaluate(()=>{const n=performance.getEntriesByType('navigation')[0];const fcp=performance.getEntriesByName('first-contentful-paint')[0];
        return {fcp:Math.round(fcp?fcp.startTime:0),lcp:Math.round(window.__lcp),klaar:Math.round(n.loadEventEnd)};});
      res[pad].push(m); await ctx.close();
    }
  }
  await b.close();
  const med=a=>a.slice().sort((x,y)=>x-y)[Math.floor(a.length/2)];
  for (const [p,r] of Object.entries(res)) console.log(p,'FCP',med(r.map(x=>x.fcp)),'ms  LCP',med(r.map(x=>x.lcp)),'ms  volledig geladen',med(r.map(x=>x.klaar)),'ms');
})();

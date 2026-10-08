const {chromium}=require('playwright');
const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
 const w=path.dirname(__dirname),report=[];
 const files={site:'D:/작업/꿀단지/kkuldanji_web/posts/finger-joint-pain-rheumatoid-arthritis-morning-stiffness.html',naver:path.join(w,fs.readdirSync(w).find(x=>x.endsWith('_네이버블로그용.html')))};
 for(const [name,file] of Object.entries(files))for(const width of [1365,390]){
  const page=await browser.newPage({viewport:{width,height:900},deviceScaleFactor:1});
  await page.route(/^https?:/,r=>r.abort());
  await page.goto(pathToFileURL(file).href,{waitUntil:'load'});
  await page.locator('img').evaluateAll(xs=>xs.forEach(x=>x.loading='eager'));
  await page.waitForTimeout(700);
  const results=await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,images:[...document.images].map(x=>({src:x.getAttribute('src'),loaded:x.complete&&x.naturalWidth>0})),anchors:[...document.querySelectorAll('a[href^="#"]')].filter(a=>a.hash.length>1&&!document.getElementById(decodeURIComponent(a.hash.slice(1)))).map(a=>a.hash)}));
  await page.screenshot({path:path.join(__dirname,`${name}-${width}-top.png`)});
  const pic=page.locator('img[src$="post03.jpg"]');await pic.scrollIntoViewIfNeeded();await page.waitForTimeout(1200);
  await page.screenshot({path:path.join(__dirname,`${name}-${width}-exercise.png`)});
  report.push({name,...results});await page.close();
 }
 fs.writeFileSync(path.join(__dirname,'browser-review.json'),JSON.stringify(report,null,2));
 console.log(JSON.stringify(report.map(x=>({name:x.name,width:x.width,scrollWidth:x.scrollWidth,images:x.images.length,broken:x.images.filter(i=>!i.loaded),missingAnchors:x.anchors})),null,2));
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});

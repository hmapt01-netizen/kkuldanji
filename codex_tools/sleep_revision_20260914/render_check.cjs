const fs=require('fs'),path=require('path');
const {chromium}=require('C:/Users/lim/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=path.resolve(__dirname,'../..'),web=path.join(root,'kkuldanji_web');
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 const specs=['sleep-hygiene-guide','sleep-lying-down-eyes-closed-20min-rule'].map(name=>({name,base:web,url:'https://preview.invalid/posts/'+name+'.html',naver:false}));
 const ndir=fs.readdirSync(path.join(root,'꿀단지 네이버')).find(x=>x.startsWith('13_'));
 const nbase=path.join(root,'꿀단지 네이버',ndir),nf=fs.readdirSync(nbase).find(x=>x.endsWith('.html'));
 specs.push({name:'naver13',base:nbase,url:'https://preview.invalid/'+encodeURIComponent(nf),naver:true});
 const report=[];
 for(const spec of specs){
  const context=await browser.newContext({viewport:{width:390,height:844}});
  await context.route('**/*',async route=>{
   const u=new URL(route.request().url());
   const assetHost=['honeyjar.co.kr','www.honeyjar.co.kr'].includes(u.hostname)&&u.pathname.startsWith('/images/');
   if(u.hostname!=='preview.invalid'&&!assetHost)return route.abort();
   const base=assetHost?web:spec.base;
   const file=path.resolve(base,'.'+decodeURIComponent(u.pathname));
   if(!file.startsWith(base+path.sep)||!fs.existsSync(file)||!fs.statSync(file).isFile())return route.abort();
   const types={'.html':'text/html; charset=utf-8','.css':'text/css','.js':'application/javascript','.jpg':'image/jpeg','.png':'image/png','.svg':'image/svg+xml'};
   await route.fulfill({body:fs.readFileSync(file),contentType:types[path.extname(file)]||'application/octet-stream'});
  });
  const page=await context.newPage();await page.goto(spec.url,{waitUntil:'load'});
  const selector=spec.naver?'#naverContent':'.article-body-content';
  for(const im of await page.locator(selector+' img, .article-featured-img-box img').all()) {await im.scrollIntoViewIfNeeded();await im.evaluate(el=>el.decode());}
  await page.locator('h1').first().scrollIntoViewIfNeeded();
  // Let content-visibility:auto repaint after moving back from the final lazy image.
  await page.waitForTimeout(400);
  await page.screenshot({path:path.join(__dirname,spec.name+'-mobile-top.png')});
  const mobile=await page.evaluate(sel=>({width:innerWidth,documentWidth:document.documentElement.scrollWidth,brokenImages:[...document.querySelectorAll(sel+' img')].filter(x=>!x.complete||!x.naturalWidth).map(x=>x.getAttribute('src')),h1:document.querySelector('h1').innerText}),selector);
  if(mobile.documentWidth>391||mobile.brokenImages.length)throw Error(JSON.stringify(mobile));
  if(!spec.naver){await page.locator('.custom-data-table-wrap').first().scrollIntoViewIfNeeded();await page.screenshot({path:path.join(__dirname,spec.name+'-mobile-table.png')});}
  else {
   // Confirm the existing copy button selects the complete amended article. No real clipboard is written.
   await page.evaluate(()=>{document.execCommand=(cmd)=>{if(cmd!=='copy')throw Error('unexpected');window.__copyText=window.getSelection().toString();return true;};});
   page.on('dialog',d=>d.dismiss());
   await page.getByRole('button',{name:'📋 본문 전체 복사하기'}).first().click();
   const copied=await page.evaluate(()=>window.__copyText||'');
   if(!copied.includes('잠 안 올 때 눈만 감고')||!copied.includes('#꿀단지')||copied.includes('베타파'))throw Error('copy range mismatch');
   mobile.copy_selection_checked=true;
  }
  await page.setViewportSize({width:1366,height:900});await page.locator('h1').first().scrollIntoViewIfNeeded();await page.waitForTimeout(400);await page.screenshot({path:path.join(__dirname,spec.name+'-desktop.png')});
  report.push({name:spec.name,mobile,desktopWidth:await page.evaluate(()=>document.documentElement.scrollWidth)});await context.close();
 }
 await browser.close();fs.writeFileSync(path.join(__dirname,'render_report.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));
})().catch(e=>{console.error(e);process.exit(1)});

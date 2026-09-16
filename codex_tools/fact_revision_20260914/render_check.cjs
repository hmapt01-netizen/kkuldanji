const fs=require('fs'),path=require('path');
const {chromium}=require('C:/Users/lim/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=path.resolve(__dirname,'../..');
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 const report=[];
 const web=path.join(root,'kkuldanji_web');
 const specs=['slow-aging-rice-recipe','coffee-after-meal-golden-time','fasting-blood-sugar-prediabetes-guide','fruit-washing-liver-health'].map(slug=>({name:slug,file:path.join(web,'posts',slug+'.html'),base:web,url:'https://preview.invalid/posts/'+slug+'.html',naver:false}));
 for(const dir of fs.readdirSync(path.join(root,'꿀단지 네이버')).filter(x=>/^(01_|07_|11_)/.test(x))){
  const base=path.join(root,'꿀단지 네이버',dir);
  for(const name of fs.readdirSync(base).filter(x=>x.endsWith('.html'))){specs.push({name:dir+(name.includes('모바일')?'-mobile':''),file:path.join(base,name),base,url:'https://preview.invalid/'+encodeURIComponent(name),naver:true});}
 }
 for(const spec of specs){
  const context=await browser.newContext({viewport:{width:390,height:844}});
  // Offline rendering only: every request is fulfilled from the scoped local output or blocked.
  await context.route('**/*',async route=>{
   const u=new URL(route.request().url());
   if(u.hostname!=='preview.invalid')return route.abort();
   const file=path.resolve(spec.base,'.'+decodeURIComponent(u.pathname));
   if(!file.startsWith(path.resolve(spec.base)+path.sep)||!fs.existsSync(file)||!fs.statSync(file).isFile())return route.abort();
   const ext=path.extname(file);const types={'.html':'text/html; charset=utf-8','.css':'text/css','.js':'application/javascript','.jpg':'image/jpeg','.png':'image/png','.svg':'image/svg+xml'};
   await route.fulfill({body:fs.readFileSync(file),contentType:types[ext]||'application/octet-stream'});
  });
  const page=await context.newPage();await page.goto(spec.url,{waitUntil:'load'});
  const body=page.locator(spec.naver?'#naverContent, #article-body':'.article-body-content');
  const h=page.locator('h1').first();await h.scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(__dirname,spec.name+'-mobile-top.png')});
  if(!spec.naver){await page.locator('.custom-data-table-wrap').first().scrollIntoViewIfNeeded();await page.screenshot({path:path.join(__dirname,spec.name+'-mobile-table.png')});}
  await body.scrollIntoViewIfNeeded();
  const result=await page.evaluate(()=>({width:innerWidth,documentWidth:document.documentElement.scrollWidth,brokenImages:[...document.images].filter(x=>x.loading!=='lazy'&&(!x.complete||x.naturalWidth===0)).map(x=>x.getAttribute('src')),h1:document.querySelector('h1')?.innerText}));
  if(result.documentWidth>result.width+1)throw Error('horizontal overflow '+spec.name+' '+JSON.stringify(result));
  if(!spec.naver&&spec.name==='slow-aging-rice-recipe'){
   await page.setViewportSize({width:1366,height:900});await h.scrollIntoViewIfNeeded();await page.screenshot({path:path.join(__dirname,'rice-desktop.png')});
  }
  report.push({name:spec.name,...result});await context.close();
 }
 fs.writeFileSync(path.join(__dirname,'offline_render_report.json'),JSON.stringify(report,null,2));
 await browser.close();console.log(JSON.stringify(report,null,2));
})().catch(e=>{console.error(e);process.exit(1)});

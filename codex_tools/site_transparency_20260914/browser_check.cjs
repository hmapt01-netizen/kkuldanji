const fs=require('fs'),path=require('path'),assert=require('assert');
const {chromium}=require('C:/Users/lim/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const web=path.resolve(__dirname,'../../kkuldanji_web');
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 const context=await browser.newContext({viewport:{width:390,height:844}});
 let submissions=0;
 await context.route('**/*',async route=>{
  const u=new URL(route.request().url());
  if(u.hostname==='formsubmit.co'){
   submissions++;assert.equal(route.request().method(),'POST');
   return route.fulfill({status:200,contentType:'application/json',body:JSON.stringify({success:'true',message:'Offline test only'})});
  }
  if(u.hostname!=='preview.invalid')return route.abort();
  const file=path.resolve(web,'.'+decodeURIComponent(u.pathname));
  if(!file.startsWith(web+path.sep)||!fs.existsSync(file)||!fs.statSync(file).isFile())return route.abort();
  const ext=path.extname(file),types={'.html':'text/html; charset=utf-8','.css':'text/css','.js':'application/javascript','.png':'image/png','.jpg':'image/jpeg','.svg':'image/svg+xml'};
  return route.fulfill({body:fs.readFileSync(file),contentType:types[ext]||'application/octet-stream'});
 });
 const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
 const report={mode:'Offline rendering, FormSubmit intercepted; no real email sent',pages:[]};
 for(const file of ['privacy.html','contact.html']){
  await page.goto('https://preview.invalid/'+file,{waitUntil:'load'});
  await page.locator(file==='privacy.html'?'#external-services':'#contact-privacy-notice').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(__dirname,file.replace('.html','')+'-mobile.png')});
  const layout=await page.evaluate(()=>({viewport:innerWidth,width:document.documentElement.scrollWidth}));
  assert(layout.width<=layout.viewport+1);report.pages.push({file,...layout});
 }
 await page.locator('#user-name').fill('로컬 검증');
 await page.locator('#user-email').fill('local-test@example.org');
 await page.locator('#inquiry-type').selectOption('other');
 await page.locator('#user-message').fill('외부로 전송하지 않는 로컬 검사입니다.');
 await page.locator('.btn-submit').click();
 assert.equal(submissions,0);
 assert.equal(await page.locator('#contact-privacy-consent').evaluate(e=>e.validity.valueMissing),true);
 await page.locator('#contact-privacy-consent').check();
 await page.locator('.btn-submit').click();
 await page.locator('#success-alert').waitFor({state:'visible'});
 assert.equal(submissions,1);
 assert.equal(await page.locator('#contact-privacy-consent').isChecked(),false);
 assert.equal(await page.locator('#user-message').inputValue(),'');
 assert.deepEqual(errors,[]);
 report.consent={blockedUnchecked:true,mockedSubmissionSucceeded:true,resetAfterSuccess:true};
 fs.writeFileSync(path.join(__dirname,'browser_report.json'),JSON.stringify(report,null,2));
 console.log(JSON.stringify(report,null,2));await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});

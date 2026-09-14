import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import path from 'node:path';
const [cssFile,...targets]=process.argv.slice(2);
assert.ok(cssFile && targets.length, 'CSS and homepage targets required');
const css=fs.readFileSync(cssFile,'utf8').replace(/\/\*[\s\S]*?\*\//g,'');
const moreRule=css.match(/\.btn-load-more\s*\{([^}]+)\}/);
assert.ok(moreRule,'load-more CSS rule required');
assert.ok(!/display\s*:[^;]*!important/i.test(moreRule[1]), 'CSS must allow the exhausted button to be hidden');
function runTarget(file,homeCount){
 const posts=['식단 & 영양','라이프 웰니스','홈트레이닝'].flatMap((category,c)=>Array.from({length:c===2?homeCount:13},(_,i)=>({category,slug:`guard-${c}-${i}.html`,title:`검증용 ${category} ${i}`,desc:'검색 확인용 문서'})));
 const source=fs.readFileSync(file,'utf8');
 const grid=source.match(/<section\b[^>]*id=["']desktopCardsGrid["'][^>]*>/);
 assert.ok(grid && /grid-template-columns\s*:\s*repeat\(3,\s*1fr\)/.test(grid[0]),'desktop grid must retain three columns');
 const script=[...source.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)].map(m=>m[1]).find(s=>s.includes('let currentSelectedCategory'));
 assert.ok(script,'actual homepage script found');
 const makeNode=(post)=>({attrs:{'data-category':post.category},textContent:'',style:{setProperty(k,v,p){this[k]=v;this[k+'Priority']=p;}},classList:{add(){},remove(){}},getAttribute(k){return this.attrs[k]??null;},setAttribute(k,v){this.attrs[k]=v;},removeAttribute(k){delete this.attrs[k];},querySelector(s){if(s==='a')return {getAttribute:()=>`posts/${post.slug}`};if(s==='h3')return {textContent:post.title};if(s==='p')return {textContent:post.desc};return null;}});
 const pc=posts.map(makeNode),mob=posts.map(makeNode),elements={},listeners=[],storage=new Map();
 for(const id of ['btnPcLoadMore','btnMobileLoadMore','mobileLoadMoreWrapper','desktopSectionTitle','currentCategoryLabel'])elements[id]={style:{},classList:{add(){},remove(){}},textContent:''};
 const doc={body:{style:{}},getElementById:id=>elements[id]??null,querySelector:()=>null,querySelectorAll:s=>s==='#desktopCardsGrid .article-item'?pc:s==='#tistoryFeedContainer .tistory-feed-item'?mob:[],addEventListener:(type,fn)=>{if(type==='DOMContentLoaded')listeners.push(fn);}};
 const ctx=vm.createContext({document:doc,window:{location:{search:''},HONEYJAR_POSTS_REGISTRY:[]},localStorage:{getItem:k=>storage.get(k)??null},URLSearchParams,console:{error:(...v)=>{throw Error(v.join(' '));}}});
 vm.runInContext(script,ctx,{filename:file,timeout:1500});
 const exec=s=>vm.runInContext(s,ctx,{timeout:1500});
 const count=list=>list.filter(n=>n.style.display==='flex').length;
 const check=(expected,msg)=>assert.equal(count(pc),expected,`${file}: ${msg}`);
 listeners.forEach(fn=>fn());check(6,'home initial');exec('loadMorePcArticles()');check(12,'home load more');
 const rows=[];
 for(const category of ['식단 & 영양','라이프 웰니스','홈트레이닝','all']){
  const total=category==='all'?posts.length:posts.filter(p=>p.category===category).length;
  exec(`filterDesktopCategory(${JSON.stringify(category)},null)`);check(Math.min(6,total),category+' reset');
  for(let shown=6;shown<total;){exec('loadMorePcArticles()');shown+=6;check(Math.min(shown,total),category+' next page');}
  assert.equal(elements.btnPcLoadMore.style.display,'none',category+' exhausted button');
  exec(`filterDesktopCategory(${JSON.stringify(category)},null)`);check(Math.min(6,total),category+' repeated click reset');
  assert.equal(elements.btnPcLoadMore.style.display,total>6?'inline-block':'none');
  rows.push({category,total,initial:Math.min(6,total)});
 }
 exec("filterTistoryFeed('식단 & 영양','식단·영양')");assert.equal(count(mob),4);exec('loadMoreMobileArticles()');assert.equal(count(mob),8);
 exec("filterTistoryFeed('라이프 웰니스','라이프 웰니스')");assert.equal(count(mob),4);check(6,'mobile switch resets desktop');
 exec("filterDesktopCategory('식단 & 영양',null)");assert.equal(count(mob),4,'desktop switch resets mobile');
 ctx.window.location.search='?cat='+encodeURIComponent('식단');listeners.forEach(fn=>fn());check(6,'direct category URL');assert.equal(count(mob),4);
 storage.set('honeyjar_hidden_slugs',JSON.stringify([posts[0].slug]));exec("filterDesktopCategory('all',null)");check(6,'hidden post replaced');assert.equal(pc[0].style.display,'none');
 exec("filterArticlesBySearch('존재하지않는검색어XYZ')");check(0,'empty search');assert.equal(elements.btnPcLoadMore.style.display,'none');
 exec("filterArticlesBySearch('')");check(6,'clear search');
 return rows;
}
for(const file of targets){
 for(const count of [0,1,5,6,7,13])runTarget(file,count);
 console.log(`[PASS] ${path.basename(file)}: first 6, next 6, category reset, exhausted button, mobile, URL, hidden posts, search; 6 boundary fixtures`);
}

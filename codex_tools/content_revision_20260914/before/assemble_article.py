"""Assemble this approved article; preserve source drafts and shared scripts."""
import ast, contextlib, hashlib, html, io, json, re, shutil, sys
from pathlib import Path
from lxml import html as lh, etree

def fragment(text): return lh.fragment_fromstring(text)
def textof(node): return ''.join(node.itertext())
def inner(node): return (node.text or '')+''.join(lh.tostring(c,encoding='unicode') for c in node)
def byclass(node,name): return node.xpath('.//*[contains(concat(" ",normalize-space(@class)," "), " '+name+' ")]')

W = Path(__file__).resolve().parent
ROOT = W.parent
sys.path.insert(0, str(ROOT/'tools'))
import audit_duplicates, audit_naver_post

# Reuse this article's reviewed Markdown renderer without its top-level writes.
tree = ast.parse((W/'prepare_draft_preview.py').read_text(encoding='utf-8'))
nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in ('inline','render')]
nodes += [n for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id=='CSS' for t in n.targets)]
exec(compile(ast.Module(body=nodes, type_ignores=[]), '<existing-article-renderer>', 'exec'))

SLUG = 'chuseok-meat-delivery-thawing-safety'
PACKAGE = ROOT/'꿀단지 네이버'/'15_추석_고기택배_수령확인'
PACKAGE.mkdir(exist_ok=True)
(PACKAGE/'images').mkdir(exist_ok=True)
for p in (W/'images').glob('*.jpg'): shutil.copy2(p, PACKAGE/'images'/p.name)
icons = [('icon','favicon.ico',''), ('icon','favicon-192x192.png','192x192'),
         ('icon','favicon-32x32.png','32x32'), ('icon','favicon.svg',''), ('apple-touch-icon','apple-touch-icon.png','')]
for _,name,_ in icons:
    for dest in (PACKAGE, W): shutil.copy2(ROOT/'kkuldanji_web'/name, dest/name)
icon_html = ''.join(f'<link rel="{rel}" href="{name}"'+(f' sizes="{size}"' if size else '')+'>' for rel,name,size in icons)
plan=json.loads((W/'image_plan.json').read_text(encoding='utf-8'))
captions={r['slot']:r.get('google_caption',r['scene_ko']) for r in plan['storyboard']}
def picture(name, channel, prefix='images/'):
    src=prefix+name
    image=f'<img src="{src}" alt="{html.escape(captions[name])}" width="1280" height="720" loading="lazy" style="display:block;width:100%;height:auto;border-radius:12px;">'
    if channel=='naver': return '<div class="img-box" style="margin:32px 0;">'+image+'</div>'
    return '<figure class="post-img-wrap" style="margin:28px 0;text-align:center;">'+image+f'<figcaption style="font-size:0.83rem;color:#64748b;margin-top:8px;line-height:1.4;">{html.escape(captions[name])}</figcaption></figure>'

mdg=(W/'google_draft.md').read_text(encoding='utf-8')
gbody,grefs=mdg.split('<!-- REFERENCES -->')
gt=gbody.splitlines()[0][2:]
g=lh.fragment_fromstring(render(gbody,'google'),create_parent='div')
g.remove(g.find('h1'))
quote=g.find('blockquote');g.remove(quote)
quote.set('class','lead-quote-card')
quote.set('style','background:#f8fafc;border-left:4px solid #e2b441;padding:18px 20px;margin:0 0 28px;line-height:1.8;')
g.insert(0,quote)
heads=g.findall('h2')
for i,h in enumerate(heads,1): h.set('id',f'sec{i}')
toc='<nav class="toc-box" style="padding:20px;border:1px solid #e2e8f0;border-radius:12px;margin:30px 0;"><strong>목차</strong><ul style="list-style:none;padding-left:0;">'+''.join(f'<li style="margin-top:10px;"><a href="#sec{i}">{html.escape(textof(h))}</a></li>' for i,h in enumerate(heads,1))+'</ul></nav>'
heads[0].addprevious(fragment(toc))
for i,h in enumerate(heads[1:],1):
    h.addnext(fragment(picture(f'post{i:02}.jpg','google',f'../images/posts/{SLUG}/')))
for p in g.iter('p'): p.set('style','font-size:1.02rem;line-height:1.9;color:#334155;margin-bottom:22px;')
for c,label in zip(byclass(g,'info-section-card'),['밖에 둔 시간','받았을 때 온도','표시·포장']):
    badge=etree.Element('span',attrib={'class':'info-badge','style':'display:block;width:fit-content;background:#dbeafe;color:#1e40af;padding:3px 10px;border-radius:6px;margin-bottom:8px;font-weight:800;'})
    badge.text=label;badge.tail=c.text;c.text=None;c.insert(0,badge)
    c.set('style','background:#f8fafc;border:1px solid #e2e8f0;border-radius:14px;padding:22px 20px;margin:28px 0;line-height:1.8;')
for t in byclass(g,'custom-data-table-wrap'):
    t.set('style','overflow-x:auto;margin:28px 0;border:1px solid #e2e8f0;border-radius:10px;')
    t.find('table').set('class','custom-data-table');t.find('table').set('style','width:100%;border-collapse:collapse;min-width:560px;font-size:0.92rem;')
    for cell in t.xpath('.//th|.//td'):cell.set('style','padding:12px;border-bottom:1px solid #e2e8f0;text-align:left;line-height:1.7;')
faqs=json.loads((W/'google_faqs.json').read_text(encoding='utf-8'))
db=json.loads((ROOT/'data/posts_db.json').read_text(encoding='utf-8-sig'))
related=next(p for p in db if 'yogurt' in p['slug'])
refitems=[inline(x[2:]) for x in grefs.splitlines() if x.startswith('- ')]
data=dict(title=gt,shortTitle='추석 고기 택배 수령과 해동 후 보관',date='2026.09.14',category='식단 & 영양',
 author='에디터 혀니',readTime='7분',slug=SLUG+'.html',slugKey=SLUG,
 desc='추석 고기 택배를 늦게 발견했다면 밖에 둔 시간, 고기의 온도, 표시와 포장을 확인하세요. 녹은 아이스팩만으로 판단하면 안 되는 이유와 해동 후 재냉동 주의사항을 살펴봅니다.',
 thumb=f'images/posts/{SLUG}/thumb.jpg',featuredCaption='선물 보냉 상자와 밀봉 고기, 녹은 아이스팩',
 isLatest=True,isEditorPick=False,academicSource='식약처·FDA·FoodSafety.gov 공공 안내 기반',
 bodyHtml=inner(g),references=refitems,relatedSlug=related['slug'],
 faqs=[{'q':f['question'],'a':f['answer']} for f in faqs])
(W/'post_data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
faqhtml='<aside><h3>자주 묻는 질문</h3>'+''.join('<details><summary>'+inline(f['q'])+'</summary><p>'+inline(f['a'])+'</p></details>' for f in data['faqs'])+'</aside>'
gpreview='<h1>'+html.escape(gt)+'</h1>'+picture('thumb.jpg','google')+inner(g).replace(f'../images/posts/{SLUG}/','images/')+faqhtml+'<footer>'+render(grefs,'google')+'</footer>'

mdn=(W/'naver_draft.md').read_text(encoding='utf-8')
nbody,nrefs=mdn.split('<!-- REFERENCES -->')
nt=nbody.splitlines()[0][2:]
n=lh.fragment_fromstring(render(nbody,'naver'),create_parent='div')
n.find('h1').addnext(fragment(picture('thumb.jpg','naver')))
nh=n.findall('h2')
for h in nh:h.set('style','border-left:4px solid #64748b;padding-left:12px;display:table;margin:40px auto 24px;font-size:20px;line-height:1.5;')
for h,name in zip(nh,['post03.jpg','post02.jpg','post01.jpg']):h.addnext(fragment(picture(name,'naver')))
paras=list(n.iter('p'))
storage=next(p for p in paras if textof(p).startswith('문제가 없는 고기는'))
storage.addnext(fragment(picture('post04.jpg','naver')))
after=next(p for p in paras if textof(p).startswith('선물을 보내는 분이라면'))
after.addprevious(fragment(picture('post05.jpg','naver')))
stickers=['깜짝 놀란 표정 😲','갸우뚱한 표정 🤔','솔깃한 미소 표정 😊','깊은 생각 표정 🤔','궁금한 표정 ❓','슬픈 표정 😢','한숨 쉬는 표정 😮‍💨','최종 고민 표정 🤔']
for index,label in zip([2,5,11,17,23,29,36,len(paras)-1],stickers):
    box=etree.Element('div',attrib={'class':'sticker-box','data-editor-only':'true'})
    box.text='[스티커: '+label+']';paras[index].addnext(box)
for strong in n.iter('strong'):
    strong.tag='mark';strong.set('style','background:#fef08a;padding:2px 4px;font-weight:bold;')
underline=next(p for p in paras if textof(p).startswith('다시 차갑게 만들어도'))
u=etree.Element('u',attrib={'style':'text-underline-offset:4px;'})
u.text=underline.text;underline.text=None
for child in list(underline): u.append(child)
underline.append(u)
for p in paras:p.set('style','font-size:17px;line-height:1.95;margin:0 0 24px;text-align:center;word-break:keep-all;')
tags=(W/'naver_hashtags.txt').read_text(encoding='utf-8').strip()
nhtml=inner(n)+'<footer>'+render(nrefs,'naver')+'</footer><p class="hashtags">'+html.escape(tags)+'</p>'
toolbar='<div class="editor-tools"><button onclick="copyArticle()">본문 복사하기</button><button onclick="copyTags()">해시태그 복사하기</button><p>스티커 안내는 편집용입니다. 본문 복사에서는 제외됩니다. 사진은 images 폴더에서 순서대로 첨부하세요.</p><div id="hashtagText">'+html.escape(tags)+'</div></div>'
js='''<script>
function fallbackCopy(text){const t=document.createElement('textarea');t.value=text;document.body.append(t);t.select();const ok=document.execCommand('copy');t.remove();return ok;}
async function copyTags(){const t=document.getElementById('hashtagText').innerText;try{await navigator.clipboard.writeText(t);alert('해시태그를 복사했습니다.');}catch(e){alert(fallbackCopy(t)?'해시태그를 복사했습니다.':'텍스트를 직접 선택해 복사해주세요.');}}
async function copyArticle(){const node=document.getElementById('naverContent').cloneNode(true);node.querySelectorAll('[data-editor-only]').forEach(e=>e.remove());try{await navigator.clipboard.write([new ClipboardItem({'text/html':new Blob([node.innerHTML],{type:'text/html'}),'text/plain':new Blob([node.innerText||node.textContent],{type:'text/plain'})})]);alert('본문을 복사했습니다. 사진은 images 폴더에서 첨부해주세요.');}catch(e){const holder=document.createElement('div');holder.innerHTML=node.innerHTML;document.body.append(holder);const r=document.createRange();r.selectNodeContents(holder);const s=window.getSelection();s.removeAllRanges();s.addRange(r);const ok=document.execCommand('copy');s.removeAllRanges();holder.remove();alert(ok?'본문을 복사했습니다.':'본문을 직접 선택해 복사해주세요.');}}
</script>'''
extra='figure img{max-width:100%}figcaption{font-size:13px;color:#64748b}.editor-tools{background:#fff6d6;border:1px solid #e9ce75;padding:18px;border-radius:12px;margin-bottom:30px;font-size:13px;line-height:1.7}.editor-tools p{font-size:13px;margin:12px 0}button{background:#315743;color:white;border:0;border-radius:8px;padding:12px 18px;margin:4px;cursor:pointer}.sticker-box{border:1px dashed #ccd6ce;background:#f6f8f4;color:#68796e;font-size:13px;padding:12px;margin:26px 0}.hashtags{font-size:13px;color:#326a4d}.naver footer p{font-size:13px;text-align:left!important}'
def doc(title,channel,body):return '<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(title)+'</title>'+icon_html+'<style>'+CSS+extra+'</style></head><body class="'+channel+'"><main>'+body+'</main></body></html>'
(W/'google_final_preview.html').write_text(doc(gt,'google',gpreview),encoding='utf-8')
ndoc=doc(nt,'naver',toolbar+'<div><div id="naverContent">'+nhtml+'</div></div>'+js)
nfile=PACKAGE/(PACKAGE.name+'_네이버블로그용.html')
nfile.write_text(ndoc,encoding='utf-8')
(W/'naver_final_preview.html').write_text(ndoc,encoding='utf-8')
finalmd=nbody
for title,name in [(nt,'thumb.jpg')]+[(textof(h),name) for h,name in zip(nh,['post03.jpg','post02.jpg','post01.jpg'])]:
    prefix='# ' if title==nt else '## '
    finalmd=finalmd.replace(prefix+title,prefix+title+'\n\n!['+captions[name]+'](images/'+name+')',1)
for text,name in [('문제가 없는 고기는 표시대로 바로 보관하고,\n육즙이 다른 음식에 닿지 않게 분리해 주세요.','post04.jpg'),('선물을 보내는 분이라면 미리\n“언제 집에서 받을 수 있어요?”라고 물어보세요.','post05.jpg')]:
    finalmd=finalmd.replace(text,text+'\n\n!['+captions[name]+'](images/'+name+')',1)
(W/'naver_final.md').write_text(finalmd+'\n<!-- REFERENCES -->\n'+nrefs+'\n\n'+tags+'\n',encoding='utf-8')
report={'google_title':gt,'naver_title':nt,'naver_package':str(nfile),'google_preview':str(W/'google_final_preview.html'),
        'image_order_google':plan['channel_plan']['google_order'],'image_order_naver':plan['channel_plan']['naver_order'],
        'google_faqs':len(data['faqs']),'naver_visible_captions':0,'naver_related_link':'사용자 지시: 네이버는 그냥 넘어가 — 이번 글 연결 생략','pending':['브라우저 화면·복사 버튼 실제 작동 확인'],'published':False}
(W/'assembly_review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))

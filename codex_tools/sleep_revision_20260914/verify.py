from pathlib import Path
import sys,json,re,hashlib
from lxml import html
W=Path(__file__).resolve().parent;R=W.parent.parent
sys.path.insert(0,str(R/'codex_tools'))
from freshness_guard import validate
validate(W)
before=json.loads((W/'posts_db.before.json').read_text(encoding='utf-8-sig'))
after=json.loads((R/'data/posts_db.json').read_text(encoding='utf-8-sig'))
def txt(doc):return re.sub(r'\s+',' ',doc.text_content()).strip()
slugs={'sleep-lying-down-eyes-closed-20min-rule.html','sleep-hygiene-guide.html'}
changed=[b['slug'] for a,b in zip(before,after) if a!=b]
assert set(changed)==slugs,changed
out={'scope':'local files; not deployed','posts':[]}
for old,new in zip(before,after):
 if new['slug'] not in slugs:continue
 for k in ['date','slug','category','isEditorPick','isLatest','thumb']:
  assert old.get(k)==new.get(k),k
 doc=html.fromstring(new['bodyHtml']);rendered=html.fromstring((R/'kkuldanji_web/posts'/new['slug']).read_text(encoding='utf-8'))
 assert rendered.xpath('//h1')[0].text_content().strip()==new['title']
 assert len(new['faqs'])==3 and len(doc.xpath('//h2'))==5
 assert not doc.xpath('//h2[contains(.,"FAQ")]')
 assert 40<=len(new['title'])<=60
 assert len(doc.xpath('//table'))==1
 assert all(len(txt(e))<=25 for e in doc.xpath('//h2'))
 for el in doc.xpath('//img'):
  assert (R/'kkuldanji_web/posts'/el.get('src')).resolve().is_file()
 assert all('post02.jpg' not in el.get('src') for el in doc.xpath('//img')) if 'lying' in new['slug'] else True
 for phrase in ['독소 100% 세척','부분 작동 (약 20~30%)','Clinical Practice Guideline: Stimulus Control','Core Body Temperature Regulation','단 1%도','불면의 악순환은 반드시']:
  assert phrase not in json.dumps(new,ensure_ascii=False),phrase
 paragraphs=[txt(e) for e in doc.xpath('//p') if txt(e)]
 article=rendered.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," article-body-content ")]')[0]
 out['posts'].append(dict(slug=new['slug'],title=new['title'],title_chars=len(new['title']),body_chars=len(txt(doc)),article_with_faq_refs_chars=len(txt(article)),paragraphs=len(paragraphs),max_paragraph_chars=max(map(len,paragraphs)),body_images=len(doc.xpath('//img')),reference_links=len(new['academicRefs'])))
npath=next((R/'꿀단지 네이버').glob('13_*/*.html'));nd=html.fromstring(npath.read_text(encoding='utf-8'));nc=nd.get_element_by_id('naverContent');np=[txt(e) for e in nc.xpath('.//p') if not txt(e).startswith('#')]
assert len(nc.xpath('.//h2'))==3 and not nc.xpath('.//table') and not nc.xpath('.//a[starts-with(@href,"http")]')
assert len(nc.xpath('.//img'))==4
assert nd.get_element_by_id('hashtagText').text_content().strip()==nc.xpath('.//p')[-1].text_content().strip()
before_n=html.fromstring((W/'naver13.before.html').read_text(encoding='utf-8'))
assert nd.xpath('//script')[0].text==before_n.xpath('//script')[0].text,'copy JS changed'
gd=html.fromstring(next(p for p in after if 'sleep-lying' in p['slug'])['bodyHtml']);gp=[txt(e) for e in gd.xpath('//p')]
def grams(t):
 ws=t.split();return {' '.join(ws[i:i+4]) for i in range(len(ws)-3)}
ng=grams(' '.join(np));gg=grams(' '.join(gp));ratio=len(ng&gg)/len(ng)*100
same=set(re.split(r'(?<=[.!?])\s+', ' '.join(np)))&set(re.split(r'(?<=[.!?])\s+',' '.join(gp)))
same=[x for x in same if len(x)>=15]
assert not same,same
assert ratio<5,ratio
out['naver']=dict(path=str(npath),title_chars=len(txt(nc.xpath('.//h1')[0])),article_chars=len(txt(nc)),body_paragraph_chars=sum(map(len,np)),h2=3,images=4,body_4gram_overlap_pct=round(ratio,2),identical_sentences_over_15chars=same,copy_js_preserved=True)
out['unchanged_posts']=len(after)-len(slugs)
(W/'verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2))

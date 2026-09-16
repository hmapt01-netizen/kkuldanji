"""Check edited content, preserved fields, generated pages and existing manuscript checks."""
from pathlib import Path
import json,re,sys,hashlib,io,contextlib
from lxml import html
R=Path(__file__).resolve().parents[2];W=Path(__file__).resolve().parent
sys.path.insert(0,str(R));sys.path.insert(0,str(R/'codex_tools'))
from freshness_guard import validate
from tools.audit_naver_post import audit_naver
from tools.audit_duplicates import audit_cross_duplicates
validate(W)
before=json.loads((W/'before/posts_db.json').read_text(encoding='utf-8-sig'))
now=json.loads((R/'data/posts_db.json').read_text(encoding='utf-8-sig'))
old={p['slug']:p for p in before};new={p['slug']:p for p in now}
targets=['slow-aging-rice-recipe.html','coffee-after-meal-golden-time.html','fasting-blood-sugar-prediabetes-guide.html','fruit-washing-liver-health.html']
assert set(old)==set(new) and len(now)==28
anchor_changes={'sleep-lying-down-eyes-closed-20min-rule.html':('공복혈당 낮추는 야간 12시간 공복 ↗','공복혈당 검사와 생활 관리 확인 ↗'),'endoscopy-meal-coffee-timing.html':('식후 커피 영양 흡수 방해 기전 ↗','식후 커피와 철분 흡수 확인 ↗')}
for slug,a in old.items():
 b=new[slug]
 for k in ['slug','date','category','thumb','isEditorPick','isLatest','relatedSlug']:
  assert a.get(k)==b.get(k),(slug,k)
 if slug not in targets:
  expected=dict(a)
  if slug in anchor_changes:
   x,y=anchor_changes[slug];expected['bodyHtml']=expected['bodyHtml'].replace(x,y)
  assert b==expected,('unrelated content modified',slug)
known_phrases=['미지근하게 살짝만 데워','흡수율 90% 이상 정상 회복','혈당이 두 자리 수치인 80~90대로','식약처 공인 30초','기능 약 50% 저하','총 폴리페놀이 약 17%','최소 45분~1시간 시차','100% 되돌릴','70~80%가','조임 압력을 30%']
report={'google':[],'naver':[],'source_review':'원문 또는 기록에 명시한 공식 검색 결과 범위에서 사람이 대조. Python은 날짜·출처 연결·구조·잔존 문구만 검사하며 사실성을 보장하지 않음.','publication':'로컬 수정·빌드. Git push 및 실서버 배포 미실행.'}
for slug in targets:
 post=new[slug];body=html.fromstring(post['bodyHtml']);page=html.fromstring((R/'kkuldanji_web/posts'/slug).read_text(encoding='utf-8'))
 visible=' '.join(body.text_content().split());assert 40<=len(post['title'])<=60
 assert page.xpath('//h1')[0].text_content().strip()==post['title']
 compiled=page.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," article-body-content ")]')[0]
 compiled_text=' '.join(compiled.text_content().split())
 # The shared template appends FAQ and references inside article-body-content.
 assert compiled_text.startswith(visible),('compiled body mismatch',slug)
 ids=set(body.xpath('//@id'));assert all(a[1:] in ids for a in body.xpath('//a/@href') if a.startswith('#'))
 for src in body.xpath('//img/@src'):assert (R/'kkuldanji_web/posts'/src).resolve().is_file()
 assert body.xpath('//table') and body.xpath('//*[contains(@class,"info-section-card")]')
 assert len(post['references'])>=3 and len(post['faqs'])==3
 for phrase in known_phrases:assert phrase not in json.dumps(post,ensure_ascii=False),(slug,phrase)
 faqblocks=[json.loads(s.text) for s in page.xpath('//script[@type="application/ld+json"]') if s.text and 'FAQPage' in s.text]
 assert faqblocks and len(faqblocks[0]['mainEntity'])==3
 for actual,expected in zip(faqblocks[0]['mainEntity'],post['faqs']):
  assert actual['name']==expected['q']
  assert html.fromstring('<div>'+actual['acceptedAnswer']['text']+'</div>').text_content()==html.fromstring('<div>'+expected['a']+'</div>').text_content()
 assert 'post02.jpg' not in post['bodyHtml'] if slug.startswith('fasting-blood') else True
 report['google'].append(dict(slug=slug,title_chars=len(post['title']),body_chars=len(visible),paragraphs=len(body.xpath('//p')),max_paragraph_chars=max(len(p.text_content()) for p in body.xpath('//p')),images=len(body.xpath('//img')),sha256=hashlib.sha256((R/'kkuldanji_web/posts'/slug).read_bytes()).hexdigest()))
log=io.StringIO()
for prefix,slug in [('01_',targets[0]),('07_',targets[1]),('11_',targets[2])]:
 for f in (R/'꿀단지 네이버').glob(prefix+'*/*.html'):
  tree=html.fromstring(f.read_text(encoding='utf-8'));root=tree.xpath('//*[@id="naverContent" or @id="article-body"]')[0]
  text=' '.join(root.text_content().split())
  for phrase in known_phrases:assert phrase not in text,(f.name,phrase)
  from urllib.parse import unquote
  for src in root.xpath('.//img/@src'):assert (f.parent/unquote(src)).resolve().is_file(),(f.name,src)
  with contextlib.redirect_stdout(log):
   assert audit_naver(str(f)),f
   assert audit_cross_duplicates(str(f),str(R/'kkuldanji_web/posts'/slug)),f
  assert 'getElementById' in f.read_text(encoding='utf-8')
  report['naver'].append(dict(path=str(f.relative_to(R)),body_chars=len(text),images=len(root.xpath('.//img')),sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
(W/'manuscript_checks.log').write_text(log.getvalue(),encoding='utf-8')
(W/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))

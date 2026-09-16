"""Compare the current Google post to its immediate predecessor without changing either."""
from pathlib import Path
from lxml import html, etree
import copy, hashlib, json, re, statistics
ROOT=Path(__file__).resolve().parents[1]
W=Path(__file__).resolve().parent
DB=ROOT/'data/posts_db.json'
def norm(s):return re.sub(r'\s+',' ',s).strip()
def text(e):return norm(''.join(e.itertext()))
def hasclass(e,name):return name in e.get('class','').split()
BLOCKS={'p','div','section','h1','h2','h3','h4','li','ul','ol','table','tr','td','th','thead','tbody','blockquote','nav','br'}
def flow(e):
 parts=[e.text or '']
 for c in e:
  if not isinstance(c.tag,str):continue
  pad=' ' if c.tag in BLOCKS else ''
  parts.extend([pad,flow(c),pad,c.tail or ''])
 return ''.join(parts)
def clean(root):
 r=copy.deepcopy(root)
 for e in list(r.iterdescendants()):
  if e.getparent() is None:continue
  if e.tag in {'nav','figure','figcaption','blockquote','script','style'} or any(hasclass(e,c) for c in ['toc-box','post-img-wrap','lead-quote-card','quote-card']):e.drop_tree()
 return r

data=json.loads(DB.read_text(encoding='utf-8-sig'))
assert data[0]['slug']=='chuseok-meat-delivery-thawing-safety.html'
result={'source':str(DB),'source_sha256':hashlib.sha256(DB.read_bytes()).hexdigest(),'method':'본문 총합: 제목·목차·상단 인용문·사진 설명·FAQ·참고문헌 제외, H2·일반 문단·표·정보 카드 포함. HTML 블록 경계는 공백 한 칸, 연속 공백/개행은 한 칸으로 정규화. 문단 통계는 일반 p 태그만(카드·표 제외).','posts':[]}
for post in data[:2]:
 r=html.fragment_fromstring(post['bodyHtml'],create_parent='div');c=clean(r)
 paragraphs=[p for p in c.iter('p') if not any(a.tag=='table' or hasclass(a,'info-section-card') for a in p.iterancestors())]
 texts=[text(p) for p in paragraphs];lengths=list(map(len,texts));body=norm(flow(c))
 section='도입';sections=[]
 for el in c:
  if el.tag=='h2':section=text(el);sections.append({'heading':section,'paragraphs':0,'paragraph_chars':0,'body_chars':0})
  if not sections:sections.append({'heading':'도입','paragraphs':0,'paragraph_chars':0,'body_chars':0})
  if el.tag=='p':sections[-1]['paragraphs']+=1;sections[-1]['paragraph_chars']+=len(text(el))
  sections[-1]['body_chars']+=len(norm(flow(el)))
 # Old lead quote is a styled div without a predictable class; identify separately below if necessary.
 row={'title':post['title'],'date':post['date'],'slug':post['slug'],'readTime_label':post.get('readTime'),'body_chars':len(body),'body_chars_no_spaces':len(re.sub(r'\s','',body)),
 'paragraphs':len(texts),'paragraph_chars_sum':sum(lengths),'paragraph_avg':round(statistics.mean(lengths),1),'paragraph_median':statistics.median(lengths),'paragraph_min':min(lengths),'paragraph_max':max(lengths),
 'paragraph_distribution':{'1-40':sum(n<=40 for n in lengths),'41-60':sum(41<=n<=60 for n in lengths),'61-80':sum(61<=n<=80 for n in lengths),'81-100':sum(81<=n<=100 for n in lengths),'101+':sum(n>100 for n in lengths)},
 'h2':[text(e) for e in c.iter('h2')],'tables':len(c.xpath('.//table')),'cards':sum(hasclass(e,'info-section-card') for e in c.iter()),'body_images':len(r.xpath('.//img')),'faqs':len(post.get('faqs',[])),'faq_chars':sum(len(norm(f['q']+' '+f['a'])) for f in post.get('faqs',[])),
 'references':len(post.get('references',[])),'reference_links':len(re.findall(r'href=',str(post.get('references',[])))),'body_internal_links':len([e for e in c.xpath('.//a[@href]') if not e.get('href').startswith(('http','#'))]),'sections':sections,
 'paragraph_texts':[{'n':i+1,'chars':len(t),'text':t} for i,t in enumerate(texts)],'body_text':body}
 result['posts'].append(row)
(W/'google_previous_comparison.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
for row in result['posts']:
 print(json.dumps({k:v for k,v in row.items() if k not in ['paragraph_texts','body_text']},ensure_ascii=False,indent=2))
 print('LONGEST',sorted(row['paragraph_texts'],key=lambda p:p['chars'],reverse=True)[:2])

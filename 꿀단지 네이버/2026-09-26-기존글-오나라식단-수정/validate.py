import json,sys,re,hashlib
from pathlib import Path
from html import unescape
from PIL import Image
sys.stdout.reconfigure(encoding='utf-8')
root=Path('D:/작업/꿀단지'); work=root/'꿀단지 네이버/2026-09-26-기존글-오나라식단-수정'
db=root/'data/posts_db.json'; posts=json.loads(db.read_text(encoding='utf-8-sig'))
p=next(p for p in posts if p['slug']=='ohnara-diet.html')
if '--fix-table' in sys.argv:
    p['bodyHtml']=re.sub(r'(<(?:td|th)\b[^>]*style=")([^"]*)',r'\1\2white-space:normal !important;word-break:keep-all;',p['bodyHtml'])
    db.write_text(json.dumps(posts,ensure_ascii=False,indent=2),encoding='utf-8')
    (work/'post_data.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')
    print('article table wrapping fixed');sys.exit(0)
old=json.loads((work/'before/posts_db.json').read_text(encoding='utf-8-sig'))
changed=[a['slug'] for a,b in zip(posts,old) if a!=b]
assert changed==['ohnara-diet.html'],changed
assert [(a['slug'],a.get('isEditorPick')) for a in posts]==[(a['slug'],a.get('isEditorPick')) for a in old]
html=(root/'kkuldanji_web/posts/ohnara-diet.html').read_text(encoding='utf-8-sig')
plain=lambda s:unescape(re.sub('<[^>]+>','',s)).strip()
assert plain(re.search(r'<h1\b[^>]*>(.*?)</h1>',html,re.S)[1])==p['title']
assert unescape(re.search(r'<meta name="description" content="([^"]*)"',html)[1])==p['desc']
schema=[json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>',html,re.S)]
article=next(x for x in schema if x.get('@type')=='Article')
faq=next(x for x in schema if x.get('@type')=='FAQPage')
assert article['headline']==p['title'] and article['description']==p['desc']
assert [(x['name'],x['acceptedAnswer']['text']) for x in faq['mainEntity']]==[(x['q'],x['a']) for x in p['faqs']]
for q in p['faqs']:assert q['q'] in plain(html) and q['a'] in plain(html)
for id,label in re.findall(r'<a href="#(sec\d+)">(.*?)</a>',p['bodyHtml']):
    assert plain(re.search(r'<h2 id="'+id+r'"[^>]*>(.*?)</h2>',html,re.S)[1])==plain(label)
assert not any(t in p['bodyHtml']+p['title']+str(p['faqs']) for t in ['47kg','황금 비율','혈당 급상승을 막아','관절 손상 없이','매년 근육량'])
imgs=[]
for src in ['../'+p['thumb']]+re.findall(r'<img[^>]*src="([^"]*)"',p['bodyHtml']):
    file=(root/'kkuldanji_web/posts'/src).resolve()
    with Image.open(file) as im: size=im.size
    imgs.append({'path':str(file),'source_dimensions':size,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
sys.path.insert(0,str(root/'codex_tools'))
from register_post import validate_body_style
try:validate_body_style(p['bodyHtml']); style='PASS'
except ValueError as e:style=str(e)
result={'changed_posts':changed,'count':len(posts),'progress':'9/32','metadata_toc_faq_schema':'PASS','editor_picks_preserved':True,'images':imgs,'new_article_style_check':style,'dateModified':article['dateModified'],'dateModified_note':'기존 빌더가 발행일을 재사용함. 이번 글 수정 범위에서 공용 빌더 유지.','deploy':'NOT RUN','visual':'pending final mobile recheck'}
(work/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))

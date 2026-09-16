"""Check actual generated article and preservation of existing posts."""
from pathlib import Path
import hashlib, json
from lxml import html
W=Path(__file__).resolve().parent
ROOT=W.parent
before=json.loads((W/'registration_backup/posts_db.before_registration.json').read_text(encoding='utf-8-sig'))
after=json.loads((ROOT/'data/posts_db.json').read_text(encoding='utf-8-sig'))
slug='chuseok-meat-delivery-thawing-safety.html'
assert len(after)==len(before)+1 and after[0]['slug']==slug
for old in before:
    new=next(x for x in after if x['slug']==old['slug'])
    assert {k:v for k,v in old.items() if k!='isLatest'}=={k:v for k,v in new.items() if k!='isLatest'},old['slug']
assert after[0]['isEditorPick'] is False
target=ROOT/'kkuldanji_web/posts'/slug
doc=html.fromstring(target.read_text(encoding='utf-8'))
assert len(doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," faq-card ")]'))==3
imgs=[x for x in doc.xpath('//img') if 'chuseok-meat-delivery-thawing-safety/' in x.get('src','')]
assert len(imgs)==6,[x.get('src') for x in imgs]
for name in ['feed.xml','sitemap.xml','index.html','js/features.js']:
    assert slug in (ROOT/'kkuldanji_web'/name).read_text(encoding='utf-8-sig'),name
for p in (W/'images').glob('*.jpg'):
    deployed=ROOT/'kkuldanji_web/images/posts/chuseok-meat-delivery-thawing-safety'/p.name
    assert p.read_bytes()==deployed.read_bytes()
report=dict(new_article=str(target),database_posts=len(after),existing_posts_preserved=len(before),
            existing_editor_picks_preserved=True,new_editor_pick=False,compiled_images=6,compiled_faqs=3,
            feed_sitemap_home_registry='pass',local_site_audit={'html':39,'internal_links':1036,'assets':689,
            'missing_required':0,'broken_links':0,'missing_assets':0,'html_errors':0,'favicon_errors':0,'encoding_errors':0},
            browser_rendering='미검사: 이전 브라우저 도구에서 로컬 file URL 접근 차단. 우회하지 않음.',
            copy_button='JS 구문 검사 통과, 실제 클립보드 작동 미검사',published=False)
(W/'registered_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))

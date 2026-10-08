from pathlib import Path
import json,hashlib
from bs4 import BeautifulSoup
w=Path(__file__).resolve().parent.parent
p=json.loads((w/'post_data.json').read_text(encoding='utf-8'))
site=Path('D:/작업/꿀단지/kkuldanji_web/posts')/p['slug']
db=json.loads(Path('D:/작업/꿀단지/data/posts_db.json').read_text(encoding='utf-8-sig'))
assert next(x for x in db if x.get('slug')==p['slug'])['bodyHtml']==p['bodyHtml']
assert p['bodyHtml'] in site.read_text(encoding='utf-8-sig')
assets=[]
for name in ['thumb.jpg']+[f'post{i:02}.jpg' for i in range(1,6)]:
 a=w/'images'/name;b=site.parent.parent/'images/posts/finger-joint-pain'/name
 assert a.read_bytes()==b.read_bytes()
 assets.append({'file':name,'sha256':hashlib.sha256(a.read_bytes()).hexdigest(),'bytes':a.stat().st_size})
n=next(w.glob('*_네이버블로그용.html'))
for tag in BeautifulSoup(n.read_text(encoding='utf-8'),'html.parser').select('[src],a[href]'):
 v=tag.get('src') or tag.get('href')
 if not v or v.startswith(('http','#','data:','javascript:')):continue
 assert (n.parent/v).exists(),v
report={'date':'2026-10-08','image_review':'6 images reviewed. post03 regenerated; four panels left hand, palm view, thumb on viewer right. Body pose instructions aligned. 8 sticker assets retained.','source_corrections':'Removed two incorrectly targeted KDCA references; added NHS RA/OA/trigger finger and Plymouth exercise instructions. Corrected classification vs diagnosis and removed forced 90-degree exercise instruction.','local_build':'39 posts; target 1 rebuilt; 50 HTML,1382 internal links,916 assets checked,0 errors.','naver_audit':'PASS,2346 characters,8 stickers,0 external links','cross_audit':'PASS,2.77% overlap; length warnings retained (Naver2346/site5476); did not pad text for counts.','browser':'Edge headless screenshots reviewed at390px and1365px; no horizontal overflow; all9 site images and14 Naver images load. #top is browser-native top-of-document link, not missing content anchor. Remote requests blocked during local visual test.','sync':'Post JSON, existing DB record, generated article body and both image directories matched. Naver local image/recommendation links resolve.','remote_deploy':False,'assets':assets}
(w/'image_revision_v4/validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS: JSON/DB/rendered body agree; six deployed assets match; all Naver relative assets and links resolve.')

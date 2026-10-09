from pathlib import Path
import json
from bs4 import BeautifulSoup
w=Path(__file__).resolve().parent.parent
p=json.loads((w/'post_data.json').read_text(encoding='utf-8-sig'))
n=BeautifulSoup(next(w.glob('*_네이버블로그용.html')).read_text(encoding='utf-8-sig'),'html.parser')
print('NAVER',n.get_text(' ',strip=True))
print('LINKS',[(a.get_text(),a.get('href')) for a in n.select('a[href]')])
root=Path('D:/작업/꿀단지');d=next(x for x in json.loads((root/'data/posts_db.json').read_text(encoding='utf-8-sig')) if x.get('slug')==p['slug'])
h=(root/'kkuldanji_web/posts'/p['slug']).read_text(encoding='utf-8-sig')
print('DBMATCH',d['bodyHtml']==p['bodyHtml'],'SITEMATCH',p['bodyHtml'] in h)
print('DBFAQ',d.get('faqs'));print('SITE_OLD_REFS',any(x in h for x in ['samsunghospital','cntnts_sn=5273']))
for f in ['thumb.jpg']+[f'post{i:02}.jpg' for i in range(1,6)]:
 print('IMG',f,(w/'images'/f).read_bytes()==(root/'kkuldanji_web/images/posts'/p['slugKey']/f).read_bytes())

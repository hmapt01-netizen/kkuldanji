from pathlib import Path
from lxml import html,etree
import json,copy
R=Path(__file__).resolve().parents[2];W=Path(__file__).resolve().parent
rice=next((R/'꿀단지 네이버').glob('01_*/*네이버블로그용.html'))
s=rice.read_text(encoding='utf-8')
s=s.replace('Effect of cooling of cooked white rice on resistant starch content and glycemic response','조리한 백미의 냉각이 저항성 전분 함량과 혈당 반응에 미치는 영향 (제목 번역)')
s=s.replace('New low-calorie rice could help cut rising obesity rates','저열량 쌀 조리법과 비만에 관한 학회 발표 소개 (자료 제목 요약)')
rice.write_text(s,encoding='utf-8')
coffee=next((R/'꿀단지 네이버').glob('07_*/*네이버블로그용.html'))
mobile=next(coffee.parent.glob('*모바일스토리형.html'))
b=W/'before'/mobile.relative_to(R);b.parent.mkdir(parents=True,exist_ok=True)
if not b.exists():b.write_bytes(mobile.read_bytes())
t=html.fromstring(mobile.read_text(encoding='utf-8-sig'));src=html.fromstring(coffee.read_text(encoding='utf-8'))
target=t.get_element_by_id('article-body');new=src.get_element_by_id('article-body')
for e in list(target):target.remove(e)
target.text=new.text
for e in new:target.append(copy.deepcopy(e))
t.xpath('//title')[0].text=src.xpath('//title')[0].text
mobile.write_text('<!DOCTYPE html>\n'+etree.tostring(t,encoding='unicode',method='html'),encoding='utf-8')
db=R/'data/posts_db.json';posts=json.loads(db.read_text(encoding='utf-8-sig'))
anchors={
 'sleep-lying-down-eyes-closed-20min-rule.html':('공복혈당 낮추는 야간 12시간 공복 ↗','공복혈당 검사와 생활 관리 확인 ↗'),
 'endoscopy-meal-coffee-timing.html':('식후 커피 영양 흡수 방해 기전 ↗','식후 커피와 철분 흡수 확인 ↗')}
for post in posts:
 if post['slug'] in anchors:
  a,z=anchors[post['slug']];post['bodyHtml']=post['bodyHtml'].replace(a,z)
db.write_text(json.dumps(posts,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Mobile coffee manuscript and two inbound link labels synchronized.')

import json,sys
from pathlib import Path
from html import escape
sys.stdout.reconfigure(encoding='utf-8')
r=Path(r'D:\작업\꿀단지');w=Path(__file__).parent
sys.path.insert(0,str(r/'codex_tools'))
from source_access_guard import transition
refs=[
('농촌진흥청 그린매거진 — 여름과일 고르기와 보관', 'https://rda.go.kr/webzine/2022/08/sub1-6.html'),
('농촌진흥청 농사로 — 옥수수 구입·손질·보관', 'https://www.nongsaro.go.kr/portal/ps/psr/psrb/monthFdmtDtl.ps?cntntsNo=211729&menuId='),
('질병관리청·정책브리핑 — 여름철 비브리오패혈증 예방', 'https://www.korea.kr/news/policyNewsView.do?newsId=148930876'),
('미국 FDA — 신선 농산물의 안전한 세척·보관', 'https://www.fda.gov/food/buy-store-serve-safe-food/selecting-and-serving-produce-safely'),
('펜실베이니아주립대 농업지도부 — 복숭아 숙도별 보관', 'https://extension.psu.edu/peach-season-in-pennsylvania'),
('독일 연방위해평가원 BfR — 감자 글리코알칼로이드 안전 안내', 'https://www.bfr.bund.de/en/service/frequently-asked-questions/topic/frequently-asked-questions-about-solanine-glycoalkaloids-in-potatoes/')]
notes='''# 근거와 편집 판단 — 2026-09-26
- RDA: 포도 과분은 천연 왁스. 농약 여부의 판별 근거로 사용하지 않음. 포도 개별 포장 냉장. 여름 과일의 품종·산지별 차이를 감안하고 모든 재료가 8월 영양 절정이라는 표현 삭제.
- 농사로: 옥수수 알이 촘촘하고 탄력 있는 것 선택. 시간이 지나면 당분이 전분으로 변함. 찐 뒤 식혀 소분 냉동.
- 질병관리청 정책브리핑: 어패류 저온 보관·85도 이상 가열, 흐르는 물 세척, 도구 소독, 고위험군 생식 회피. 기존 KDCA 주소는 웹 열기 404여서 정책브리핑의 질병관리청 자료로 교체.
- FDA: 흐르는 물로 과일 씻기. 비누·세제 불필요. 자른 과일 냉장, 날해산물과 분리. 세척으로 모든 균 제거 보장하지 않음.
- Penn State Extension: 검색에서 원문 본문 확인(직접 열기 실패). 덜 익은 복숭아 실온 후숙, 익으면 냉장. 미국 수확시기를 국내 제철 근거로 사용하지 않음.
- BfR FAQ: 감자 서늘·건조·어두운 곳 보관. 녹색/강하게 싹남/쭈그러진 감자 식용 부적합. 작은 눈 깊이 제거 지침은 있으나 기존 글의 무조건 안전 보장 삭제. 쓴맛 감자 먹지 않음.
- 식탁 예시, 구매량·소스 선택은 편집자가 구성한 실용 예시로 표시. 임상 효능·특정 음식 궁합·정량 영양 수치 새 주장 없음.
- 흐름: 장보기 계획 → 전복 → 장어 → 과일 → 옥수수·감자 → 식탁 예시. 사진 4장 유지, 장어는 사진과 일치하는 양념구이로 표기.
\n'''+ '\n'.join(f'- [{t}]({u})' for t,u in refs)
(w/'source_notes.md').write_text(notes,encoding='utf-8')
transition(w,'writing','공식 자료 확인 완료. 사용자의 문맥·흐름 교정 요청을 반영하여 기존 글 재구성')
db=r/'data/posts_db.json';data=json.loads(db.read_text(encoding='utf-8-sig'))
p=next(x for x in data if x['slug']=='august-seasonal-foods.html')
def para(t):return '<p style="font-size:1.02rem;line-height:1.9;color:#334155;margin-bottom:22px;">'+t+'</p>'
def photo(name,caption):return f'<figure class="post-img-wrap post-photo-figure"><img src="../images/posts/august/{name}.jpg" alt="{caption}" loading="lazy" decoding="async"><figcaption>{caption}</figcaption></figure>'
def cite(n):
 t,u=refs[n-1];return f'<a href="{escape(u,quote=True)}" target="_blank" rel="noopener noreferrer">{t}</a>'
heads=['장보기 전에 먹을 날짜부터 정하기','전복은 보관과 충분한 가열부터','장어는 제품 상태와 양념 확인하기','복숭아와 포도는 익은 정도에 맞춰 보관하기','옥수수는 소분하고 감자는 상태 살피기','장본 재료를 한 끼와 간식으로 나누기']
parts=['<div class="lead-quote-card" style="background:#fff9ef;border-left:4px solid #d6a24a;padding:24px;border-radius:12px;margin-bottom:28px;"><strong>8월 장보기는 먹을 날짜와 보관할 자리부터 생각해 보세요.</strong>'+para('복숭아·포도·옥수수 같은 여름 먹거리와 전복·장어·감자를 식탁에 활용하는 방법을 정리했습니다. 구입할 때 확인할 점부터 집에서 손질하고 보관하는 순서까지 살펴봅니다.')+'</div>',
para('복숭아 한 상자와 옥수수 한 봉지를 사 왔는데, 어디부터 정리해야 할지 막막할 때가 있습니다. 여름에는 맛있어 보이는 재료를 고르는 것만큼 먹기 전까지 상태를 유지하는 일도 중요합니다. 먼저 먹을 음식과 나누어 보관할 음식을 구분하면 장본 뒤의 일이 한결 간단해집니다.'),
para('수확과 출하 시기는 품종·지역·재배 방식에 따라 달라집니다. 여기서는 여름 과일과 옥수수를 중심으로, 함께 차리기 좋은 수산물과 감자까지 살펴봅니다. 매장에서는 산지와 포장 상태, 보관 안내도 함께 확인하세요.'),
'<nav class="toc-box"><div class="toc-title"><strong>목차</strong></div><ul>'+''.join(f'<li><a href="#section{i}">{h}</a></li>' for i,h in enumerate(heads,1))+'</ul></nav>']
def section(i):parts.append(f'<h2 id="section{i}">{heads[i-1]}</h2>')
section(1)
parts += [para('장을 보기 전에 오늘 조리할 주재료 하나와 며칠 안에 먹을 과일을 정해 보세요. 전복과 장어를 모두 살 필요는 없습니다. 식사 인원과 조리 시간을 기준으로 하나를 고르고, 옥수수는 바로 먹을 양과 냉동할 양을 나누어 생각하면 됩니다.'),
'<div class="table-wrap"><table><thead><tr><th>재료</th><th>살 때 확인할 점</th><th>집에 오면 먼저 할 일</th></tr></thead><tbody><tr><td>전복·장어</td><td>냉장·냉동 상태, 포장과 표시사항</td><td>제품 안내에 맞춰 바로 보관하고 조리 순서 정하기</td></tr><tr><td>복숭아</td><td>상처와 무름, 익은 정도</td><td>덜 익은 것과 익은 것 구분하기</td></tr><tr><td>포도</td><td>터지거나 짓무른 알이 있는지</td><td>송이별로 포장해 냉장하기</td></tr><tr><td>옥수수</td><td>알이 촘촘하고 탄력이 있는지</td><td>먹을 양을 찌고 나머지는 소분 냉동 준비하기</td></tr><tr><td>감자</td><td>녹색 변색, 심한 싹, 쭈그러짐</td><td>서늘하고 어둡고 건조한 곳에 두기</td></tr></tbody></table></div>',
para('이제 재료별로 구입 후의 순서를 살펴보겠습니다. 먼저 저온 보관이 필요한 수산물부터 정리하고, 과일과 나머지 재료를 차례로 챙기면 됩니다.')]
section(2)
parts += [photo('abalone','껍데기에 담아 마늘을 곁들인 전복구이'),
para('전복을 샀다면 상온에 꺼내 두기보다 보관 안내에 맞춰 먼저 냉장·냉동하세요. 질병관리청은 비브리오패혈증 예방을 위해 어패류를 5℃ 이하로 보관하고 85℃ 이상에서 충분히 익혀 먹도록 안내합니다. 특히 간 질환·당뇨병 등 기저질환이 있는 사람은 날것 섭취를 피해야 합니다.'),
para('손질할 때는 장갑을 끼고 흐르는 수돗물로 씻으며, 사용한 칼과 도마는 세척·소독합니다. 과일처럼 그대로 먹을 음식은 날해산물과 따로 다루세요. '+cite(3)),
para('손질한 전복은 죽이나 구이처럼 충분히 가열하는 메뉴에 활용할 수 있습니다. 사진처럼 마늘을 곁들여 굽거나, 잘게 썰어 쌀·채소와 함께 죽으로 끓여 보세요. 처음 조리한다면 손질된 제품의 조리 안내를 따라가는 편이 수월합니다.')]
section(3)
parts += [photo('eel','양념을 발라 구운 장어에 생강채를 곁들인 접시'),
para('장어도 구입한 형태에 따라 준비 과정이 달라집니다. 생물·손질 제품인지, 초벌했거나 완전히 조리된 제품인지 먼저 확인하세요. 초벌 제품은 그대로 먹는 것으로 생각하지 말고 포장에 적힌 추가 가열 방법을 따릅니다. 냉장·냉동 보관과 해동 방법 역시 제품 표시를 기준으로 합니다.'),
para('양념이 따로 들어 있는 제품이라면 처음부터 전부 붓지 않고 먹을 때 조금씩 더해 보세요. 이미 양념된 제품은 영양정보가 표시되어 있을 경우 같은 중량 기준으로 나트륨과 당류를 비교할 수 있습니다. 사진은 소금구이가 아닌 양념구이 예시입니다.'),
para('장어를 한 끼의 주재료로 정했다면 밥과 채소 반찬을 곁들여 메뉴를 구성해 보세요. 아래 식탁 예시처럼 다른 재료와 나누어 쓰면 여러 보양식을 한 번에 준비하는 부담을 덜 수 있습니다.')]
section(4)
parts += [photo('fruit','바구니에 담긴 복숭아와 포도'),
para('복숭아는 멍이 들거나 짓무른 것을 피하고, 먹을 날에 맞춰 익은 정도를 고릅니다. 덜 익은 복숭아는 실온에서 상태를 확인하며 후숙하고, 먹기 좋게 익은 뒤에는 냉장해 오래 두지 않고 먹는 방식이 좋습니다. 이미 무른 과일을 더운 곳에 계속 두지 마세요. '+cite(5)),
para('포도는 터지거나 곰팡이가 핀 알이 없는지 살핍니다. 표면의 흰 가루는 자연적으로 생기는 과분일 수 있지만, 그것만으로 농약 사용 여부를 판단할 수는 없습니다. 농촌진흥청은 포도를 종이 봉지에 싼 채 송이별로 비닐봉지에 넣어 냉장 보관하도록 안내합니다. '+cite(1)),
para('먹기 전에는 과일을 흐르는 물에 씻으세요. 껍질을 벗길 과일도 자르기 전에 씻고, 비누나 세제는 사용하지 않습니다. 잘라 둔 과일은 냉장하며, 상한 과일은 먹지 않습니다. '+cite(4)),
para('한 번에 큰 상자를 사기보다 먹을 수 있는 양을 고르면 보관이 쉬워집니다. 과일을 정리한 뒤에는 옥수수와 감자를 서로 다른 방식으로 보관해 주세요.')]
section(5)
parts += [photo('vege','찐 옥수수와 감자를 함께 담은 모습'),
para('옥수수는 알이 촘촘하고 탄력 있으며 겉껍질이 지나치게 마르지 않은 것을 고릅니다. 수확 후 시간이 지나면 당분이 전분으로 바뀌므로, 오래 둘 분량은 찐 뒤 식혀 한 번 먹을 양씩 냉동하세요. 나중에 다시 찌거나 알을 떼어 밥에 넣어 활용할 수 있습니다. '+cite(2)),
para('감자는 녹색으로 변했거나 싹이 많이 나고 쭈그러진 것을 피합니다. 집에서는 서늘하고 어둡고 건조한 곳에 보관하세요. 감자의 녹색 부위와 싹에는 솔라닌 등 글리코알칼로이드가 많을 수 있습니다.'),
para('독일 연방위해평가원은 녹색이거나 싹이 심하게 난 감자는 먹지 않도록 권고합니다. 상태가 나쁜 감자를 삶기만 하면 괜찮아진다고 생각하지 마세요. 감자 요리에서 쓴맛이 느껴지면 먹기를 멈춥니다. '+cite(6)),
para('보관 준비를 마쳤다면, 바로 먹을 옥수수와 감자를 식사나 간식 중 어디에 쓸지 정해 보세요. 밥과 함께 먹을 때는 곁들이는 양까지 보고 한 끼 분량을 조절하면 됩니다.')]
section(6)
parts += [para('다음은 장본 재료를 활용하는 메뉴 예시입니다. 여섯 재료를 모두 한 상에 올리기보다, 주재료 하나를 정하고 나머지를 식사나 간식으로 나누어 보세요.'),
'<ul><li><strong>전복을 산 날:</strong> 충분히 익힌 전복채소죽에 평소 먹는 반찬을 곁들입니다.</li><li><strong>장어를 산 날:</strong> 장어구이에 밥과 채소를 차리고, 추가 양념은 따로 냅니다.</li><li><strong>간식을 준비할 때:</strong> 먹기 전에 씻은 복숭아·포도 또는 찐 옥수수 중에서 골라 덜어 먹습니다.</li><li><strong>감자를 쓸 때:</strong> 상태를 확인한 감자를 삶거나 채소국에 넣어 다음 식사에 활용합니다.</li></ul>',
para('장보기 메모에는 재료 이름 옆에 “오늘 조리”, “익으면 냉장”, “쪄서 소분”처럼 다음 행동을 적어 보세요. 냉장고에 무엇이 남아 있는지 확인하고 다음 구입량을 조절하면, 여름 먹거리를 무르거나 시들기 전에 활용하기가 쉬워집니다.')]
p.update(title='8월 제철 음식 장보기, 전복·장어부터 과일까지 고르는 법과 안전한 보관 요령',shortTitle='8월 제철 음식, 고르는 법과 보관 요령',desc='복숭아·포도·옥수수와 전복·장어·감자를 여름 식탁에 활용하는 방법. 장보기 계획부터 숙도별 과일 보관, 수산물 가열, 옥수수 냉동과 감자 상태 확인까지 정리했습니다.',featuredCaption='여름 식탁에 활용할 수산물과 과일, 옥수수·감자',academicSource='농촌진흥청·질병관리청 등의 식품 보관·안전 자료 참고',bodyHtml='\n\n'.join(parts),referencesTitle='식재료 보관·안전 참고 자료',references=[f'<a href="{escape(u,quote=True)}" target="_blank" rel="noopener noreferrer">{t}</a>' for t,u in refs],faqs=[
{'q':'복숭아는 냉장고에 넣으면 안 되나요?','a':'덜 익은 복숭아는 실온에서 상태를 확인하며 후숙하고, 먹기 좋게 익은 뒤에는 냉장해 오래 두지 않고 먹습니다. 익은 과일까지 더운 실온에 계속 둘 필요는 없습니다.'},
{'q':'복숭아와 포도를 씻을 때 세제가 필요한가요?','a':'과일은 먹기 전에 흐르는 물로 씻으며, 비누나 세제는 사용하지 않습니다. 껍질을 벗길 과일도 자르기 전에 씻고, 잘라 둔 과일은 냉장합니다.'},
{'q':'녹색으로 변하거나 싹이 많이 난 감자는 삶으면 괜찮나요?','a':'삶는 것만으로 안전해진다고 판단하지 마세요. 녹색으로 변했거나 싹이 심하게 나고 쭈그러진 감자는 먹지 않는 편이 안전합니다. 감자 요리에서 쓴맛이 나면 먹기를 멈춥니다.'}])
p.pop('academicRefs',None)
assert 40<=len(p['title'])<=60,len(p['title'])
with db.open('w',encoding='utf-8-sig',newline='\r\n') as f:f.write(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(w/'august-seasonal-foods.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')
print('Saved article; title characters:',len(p['title']))

import copy
import hashlib
import json
from pathlib import Path

ROOT = Path('D:/작업/꿀단지')
WORK = Path(__file__).parent
DB = ROOT / 'data/posts_db.json'
raw = DB.read_bytes()
posts = json.loads(raw.decode('utf-8-sig'))
old = copy.deepcopy(posts)
p = next(p for p in posts if p['slug'] == 'water-intake-guide.html')
backup = WORK / 'before'
backup.mkdir(exist_ok=True)
if (backup / 'posts_db.json').exists():
    raise SystemExit('Backup already exists; inspect instead of overwriting.')
(backup / 'posts_db.json').write_bytes(raw)
(backup / 'water-intake-guide.html').write_bytes((ROOT / 'kkuldanji_web/posts/water-intake-guide.html').read_bytes())

p['title'] = '하루 물 섭취량, 체중만으로 정해도 될까? 커피와 식사 중 물 마시는 습관'
p['shortTitle'] = '하루 물 섭취량, 커피와 식사 중 물은?'
p['desc'] = '체중별 계산만으로 하루 물 섭취량을 정하기 어려운 이유와 총수분·음료의 차이를 설명합니다. 커피와 식사 중 물에 대한 오해, 실제 마신 양 기록법과 수분 제한이 필요한 경우를 확인하세요.'
p['featuredCaption'] = '하루 마신 물과 음료를 살펴보고 생활 조건에 맞게 조절하는 수분 섭취 습관'
p['academicSource'] = 'NHS·Mayo Clinic·NIDDK의 수분 섭취 안내를 바탕으로 정리'
p['bodyHtml'] = '''<div class="lead-quote-card">
<strong>하루 물 섭취량은 체중 하나로 결정되지 않습니다.</strong>
<p>음식과 음료로 얻는 수분, 활동량, 날씨와 건강 상태를 함께 봐야 합니다. 커피도 수분 섭취에 포함되며, 식사 중 물을 마신다고 소화액이 희석되어 소화가 나빠지는 것은 아닙니다. 정해진 숫자를 억지로 채우기 전에 지금 마시는 양부터 확인해 보세요.</p>
</div>
<p>500mL 텀블러를 두 번 채웠는데, 하루 물 섭취량은 1L로 적어도 될까요? 남긴 물이 있다면 실제 마신 양은 그보다 적습니다. 반대로 물만 기록했다면 우유나 차로 마신 수분은 빠져 있을 수 있습니다. 수분 섭취량을 살필 때는 먼저 <strong>무엇을 세고 있는지</strong> 구분하는 것이 도움이 됩니다.</p>
<nav class="toc-box" aria-label="본문 목차"><strong>목차</strong><ul>
<li><a href="#section1">체중별 계산보다 먼저 구분할 총수분과 음료</a></li>
<li><a href="#section2">텀블러로 실제 마신 양 기록하기</a></li>
<li><a href="#section3">커피와 차도 수분 섭취에 포함될까?</a></li>
<li><a href="#section4">식사 중 물과 생활 속 마시는 시간</a></li>
<li><a href="#section5">양을 늘리기 전에 확인할 몸 상태</a></li>
</ul></nav>

<h2 id="section1">체중별 계산보다 먼저 구분할 총수분과 음료</h2>
<figure class="post-img-wrap"><img src="../images/posts/water/water04.jpg" alt="과일과 물이 담긴 유리병" loading="lazy" width="1200" height="670"><figcaption>수분은 마시는 물뿐 아니라 음식과 다른 음료에서도 얻습니다.</figcaption></figure>
<p><strong>총수분 섭취량</strong>에는 생수, 차, 우유 같은 음료와 음식에 들어 있는 수분이 모두 포함됩니다. 반면 ‘오늘 물을 얼마나 마셨나’라는 기록은 대개 맹물만 셉니다. 둘을 같은 수치로 비교하면 충분한지 부족한지 판단이 어긋날 수 있습니다.</p>
<p>체중에 일정한 숫자를 곱한 계산값만으로 누구에게나 맞는 맹물의 양을 정할 수는 없습니다. 같은 체중이라도 더운 곳에서 일하거나 오래 운동하는 날과 실내에서 쉬는 날의 필요량이 다를 수 있기 때문입니다. 식사로 얻는 수분도 매일 같지 않아, 계산값에서 음식 몫으로 무조건 1L를 빼는 방식은 적절하지 않습니다.</p>
<p>NHS가 안내하는 하루 6~8잔의 음료 역시 일반적인 참고 기준입니다. 개인에게 반드시 맞춰야 할 처방량으로 해석하지 말고, 활동과 날씨, 임신·수유 등 자신의 조건에 맞춰 살펴야 합니다.</p>

<h2 id="section2">텀블러로 실제 마신 양 기록하기</h2>
<figure class="post-img-wrap"><img src="../images/posts/water/water02.jpg" alt="노트북 옆에 놓인 텀블러와 수첩" loading="lazy" width="1200" height="670"><figcaption>채운 횟수뿐 아니라 남긴 양까지 확인하면 실제 마신 양을 기록하기 쉽습니다.</figcaption></figure>
<p>하루 동안 컵이나 텀블러의 용량과 남긴 양을 적어 보세요. 물과 다른 음료를 따로 적으면 ‘맹물을 마신 양’과 ‘음료 전체를 마신 양’을 구분할 수 있습니다.</p>
<div class="custom-data-table-wrap" style="overflow-x:auto;"><table><caption>계산 방법을 보여 주는 가상의 하루 기록 — 권장 섭취량이 아닙니다</caption><thead><tr><th scope="col">기록 항목</th><th scope="col">계산</th><th scope="col">실제 마신 양</th></tr></thead><tbody>
<tr><td>물</td><td>500mL씩 두 번 채우고 총 200mL 남김</td><td>800mL</td></tr>
<tr><td>커피</td><td>200mL 한 잔을 모두 마심</td><td>200mL</td></tr>
<tr><td>우유</td><td>200mL 한 팩을 모두 마심</td><td>200mL</td></tr>
<tr><td>음료 합계</td><td>물 + 커피 + 우유</td><td>1,200mL</td></tr>
</tbody></table></div>
<p>이 예시에서 물은 800mL, 음료 전체는 1,200mL입니다. 음식 속 수분은 포함하지 않았으므로 이 숫자가 총수분 섭취량은 아닙니다. 숫자만 보고 부족하다고 단정하거나, 다른 사람의 목표량에 맞추기 위해 한꺼번에 물을 더 마시지는 마세요.</p>

<h2 id="section3">커피와 차도 수분 섭취에 포함될까?</h2>
<figure class="post-img-wrap"><img src="../images/posts/water/water03.jpg" alt="물 한 잔과 곡물차가 놓인 쟁반" loading="lazy" width="1200" height="670"><figcaption>음료가 수분에 기여하는지와 자주 마시기 좋은 선택인지는 구분해서 살펴보세요.</figcaption></figure>
<p>평상시 마시는 커피와 차도 수분 섭취에 포함됩니다. 카페인에 이뇨 작용이 있다는 이유만으로 <strong>‘커피를 마신 양의 1.5~2배가 빠져나간다’거나 ‘반드시 물 두 잔으로 보충해야 한다’고 계산하지 않습니다.</strong></p>
<p>다만 수분에 포함된다는 것이 커피를 물처럼 계속 마셔도 된다는 뜻은 아닙니다. 카페인과 당류도 함께 고려해야 합니다. 물은 당류 없이 수분을 보충할 수 있는 기본 선택입니다.</p>
<div class="custom-data-table-wrap" style="overflow-x:auto;"><table><thead><tr><th scope="col">마시는 것</th><th scope="col">수분 기록</th><th scope="col">함께 살필 점</th></tr></thead><tbody>
<tr><td>물</td><td>마신 양을 기록</td><td>억지로 한꺼번에 많은 양을 채우지 않기</td></tr>
<tr><td>커피·차</td><td>수분 섭취에 포함</td><td>카페인, 첨가한 설탕·시럽 확인</td></tr>
<tr><td>우유</td><td>수분 섭취에 포함</td><td>식사에서 얻는 영양과 함께 고려</td></tr>
<tr><td>당이 든 음료</td><td>수분은 포함되지만 별도로 구분</td><td>수분 보충만을 위해 자주 선택하기보다 물로 바꾸기</td></tr>
</tbody></table></div>

<h2 id="section4">식사 중 물과 생활 속 마시는 시간</h2>
<figure class="post-img-wrap"><img src="../images/posts/water/water01.jpg" alt="햇살이 드는 식탁 위 레몬 조각을 넣은 물" loading="lazy" width="1200" height="670"><figcaption>사진은 물을 준비한 예시입니다. 레몬을 넣거나 특정 시간에 마셔야 하는 것은 아닙니다.</figcaption></figure>
<p>식사 중이나 식후에 물을 마시는 것이 소화액을 희석해 소화를 방해한다는 설명은 맞지 않습니다. 따라서 누구나 식사 중 물을 100mL 이하로 제한하거나 식후 한 시간을 기다릴 필요는 없습니다.</p>
<p>물을 자주 잊는다면 식사할 때와 식사 사이처럼 반복되는 일상에 연결해 보세요. 물병을 책상에 두거나 외출할 때 챙기는 방식도 기록을 이어 가는 데 쓸 수 있습니다. 이런 습관은 마실 기회를 만드는 방법이지, 특정 시각에 흡수율이 높아진다는 의미는 아닙니다.</p>
<p>취침 전 물 한 잔이 심근경색이나 뇌경색을 예방한다고 약속할 근거는 이 글에서 확인하지 못했습니다. 질병 예방 효과를 기대하며 정해진 양을 억지로 마시는 시간표는 권하지 않습니다.</p>

<h2 id="section5">양을 늘리기 전에 확인할 몸 상태</h2>
<p>갈증, 평소보다 적어진 소변, 진해진 소변, 어지럼처럼 여러 변화를 함께 살펴보세요. 소변이 연한 노란색인지는 수분 상태를 가늠하는 참고가 되지만, <strong>소변 색 하나만으로 탈수나 과도한 수분 섭취를 진단할 수는 없습니다.</strong></p>
<p>건강한 성인이 평소 생활에서 물을 너무 많이 마시는 경우는 드물지만, 과도한 물 섭취는 혈중 나트륨 농도를 낮춰 위험해질 수 있습니다. 목표량을 채우려고 단시간에 많은 양을 몰아 마시지 마세요.</p>
<p>콩팥병이 있거나 심장·간 질환 등으로 수분 제한을 안내받았다면 일반적인 권장량보다 담당 의료진의 지침이 우선입니다. 모든 콩팥병 환자가 물을 제한해야 하는 것도 아니므로, 자신의 상태에 맞는 양을 확인해야 합니다.</p>
<p>구토나 설사가 있으면 물뿐 아니라 전해질도 잃을 수 있어 약사나 의료진에게 경구수분보충액 사용을 상담할 수 있습니다. 일어설 때 어지럼이 계속되거나 소변량이 크게 줄면 신속히 진료를 받으세요. 의식이 흐려지거나 호흡이 힘들다면 즉시 응급 도움을 요청해야 합니다.</p>'''
p['faqs'] = [
    {'q': '체중으로 계산한 하루 물 섭취량을 꼭 채워야 하나요?', 'a': '체중만으로 필요한 맹물의 양을 정할 수는 없습니다. 음식과 음료로 얻는 수분, 활동량, 날씨와 건강 상태를 함께 고려해야 합니다. 수분 제한을 안내받았다면 담당 의료진의 지침을 따르세요.'},
    {'q': '커피 한 잔을 마시면 물 두 잔을 더 마셔야 하나요?', 'a': '평상시 마시는 커피도 수분 섭취에 포함됩니다. 마신 양의 1.5~2배가 빠져나간다고 계산해 일정량의 물을 반드시 추가할 필요는 없습니다. 다만 카페인과 첨가당을 고려하고, 수분 보충의 기본 음료로는 물을 선택하세요.'},
    {'q': '식사 중 물은 소화액을 희석해 소화를 방해하나요?', 'a': '식사 중이나 식후에 물을 마시는 것이 소화액을 희석해 소화를 방해하는 것은 아닙니다. 누구나 물을 100mL로 제한하거나 식후 한 시간을 기다릴 필요는 없습니다. 별도의 질환으로 수분 제한을 안내받았다면 그 지침이 우선입니다.'}
]
refs = [
    ('https://www.nhs.uk/live-well/eat-well/food-guidelines-and-food-labels/water-drinks-nutrition/', 'NHS — Water, drinks and hydration: 일반적인 음료 섭취 안내와 커피·차의 수분 기여'),
    ('https://www.mayoclinic.org/healthy-lifestyle/nutrition-and-healthy-eating/expert-answers/digestion/faq-20058348', 'Mayo Clinic — Water after meals: Does it disturb digestion? 식사 중·후 물과 소화'),
    ('https://www.mayoclinic.org/healthy-lifestyle/nutrition-and-healthy-eating/in-depth/water/art-20044256', 'Mayo Clinic — Water: How much should you drink every day? 개인별 수분 필요량과 과잉 섭취'),
    ('https://www.nhs.uk/conditions/dehydration/', 'NHS — Dehydration: 탈수 증상과 진료가 필요한 상황'),
    ('https://www.niddk.nih.gov/health-information/kidney-disease/chronic-kidney-disease-ckd/healthy-eating-adults-chronic-kidney-disease', 'NIDDK — Healthy Eating for Adults with Chronic Kidney Disease: 콩팥 기능에 따른 수분 조절')
]
p['references'] = [f'<a href="{url}" rel="noopener noreferrer" target="_blank">{label}</a>' for url, label in refs]
p.pop('academicRefs', None)  # This field takes precedence over actual reference links in the renderer.
p['referencesTitle'] = '참고 자료'
assert len(p['title']) >= 40
assert len(posts) == len(old) == 32
assert sum(a != b for a,b in zip(old,posts)) == 1
assert DB.read_bytes() == raw, 'Source changed concurrently'
(WORK / 'post_data.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n', encoding='utf-8')
newline = '\r\n' if b'\r\n' in raw else '\n'
serialized = json.dumps(posts, ensure_ascii=False, indent=2) + '\n'
DB.write_bytes((b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'') + serialized.replace('\n',newline).encode('utf-8'))
print('Updated only water-intake-guide.html; title length:',len(p['title']))

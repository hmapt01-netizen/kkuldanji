import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
W=Path(__file__).resolve().parent
sys.path.insert(0,str(W.parent/'codex_tools'))
from title_adapter import check_titles
titles=[
'“술자리 다음 날 나온 숫자?” 중성지방 재검을 앞두고 식사·음주 이력 정리하기',
'“빈속으로 갔는데 또 높다고?” 중성지방 검사 공복 조건과 결과 해석의 차이',
'“잠깐 금주하면 괜찮을까?” 중성지방 술 영향과 검사 결과 비교에 필요한 기록',
'중성지방 재검, 한 번 낮아진 숫자로 안심해도 될까? 검사 조건과 변화 읽는 법',
'중성지방 검사 공복만 지키면 충분할까? 음주 이력과 함께 살펴볼 준비 사항',
'중성지방 술 때문이라며 넘겨도 될까? 식사·복용약·이전 결과를 함께 보는 이유',
'건강검진 결과표의 중성지방 재검 안내, 검사 시기 상담과 생활 기록 준비 가이드',
'중성지방 검사 공복 조건 이해하기, 마지막 식사부터 채혈까지 기록할 항목 3가지',
'중성지방 술 영향 살펴보기, 금주 전후 검사에서 수치와 함께 비교해야 할 조건',
'중성지방 재검 전 알아둘 검사 조건과 결과표 읽기, 금주 후 변화 확인하는 순서'
]
queries=['중성지방 재검','중성지방 검사 공복','중성지방 술']*3+['중성지방 재검']
data={'google_candidates':titles,'search_queries':queries}
for i,t in enumerate(titles,1):print(i,len(t),t)
check_titles(data,'google')
(W/'google_candidates.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')

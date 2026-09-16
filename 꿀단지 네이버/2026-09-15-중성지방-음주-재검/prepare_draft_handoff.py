import hashlib, json, sys
from pathlib import Path
W=Path(__file__).resolve().parent
sys.path.insert(0,str(W.parent/'codex_tools'))
from reuse_guard import selections
def ref(name, excerpt):
    p=W/name
    assert excerpt in p.read_text(encoding='utf-8-sig')
    return dict(path=name,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),excerpt=excerpt)
refs=[ref('source_notes.md','며칠 금주하면 정상화된다는 보장은 제시하지 않는다.'),ref('draft_source_notes.md','특정 금주 일수와 감소율은 본문에 넣지 않는다.')]
data=dict(version=1,stage='draft',selected_titles=selections(W,'draft'),intent='선택 제목이 약속한 재검 조건·금주 후 변화 비교를 두 채널의 독립된 구성으로 설명',reviewed_existing=refs,questions=[dict(question='검사 준비와 금주 후 결과를 어떻게 비교할 것인가?',mode='reuse',answer='검사 조건·생활 변화·다른 결과를 함께 기록하고 의료진과 다음 일정을 정한다.',limits='성인 일반 안내. 금주 일수·정상화·투약 여부의 개별 판단을 대신하지 않음.',body_location='네이버 3개 절, 구글 검사 조건·기록·결과표·결론 및 FAQ',evidence=refs)])
(W/'codex_reuse/draft.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')

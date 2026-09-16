from pathlib import Path
import re,json,sys,shutil
W=Path(__file__).resolve().parent;R=W.parents[1]
sys.path.insert(0,str(R/'codex_tools'))
import workflow_guard as g
p=W/'post_data.json';data=g.read(p)
shutil.copy2(p,W/'registration_backup/post_data_before_trim.json')
body=data['bodyHtml']
remove=[
'기존 기록의 ACC 2026 지침 적용 교육도 비공복 선별검사와 공복 확인이 필요한 상황을 구분합니다.',
'질병관리청 국가건강정보포털의 《지질 검사》에도 공복 준비 안내가 있지만, 이를 모든 지질검사에 똑같이 적용하는 규칙으로 읽지는 마세요.',
'Mayo Clinic도 당류와 정제 탄수화물, 체중 관리 등 여러 생활 요소를 함께 다룹니다.',
'MedlinePlus는 중성지방을 포함한 지질검사와 개인의 위험요인을 함께 평가한다고 설명합니다.',
'기존 질병관리청 자료와 Mayo Clinic 안내에서도 생활습관 외에 혈당 상태, 갑상선 문제, 약물 등 관련 요인을 다룹니다.',
'Mayo Clinic은 처방받은 약을 지시대로 복용하고 생활 관리를 함께 이어가도록 안내합니다.',
'아래 표는 상담 준비를 위한 기록 양식이며, 원인을 판별하거나 건강 상태를 점수로 매기는 도구는 아닙니다.'
]
for sentence in remove:
    body,n=re.subn(r'<p\b[^>]*>'+re.escape(sentence)+r'</p>\s*','',body)
    assert n==1,sentence
replacements={
'미국 국립의학도서관 MedlinePlus는 중성지방 검사 전 9~12시간의 금식이 필요할 수 있으며, 금식 여부와 특별한 준비는 의료진이 안내한다고 설명합니다.':'금식이 필요한 검사라면 보통 9~12시간을 안내받습니다. 이번 검사에 필요한 공복 시간은 예약한 기관에 확인하세요.',
'Mayo Clinic의 《Triglycerides: Why do they matter?》는 음주가 중성지방에 영향을 주며, 심한 고중성지방혈증에서는 술을 피하도록 안내합니다.':'술은 중성지방에 영향을 줍니다. 특히 수치가 매우 높다면 술을 피해야 합니다.',
'MedlinePlus가 제시하는 성인 중성지방의 일반 분류는':'성인 중성지방의 일반적인 참고 범위는',
'MedlinePlus의 매우 높은 범위인 500mg/dL 이상 결과는':'500mg/dL 이상은 매우 높은 범위입니다. 이 정도의 결과는'
}
for a,b in replacements.items():
    assert a in body,a
    body=body.replace(a,b)
lead='<p style="font-size:1.02rem;line-height:1.9;color:#334155;margin-bottom:22px;"><strong>재검 전에는 공복 안내를 확인하고, 금주 시작일과 이전 결과표를 챙기세요. 수치가 내려가도 관리가 끝난 것은 아닙니다.</strong></p>'
body=body.replace('</blockquote>','</blockquote>'+lead,1)
data['bodyHtml']=body
p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
receipt=next(r for r in g.state_of(W)['receipts'] if r['stage']=='assembly')
g.record(W,'assembly',[x['path'] for x in receipt['artifacts']],'사용자 요청: 본문 기관명·근거 반복 7문단 제거, 결론 우선 배치. 참고문헌 및 필요한 검사 조건 유지')
print('Removed 7 repeated explanatory paragraphs; lead answer added')

from pathlib import Path
import json,re,sys,shutil
W=Path(__file__).resolve().parent;R=W.parents[1]
sys.path.insert(0,str(R/'codex_tools'))
import workflow_guard as g
p=W/'post_data.json';data=g.read(p)
shutil.copy2(p,W/'registration_backup/post_data_before_content_review.json')
old='같은 날 받는 다른 검사까지 있다면 물이나 복용약에 관한 준비가 달라질 수 있으므로 예약한 기관의 안내를 확인해야 합니다.'
new='지질검사만 받는 경우 맹물은 보통 마실 수 있습니다. 다른 검사도 함께 받는다면 물과 복용약에 대한 기관 안내를 따르세요.'
assert old in data['bodyHtml']
data['bodyHtml']=data['bodyHtml'].replace(old,new).replace('마지막 음식이나 음료를 섭취한 시각','마지막 음식이나 맹물 외 음료를 섭취한 시각').replace('아침에 음료를 마셨다면','아침에 맹물 외 음료를 마셨다면')
data['references'].append('Mayo Clinic 《Cholesterol test》 — 지질검사 금식 중 맹물 허용과 검사별 준비 안내. <a href="https://www.mayoclinic.org/tests-procedures/cholesterol-test/about/pac-20384601">원문</a>')
p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
for name in ('naver_final.md','naver_with_images.html','naver_draft_preview.html'):
    f=W/name
    s=f.read_text(encoding='utf-8')
    s=s.replace('간식을 먹거나 음료를 마셨다면','간식을 먹거나 맹물 외 음료를 마셨다면')
    for br in ('\n','<br>'):
        s=s.replace('동시에 받는 검사에 따라'+br+'물이나 약에 관한 안내도 확인할 수 있습니다.','지질검사만 한다면 맹물은 보통 괜찮지만'+br+'다른 검사도 있다면 기관 안내를 따르세요.')
    f.write_text(s,encoding='utf-8')
report={'scope':'최종 구글 본문·FAQ 내용 및 연관 네이버 문구 대조. 브라우저 시각 검수와 공개 배포는 제외','verified':['조건부 금식 9~12시간','성인 중성지방 참고 범위 150/200/500 mg/dL 경계','매우 높은 중성지방과 췌장염 위험','금주 일수와 정상화 보장 없음','비공복 검사 활용 및 검사 목적별 재검 판단','임의 약물 중단 금지'],'corrected':'맹물과 다른 음료를 구분하도록 구글·네이버 표현 보완','sources':['https://medlineplus.gov/lab-tests/triglycerides-test/','https://www.mayoclinic.org/diseases-conditions/high-blood-cholesterol/in-depth/triglycerides/art-20048186','https://www.mayoclinic.org/tests-procedures/cholesterol-test/about/pac-20384601','https://learn.acc.org/AssetListing/Putting-the-Guidelines-into-Practice-Building-a-State-of-the-Art-Lipid-and-Cardiometabolic-Clinic-26302/Key-Implementation-Highlights-from-the-2026-Guideline-on-the-Management-of-Dyslipidemia-36096']}
(W/'content_review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
receipt=next(r for r in g.state_of(W)['receipts'] if r['stage']=='assembly')
g.record(W,'assembly',[a['path'] for a in receipt['artifacts']]+['content_review.json'],'본문 사실관계 대조 및 맹물/음료 구분 보완. 네이버 동일 표현 동기화')

from pathlib import Path
import json,re
w=Path(__file__).resolve().parent.parent
def save(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=json.loads((w/'post_data.json').read_text(encoding='utf-8-sig'))
b=p['bodyHtml']
b=re.sub(r'<blockquote class="lead-quote-card"(.*?)</blockquote>', '<div class="lead-quote-card" style="background:#f8fafc;border-left:4px solid #22c55e;padding:18px 20px;margin:0 0 28px;line-height:1.8;"><strong>핵심 요약</strong><br>아침에 굳는 시간과 아픈 마디 위치는 참고 단서입니다. 이 두 가지로 류마티스 관절염을 확정하거나 배제할 수는 없습니다. 작은 관절의 붓기가 지속되면 혈액검사가 정상이더라도 진료를 미루지 마세요. 갑자기 심하게 아프고 부으면 신속한 진료가 먼저입니다.</div>',b,flags=re.S)
changes={
'수면 시간 동안 손가락 관절의 움직임이 줄어들면 관절낭 내부의 유연성이 일시적으로 떨어지며 아침에 일어났을 때 뻣뻣한 느낌이 들 수 있습니다.':'골관절염이나 류마티스 관절염에서는 잠에서 깬 뒤 또는 한동안 움직이지 않은 뒤 관절이 뻣뻣하게 느껴질 수 있습니다.',
'국제 공인 분류 기준에서도 조조강직 지속 시간 하나만으로 진단하지 않으며, 침범 관절 수와 혈청학적 검사, 염증 수치, 증상 지속 기간을 종합적으로 합산하여 평가합니다.':'류마티스 관절염 분류 기준은 관절 침범, 혈액검사, 염증 수치와 증상 기간을 함께 평가합니다. 이 기준은 진료를 돕는 분류 도구이며, 개인의 진단을 대신하는 자가진단표는 아닙니다.',
'양손 대칭으로 침범하는 경향이 뚜렷하며':'양손에 대칭으로 나타나는 경향이 있지만 항상 그런 것은 아니며',
'(양측 대칭)':'(대칭 경향)',
'손을 많이 쓴 날 늦은 저녁':'손을 많이 사용한 뒤',
'손가락 끝마디의 헤베르덴 결절 부위를 억지로 누르거나 강하게 문지르는 마사지를 하면 통증과 부종이 악화될 수 있으므로 무리한 압박을 피하시기 바랍니다.':'튀어나온 마디를 누르거나 문지를 때 아프다면 그 자극을 멈추세요. 결절이나 통증이 새로 생겼다면 진료를 통해 원인을 확인하는 편이 좋습니다.',
'또한 관절 마디가 붉게 달아오르고 부어오른 상태에서 뜨거운 온찜질을 곧바로 적용하면 국소 혈류가 늘어나 붓기가 더 심해질 수 있으므로, 열감이 남아있을 때는 섣부른 온열 찜질을 피하고 차분히 안정을 취해야 합니다.':'관절이 갑자기 붉게 달아오르거나 심하게 붓고 아플 때는 찜질로 해결하려 하지 말고 먼저 진료를 받으세요. 뜨거운 물이나 찜질로 불편함을 참아가며 손을 움직이지 마세요.',
'손 펴기·갈고리·가벼운 주먹·끝마디를 편 주먹의 네 가지 자세':'같은 왼손을 손바닥 쪽에서 본 손 펴기·갈고리·가벼운 주먹·끝마디를 편 주먹 자세',
'무리하게 주먹을 쥐어짜지 않고 힘줄의 유연한 움직임을 돕는 4가지 기본 동작으로 구성됩니다.':'아래는 건글라이딩에 쓰이는 네 가지 자세 예시입니다. 개인 상태에 따라 적합한 동작이 다르므로 통증이나 붓기가 지속되면 의료진에게 먼저 확인하세요. 각 자세 사이에는 손을 다시 편 자세로 돌아옵니다.',
'건글라이딩 4단계 실천 순서':'건글라이딩 네 가지 자세',
'손가락 끝마디는 편 채로 손바닥 관절과 가운데마디를 직각으로 구부려 손바닥에 닿게 합니다.':'손가락 끝마디는 편 채로 뿌리마디와 가운데마디를 부드럽게 굽힙니다. 손끝이 손바닥을 향하도록 하되 억지로 닿게 누르지 않습니다.',
'손가락 전체를 손바닥 안쪽으로 둥글게 말아 쥐며 주먹 자세를 취합니다.':'손가락 전체를 손바닥 안쪽으로 둥글게 말아 가볍게 주먹을 쥡니다. 꽉 쥐어짜지 않습니다.',
'※ 개인의 관절 상태에 맞추어 통증이 생기지 않는 편안한 범위 내에서 각 동작을 잠시 유지하며 부드럽게 반복합니다.':'※ 통증 없는 범위에서 천천히 움직이고, 아프면 중단하세요. 갑작스러운 심한 통증·부종이 있을 때는 운동보다 진료가 먼저입니다. 다쳤거나 수술받은 손은 담당 의료진이 정한 동작과 횟수를 따르세요.'}
for old,new in changes.items():
    assert old in b,old
    b=b.replace(old,new)
p['bodyHtml']=b
p['academicSource']='NHS·NICE NG100·2010 ACR/EULAR 분류 기준 및 NHS 손 재활 안내 기반'
p['references']=[r for r in p['references'] if 'health.kdca.go.kr' not in r]
newrefs=[('https://www.nhs.uk/conditions/osteoarthritis/','NHS: Osteoarthritis','골관절염의 증상 및 진단 참고 사항'),('https://www.nhs.uk/conditions/rheumatoid-arthritis/symptoms/','NHS: Rheumatoid arthritis symptoms','조조강직과 대칭성의 경향 및 예외'),('https://www.nhs.uk/conditions/trigger-finger/','NHS: Trigger finger','걸림, 탄발감 및 손 사용 시 증상'),('https://www.plymouthhospitals.nhs.uk/display-pil/pil-active-tendon-gliding-exercises-5881/','University Hospitals Plymouth NHS Trust: Active Tendon Gliding Exercises','손 힘줄 운동 자세와 개인별 적용 주의')]
p['references'] += [f'<a href="{u}">{t}</a> — {s}.' for u,t,s in newrefs]
p['faqs'][1]['a']='튀어나온 마디를 만질 때 아프다면 누르거나 문지르는 자극을 멈추세요. 뼈 돌출처럼 보이는 변화가 모두 같은 원인은 아니므로 새로 생긴 결절이나 통증은 진료로 확인하는 것이 좋습니다.'
save(w/'post_data.json',p)
n=next(w.glob('*_네이버블로그용.html'));h=n.read_text(encoding='utf-8-sig')
h=h.replace('관절낭 안쪽의 유연성이 떨어지며 이른 아침에 뻣뻣한 \'조조강직\'이 나타납니다.','골관절염이나 류마티스 관절염이 있으면 아침 또는 쉬고 난 뒤 뻣뻣함을 느낄 수 있어요.')
h=h.replace('잠을 자는 동안에는 손을 거의 쓰지 않다 보니','아침에 느끼는 손의 뻣뻣함을 조조강직이라고 하는데요.')
h=h.replace('양쪽 손에 비슷하게 말랑한 물주머니처럼 부어오릅니다.','양쪽 손에서 비슷하게 붓는 경향이 있어요. 다만 한쪽만 불편하다고 배제할 수는 없습니다.')
h=h.replace('튀어나온 돌기 부위가 거슬린다고 손톱 끝으로 꾹꾹 누르거나 강판 밀듯 문지르면 마디가 더 붓고 욱신거릴 수 있으니 세게 만지지 않아야 합니다.','튀어나온 마디를 누르거나 문지를 때 아프다면 그만 멈추세요. 새로 생긴 돌기나 통증은 진료로 확인하는 편이 좋아요.')
h=h.replace('뻣뻣함을 풀 때는 따뜻한 물에 손을 가볍게 담그는 것이 편안하지만 후끈거림이 감돌 때는 온찜질을 잠시 멈추시고,','갑자기 심하게 붓거나 아플 때는 찜질이나 운동보다 진료가 먼저예요.')
h=h.replace('힘줄이 결대로 부드럽게 미끄러지도록 유도하는 건글라이딩 동작을 통증이 없는 선에서 가볍게 따라 해 보세요.','아래 그림은 힘줄 움직임을 돕는 네 가지 자세 예시예요. 통증 없이 가볍게 움직일 수 있을 때만 해보고, 아프면 중단하세요.')
h=h.replace('손 펴기·갈고리·가벼운 주먹·끝마디를 편 주먹의 네 가지 자세',changes['손 펴기·갈고리·가벼운 주먹·끝마디를 편 주먹의 네 가지 자세'])
needle='<img src="images/stickers/sticker06_emergency.jpg"'
h=h.replace(needle,'<p>그림은 모두 같은 왼손을 손바닥 쪽에서 본 모습이에요.<br>손 펴기 → 갈고리 모양 → 가벼운 주먹 → 끝마디를 편 주먹을 보여줍니다. 각 자세 사이에는 다시 손을 펴주세요. 꽉 쥐거나 억지로 굽히지 않고, 다쳤거나 수술한 손은 담당 의료진의 안내를 따르세요.</p>\n\n        '+needle)
h=h.replace('• 보건당국 국가건강정보포털: 류마티스 관절염 및 골관절염 표준 진료지침<br>','• NHS: 골관절염·류마티스 관절염의 증상 안내<br>')
h=h.replace('• UK NHS: 수부 골관절염 및 감염성 관절염 진료 가이드','• UK NHS: 수부 골관절염 및 감염성 관절염 안내<br>• University Hospitals Plymouth NHS Trust: Active Tendon Gliding Exercises<br>• Deweber 외, 2011: 손가락 꺾기와 손 골관절염의 연관성 연구')
h=h.replace('href="plantar-fasciitis-morning-heel-pain-stretching.html"','href="../../kkuldanji_web/posts/plantar-fasciitis-morning-heel-pain-stretching.html"')
n.write_text(h,encoding='utf-8')
m=json.loads((w/'evidence_manifest.json').read_text(encoding='utf-8-sig'))
m['excluded_sources']=[dict(s,exclusion_reason='2026-10-08 재확인: 5298은 홈페이지로 이동, 5309는 C형간염. 본문 근거에서 제외. 기존 요약의 직접 인용 여부 미확인.') for s in m['sources'] if s['id'].startswith('src_kdca')]
m['sources']=[s for s in m['sources'] if not s['id'].startswith('src_kdca')]
for s in m['sources']:
    if 'evidence_quote' in s:s['evidence_summary']=s.pop('evidence_quote')
    s['quotation_note']='기존 근거 요약으로 취급하며 직접 인용으로 사용하지 않음'
for sid,(u,t,s) in zip(['src_nhs_oa_overview','src_nhs_ra','src_nhs_trigger','src_plymouth_tendon'],newrefs):
    m['sources'].append(dict(id=sid,url=u,title=t,type='official_patient_information',evidence_summary=s,checked_date='2026-10-08'))
for c in m['claims']:
    c['source_ids']=[s for s in c['source_ids'] if not s.startswith('src_kdca')]
    if c['id']=='claim_morning_stiffness': c['source_ids']=['src_nhs_oa_overview','src_nhs_ra']
    if c['id']=='claim_heberden_pressure':c.update(statement='통증을 유발하는 압박은 멈추고 새로 생긴 결절이나 통증은 진료로 확인한다.',source_ids=['src_nhs_oa_overview'],limits='일반적인 증상 관리 표현. 특정 마사지의 손상·부종 유발 기전으로 단정하지 않음.')
m['review_note']='2026-10-08: 잘못된 질병관리청 인용 제거, 손 운동 그림과 설명 대조. 원문 열람은 research 단계였으나 재개 후 NHS 4개 URL 도구 호출 직전 check 누락; 사전 검사 완료로 소급 기록하지 않음.'
save(w/'evidence_manifest.json',m)
note='\n\n## 2026-10-08 이미지·전체 재검수 보완\n- 운동 그림을 같은 왼손, 손바닥 방향으로 통일. 각 자세 사이 손 펴기, 통증 없는 범위, 부상·수술 시 개별 안내 조건을 본문에 반영.\n- KDCA 5298은 홈페이지 이동, 5309는 C형간염 페이지이므로 인용 제외.\n- NHS OA: 사용 시 통증, 아침 강직 없음 또는 30분 미만은 진단 참고 단서이며 단독 진단 기준 아님. NHS RA: 대칭 경향은 항상 나타나지 않음.\n- NHS trigger finger: 굽힌 채 걸림, 펼 때 딸깍거림, 손 사용 시 악화.\n- Plymouth 손 재활 안내: 개인별 동작은 치료사와 결정. 갈고리는 뿌리마디를 편 채 중간·끝 관절 굽힘, 가벼운 주먹, 끝마디를 편 주먹, 자세 사이 손 펴기. 자료 게시2022·검토예정2024; 2026 개정 지침으로 표기하지 않음.\n'+ '\n'.join('- '+u for u,t,s in newrefs)+'\n'
for f in ['source_notes.md','리서치.md']:
    with (w/f).open('a',encoding='utf-8') as out:out.write(note)
ip=json.loads((w/'image_plan.json').read_text(encoding='utf-8-sig'))
ip['revision_v4']={'post03':'같은 왼손의 손바닥 방향 4자세. 좌우·관찰면, 엄지 위치, 본문 동작 설명 대조 완료.','record':'image_revision_v4/generation.json'}
save(w/'image_plan.json',ip)
dbp=Path('D:/작업/꿀단지/data/posts_db.json');db=json.loads(dbp.read_text(encoding='utf-8-sig'))
target=[x for x in db if x.get('slug')==p['slug']];assert len(target)==1
target[0].update(p);save(dbp,db)
print('Updated post, Naver, references, evidence notes, image plan and existing DB entry.')

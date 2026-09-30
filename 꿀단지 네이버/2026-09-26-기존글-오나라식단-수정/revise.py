import json, sys, shutil, hashlib
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
root=Path('D:/작업/꿀단지')
work=root/'꿀단지 네이버/2026-09-26-기존글-오나라식단-수정'
sys.path.insert(0,str(root/'codex_tools'))
import source_access_guard as access
db=root/'data/posts_db.json'
posts=json.loads(access.fetch(work,str(db)))
post=next(p for p in posts if p['slug']=='ohnara-diet.html')
before=work/'before'; before.mkdir(exist_ok=True)
for src,dst in [(db,before/'posts_db.json'),(root/'kkuldanji_web/posts/ohnara-diet.html',before/'ohnara-diet.html')]:
    if not dst.exists(): shutil.copy2(src,dst)
old=json.loads(json.dumps(post))
notes='''# 9번째 기존 글 근거 및 편집 기록

확인일: 2026-09-26. 기존 7편 수정내역·image-edits 및 8월 제철음식 수정내역에서 8/32 완료 확인. DB를 기존 작업 순서인 아래에서 위로 대조하여 다음 대상 ohnara-diet.html 확인. 네이버는 WORKFLOW.md의 기존 글 검토 범위 변경에 따라 제외.

## 검증 결과와 적용
- 오나라 47kg·나이·세 샐러드가 체중 유지 비결이라는 내용: 검색에서 2차 기사만 확인. 본인 원문과 장기 식사·체중 기록 미확인. 수치와 인과관계 삭제. 오나라 식단이라는 검색 의도만 도입에 유지하며 메뉴는 편집부 한 끼 조합 예시로 명시. 관련 기사 제목·요약 확인 URL: https://health.chosun.com/site/data/html_dir/2026/06/04/2026060401543.html (의학 근거로 사용하지 않음).
- 기존 학회 직접 인용은 실재 문구 확인 불가, 자체 핵심 요약으로 대체. 메밀 혈관 탄력·과당 흡수 차단·면역력·매년 근육 1~2%·관절 손상 없음·기초대사량 회복 보장 삭제. 50대 단백질 체중당 1.0~1.2g 일괄 권장도 삭제.
- 국내 식사 근거: 질병관리청, 심장과 뇌 건강을 위한 운동과 식사요법, 어떻게 하나요? (2023-08). https://health.kdca.go.kr/healthinfo/biz/health/ntcnInfo/healthSourc/thtimtCntnts/thtimtCntntsView.do?thtimt_cntnts_sn=55 . 통곡물·채소·생선·콩류 등 식품 선택, 설탕·포화지방 제한, 유산소/근력/유연성 역할 구분. 특정 식재료의 감량 효과로 확대하지 않음. 메뉴 조립·장보기 순서는 편집부 실천 예시.
- 국내 운동 기준: 질병관리청 신체활동! 알려드리겠습니다! (업데이트 2026-07-27). https://health.kdca.go.kr/healthinfo/biz/health/gnrlzHealthInfo/gnrlzHealthInfo/gnrlzHealthInfoView.do?cntnts_sn=6251 . 원문 짧은 발췌: “근력운동을 일주일에 2일 이상 해야 합니다.” 성인 중강도 유산소 주150~300분, 같은 부위 하루 이상 휴식, 수준에 맞춰 점진 증가. 본문 주간 계획·FAQ 적용.
- 동작 보충: NHS Strength exercises (검토2024-02-28, 다음검토2027-02-28). https://www.nhs.uk/live-well/exercise/strength-exercises/ . 바퀴 없는 안정적 의자, 의자 일어서기5회, 벽 밀기 자세. 국내 자료에 없는 구체적 시작 자세 보충. 표는 체력에 맞춰 조절할 시작 예시이지 개인 처방 아님.
- 사진 자세: AAOS Spine Conditioning Program, 2025 파일. https://orthoinfo.aaos.org/globalassets/pdfs/spine-conditioning-program_3-20-25.pdf . 4페이지 버드독: 손은 어깨 아래, 무릎은 골반 아래, 반대 팔·다리를 몸통 높이로, 허리 평평하게, 통증 시 중단. 표와 사진 설명 일치. 치료/재활은 전문가 지도 필요. 유지시간 처방은 생략.
- 농식품부 2021 식생활지침 발표 본문 확인 https://www.mafra.go.kr/bbs/mafra/131/326885/artclView.do . 첨부 PDF는 열리지 않아 세부 근거로 사용하지 않음. NHIS 근감소증 상세 원문도 접근 실패, 근거에서 제외.

## FAQ 질문과 답변 범위
- 매일 같은 근력운동? 같은 부위 하루 이상 휴식, 주2일 이상 기준(질병관리청6251).
- 무릎 아픈데 의자 운동? 통증을 참으며 반복하지 말고 중단, 지속되면 상담(AAOS 통증 원칙, NHS 의자 조건).
- 스트레칭만으로 근력운동 대체? 유연성/저항성 구분, 서로 보완(질병관리청55).

## 사진
원본 3장(대표1·본문2)을 육안 확인. 인물 사진은 일상 장면이며 식단 효과 증거로 표현하지 않음. 운동은 버드독. 신규 이미지 생성/편집 없음. HTML 표시를16:9로 맞추고 원본 파일 보존. 정사각형 인물은 얼굴이 보이도록 표시 위치 조정.
'''
(work/'source_notes.md').write_text(notes,encoding='utf-8')
access.transition(work,'writing','공식 근거 및 기존 사진 확인 완료. 미확인 체중·효능 삭제, 실천 예시로 재구성')
P='font-size:1.02rem;line-height:1.9;color:#334155;margin-bottom:22px;'
H='font-size:1.32rem;font-weight:850;color:#0f172a;margin:42px 0 16px;line-height:1.45;border-bottom:2px solid #0f172a;padding-bottom:8px;'
def p(t):return f'<p style="{P}">{t}</p>'
def h(i,t):return f'<h2 id="{i}" style="{H}">{t}</h2>'
def photo(file,alt,pos='center'):
    return f'<figure class="post-img-wrap post-photo-figure" style="margin:24px 0;"><img src="../images/posts/ohnara/{file}" alt="{alt}" loading="lazy" decoding="async" style="width:100%;aspect-ratio:16/9;object-fit:cover;object-position:{pos};border-radius:12px;display:block;"><figcaption>{alt}</figcaption></figure>'
sections=[('sec1','샐러드를 한 끼로 채우는 기준'),('sec2','장본 재료로 돌려 먹는 세 조합'),('sec3','한 끼를 넘어 하루 식사로 연결'),('sec4','걷기와 근력 운동을 나눠 시작'),('sec6','내일도 이어갈 작은 습관 고르기')]
body='<div class="lead-quote-card" style="border-left:4px solid #c26908;background:#f8fafc;padding:20px 22px;border-radius:10px;margin:24px 0;"><strong>핵심 요약</strong>'+p('샐러드를 식사로 먹는다면 채소에 단백질 식품과 밥·빵·면 등을 함께 담아보세요.')+p('걷기와 근력 운동은 나누어 계획하고, 현재 체력에 맞춰 조금씩 늘립니다.')+'</div>'
body+=p('오나라 식단을 찾아보다 “샐러드로 한 끼를 먹으면 나도 관리가 될까?” 하는 생각이 들었다면, 먼저 접시에 무엇이 들어 있는지 살펴보세요.')
body+=p('연예인의 사진이나 알려진 체중만으로 식단의 효과를 판단하기는 어려워, 이 글에서는 집에서 활용할 <strong>샐러드 식사 조합과 중년의 운동 시작 방법</strong>을 정리했습니다.')
body+='<nav class="toc-box" style="background:#f8fafc;border:1px solid #e2e8f0;border-left:4px solid #c26908;border-radius:10px;padding:18px 20px;margin:28px 0;"><strong>목차</strong><ul>'+''.join(f'<li><a href="#{i}">{t}</a></li>' for i,t in sections)+'</ul></nav>'
body+=h(*sections[0])+photo('ohnara02.jpg','야외에서 손목시계를 보는 일상 장면','center 35%')
body+=p('샐러드 한 그릇을 만들 때는 <strong>채소 → 단백질 식품 → 주식</strong> 순서로 담으면 빠진 재료를 찾기 쉽습니다.')
body+=p('잎채소와 토마토를 담았다면 달걀·두부·생선·닭고기 중 하나를 고르고, 밥이나 통곡물빵, 면처럼 식사의 바탕이 될 음식도 곁들여보세요.')
body+=p('마트에서는 채소 두 종류, 단백질 식품 한두 종류, 집에 있는 주식을 먼저 떠올리면 한 번 산 재료를 여러 끼에 나누어 쓰기 좋습니다.')
body+=p('드레싱은 작은 그릇에 따로 덜어 필요한 만큼 섞고, 견과류나 치즈 같은 토핑도 한꺼번에 많이 얹기보다 맛을 더할 정도로 시작해보세요.')
body+=h(*sections[1])+p('아래 세 가지는 집에서 조합해 볼 식사 예시입니다.')
body+='<div class="info-section-card" style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:14px;padding:22px 20px;margin:28px 0;">'
for title,text in [('버섯·당근·달걀 메밀면','메밀면에 익힌 버섯, 채 썬 당근, 잎채소를 담고 삶은 달걀이나 두부를 더합니다. 면을 삶는 동안 채소를 준비하고 소스는 먹기 직전에 섞어보세요.'),('토마토·단호박·닭고기','익힌 닭고기와 찐 단호박에 토마토를 곁들입니다. 닭고기 대신 두부를 써도 좋고, 단호박을 조금만 담았다면 밥이나 빵도 함께 준비해 한 끼 양을 맞춥니다.'),('참외·루꼴라와 두부 곁들이기','씻어 손질한 참외와 루꼴라에 두부구이나 달걀을 곁들여보세요. 식사로 먹을 때는 빵이나 밥을 추가하고, 루꼴라가 낯설면 집에 있는 잎채소로 바꿔도 됩니다.')]:
    body+=f'<h3 style="font-size:1.08rem;margin:18px 0 10px;">{title}</h3>'+p(text)
body+='</div>'+p('메밀면은 제품마다 배합이 다르므로 포장지의 원재료와 영양정보를 보고 고르면 됩니다.')
body+=p('특정 면을 고르는 것만으로 감량을 기대하기보다, 실제 먹는 면·소스의 양과 곁들이는 재료를 함께 살펴보세요.')
body+=h(*sections[2])+p('한 끼 구성이 잡혔다면 하루 중 다른 식사에도 단백질 식품과 채소가 들어가는지 확인해보세요.')
body+=p('예를 들어 아침에는 통곡물빵과 달걀, 점심에는 닭고기 샐러드와 주식, 저녁에는 밥과 두부 또는 생선 반찬을 먹는 식으로 재료를 바꿔볼 수 있습니다.')
body+=p('샐러드를 매 끼니 준비할 필요는 없으며, 평소 먹는 밥상에 빠진 반찬 하나를 더하는 방법도 충분히 실용적입니다.')
body+=p('식사를 바꾼 뒤에는 허기가 심해지는 시간이나 먹고 난 뒤의 편안함을 살피면서 양과 구성을 조절해보세요.')
body+=p('질환 때문에 식사량이나 단백질 섭취를 조절 중이라면 기존에 안내받은 식사 계획에 맞춰 재료를 고릅니다.')
body+=h(*sections[3])+photo('04_core_workout.jpg','반대쪽 팔과 다리를 뻗는 버드독 자세')
body+=p('식사와 함께 운동을 계획할 때는 <strong>걷는 날과 근력을 기르는 날</strong>을 달력에 표시해보세요.')
body+=p('성인의 일반적인 목표는 중강도 유산소 활동을 주 150~300분, 근력 운동을 주 2일 이상 하는 것이지만, 처음에는 할 수 있는 양부터 천천히 늘립니다.')
body+=p('표의 동작은 시작 방법을 고르기 위한 예시이며, 모두 같은 횟수로 채워야 하는 숙제는 아닙니다.')
rows=[('의자에서 일어서기','하체 근력','미끄러지지 않는 바퀴 없는 의자에 앉아 발을 바닥에 붙이고, 몸을 조금 앞으로 기울여 천천히 일어섰다 앉기','우선 5회, 자세가 흐트러지면 쉬기'),('벽 밀기','상체 근력','벽에 손을 가슴 높이로 짚고 몸을 곧게 유지하며 팔꿈치를 천천히 굽혔다 펴기','적은 횟수부터, 편안해지면 점차 늘리기'),('버드독','몸통 안정화','손은 어깨 아래, 무릎은 골반 아래에 두고 반대 팔·다리를 몸통 높이로 뻗은 뒤 돌아오기','허리가 꺾이거나 몸통이 돌아가지 않는 범위'),('걷기','유산소 활동','평탄한 길에서 편안한 속도로 출발해 익숙해지면 속도와 시간을 늘리기','짧게 나누어 시작해 주간 활동량 늘리기')]
body+='<div class="custom-data-table-wrap" role="region" aria-label="운동 시작 방법 비교표" tabindex="0" style="overflow-x:auto;margin:28px 0;border:1px solid #e2e8f0;border-radius:10px;"><table class="custom-data-table" style="width:100%;border-collapse:collapse;min-width:640px;font-size:0.92rem;text-align:left;"><thead><tr style="background:#f1f5f9;">'+''.join(f'<th scope="col" style="padding:14px 12px;border-bottom:2px solid #cbd5e1;">{x}</th>' for x in ['동작','역할','시작 자세','조절 기준'])+'</tr></thead><tbody>'
for row in rows:
    body+='<tr>'+''.join(f'<td style="padding:14px 12px;border-bottom:1px solid #e2e8f0;line-height:1.7;">{x}</td>' for x in row)+'</tr>'
body+='</tbody></table></div>'
body+=p('예를 들어 월요일과 목요일에 근력 운동을 하고, 다른 날에는 걷기를 더하는 식으로 시작할 수 있으며, 같은 부위를 운동한 뒤에는 하루 이상 쉬어줍니다.')
body+=p('동작 중 통증이 생기면 멈추고, 통증이 지속되거나 관절·허리 질환으로 치료 중이라면 운동 종류와 강도를 상담해 정하세요.')
body+=p('몸통 운동을 더 살펴보고 싶다면 <a href="core-exercise-home.html">초보자 코어 운동의 시작 자세</a>도 함께 확인할 수 있습니다.')
body+=h(*sections[4])+p('내일 식사를 위해 냉장고에 있는 단백질 식품 하나와 채소부터 골라두세요.')
body+=p('운동은 이번 주에 가능한 두 날을 정하고, 의자에서 천천히 일어서는 동작처럼 익숙해질 수 있는 것부터 시작하면 됩니다.')
body+=p('식사와 활동을 꾸준히 이어갈 수 있도록 한 번에 바꾸는 양을 줄여보세요.')
post.update(title='오나라 식단이 궁금하다면, 중년 샐러드 한 끼 구성과 집에서 시작하는 근력 운동',shortTitle='중년 샐러드 한 끼 구성과 운동 시작법',desc='오나라 식단이 궁금할 때 살펴볼 샐러드 한 끼 구성법. 집에서 활용하는 재료 조합 세 가지와 하루 식사 연결, 걷기·근력 운동의 시작 방법을 정리했습니다.',featuredCaption='야외 소파에서 쉬는 일상 장면',academicSource='식사 구성과 신체활동 지침을 참고한 실천 안내',bodyHtml=body,
 faqs=[{'q':'근력 운동은 매일 같은 동작을 해도 되나요?','a':'같은 부위를 근력 운동한 뒤에는 하루 이상 쉬어주는 것이 좋습니다. 주 2일 이상을 목표로 하되, 처음에는 현재 체력에 맞춰 횟수와 강도를 조절하세요.'},{'q':'무릎이 아픈데 의자에서 일어서기를 계속해도 되나요?','a':'통증이 생기면 중단하세요. 의자는 바퀴가 없고 미끄러지지 않아야 하며, 앉았을 때 발이 바닥에 닿아야 합니다. 통증이 이어지면 진료나 운동 상담으로 가능한 동작을 확인하세요.'},{'q':'스트레칭만 해도 근력 운동을 대신할 수 있나요?','a':'스트레칭은 주로 유연성을 기르는 활동입니다. 근력을 기르는 저항성 운동, 걷기 같은 유산소 활동과 역할이 달라 함께 계획하는 것이 좋습니다.'}])
refs=[('질병관리청 — 심장과 뇌 건강을 위한 운동과 식사요법 (2023)','https://health.kdca.go.kr/healthinfo/biz/health/ntcnInfo/healthSourc/thtimtCntnts/thtimtCntntsView.do?thtimt_cntnts_sn=55'),('질병관리청 — 신체활동! 알려드리겠습니다! (2026 갱신)','https://health.kdca.go.kr/healthinfo/biz/health/gnrlzHealthInfo/gnrlzHealthInfo/gnrlzHealthInfoView.do?cntnts_sn=6251'),('NHS — Strength exercises (2024 검토)','https://www.nhs.uk/live-well/exercise/strength-exercises/'),('AAOS — Spine Conditioning Program, Bird Dog (2025)','https://orthoinfo.aaos.org/globalassets/pdfs/spine-conditioning-program_3-20-25.pdf')]
post['references']=[f'<a href="{url}" target="_blank" rel="noopener noreferrer">{label}</a>' for label,url in refs]
post['academicRefs']='<ul>'+''.join(f'<li>{s}</li>' for s in post['references'])+'</ul>'
assert len(post['title'])>=40 and len(post['title'])<=60
for key in ['slug','slugKey','date','isEditorPick','thumb','relatedSlug','category','isLatest']:assert old.get(key)==post.get(key)
(work/'post_data.json').write_text(json.dumps(post,ensure_ascii=False,indent=2),encoding='utf-8')
db.write_text(json.dumps(posts,ensure_ascii=False,indent=2),encoding='utf-8')
(work/'image-edits.md').write_text('# 이미지 확인\n기존 대표1장·본문2장 유지. 파일 편집 및 생성 없음. 본문은16:9 표시로 통일하며 인물 사진 object-position을 center 35%로 조정. 운동사진 설명을 실제 버드독 자세로 변경. 원본 치수 및 최종 표시 비율은 validation.json에 기록.\n',encoding='utf-8')
print(json.dumps({'title':post['title'],'title_length':len(post['title']),'body_length':len(body),'changed_slug':post['slug']},ensure_ascii=False))

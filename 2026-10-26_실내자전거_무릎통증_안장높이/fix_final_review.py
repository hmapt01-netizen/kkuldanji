from pathlib import Path
import json,re,shutil,hashlib,io
from PIL import Image
R=Path(r'D:\작업\꿀단지'); W=R/'2026-10-26_실내자전거_무릎통증_안장높이'
B=W/'_before_final_fix_20261026'; B.mkdir(exist_ok=True)
for name in ['post_data.json','네이버.html','evidence_manifest.json','리서치.md','official_source_raw.txt','image_plan.json','image_generation_manifest.json']:
    shutil.copy2(W/name,B/name)
shutil.copy2(R/'data/posts_db.json',B/'posts_db.json')
for folder,name in [('images','post03.jpg'),('vertical','post03_9x16.png')]:
    shutil.copy2(W/folder/name,B/name)
d=json.loads((W/'post_data.json').read_text(encoding='utf-8-sig'))
pstyle='style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;"'
def paras(texts): return '\n'.join('<p '+pstyle+'>'+t+'</p>' for t in texts)
claims=[
('C1','실내자전거는 무릎관절염 환자에게 권장되는 운동 중 하나이며, 자신의 관절 상태와 통증에 맞춰 강도를 조절해야 합니다.',['S1'],'모든 사람에게 같은 강도·시간·회전수를 적용하지 않습니다.'),
('C2','2011년 문헌고찰은 안장 높이 설정 방법으로 무릎 굴곡 25~30도를 제안했지만, 이를 모든 사람의 안전을 보장하는 경계값으로 볼 수는 없습니다.',['S2','S4'],'정적·동적 측정 조건을 구분합니다. 뒤꿈치를 대는 동작만으로 각도를 확정하지 않습니다.'),
('C3','건강한 젊은 성인 20명을 대상으로 한 실험에서는 낮은 안장에서 무릎 굴곡과 내전 모멘트가 증가했습니다.',['S3'],'각 조건의 운동은 3분이었으며 연골 손상을 추적하거나 관절염 환자를 대상으로 한 연구가 아닙니다.'),
('C4','운동은 낮은 강도와 짧은 시간부터 시작하고, 운동 중과 운동 후의 통증 반응을 보며 서서히 늘리는 것이 기본입니다.',['S1'],'고정 RPM·30분 루틴·주간 목표를 관절염 환자의 일률적인 처방으로 제시하지 않습니다.')
]
lead='<div class="lead-quote-card" style="background:#f8fafc; border-left:4px solid #0284c7; padding:18px 22px; margin-bottom:28px; border-radius:4px;">'+paras([claims[0][1],'무릎이 불편하다면 운동을 멈추고 안장 높이·저항·운동량을 함께 살펴보세요. 통증 위치만으로 원인을 확정하거나, 특정 각도에 맞추면 안전하다고 판단해서는 안 됩니다.',claims[3][1]])+'</div>'
intro=paras(['실내자전거를 타고 나서 무릎이 시큰거리면 안장부터 내려야 할지, 운동량을 줄여야 할지 헷갈리기 쉽습니다. 중요한 것은 아픈 상태에서 설정을 바꿔가며 계속 버티지 않는 것입니다.',
'안장 높이는 점검할 항목 중 하나입니다. 페달 저항, 갑자기 늘린 운동 시간, 원래 있던 무릎 문제도 함께 고려해야 합니다. 같은 자전거를 가족이 나눠 쓴다면 타기 전에 각자에게 맞는 설정인지 확인하세요.',
'이 글에서는 안장 높이에 관한 연구가 실제로 확인한 범위와 집에서 살펴볼 항목, 운동을 줄이거나 진료를 받아야 할 상황을 구분해 설명합니다.'])
heads=['낮은 안장은 무릎에 어떤 영향을 줄까요? 연구 결과와 한계','안장 높이의 참고 각도와 집에서 확인할 항목','무릎 앞쪽과 뒤쪽 통증, 위치만으로 원인을 알 수 있을까요?','회전수 숫자보다 먼저 살펴볼 운동 강도와 시간','통증·붓기·잠김이 생겼을 때 운동을 멈추는 기준']
alts=['실내자전거 옆 의자에 앉아 무릎 상태를 살피는 여성','실내자전거 안장 기둥과 높이 조절 손잡이 확대 모습','실내자전거 옆에 서서 안장과 높이 조절 손잡이를 점검하는 여성','실내자전거 옆에 놓인 운동화와 매트, 수건, 물병','실내자전거 운동을 마치고 의자에 앉아 물을 마시며 쉬는 여성']
caps=['무릎이 불편하면 운동을 쉬고 안장 높이와 운동 강도를 함께 점검합니다.','안장 조절부의 고정 상태와 기기의 사용 설명서를 확인하세요.','안장은 자전거에서 내려 점검합니다. 사진은 개인별 적정 높이나 각도를 보여주는 기준이 아닙니다.','기기의 저항 단계나 목표 시간보다 운동 중과 운동 후의 몸 상태를 먼저 살펴봅니다.','운동 후 쉬어도 통증이나 붓기가 지속된다면 진료로 원인을 확인하세요.']
sections=[
[claims[2][1],'이 연구에서 말하는 내전 모멘트는 무릎에 작용하는 회전 효과를 나타내는 생체역학 지표입니다. 슬개대퇴 접촉 압력이나 연골 마모량을 직접 측정한 결과와는 다릅니다.',
'참가자는 건강한 젊은 성인이었고, 각 안장 조건에서 운동한 시간은 3분이었습니다. 이 결과만으로 관절염 환자의 장기적인 손상 위험이나 통증 원인을 단정할 수 없습니다.',
'따라서 안장이 너무 낮아 무릎이 답답하게 접히는지 살펴볼 수는 있지만, 낮은 안장을 곧바로 연골 손상과 연결할 필요는 없습니다. 부하의 변화와 실제 부상은 구분해서 읽어야 합니다.'],
[claims[1][1],'후속 체계적 문헌고찰은 페달을 돌리는 동안의 동적 무릎 각도 측정을 지지하면서도, 안장 높이를 바꾸는 것이 부상 위험에 미치는 영향에 대해서는 근거가 제한적이라고 설명합니다.',
'집에서는 먼저 자전거 사용 설명서의 안장 조절 범위와 고정 방법을 확인하세요. 조절할 때는 자전거에서 내리고, 다시 타기 전에 고정 장치가 잠겼는지 확인합니다.',
'자세를 살펴볼 때는 페달에 발을 안정적으로 놓을 수 있는지, 다리를 뻗으려고 골반을 좌우로 흔들거나 발끝을 억지로 내리는지 확인합니다. 불편하다면 운동을 멈추고 설정을 다시 점검하세요.',
'뒤꿈치를 페달에 대보는 힐 테스트나 무릎과 페달 축의 위치를 보는 KOPS는 피팅에 쓰이는 참고 방법입니다. 이것만으로 무릎이 정확히 특정 각도가 되거나 관절 부하가 사라진다고 판단하지 않습니다. 통증이 있거나 조절이 어렵다면 전문가의 도움을 받으세요.'],
['무릎 앞쪽이 뻐근하다고 해서 반드시 안장이 낮다는 뜻은 아닙니다. 뒤쪽이 당긴다고 안장이 높은 것으로 확정할 수도 없습니다. 통증의 위치는 점검을 돕는 정보이지 원인을 판정하는 도구가 아닙니다.',
'페달을 돌릴 때 다리가 지나치게 접히거나, 다리를 뻗기 위해 골반이 흔들리는지 살펴보세요. 안장뿐 아니라 저항과 운동 시간도 함께 확인해야 합니다.',
'조정할 때마다 이전 위치를 기억해 두고 기기의 허용 범위 안에서 조금씩 바꾸세요. 통증이 계속되면 더 높이거나 낮추는 시도를 반복하지 말고 진료를 받아 원인을 확인하는 편이 좋습니다.',
'무릎 앞쪽 불편감과 보호대에 관한 내용은 <a class="inline-pill-link" href="/posts/running-knee-brace-strap-position-anterior-knee-pain-guide.html">러닝 무릎보호대 착용 위치와 전방 무릎 통증 ↗</a>에서도 살펴볼 수 있습니다. 보호대가 통증 원인 확인을 대신하지는 않습니다.'],
[claims[3][1],'분당 회전수(RPM)만으로 운동이 안전한지 판단할 수는 없습니다. 같은 속도로 돌리더라도 저항이 다르면 필요한 힘이 달라지고, 같은 저항 단계도 기기마다 의미가 다릅니다.',
'처음부터 정해진 시간표를 채우려 하지 말고 무릎에 통증이 생기지 않는 범위에서 가볍게 시작하세요. 운동 중 불편감이 커지거나 끝난 뒤에도 남는다면 운동량을 줄이고, 증상이 이어지면 진료를 받으세요.',
'시작할 때는 천천히 몸 상태를 확인하고, 편안하게 움직일 수 있을 때만 이어갑니다. 마칠 때도 강도를 서서히 낮추세요. 최근 수술을 받았거나 재활 중이라면 담당 의료진이 정한 범위가 우선입니다.',
'근력 운동을 함께 고려한다면 <a class="inline-pill-link" href="/posts/adjustable-dumbbell-sarcopenia-lower-body-workout-guide.html">덤벨을 활용한 하체 근력 운동 안내 ↗</a>를 참고하되, 현재 통증과 운동 경험에 맞춰 동작을 선택하세요.'],
['실내자전거는 손상된 연골을 다시 자라게 하는 치료가 아닙니다. 관절염 관리는 통증을 줄이고 근력과 일상 기능을 유지하는 데 초점을 맞춥니다.',
'운동 중 날카로운 무릎 통증이 생기면 즉시 멈추세요. 운동 후 열감이나 붓기가 있으면 쉬면서 상태를 살피고, 필요하면 피부에 직접 닿지 않도록 감싼 냉찜질을 사용할 수 있습니다.',
'휴식 후에도 통증이나 부종이 지속되거나 반복된다면 진료가 필요합니다. 무릎이 걸려 펴지지 않거나 체중을 싣기 어렵다면 자전거로 풀어보려 하지 말고 신속히 진료를 받으세요. 냉찜질 때문에 진료를 미루지 마세요.',
'통증이 없는 범위의 가벼운 움직임이 궁금하다면 <a class="inline-pill-link" href="/posts/pelvic-stretching-back-pain-relief.html">골반 주변 스트레칭 안내 ↗</a>를 참고할 수 있습니다. 붓거나 잠긴 무릎을 억지로 늘리는 용도로 따라 하지 마세요.']
]
# Preserve existing figure markup and section layout; replace unsupported prose.
figures=re.findall(r'<figure\b[\s\S]*?</figure>',d['bodyHtml']); assert len(figures)==5
for i in range(5):
    figures[i]=re.sub(r'alt="[^"]*"',lambda m:'alt="'+alts[i]+'"',figures[i])
    figures[i]=re.sub(r'(<figcaption\b[^>]*>)[\s\S]*?(</figcaption>)',lambda m:m[1]+caps[i]+m[2],figures[i])
body=lead+'\n'+intro
for i in range(5): body+='\n<h2>'+heads[i]+'</h2>\n'+figures[i]+'\n'+paras(sections[i])
# Compact comparison table: observations, not diagnostic angle thresholds.
table='<div class="custom-data-table-wrap"><table class="custom-data-table"><thead><tr><th>살펴볼 상황</th><th>점검할 내용</th></tr></thead><tbody><tr><td>다리가 답답하게 접힘</td><td>안장 높이와 저항을 함께 확인</td></tr><tr><td>페달에 닿으려 골반이 흔들림</td><td>발 위치와 안장 설정을 점검</td></tr><tr><td>설정을 바꿔도 통증이 지속됨</td><td>운동을 쉬고 진료로 원인 확인</td></tr></tbody></table></div>'
body=body.replace('<h2>'+heads[2]+'</h2>',table+'\n<h2>'+heads[2]+'</h2>')
d['bodyHtml']=body
d['desc']='실내자전거를 탈 때 무릎이 불편하다면 안장 높이, 페달 저항과 운동 시간을 함께 점검하세요. 안장 각도 연구의 한계, 통증 위치만으로 원인을 단정할 수 없는 이유, 운동을 멈추고 진료가 필요한 상황을 정리했습니다.'
d['featuredCaption']='실내자전거를 타기 전 안장 설정과 자신의 몸 상태를 점검하세요.'
d['references']=[
'<a href="https://health.kdca.go.kr/healthinfo/biz/health/ntcnInfo/healthSourc/thtimtCntnts/thtimtCntntsView.do?thtimt_cntnts_sn=54">질병관리청 국가건강정보포털 — 무릎관절염, 올바로 관리하기: 나에게 맞는 관리 방법은 무엇인가요?</a>',
'<a href="https://pubmed.ncbi.nlm.nih.gov/21615188/">Bini R, Hume PA, Croft JL. Effects of bicycle saddle height on knee injury risk and cycling performance. Sports Med. 2011;41(6):463–476. PMID: 21615188. DOI: 10.2165/11588740-000000000-00000.</a>',
'<a href="https://pubmed.ncbi.nlm.nih.gov/31269871/">Cycling with Low Saddle Height is Related to Increased Knee Adduction Moments in Healthy Recreational Cyclists. Eur J Sport Sci. 2020;20(4):461–467. PMID: 31269871. DOI: 10.1080/17461391.2019.1635651.</a>',
'<a href="https://pubmed.ncbi.nlm.nih.gov/34706617/">Bini R, Priego-Quesada J. Methods to determine saddle height in cycling and implications of changes in saddle height in performance and injury risk: A systematic review. J Sports Sci. 2022;40(4):386–400. PMID: 34706617. DOI: 10.1080/02640414.2021.1994727.</a>'
]
d['faqs']=[
{'q':'안장 높이는 무릎 각도만 맞추면 되나요?','a':'25~30도는 문헌고찰에서 제안한 참고값이며 개인별 안전을 보장하는 기준은 아닙니다. 힐 테스트만으로 정확한 각도를 확인할 수는 없습니다. 기기 설명서, 발 위치, 골반 흔들림, 통증 반응을 함께 살피고 필요하면 전문 피팅이나 진료를 받으세요.'},
{'q':'무릎 앞쪽과 뒤쪽 통증으로 안장 높이를 판단할 수 있나요?','a':'통증 위치만으로 안장 높이나 질환을 확정할 수 없습니다. 안장 설정과 함께 저항, 운동량을 살펴보세요. 조절해도 통증이 계속되면 운동을 쉬고 진료를 받는 것이 좋습니다.'},
{'q':'무릎이 불편할 때 몇 RPM으로 얼마나 타야 하나요?','a':'모두에게 맞는 고정 회전수나 시간은 없습니다. 낮은 강도와 짧은 시간부터 시작해 운동 중과 운동 후 통증이 없는 범위에서 점차 늘리세요. 날카로운 통증이 생기면 멈추고, 통증·붓기가 지속되거나 무릎이 잠긴다면 진료를 받으세요.'}]
(W/'post_data.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
# Retain Naver layout, stickers, photos and copy tools; replace paragraphs in place.
nav=(W/'네이버.html').read_text(encoding='utf-8')
navheads=['| 자전거를 탔는데 무릎이 불편해졌다면','| 숫자 하나보다 내 몸의 움직임을 살펴요','| 앞쪽과 뒤쪽, 아픈 곳만으로 정하지 마세요','| 오늘 탈 수 있는 만큼 가볍게 시작해요','| 쉬어도 불편하면 확인이 필요해요']
idx=iter(navheads)
nav=re.sub(r'(<div class="naver-h2">)[\s\S]*?(</div>)',lambda m:m[1]+next(idx)+m[2],nav)
texts=[
'찬바람이 불면 거실 자전거에 눈길이 가죠.<br>밖에 나가지 않아도 움직일 수 있으니까요.<br>그런데 타고 나서 무릎이 시큰했다면 어떨까요?',
'“운동을 안 해서 그런가?” 하고 참기보다<br>일단 쉬면서 몸 상태를 살펴보세요.<br>무릎 통증을 운동이 잘됐다는 표시로 넘기지는 않는 게 좋습니다.',
'안장이 맞지 않을 수도 있지만,<br>저항이 무겁거나 갑자기 오래 탄 영향도 살펴야 해요.<br><b>한 가지 원인으로 정해놓지 않는 것</b>부터 시작해 봅시다.',
'가족이 같은 자전거를 쓰고 있다면<br>안장 위치도 누군가의 몸에 맞춰져 있을 수 있어요.<br>내 차례가 되면 그대로 타기 전에 설정을 확인해 보세요.',
'낮은 안장에서 무릎 움직임과 회전 부하가 달라졌다는 연구는 있어요.<br>다만 그 결과가 “안장을 낮추면 연골이 닳는다”는 뜻은 아닙니다.<br>불편한 설정을 점검할 이유와 손상 진단은 구분해야 합니다.',
'다리가 너무 접혀 답답한지,<br>페달에 닿으려고 몸을 좌우로 움직이는지 살펴보세요.<br>아프다면 계속 타면서 시험하지 말고 먼저 내려 쉬세요.',
'인터넷에는 정답처럼 보이는 각도가 많지요.<br><b>25~30도</b>도 연구에서 제안한 참고값이지만,<br>누구에게나 통증이 없는 자세를 보장하지는 않습니다.',
'뒤꿈치를 페달에 대보는 방법을 쓰더라도<br>그 동작 하나로 각도가 정확히 맞았다고 할 수는 없어요.<br>신발과 발 위치, 몸의 움직임도 함께 봐야 하니까요.',
'집에서는 사용 설명서를 먼저 확인하고,<br>자전거에서 내려 안장을 조절한 다음 단단히 고정하세요.<br>내 몸에 맞는지 어렵게 느껴진다면 전문가에게 도움을 받으셔도 됩니다.',
'무릎 앞이 아프면 무조건 높이고,<br>뒤가 당기면 무조건 낮추는 식으로 정하지는 마세요.<br>어디가 아픈지만으로 원인을 알 수는 없습니다.',
'설정을 조금 바꿔도 계속 불편하다면<br>높이를 바꿔가며 버티기보다 운동을 쉬어주세요.<br>반복되는 통증은 진료로 확인하는 편이 좋습니다.',
'운동한 느낌을 내려 페달을 무겁게 할 필요는 없어요.<br>처음에는 힘겹게 누르지 않아도 돌아가는 정도로<br>가볍고 짧게 시작해 보세요.',
'<mark style="background:#fef08a;">정해진 회전수보다 무릎의 반응이 먼저예요.</mark><br>기기마다 저항이 다르고 사람마다 상태도 다릅니다.<br>남이 타는 속도를 그대로 맞추지 않아도 괜찮아요.',
'시작할 때 천천히 몸 상태를 살피고,<br>편안할 때만 이어가다가 마칠 때도 서서히 강도를 낮춰요.<br>정해진 시간을 채우려 아픈 무릎을 참지는 마세요.',
'허벅지의 피로감과 무릎 관절 통증은 구분해 주세요.<br>타는 도중 날카롭게 아프면 바로 멈추고,<br>운동 뒤에도 붓거나 열감이 남는지 살펴보세요.',
'쉬어도 아프거나 붓기가 반복된다면 진료를 받아보세요.<br>무릎이 걸려 펴지지 않거나 발을 딛기 어렵다면<br>자전거로 풀어보려 하지 말고 신속히 진료를 받으세요.',
'지금 사용하는 자전거는 혼자 쓰시나요, 가족과 함께 쓰시나요?<br>다음에 타기 전에는 안장 고정 상태와 몸의 불편함부터 살펴보세요.'
]
counter=[0]
def nrep(m):
    j=counter[0];counter[0]+=1
    return m[1]+texts[j]+m[2]
nav=re.sub(r'(<p class="naver-text"[^>]*>)[\s\S]*?(</p>)',nrep,nav)
assert counter[0]==len(texts),counter
for i,alt in enumerate(alts,1):
    nav=re.sub(r'(<img\b[^>]*src="images/post0'+str(i)+r'.jpg"[^>]*alt=")[^"]*(")',lambda m:m[1]+alt+m[2],nav)
nav=nav.replace('낮은 안장과 슬개대퇴 압박 분석 (2020)','낮은 안장과 무릎 내전 모멘트 연구 (2020)')
(W/'네이버.html').write_text(nav,encoding='utf-8')
m=json.loads((W/'evidence_manifest.json').read_text(encoding='utf-8-sig'))
m['claims']=[dict(id=id,statement=s,source_ids=ids,limits=limit,statement_hash=hashlib.sha256(re.sub(r'\s+','',s).encode()).hexdigest()[:16]) for id,s,ids,limit in claims]
m['sources'][3]['authors']='Rodrigo Bini; Jose Priego-Quesada'
(W/'evidence_manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
# Correct bibliographic headers only, leaving captured abstract text intact.
raw=(W/'official_source_raw.txt').read_text(encoding='utf-8-sig')
raw=raw.replace('Bini RR, Diefenthaeler F, Hume PA','Bini R, Priego-Quesada J')
raw=raw.replace('저자: Rodrigo Bini et al.','저자: Rodrigo Bini; Jose Priego-Quesada')
(W/'official_source_raw.txt').write_text(raw,encoding='utf-8')
notes='''# 실내자전거 원고 수정 근거 — 2026-10-26
동일 대화에서 열람한 KDCA 본문과 PMID 21615188, 31269871, 34706617 초록을 재사용함. 논문 전문 전체 검토 아님.
- KDCA: 개인별 운동량·시간·횟수에 절대 기준을 정하기 어려움. 낮은 강도부터 점진적으로 늘리고 통증·열감·붓기 관찰.
- 2011 문헌고찰: 25~30도 제안은 상충하는 근거를 전제로 한 참고값. 개인별 안전 경계값이 아님.
- 2020 실험: 건강한 젊은 성인 20명, 각 조건 3분. 내전 모멘트와 움직임 측정. 연골 손상 또는 관절염 환자의 장기 경과 연구 아님.
- 2022 문헌고찰: 동적 무릎 각도 측정 지지, 부상 위험 근거 제한. Bini R, Priego-Quesada J. J Sports Sci. 2022;40(4):386–400. DOI 10.1080/02640414.2021.1994727.
- 삭제: 고정 RPM·시간 처방, 3cm/16% 이상 공포 표현, 장골능 높이 설정법, 각도별 위험 임계값, KOPS의 전단력 제거 보장.
- 유지: 기기 설명서 준수, 통증 시 중단, 지속 증상·잠김 진료 안내. 사진은 개별 피팅의 정답을 제시하지 않음.
'''
(W/'source_notes.md').write_text(notes,encoding='utf-8')
(W/'리서치.md').write_text(notes+'\n## 출처\n'+'\n'.join(s['url'] for s in m['sources'])+'\n기존 조사 장부는 _before_final_fix_20261026/리서치.md에 보존. 확인되지 않은 처방을 재사용하지 않도록 현재 근거 요약으로 대체함.\n',encoding='utf-8')
gbase=Path(r'C:\Users\lim\.codex\generated_images\01a17041-9010-7ba2-bb1c-d23261e3c486')
lp=gbase/'exec-37dff901-ae2e-4df2-b02e-b9ffc70c8f74.png'; vp=gbase/'exec-fcc38c27-28c5-45f7-8b20-209ffff49355.png'
im=Image.open(lp).convert('RGB').resize((1280,720),Image.Resampling.LANCZOS)
im.save(W/'images/post03.jpg','JPEG',quality=95,optimize=True)
Image.open(vp).convert('RGB').resize((1080,1920),Image.Resampling.LANCZOS).save(W/'vertical/post03_9x16.png','PNG',optimize=True)
plan=json.loads((W/'image_plan.json').read_text(encoding='utf-8-sig'))
for it in plan['storyboard']:
    if it['slot']=='post03.jpg': it['prompt']='Same woman standing beside parked bicycle, checking saddle and adjustment knob. Medium crop above crank, no cycling demonstration, no text.'; it['revision_reason']='페달 회전축 구조 오류를 제거하고 안장 점검 장면으로 교체'
(W/'image_plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
man=json.loads((W/'image_generation_manifest.json').read_text(encoding='utf-8'))
for a in man['assets']:
    if a['id']=='post03': a.update(landscape=str(lp),vertical=str(vp),prompt=next(x['prompt'] for x in plan['storyboard'] if x['slot']=='post03.jpg'))
(W/'image_generation_manifest.json').write_text(json.dumps(man,ensure_ascii=False,indent=2),encoding='utf-8')
db=R/'data/posts_db.json'; posts=json.loads(db.read_text(encoding='utf-8-sig'))
idx=next(i for i,p in enumerate(posts) if p['slug']==d['slug']); posts[idx]=d
db.write_text(json.dumps(posts,ensure_ascii=False,indent=2),encoding='utf-8-sig')
shutil.copy2(W/'images/post03.jpg',R/'kkuldanji_web/images/posts'/d['slugKey']/'post03.jpg')
print('Google/Naver body, FAQ, captions, evidence notes and source headers updated; post03 images replaced.')


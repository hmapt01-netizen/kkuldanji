import hashlib, json, sys
from pathlib import Path
from urllib.parse import quote
sys.stdout.reconfigure(encoding='utf-8')
W=Path(__file__).resolve().parent
sys.path.insert(0,str(W.parents[1]/'tools'))
sys.path.insert(0,str(W.parent/'codex_tools'))
from serp_collection import now, fetch_serp
from collect_research import fetch
from title_adapter import check_titles
def read(n):return json.loads((W/n).read_text(encoding='utf-8'))
def save(n,d):(W/n).write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
stamp=now(); day=stamp[:10]
audit=read('topic_serp_review.json'); rec=audit['records'][0]
notes=[
('partial','마른 체형이라는 질문에 식사·음주·금식과 여러 원인을 설명한다. 전날 음주 후 재검만을 중심으로 하지는 않는다.'),
('direct','전날 늦은 식사와 음주에 따른 변동 및 공복 재검을 직접 설명한다. 답변별 금식 시간 표현에 차이가 있고 일부는 보충제 홍보를 포함한다.'),
('direct','음주·금주 후 변화, 재검, 다른 원인, 높은 수치 구분까지 자세히 설명한다. 강한 직접 경쟁이다.'),
('direct','전날 음식과 술의 영향, 공복만으로 원인을 확정할 수 없는 이유와 반복 상승을 직접 설명한다.'),
('direct','전날 음식·음주와 공복검사, 복용약 및 다른 결과를 확인하는 항목까지 설명한다.'),
('direct','180이라는 구체적 수치에서 전날 음주와 금식 조건을 확인하고 재검하는 흐름이 있다. 모든 소량 음주 영향을 단정하는 부분은 근거로 전용하지 않는다.'),
('partial','콜레스테롤·중성지방의 차이와 공복 채혈·관리 전반. 전날 음주 뒤 재검 판단의 세부 설명은 제한적이다.'),
('partial','검진 전 물·금식·음주 일반 준비. 결과가 높은 사람의 중성지방 재검에 초점을 맞추지 않는다.'),
('partial','약 복용 중 재상승하는 대상에게 이전 검사 조건·음주·다른 질환 및 복용약을 확인하도록 한다. 첫 결과의 전날 음주와 대상이 다르다.'),
('direct','검진 전날 회와 음주 후 결과 영향 및 높게 나오면 음주 사실을 알리고 재검을 결정하는 흐름을 설명한다.')]
for doc,(coverage,note) in zip(rec['top_docs'],notes):
    doc.update(answer_coverage=coverage,review_note=note,reviewed_at=stamp)
qdocs=[rec['top_docs'][1],rec['top_docs'][9]]
questions=[fetch(d) for d in qdocs]
save('reader_questions.json',questions)
rec['review']={
 'query':rec['clean_query'],'reader_question':'중성지방이 높게 나왔는데 전날 술 때문일까? 공복 조건과 음주 사실을 어떻게 알리고 재검을 준비해야 할까?',
 'demand':[{'kind':'repeated_questions','query':rec['clean_query'],'source_url':qdocs[0]['url'],'question_urls':[d['url'] for d in qdocs], 'observed_at':stamp,'period':'2026년 8~9월 작성 질문 원문, 2026-09-15 조회','value':2,'interpretation':'전날 음주와 혈액검사 결과의 관계를 묻는 서로 다른 질문 2건. 정성적 수요이며 월간 검색량이 아니다.'}],
 'competition':'medium','competition_reason':'네이버 수집 10개 본문 모두 열람. 직접 6개, 부분 4개로 직접 답변이 이미 존재한다. 상세 의원 글도 있어 낮은 경쟁이라고 부르지 않는다.',
 'gap':'완전히 비어 있는 질문은 아니다. 서로 다른 공복 안내와 고정 금주·재검 기간 단정을 구분하고 검사기관 지시 및 기록 항목을 명확히 정리할 여지가 있다.',
 'answer_plan':'전날 술을 원인으로 단정하지 않고 ①마지막 식사·음주 ②이전 지질검사·혈당 ③복용약 기록을 챙긴다. 공복 재검 필요와 일정은 결과·개인 위험에 따라 정하며, 생활관리 평가 기간과 전날 음주의 영향 확인을 구분한다.',
 'sources':[{'url':'https://medlineplus.gov/lab-tests/triglycerides-test/','finding':'검사 전 금식 필요 여부와 시간은 의료진 지시를 확인. 지질검사 결과와 위험도 함께 해석. 원문 날짜·선택 주장 한계는 source_notes.md.','checked_at':stamp},{'url':'https://www.mayoclinic.org/diseases-conditions/high-blood-cholesterol/in-depth/triglycerides/art-20048186','finding':'2026-01-21 안내에서 음주·당류·대사상태·약물 등 다양한 관련 요인 확인. 고정 금주 후 정상화 보장 없음.','checked_at':stamp}],
 'duplication_review':'28편 제목·설명 전수 대조 및 관련 본문 대조. fasting-water-coffee-health-checkup.html은 검사 당일 물/커피·내시경이고 이번 글은 중성지방 결과 후 음주와 재검. mediterranean-diet.html(식생활), post-meal-walk-blood-sugar.html(활동)과 연결 가능하나 기존 글의 효과 수치를 새 글 근거로 전용하지 않는다.',
 'decision_reason':'사용자가 후보 3을 선택. 직접 경쟁을 인정한 중간 경쟁 주제로 진행하고 금식 조건·재검 전 기록을 선명하게 다룬다.','reviewed_at':stamp}
save('topic_serp_review.json',audit)
save('codex_target.json',{'site_fit':'core','site_fit_reason':'40~50대 검진 결과와 대사 건강, 음주 후 지질검사 재확인에 관한 생활 질문','user_topic_selection':'3','channels':{'naver':{'query':rec['clean_query'],'intent_terms':['중성지방','전날','술'],'evidence_file':'topic_serp_review.json'}}})
recentq='중성지방 재검 음주 after:2026-07-01 before:2026-09-16'
recent=fetch_serp('google',recentq)
save('google_recent_attempt.json',dict(query=recentq,**recent))
def evidence(file,excerpt):return {'evidence_file':file,'evidence_sha256':hashlib.sha256((W/file).read_bytes()).hexdigest(),'evidence_excerpt':excerpt}
searches=[dict(id='recent_google',query=recentq,url=recent['search_url'],searched_on=day,purpose='recent_discovery',channel='google',**{'from':'2026-07-01','to':day},**evidence('google_recent_attempt.json',recentq)),dict(id='validity',query='site.acc.org 2026 dyslipidemia guideline triglycerides fasting alcohol',url='https://www.google.com/search?q='+quote('site.acc.org 2026 dyslipidemia guideline triglycerides fasting alcohol'),searched_on=day,purpose='validity_check',result='웹 검색 및 ACC 2026 교육 원문 확인. 비공복 선별·조건부 공복 재검 구분. 과거 문서의 일괄 공복 단정 및 치료 알고리즘은 채택하지 않는다.',**evidence('source_notes.md','2026 이상지질혈증 지침이 2018 지침을 대체한다는 학회 원문 검색 결과 확인.')),dict(id='naver_serp',query=rec['clean_query'],url=rec['search_url'],searched_on=day,purpose='current_serp',**evidence('topic_serp_review.json',rec['clean_query']))]
sources=[]
for sid,title,url,marker,date in [
('medline','Triglycerides Test','https://medlineplus.gov/lab-tests/triglycerides-test/','Last updated December 9, 2024',None),
('mayo','Triglycerides: Why do they matter?','https://www.mayoclinic.org/diseases-conditions/high-blood-cholesterol/in-depth/triglycerides/art-20048186','Jan. 21, 2026','2026-01-21'),
('acc2026','Key Implementation Highlights from the 2026 Guideline on the Management of Dyslipidemia','https://learn.acc.org/AssetListing/Putting-the-Guidelines-into-Practice-Building-a-State-of-the-Art-Lipid-and-Cardiometabolic-Clinic-26302/Key-Implementation-Highlights-from-the-2026-Guideline-on-the-Management-of-Dyslipidemia-36096','비공복 지질 선별검사와 중성지방이 높은 경우의 공복검사를 구분',None)]:
    s=dict(id=sid,title=title,url=url,role='fact',accessed_on=day,published_on=date,date_evidence=marker,exception_reason='최근 검색 수행 후 채택한 질문 관련 공인 안내. 날짜·채택 범위와 한계는 원문 확인 기록에 명시.',validity_search_id='validity',validity_note='2026 학회 검색·교육 자료와 제한된 주장 대조. 모든 검사에 공복을 강요하거나 일정한 재검일·정상화를 보장하지 않는다.',**evidence('source_notes.md',marker))
    if not date:s['date_status']='unknown'
    sources.append(s)
for i,d in enumerate(rec['top_docs']):
    sources.append(dict(id=f'competitor{i+1}',title=d['title'],url=d['url'],role='competitor',accessed_on=day,published_on=None,date_status='unknown',exception_reason='현재 네이버 수집 결과에 노출된 경쟁 문서. 게시일을 URL이나 제목으로 추정하지 않으며 내용 비교에 사용.',current_serp_search_id='naver_serp',**evidence('topic_serp_review.json',d['review_note'])))
for i,d in enumerate(qdocs):
    sources.append(dict(id=f'question{i+1}',title=d['title'],url=d['url'],role='reader_question',accessed_on=day,published_on=None,date_status='unknown',exception_reason='해당 음주·검사 질문 실재 확인. 날짜는 답변일과 질문일 혼동을 피하여 원문 별도 확인 기록으로 보존.',validity_search_id='validity',validity_note='실제 접근 가능한 현재 질문 원문. 답변을 의학 사실 근거로 전용하지 않음.',**evidence('reader_questions.json',d['title'])))
save('freshness_review.json',dict(schema_version=1,checked_on=day,searches=searches,sources=sources,claims=[{'text':'음주 외에 당류·다른 질환·복용약 등이 중성지방과 관련되어 전날 술만으로 높은 결과의 원인을 단정하지 않는다.','source_ids':['mayo','medline']},{'text':'중성지방 검사에서 금식이 필요할 수 있으며 검사 목적과 의료진 안내에 맞춘다.','source_ids':['medline','acc2026']}]))
titles=[
'“전날 술 때문일까?” 중성지방 수치 높게 나왔다면 재검 전에 챙길 기록 3가지',
'“굶고 갔는데 왜 높지?” 중성지방 검사 금식과 전날 음주, 다시 살펴볼 준비 조건',
'“며칠 쉬면 내려갈까?” 중성지방 재검 전 금주 기간과 결과표에서 함께 볼 항목',
'중성지방 수치 높으면 전날 술만 탓해도 될까? 재검 전 놓치기 쉬운 확인 사항 3가지',
'중성지방 검사 금식, 저녁만 안 먹으면 충분할까? 재검 전 음식·음주 기록하는 법',
'중성지방 재검, 술 끊고 수치가 내려가면 끝일까? 이전 결과와 비교할 항목 3가지',
'중성지방 수치 높을 때 전날 술 확인부터, 재검 전에 챙길 식사·복용약 기록 3가지',
'중성지방 검사 금식 시간과 전날 술, 공복으로 다시 확인할 때 준비해야 할 내용',
'중성지방 재검 시기, 전날 술 마셨다면 금주 기간과 함께 확인할 결과표 항목',
'중성지방 수치 높게 나온 날, 전날 술과 늦은 식사 외에 재검 전에 확인할 3가지']
data={'naver_candidates':titles,'search_queries':['중성지방 전날 술','중성지방 검사 금식','중성지방 재검','중성지방 전날 술','중성지방 검사 금식','중성지방 재검','중성지방 전날 술','중성지방 검사 금식','중성지방 재검','중성지방 전날 술']}
for i,t in enumerate(titles,1):print(i,len(t),t)
check_titles(data,'naver')
save('naver_candidates.json',data)

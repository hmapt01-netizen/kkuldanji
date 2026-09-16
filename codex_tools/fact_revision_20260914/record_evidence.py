"""Record the source review performed in this conversation (not automatic fact checking)."""
from pathlib import Path
import json, hashlib
from urllib.parse import quote

W = Path(__file__).resolve().parent
rows = [
 ('rice_safe','NHS — Starchy foods and carbohydrates','https://www.nhs.uk/live-well/eat-well/food-types/starchy-foods-and-carbohydrates/','2023-03-15','Page last reviewed: 15 March 2023','밥은 신속히 식혀 냉장하고 24시간 안에 먹으며, 재가열 시 속까지 뜨겁게 한다. 상온에 밤새 둔 밥은 버린다.'),
 ('rice_heat','FSA — Cooking your food','https://www.food.gov.uk/safety-hygiene/cooking-your-food',None,'Last updated: 12 June 2024','전자레인지에서는 가장자리와 가운데가 다르게 가열될 수 있어 저어 주고 전체가 뜨거운지 확인한다.'),
 ('rice_study','Sonia et al. — Effect of cooling of cooked white rice on resistant starch content and glycemic response','https://apjcn.qdu.edu.cn/24_4_24.pdf',None,'Asia Pac J Clin Nutr 2015;24(4):620-625','2015년 백미 냉각 연구는 냉장 후 재가열한 밥도 시험했다. 특정 혼합 잡곡밥의 노화 억제나 혈당 개선 보장을 입증한 연구가 아니다.'),
 ('rice_oil','ACS — New low-calorie rice could help cut rising obesity rates','https://www.acs.org/pressroom/newsreleases/2015/march/new-low-calorie-rice-could-help-cut-rising-obesity-rates.html','2015-03-23','March 23, 2015','2015년 학회 발표 소개의 오일은 코코넛유다. 올리브유를 넣는 국내 잡곡밥의 효과로 일반화하지 않는다.'),
 ('coffee_study','Morck et al. — Inhibition of food iron absorption by coffee','https://pubmed.ncbi.nlm.nih.gov/6402915/',None,'1983 Mar;37(3):416-20','커피를 식전 1시간에 마신 경우와 식후 1시간에 마신 경우의 결과가 다르다. 식후 1시간에도 식사와 함께 마셨을 때와 같은 정도의 억제가 관찰됐다.'),
 ('iron','NIH ODS — Iron, Health Professional Fact Sheet','https://ods.od.nih.gov/factsheets/Iron-HealthProfessional/',None,'Updated: September 4, 2025','헴철과 비헴철을 구분한다. 비타민 C는 비헴철 흡수를 돕고 일부 폴리페놀은 억제한다. 한 끼 흡수 변화와 장기적인 철분 상태를 구분한다.'),
 ('iron_medicine','NHS — About ferrous sulfate','https://www.nhs.uk/medicines/ferrous-sulfate/about-ferrous-sulfate/',None,'발행일 미확인','황산철 복용 뒤 차·커피 등을 마시기까지 2시간 간격을 안내한다. 모든 비타민의 복용법으로 확대하지 않는다.'),
 ('reflux','NIDDK — Eating, Diet, & Nutrition for GER & GERD','https://www.niddk.nih.gov/health-information/digestive-diseases/acid-reflux-ger-gerd-adults/eating-diet-nutrition',None,'Last Reviewed July 2020','일부 사람에게 커피와 카페인이 역류 증상과 관련된다. 개인별로 증상을 악화시키는 음식을 줄이거나 피하도록 상담한다.'),
 ('glucose_tests','NIDDK — Diabetes Tests & Diagnosis','https://www.niddk.nih.gov/health-information/diabetes/overview/tests-diagnosis',None,'발행일 미확인','비임신 성인의 공복혈당 100~125와 당화혈색소 5.7~6.4는 전단계 범위다. 공복검사는 최소 8시간 금식하며 당뇨병 판단에는 보통 확인 검사를 쓴다.'),
 ('glucose_confirm','NIDDK — Diabetes & Prediabetes Tests','https://www.niddk.nih.gov/health-information/professionals/clinical-tools-patient-management/diabetes/diabetes-prediabetes',None,'발행일 미확인','가정용 측정기는 확진용 검사를 대체하지 않는다. 검사 종류의 결과가 다르면 기준을 넘은 검사를 다시 확인한다.'),
 ('dpp','NIDDK — Diabetes Prevention Program (DPP)','https://www.niddk.nih.gov/about-niddk/research-areas/diabetes/diabetes-prevention-program-dpp',None,'발행일 미확인','생활습관 중재군의 약 3년간 제2형 당뇨병 발생 위험은 위약군 대비 58% 낮았다. 15년 결과나 개인의 정상화 확률과 동일하지 않다.'),
 ('ada','ADA — Prevention or Delay of Diabetes and Associated Comorbidities: Standards of Care in Diabetes—2026','https://diabetesjournals.org/care/article/49/Supplement_1/S50/163924/3-Prevention-or-Delay-of-Diabetes-and-Associated',None,'Diabetes Care Volume 49 Supplement 1, January 2026','공식 검색 결과의 권고 3.3: 과체중·비만 고위험 성인의 초기 체중 5~7% 이상 감량과 주 150분 이상 중강도 활동. 권고 3.7: 일부 고위험 성인에게 메트포르민 고려. 웹 원문 열기는 오류여서 공식 검색 결과의 해당 권고 범위만 사용.'),
 ('lifestyle','NIDDK — Healthy Living with Diabetes','https://www.niddk.nih.gov/health-information/diabetes/overview/healthy-living-with-diabetes',None,'발행일 미확인','식사 구성·양·시점과 활동을 함께 조정한다. 인슐린이나 일부 약을 쓰는 경우 끼니를 거르거나 운동할 때 저혈당 위험을 고려해야 한다.'),
 ('produce','FDA — Selecting and Serving Produce Safely','https://www.fda.gov/food/buy-store-serve-safe-food/selecting-and-serving-produce-safely',None,'발행일 미확인','멍든 부위는 잘라내고 썩은 것은 버린다. 흐르는 물로 세척하며 세척이 모든 세균을 없애지는 않는다. 껍질을 벗기기 전에도 씻는다. 절단 농산물은 냉장한다.'),
 ('produce_steps','FDA — 7 Tips for Cleaning Fruits, Vegetables','https://www.fda.gov/consumers/consumer-updates/7-tips-cleaning-fruits-vegetables',None,'발행일 미확인','손 씻기, 흐르는 물에서 부드럽게 문지르기, 단단한 농산물용 깨끗한 솔, 깨끗한 수건으로 물기 제거를 안내한다.'),
 ('mold','USDA FSIS — Molds on Food: Are They Dangerous?','https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/molds-food-are-they-dangerous',None,'Last Updated: Aug 22, 2013','공식 검색 결과의 표: 복숭아 등 수분 많은 연한 과채류에 곰팡이가 있으면 버린다. 표면 아래도 오염될 수 있다. 웹 원문 403으로 검색에 제공된 표 범위만 사용.'),
]
queries = [
 ('recent','recent_discovery','site:mfds.go.kr 2026 7월 8월 과일 세척','최근 범위의 적합한 세척 기준을 찾지 못해 기존 FDA 안전 지침을 사용. 무관한 계절 통계는 제외.'),
 ('valid','validity_check','site.diabetesjournals.org 2026 Standards Care prevention delay diabetes 150 5 7%','2026 ADA 공식 검색 결과의 수치와 NIDDK 안내를 대조. 자료별 보완: FSA 재가열, NHS 황산철, FDA 세척, 2015 냉각 연구, 1983 커피 논문을 원문 또는 명시한 공식 검색 결과 범위에서 확인.'),
]
notes=['# 2026년 9월 14일 기존 4편 근거 재검토','조회일과 발행일을 구별한다. 아래는 실제 웹 도구 확인 기록의 한국어 요약이며 자동 수집 원문이 아니다. 최신 자료의 부재는 모든 최신 자료를 검색했다는 뜻이 아니다.']
for sid, purpose, q, result in queries:
 notes += [f'## 검색 {sid}',q,result]
for sid,title,url,date,marker,note in rows:
 notes += [f'## {sid}',title,url,marker,note]
notes += ['# FAQ 수정 범위','밥: 배합 비율의 개인차, 첨가물 의무 아님, 상온 방치 밥. 커피: 음료별 흡수율을 동일시하지 않음, 황산철 복용 간격, 피로만으로 철분 부족 단정하지 않음. 혈당: 약물 여부·검사 준비·검사 간 차이. 과일: 세척 첨가제의 만능 효과 배제, 멍과 부패 구분, 세척 완료 포장 표시.']
e='\n\n'.join(notes)+'\n'
(W/'리서치.md').write_text(e,encoding='utf-8')
h=hashlib.sha256((W/'리서치.md').read_bytes()).hexdigest()
def proof(excerpt):return dict(evidence_file='리서치.md',evidence_sha256=h,evidence_excerpt=excerpt)
searches=[]
for sid,purpose,q,result in queries:
 row=dict(id=sid,purpose=purpose,query=q,url='https://www.google.com/search?q='+quote(q),searched_on='2026-09-14',result=result,**proof(q))
 if purpose=='recent_discovery': row.update(channel='google', **{'from':'2026-07-01','to':'2026-09-14'})
 searches.append(row)
sources=[]
for sid,title,url,date,marker,note in rows:
 sources.append(dict(id=sid,title=title,url=url,role='fact',accessed_on='2026-09-14',published_on=date,date_status='known' if date else 'unknown',date_evidence=marker,exception_reason='기존 오류를 고치는 데 직접 필요한 연구 또는 현재 제공 중인 공공기관 안내. 조회일을 최신 발표일로 바꾸지 않는다.',validity_search_id='valid',validity_note=note,**proof(note)))
data=dict(schema_version=1,checked_on='2026-09-14',searches=searches,sources=sources,claims=[dict(text=r[5],source_ids=[r[0]]) for r in rows])
(W/'freshness_review.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Source review recorded:',len(rows))

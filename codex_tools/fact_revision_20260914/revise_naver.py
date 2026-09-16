from pathlib import Path
from lxml import html, etree
from html import escape
import json
ROOT=Path(__file__).resolve().parents[2];W=Path(__file__).resolve().parent
def para(t):return '<p>'+t+'</p>'
def pic(src,cap):return '<div class="img-wrap"><img src="'+src+'" alt="'+cap+'" style="width:100%;height:auto;border-radius:10px;"><div class="img-caption">'+cap+'</div></div>'
data=[dict(prefix='01_',title='잡곡밥 처음 짓는 날, 렌틸콩·귀리는 얼마나 섞을까? 남은 밥 데울 때도 확인하세요',intro=[
 '몸에 좋다는 잡곡을 사놓고도 밥솥 앞에서 망설일 때가 있죠.',
 '콩을 많이 넣어야 할지, 소주나 기름까지 넣어야 할지 정보가 많아서 더 헷갈립니다.',
 '오늘은 재료를 더 사기 전에 확인할 것부터 정리해 보겠습니다.',
 '<mark>정해진 배합보다 내 식사량과 안전한 보관을 먼저 살펴보세요.</mark>'
 ],sections=[('내가 먹기 편한 밥부터 시작합니다',[
 '현미나 귀리 같은 통곡물은 식이섬유를 더하는 선택이 될 수 있습니다.',
 '영국 NHS도 통곡물을 이런 관점에서 소개하지만, 백미를 먹으면 곧바로 몸이 나빠진다는 뜻은 아닙니다.',
 '렌틸콩을 정해진 비율만큼 넣어야 한다고 부담 갖기보다, 집에서 먹던 양과 재료를 먼저 돌아보세요.',
 '잡곡으로 바꿨다는 이유로 밥을 더 수북하게 담을 필요도 없습니다.',
 '곡물 포장에 적힌 물 양과 취사 안내를 읽고, 갖고 있는 밥솥의 사용법에 맞춰 준비하는 편이 낫습니다.',
 '먹고 나서 불편했다면 재료와 양을 적어 두세요.',
 '한 가지 성분이 문제라고 스스로 결론내리기보다, 반복되는 불편은 의료진과 상의할 수 있습니다.',
 '남에게 맞는 비율을 그대로 지키는 것보다 내가 꾸준히 먹을 수 있는 식탁을 찾는 과정입니다.'
 ]),('소주와 기름을 넣기 전에 볼 점',[
 '소주를 넣어야 잡곡밥이 건강해진다는 안내는 이번 원고에서 제외했습니다.',
 '취사만 하면 알코올 걱정이 사라진다고 설명할 근거도 확인되지 않았습니다.',
 '기름을 넣은 밥에 관한 미국화학학회 자료는 2015년 학회 발표를 소개한 글입니다.',
 '그때 다룬 재료는 코코넛유였고, 사람을 대상으로 한 후속 연구도 필요하다고 설명했습니다.',
 '이 내용을 집에서 쓰는 올리브유와 혼합 잡곡에 그대로 적용해 같은 결과를 기대할 수는 없습니다.',
 '따라서 밥물에 기름을 붓는 사진은 조리 장면의 예시로만 봐주세요.',
 '첨가물을 챙기는 것보다 재료가 알맞게 익었는지, 평소 먹는 양에 맞게 담았는지부터 확인하면 좋겠습니다.',
 '밥만 바꾸면 식후 졸음이나 혈당 고민이 해결된다는 식의 약속도 내려놓겠습니다.'
 ]),('남겨 둔 밥은 속까지 데웁니다',[
 '찬밥 속 전분을 다룬 연구가 있다고 해서, 일부러 덜 데워 먹어야 하는 것은 아닙니다.',
 '2015년 발표된 백미 연구에도 냉장한 뒤 다시 가열해서 먹는 조건이 포함돼 있습니다.',
 '밥을 다룰 때는 연구의 조리 조건보다 가정용 식품안전 안내를 먼저 따르는 편이 낫습니다.',
 '영국 NHS의 밥 보관 안내를 보면, 조리 후 한 시간 이내 냉장과 하루 이내 섭취를 함께 확인할 수 있습니다.',
 '<u>먹을 때는 가운데까지 뜨겁게 데우고, 데운 밥을 남겨 다시 가열하는 일은 피하세요.</u>',
 '영국 FSA는 전자레인지에서 고르게 데워지도록 중간에 저어 주는 방법도 안내합니다.',
 '상온에서 밤을 보낸 밥은 다시 데우면 괜찮겠지 하고 먹지 마세요.',
 'NHS는 이 경우 폐기를 안내합니다.',
 '보관을 잘못해서 생긴 독소까지 데우는 과정으로 없앨 수 있는 것은 아니기 때문입니다.',
 '밥을 담을 때 먹을 만큼 나누고, 남은 것은 바로 정리할 준비를 해두면 덜 헷갈립니다.'
 ])],caps=['밥그릇에 담아 둔 잡곡 한 끼','배합 전에 준비한 여러 곡물','기름을 더하는 장면은 조리 예시','반찬과 밥을 함께 놓은 식사','차 한 잔과 함께하는 휴식'],refs=['NHS, Starchy foods and carbohydrates — 2023년 검토된 통곡물과 밥 보관 안내.','FSA, Cooking your food — 2024년 갱신된 음식 재가열 안내.','Sonia 외, Effect of cooling of cooked white rice on resistant starch content and glycemic response — 2015년 연구.','ACS, New low-calorie rice could help cut rising obesity rates — 2015년 코코넛유 이용 발표 소개.'],ending='여러분은 먹을 만큼만 밥을 짓는 편인가요, 남길 양까지 미리 나누는 편인가요?',tags='#잡곡밥 #렌틸콩 #귀리 #밥짓기 #잡곡밥비율 #밥냉장보관 #밥재가열 #남은밥 #식사량 #식사습관 #에디터혀니 #꿀단지'),
dict(prefix='07_',title='점심 먹고 커피 마셨는데 철분이 걱정된다면? 한 시간 기다리기보다 먼저 확인할 것',intro=[
 '점심을 먹자마자 커피를 들고 나왔는데, 영양분을 놓치는 건 아닌지 걱정될 때가 있죠.',
 '그렇다고 식사를 다시 하거나 영양제를 더 챙길 일은 아닙니다.',
 '식사와 음료를 함께 살피는 경우와 철분제를 복용하는 경우를 나눠 보겠습니다.',
 '<mark>모두에게 같은 대기 시간을 정하기보다 내 식사와 약부터 확인하는 것이 먼저입니다.</mark>'
 ],sections=[('한 잔 마셨다고 식사가 헛일은 아닙니다',[
 '음식 속 철분은 형태에 따라 흡수에 영향을 받는 정도가 다릅니다.',
 '미국 NIH 영양보충제국은 식물성 식품에 들어 있는 철분을 비헴철로 설명합니다.',
 '육류나 해산물에는 헴철과 비헴철이 함께 들어 있습니다.',
 '커피를 다룬 연구에서 비헴철의 흡수가 줄어든 결과가 있다고 해서, 점심의 모든 영양분이 사라진 것은 아닙니다.',
 '단백질과 비타민까지 한꺼번에 잃었다고 생각할 필요는 없다는 뜻입니다.',
 '오후에 피곤하다는 이유만으로 커피 때문에 철분이 부족해졌다고 결론내리기도 어렵습니다.',
 '피로가 계속된다면 식사와 수면 같은 생활 이야기를 의료진에게 전하고 필요한 확인을 받으세요.',
 '불안해서 철분제 양부터 늘리는 방법은 피하는 편이 좋겠습니다.'
 ]),('시계의 한 시간만으로 판단하지 마세요',[
 '기존에 소개한 AJCN의 커피 논문은 1983년에 발표된 자료입니다.',
 '내용을 다시 대조하니, 밥을 먹기 한 시간 전에 마신 경우와 먹은 뒤 한 시간에 마신 경우의 결과가 달랐습니다.',
 '식후 한 시간이 지난 뒤에도 식사와 같이 마셨을 때와 비슷한 정도의 흡수 억제가 관찰됐습니다.',
 '그래서 한 시간만 기다리면 철분 흡수가 원래대로 돌아온다는 안내는 사용하지 않겠습니다.',
 '당시의 식사 구성과 커피 농도에 따른 결과를, 우리 집 모든 음료에 같은 수치로 붙일 수도 없습니다.',
 '디카페인이나 라떼도 이름만 보고 영향이 없다고 판단하기 어렵습니다.',
 '반대로 일반 커피와 차이가 없다고 단정할 근거 역시 이번에는 확인하지 못했습니다.',
 '숫자로 된 시간표를 외우기보다, 철분 제품을 먹는 날인지부터 떠올려 보세요.'
 ]),('복용 안내와 속의 반응을 함께 봅니다',[
 'NHS의 황산철 안내에는 약을 먹은 뒤 차나 커피까지 두 시간 간격을 두라는 설명이 있습니다.',
 '황산철은 철분 제품의 성분명이며, 이 안내를 모든 비타민에 적용하는 것은 아닙니다.',
 '집에 있는 포장에서 성분을 확인하고, 복용 중인 다른 약이 있다면 약사에게 함께 알려주세요.',
 '보통 약을 언제 먹고 커피는 언제 마시는지 적어 가면 시간 조정을 상의하기 쉽습니다.',
 '커피 때문에 약을 빼먹거나 양을 바꾸지는 마세요.',
 '속이 쓰리거나 신물이 올라오는 일이 반복되는 분은 음료를 마신 뒤의 반응도 살펴보세요.',
 'NIDDK는 일부 사람에게 커피와 카페인이 역류 증상을 악화시킬 수 있다고 안내합니다.',
 '정해진 시간만 기다렸으니 괜찮다고 참기보다, 양을 줄이거나 쉬었을 때 달라지는지 살피고 상담할 수 있습니다.',
 '식사 뒤 커피를 잠시 미루고 싶다면 물로 입가심하는 간단한 선택도 있습니다.',
 '물 한 잔에도 특별한 흡수 효과를 기대하기보다 편하게 마실 음료로 생각하시면 됩니다.'
 ])],caps=['커피를 들고 점심 산책을 나온 모습','샐러드 옆에 곁들인 차가운 음료','마신 뒤 느껴지는 불편을 돌아보는 순간','탕비실에서 커피를 내리는 일상','커피 대신 물로 입가심하는 모습'],refs=['AJCN, Inhibition of food iron absorption by coffee — 1983년 식사 시점별 비헴철 연구.','NIH ODS, Iron Health Professional Fact Sheet — 2025년 갱신된 철분 형태와 흡수 안내.','NHS, About ferrous sulfate — 황산철 복용 뒤 차와 커피의 간격 안내.','NIDDK, Eating, Diet, & Nutrition for GER & GERD — 2020년 검토된 개인별 역류 음식 안내.'],ending='점심 뒤에는 커피를 바로 마시는 편인가요, 잠깐 다른 일을 하고 마시는 편인가요?',tags='#식후커피 #커피시간 #철분흡수 #철분제 #황산철 #점심커피 #디카페인 #속쓰림 #식사기록 #음료습관 #에디터혀니 #꿀단지'),
dict(prefix='11_',title='검진표 공복혈당 100~125가 걱정될 때, 당화혈색소와 식사 기록부터 챙겨보세요',intro=[
 '결과표에 빨간 주의 표시가 있으면 평소 먹던 밥부터 걱정되죠.',
 '하지만 한 번 나온 숫자만으로 앞으로의 경과를 미리 정할 수는 없습니다.',
 '정해진 기간 안에 숫자를 되돌리겠다는 목표보다, 다음 상담에 가져갈 정보를 차근차근 준비해 보세요.',
 '<mark>공복혈당뿐 아니라 다른 검사 결과와 평소 생활을 함께 보는 과정입니다.</mark>'
 ],sections=[('서로 다른 두 검사 값을 살펴봅니다',[
 'NIDDK가 소개한 비임신 성인의 기준에서 공복혈당 100~125mg/dL는 전단계에 해당하는 구간입니다.',
 '당화혈색소는 5.7~6.4% 구간을 전단계로 봅니다.',
 '두 항목이 모두 높아야만 살펴볼 필요가 생기는 것은 아닙니다.',
 '공복혈당은 검사한 때의 수치이고, 당화혈색소에는 최근 몇 달의 평균적인 상태가 반영됩니다.',
 '그래서 한쪽은 정상 구간인데 다른 쪽에 주의 표시가 있을 수 있습니다.',
 '이때는 어떤 검사를 다시 볼지 의료진에게 물어보세요.',
 '집에서 재는 기기의 숫자만으로 의료기관의 검사 판단을 대신할 수도 없습니다.',
 '검진 당일 몸이 아팠는지, 평소와 다르게 약을 먹었는지 같은 정보도 적어 두면 상담에 도움이 됩니다.',
 '숫자만으로 췌장이 얼마나 지쳤는지 계산하거나, 야식 하나 때문이라고 결론짓지는 마세요.'
 ]),('식사와 활동은 함께 조정합니다',[
 '먹는 순서 하나를 바꿨다고 다음 날 아침 수치까지 일정하게 달라지는 것은 아닙니다.',
 '밥과 반찬, 간식, 달게 마시는 음료까지 평소 모습을 기록해 보세요.',
 '2026년 미국당뇨병학회 예방 권고에는 과체중·비만이 있는 고위험 성인의 체중을 처음보다 5~7% 이상 줄여 유지하는 목표가 나옵니다.',
 '이 내용을 마른 사람까지 똑같이 감량해야 한다는 뜻으로 받아들이지는 마세요.',
 '같은 권고의 활동 목표는 일주일에 중강도 운동 150분 이상입니다.',
 '처음부터 힘든 운동을 몰아서 하기보다, 현재 체력에서 가능한 활동을 나누어 시작할 수 있습니다.',
 '짧은 산책을 시작해도 좋지만 몇 분 걸으면 수치가 정상으로 바뀐다고 약속할 수는 없습니다.',
 '식사를 거르거나 운동량을 늘릴 때 주의가 필요한 약도 있으므로, 복용 중이라면 의료진과 먼저 조정하세요.'
 ]),('다음 확인 날짜를 정해 두세요',[
 '자주 인용되는 58%라는 숫자도 개인의 성공 확률은 아닙니다.',
 'NIDDK의 DPP 설명에서는 약 3년 동안 생활습관 중재를 받은 집단의 제2형 당뇨병 발생 위험이 위약 집단보다 58% 낮았다고 합니다.',
 '걷기나 식사 순서 한 가지만의 결과가 아니고, 모든 사람의 수치가 되돌아온다는 의미도 아닙니다.',
 '일부 고위험 성인은 약을 고려할 수 있다는 ADA 안내도 있으므로, 약 없이 해야 성공이라는 부담은 갖지 마세요.',
 '식사 시간을 정리하더라도 밤에 일정 시간을 굶으면 아침 수치가 내려온다고 단정할 수는 없습니다.',
 '검사 전 준비와 평소 식사 계획은 따로 확인하는 편이 좋습니다.',
 '공복혈당 검사는 최소 여덟 시간의 금식이 안내되지만, 다른 검사가 함께 있으면 물과 약에 관한 준비가 달라질 수 있습니다.',
 '좋은 결과를 얻으려고 임의로 더 오래 굶기보다 검진기관이 알려준 방법을 따르세요.',
 '다음 검사 날짜와 상담할 항목을 기록해 두고, 그 사이 실천할 작은 일을 골라보면 좋겠습니다.'
 ])],caps=['걷기 좋은 길에서 보내는 오후','검진표를 천천히 읽어 보는 모습','채소를 곁들여 먹는 한 끼','여러 반찬을 나누어 차린 식사','식사를 마친 뒤 쉬어 가는 시간'],refs=['NIDDK, Diabetes Tests & Diagnosis / Diabetes & Prediabetes Tests — 검사별 기준과 결과 확인 안내.','ADA, Prevention or Delay of Diabetes and Associated Comorbidities: Standards of Care in Diabetes—2026 — 개인별 생활 관리와 약물 고려.','NIDDK, Diabetes Prevention Program (DPP) — 약 3년간 집단 간 발생 위험 비교.','NIDDK, Healthy Living with Diabetes — 식사·활동과 복용약에 따른 주의 안내.'],ending='다음 확인까지 식사 기록부터 시작할까요, 평소 걷는 시간을 먼저 적어볼까요?',tags='#공복혈당 #당화혈색소 #공복혈당100 #공복혈당125 #검진결과 #혈당관리 #식사기록 #운동기록 #검사준비 #생활습관 #에디터혀니 #꿀단지')]
for item in data:
 f=next((ROOT/'꿀단지 네이버').glob(item['prefix']+'*/*네이버블로그용.html'))
 backup=W/'before'/f.relative_to(ROOT);backup.parent.mkdir(parents=True,exist_ok=True)
 if not backup.exists():backup.write_bytes(f.read_bytes())
 raw=backup.read_text(encoding='utf-8-sig');tree=html.fromstring(raw)
 target=tree.xpath('//*[@id="naverContent" or @id="article-body"]')[0]
 images=target.xpath('.//img/@src')
 # Remove the AI-generated document/diagnostic chart pretending to be an official KDA publication.
 if item['prefix']=='11_':images=[s for s in images if not s.endswith('post02.jpg')]
 assert len(images)==len(item['caps'])
 old_titles=[el.text_content() for el in tree.xpath('//title|//h1')]
 for el in tree.xpath('//title'):el.text=item['title']
 if item['prefix']=='01_':
  for el in tree.xpath('//div[@class="header-bar"]//h2'):el.text=item['title']
 assert 40<=len(item['title'])<=60,(len(item['title']),item['title'])
 out='<h1>'+item['title']+'</h1>'+''.join(para(t) for t in item['intro'])+pic(images[0],item['caps'][0])
 for i,(heading,paras) in enumerate(item['sections']):
  out+='<h2>| '+heading+'</h2>'+''.join(para(t) for t in paras)+pic(images[i+1],item['caps'][i+1])
 out+=pic(images[-1],item['caps'][-1])+para('오늘은 확인한 내용 중 내 생활에 맞는 작은 실천부터 골라보세요.')+para(item['ending'])+para('댓글로 평소 습관을 편하게 남겨주세요.')
 out+='<div class="ref-box" style="font-size:0.84rem;color:#64748b;margin-top:28px;">'+para('자료 대조·수정일 2026년 9월 14일. 아래 연도는 원문 발표·검토 시점입니다.')+''.join(para(escape(x)) for x in item['refs'])+'</div>'
 out+='<p id="hashtagText">'+item['tags']+'</p>'
 for child in list(target):target.remove(child)
 target.text=None
 out=out.replace('상담','상의').replace('예방 권고','관리 권고').replace('정리하더라도','정리해도')
 for el in html.fragments_fromstring(out):target.append(el)
 for el in tree.xpath('//button'):
  if el.text and '본문 전체 복사하기' in el.text:el.text='📋 본문 전체 복사하기'
 # Preserve existing copy handlers; the blood-glucose package already has hashtag controls.
 f.write_text('<!DOCTYPE html>\n'+etree.tostring(tree,encoding='unicode',method='html'),encoding='utf-8')
 print(f.relative_to(ROOT),len(item['title']),len(' '.join(target.text_content().split())))
print('Three existing Naver packages synchronized; fruit package not found. No Naver publication performed.')

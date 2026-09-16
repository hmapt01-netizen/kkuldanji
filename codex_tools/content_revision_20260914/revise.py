"""Bounded revision of two existing articles; no publication or shared-rule edits."""
from pathlib import Path
import copy, hashlib, html, json, re, shutil
from lxml import html as lh

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
MEAT=ROOT/'2026-09-14-추석-고기-선물-수령안전'
NOSE=ROOT/'2026-09-13-환절기-비염-스프레이-부작용'
DB=ROOT/'data/posts_db.json'
NP=ROOT/'꿀단지 네이버/14_환절기_비염_스프레이_부작용/14_환절기_비염_스프레이_부작용_네이버블로그용.html'
backup=OUT/'before';backup.mkdir(exist_ok=True)
for f in [DB,MEAT/'google_draft.md',MEAT/'post_data.json',MEAT/'google_final_preview.html',NP]:
    dst=backup/f.relative_to(ROOT);dst.parent.mkdir(parents=True,exist_ok=True)
    if not dst.exists():shutil.copy2(f,dst)
rows=json.loads((backup/DB.relative_to(ROOT)).read_text(encoding='utf-8-sig'))
original=copy.deepcopy(rows)
meat=next(p for p in rows if p['slug']=='chuseok-meat-delivery-thawing-safety.html')
nose=next(p for p in rows if p['slug']=='nasal-spray-rebound-rhinitis-5day-rule.html')
def parse(s):return lh.fragment_fromstring(s,create_parent='div')
def inner(n):return (n.text or '')+''.join(lh.tostring(c,encoding='unicode') for c in n)
def p(s):return '<p style="font-size:1.02rem;line-height:1.9;color:#334155;margin-bottom:22px;">'+s+'</p>'
def paras(s):return ''.join(p(x.strip()) for x in s.strip().split('\n\n'))
def save(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Keep food-safety claims and approved image placements; remove repeated prose.
g=(backup/(MEAT/'google_draft.md').relative_to(ROOT)).read_text(encoding='utf-8')
tree=parse(meat['bodyHtml'])
remove=[
'문 앞에 언제 도착했고, 언제 상자를 열었으며, 냉장고에는 언제 넣었는지를 먼저 떠올려 보세요.',
'예를 들어 어제 도착한 택배를 오늘 저녁에 발견했다면, ‘오늘 받았다’고만 적지 말고 알림에 나온 도착 시각도 함께 남겨두세요.',
'직접 본 상태와 알 수 없는 부분을 나눠 적어야, 주문한 곳에 상황을 설명할 때도 혼동이 줄어듭니다.',
'여기서 약 4.4℃는 미국 안내의 화씨 온도를 섭씨로 바꾼 값입니다.',
'아이스팩을 확인했다면 이제 고기 쪽으로 눈을 돌려, 포장마다 어떤 상태로 도착했는지 살펴봅니다.',
'이미 냉장고나 냉동실에 넣었다면, 넣기 전 상태와 보관한 시각도 함께 기록해 두세요.',
'포장에 적힌 취급 방법이 헷갈린다면, 상품명과 보관 표시가 보이는 사진을 준비해 주문한 곳에 확인하세요.',
'다만 제품의 보관 방법을 물어보는 것과, 따뜻하게 방치된 고기를 먹어도 된다는 판단은 구분해야 합니다.'
]
for text in remove:
    nodes=[e for e in tree.findall('p') if e.text_content().strip()==text]
    assert len(nodes)==1,text
    tree.remove(nodes[0]);assert text in g;g=g.replace(text+'\n\n','',1)
ending='''추석 고기 선물을 받을 예정이라면, 도착 알림을 켜두고 냉장고에 보관할 자리를 미리 마련해 두세요.

식약처는 오랫동안 자리를 비워 받기 어려운 경우에는 냉장축산물 주문을 피하도록 안내합니다.

선물을 보내기 전에 ‘언제 집에서 받을 수 있어요?’라고 물어보고, 받는 분의 일정에 맞춰 보내면 좋겠습니다.

상태가 이상하면 상자·고기 포장 사진에 도착·개봉 시각을 덧붙여 주문한 곳에 전달하세요.

이미 냉장고에 넣었다면 넣기 전 상태도 알리되, 재지 않은 온도는 추측해서 적지 않습니다.

이 기록은 상황을 설명하는 데 도움이 되지만, 교환·환불 여부는 주문한 곳의 처리 절차를 확인해야 합니다.

함께 준비한 과일도 있다면 [과일 세척할 때 확인할 점](https://honeyjar.co.kr/posts/fruit-washing-liver-health.html)을 이어서 살펴보세요.

고마운 마음으로 받은 선물인 만큼, 오래 두기 전에 챙겨 가족과 편안한 식사를 나누시길 에디터 혀니가 응원합니다.'''
sec6=tree.xpath('./h2[@id="sec6"]')[0]
for node in list(sec6.itersiblings()):
    if node.tag=='p':tree.remove(node)
for line in ending.split('\n\n'):
    line=re.sub(r'\[([^]]+)\]\((https?://[^)]+)\)',r'<a href="\2">\1</a>',line)
    tree.append(lh.fragment_fromstring(p(line)))
g=g[:g.index('## 받는 날의 준비가 선물을 지켜줘요')]+ '## 받는 날의 준비가 선물을 지켜줘요\n\n'+ending+'\n\n'+g[g.index('<!-- REFERENCES -->'):]
meat['bodyHtml']=inner(tree)
meat['relatedSlug']='fruit-washing-liver-health.html'
(MEAT/'google_draft.md').write_text(g,encoding='utf-8')
save(MEAT/'post_data.json',meat)

# Retain the existing five images, TOC anchors, table/card and FAQ separation.
old=parse(nose['bodyHtml'])
imgs=[lh.tostring(e,encoding='unicode') for e in old.xpath('./div[.//img]')]
assert len(imgs)==5
imgs[3]=imgs[3].replace('코 바깥쪽 45도 방향으로','코 바깥쪽 방향으로')
headings=['코 스프레이는 성분부터 확인하세요','사용 기간은 제품 안내와 함께 보세요','분사할 때는 코 가운데를 피하세요','끊기 어렵다면 사용 기록을 챙기세요','코세척은 물과 용기를 먼저 챙겨요']
toc='<nav class="toc-box" style="padding:20px;border:1px solid #e2e8f0;border-radius:12px;margin:30px 0;"><strong>목차</strong><ul>'+''.join(f'<li><a href="#sec{i}">{h}</a></li>' for i,h in enumerate(headings,1))+'</ul></nav>'
body='<div class="lead-quote-card" style="background:#f8fafc;border-left:4px solid #f59e0b;padding:18px 20px;margin-bottom:28px;">코막힘 스프레이는 성분과 사용 기간을 함께 확인하세요.<br><small>식약처 의약품안전나라 제품 안내를 바탕으로 정리한 핵심 요점</small></div>'
body+=paras('''환절기 코막힘 때문에 비염 스프레이를 찾았는데, 요즘은 뿌려도 금방 다시 답답해지시나요?

잠깐 숨쉬기가 편해지면 침대 옆이나 가방에 넣어두고, 코가 막힐 때마다 손이 가기 쉽습니다.

그럴 때는 더 자주 뿌리기 전에 내가 쓰는 제품의 성분과 사용한 날짜부터 살펴보세요.

이 글은 성분·사용 기간·분사 방향을 확인하는 생활 안내이며, 개인의 약 중단 일정은 진료를 통해 정해야 합니다.''')+toc
sections=[
'''코에 뿌리는 제품이라고 모두 같은 약은 아니니, 용기의 모양보다 상자에 적힌 성분명을 먼저 봅니다.

옥시메타졸린·자일로메타졸린 같은 비충혈제거제는 부은 코 점막의 혈관을 수축시켜 코막힘을 잠시 덜어주는 약입니다.

반면 플루티카손 같은 비강 스테로이드는 코 안의 염증과 부기를 줄이는 데 사용하며, 생리식염수와도 역할이 다릅니다.

NHS는 플루티카손 비강분무제를 규칙적으로 사용해야 효과를 볼 수 있다고 설명하므로, 바로 시원하지 않다고 임의로 횟수를 늘리지 마세요.

성분명을 읽기 어렵다면 제품 전체 이름과 뒷면을 휴대전화로 찍어 약사에게 보여주는 것이 간단합니다.

‘코막힘용’이라는 앞면 문구만으로 구분하기보다, 처음 사용한 날짜도 상자에 함께 적어두면 다음에 확인하기 편합니다.''',
'''식약처 의약품안전나라의 <strong>오트리빈에스비강분무액</strong> 안내에는 7일 이상 계속 사용하지 말고, 3일 사용해도 좋아지지 않으면 중지 후 의사·약사와 상의하도록 적혀 있습니다.

이는 해당 제품의 안내이므로, 다른 성분이나 어린이용 제품에 같은 사용법을 그대로 적용하지 마세요.

영국 MHRA는 2026년 4월 30일 옥시메타졸린·자일로메타졸린 제품의 연속 사용을 최대 5일로 제한하는 안전 권고를 발표했습니다.

국내 제품 설명과 영국의 권고는 적용되는 안내가 다르며, ‘5일을 넘는 순간 누구나 비염이 생긴다’는 뜻도 아닙니다.

핵심은 더 오래, 더 자주 쓰면서 버티지 않는 것이며, 증상이 남거나 사용을 멈추기 어렵다면 제품을 가져가 확인받으세요.

약효가 사라진 뒤 다시 코가 막혀 반복해서 쓰게 되는 현상을 반동성 코막힘이라고 하며, 장기적인 과용은 약물성 비염으로 이어질 수 있습니다.''',
'''스프레이를 콧속에 깊이 밀어 넣거나 가운데 벽을 향해 쏘고 있지는 않은지, 거울 앞에서 손의 방향을 확인해 보세요.

영국 Dartford and Gravesham NHS 병원 안내는 고개를 살짝 앞으로 숙이고, 코 가운데 벽인 비중격을 피해서 바깥쪽으로 분사하도록 설명합니다.

오른쪽 콧구멍에는 왼손을, 왼쪽에는 오른손을 쓰면 바깥쪽을 향하는 데 도움이 됩니다.

특정 각도를 재기보다 노즐을 가운데 벽에 겨누지 않는 것이 요점이며, 준비 분사와 호흡 방법은 제품 설명을 따르세요.

코피나 따가움이 계속되면 같은 곳에 반복해서 뿌리며 참지 말고, 사용 중인 제품과 분사 방법을 확인받는 편이 좋습니다.''',
'''‘안 뿌리면 잠을 못 자겠는데, 오늘부터 어떻게 해야 할까요?’라는 걱정이 들면 혼자 중단 일정을 정하기보다 진료를 받으세요.

MHRA는 오래 사용해 끊기 어려운 경우 의료진의 도움을 받아 사용을 줄이고, 필요하면 다른 치료를 검토하도록 안내합니다.

한쪽 코부터 끊는 방법이나 특정 회복 기간을 누구에게나 맞는 정답처럼 따라 하지는 마세요.

진료 때는 제품 이름, 처음 쓴 날짜, 하루에 뿌리는 횟수, 효과가 얼마나 가는지를 메모해 가져가면 설명하기 편합니다.

처방받은 스테로이드 스프레이도 ‘몸에 전혀 흡수되지 않아 무조건 안전하다’고 받아들여서는 안 됩니다.

NHS의 플루티카손 안내는 전신에 흡수되는 양이 적다고 설명하지만, 코 건조감·코피 등이 생길 수 있고 높은 용량을 오래 쓰면 위험이 달라질 수 있다고 덧붙입니다.

다른 스테로이드 약도 함께 쓰고 있다면 이를 알리고, 용량이나 제품을 스스로 바꾸지 마세요.''',
'''코세척을 한다면 코세척용으로 표시된 생리식염수나 전용 분말·용기의 사용 안내부터 확인하세요.

미국 CDC는 코세척에 증류수·멸균수 또는 끓인 뒤 식힌 물을 쓰도록 안내하며, 수돗물을 그대로 코에 넣지 말라고 설명합니다.

마셔도 되는 물과 코세척에 적합한 물은 같지 않으므로, 정수기에서 받은 물도 멸균수라고 생각해서는 안 됩니다.

전용 분말을 사용할 때는 물과 분말의 양을 설명서대로 맞추고, 용기 세척과 건조도 해당 제품의 안내를 따르세요.

세척은 약의 중단 계획을 대신하지 않으며, 통증이 나는데도 억지로 계속할 일은 아닙니다.

밤에 코가 막혀 잠이 불편하다면 코 증상을 먼저 확인하고, 잠자리 습관은 <a href="sleep-lying-down-eyes-closed-20min-rule.html">잠이 오지 않을 때 침대에서 할 일</a>에서 따로 살펴보세요.

오늘은 더 강하게 뿌리기보다 약 상자를 찾아 성분과 사용 날짜를 적어보세요.

에디터 혀니는 혼자 참고 버티기보다, 내 제품에 맞는 사용법을 확인하는 작은 실천을 권합니다.'''
]
table='<div class="custom-data-table-wrap" style="overflow-x:auto;margin:28px 0;border:1px solid #e2e8f0;border-radius:10px;"><table class="custom-data-table" style="width:100%;min-width:560px;border-collapse:collapse;font-size:0.92rem;"><thead><tr><th>구분</th><th>비충혈제거제</th><th>비강 스테로이드</th><th>생리식염수</th></tr></thead><tbody>'
for row in [('역할','단기간 코막힘 완화','코 안의 염증·부기 관리','코 안 세척·보습'),('확인할 것','제품별 횟수·연속 사용 제한','처방 또는 제품의 사용 일정','세척용 물·용기 관리'),('주의할 점','오래 쓰면 반동성 코막힘 가능','코피·자극 등 이상 반응 확인','수돗물을 그대로 쓰지 않기')]:
    table+='<tr>'+''.join('<td style="padding:12px;border-bottom:1px solid #e2e8f0;line-height:1.7;">'+c+'</td>' for c in row)+'</tr>'
table+='</tbody></table></div>'
card='<div class="info-section-card" style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:14px;padding:22px;margin:28px 0;"><strong>다음에 뿌리기 전 확인할 세 가지</strong>'
for label,text in [('성분','비충혈제거제인지 다른 종류인지 상자를 봅니다.'),('기간','처음 사용한 날과 실제 횟수를 기록합니다.'),('방향','노즐이 코 가운데 벽을 향하는지 살펴봅니다.')]:
    card+='<div style="margin-top:14px;line-height:1.8;"><span class="info-badge" style="background:#dbeafe;padding:3px 8px;border-radius:6px;">'+label+'</span> '+text+'</div>'
card+='</div>'
for i,(heading,section,img) in enumerate(zip(headings,sections,imgs),1):
    body+=f'<h2 id="sec{i}" style="font-size:1.32rem;line-height:1.5;margin:42px 0 18px;">{heading}</h2>'+paras(section)+img
    if i==2:body+=table
    if i==4:body+=card
nose['bodyHtml']=body
nose['title']='“스프레이 없으면 숨을 못 쉬어요” 환절기 코막힘, 비염 스프레이 끊기 전 확인할 3가지'
nose['desc']='비염 스프레이를 뿌려도 코가 금방 다시 막힌다면 성분과 사용 기간부터 확인하세요. 국내 제품 안내와 영국의 5일 권고를 구분하고, 분사 방향과 중단 전 챙길 기록을 살펴봅니다.'
nose['academicSource']='식약처 제품 안내·MHRA·NHS·CDC 공식 자료 기반'
nose['faqs']=[
 {'q':'스테로이드 코 스프레이도 5일 뒤에 끊어야 하나요?','a':'비충혈제거제의 단기 사용 권고를 모든 코 스프레이에 적용하지 않습니다. 플루티카손 같은 비강 스테로이드는 규칙적인 사용이 필요한 약이므로 처방과 제품 설명을 따르세요. 종류를 모르겠다면 약사에게 성분부터 확인해 보세요.'},
 {'q':'다시 답답해지면 한 번 더 뿌려도 될까요?','a':'증상이 돌아왔다는 이유로 정해진 횟수나 사용 간격을 넘기지 마세요. 더 자주 써야 할 것 같거나 사용 후에도 좋아지지 않는다면, 제품을 가져가 의사·약사에게 사용 기간과 횟수를 알려주세요.'},
 {'q':'가족이 같은 스프레이 용기를 함께 써도 되나요?','a':'식약처의 해당 제품 안내는 오염을 막기 위해 공동 사용을 피하도록 합니다. 가족끼리라도 각자 제품을 사용하고, 노즐은 제품 설명에 맞춰 관리하세요.'}
]
sources=[
('식약처 의약품안전나라 《오트리빈에스비강분무액 제품정보》','https://nedrug.mfds.go.kr/pbp/CCBBB01/getItemDetail?itemSeq=201903221','해당 제품의 연속 사용 제한·증상 미개선 시 조치·공동 사용 주의. 2026-09-14 조회; 본문 개정일 미확인.'),
('MHRA 《Nasal decongestant sprays and drops…with overuse》','https://www.gov.uk/drug-safety-update/nasal-decongestant-sprays-and-drops-containing-xylometazoline-hydrochloride-slash-oxymetazoline-hydrochloride-increased-risk-of-rebound-congestion-rhinitis-medicamentosa-and-tachyphylaxis-with-overuse','영국의 5일 권고와 과용·중단 관리. 2026-04-30 발표.'),
('NHS 《About / Side effects of fluticasone nasal spray and drops》','https://www.nhs.uk/medicines/fluticasone-nasal-spray-and-drops/side-effects-of-fluticasone-nasal-spray-and-drops/','적은 전신 흡수와 코피·자극, 고용량 장기 사용 주의. 마지막 검토 2023-02-24; 2026-09-14 원문 재확인.'),
('Dartford and Gravesham NHS 《How to take your nasal spray》','https://wheeze.dgt.nhs.uk/guides/nasal-spray','비중격을 피하는 분사 방향과 반대 손 사용. 수정 2023-01-18.'),
('CDC 《How to Safely Rinse Sinuses》','https://www.cdc.gov/naegleria/prevention/sinus-rinsing.html','코세척에 사용하는 안전한 물. 2025-07-16 발표.')]
nose['references']=[f'<a href="{url}">{title}</a> — {note}' for title,url,note in sources]
save(NOSE/'post_data.json',nose)

# Synchronize factual corrections in the existing Naver package, keeping images/tools.
ns=(backup/NP.relative_to(ROOT)).read_text(encoding='utf-8-sig')
n=lh.fromstring(ns);content=n.get_element_by_id('naverContent')
title=content.find('h1').text_content()
newtitle=title.replace('5일 사용 기준','사용 기간 확인')
ns=ns.replace(title,newtitle)
n=lh.fromstring(ns);content=n.get_element_by_id('naverContent')
replacements=[
'아침저녁 바람이 서늘해지면<br>코가 답답해 스프레이를 찾게 되시죠?',
'잠깐 편해졌다가 금방 다시 막히니<br>가방에도 침대 옆에도 두고 싶어집니다.',
'<mark>그럴수록 횟수를 늘리기 전에<br>내가 쓰는 성분과 사용 날짜부터 보세요.</mark>',
'제품은 비슷하게 생겼어도<br>코막힘용 약과 식염수는 역할이 다르거든요.',
'오늘은 약 상자를 옆에 놓고<br>놓치기 쉬운 표시를 함께 찾아볼게요.',
'상자의 성분란에 옥시메타졸린이나<br>자일로메타졸린이 적혀 있는지 살펴보세요.',
'<mark>이런 비충혈제거제는 혈관을 수축시켜<br>답답한 코를 잠시 편하게 해주는 약입니다.</mark>',
'염증을 다루는 스테로이드 스프레이와는<br>사용하는 이유와 일정이 달라요.',
'<u>이름이 낯설어 헷갈린다면</u><br>뒷면을 찍어 약사에게 보여주셔도 됩니다.',
'국내 오트리빈에스 제품 안내에는<br>7일 이상 이어서 쓰지 말라고 적혀 있습니다.',
'<mark>같은 제품을 3일 사용해도 나아지지 않으면<br>중지하고 의사·약사와 상의하도록 안내합니다.</mark>',
'영국 MHRA는 2026년 4월에 해당 성분들의<br>연속 사용을 최대 5일로 제한하도록 발표했어요.',
'국내 안내와 영국 권고를 섞어서<br>모든 스프레이가 5일짜리라고 생각하면 곤란합니다.',
'계속 쓰는데 더 답답해지는 상황이라면<br>의지만으로 버티지 말고 진료를 받아보세요.',
'<mark>한쪽 코만 끊으면 된다는 방법을 따라 하기보다<br>내가 쓴 약과 기간에 맞춰 중단 계획을 정하세요.</mark>',
'분사할 때는 가운데 벽을 피해 바깥쪽으로 향하고<br>노즐 준비와 호흡은 제품 설명을 따라주세요.',
'플루티카손도 전신 흡수가 적다는 뜻이지<br>코피나 자극 걱정이 전혀 없다는 뜻은 아닙니다.',
'세척을 하신다면 CDC가 안내한 멸균수·증류수나<br>끓여 식힌 물을 쓰고 전용 제품 설명을 지켜주세요.',
'사용 날짜를 상자에 적어두시는 편인가요,<br>아니면 오늘부터 기록해 보실까요? 😊'
]
target=content.findall('p')[:-1]
assert len(target)==len(replacements),(len(target),len(replacements))
for el,new in zip(target,replacements):
    el.text=None
    for c in list(el):el.remove(c)
    frag=parse(new);el.text=frag.text
    for c in list(frag):el.append(c)
for el,text in zip(content.findall('h2'),['| 겉모양보다 성분부터 읽어보세요','| 며칠 썼는지 상자에 적어두세요','| 끊기 어렵다면 기록을 챙겨보세요']):el.text=text
for el in content.xpath('.//img'):
    el.set('alt',el.get('alt','').replace('45도 방향으로','바깥쪽으로').replace('코 바깥쪽 바깥쪽으로','코 바깥쪽으로'))
# Keep Naver short blocks and add useful reading guidance, not fixed medical schedules.
extras=[
('상자의 성분란에','이름이 같은 제품군 안에서도<br>성인용과 어린이용은 다를 수 있어요.'),
('국내 오트리빈에스','여기서 말하는 날짜는 정해진 날까지<br>무조건 채워 써야 한다는 뜻이 아닙니다.'),
('국내 안내와','며칠 썼는지 가물가물하다면<br>처음 쓴 날부터 휴대전화 메모를 남겨보세요.'),
('계속 쓰는데','제품 이름과 하루 분사 횟수를 적어두면<br>내 상황을 설명할 때 빠뜨릴 일이 줄어듭니다.'),
('분사할 때는','영국 NHS 병원 안내는 반대쪽 손으로 잡아<br>코 가운데를 피하는 방법을 소개합니다.'),
('플루티카손도','NHS는 코가 마르거나 따가울 수 있다고도 적고 있어요.<br>불편함이 계속되면 사용 방법을 확인받으세요.'),
('세척을 하신다면','마셔도 되는 물이 코세척용 물과 같지는 않아요.<br>정수기 물도 멸균수로 여기면 안 됩니다.'),
('사용 날짜를','에디터 혀니는 더 자주 뿌리기 전에<br>약 상자를 한 번 더 읽어보셨으면 합니다.')]
for start,text in extras:
    el=next(e for e in content.findall('p') if e.text_content().startswith(start));el.addprevious(lh.fragment_fromstring('<p>'+text+'</p>'))
ref=content.xpath('./div[div[contains(text(),"공인 의학")]]')[0]
ref.text=None
for c in list(ref):ref.remove(c)
ref.append(lh.fragment_fromstring('<strong>공식 자료 확인</strong>'))
for title,url,note in sources:
    e=lh.fragment_fromstring('<p>'+html.escape(title+' — '+note)+'</p>');e.set('style','font-size:0.84rem;line-height:1.65;text-align:left;');ref.append(e)
# Update only the content fragment and title; preserve surrounding copy scripts/styles byte-for-byte.
oldcontent=lh.fromstring(ns).get_element_by_id('naverContent')
start=ns.index('<div id="naverContent">');end=ns.index('    <!-- 하단 복사 버튼 -->',start)
ns=ns[:start]+lh.tostring(content,encoding='unicode')+'\n\n'+ns[end:]
ns=ns.replace('무조건 채워','끝까지 채워').replace('영국 NHS 병원 안내','영국 NHS 안내').replace('식약처 의약품안전나라 《','식약처 《')
ns=ns.replace('코막힘 각성 막는 침대 20분 수칙','잠자리 습관을 살펴보는 침대 20분 수칙')
ns=ns.replace('#비염스프레이부작용','#비염스프레이주의점')
NP.write_text(ns,encoding='utf-8')
assert len(rows)==len(original)
for before,after in zip(original,rows):
    if before['slug'] not in [meat['slug'],nose['slug']]:assert before==after
    for key in ['slug','date','thumb','isLatest','isEditorPick']:assert before.get(key)==after.get(key)
save(DB,rows)
save(OUT/'revised_sources.json',{'sources':sources})
print('Updated two Google DB entries, meat draft/source, rhinitis source and Naver rhinitis package. No deployment.')

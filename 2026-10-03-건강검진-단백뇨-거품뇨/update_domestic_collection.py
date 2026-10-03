from pathlib import Path
import json,re,shutil
w=Path(__file__).resolve().parent
r=w.parent
pf=w/'post_data.json'
nf=next(w.glob('*네이버블로그용.html'))
backup=w/'before_domestic_revision'
backup.mkdir(exist_ok=True)
for f in (pf,nf): shutil.copy2(f,backup/f.name)
p=json.loads(pf.read_text(encoding='utf-8-sig'))
b=p['bodyHtml']; n=nf.read_text(encoding='utf-8-sig')
old='기립성 단백뇨를 배제하는 아침 첫 소변 재검사 수칙'
new='아침 첫 소변 재검, 채취 장소부터 확인하세요'
b=b.replace(old,new)
b=b.replace("일시적 단백뇨를 감별하기 위해서는 낮 시간 활동의 간섭을 줄일 수 있는 '아침 첫 소변'의 중간뇨로 재검사를 받는 것이 권장됩니다.","재검 전에는 검사기관에 채취 장소와 아침 첫 소변이 필요한지 먼저 확인하세요. 아침 첫 소변이 권장되지만 다른 시간에도 검사할 수 있으며, 별도 안내 없이 집에서 미리 받아 갈 필요는 없습니다.")
b=b.replace('[안정 후 아침 첫 소변 재검]','[채취 방법 확인 후 재검]')
b=b.replace('진짜 거품뇨의 구별법','거품만으로 판별하기 어려운 이유')
b=b.replace('차분한 생활 관리와 아침 첫 소변 재검사로','차분한 생활 관리와 검사기관 안내에 따른 재검사로')
style=' style="font-size:1.02rem;line-height:1.9;color:#334155;margin-bottom:22px;"'
paras=[
'단백뇨 재검을 예약할 때는 소변을 어디에서 채취하는지, 아침 첫 소변이 필요한지부터 확인하세요. 검사기관에서 용기를 받아 채취한 뒤 지정된 장소에 제출하는 방식으로 진행할 수 있습니다.',
'아침 첫 소변은 권장되는 검체지만, 일반 소변검사는 다른 시간에도 채취할 수 있습니다. 아침 첫 소변을 권장한다는 말이 집에서 받아 가져오라는 뜻은 아닙니다.',
'집에서 채취하라는 안내를 받은 경우에만 검사기관이 제공하거나 지정한 용기를 사용하세요. 채취 시점과 보관 방법, 제출 가능 시간도 해당 기관의 안내를 따라야 합니다. 임의의 컵이나 병에 미리 받아 가져가지 마세요.',
'소변을 받을 때는 처음 나오는 부분을 흘려보낸 뒤 중간뇨를 용기에 받습니다. 용기 안쪽과 뚜껑 안쪽에 손이 닿지 않도록 하고, 채취량과 제출 방법은 검사실 안내를 따르세요.',
'재검 전 격렬한 운동은 피하고 평소와 비슷하게 수분을 섭취하세요. 검사 직전에 물을 과하게 마시지 말고, 생리 중이거나 최근 발열·격한 운동이 있었다면 의료진에게 알려주세요.',
'24시간 소변을 모으는 검사는 한 번의 소변을 받는 재검과 별도입니다. 이 검사를 처방받았다면 전용 용기와 수집·보관 안내를 받아 진행합니다.'
]
start=b.index('<h2 id="sec4">')
figend=b.index('</figure>',start)+len('</figure>')
end=b.index('<h2 id="sec5">',figend)
b=b[:figend]+'\n\n'+'\n\n'.join('<p'+style+'>'+x+'</p>' for x in paras)+'\n\n'+b[end:]
p['desc']='건강검진 단백뇨 1+의 의미와 거품뇨 자가 판별의 한계를 알아봅니다. 일시적 원인, 아침 첫 소변 권장 이유, 검사기관에서의 채취와 자택 채취 안내를 구분하고 재검 준비 사항을 정리했습니다.'
p['faqs'][0]['a']='요단백 1+ 한 번만으로 원인이나 치료 필요성을 결정하지 않습니다. 검진 결과를 가지고 의료진과 재검을 상의하고 채취 장소와 시간을 안내받으세요. 붓기나 혈뇨 등 동반 증상이 있다면 함께 알리고, 임의로 약이나 민간요법을 시작하지 마세요.'
p['faqs'][2]={'q':'단백뇨 재검 때 아침 소변을 집에서 받아 가야 하나요?','a':'무조건 집에서 받아 가는 것은 아닙니다. 아침 첫 소변이 권장되지만 일반 소변검사는 다른 시간에도 가능합니다. 재검 기관에 채취 장소와 아침 첫 소변 필요 여부를 먼저 확인하세요. 집에서 채취하도록 안내받았을 때만 지정 용기와 보관·제출 지침을 따릅니다. 어느 장소에서든 처음 나오는 부분을 흘려보내고 중간뇨를 받되 검사실의 안내를 우선하세요.'}
kdca='https://health.kdca.go.kr/healthinfo/biz/health/gnrlzHealthInfo/gnrlzHealthInfo/gnrlzHealthInfoView.do?cntnts_sn=5807'
p['references'][0]=f'<a href="{kdca}">질병관리청 국가건강정보포털 — 소변검사: 검사 검체와 검사 종류</a>'
ref='<a href="https://seranmed.co.kr/equipment/urinalysis/">세란내과 — 소변검사 용기 수령·채취·제출 절차</a>'
if ref not in p['references']:p['references'].append(ref)
n=n.replace('| 왜 재검사는 아침 첫 소변 중간뇨를 권장할까요','| 재검할 소변, 병원에서 받을까요 집에서 받아 갈까요')
n=re.sub(r'<p>일시적인 현상인지 확인하는 가장 권장되는.*?</p>', '<p>재검 예약을 했다면 먼저 <mark>채취 장소와 아침 첫 소변이 필요한지</mark> 확인해 주세요.<br>검사기관에서 용기를 받아 소변을 채취하고, 지정된 곳에 제출하는 방식으로 진행할 수 있습니다.</p>',n,flags=re.S)
n=re.sub(r'<p>밤새 누워 자는 동안에는.*?</p>','<p>아침 첫 소변이 권장되지만 다른 시간의 소변으로도 검사가 가능합니다.<br><mark>아침 첫 소변이 좋다는 말이 집에서 미리 받아 오라는 뜻은 아니에요.</mark></p><p>집에서 채취하라는 안내를 받은 경우에만 지정된 용기를 사용해 주세요.<br>보관 방법과 제출 시간도 검사기관 안내를 따라야 하며, 임의의 컵이나 병에 미리 받아 갈 필요는 없습니다.</p>',n,flags=re.S)
n=re.sub(r'<p>소변을 받을 때도 요령이 필요합니다.*?</p>','<p>소변을 받을 때는 처음 나오는 부분을 흘려보낸 뒤 <mark>중간뇨</mark>를 받습니다.<br>용기와 뚜껑 안쪽에 손이 닿지 않도록 하고, 채취량과 제출 방법은 검사실 안내를 따라 주세요.</p><p>참고로 <mark>24시간 소변을 모으는 검사</mark>는 별도로 처방되는 검사예요.<br>일반적인 한 번의 재검과 구분하고, 전용 용기와 수집 안내를 받아 진행합니다.</p>',n,flags=re.S)
n=n.replace('몸 상태를 안정시킨 뒤 아침 첫 소변 재검사로','검사기관에서 안내받은 방법으로 재검사를 진행하며')
n=n.replace('재검사 전 24~48시간 동안은 과격한 근력 운동, 마라톤, 사우나 등 체액을 급격히 소모하는 활동을 피하시는 편이 바람직합니다.','재검 전 격렬한 운동은 피하고, 최근 운동이나 발열, 생리 여부를 의료진에게 알려 주세요.')
n=n.replace('충분한 미온수를 드시는 것은 이롭지만,','평소와 비슷하게 물을 드시되 검사 직전 과하게 마시지 마세요. 또한')
n=n.replace('<li>국가건강정보포털 — 소변이상(단백뇨) 질환 및 검사 지침</li>',f'<li><a href="{kdca}">질병관리청 국가건강정보포털 — 소변검사</a></li><li>{ref}</li>')
caps={2:'검사기관에서 안내를 받으며 소변검사용 용기를 수령하는 모습',4:'채취한 검체를 검사기관의 지정 장소에 제출하는 모습'}
for i,c in caps.items():
 stem=f'post{i:02d}';name=f'{stem}-v4.jpg'
 shutil.copy2(w/'images'/name,r/'kkuldanji_web'/'images'/'posts'/p['slugKey']/name)
 def fig(m):
  s=m.group(0)
  if stem not in s:return s
  s=re.sub(stem+r'(?:-v\d+)?\.jpg',name,s)
  s=re.sub(r'alt="[^"]*"',f'alt="{c}"',s)
  return re.sub(r'<figcaption>.*?</figcaption>',f'<figcaption>{c} (AI 생성 이미지·절차 예시)</figcaption>',s,flags=re.S)
 b=re.sub(r'<figure\b.*?</figure>',fig,b,flags=re.S)
 def img(m):
  s=m.group(0)
  if stem not in s:return s
  s=re.sub(stem+r'(?:-v\d+)?\.jpg',name,s)
  return re.sub(r'alt="[^"]*"',f'alt="{c} (AI 생성 이미지·절차 예시)"',s)
 n=re.sub(r'<img\b[^>]*>',img,n)
p['bodyHtml']=b
pf.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')
nf.write_text(n,encoding='utf-8')
dbf=r/'data'/'posts_db.json';db=json.loads(dbf.read_text(encoding='utf-8-sig'))
target=next(x for x in db if x['slug']==p['slug'])
for key in ('bodyHtml','desc','faqs','references'):target[key]=p[key]
dbf.write_text(json.dumps(db,ensure_ascii=False,indent=2),encoding='utf-8')
planf=w/'image_plan.json';plan=json.loads(planf.read_text(encoding='utf-8-sig'))
for i,c in caps.items():
 plan['storyboard'][i]['output_file']=f'images/post{i:02d}-v4.jpg'
 plan['storyboard'][i]['google_caption']=c+' (AI 생성 이미지·절차 예시)'
plan['storyboard'][4]['h2_mapping']=new
plan['storyboard'][4]['prompt']=plan['storyboard'][4]['prompt'].replace('securely capped','securely YELLOW capped')
plan['location_anchor']='1·3·5번은 같은 한국 아파트, 2·4번은 국내 재검 안내에 따른 검사기관의 용기 수령·제출 절차 예시'
planf.write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
print('Updated both manuscripts, FAQ, domestic references, DB and clinic images 2/4.')

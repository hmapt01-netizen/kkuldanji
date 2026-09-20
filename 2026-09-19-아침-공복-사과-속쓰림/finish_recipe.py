import json,re,shutil,hashlib
from pathlib import Path
from PIL import Image
r=Path(__file__).resolve().parent
package=r.parent/'꿀단지 네이버'/'17_아침_공복_사과_속쓰림'
backup=r/'backup-before-image-assembly'
backup.mkdir(exist_ok=True)
caps={'thumb':'아침 식탁에 준비한 사과와 물 한 잔','post01':'사과를 먹은 뒤 불편한 부위와 증상을 살피는 모습','post02':'껍질이 질기게 느껴질 때 선택적으로 손질하는 예시','post03':'씨를 제거한 사과 반쪽을 덮개 있는 용기에 익혀 꺼내는 모습','post04':'껍질째 익힌 사과를 자르고 시나몬을 가볍게 더한 간식','post05':'식사를 잠시 멈추고 불편했던 증상을 기록하는 모습'}
for slot in caps:
    dst=r/'images'/f'{slot}.jpg'
    if dst.exists() and not (backup/dst.name).exists():shutil.copy2(dst,backup/dst.name)
    im=Image.open(r/'images-young-v2'/f'{slot}.png').convert('RGB')
    im.resize((1280,720),Image.Resampling.LANCZOS).save(dst,quality=92,optimize=True)
(package/'images').mkdir(exist_ok=True)
for slot in caps:shutil.copy2(r/'images'/f'{slot}.jpg',package/'images'/f'{slot}.jpg')
gp=r/'post_data.json'
np=r/'31_아침_공복_사과_속쓰림_네이버블로그용.html'
for f in [gp,np]:shutil.copy2(f,backup/f.name)
p=json.loads(gp.read_text(encoding='utf-8-sig'));b=p['bodyHtml']
b=b.replace('사과 반쪽을 익혀 자르는 간단 레시피와 식사 조합','사과 반쪽을 익혀 자르는 간단 레시피')
b=re.sub(r'<tr>\s*<td[^>]*>일반 식사\(달걀 등\)와 병행</td>[\s\S]*?</tr>','',b)
figs={}
for m in re.finditer(r'<figure\b[^>]*>[\s\S]*?</figure>',b):
    sm=re.search(r'(post\d\d)\.jpg',m.group())
    if sm:
        slot=sm.group(1);f=m.group()
        f=re.sub(r'alt="[^"]*"','alt="'+caps[slot]+'"',f)
        f=re.sub(r'(<figcaption[^>]*>)[\s\S]*?(</figcaption>)',lambda x:x[1]+caps[slot]+x[2],f)
        figs[slot]=f
b=re.sub(r'<figure\b[^>]*>[\s\S]*?</figure>','',b)
for sec,slots in [(1,['post01']),(3,['post02']),(4,['post03']),(5,['post05'])]:
    b=re.sub(r'(<h2 id="sec'+str(sec)+r'">.*?</h2>)',lambda m:m[1]+'\n'+''.join(figs[s] for s in slots),b,count=1)
# The finished dish belongs after cooking instructions, before comparison table.
b=b.replace('<div class="custom-data-table-wrap"',figs['post04']+'\n<div class="custom-data-table-wrap"',1)
p['bodyHtml']=b;p['featuredCaption']=caps['thumb']
gp.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')
h=np.read_text(encoding='utf-8-sig')
h=h.replace('一般','一般').replace('일반 식사와 함께 곁들이면 한결 편안합니다','충분히 식힌 뒤 소량부터 먹어보세요')
mapping={
'공복에 사과만 따로 드시기보다':'익힌 사과는 겉보다 속이 더 뜨거울 수 있어요.<br>충분히 식힌 뒤 먹기 좋은 크기로 잘라주세요.',
'사과를 혼자 드시기보다':'반쪽을 만들었다고 한 번에 다 먹을 필요는 없습니다.<br>몇 조각부터 천천히 먹고 내게 편한 양을 찾아보세요.',
'단, 특정 음식이 위벽을 완벽히 보호해':'껍질이 질기게 남으면 벗겨도 되고, 시나몬은 생략해도 됩니다.<br>익힌 사과를 먹고도 속이 불편하면 더 먹지 마세요.'}
for needle,text in mapping.items():
    hit=[0]
    def sub(m):
        if needle in m[0]:hit[0]+=1;return '<p>'+text+'</p>'
        return m[0]
    h=re.sub(r'<p\b[^>]*>[\s\S]*?</p>',sub,h)
    assert hit[0]==1,(needle,hit)
for slot,caption in caps.items():
    h=re.sub(r'(<img\b[^>]*src="images/'+slot+r'\.jpg"[^>]*alt=")[^"]*(")',lambda m:m[1]+caption+m[2],h)
    h=re.sub(r'(<img\b[^>]*src="images/'+slot+r'\.jpg"[^>]*>)',lambda m:m[1]+'<p class="image-caption" style="font-size:0.85rem;color:#64748b;">'+caption+'</p>',h,count=1)
np.write_text(h,encoding='utf-8')
shutil.copy2(np,package/'17_아침_공복_사과_속쓰림_네이버블로그용.html')
assert len(re.findall(r'<figure\b',b))==5
assert len(re.findall(r'<img\b',h))==6
assert '달걀' not in b and '계란' not in h and '달걀' not in h
assert '1~2분' not in b+h and '1분 30초' not in b+h
assert all((r/('images/'+s+'.jpg')).exists() for s in caps)
assert len({hashlib.sha256((r/'images'/f'{s}.jpg').read_bytes()).hexdigest() for s in caps})==6
print('Checked: both drafts, six unique image files, captions, Google placement, timing, egg removal, canonical Naver package.')

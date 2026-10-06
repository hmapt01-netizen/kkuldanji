from pathlib import Path
import json, shutil, io, hashlib
from PIL import Image

root=Path('D:/작업/꿀단지')
work=root/'2026-10-06-독감-등교-출석인정-서류'
package=Path(__file__).resolve().parent.parent
out=Path(__file__).resolve().parent
gen=Path('C:/Users/lim/.codex/generated_images/01a10e90-1c70-7d10-8b0a-bbaa5dd9bf50')
ids=['d1e56f73-42e2-415a-8728-9610f5d469b9','ae758d91-61b2-4d3e-8e7d-7d8d622d5c65','a8a1c4c4-0063-4779-ad31-6d14683f84fc','56c1477f-815e-4e73-a92a-13eb2605520d','d293cbeb-d05c-4030-bcaa-3ef53cf08ef3','e29222ab-49aa-4b17-bbe1-9119ab3c5f63']
names=['thumb.jpg']+[f'post{i:02}.jpg' for i in range(1,6)]
destinations=[work/'images',package/'images',root/'kkuldanji_web/images/posts/flu-school-attendance-criteria-proof-documents']
(out/'originals').mkdir(exist_ok=True)
(out/'final').mkdir(exist_ok=True)
(out/'backup').mkdir(exist_ok=True)
manifest=[]
for name,uid in zip(names,ids):
    src=gen/f'exec-{uid}.png'
    shutil.copy2(src,out/'originals'/f'{Path(name).stem}.png')
    im=Image.open(src).convert('RGB').resize((1280,720),Image.Resampling.LANCZOS)
    choices=[]
    for q in range(80,99):
        b=io.BytesIO();im.save(b,'JPEG',quality=q,optimize=True)
        choices.append((q,b.getvalue()))
    valid=[x for x in choices if 150*1024<=len(x[1])<=250*1024]
    q,data=min(valid or choices,key=lambda x:abs(len(x[1])-195*1024))
    final=out/'final'/name;final.write_bytes(data)
    for i,d in enumerate(destinations):
        d.mkdir(parents=True,exist_ok=True)
        backup=out/'backup'/str(i);backup.mkdir(exist_ok=True)
        if (d/name).exists() and not (backup/name).exists():shutil.copy2(d/name,backup/name)
        shutil.copy2(final,d/name)
    manifest.append(dict(slot=name,source=str(src),size=len(data),quality=q,dimensions=[1280,720],sha256=hashlib.sha256(data).hexdigest()))

changes={
'체온계를 확인하며 등교 가능 기준을 고민하는 학부모':'체온계를 내려놓으며 아이 상태를 살피는 학부모',
'해열제 복용 시간과 체온 변화를 기록한 메모장과 체온계':'체온 기록 예시를 적은 노트와 체온계',
'스마트폰으로 학교 알림장의 출석 인정 서류 안내를 확인하는 학부모':'스마트폰으로 학교 안내를 확인하는 학부모',
'병원에서 발급받은 진료확인서와 학교 제출용 결석 서류':'학교 제출 서류 체크리스트와 봉투',
'격리가 끝나고 건강하게 등교를 준비하며 아이 책가방을 챙기는 어머니':'책가방에 물병을 챙기는 학부모'}
files=[work/'post_data.json',root/'data/posts_db.json',*work.glob('*.html'),*package.glob('*.html')]
for i,f in enumerate(files):
    backup=out/'backup'/f'text_{i}_{f.name}'
    if not backup.exists():shutil.copy2(f,backup)
    s=f.read_text('utf-8-sig')
    for a,b in changes.items():s=s.replace(a,b)
    f.write_text(s,encoding='utf-8')

plan_path=work/'image_plan.json'
shutil.copy2(plan_path,out/'backup/image_plan_before.json')
plan=json.loads(plan_path.read_text('utf-8-sig'))
plan['version']='2026-10-06-v2'
plan['approval_note']='사용자 요청: 이전 글 보고 썸네일 이미지 어떻게 만들었는지 확인하고 썸네일부터 전체 이미지 새로 생성해서 만들어줘 만든후 평가해서 문제가 있는건 다시 생성해서 완성 시켜줘'
plan['generation_tool']='built-in image_gen'
plan['character_anchor']['anchor_source_image']='images/thumb.jpg'
plan['prop_anchor']='흰 귀 체온계: 회색 화면과 세이지 원형 버튼. 네이비 책가방: 검은 지퍼와 직사각 앞주머니.'
descs=['직전 글처럼 큰 한글 제목을 왼쪽, 인물과 체온계 및 책가방을 오른쪽에 배치. 독감 등교 / 언제부터? / 출석 인정 서류까지','동일 인물이 같은 체온계를 탁자에 내려놓는 장면. 첫 시안은 화면 방향이 부자연스러워 폐기 후 재생성','동일 체온계와 한글 체온 기록 예시 및 학교 확인 항목을 적은 노트와 펜 정물','동일 인물이 소파에서 스마트폰 학교 안내를 확인. 화면 뒷면만 표시','학교 제출 서류 준비 체크리스트와 학교 제출용 봉투 및 펜. 한글 인쇄, 진단서나 도장 없음','동일 인물이 같은 네이비 가방에 세이지 물병을 넣는 등교 준비 장면']
for i,item in enumerate(plan['storyboard']):
    item['source']=manifest[i]['source']
    item['prompt']='Photorealistic editorial, 16:9, same Korean mother beige cardigan white tee charcoal trousers, pale oak apartment; '+descs[i]
    item['scene_ko']=descs[i]
    item['caption']=changes.get(item['caption'],item['caption'])
    item['reference_paths']=[] if i==0 else ['images/thumb.jpg','images/post01.jpg']
    item['requires_anchor_inheritance']=i>0
    item['is_anchor_origin']=i==0
plan_path.write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'image_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'prompt_set.json').write_text(json.dumps(plan['storyboard'],ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(manifest,ensure_ascii=False,indent=2))


from pathlib import Path
from PIL import Image, ImageOps
import json, shutil, hashlib, io
work=Path(r'D:\작업\꿀단지\2026-10-22_간수치_비알코올성지방간')
site=Path(r'D:\작업\꿀단지\kkuldanji_web')
slug='nonalcoholic-fatty-liver-elevated-alt-ggt-fructose-diet-guide'
gen=Path(r'C:\Users\lim\.codex\generated_images\01a15bbf-8f26-7bb3-a77f-02cd045e134b')
ids=['67eeb845-1999-49c3-9d96-3972b70796a9','3f1aa764-3aa8-4675-8631-3906b8939018','31dc154a-f625-4447-8d1a-fdf66ffd2f4b','af15fd8e-1400-411e-a7f9-e6f15a4c9366','7fb8908f-65fe-479e-a7e4-0d61a4f74847','7e6809ed-2544-4a4c-8a05-792ff12fd2cf']
names=['thumb.jpg']+[f'post{i:02}.jpg' for i in range(1,6)]
protected=[work/'post_data.json',site/'posts'/f'{slug}.html',work/'네이버.html']
hashfile=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before={str(p):hashfile(p) for p in protected}
backup=work/'image_backup_before_40s'
backup.mkdir(exist_ok=True)
result=[]
for name,gid in zip(names,ids):
    target=work/'images'/name
    if not (backup/name).exists(): shutil.copy2(target,backup/name)
    img=ImageOps.fit(Image.open(gen/f'exec-{gid}.png').convert('RGB'),(1280,720),method=Image.Resampling.LANCZOS)
    for quality in range(85,98):
        buf=io.BytesIO()
        img.save(buf,format='JPEG',quality=quality,optimize=True)
        if len(buf.getvalue())>=150*1024: break
    target.write_bytes(buf.getvalue())
    actual=site/'images'/'posts'/slug/name
    shutil.copy2(target,actual)
    assert hashfile(target)==hashfile(actual)
    result.append({'file':name,'size':img.size,'bytes':target.stat().st_size,'sha256':hashfile(target),'source':str(gen/f'exec-{gid}.png')})
assert before=={str(p):hashfile(p) for p in protected}
assert len({r['sha256'] for r in result})==6
plan=json.loads((work/'image_plan.json').read_text(encoding='utf-8'))
plan['character_anchor']={'gender':'female Korean','age_range':'40s, approximately 45','hair':'shoulder-length dark brown','persona_summary':'동일한 40대 한국 여성, 크림 가디건, 흰 티셔츠, 차콜 바지','reference':str(gen/f'exec-{ids[0]}.png')}
plan['location_anchor']='Warm daylight Korean apartment, cream walls, light oak furnishings'
for i,s in enumerate(plan['storyboard']):
    s['slot']=s['file'];s['type']='still_life' if i in [2,3] else 'character'
    s['ImagePaths']=[] if i in [0,2,3] else [str(gen/f'exec-{ids[0]}.png')]
plan['generation_tool']='built-in image_gen'
(work/'image_plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
(work/'image_replacement_audit.json').write_text(json.dumps({'images':result,'text_files_unchanged':before,'scope':'local work images and actual site image assets replaced; no remote deployment'},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
print('Article source, captions and HTML byte-identical; actual site copies match all 6 images.')


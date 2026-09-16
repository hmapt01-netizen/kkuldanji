"""Preserve generated originals and export approved blog image assets."""
from pathlib import Path
from PIL import Image, ImageOps
import hashlib, json, shutil
W=Path(__file__).resolve().parent
G=Path('C:/Users/lim/.codex/generated_images/01a0a20c-1056-7ed2-87ba-72c29acdefd2')
files={
'thumb':'exec-524f5647-2c13-46b2-9378-b0f67136c049.png',
'post01':'exec-a569ecbc-0393-4e73-a991-50ae519573b5.png',
'post02':'exec-a19d48e4-7352-4a27-a9bd-6ca046cdf0d7.png',
'post03':'exec-a5b5309e-470f-4d8a-a416-afd6a8192315.png',
'post04':'exec-97c9652b-f383-4317-a5d2-91f3355668d1.png',
'post05':'exec-521489d4-0d90-4d7e-a663-286518a101a8.png',
'naver_extra01':'exec-151fb495-f0ac-4369-a062-2d1a2ac2516d.png'}
(W/'images').mkdir(exist_ok=True)
(W/'image_originals').mkdir(exist_ok=True)
results=[]
for name,source in files.items():
    dest=W/'images'/f'{name}.jpg'
    if dest.exists(): raise FileExistsError(dest)
    shutil.copy2(G/source,W/'image_originals'/f'{name}.png')
    im=Image.open(G/source).convert('RGB')
    im=ImageOps.fit(im,(1280,720),method=Image.Resampling.LANCZOS)
    im.save(dest,quality=85,optimize=True,subsampling=0)
    results.append(dict(slot=dest.name,source=str(G/source),width=1280,height=720,kb=round(dest.stat().st_size/1024,1),quality=85,sha256=hashlib.sha256(dest.read_bytes()).hexdigest()))
assert len({r['sha256'] for r in results})==7
report=dict(images=results,visual_review='7장 확인. 인물 3컷 얼굴·머리·크림 블라우스·베이지 바지 일관. 정물과 인물 장면 구분. 읽을 수 있는 검사 수치·개인정보 없음. 일부 컷 소품 컵은 일상 배경으로 검사 중 섭취 장면이 아님.',size_note='1280×720, JPEG 85%, 무손실 원본 별도 보존. 용량 하한을 맞추기 위한 패딩은 하지 않음.')
(W/'image_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
plan=json.loads((W/'image_plan.json').read_text(encoding='utf-8'))
items=plan['storyboard']+plan['naver_additional_storyboard']
cards=''.join(f'<figure><img src="images/{i["slot"]}" alt="{i["scene_ko"]}"><figcaption>{i["scene_ko"]}</figcaption></figure>' for i in items)
(W/'image_gallery.html').write_text('<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>중성지방 재검 · 화보 7장</title><style>body{background:#f5f4ef;color:#234338;font-family:"Malgun Gothic",sans-serif;margin:30px auto;max-width:1200px;padding:20px}section{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:24px}figure{margin:0;background:white;border-radius:14px;overflow:hidden}img{width:100%;display:block}figcaption{padding:18px;line-height:1.6}</style><h1>중성지방 재검 · 화보 7장</h1><section>'+cards+'</section></html>',encoding='utf-8')
print(json.dumps(results,ensure_ascii=False))

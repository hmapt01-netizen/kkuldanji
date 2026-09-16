"""Apply the user-requested post05 correction to both local article packages."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys
W=Path(__file__).resolve().parent
R=W.parent
c=json.loads((W/'post05_correction_v3.json').read_text(encoding='utf-8'))
backup=W/'image_originals'/'post05_correction_history'
backup.mkdir(exist_ok=True)
for src,name in [(W/'image_originals/post05.png','post05-v1.png'),(W/'images/post05.jpg','post05-v1.jpg'),(W/'image_generation.json','image_generation-v1.json'),(W/'image_review.json','image_review-v1.json')]:
    if not (backup/name).exists():shutil.copy2(src,backup/name)
shutil.copy2(c['reference'],backup/'post05-v2.png')
shutil.copy2(c['source'],W/'image_originals/post05.png')
m=json.loads((W/'image_generation.json').read_text(encoding='utf-8'))
row=next(x for x in m['assets'] if x['id']=='post05')
row.update(prompt=c['prompt'],original_source=c['source'],reference_paths=[str(backup/'post05-v2.png')],visual_review=c['visual_review'])
(W/'image_generation.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
subprocess.run([sys.executable,'-B','-X','utf8',str(W/'prepare_images.py')],check=True)
targets=[R/'꿀단지 네이버/15_추석_고기택배_수령확인/images/post05.jpg',R/'kkuldanji_web/images/posts/chuseok-meat-delivery-thawing-safety/post05.jpg']
for target in targets:
    shutil.copy2(W/'images/post05.jpg',target)
    assert target.read_bytes()==(W/'images/post05.jpg').read_bytes()
sys.path.insert(0,str(R/'codex_tools'))
import workflow_guard as guard
state=guard.state_of(W)
receipt=next(x for x in state['receipts'] if x['stage']=='assembly')
artifacts=[a['path'] for a in receipt['artifacts']]
guard.record(W,'assembly',artifacts,'사용자가 지적한 post05 휴대전화 가시성 수정. 화면에 같은 고기가 보이는 어깨 뒤쪽 촬영 구도 직접 확인 후 구글·네이버의 동일 이미지 경로 교체. 이미지 검사 통과. 제목·본문·기존 계획 장면은 유지.')
result=dict(method=c['method'],visual_review=c['visual_review'],synced=[str(x) for x in targets],
            sha256=hashlib.sha256((W/'images/post05.jpg').read_bytes()).hexdigest(),published=False)
(W/'post05_correction_applied.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))

from pathlib import Path
import json, re, shutil

work = Path(__file__).resolve().parent
root = work.parent
web = root / 'kkuldanji_web'
post_file = work / 'post_data.json'
post = json.loads(post_file.read_text(encoding='utf-8-sig'))
naver_file = next(work.glob('*네이버블로그용.html'))
backup = work / 'images' / 'before_replacement'
for f in [post_file, naver_file]:
    shutil.copy2(f, backup / f.name)
captions = [
    '집에서 건강검진 결과지를 차분히 살펴보는 모습',
    '소변검사를 위해 준비된 검체 용기와 검사 서류',
    '운동 도구를 정리해 두고 재검사를 앞두고 쉬는 모습',
    '아침 소변검사를 앞두고 준비한 뚜껑 있는 검체 용기',
    '검진 결과지를 가방에 챙기며 진료를 준비하는 모습',
]
body = post['bodyHtml']
naver = naver_file.read_text(encoding='utf-8-sig')
asset_dir = web / 'images' / 'posts' / post['slugKey']
for i, caption in enumerate(captions, 1):
    stem = f'post{i:02d}'
    filename = f'{stem}-v3.jpg'
    shutil.copy2(work / 'images' / filename, asset_dir / filename)
    def figure(match):
        block = match.group(0)
        if not re.search(stem + r'(?:-v\d+)?\.jpg', block):
            return block
        block = re.sub(stem + r'(?:-v\d+)?\.jpg', filename, block)
        block = re.sub(r'alt="[^"]*"', f'alt="{caption}"', block)
        return re.sub(r'<figcaption>.*?</figcaption>', f'<figcaption>{caption} (AI 생성 이미지)</figcaption>', block, flags=re.S)
    body = re.sub(r'<figure\b.*?</figure>', figure, body, flags=re.S)
    def nimg(match):
        tag = match.group(0)
        if not re.search(stem + r'(?:-v\d+)?\.jpg', tag):
            return tag
        tag = re.sub(stem + r'(?:-v\d+)?\.jpg', filename, tag)
        return re.sub(r'alt="[^"]*"', f'alt="{caption} (AI 생성 이미지)"', tag)
    naver = re.sub(r'<img\b[^>]*>', nimg, naver)
post['bodyHtml'] = body
post_file.write_text(json.dumps(post, ensure_ascii=False, indent=2), encoding='utf-8')
naver_file.write_text(naver, encoding='utf-8')
db_file = root / 'data' / 'posts_db.json'
db = json.loads(db_file.read_text(encoding='utf-8-sig'))
matches = [p for p in db if p['slug'] == post['slug']]
assert len(matches) == 1
matches[0]['bodyHtml'] = body
db_file.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding='utf-8')
plan_file = work / 'image_plan.json'
plan = json.loads(plan_file.read_text(encoding='utf-8-sig'))
for i, caption in enumerate(captions, 1):
    slot = plan['storyboard'][i]
    slot['scene_ko'] = caption
    slot['google_caption'] = caption + ' (AI 생성 이미지)'
    slot['output_file'] = f'images/post{i:02d}-v3.jpg'
    if i in (3, 5):
        slot['reference_paths'] = [str(work / 'images' / 'post01-v3.png')]
plan['replacement_status'] = '5 images generated, visually inspected, resized and placed in both manuscripts; local build pending'
plan_file.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')
print('Updated Google source, matching DB body, Naver source and image plan. Five v3 site assets copied.')

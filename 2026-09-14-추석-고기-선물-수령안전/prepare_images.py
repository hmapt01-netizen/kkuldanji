"""Article-local resizing only; preserve generated originals and shared tools."""
from pathlib import Path
import contextlib, hashlib, io, json, shutil, sys
from PIL import Image

WORK = Path(__file__).resolve().parent
sys.path.insert(0, str(WORK.parent / 'tools'))
import image_guard

manifest = json.loads((WORK / 'image_generation.json').read_text(encoding='utf-8'))
report = []
for row in manifest['assets']:
    name = row['id']
    original = WORK / 'image_originals' / (name + '.png')
    if not original.exists():
        shutil.copy2(row['original_source'], original)
    with Image.open(original) as image:
        original_size = image.size
        assert abs(image.width / image.height - 16/9) < 0.01
        scaled = image.convert('RGB').resize((1280, 720), Image.Resampling.LANCZOS)
        candidates = []
        for quality in range(80, 96):
            buf = io.BytesIO()
            scaled.save(buf, format='JPEG', quality=quality, optimize=True)
            candidates.append((quality, buf.getvalue()))
        preferred = [c for c in candidates if 150*1024 <= len(c[1]) <= 250*1024]
        quality, data = min(preferred or candidates, key=lambda c: (0 if 80 <= c[0] <= 85 else 1, abs(len(c[1])-200*1024)))
    output = WORK / 'images' / (name + '.jpg')
    output.write_bytes(data)
    with Image.open(output) as check:
        check.load()
        assert check.size == (1280, 720)
    report.append(dict(file=output.name, original_size=original_size, width=1280, height=720,
                       kb=round(len(data)/1024, 1), quality=quality,
                       sha256=hashlib.sha256(data).hexdigest()))
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    plan_ok = image_guard.validate_image_plan(str(WORK), require_approval=True)
    files_ok = image_guard.validate_images(str(WORK / 'images'))
(WORK / 'image_guard.log').write_text(buf.getvalue(), encoding='utf-8')
(WORK / 'image_review.json').write_text(json.dumps(dict(assets=report, existing_plan_guard=plan_ok,
    existing_file_guard=files_ok, visual_review='생성 결과 6장 직접 확인. 인물 연속성, 밀봉 포장, 손·온도계·라벨 확인.',
    limits='AI 연출 이미지이며 실제 온도 또는 배송 상태의 증거가 아님. Python 검사는 파일 규격·해시 범위.'), ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=False, indent=2))
assert plan_ok and files_ok

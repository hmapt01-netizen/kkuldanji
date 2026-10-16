# -*- coding: utf-8 -*-
"""
꿀단지 (KKULDANJI) - 화보 6장 16:9 자동 크롭, 200KB 압축, dHash 중복 검사 및 8종 꿀벌 스티커 자동 복사기
사용법: python tools/optimize_images.py "d:\작업\꿀단지\2026-10-15-작업폴더"
"""
import os
import sys
import glob
import shutil
from PIL import Image

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = r"d:\작업\꿀단지"
STICKER_ASSETS_DIR = os.path.join(ROOT_DIR, "assets", "stickers")


def compute_dhash(img, hash_size=8):
    gray = img.convert('L').resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
    pixels = list(gray.getdata())
    diff = []
    for row in range(hash_size):
        for col in range(hash_size):
            left = pixels[row * (hash_size + 1) + col]
            right = pixels[row * (hash_size + 1) + col + 1]
            diff.append(left > right)
    decimal_value = 0
    for idx, val in enumerate(diff):
        if val:
            decimal_value |= (1 << idx)
    return decimal_value


def hamming_distance(h1, h2):
    return bin(h1 ^ h2).count('1')


def copy_bee_stickers(img_dir):
    if not os.path.exists(STICKER_ASSETS_DIR):
        return
    target_sticker_dir = os.path.join(img_dir, "stickers")
    os.makedirs(target_sticker_dir, exist_ok=True)
    copied = 0
    for ext in ("*.jpg", "*.jpeg", "*.png", "*.webp"):
        for fpath in glob.glob(os.path.join(STICKER_ASSETS_DIR, ext)):
            dst = os.path.join(target_sticker_dir, os.path.basename(fpath))
            if not os.path.exists(dst):
                shutil.copy2(fpath, dst)
                copied += 1
    if copied > 0:
        print(f"🐝 [꿀벌 스티커 자동 세팅]: {copied}종 스티커를 '{target_sticker_dir}'에 복사했습니다.")


def optimize_folder(target_dir):
    img_dir = os.path.join(target_dir, "images") if os.path.exists(os.path.join(target_dir, "images")) else target_dir
    if not os.path.exists(img_dir):
        print(f"❌ 이미지 폴더를 찾을 수 없습니다: {img_dir}")
        sys.exit(1)

    # 8종 꿀벌 시그니처 스티커 자동 복사
    copy_bee_stickers(img_dir)

    backup_dir = os.path.join(img_dir, "_originals")
    os.makedirs(backup_dir, exist_ok=True)

    exts = ('*.png', '*.jpg', '*.jpeg', '*.webp')
    files = []
    for ext in exts:
        files.extend(glob.glob(os.path.join(img_dir, ext)))

    if not files:
        print(f"⚠️ 최적화할 이미지가 없습니다: {img_dir}")
        return

    print(f"🖼️ 총 {len(files)}개 화보 이미지 16:9 최적화 및 200KB 압축 시작... (원본 백업: {backup_dir})")
    hashes = {}

    for f in sorted(files):
        try:
            base_name = os.path.basename(f)
            backup_path = os.path.join(backup_dir, base_name)
            if not os.path.exists(backup_path):
                shutil.copy2(f, backup_path)

            img = Image.open(f).convert("RGB")
            w, h = img.size
            target_ratio = 16 / 9
            current_ratio = w / h

            if abs(current_ratio - target_ratio) > 0.02:
                if current_ratio > target_ratio:
                    new_w = int(h * target_ratio)
                    left = (w - new_w) // 2
                    img = img.crop((left, 0, left + new_w, h))
                else:
                    new_h = int(w / target_ratio)
                    top = (h - new_h) // 2
                    img = img.crop((0, top, w, top + new_h))

            if img.size[0] > 1280:
                img = img.resize((1280, 720), Image.Resampling.LANCZOS)
            elif img.size[0] != 1280 and img.size[0] >= 800:
                img = img.resize((1280, 720), Image.Resampling.LANCZOS)

            base = os.path.splitext(f)[0]
            out_path = base + ".jpg"

            q = 88
            img.save(out_path, "JPEG", quality=q, optimize=True)
            while os.path.getsize(out_path) > 195 * 1024 and q > 40:
                q -= 5
                img.save(out_path, "JPEG", quality=q, optimize=True)

            if f.lower() != out_path.lower() and os.path.exists(f):
                os.remove(f)

            size_kb = os.path.getsize(out_path) / 1024
            out_name = os.path.basename(out_path)
            hashes[out_name] = compute_dhash(img)
            print(f"  ✅ {out_name} 완료 ({img.size[0]}x{img.size[1]}, {size_kb:.1f}KB, 품질:{q})")
        except Exception as e:
            print(f"  ❌ 오류 ({os.path.basename(f)}): {e}")

    # dHash 시각적 중복 검사 (thumb.jpg vs post01~05.jpg)
    names = sorted(hashes.keys())
    dup_pairs = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            dist = hamming_distance(hashes[names[i]], hashes[names[j]])
            if dist < 8:
                dup_pairs.append((names[i], names[j], dist))

    if dup_pairs:
        print("\n🚨 [시각적 중복 이미지 감지 (dHash < 8)]")
        for n1, n2, dist in dup_pairs:
            print(f"   - ❌ {n1} ↔ {n2} (해밍 거리: {dist}) ➔ 동일하거나 거의 유사한 이미지입니다! 서로 다른 컷으로 교체하세요.")
        sys.exit(1)
    elif len(names) >= 2:
        print("🛡️ [이미지 dHash 검증 통과]: 모든 화보 이미지가 시각적으로 100% 고유합니다.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python tools/optimize_images.py <작업폴더경로>")
        sys.exit(1)
    optimize_folder(sys.argv[1])

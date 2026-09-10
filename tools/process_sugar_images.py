# -*- coding: utf-8 -*-
import os
import sys
from PIL import Image

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

src_map = {
    "thumb.jpg": r"C:\Users\lim\.gemini\antigravity\brain\55c785b0-aeaa-480a-ba32-41c502c604a9\sugar_thumb_1789039402809.jpg",
    "post01.jpg": r"C:\Users\lim\.gemini\antigravity\brain\55c785b0-aeaa-480a-ba32-41c502c604a9\sugar_post01_1789039383460.jpg",
    "post02.jpg": r"C:\Users\lim\.gemini\antigravity\brain\55c785b0-aeaa-480a-ba32-41c502c604a9\sugar_post02_1789039420870.jpg",
    "post03.jpg": r"C:\Users\lim\.gemini\antigravity\brain\55c785b0-aeaa-480a-ba32-41c502c604a9\sugar_post03_1789039441111.jpg",
    "post04.jpg": r"C:\Users\lim\.gemini\antigravity\brain\55c785b0-aeaa-480a-ba32-41c502c604a9\sugar_post04_1789039459549.jpg",
    "post05.jpg": r"C:\Users\lim\.gemini\antigravity\brain\55c785b0-aeaa-480a-ba32-41c502c604a9\sugar_post05_1789039479639.jpg"
}

target_dir = r"d:\작업\꿀단지\2026-09-10-fasting-blood-sugar-prediabetes\images"
os.makedirs(target_dir, exist_ok=True)

print("🖼️ 이미지 최적화 및 복사 시작...")

for name, src_path in src_map.items():
    dest_path = os.path.join(target_dir, name)
    if not os.path.exists(src_path):
        print(f"❌ 소스 파일 없음: {src_path}")
        sys.exit(1)

    with Image.open(src_path) as img:
        # RGB 변환
        if img.mode != "RGB":
            img = img.convert("RGB")
        
        # 16:9 비율 확인 및 리사이즈 (가로 1280, 세로 720 기준)
        w, h = img.size
        # 이미 16:9에 가까우므로 부드럽게 1280x720으로 최적화
        img_resized = img.resize((1280, 720), Image.Resampling.LANCZOS)
        
        # 250~350KB 타깃으로 품질 88 저장
        img_resized.save(dest_path, "JPEG", quality=88, optimize=True)
        size_kb = os.path.getsize(dest_path) / 1024.0
        print(f"  ✓ {name}: {img_resized.size[0]}x{img_resized.size[1]} ({size_kb:.1f} KB) -> {dest_path}")

print("🎉 모든 이미지 저장 및 최적화 완료!")

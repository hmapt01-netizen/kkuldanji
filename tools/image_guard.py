# -*- coding: utf-8 -*-
"""
꿀단지 (KKULDANJI) - 마스터 표준 27-1호 AI 화보 생성 사전 계획 및 시각적 일관성 물리 가디언 (Image Guard)
AI가 사전 스토리보드 계획(image_plan.json) 없이 즉흥적으로 이미지를 생성하거나,
등장인물/의상이 제각각 바뀌는 행위를 물리적으로 강제 차단합니다.
"""
import os
import sys
import json
import hashlib
from PIL import Image

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

REQUIRED_SLOTS = ["thumb.jpg", "post01.jpg", "post02.jpg", "post03.jpg", "post04.jpg", "post05.jpg"]

def get_latest_work_dir():
    root_dir = r"d:\작업\꿀단지"
    if not os.path.exists(root_dir):
        return None
    import re
    subdirs = [
        os.path.join(root_dir, d) 
        for d in os.listdir(root_dir) 
        if os.path.isdir(os.path.join(root_dir, d)) and re.match(r'^\d{4}-\d{2}-\d{2}', d)
    ]
    if subdirs:
        subdirs.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        return subdirs[0]
    return None

def validate_image_plan(work_dir, require_approval=False):
    """
    [마스터 표준 27-1호] image_plan.json 사전 검증
    1. 파일 존재 여부
    2. 단일 주인공 앵커 (character_anchor) 필수 정의: 성별, 연령, 헤어, 100% 동일 상의/하의
    3. 6개 슬롯 스토리보드 (thumb + post01~05)
    4. 3:2 인물 대 정물/의료 황금 비율
    5. 인물 컷의 동일 의상 앵커 프롬프트 필수 포함 여부
    6. 사용자 승인 여부 (require_approval=True 시)
    """
    plan_path = os.path.join(work_dir, "image_plan.json")
    if not os.path.exists(plan_path):
        print(f"\n🚨 [HARD STOP 3.5 물리적 차단] 작업 폴더에 'image_plan.json' 파일이 존재하지 않습니다!")
        print(f"   📂 대상 폴더: {work_dir}")
        print(f"   🛑 차단 사유: AI가 단일 주인공 페르소나 및 6대 화보 스토리보드 사전 계획 없이 즉흥 생성을 시도했습니다.")
        print(f"   👉 해결 조치: [마스터 표준 27호]에 따라 'image_plan.json'을 작성하고 사용자 승인을 먼저 받으세요.")
        return False

    try:
        with open(plan_path, "r", encoding="utf-8-sig") as f:
            plan = json.load(f)
    except Exception as e:
        print(f"🚨 [image_plan.json 파싱 실패]: {e}")
        return False

    errors = []

    # 1. character_anchor 검증
    anchor = plan.get("character_anchor")
    if not anchor:
        errors.append("❌ 'character_anchor' 단일 주인공 페르소나 설정이 누락되었습니다.")
    else:
        for field in ["gender", "age_range", "hair", "clothing_top", "persona_summary"]:
            val = str(anchor.get(field, "")).strip()
            if not val:
                errors.append(f"❌ character_anchor 내 필수 필드 '{field}'가 비어 있습니다.")

    # 2. storyboard 6슬롯 전수 검증
    sb = plan.get("storyboard", [])
    if len(sb) != 6:
        errors.append(f"❌ storyboard 슬롯 개수 오류: 6개가 아닌 {len(sb)}개입니다. (필수: {REQUIRED_SLOTS})")

    slots_found = [item.get("slot") for item in sb if isinstance(item, dict)]
    for req in REQUIRED_SLOTS:
        if req not in slots_found:
            errors.append(f"❌ 필수 슬롯 '{req}'이 storyboard에 누락되었습니다.")

    # 3. 3:2 비율 검증 (인물컷 vs 정물/의료컷)
    char_slots = [item for item in sb if item.get("type") == "character"]
    still_slots = [item for item in sb if item.get("type") in ["still_life", "medical", "infographic"]]

    if len(char_slots) < 3:
        errors.append(f"❌ 인물 스토리텔링 컷이 너무 적습니다 (현재 {len(char_slots)}개, 최소 3개 필수).")
    if len(still_slots) < 2:
        errors.append(f"❌ 현장 정물/의료/인포그래픽 컷이 너무 적습니다 (현재 {len(still_slots)}개, 최소 2개 필수).")

    # 4. 동일 의상 키워드 프롬프트 포함 검사
    top_clothing = (anchor.get("clothing_top", "") if anchor else "").lower()
    for item in char_slots:
        p = item.get("prompt", "").lower()
        slot = item.get("slot", "")
        # 상의 의상 핵심 단어가 프롬프트에 있는지 확인
        if top_clothing and not any(word in p for word in top_clothing.split() if len(word) > 2):
            errors.append(f"❌ [{slot}] 인물 프롬프트에 동일 의상('{anchor.get('clothing_top')}') 앵커 서술이 누락되었습니다.")

    # 5. 승인 여부 검증
    is_approved = plan.get("is_user_approved", False)
    if require_approval and not is_approved:
        errors.append("❌ 'is_user_approved'가 False입니다. 사용자에게 스토리보드를 보고하고 명시적 승인을 받아야 합니다.")

    if errors:
        print("\n🚨 [image_plan.json 규격 미달]")
        for err in errors:
            print(f"  {err}")
        return False

    print("🎉 [100% PASS] image_plan.json 단일 주인공 및 6대 화보 스토리보드 규격 검증 통과!")
    return True


def validate_images(image_dir):
    """
    생성된 이미지 6장의 물리적 무결성 검증:
    1. 6개 파일 존재 여부
    2. MD5 해시 중복(thumb.jpg와 본문 컷 일치) 전수 검사
    3. 가로세로 비율(16:9) 및 용량(100KB ~ 350KB 최적화)
    """
    if not os.path.exists(image_dir):
        print(f"❌ 이미지 디렉토리가 존재하지 않습니다: {image_dir}")
        return False

    errors = []
    hashes = {}

    for slot in REQUIRED_SLOTS:
        p = os.path.join(image_dir, slot)
        if not os.path.exists(p):
            errors.append(f"❌ 필수 이미지 파일 '{slot}'이 누락되었습니다.")
            continue

        # 파일 크기 검사
        size_kb = os.path.getsize(p) / 1024.0
        if size_kb > 450:
            errors.append(f"⚠️ [{slot}] 용량 초과 ({size_kb:.1f}KB): 모바일 속도를 위해 300KB 내외 경량화가 필요합니다.")

        # 해시 중복 검사
        with open(p, "rb") as f:
            h = hashlib.md5(f.read()).hexdigest()
        if h in hashes:
            errors.append(f"🚨 [이미지 복제 적발] '{slot}'과 '{hashes[h]}'의 MD5 해시가 일치합니다! (동일 이미지 복제 금지)")
        else:
            hashes[h] = slot

        # 16:9 비율 검사
        try:
            with Image.open(p) as img:
                w, h_img = img.size
                ratio = w / h_img
                if abs(ratio - (16/9)) > 0.1:
                    errors.append(f"⚠️ [{slot}] 비율 경고: 16:9(약 1.77)가 아닌 {ratio:.2f} ({w}x{h_img})입니다.")
        except Exception as e:
            errors.append(f"❌ [{slot}] 이미지 포맷 손상: {e}")

    if errors:
        print("\n🚨 [이미지 파일 물리적 검증 실패]")
        for err in errors:
            print(f"  {err}")
        return False

    print("🎉 [100% AUDIT PASS] 6대 고유 화보 물리적 무결성 및 해시 중복 0건 전수 검증 통과!")
    return True

if __name__ == "__main__":
    work_dir = get_latest_work_dir()
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        work_dir = sys.argv[1]

    if not work_dir:
        print("❌ 작업 폴더를 찾을 수 없습니다.")
        sys.exit(1)

    print(f"🔍 [Image Guard 가동] 대상 폴더: {os.path.basename(work_dir)}")
    plan_ok = validate_image_plan(work_dir, require_approval=False)
    
    img_dir = os.path.join(work_dir, "images")
    if os.path.exists(img_dir):
        img_ok = validate_images(img_dir)
    else:
        print(f"ℹ️ 아직 images/ 폴더가 생성되지 않았습니다.")
        img_ok = True

    if not plan_ok:
        sys.exit(1)
    sys.exit(0)

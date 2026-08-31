import os
import sys
import json
import shutil
import subprocess

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

VALID_CATEGORIES = ["식단 & 영양", "홈트레이닝", "라이프 웰니스"]

def add_post(post_data, image_dir=None):
    """
    꿀단지 - 신규 칼럼 원스톱 자동 등록 및 일괄 컴파일 엔진
    """
    print(f"🚀 [꿀단지 신규 글 자동 등록 엔진 가동] '{post_data.get('title', '')}'")

    # 1. 카테고리 엄격 검증
    cat = post_data.get("category", "")
    if cat not in VALID_CATEGORIES:
        print(f"⚠️ [카테고리 오류] 입력된 카테고리 '{cat}'은 허용되지 않습니다. (허용: {VALID_CATEGORIES})")
        if "식단" in cat or "영양" in cat or "음식" in cat or "과일" in cat:
            cat = "식단 & 영양"
        elif "운동" in cat or "홈트" in cat or "자세" in cat or "스트레칭" in cat:
            cat = "홈트레이닝"
        else:
            cat = "라이프 웰니스"
        print(f"  ➔ '{cat}' 카테고리로 자동 보정되었습니다.")
        post_data["category"] = cat

    # 2. 이미지 자동 복사 (지정된 경우)
    slug_key = post_data.get("slugKey", post_data.get("slug", "").replace(".html", ""))
    target_img_dir = os.path.join(r"d:\작업\꿀단지\kkuldanji_web\images\posts", slug_key)
    
    if image_dir and os.path.exists(image_dir):
        os.makedirs(target_img_dir, exist_ok=True)
        img_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        print(f"  📁 {len(img_files)}개 이미지를 {target_img_dir}로 복사 중...")
        for img in img_files:
            shutil.copy2(os.path.join(image_dir, img), os.path.join(target_img_dir, img))
        print(f"  ✓ 이미지 복사 완료")

    # 3. posts_db.json 최상단(1번) 자동 삽입
    db_path = r"d:\작업\꿀단지\data\posts_db.json"
    with open(db_path, "r", encoding="utf-8-sig") as f:
        posts = json.load(f)

    # 기존 글 isLatest = False 설정
    for p in posts:
        p["isLatest"] = False

    post_data["isLatest"] = True
    
    # 중복 slug 검사
    existing_idx = next((i for i, p in enumerate(posts) if p["slug"] == post_data["slug"]), None)
    if existing_idx is not None:
        posts.pop(existing_idx)
        print(f"  🔄 기존 등록된 글 '{post_data['slug']}'을 최신 데이터로 갱신합니다.")

    posts.insert(0, post_data)

    with open(db_path, "w", encoding="utf-8-sig") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

    print(f"  ✓ posts_db.json 최상단(1번 자리) 등록 완료 (총 {len(posts)}편)")

    # 4. build_site.py 자동 실행하여 전체 사이트 일괄 컴파일
    print("  ⚙️ 정석 SSG 컴파일러 자동 가동 중...")
    build_script = r"d:\작업\꿀단지\tools\build_site.py"
    res = subprocess.run([sys.executable, build_script], capture_output=True, text=True, encoding="utf-8")
    print(res.stdout)
    if res.returncode != 0:
        print("❌ 빌드 오류:", res.stderr)
        return False

    print("🎉 [완전 자동화 완료] 꿀단지 신규 글 등록 ➔ SSG 컴파일이 원스톱으로 완료되었습니다!")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        with open(sys.argv[1], "r", encoding="utf-8-sig") as f:
            data = json.load(f)
        add_post(data)
    else:
        print("사용법: python add_post.py [post_data.json]")

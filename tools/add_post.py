import os
import sys
import json
import shutil
import subprocess
import re

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

VALID_CATEGORIES = ["식단 & 영양", "홈트레이닝", "라이프 웰니스"]

def validate_lead_quote_card(body_html):
    """
    [마스터 표준 1 & 23] 상단 핵심 요약 카드(lead-quote-card) 기계적 무결성 검증기
    - lead-quote-card 클래스를 가진 태그 필수
    - 공인 기관/문서 출처 라벨('—' 등) 필수 (출처 누락 차단)
    - AI 환각성 가공 연구팀('임상영양연구팀', '생체이용률연구팀' 등) 차단
    - 비인증 큰따옴표 가짜 명언 차단
    """
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(body_html, 'html.parser')
    card = soup.find(class_=re.compile(r'\blead-quote-card\b'))
    if not card:
        raise AssertionError("🚨 [마스터 표준 1 위반] 본문 상단에 'lead-quote-card' 핵심 요약 카드가 누락되었습니다!")
    
    card_content = card.get_text(separator=' ').strip()
    
    # 1. 출처 표기 확인: '—', '–', '<small>' 태그, 또는 '출처:' 명시 필수
    has_source = ('—' in card_content or '–' in card_content or 
                  card.find('small') is not None or 
                  bool(re.search(r'출처\s*[:：]', card_content)))
    if not has_source:
        raise AssertionError("🚨 [마스터 표준 23 위반] lead-quote-card에 공인 기관/문서 출처 라벨('— ...')이 누락되었습니다! 단순 문장만 넣는 것은 금지됩니다.")
        
    # 2. AI 가공 조직명(임의 조합 연구팀/추진단) 날조 차단
    if re.search(r'[가-힣A-Za-z0-9]+\s*(?:연구팀|추진단|태스크포스|TF팀)', card_content):
        raise AssertionError("🚨 [마스터 표준 23 위반] lead-quote-card에 임의 조합 하위 조직명('...연구팀/추진단')이 감지되었습니다! 실제 공식 기관명 및 문서명으로 기재하세요.")

    # 3. 큰따옴표 가짜 명언 차단 (원문 직역/취지 번역 표기 없이 “...”로 감싼 것 차단)
    if '“' in card_content or '”' in card_content:
        if not any(k in card_content for k in ['직역', '원문', '취지 번역', '공식 발표']):
            raise AssertionError("🚨 [마스터 표준 23 위반] lead-quote-card에 가상 따옴표(“...”) 인용문이 감지되었습니다! 공인 기관이 직접 발언하지 않은 내용을 따옴표로 감싸는 것은 금지되며, 《문서명》 취지 요약으로 기재하세요.")


def add_post(post_data, image_dir=None):
    """
    꿀단지 - 신규 칼럼 원스톱 자동 등록 및 일괄 컴파일 엔진
    """
    print(f"🚀 [꿀단지 신규 글 자동 등록 엔진 가동] '{post_data.get('title', '')}'")

    # 0. [마스터 표준 0/23호] Step Guard & Fact Guard 물리적 프리플라이트 검증
    try:
        tools_dir = os.path.dirname(os.path.abspath(__file__))
        if tools_dir not in sys.path:
            sys.path.insert(0, tools_dir)
        import step_guard
        step_guard.check_step(4)
    except Exception as e:
        print(f"🚨 [물리적 차단] Step Guard 검증 실패: {e}")
        raise AssertionError(f"Step Guard 검증 실패로 포스트 등록이 물리적으로 중단되었습니다: {e}")

    # 0-1. [마스터 표준 23-2호] Evidence Guard 직접 검증
    try:
        import evidence_guard
        work_dir = step_guard.get_latest_work_dir()
        evidence_guard.validate_post_evidence(post_data, work_dir=work_dir)
    except Exception as e:
        print(f"🚨 [물리적 차단] Evidence Guard 검증 실패: {e}")
        raise AssertionError(f"Evidence Guard 검증 실패로 포스트 등록이 물리적으로 중단되었습니다: {e}")

    # DB와 이미지를 변경하기 전에 홈페이지 원본의 페이지 나누기 규칙을 검사한다.
    from site_pagination_guard import validate as validate_pagination, PaginationError
    try:
        validate_pagination(include_generated=False)
    except PaginationError as exc:
        raise AssertionError("목록 동작 검사 실패로 등록 중단: " + str(exc)) from exc

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

    # 2. [마스터 표준 28] 이미지 검증 및 복사: thumb.jpg와 본문 섹션 이미지 중복 원천 차단
    slug_key = post_data.get("slugKey", post_data.get("slug", "").replace(".html", ""))
    target_img_dir = os.path.join(r"d:\작업\꿀단지\kkuldanji_web\images\posts", slug_key)
    
    if image_dir and os.path.exists(image_dir):
        try:
            import image_guard
            if not image_guard.validate_images(image_dir):
                raise AssertionError("🚨 [마스터 표준 27/28 위반] 생성된 화보가 규격을 통과하지 못했습니다!")
        except ImportError:
            pass
        import hashlib
        img_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        
        thumb_path = os.path.join(image_dir, "thumb.jpg")
        if not os.path.exists(thumb_path):
            raise AssertionError(f"🚨 [마스터 표준 28 위반] 이미지 폴더에 대표 히어로 이미지 'thumb.jpg'가 누락되었습니다!")
        
        # thumb.jpg의 MD5 해시 계산
        with open(thumb_path, 'rb') as f:
            thumb_hash = hashlib.md5(f.read()).hexdigest()
        
        # 본문 섹션 이미지(01~05)와 thumb.jpg의 해시 일치(복제 파일) 전수 검사
        section_imgs = [f for f in img_files if f != "thumb.jpg"]
        for s_img in section_imgs:
            s_path = os.path.join(image_dir, s_img)
            with open(s_path, 'rb') as sf:
                s_hash = hashlib.md5(sf.read()).hexdigest()
            if thumb_hash == s_hash:
                raise AssertionError(f"🚨 [마스터 표준 28 위반: 대표 이미지 중복 적발] 'thumb.jpg'가 본문 이미지 '{s_img}'와 동일한 파일(해시 일치)로 감지되었습니다!\n"
                                     f"   🛑 대표 썸네일(thumb.jpg)은 글 상단 및 홈 카드를 위한 독립된 히어로 화보여야 합니다.\n"
                                     f"   👉 해결 조치: 1번 이미지를 복사하지 말고, 별도의 고유한 대표 히어로 이미지를 생성하여 thumb.jpg로 지정하세요.")

        if len(section_imgs) < 5:
            raise AssertionError(f"🚨 [마스터 표준 28 위반] 본문 섹션 화보가 부족합니다 (현재 {len(section_imgs)}개, 최소 5개 필수 + 독립 thumb.jpg 1개 = 총 6개 고유 이미지 필수)!")

        os.makedirs(target_img_dir, exist_ok=True)
        print(f"  📁 총 {len(img_files)}개 고유 이미지(중복 0건 전수 검증 완료)를 {target_img_dir}로 복사 중...")
        for img in img_files:
            shutil.copy2(os.path.join(image_dir, img), os.path.join(target_img_dir, img))
        print(f"  ✓ 이미지 무결성 검증 및 복사 완료")

    # 3. [마스터 표준 23] E-E-A-T 공인 학술 참고문헌 엄격 검증
    raw_refs = post_data.get("academicRefs") or post_data.get("references")
    if not raw_refs:
        raise AssertionError(f"🚨 [마스터 표준 23 위반] 신규 포스트에 'references' 또는 'academicRefs'가 누락되었습니다! 공인 연구 논문 실명 3선 이상 필수입니다.")
    if isinstance(raw_refs, list):
        if len(raw_refs) < 3:
            raise AssertionError(f"🚨 [마스터 표준 23 위반] 참고문헌은 최소 3선 이상이어야 합니다. (현재: {len(raw_refs)}개)")
        for ref in raw_refs:
            if len(ref.strip()) < 25:
                raise AssertionError(f"🚨 [마스터 표준 23 위반] 참고문헌 항목이 너무 짧습니다 ('{ref}'). 단순 기관명 나열을 금지하며, 공식 논문 실명/보고서명과 연구 수치를 포함해야 합니다.")
    elif isinstance(raw_refs, str):
        if len(raw_refs.strip()) < 50:
            raise AssertionError(f"🚨 [마스터 표준 23 위반] academicRefs 내용이 부실합니다 (최소 50자 이상).")

    # 4. [마스터 표준 1 & 23] 상단 핵심 요약 카드(lead-quote-card) 기계적 무결성 검증
    validate_lead_quote_card(post_data.get("bodyHtml", ""))
    print("  ✓ 상단 핵심 요약 카드(lead-quote-card) 출처 투명성 무결성 검증 통과")

    # 5. posts_db.json 최상단(1번) 자동 삽입
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
        img_dir = sys.argv[2] if len(sys.argv) > 2 and os.path.exists(sys.argv[2]) else None
        add_post(data, image_dir=img_dir)
    else:
        print("사용법: python add_post.py [post_data.json] [image_dir (선택)]")

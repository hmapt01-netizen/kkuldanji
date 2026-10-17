# -*- coding: utf-8 -*-
"""
꿀단지 (KKULDANJI) - 마스터 제목 공식 및 플랫폼 분리 금칙어 기계적 자동 검증기 (Title Validator)
- 네이버 전용 감점 단어는 네이버 제목(naver_10)에만 적용합니다 (구글 오염 원천 금지).
- 구글 제목(google_10)에서는 '진단', '치료', '병원', '추천', '가격', '비교', '가이드' 등 자연 검색어를 전면 허용합니다.
- 구형 SERP 크롤링 락(collect_title_evidence)을 폐기하고 즉시 검증합니다.
"""
import sys
import os
import re
import json

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = r"d:\작업\꿀단지"

COMMON_FORBIDDEN_WORDS = [
    "실익", "셈법", "맹점", "완치", "100% 치료", "암세포 박멸", "기적의 특효약", "즉각 완치", "만병통치"
]
DAUM_FORBIDDEN_WORDS = list(COMMON_FORBIDDEN_WORDS)

NAVER_FORBIDDEN_WORDS = [
    "최고", "완벽", "추천", "가격", "구매", "할인", "무료",
    "이벤트", "1위", "최저가", "총정리", "진단", "치료", "처방", "약국", "병원", "의사",
    "실익", "셈법", "맹점", "완치", "100% 치료", "암세포 박멸", "기적의 특효약", "즉각 완치"
]

# 구글은 공통 번역투/만병통치 과장 표현만 차단하며, 진단/치료/병원/추천/가격/가이드 등 대중 검색어는 전면 허용
GOOGLE_FORBIDDEN_WORDS = list(COMMON_FORBIDDEN_WORDS)


def get_latest_work_dir():
    if not os.path.exists(ROOT_DIR):
        return None
    subdirs = [
        os.path.join(ROOT_DIR, d)
        for d in os.listdir(ROOT_DIR)
        if os.path.isdir(os.path.join(ROOT_DIR, d)) and re.match(r'^\d{4}-\d{2}-\d{2}', d)
    ]
    if subdirs:
        subdirs.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        return subdirs[0]
    return None


def validate_naver_titles(titles, run_serp=False, search_queries=None):
    """
    네이버 블로그 마스터 제목 10선 공식 검증 ([트랙 A: 홈판형 5선] + [트랙 B: 하이브리드형 5선])
    """
    print("🔍 [네이버 제목 10선 2대 트랙(홈판형 5선 + 하이브리드형 5선) 공식 기계적 검증 시작]")
    errors = []

    if len(titles) != 10:
        errors.append(f"❌ 제목 개수 오류: 10개가 아닌 {len(titles)}개입니다.")

    for idx, title in enumerate(titles, 1):
        found_forbidden = [w for w in NAVER_FORBIDDEN_WORDS if w in title]
        if found_forbidden:
            errors.append(f"❌ {idx}번 네이버 제목 금칙어 적발: {found_forbidden} -> '{title}'")

        # 트랙 A (1~3번 이상): 홈판형 독백/대화 따옴표 훅 검증
        if 1 <= idx <= 3:
            if not ('"' in title or '“' in title or "'" in title or '‘' in title):
                errors.append(f"❌ 트랙 A(홈판형) 규격 미달 ({idx}번): 생생한 독백/대화 따옴표 훅('\"...\"')이 누락되었습니다 -> '{title}'")

        if "..." in title:
            errors.append(f"❌ 말줄임표('...') 혼입 ({idx}번): 물음표/쉼표/구어체로 깔끔하게 종결하세요 -> '{title}'")

        clean_len = len(title.strip())
        if clean_len > 46:
            errors.append(f"❌ 글자 수 초과 ({idx}번, {clean_len}자): 네이버 모바일 가독성을 위해 46자 이하여야 합니다 (권장 25~38자) -> '{title}'")
        elif clean_len < 16:
            errors.append(f"❌ 글자 수 부족 ({idx}번, {clean_len}자): 최소 16자 이상이어야 합니다 -> '{title}'")

    if errors:
        print("\n🚨 [검증 실패: 네이버 제목 규격 미달]")
        for err in errors:
            print(f"  {err}")
        return False

    print("🎉 [100% 검증 통과] 네이버 제목 10선이 [트랙 A: 홈판형 5선] + [트랙 B: 하이브리드형 5선] 규격을 완벽히 충족했습니다!")
    return True


GOOGLE_BLIND_WORDS = [
    "이것", "이 질환", "이 증상", "이 음식", "이 영양제", "이 자세", "이 습관", "이 방법", "이 동작", "이 병"
]

GOOGLE_COMPLEX_UNITS = [
    "mmHg", "g/dL", "mg/dL", "μg/L", "ug/L", "mL", "kcal", "mcg"
]


def validate_google_titles(titles, run_serp=False, search_queries=None):
    """
    꿀단지 구글 본진 듀얼 트랙 제목 10선 공식 검증
    ([트랙 A: 검색·진료 가이드형 5선] + [트랙 B: 디스커버·착각 반전형 5선])
    """
    print("🔍 [구글 본진 제목 10선 듀얼 트랙(검색·진료 가이드형 5선 + 디스커버·착각 반전형 5선) 공식 기계적 검증 시작]")
    errors = []

    if len(titles) != 10:
        errors.append(f"❌ 제목 개수 오류: 10개가 아닌 {len(titles)}개입니다. ([트랙 A 5선] + [트랙 B 5선] 총 10개 필수)")

    for idx, title in enumerate(titles, 1):
        track_label = "트랙 A(검색·진료형)" if idx <= 5 else "트랙 B(디스커버·반전형)"

        found_forbidden = [w for w in GOOGLE_FORBIDDEN_WORDS if w in title]
        if found_forbidden:
            errors.append(f"❌ {idx}번 [{track_label}] 공통 금칙어 적발: {found_forbidden} -> '{title}'")

        if "..." in title or "…" in title:
            errors.append(f"❌ {idx}번 [{track_label}] 말줄임표('...' 또는 '…') 혼입 -> '{title}'")

        if ":" in title or "：" in title:
            errors.append(f"❌ {idx}번 [{track_label}] 구형 콜론(':') 키워드 나열식 적발 (자연스러운 문장형 필수) -> '{title}'")

        found_blind = [w for w in GOOGLE_BLIND_WORDS if w in title]
        if found_blind:
            errors.append(f"❌ {idx}번 [{track_label}] 블라인드 지시어 은닉 적발 ({found_blind}, 정식 명칭 명시 필수) -> '{title}'")

        found_units = [u for u in GOOGLE_COMPLEX_UNITS if re.search(re.escape(u), title, re.IGNORECASE)]
        if found_units:
            errors.append(f"❌ {idx}번 [{track_label}] 복잡한 임상·계량 단위 노출 적발 ({found_units}, 본문에만 수록하고 제목에는 쉬운 해답 개수 N가지 사용) -> '{title}'")

        clean_len = len(title.strip())
        if clean_len > 46:
            errors.append(f"❌ 글자 수 초과 ({idx}번 [{track_label}], {clean_len}자): 모바일 완독을 위해 46자 이하여야 합니다 -> '{title}'")
        elif clean_len < 24:
            errors.append(f"❌ 글자 수 부족 ({idx}번 [{track_label}], {clean_len}자): 최소 24자 이상이어야 합니다 -> '{title}'")

    if errors:
        print("\n🚨 [검증 실패: 구글 듀얼 트랙 제목 규격 미달]")
        for err in errors:
            print(f"  {err}")
        return False

    print("🎉 [100% 검증 통과] 구글 본진 제목 10선이 [트랙 A: 검색·진료 가이드형 5선] + [트랙 B: 디스커버·착각 반전형 5선] 규격을 완벽히 충족했습니다!")
    return True


def validate_daum_titles(titles):
    errors = []
    if len(titles) != 10:
        errors.append(f"❌ 제목 개수 오류: {len(titles)}개")
    for idx, title in enumerate(titles, 1):
        found = [w for w in DAUM_FORBIDDEN_WORDS if w in title]
        if found:
            errors.append(f"❌ {idx}번 금칙어: {found}")
    return len(errors) == 0


if __name__ == "__main__":
    mode = "auto"
    target_path = None

    if len(sys.argv) > 1:
        if sys.argv[1] in ["naver", "google", "daum"]:
            mode = sys.argv[1]
            if len(sys.argv) > 2:
                target_path = sys.argv[2]
        elif os.path.exists(sys.argv[1]):
            target_path = sys.argv[1]

    if not target_path:
        latest = get_latest_work_dir()
        if latest and os.path.exists(os.path.join(latest, "titles.json")):
            target_path = os.path.join(latest, "titles.json")

    if not target_path or not os.path.exists(target_path):
        print("❌ 검증할 titles.json 파일을 찾을 수 없습니다.")
        sys.exit(1)

    with open(target_path, "r", encoding="utf-8-sig") as f:
        data = json.load(f)

    all_ok = True
    if isinstance(data, dict):
        naver_list = data.get("naver_10") or data.get("naver_candidates") or data.get("naver") or []
        google_list = data.get("google_10") or data.get("google_candidates") or data.get("google") or []

        if mode == "naver" or (mode == "auto" and naver_list):
            all_ok = validate_naver_titles(naver_list) and all_ok
        if mode == "google" or (mode == "auto" and google_list):
            all_ok = validate_google_titles(google_list) and all_ok
    elif isinstance(data, list):
        if mode == "google":
            all_ok = validate_google_titles(data)
        else:
            all_ok = validate_naver_titles(data)

    sys.exit(0 if all_ok else 1)

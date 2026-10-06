# -*- coding: utf-8 -*-
"""
꿀단지 (KKULDANJI) - 마스터 제목 공식 및 실시간 SERP 기계적 자동 검증기 (Title Validator)
AI가 짐작이나 기억에 의존해 공식을 왜곡하거나 금칙어를 포함하는 행위를 물리적으로 차단하고,
형식 검사와 검색 수집을 분리하며, 문구 점수로 노출 가능성을 판단하지 않습니다.
"""
import sys
import os
import re
import json
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

COMMON_FORBIDDEN_WORDS = ["실익", "셈법", "맹점"]
DAUM_FORBIDDEN_WORDS = ["실익", "셈법", "맹점"]

NAVER_FORBIDDEN_WORDS = [
    "해요", "하더라", "가격", "구매", "판매", "할인", "진단",
    "가장", "최고", "최상", "1위", "추천", "블로그", "정확",
    "대출", "금융", "사이트", "인사이트", "100%", "최초",
    "만족", "확실", "방지", "후회", "충격", "폭탄", "민낯",
    "처절한", "서늘한", "만땅", "셈법", "실익", "맹점", "발칵",
    "실체", "반전", "놀란 이유", "깜짝 놀란"
]

GOOGLE_FORBIDDEN_WORDS = list(dict.fromkeys(NAVER_FORBIDDEN_WORDS + COMMON_FORBIDDEN_WORDS))

try:
    from audit_serp_live import audit_titles
except ImportError:
    try:
        from tools.audit_serp_live import audit_titles
    except ImportError:
        audit_titles = None


def extract_health_keyword_triad(title):
    """
    [마스터 표준 27-4] 건강/웰니스 제목 10선 🔑 키워드 3단 조합 자동 분해 엔진
    - 🔑 메인 필수 검색어 (Core Demand): 대형 트래픽 바닥 (질환/식품/검진/영양소)
    - 🔗 실시간 연관 검색어 (Related Intent): 실제 유저 불편/상황/증상 (복용시간/공복/당일/통증/부작용)
    - 💡 독창적 아이디어 변주 (Unique Variation): 대형 병원 칼럼 결손 공략 (골든타임/3분대처/라벨판별/시차)
    """
    cleaned = re.sub(r'["“\'”\?!\(\)\[\]·,]', ' ', title)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    words = cleaned.split()

    quote_match = re.search(r'["“\']([^"”\']+)["”\']', title)
    quote_text = quote_match.group(1).strip() if quote_match else ""

    # 1. 💡 변주(Variation): 해결책, 셈법, 행동 요령, 골든타임 등 추출
    variation_patterns = [
        r'\b\d+분\s*대처[법]*\b', r'\b골든타임\b', r'\b\d+초\s*판별[법]*\b', r'\b반감기\s*시간표\b',
        r'\b시간표\b', r'\b성분표\s*\d+초\b', r'\b\d+분\s*시차\b', r'\b성분\s*셈법\b', r'\b대조\b',
        r'\b손익\b', r'\b체크리스트\b', r'\b구별법\b', r'\b판별법\b', r'\b현실\s*검증\b',
        r'\b행동\s*요령\b', r'\b주의점\b', r'\b3초\s*판별\b'
    ]
    variation = ""
    for pat in variation_patterns:
        m = re.search(pat, cleaned)
        if m:
            variation = m.group(0)
            break
    if not variation:
        if len(words) >= 2:
            variation = " ".join(words[-2:])
        else:
            variation = "실천 솔루션"

    # 2. 🔑 메인어(Core): 제목 전면의 1~2개 핵심 명사
    if quote_text and len(words) >= 3:
        after_quote = cleaned.replace(quote_text, '').strip().split()
        core = " ".join(after_quote[:2]) if len(after_quote) >= 2 else (after_quote[0] if after_quote else words[0])
    else:
        core = " ".join(words[:2]) if len(words) >= 2 else words[0]

    # 3. 🔗 연관어(Related): 메인어와 변주를 제외한 중간 롱테일/상황어
    related_candidates = [
        w for w in words 
        if w not in core.split() and w not in variation.split() and len(w) >= 2
        and w not in ["이유와", "따른", "위한", "대한", "관련", "분석", "팩트체크", "정리"]
    ]
    if related_candidates:
        related = ", ".join(related_candidates[:3])
    else:
        related = "실시간 연관 수요"

    return core, related, variation


def calculate_low_authority_score(title, audit_record):
    return None, ["문구 기반 노출 점수는 사용하지 않습니다"]


def render_evidence_table(records):
    try:
        from blue_ocean import evaluate
    except ImportError:
        try:
            from tools.blue_ocean import evaluate
        except ImportError:
            try:
                import sys, os
                sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
                from blue_ocean import evaluate
            except Exception:
                evaluate = lambda r: {'badge': '⚠️ 미확인', 'reason': '평가기 로드 실패'}
    print("| 번호 | 제목 | 검색 질문 | 검토 상태 | 근거 / 미확인 |")
    print("|---|---|---|---|---|")
    for record in records:
        result = evaluate(record)
        values = [record.get('idx'), record.get('title'), record.get('clean_query', ''),
                  result['badge'], result['reason']]
        print('| ' + ' | '.join(str(v).replace('|', '&#124;').replace('\n', ' ') for v in values) + ' |')
    print("자동 추천 보류. 후보의 상대적 우선순위는 topic_opportunity 보고서에서 근거와 함께 판단합니다.")
    return None


def collect_title_evidence(titles, channel, search_queries):
    if not search_queries or len(search_queries) != len(titles) or any(not isinstance(q, str) or not q.strip() for q in search_queries):
        raise ValueError("제목 순서에 맞는 search_queries가 필요합니다. 제목을 잘라 검색하지 않습니다.")
    import contextlib
    import io
    records = audit_titles(search_queries, channel=channel)
    for title, record in zip(titles, records):
        record['title'] = title
    with contextlib.redirect_stdout(io.StringIO()) as output:
        render_evidence_table(records)
    report = output.getvalue()
    print(report)
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    os.makedirs(data_dir, exist_ok=True)
    with open(os.path.join(data_dir, f'last_{channel}_titles_audit.json'), 'w', encoding='utf-8') as f:
        json.dump(dict(timestamp=datetime.now().astimezone().isoformat(), channel=channel,
            total_candidates=len(titles), report_schema=3, serp_table_rendered=True, triad_table_rendered=False,
            markdown_table=report, top_pick=None, records=records), f, ensure_ascii=False, indent=2)


def validate_naver_titles(titles, run_serp=True, search_queries=None):
    """
    네이버 블로그 마스터 제목 10선 공식 검증 및 [마스터 표준 27호] 실시간 SERP 실사
    """
    print("🔍 [네이버 제목 10선 공식 기계적 검증 시작]")
    errors = []

    if len(titles) != 10:
        errors.append(f"❌ 제목 개수 오류: 10개가 아닌 {len(titles)}개입니다.")

    for idx, title in enumerate(titles, 1):
        found_forbidden = [w for w in NAVER_FORBIDDEN_WORDS if w in title]
        if found_forbidden:
            errors.append(f"❌ {idx}번 네이버 제목 금칙어 적발: {found_forbidden} -> '{title}'")

        if 1 <= idx <= 3:
            if not ('"' in title or '“' in title or "'" in title):
                errors.append(f"❌ 그룹 1 규격 미달 ({idx}번): 따옴표 인플루언서 독백 훅('\"...\"')이 누락되었습니다 -> '{title}'")

        if "..." in title:
            errors.append(f"❌ 다음 채널 패턴 혼입 ({idx}번): 말줄임표('...')는 다음 채널 전용 훅입니다 -> '{title}'")

        clean_len = len(title.strip())
        if clean_len > 60:
            errors.append(f"❌ 글자 수 초과 ({idx}번, {clean_len}자): 네이버 검색 노출을 위해 60자 이하여야 합니다 (권장 25~55자) -> '{title}'")
        elif clean_len < 18:
            errors.append(f"❌ 글자 수 부족 ({idx}번, {clean_len}자): 검색 키워드 유입을 위해 최소 18자 이상이어야 합니다 -> '{title}'")

    if errors:
        print("\n🚨 [검증 실패: 규격 미달]")
        for err in errors:
            print(f"  {err}")
        return False

    print("\n🎉 [100% 검증 통과] 네이버 제목 10선이 3대 그룹 공식 및 금칙어(실익·셈법·맹점 포함) 0개를 완벽히 충족했습니다!")

    if run_serp:
        collect_title_evidence(titles, 'naver', search_queries)

    return True


def validate_daum_titles(titles):
    """
    다음(Daum) 채널 마스터 제목 10선 공식 검증
    - 총 10개 구성
    - 3단 결합 공식: 따옴표(" ") 훅 + 말줄임표(...) + 블라인드/수치/종결어
    - 다음 금칙어(실익, 셈법, 맹점) 0개
    """
    print("🔍 [다음 제목 10선 3단 결합 공식 및 금칙어 기계적 검증 시작]")
    errors = []

    if len(titles) != 10:
        errors.append(f"❌ 제목 개수 오류: 10개가 아닌 {len(titles)}개입니다.")

    for idx, title in enumerate(titles, 1):
        found_forbidden = [w for w in DAUM_FORBIDDEN_WORDS if w in title]
        if found_forbidden:
            errors.append(f"❌ {idx}번 다음 제목 금칙어 적발: {found_forbidden} -> '{title}'")

        if not ('"' in title or '“' in title):
            errors.append(f"❌ 1단계 훅 누락 ({idx}번): 전반부 따옴표(\" \") 인용/의문 훅이 없습니다 -> '{title}'")

        if "..." not in title and "… " not in title:
            errors.append(f"❌ 2단계 연결부 누락 ({idx}번): 중간 말줄임표('...') 호흡 단절이 누락되었습니다 -> '{title}'")

        clean_len = len(title.strip())
        if clean_len > 50:
            errors.append(f"❌ 글자 수 초과 ({idx}번, {clean_len}자): 카카오 다음 채널 등록 제한을 위해 반드시 50자 이내여야 합니다 (권장 40~48자) -> '{title}'")

    if errors:
        print("\n🚨 [검증 실패: 규격 미달]")
        for err in errors:
            print(f"  {err}")
        return False

    print("\n🎉 [100% 검증 통과] 다음 제목 10선이 3단 결합 공식 및 금칙어(실익·셈법·맹점) 0개를 완벽히 충족했습니다!")
    return True


def validate_google_titles(titles, run_serp=True, search_queries=None):
    """
    꿀단지 구글 본진 마스터 제목 10선 공식 검증 및 [마스터 표준 27호] 실시간 SERP 4단계 경쟁도 실사
    """
    print("🔍 [구글 본진 제목 10선 공식 기계적 검증 시작]")
    errors = []

    if len(titles) != 10:
        errors.append(f"❌ 제목 개수 오류: 10개가 아닌 {len(titles)}개입니다.")

    for idx, title in enumerate(titles, 1):
        found_forbidden = [w for w in GOOGLE_FORBIDDEN_WORDS if w in title]
        if found_forbidden:
            errors.append(f"❌ {idx}번 구글 제목 금칙어 적발: {found_forbidden} -> '{title}'")

        if "..." in title:
            errors.append(f"❌ 다음 채널 패턴 혼입 ({idx}번): 말줄임표('...')는 다음 채널 전용 훅입니다 -> '{title}'")

        clean_len = len(title.strip())
        if clean_len > 70:
            errors.append(f"❌ 글자 수 초과 ({idx}번, {clean_len}자): 구글 검색 결과 잘림 방지를 위해 70자 이하여야 합니다 (권장 25~65자) -> '{title}'")
        elif clean_len < 22:
            errors.append(f"❌ 글자 수 부족 ({idx}번, {clean_len}자): 검색 의도 및 E-E-A-T 신뢰도를 위해 최소 22자 이상이어야 합니다 -> '{title}'")

    if errors:
        print("\n🚨 [검증 실패: 규격 미달]")
        for err in errors:
            print(f"  {err}")
        return False

    print("\n🎉 [100% 검증 통과] 구글 본진 제목 10선이 규격 및 금칙어(실익·셈법 포함) 0개를 완벽히 충족했습니다!")

    if run_serp:
        collect_title_evidence(titles, 'google', search_queries)

    return True


if __name__ == "__main__":
    if len(sys.argv) > 1:
        mode = "auto"
        target_path = None
        if sys.argv[1] in ["naver", "google", "daum"]:
            mode = sys.argv[1]
            if len(sys.argv) > 2:
                target_path = sys.argv[2]
        elif os.path.exists(sys.argv[1]):
            target_path = sys.argv[1]

        if target_path and os.path.exists(target_path):
            with open(target_path, "r", encoding="utf-8-sig") as f:
                data = json.load(f)
            
            all_ok = True
            if mode == "google":
                titles = data if isinstance(data, list) else (data.get("google_candidates") if isinstance(data.get("google_candidates"), list) else data.get("google", []))
                all_ok = validate_google_titles(titles, search_queries=data.get('search_queries') if isinstance(data, dict) else None)
            elif mode == "daum":
                titles = data if isinstance(data, list) else (data.get("daum_candidates") if isinstance(data.get("daum_candidates"), list) else data.get("daum", []))
                all_ok = validate_daum_titles(titles)
            elif mode == "naver":
                titles = data if isinstance(data, list) else (data.get("naver_candidates") if isinstance(data.get("naver_candidates"), list) else data.get("naver", []))
                all_ok = validate_naver_titles(titles, search_queries=data.get('search_queries') if isinstance(data, dict) else None)
            else:
                if isinstance(data, list):
                    if any("..." in t for t in data):
                        all_ok = validate_daum_titles(data)
                    elif any(len(t) > 36 for t in data):
                        all_ok = validate_google_titles(data)
                    else:
                        all_ok = validate_naver_titles(data)
                elif isinstance(data, dict):
                    if "naver" in data:
                        all_ok = validate_naver_titles(data["naver"], search_queries=data.get("naver_search_queries", data.get("search_queries"))) and all_ok
                    if "daum" in data:
                        all_ok = validate_daum_titles(data["daum"]) and all_ok
                    if "google" in data:
                        all_ok = validate_google_titles(data["google"], search_queries=data.get("google_search_queries", data.get("search_queries"))) and all_ok
            
            if not all_ok:
                sys.exit(1)
            sys.exit(0)

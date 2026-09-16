# Existing Git HEAD scoring function, preserved verbatim. Heuristic score only; not measured ranking probability.
import re

def calculate_low_authority_score(title, audit_record):
    r"""
    [마스터 표준 26-1] 실전 대중 검색어 100% 탑재 및 '검색어 조합 + 살짝 변주(Twist) + 연관어 결합' 블루오션 채점 알고리즘 (0~100점)
    1. 대중 실전 검색어 1 + 상황적 살짝 변주(Twist 훅): 경험·상황 체감 훅 탑재 여부 (+20점)
    2. 대중 실전 검색어 2 (연관 검색어 조합) 보존: 실제 유저 검색 시드 단어 온전 보존 (+35점 / 누락 시 -30점)
    3. 구체적 수치/골든타임/행동 솔루션: 숫자(\d+초, \d+분 등) 및 구체적 실천 단위 결합 (+20점)
    4. 안티 클리셰 감점: 상투적 설명 명사(완화, 증상, 예방 등) 단순 나열 연쇄 (-25점)
    5. SERP 실사 경쟁도: 실시간 검색 결과 뱃지 (+30점 ~ -40점)
    """
    score = 0
    breakdowns = []
    
    # 1. 블록 A: 상황/체감 훅 (DIA+ 스마트블록 클릭률 및 경험 가산점)
    has_quote_hook = ('"' in title or '“' in title or "'" in title or '‘' in title)
    has_question_or_situation = ('?' in title or '때' in title or '라면' in title or '전' in title)
    if has_quote_hook or has_question_or_situation:
        score += 20
        breakdowns.append("✅ 블록 A: 경험·상황 체감 훅 탑재 (스마트블록 DIA+ 우대) (+20점)")
    else:
        score += 5
        breakdowns.append("ℹ️ 평서문 구조 (+5점)")

    # 2. 블록 B: 핵심 타깃 검색어 보존 여부 (검색량 0의 함정 방어)
    seed = audit_record.get("seed", "")
    seed_words = [w for w in seed.split() if len(w) >= 2]
    if seed_words:
        matched_seed = [w for w in seed_words if w in title]
        if len(matched_seed) == len(seed_words):
            score += 35
            breakdowns.append(f"✅ 블록 B: 핵심 검색어 '{seed}' 100% 온전 보존 (+35점)")
        elif len(matched_seed) >= 1:
            score += 20
            breakdowns.append(f"✅ 블록 B: 핵심 검색어 부분 보존 ({matched_seed[0]}) (+20점)")
        else:
            score -= 30
            breakdowns.append("🚨 블록 B 누락: 핵심 검색어 실종으로 검색 노출 불가 위험 (-30점)")
    else:
        score += 25
        breakdowns.append("✅ 핵심 검색 엔티티 반영 (+25점)")

    # 3. 블록 C: 구체적 수치/골든타임/차별화 행동 솔루션
    has_metrics = bool(re.search(r'\d+(?:초|분|시간|단계|가지|선|g|mg|kcal|대|배|일)', title))
    has_action = bool(re.search(r'(?:골든타임|타이밍|순서|요령|루틴|성분표|비결|라벨|수칙)', title))
    if has_metrics and has_action:
        score += 20
        breakdowns.append("✅ 블록 C: 구체적 수치 + 실천 행동 결합 (+20점)")
    elif has_metrics or has_action:
        score += 15
        breakdowns.append("✅ 블록 C: 구체적 수치 또는 실천 행동 결합 (+15점)")
    else:
        score += 5
        breakdowns.append("⚠️ 추상적 표현 (+5점)")

    # 4. 안티 클리셰 감점: 상투적 설명 명사 단순 나열(명사 연쇄) 적발
    # 상투적 설명 명사가 연속으로 붙어 형태소 유사도가 급증하는 패턴 적발
    cliche_chain_pattern = r'(?:완화|치료|예방|증상|원인|효능|방법|스트레칭|마사지|식단)\s*[,·]?\s*(?:완화|치료|예방|증상|원인|효능|방법|스트레칭|마사지|식단)'
    if re.search(cliche_chain_pattern, title):
        score -= 25
        breakdowns.append("⚠️ 상투적 설명 명사 연속 나열로 네이버 유사도 40%+ 위험 (-25점)")

    # 5. SERP 실사 뱃지 점수
    badge = audit_record.get("badge", "")
    if "💎" in badge:
        score += 30
        breakdowns.append("✅ SERP 실사 독점 빈집 (+30점)")
    elif "🟢" in badge:
        score += 25
        breakdowns.append("✅ SERP 실사 알짜 틈새 (+25점)")
    elif "🟡" in badge:
        score += 10
        breakdowns.append("🟡 SERP 중간 경쟁 (+10점)")
    elif "🔴" in badge:
        score -= 20
        breakdowns.append("🔴 SERP 초극심 레드오션 (-20점)")
    elif "⚠️" in badge:
        score -= 40
        breakdowns.append("⚠️ 허수 빈집(검색수요 0) (-40점)")

    final_score = max(0, min(100, score))
    return final_score, breakdowns

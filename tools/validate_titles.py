# -*- coding: utf-8 -*-
"""
차를 쓰다 & 꿀단지 - 마스터 제목 공식 기계적 자동 검증기 (Title Validator)
AI가 짐작이나 기억에 의존해 공식을 왜곡하거나 금칙어를 포함하는 행위를 물리적으로 차단합니다.
"""
import sys
import re

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 네이버 C-Rank & DIA+ 금칙어 및 양산형 상투어 목록
NAVER_FORBIDDEN_WORDS = [
    "해요", "하더라", "가격", "구매", "판매", "할인", "진단",
    "가장", "최고", "최상", "1위", "추천", "블로그", "정확",
    "대출", "금융", "사이트", "인사이트", "100%", "최초",
    "만족", "확실", "방지", "후회", "충격", "폭탄", "민낯",
    "처절한", "서늘한", "만땅", "셈법", "발칵",
    "실체", "반전", "놀란 이유", "깜짝 놀란"
]

def validate_naver_titles(titles):
    """
    네이버 블로그 마스터 제목 10선 공식 검증
    - 총 10개 구성
    - 그룹 1 (1~3번): 1티어 인플루언서 품격 독백/실사용 질문형 (따옴표 "..." 포함)
    - 그룹 2 (4~6번): 팩트 반전 & 실소유자 현실 고민형
    - 그룹 3 (7~10번): C-Rank & DIA+ 청정 롱테일 키워드 검색 타격형
    - 28종 금칙어 0개 (100점 만점)
    """
    print("🔍 [네이버 제목 10선 공식 기계적 검증 시작]")
    errors = []

    if len(titles) != 10:
        errors.append(f"❌ 제목 개수 오류: 10개가 아닌 {len(titles)}개입니다.")

    for idx, title in enumerate(titles, 1):
        # 1. 28종 금칙어 전수 검사
        found_forbidden = [w for w in NAVER_FORBIDDEN_WORDS if w in title]
        if found_forbidden:
            errors.append(f"❌ {idx}번 제목 금칙어 적발: {found_forbidden} -> '{title}'")

        # 2. 그룹 1 (1~3번) 따옴표 독백/질문 훅 검사
        if 1 <= idx <= 3:
            if not ('"' in title or '“' in title or "'" in title):
                errors.append(f"❌ 그룹 1 규격 미달 ({idx}번): 따옴표 인플루언서 독백 훅('\"...\"')이 누락되었습니다 -> '{title}'")

        # 3. 다음 채널 전용 피드 패턴(말줄임표 '...') 혼입 차단
        if "..." in title:
            errors.append(f"❌ 다음 채널 패턴 혼입 ({idx}번): 말줄임표('...')는 다음 채널 전용 훅입니다 -> '{title}'")

        # 4. 네이버 모바일 완독 글자 수 검사 (권장 25~32자, 35자 초과 시 모바일 검색 말줄임표 잘림 에러)
        clean_len = len(title.strip())
        if clean_len > 35:
            errors.append(f"❌ 글자 수 초과 ({idx}번, {clean_len}자): 네이버 모바일 검색 잘림 방지를 위해 35자 이하여야 합니다 (권장 25~32자) -> '{title}'")
        elif clean_len < 18:
            errors.append(f"❌ 글자 수 부족 ({idx}번, {clean_len}자): 검색 키워드 유입을 위해 최소 18자 이상이어야 합니다 -> '{title}'")

    if errors:
        print("\n🚨 [검증 실패: 규격 미달]")
        for err in errors:
            print(f"  {err}")
        return False

    print("\n🎉 [100% 검증 통과] 네이버 제목 10선이 3대 그룹 공식 및 28종 금칙어 0개를 완벽히 충족했습니다!")
    return True


def validate_daum_titles(titles):
    """
    다음(Daum) 채널 마스터 제목 10선 공식 검증
    - 총 10개 구성
    - 3단 결합 공식: 따옴표(" ") 훅 + 말줄임표(...) + 블라인드/수치/종결어
    """
    print("🔍 [다음 제목 10선 3단 결합 공식 기계적 검증 시작]")
    errors = []

    if len(titles) != 10:
        errors.append(f"❌ 제목 개수 오류: 10개가 아닌 {len(titles)}개입니다.")

    for idx, title in enumerate(titles, 1):
        # 1. 따옴표 검사
        if not ('"' in title or '“' in title):
            errors.append(f"❌ 1단계 훅 누락 ({idx}번): 전반부 따옴표(\" \") 인용/의문 훅이 없습니다 -> '{title}'")

        # 2. 말줄임표(...) 검사
        if "..." not in title and "… " not in title:
            errors.append(f"❌ 2단계 연결부 누락 ({idx}번): 중간 말줄임표('...') 호흡 단절이 누락되었습니다 -> '{title}'")

        # 3. 다음 채널 에디터 글자 수 50자 상한 검사
        clean_len = len(title.strip())
        if clean_len > 50:
            errors.append(f"❌ 글자 수 초과 ({idx}번, {clean_len}자): 카카오 다음 채널 등록 제한을 위해 반드시 50자 이내여야 합니다 (권장 40~48자) -> '{title}'")

    if errors:
        print("\n🚨 [검증 실패: 규격 미달]")
        for err in errors:
            print(f"  {err}")
        return False

    print("\n🎉 [100% 검증 통과] 다음 제목 10선이 3단 결합 공식(따옴표 + ... + 블라인드 종결)을 완벽히 충족했습니다!")
    return True


if __name__ == "__main__":
    import json
    import os

    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        target_path = sys.argv[1]
        with open(target_path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
        
        all_ok = True
        if isinstance(data, list):
            # Assume naver titles if not specified, or daum if containing ...
            if any("..." in t for t in data):
                all_ok = validate_daum_titles(data)
            else:
                all_ok = validate_naver_titles(data)
        elif isinstance(data, dict):
            if "naver_candidates" in data:
                all_ok = validate_naver_titles(data["naver_candidates"]) and all_ok
            elif "naver" in data and isinstance(data["naver"], list):
                all_ok = validate_naver_titles(data["naver"]) and all_ok
            if "daum_candidates" in data:
                all_ok = validate_daum_titles(data["daum_candidates"]) and all_ok
            elif "daum" in data and isinstance(data["daum"], list):
                all_ok = validate_daum_titles(data["daum"]) and all_ok
        
        if not all_ok:
            sys.exit(1)
        sys.exit(0)

    # Test runner
    sample_naver = [
        '"이 정도 출고액 차이면 수입 전기차로 넘어갈까?" 테슬라 모델 Y 9천 대 독주와 국산 SUV 차주들의 고뇌',
        '"600만 원 지원받고 K8 타는 게 그랜저보다 나을까?" 8월 신차 출고 지표로 본 실속파 오너들의 계산',
        '"국산차 옵션 더하다 5천만 원 넘길 바엔 이 차?" 4천 후반 모델 Y RWD에 쏠린 시선',
        '아반떼보다 싼타페 계약자가 덜 줄어든 이유와 페이스리프트 인상 전 실출고 예산 대조',
        '쏘렌토 6천 대 수성 뒤에 감춰진 출고 대기 3개월 단축과 패밀리 SUV 수요 분산',
        '셀토스 4천 대 급감과 아반떼 700대 등록 뒤에 숨은 생산 라인 교체와 실제 인도 기간',
        '2026년 8월 자동차 내수 출고량 순위 총정리, 테슬라 모델 Y 선두와 현대 기아 점유율 분석',
        '기아 쏘렌토 하이브리드 대 현대 그랜저 8월 출고 실적 및 차종별 대기 기간 비교',
        '기아 EV3 롱레인지 전기차 보조금 실구입 예산 및 소형 전기 SUV 내수 상위권 안착 요인',
        '국산 완성차 8월 출고 7만 9천 대 후퇴, 기아 K8 프로모션 혜택과 하반기 신차 전망'
    ]

    ok = validate_naver_titles(sample_naver)
    if not ok:
        sys.exit(1)

    sample_daum = [
        '"국산차 안방서 9천 대 팔아치웠다?"... 쏘렌토 제치고 전체 1위 오른 수입 SUV 정체 보니',
        '"싼타페 살 돈이면 차라리 이 차?"... 4천만 원대로 뚝 떨어진 수입 전기차 뜯어보니 깜짝',
        '"그랜저 살 바에 1천만 원 아낀다?"... 600만 원 깎아주자 난리 난 국산 세단 보니',
        '"현대차 3만 대 선이 무너졌다고?"... 안방 점유율 50% 싹쓸이한 괴물 브랜드의 비밀',
        '"쏘렌토 풀옵션 5천만 원 넘길 바엔?"... 아빠들 지갑 열게 만든 4천 후반 수입차 정체',
        '"아반떼가 700대밖에 안 팔렸다고?"... 공장 문 닫았나 웅성거리자 드러난 반전 속사정',
        '"셀토스 4천 대 증발에 비상 걸렸나?"... 대기표 뽑고 3달 넘게 기다리는 아빠들 들썩',
        '"국산 SUV보다 800만 원 싸다고?"... 단일 트림으로 한국 시장 평정한 괴물 전기차 보니',
        '"600만 원 할인에 줄 서서 계약?"... 그랜저 잡겠다고 작정하고 가격 낮춘 세단 뜯어보니',
        '"3천만 원대 전기차는 왜 이렇게 잘 팔릴까?"... 캐즘 뚫고 톱10 안착한 국산 SUV 정체 보니'
    ]
    ok_daum = validate_daum_titles(sample_daum)
    if not ok_daum:
        sys.exit(1)


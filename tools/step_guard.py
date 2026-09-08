# -*- coding: utf-8 -*-
"""
꿀단지 (KKULDANJI) - 마스터 표준 0호 / 23호 단계별 하드 게이트 및 최신 팩트 검증기 (Step Guard)
AI가 Step 0 최신 팩트 리서치(웹검색)를 빼먹거나, Step 1/2/3 제목 결정을 건너뛰고 본문을 작성하지 못하도록 물리적으로 강제 차단합니다.
"""
import os
import sys
import json
import re
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def get_latest_work_dir():
    """
    d:\작업\꿀단지 루트에서 'YYYY-MM-DD-주제명' 형식의 가장 최신 작업 폴더를 자동 탐색합니다.
    """
    root_dir = r"d:\작업\꿀단지"
    if not os.path.exists(root_dir):
        return None
    subdirs = [
        os.path.join(root_dir, d) 
        for d in os.listdir(root_dir) 
        if os.path.isdir(os.path.join(root_dir, d)) and re.match(r'^\d{4}-\d{2}-\d{2}', d)
    ]
    if subdirs:
        subdirs.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        return subdirs[0]
    return None

def get_target_months():
    now = datetime.now()
    cur_year = now.year
    cur_month = now.month
    if cur_month == 1:
        prev_year = cur_year - 1
        prev_month = 12
    else:
        prev_year = cur_year
        prev_month = cur_month - 1
    
    # 당월 표기 패턴
    cur_patterns = [
        f"{cur_year}년 {cur_month}월", f"{cur_year}년{cur_month}월",
        f"{cur_year}.{cur_month:02d}", f"{cur_year}-{cur_month:02d}",
        f"{cur_year}.{cur_month}", f"{cur_year}/{cur_month:02d}"
    ]
    # 전월 표기 패턴
    prev_patterns = [
        f"{prev_year}년 {prev_month}월", f"{prev_year}년{prev_month}월",
        f"{prev_year}.{prev_month:02d}", f"{prev_year}-{prev_month:02d}",
        f"{prev_year}.{prev_month}", f"{prev_year}/{prev_month:02d}"
    ]
    # 2026년 당해 연도 표기 패턴
    year_patterns = [f"{cur_year}년", f"{cur_year}."]

    # 예외 프로토콜 (유효성 재확인 표기 패턴)
    validity_patterns = [
        "현재 기준", "조회 기준", "최신 유효", "공인 표준", "변동 없이 유지", "유효성 확인", "정설로 인용", "개정본"
    ]
    return cur_patterns, prev_patterns, year_patterns, validity_patterns, (cur_year, cur_month), (prev_year, prev_month)

def verify_research_facts(work_dir):
    """
    [마스터 표준 23] 건강·영양 최신 데이터 팩트체크 리서치 검증기
    리서치.md에 당월/전월/당해연도 기준 시점 또는 당월 유효성 재확인 및 공인 출처 2건 이상이 기재되어 있는지 기계적으로 검사합니다.
    """
    research_path = os.path.join(work_dir, "리서치.md")
    if not os.path.exists(research_path):
        print(f"\n🚨 [HARD STOP 0 물리적 차단] 작업 폴더에 '리서치.md' 파일이 존재하지 않습니다!")
        print(f"   📂 대상 폴더: {work_dir}")
        print(f"   🛑 차단 사유: AI가 웹 검색(search_web)과 최신 팩트 리서치를 건너뛰고 작업을 시도했습니다.")
        print(f"   👉 해결 조치: Step 0 웹 검색을 먼저 실행하고 '리서치.md'에 최신 임상/공인기관 팩트를 정리하세요.")
        sys.exit(1)

    try:
        with open(research_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(research_path, "r", encoding="utf-8-sig") as f:
            content = f.read()

    cur_patterns, prev_patterns, year_patterns, validity_patterns, cur_ym, prev_ym = get_target_months()
    has_cur = any(p in content for p in cur_patterns)
    has_prev = any(p in content for p in prev_patterns)
    has_year = any(p in content for p in year_patterns)
    has_validity = any(p in content for p in validity_patterns)
    has_valid_date = has_cur or has_prev or (has_year and has_validity)

    # 건강/의학/영양 분야 공인 출처 키워드 풀
    source_keywords = [
        "식약처", "식품의약품안전처", "질병관리청", "질병청", "농촌진흥청", "농진청", 
        "보건복지부", "소비자원", "한국소비자원", "식품안전나라", "하버드", "Harvard", 
        "란셋", "Lancet", "ADA", "미국당뇨병학회", "WHO", "세계보건기구", "ESC", "유럽심장학회", 
        "AJCN", "임상영양", "국민건강영양조사", "학술지", "논문", "임상시험", "메타분석", 
        "가이드라인", "코호트", "대한영양사협회", "대한당뇨병학회", "NEJM", "Nature", "BMJ",
        "http://", "https://"
    ]
    matched_sources = list(set([kw for kw in source_keywords if kw in content]))

    print(f"   - [Step 0 리서치 파일]: ✅ 확인됨 ({os.path.basename(research_path)})")
    
    # 날짜 검증 상태 출력
    if has_cur:
        date_status = f"✅ 당월 최신 팩트 확인 ({cur_ym[0]}년 {cur_ym[1]}월)"
    elif has_prev:
        date_status = f"✅ 전월 팩트 확인 ({prev_ym[0]}년 {prev_ym[1]}월)"
    elif has_year and has_validity:
        date_status = f"✅ {cur_ym[0]}년 당해연도 유효성 재확인 완료 (학계 공인 표준)"
    else:
        date_status = f"❌ 미기재 (당월 {cur_ym[0]}년 {cur_ym[1]}월 또는 {cur_ym[0]}년 최신성/유효성 재확인 표기 필수)"
    print(f"   - [Step 0 최신 기준 시점]: {date_status}")

    # 출처 검증 상태 출력
    source_status = f"✅ {', '.join(matched_sources[:4])} 등 총 {len(matched_sources)}개 확인" if len(matched_sources) >= 2 else f"❌ 공인 출처 부족 (현재 {len(matched_sources)}개, 최소 2개 필수)"
    print(f"   - [Step 0 공인 출처 검증]: {source_status}")

    # 1) 최신 시점 누락 시 즉각 물리 차단
    if not has_valid_date:
        print(f"\n🚨 [HARD STOP 0 물리적 차단] '리서치.md'에 최신성 기준 시점 또는 당월 유효성 재확인이 누락되었습니다!")
        print(f"   🛑 기준: 당월({cur_ym[0]}년 {cur_ym[1]}월), 전월({prev_ym[0]}년 {prev_ym[1]}월), 또는 '{cur_ym[0]}년 M월 조회/현재 기준 공인 표준 유지' 표기 필요.")
        print(f"   👉 조치: search_web으로 최신 공인 자료를 확인하고 리서치.md를 보강하세요.")
        sys.exit(1)

    # 2) 공인 출처 부족 시 즉각 물리 차단
    if len(matched_sources) < 2:
        print(f"\n🚨 [HARD STOP 0 물리적 차단] '리서치.md'에 공인 출처(식약처, 질병청, 하버드, 란셋 등)가 2건 이상 기재되지 않았습니다!")
        print(f"   🛑 블로그 찌라시나 미검증 민간요법 방지를 위해 공인 연구기관/정부 통계 출처 2건 이상이 필수입니다.")
        print(f"   👉 조치: 신뢰할 수 있는 공인 기관의 최신 발표자료를 search_web하여 리서치.md에 기재하세요.")
        sys.exit(1)

    # 3) 위험한 만병통치약 과장 금칙어 검출 (금칙어 소각/교체 계획 섹션 제외)
    dangerous_words = ["완치", "100% 치료", "암세포 박멸", "기적의 치료제", "특효약", "즉각 완치"]
    body_for_check = re.sub(r'(?:금칙어|소각|교체\s*계획)[\s\S]*$', '', content, flags=re.I)
    found_danger = [w for w in dangerous_words if w in body_for_check]
    if found_danger:
        print(f"\n🚨 [HARD STOP 0 물리적 차단] '리서치.md' 서술 본문에 의료법/식품위생법 위반 과장 표현이 감지되었습니다: {found_danger}")
        print(f"   👉 조치: '개선', '보완', '관리', '부담 완화' 등 안전하고 절제된 표현으로 수정하세요.")
        sys.exit(1)

    print("   - [Step 0 안전성 및 과장표현]: ✅ 100% 무결성 확인 (위험 표현 0개)")
    return True

def check_step(required_step):
    """
    required_step:
      0 -> Step 0 (리서치 검증 단계)
      1 -> Step 1 (네이버 제목 보고 단계: Step 0 리서치 통과 필수)
      2 -> Step 2 (다음 제목 보고 단계: 네이버 제목 승인 필수)
      3 -> Step 3 (구글 제목 보고 단계: 네이버 & 다음 제목 승인 필수)
      4 -> Step 4 (본문 작성 단계: Step 0 리서치 & 3대 제목 100% 승인 필수)
    """
    work_dir = get_latest_work_dir()
    if not work_dir:
        print("❌ 작업 폴더(YYYY-MM-DD-주제명)가 존재하지 않습니다.")
        sys.exit(1)

    print(f"🔍 [꿀단지 단계별 게이트 검사] 대상 폴더: {os.path.basename(work_dir)}")

    # 1. Step 0 리서치 최신 팩트체크 검증 (모든 단계 진입 시 필수 통과)
    verify_research_facts(work_dir)

    tj_path = os.path.join(work_dir, "titles.json")
    titles = {}
    if os.path.exists(tj_path):
        with open(tj_path, "r", encoding="utf-8-sig") as f:
            titles = json.load(f)

    naver = (titles.get("naver_title") or titles.get("naver") or "").strip()
    daum = (titles.get("daum_title") or titles.get("daum") or "").strip()
    google = (titles.get("google_title") or titles.get("google") or "").strip()

    # 꿀단지 2-Track 모드 호환 (다음이 N/A이거나 없는 경우 2-Track으로 자동 판정)
    is_2track = ("N/A" in daum or not daum)

    print(f"   - [Step 1] 네이버 제목: {'✅ ' + naver if naver else '❌ 미승인'}")
    if not is_2track:
        print(f"   - [Step 2] 다음 채널 제목: {'✅ ' + daum if daum else '❌ 미승인'}")
    else:
        print(f"   - [Step 2] 다음 채널 제목: ℹ️ 꿀단지 2-Track 모드 (구글+네이버 집중)")
    print(f"   - [Step 3] 구글 본진 제목: {'✅ ' + google if google else '❌ 미승인'}")

    if required_step == 2 and not naver:
        print("\n🚨 [HARD STOP 1 위반] 네이버 제목이 승인·확정되지 않았습니다! 다음 단계 진행이 물리적으로 차단됩니다.")
        sys.exit(1)
    elif required_step == 3 and not is_2track and not (naver and daum):
        print("\n🚨 [HARD STOP 2 위반] 네이버 또는 다음 제목이 확정되지 않았습니다! 구글 제목 단계 진행이 물리적으로 차단됩니다.")
        sys.exit(1)
    elif required_step == 4:
        if is_2track and not (naver and google):
            print("\n🚨 [HARD STOP 3 위반] 네이버 및 구글 제목이 titles.json에 확정되지 않았습니다! 본문 파일 작성이 물리적으로 차단됩니다.")
            sys.exit(1)
        elif not is_2track and not (naver and daum and google):
            print("\n🚨 [HARD STOP 3 위반] 3대 제목(네이버/다음/구글)이 모두 titles.json에 확정되지 않았습니다! 본문 파일 작성이 물리적으로 차단됩니다.")
            sys.exit(1)

    print(f"\n🔒 [게이트 통과] Step {required_step} 진입 조건이 물리적으로 100% 충족되었습니다.")
    return True

if __name__ == "__main__":
    step = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    check_step(step)

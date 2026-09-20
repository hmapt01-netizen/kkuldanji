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

def trigger_governance_block(source_rule, issue_desc, diff_old="", diff_new=""):
    """
    [마스터 표준 0-8] 시스템 하드락 발동 및 AI 보고 강제 표준 양식 출력
    """
    print("\n" + "=" * 80)
    print("🚨 [가디언 시스템 하드락 발동 / AI 행동 강제 지침]")
    print("AI는 절대로 억지로 작업을 강행하거나, 가짜 출처/수치를 날조하여 넘어가려 하지 마십시오!")
    print("지금 즉시 대표님께 아래 표준 양식으로 상황을 보고하고 규칙/코드 수정을 건의하십시오:\n")
    print("--------------------------------------------------------------------------------")
    print("🚨 [에이전트 규칙/팩트 불일치 감지 보고]")
    print(f"1. 원인 조항: {source_rule}")
    print(f"2. 발생 문제: {issue_desc}")
    if diff_old and diff_new:
        print("3. 해결 제안 (Diff):")
        print(f"   [기존]: {diff_old}")
        print(f"   [수정안]: {diff_new}")
    print("4. 조치 요청: 대표님의 승인 후 규칙/코드를 패치하고 작업을 재개하겠습니다.")
    print("--------------------------------------------------------------------------------")
    print("=" * 80 + "\n")
    sys.exit(1)

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

def verify_research_facts(work_dir, required_step=1):
    """
    [마스터 표준 0 / 23] 건강·영양 최신 데이터 팩트체크 리서치 2단계 검증기
    - Step 1~3 (제목 단계): 1차 사전 팩트 탐색 (최신성, 공인기관 2건+URL, 과장표현 0개, SERP 실사, 내부링크)
    - Step 4 (본문 단계): 2차 제목 맞춤형 심층 리서치 (확정 제목 맞춤 FAQ 2~3선 및 공인 근거 필수)
    """
    # 0-1. Zero-Example 안티-앵커링 규칙 검사 선행 (규칙/스킬 문서 내 예시 박제 차단)
    try:
        from lint_rules_zero_example import run_linter
        if run_linter() != 0:
            print("\n🚨 [HARD STOP 물리적 차단] 규칙 또는 스킬 문서에 안티-앵커링 위반(성분명/약물명/식품명 예시 박제)이 발견되었습니다!")
            print("   👉 조치: 'python tools/lint_rules_zero_example.py'의 위반 사항을 먼저 해결하세요.")
            sys.exit(1)
    except ImportError:
        pass

    # 0-2. 규칙-코드 정합성 및 런타임 충돌 자가 진단 선행
    try:
        from audit_rule_integrity import run_audit
        if run_audit() != 0:
            print("\n🚨 [HARD STOP 물리적 차단] 규칙 문서와 파이썬 가디언 코드 간의 충돌·모순이 발견되었습니다!")
            print("   👉 AI 행동 강령: 억지로 작업을 진행하지 말고, 즉시 대표님께 [원인 조항 / 발생 문제 / 규칙 수정안(Diff)]을 보고하고 승인을 요청하세요.")
            sys.exit(1)
    except ImportError:
        pass

    research_path = os.path.join(work_dir, "리서치.md")
    if not os.path.exists(research_path):
        trigger_governance_block(
            "마스터 표준 0호 (Step 0-A 사전 팩트 탐색)",
            f"작업 폴더에 '리서치.md'가 없습니다. AI가 웹 검색(search_web) 및 사전 팩트 확인을 건너뛰고 작업을 시도했습니다.",
            "리서치.md 없이 작업 진행",
            "search_web으로 공인 1차 기관 기준선 및 최신 팩트를 확인하여 '리서치.md' 생성 후 재개"
        )

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
    korea_official_keywords = [
        "식약처", "식품의약품안전처", "질병관리청", "질병청", "농촌진흥청", "농진청", 
        "보건복지부", "국민건강보험", "건강보험심사평가원", "심평원", "식품안전나라", 
        "국가건강정보포털", "국립암센터", "대한의학회", "대한내과학회", "대한소화기학회",
        "대한당뇨병학회", "국가표준식품성분표", "국민건강영양조사"
    ]
    source_keywords = korea_official_keywords + [
        "소비자원", "한국소비자원", "하버드", "Harvard", 
        "란셋", "Lancet", "ADA", "미국당뇨병학회", "WHO", "세계보건기구", "ESC", "유럽심장학회", 
        "AJCN", "임상영양", "학술지", "논문", "임상시험", "메타분석", 
        "가이드라인", "코호트", "대한영양사협회", "NEJM", "Nature", "BMJ",
        "http://", "https://"
    ]
    matched_sources = list(set([kw for kw in source_keywords if kw in content]))
    matched_korea = list(set([kw for kw in korea_official_keywords if kw in content]))

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
    if not matched_korea:
        source_status = "❌ 한국 공인 1차 기관 출처 누락 (질병관리청, 식약처, 농진청 등 필수)"
    elif len(matched_sources) >= 2:
        source_status = f"✅ 한국 공인({', '.join(matched_korea[:2])}) 포함 총 {len(matched_sources)}개 확인"
    else:
        source_status = f"❌ 공인 출처 부족 (현재 {len(matched_sources)}개, 최소 2개 필수)"
    print(f"   - [Step 0 공인 출처 검증]: {source_status}")

    # 1) 최신 시점 누락 시 즉각 물리 차단
    if not has_valid_date:
        print(f"\n🚨 [HARD STOP 0 물리적 차단] '리서치.md'에 최신성 기준 시점 또는 당월 유효성 재확인이 누락되었습니다!")
        print(f"   🛑 기준: 당월({cur_ym[0]}년 {cur_ym[1]}월), 전월({prev_ym[0]}년 {prev_ym[1]}월), 또는 '{cur_ym[0]}년 M월 조회/현재 기준 공인 표준 유지' 표기 필요.")
        print(f"   👉 조치: search_web으로 최신 공인 자료를 확인하고 리서치.md를 보강하세요.")
        sys.exit(1)

    # 1-1) [마스터 표준 0-5] 한국 공인 1차 기관 누락 시 즉각 물리 차단
    if not matched_korea:
        print(f"\n🚨 [HARD STOP 0 물리적 차단 / 마스터 표준 0-5] '리서치.md'에 한국 공인 1차 기관(질병관리청, 식약처, 농진청, 보건복지부 등) 출처가 1건도 없습니다!")
        print(f"   🛑 외국 사이트에만 의존하는 행위를 방지하고 국내 독자의 식습관과 보건 기준에 부합하기 위해 한국 공인 기관 기준선이 1순위 필수입니다.")
        print(f"   👉 조치: 질병관리청 국가건강정보포털, 식약처, 농촌진흥청 등의 공식 발표자료를 search_web하여 리서치.md를 보강하세요.")
        sys.exit(1)

    # 2) 공인 출처 부족 시 즉각 물리 차단
    if len(matched_sources) < 2:
        print(f"\n🚨 [HARD STOP 0 물리적 차단] '리서치.md'에 공인 출처가 2건 이상 기재되지 않았습니다!")
        print(f"   🛑 블로그 찌라시나 미검증 민간요법 방지를 위해 공인 연구기관/정부 통계 출처 2건 이상이 필수입니다.")
        print(f"   👉 조치: 신뢰할 수 있는 공인 기관의 최신 발표자료를 search_web하여 리서치.md에 기재하세요.")
        sys.exit(1)

    # 2-1) [마스터 표준 0-5] 실제 클릭 가능한 공인 출처 URL (https://...) 필수 검증
    urls_found = re.findall(r'https?://[^\s\)\"\'\>]+', content)
    if not urls_found:
        print(f"\n🚨 [HARD STOP 0 물리적 차단 / 마스터 표준 0-5] '리서치.md'에 실제 클릭 가능한 공인기관/학술 원문 웹사이트 URL(https://...)이 단 1개도 기재되지 않았습니다!")
        print(f"   🛑 2차 블로그 인용 및 가짜 텍스트 출처 표기를 원천 방어하기 위해 실제 원문 공식 URL 기재가 100% 필수입니다.")
        print(f"   👉 조치: 식약처, 질병청, 공인 논문 등 실제 1차 출처 URL을 리서치.md에 등록하세요.")
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

    # 4) [마스터 표준 25호] 신규 주제 사전 검토 6대 실사 및 내부링크 연계망 검증
    audit_keywords = ["사전 검토", "실사 브리핑", "6대 실사", "4대 실사", "토픽 클러스터", "로드맵", "CONTENT_ROADMAP"]
    has_audit_section = any(kw in content for kw in audit_keywords)

    db_path = os.path.join(r"d:\작업\꿀단지", "data", "posts_db.json")
    matched_links = []
    if os.path.exists(db_path):
        try:
            with open(db_path, "r", encoding="utf-8-sig") as df:
                posts_data = json.load(df)
            for p in posts_data:
                slug = p.get("slug", "")
                if slug and (slug in content or f"{slug}.html" in content):
                    matched_links.append(slug)
        except Exception:
            pass

    print(f"   - [Step 0 사전 실사 기록]: {'✅ 확인됨' if has_audit_section else '❌ 누락'}")
    link_status = f"✅ 기존 글 {len(matched_links)}편 연계 확인 ({', '.join(matched_links[:2])}...)" if len(matched_links) >= 2 else f"❌ 내부링크 연계 부족 (현재 {len(matched_links)}편, 최소 2편 필수)"
    print(f"   - [Step 0 기존 글 연계망]: {link_status}")

    # 실사 기록 누락 시 즉각 물리 차단
    if not has_audit_section:
        print(f"\n🚨 [HARD STOP 0 물리적 차단] '리서치.md'에 [마스터 표준 25호] '사전 검토 6대 실사 브리핑' 기록이 누락되었습니다!")
        print(f"   🛑 사유: AI가 기발행 글 DB 전수 대조와 콘텐츠 로드맵 실사를 거치지 않고 임의로 글을 작성하는 것을 방지합니다.")
        print(f"   👉 조치: 'python tools/suggest_topics.py' 실행 결과인 사전 검토 6대 실사 브리핑 표를 리서치.md 상단에 기록하세요.")
        sys.exit(1)

    # 5) [마스터 표준 26호] 실시간 SERP 실사 및 4단계 실제 경쟁도(레드/블루오션) 성적표 검증
    serp_keywords = ["경쟁도", "경쟁 강도", "레드오션", "블루오션", "SERP"]
    has_serp_section = any(kw in content for kw in serp_keywords)
    has_serp_badges = any(b in content for b in ["🔴", "🟡", "🟢", "💎"])
    has_serp_table = has_serp_section and has_serp_badges

    print(f"   - [Step 0 SERP 경쟁도 표]: {'✅ 확인됨 (4단계 팩트체크 성적표)' if has_serp_table else '❌ 누락'}")
    if not has_serp_table:
        print(f"\n🚨 [HARD STOP 0 물리적 차단] '리서치.md'에 [마스터 표준 26호] '실시간 SERP 실사 및 4단계 실제 경쟁도(레드/블루오션) 성적표'가 누락되었습니다!")
        print(f"   🛑 사유: AI가 실시간 포털 검색 결과를 실사하지 않고 짐작으로 작성하거나 보고서 표를 누락하는 것을 방지합니다.")
        print(f"   👉 조치: 'search_web'으로 상위 포털 결과를 실사하고 [🔴 초극심 레드오션 / 🟡 중간 경쟁 / 🟢 알짜 틈새 / 💎 진짜 블루오션 빈집] 성적표를 리서치.md에 반드시 기록하세요.")
        sys.exit(1)

    # [마스터 표준 27호 물리적 게이트 잠금] data/last_serp_audit.json 파일 실존 및 유효성 검증
    audit_file = os.path.join(r"d:\작업\꿀단지", "data", "last_serp_audit.json")
    if not os.path.exists(audit_file):
        print(f"\n🚨 [HARD STOP 0 물리적 차단] 실시간 SERP 실사 감사 로그('data/last_serp_audit.json')가 존재하지 않습니다!")
        print(f"   🛑 사유: AI가 실시간 포털 검색 결과를 실제로 크롤링·실사하지 않고 임의로 레드/블루오션을 지어내는 것을 원천 차단합니다.")
        print(f"   👉 조치: 'python tools/audit_serp_live.py'를 실행하여 실제 네이버 1페이지 문서를 크롤링·실사하세요.")
        sys.exit(1)

    try:
        with open(audit_file, "r", encoding="utf-8") as af:
            audit_data = json.load(af)
        records = audit_data.get("records", audit_data.get("results", []))
        if not records or len(records) == 0:
            print(f"\n🚨 [HARD STOP 0 물리적 차단] 'data/last_serp_audit.json'에 실사된 검색 쿼리 기록이 0건입니다!")
            print(f"   👉 조치: 'python tools/audit_serp_live.py <후보_키워드들>'을 실행하여 실제 문서를 크롤링하세요.")
            sys.exit(1)

        ts_str = audit_data.get("timestamp", "")
        if ts_str:
            audit_dt = datetime.fromisoformat(ts_str)
            if audit_dt.tzinfo is not None:
                from datetime import timezone
                now_dt = datetime.now(timezone.utc)
                audit_dt_utc = audit_dt.astimezone(timezone.utc)
                diff_hours = (now_dt - audit_dt_utc).total_seconds() / 3600
            else:
                diff_hours = (datetime.now() - audit_dt).total_seconds() / 3600
            if diff_hours > 24:
                print(f"\n🚨 [HARD STOP 0 물리적 차단] 실시간 SERP 감사 로그가 24시간 이상 경과하여 만료되었습니다 ({diff_hours:.1f}시간 경과)!")
                print(f"   👉 조치: 'python tools/audit_serp_live.py'를 재실행하여 최신 SERP를 다시 실사하세요.")
                sys.exit(1)

        # [사각지대 4 방어: 주제 일치성 검증 - 캐시 구멍 원천 차단]
        first_line = content.splitlines()[0] if content else ""
        topic_tokens = [w for w in re.findall(r'[가-힣a-zA-Z0-9]+', first_line) if len(w) >= 2 and w not in ["리서치", "온라인", "신청법과", "절차", "기준", "정리", "안내", "가이드"]]
        audited_texts = [r.get("title", "") + " " + r.get("clean_query", "") for r in records]
        topic_matched = any(any(tok in at for tok in topic_tokens) for at in audited_texts)
        if not topic_matched:
            print(f"\n🚨 [HARD STOP 0 물리적 차단] 실시간 SERP 감사 로그의 주제가 현재 작업 폴더 주제와 일치하지 않습니다!")
            print(f"   - 현재 작업 주제: {first_line[:40]}...")
            print(f"   - 감사 로그 주제: {records[0].get('clean_query', '')}...")
            print(f"   👉 조치: 'python tools/audit_serp_live.py'를 현재 주제로 재실행하세요.")
            sys.exit(1)

        print(f"   - [Step 0 SERP 크롤링 증거]: ✅ 100% 무결성 확인 (실사 {len(records)}건, 주제일치: 확인됨, 채널: {audit_data.get('channel', 'naver')})")
    except Exception as e:
        print(f"\n🚨 [HARD STOP 0 물리적 차단] 'data/last_serp_audit.json' 파싱 오류: {e}")
        sys.exit(1)



    # 기존 글 내부링크 2편 미만 시 즉각 물리 차단
    if len(matched_links) < 2:
        print(f"\n🚨 [HARD STOP 0 물리적 차단] '리서치.md'에 [마스터 표준 25호] 기존 글 내부링크 연계망(최소 2편 이상)이 누락되었습니다!")
        print(f"   🛑 사유: 기존 발행 자산과의 연계 없이 단독 글을 발행하는 행위는 고립 페이지(Orphan Page)를 발생시키고 주제 추천 실사를 건너뛴 증거입니다.")
        print(f"   👉 조치: data/posts_db.json의 기존 글 중 연계할 2편 이상의 링크(.html 또는 슬러그)를 리서치.md에 기재하세요.")
        sys.exit(1)

    # 6) [마스터 표준 23-1호] FAQ 및 심층 데이터 검증 (2단계 리서치 분리)
    faq_keywords = ["FAQ", "자주 묻는 질문", "질의응답", "Q&A", "핵심 질문", "질문 1", "질문 2", "질문 3"]
    has_faq_research = any(kw in content for kw in faq_keywords)

    if required_step == 4:
        # Step 4(본문 작성 단계)에서만 확정 제목 맞춤 FAQ 및 심층 데이터 필수 검증
        print(f"   - [Step 0-B 확정 제목 맞춤 FAQ 실사]: {'✅ 확인됨 (공인 근거 실사)' if has_faq_research else '❌ 누락'}")
        if not has_faq_research:
            trigger_governance_block(
                "마스터 표준 23-1호 (Step 0-B 확정 제목 맞춤 FAQ 실사)",
                "확정된 제목의 분석 스코프에 맞춘 FAQ 2~3선 및 공인 근거가 '리서치.md'에 누락되었습니다.",
                "FAQ 사전 실사 없이 본문 작성 강행 시도",
                "확정된 제목이 약속한 쟁점/의문에 직결된 질문 2~3선과 공인 출처를 '리서치.md'에 보강 후 재개"
            )

        # 7) [마스터 표준 23-6호] Step 0-B 확정 제목 전제 팩트체크 및 정합성 검증
        title_error_patterns = [
            r'\[\s*(?:제목\s*오류|전제\s*오류|팩트\s*오류|오류\s*감지|정합성\s*실패|FAIL)\s*\]',
            r'제목\s*수정\s*필요',
            r'제목의\s*전제가\s*(?:틀림|오류|반증|위험)'
        ]
        has_title_error = any(re.search(pat, content, re.IGNORECASE) for pat in title_error_patterns)

        tj_path = os.path.join(work_dir, "titles.json")
        title_error_in_json = False
        if os.path.exists(tj_path):
            try:
                with open(tj_path, "r", encoding="utf-8-sig") as tj_f:
                    tj_data = json.load(tj_f)
                    title_error_in_json = tj_data.get("title_error", False) is True
            except Exception:
                pass

        if has_title_error or title_error_in_json:
            trigger_governance_block(
                "마스터 표준 23-6호 (Step 0-B 확정 제목 전제 오류 감지 및 긴급 중단)",
                "Step 0-B 심층 리서치 과정에서 확정된 제목의 전제에 의학적/사실적 오류(반증)가 감지되었습니다. 잘못된 제목으로 본문을 작성하는 행위가 물리적으로 차단됩니다.",
                "오류가 확인된 제목으로 본문 작성 강행 시도",
                "즉시 대표님께 [감지된 오류 내용 / 의학적 반증 근거 / 대체 제목 후보 3선]을 보고하고 제목 재승인 후 진행"
            )

        premise_keywords = ["제목 전제", "정합성 검증", "전제 팩트체크", "전제 검증", "제목 검증"]
        has_premise_check = any(kw in content for kw in premise_keywords)
        print(f"   - [Step 0-B 확정 제목 전제 정합성 실사]: {'✅ 확인됨 (팩트 무결성)' if has_premise_check else '❌ 누락'}")
        if not has_premise_check:
            trigger_governance_block(
                "마스터 표준 23-6호 (확정 제목 전제 정합성 사전 실사)",
                "확정된 제목의 핵심 전제가 사실/의학적 근거와 일치하는지 검증한 '### 🚨 [확정 제목 전제 팩트체크 및 정합성 검증]' 기록이 '리서치.md'에 누락되었습니다.",
                "제목 전제 검증 없이 본문 작성 강행 시도",
                "확정된 제목의 전제를 공인 출처로 검증하여 [정합성 판정: 정상 (PASS)]을 '리서치.md'에 기록 후 재개"
            )
    else:
        # Step 1~3 (제목 단계)에서는 사전 팩트 안전선만 검증하고 FAQ는 요구하지 않음
        faq_note = "✅ 사전 팩트 안전선 확보 완료 (맞춤 FAQ 및 제목 전제 검증은 제목 확정 후 Step 0-B 심층 리서치에서 진행)"
        print(f"   - [Step 0-A 사전 팩트 검증]: {faq_note}")

    return True

def verify_titles_audit(channel, selected_title):
    """
    [마스터 표준 27-4] 제목 10선 키워드 3단 조합(메인+연관+변주) 및 실시간 SERP 감사 로그 물리적 검증기
    AI가 표 생성을 건너뛰거나, 3단 조합 분해 없이 제목을 날조하여 선택하는 행위를 물리적으로 차단합니다.
    """
    audit_filename = f"last_{channel}_titles_audit.json"
    audit_path = os.path.join(r"d:\작업\꿀단지", "data", audit_filename)
    if not os.path.exists(audit_path):
        print(f"\n🚨 [HARD STOP 물리적 차단 / 마스터 표준 27-4] {channel.upper()} 제목 10선 감사 로그('{audit_filename}')가 존재하지 않습니다!")
        print(f"   🛑 사유: AI가 키워드 3단 조합 표 생성 및 실시간 SERP 실사를 거치지 않고 임의로 진행하는 것을 방지합니다.")
        print(f"   👉 조치: 'python tools/validate_titles.py {channel} <제목파일>'을 먼저 실행하여 성적표를 생성·보고하세요.")
        sys.exit(1)

    try:
        with open(audit_path, "r", encoding="utf-8") as f:
            audit_data = json.load(f)
    except Exception as e:
        print(f"\n🚨 [HARD STOP 물리적 차단] {audit_filename} 파싱 오류: {e}")
        sys.exit(1)

    # 1. 24시간 이내 유효성
    ts_str = audit_data.get("timestamp", "")
    if ts_str:
        audit_dt = datetime.fromisoformat(ts_str)
        if audit_dt.tzinfo is not None:
            from datetime import timezone
            now_dt = datetime.now(timezone.utc)
            audit_dt_utc = audit_dt.astimezone(timezone.utc)
            diff_hours = (now_dt - audit_dt_utc).total_seconds() / 3600
        else:
            diff_hours = (datetime.now() - audit_dt).total_seconds() / 3600
        if diff_hours > 24:
            print(f"\n🚨 [HARD STOP 물리적 차단] {channel.upper()} 제목 감사 로그가 24시간 이상 경과했습니다 ({diff_hours:.1f}시간).")
            print(f"   👉 조치: 'python tools/validate_titles.py {channel}'로 최신 실사를 재실행하세요.")
            sys.exit(1)

    # 2. triad_table_rendered 검증
    if not audit_data.get("triad_table_rendered") and not audit_data.get("serp_table_rendered"):
        print(f"\n🚨 [HARD STOP 물리적 차단] {audit_filename}에 키워드 3단 조합 표 생성(triad_table_rendered) 플래그가 없습니다!")
        sys.exit(1)

    # 3. 10개 후보 전수 키워드 3단 조합(core, related, variation) 실존 검증
    records = audit_data.get("records", [])
    if len(records) < 10:
        print(f"\n🚨 [HARD STOP 물리적 차단] {audit_filename}의 후보 개수가 {len(records)}개로 10개 미만입니다!")
        sys.exit(1)

    for r in records:
        triad = r.get("triad", {})
        if not triad.get("core") or not triad.get("variation"):
            print(f"\n🚨 [HARD STOP 물리적 차단] {channel.upper()} 후보 {r.get('idx')}번에 키워드 3단 조합 분해가 누락되었습니다!")
            print(f"   제목: {r.get('title')}")
            sys.exit(1)

    # 4. 확정된 제목이 감사 로그 10선 내 실존하는지 대조 검증
    if selected_title:
        audited_titles = [r.get("title", "").strip() for r in records]
        norm_sel = re.sub(r'[\s\"\'“”‘’]', '', selected_title)
        tokens_sel = set(re.findall(r'[a-zA-Z0-9가-힣]+', selected_title))
        matched = False
        for at in audited_titles:
            norm_at = re.sub(r'[\s\"\'“”‘’]', '', at)
            if norm_sel == norm_at or norm_sel in norm_at or norm_at in norm_sel:
                matched = True
                break
            tokens_at = set(re.findall(r'[a-zA-Z0-9가-힣]+', at))
            if tokens_sel and tokens_at:
                overlap = len(tokens_sel & tokens_at) / max(len(tokens_sel), len(tokens_at))
                if overlap >= 0.65:
                    matched = True
                    break

        if not matched:
            print(f"\n🚨 [HARD STOP 물리적 차단 / 마스터 표준 27-4] 확정된 {channel.upper()} 제목이 감사 로그의 10선 후보 목록과 일치하지 않습니다!")
            print(f"   - 확정 제목: '{selected_title}'")
            print(f"   - 감사 로그 후보 10선: {[at[:25] for at in audited_titles[:3]]}...")
            print(f"   🛑 사유: 키워드 3단 조합 및 SERP 실사를 통과하지 않은 미검증 제목의 임의 채택을 원천 차단합니다.")
            sys.exit(1)

    print(f"   - [{channel.upper()} 키워드 3단 조합 및 SERP 감사]: ✅ 100% 무결성 확인 (10선 전수 분해 및 확정 일치 확인됨)")
    return True

def check_step(required_step):
    """
    required_step:
      0 -> Step 0 (리서치 검증 단계)
      1 -> Step 1 (네이버 제목 보고 단계: Step 0-A 사전 팩트 통과 필수)
      2 -> Step 2 (다음 제목 보고 단계: 네이버 제목 승인 필수)
      3 -> Step 3 (구글 제목 보고 단계: 네이버 & 다음 제목 승인 필수)
      4 -> Step 4 (본문 작성 단계: Step 0-B 심층 리서치 & 3대 제목 100% 승인 필수)
    """
    work_dir = get_latest_work_dir()
    if not work_dir:
        print("❌ 작업 폴더(YYYY-MM-DD-주제명)가 존재하지 않습니다.")
        sys.exit(1)

    print(f"🔍 [꿀단지 단계별 게이트 검사] 대상 폴더: {os.path.basename(work_dir)}")

    # 1. 최신 팩트체크 검증 (required_step에 따라 Step 0-A 또는 Step 0-B 자동 분리)
    verify_research_facts(work_dir, required_step=required_step)

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

    if required_step == 2:
        if not naver:
            print("\n🚨 [HARD STOP 1 위반] 네이버 제목이 승인·확정되지 않았습니다! 다음 단계 진행이 물리적으로 차단됩니다.")
            sys.exit(1)
        verify_titles_audit("naver", naver)
    elif required_step == 3:
        if not is_2track and not (naver and daum):
            print("\n🚨 [HARD STOP 2 위반] 네이버 또는 다음 제목이 확정되지 않았습니다! 구글 제목 단계 진행이 물리적으로 차단됩니다.")
            sys.exit(1)
        verify_titles_audit("naver", naver)
    elif str(required_step) in ["3.5", "35"]:
        if is_2track and not (naver and google):
            print("\n🚨 [HARD STOP 3 위반] 제목이 확정되지 않았습니다! 이미지 계획 작성이 차단됩니다.")
            sys.exit(1)
        verify_titles_audit("naver", naver)
        verify_titles_audit("google", google)
        try:
            import image_guard
            if not image_guard.validate_image_plan(work_dir, require_approval=False):
                sys.exit(1)
        except Exception as e:
            print(f"🚨 [Image Guard 연동 실패]: {e}")
            sys.exit(1)
    elif required_step == 4:
        if is_2track and not (naver and google):
            print("\n🚨 [HARD STOP 3 위반] 네이버 및 구글 제목이 titles.json에 확정되지 않았습니다! 본문 파일 작성이 물리적으로 차단됩니다.")
            sys.exit(1)
        elif not is_2track and not (naver and daum and google):
            print("\n🚨 [HARD STOP 3 위반] 3대 제목(네이버/다음/구글)이 모두 titles.json에 확정되지 않았습니다! 본문 파일 작성이 물리적으로 차단됩니다.")
            sys.exit(1)

        # [마스터 표준 27-4] 네이버 및 구글 제목 키워드 3단 조합 및 SERP 감사 로그 전수 검증
        verify_titles_audit("naver", naver)
        verify_titles_audit("google", google)

        # [마스터 표준 27-1호] 화보 생성 사전 계획(image_plan.json) 및 사용자 승인 검증
        try:
            import image_guard
            if not image_guard.validate_image_plan(work_dir, require_approval=True):
                print("\n🚨 [HARD STOP 3.5 위반] image_plan.json이 누락되었거나 사용자 승인(is_user_approved=True)이 완료되지 않았습니다!")
                print("   🛑 사유: AI가 단일 주인공/한국 아파트 배경 앵커 사전 승인 없이 본문 또는 이미지를 즉흥 작성하는 행위를 원천 차단합니다.")
                sys.exit(1)
        except Exception as e:
            print(f"🚨 [Image Guard 검증 오류]: {e}")
            sys.exit(1)

        # [마스터 표준 23-2호] Evidence Guard 공인 근거 및 팩트 무결성 검증
        try:
            import evidence_guard
            pj_path = os.path.join(work_dir, "post_data.json")
            if os.path.exists(pj_path):
                with open(pj_path, "r", encoding="utf-8-sig") as f:
                    p_data = json.load(f)
                evidence_guard.validate_post_evidence(p_data, work_dir=work_dir)
        except Exception as e:
            trigger_governance_block(
                "마스터 표준 23-2호 (Evidence Guard 공인 근거 및 팩트 무결성)",
                f"Evidence Guard 검증 실패: {e}",
                "미검증/오류 출처 및 수치 불일치 원고 등록 시도",
                "evidence_manifest.json 및 원고의 수치·출처·금칙어를 검증 규격에 맞춰 정정 후 재개"
            )

    print(f"\n🔒 [게이트 통과] Step {required_step} 진입 조건이 물리적으로 100% 충족되었습니다.")
    return True

if __name__ == "__main__":
    raw_step = sys.argv[1] if len(sys.argv) > 1 else "1"
    try:
        step = int(raw_step)
    except ValueError:
        try:
            step = float(raw_step)
        except ValueError:
            step = raw_step
    check_step(step)


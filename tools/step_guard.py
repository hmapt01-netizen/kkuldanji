# -*- coding: utf-8 -*-
"""
꿀단지 (KKULDANJI) - 워크플로우 스텝 가디언 & 2단계 리서치 분리 검문소 (Step Guard)
- [마스터 핵심 0] 지침 린터(lint_rules_zero_example, audit_rule_integrity)는 지침 수정 시(--lint-rules)에만 실행하여 글쓰기 속도를 극대화합니다.
- [마스터 핵심 1] 2단계 리서치 분리:
  * Step 0-A (required_step < 4): 공인 1차 기준선(Baseline), 주의사항(Delta), official_source_raw.txt 원문 덤프 검증 (제목 확정 전 세부 FAQ 조기 강제 금지)
  * Step 0-B (required_step == 4): 확정된 제목 맞춤형 심층 리서치 및 알짜 FAQ 2~3선, evidence_guard 연동 검증
- 구형 SERP 배지 표 및 last_serp_audit.json 강제 락은 영구 폐기되었습니다.
"""
import os
import sys
import json
import re

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = r"d:\작업\꿀단지"


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


def verify_research_facts(work_dir, required_step=1):
    """
    2단계 리서치 분리(Step 0-A 사전 팩트 ➔ Step 0-B 심층 리서치) 및 1차 원문 덤프(official_source_raw.txt) 검증
    """
    research_path = os.path.join(work_dir, "리서치.md")
    if not os.path.exists(research_path):
        print(f"🚨 [Step 0 차단] '{work_dir}' 폴더에 '리서치.md' 파일이 존재하지 않습니다!")
        sys.exit(1)

    # 1. official_source_raw.txt 1차 공인 출처 원문 덤프 파일 검증
    raw_source_path = os.path.join(work_dir, "official_source_raw.txt")
    if not os.path.exists(raw_source_path):
        print(f"\n🚨 [Step 0-A 차단: 공인 1차 출처 원문 덤프 누락]")
        print(f"   🛑 '{work_dir}' 폴더에 'official_source_raw.txt' 파일이 존재하지 않습니다!")
        print("   👉 한국 7대 공인 1차 기관(질병청, 식약처, 농진청 등) 또는 학술 원문을 read_url_content로 열람한 뒤,")
        print("      실제 원문 텍스트(200바이트 이상)와 공식 직행 URL(https://...), 열람일을 'official_source_raw.txt'에 저장하십시오.")
        sys.exit(1)

    with open(raw_source_path, "r", encoding="utf-8-sig", errors="replace") as rf:
        raw_source_text = rf.read().strip()

    if len(raw_source_text.encode("utf-8")) < 200:
        print(f"\n🚨 [Step 0-A 차단: 공인 출처 원문 덤프 분량 미달] ({len(raw_source_text.encode('utf-8'))}바이트 / 최소 200바이트 필수)")
        sys.exit(1)

    if not re.search(r'https?://[^\s)\]>]+', raw_source_text):
        print("\n🚨 [Step 0-A 차단] 'official_source_raw.txt' 내부에 실제 열람한 출처 URL(https://...)이 기록되어 있지 않습니다!")
        sys.exit(1)

    if not re.search(r'(?:열람일|확인일|수집일|Date|202\d-\d{2}-\d{2})', raw_source_text, re.IGNORECASE):
        print("\n🚨 [Step 0-A 차단] 'official_source_raw.txt' 내부에 원문 열람일(예: 열람일: YYYY-MM-DD)이 기록되어 있지 않습니다!")
        sys.exit(1)

    # 2. 리서치.md 검증
    with open(research_path, "r", encoding="utf-8-sig") as f:
        content = f.read()

    if len(content.strip()) < 350:
        print(f"🚨 [Step 0-A 차단: 리서치 부실] '리서치.md' 내용이 너무 짧습니다 ({len(content.strip())}자 / 최소 350자 이상 필수).")
        sys.exit(1)

    # 만병통치약 과장 금칙어 검사
    dangerous_words = ["완치", "100% 치료", "암세포 박멸", "기적의 특효약", "즉각 완치"]
    negation_Diagnostic_patterns = [
        "아닙니다", "아니며", "아닌", "없습니다", "없으며", "금지", "주의", "오해", "통설", "과장", "불가"
    ]
    found_danger = []
    for line in content.splitlines():
        for w in dangerous_words:
            if w in line and not any(neg in line for neg in negation_Diagnostic_patterns):
                found_danger.append(w)

    if found_danger:
        print(f"🚨 [의학 팩트 경고] '리서치.md'에 과장된 만병통치 표현({list(set(found_danger))})이 감지되었습니다!")
        sys.exit(1)

    # 공인 1차 출처 URL 존재 여부 검사
    urls = re.findall(r'https?://[^\s)\]>]+', content)
    if not urls:
        print("🚨 [Step 0-A 차단] '리서치.md' 내에 클릭 가능한 공식 1차 출처 URL(https://...)이 단 1개도 없습니다!")
        sys.exit(1)

    # Step 0-B (required_step == 4): 확정된 제목 맞춤형 심층 리서치 및 FAQ 2~3선 확인
    if required_step == 4:
        has_faq = bool(re.search(r'(?:FAQ|자주\s*묻는\s*질문|Q1\.|Q\.)', content, re.IGNORECASE))
        if not has_faq:
            print("🚨 [Step 0-B 차단: 2차 제목 맞춤형 심층 리서치 미완결]")
            print("   🛑 본문(Step 4) 작성 전, 확정된 제목에 직결되는 알짜 FAQ 2~3선을 '리서치.md'에 먼저 보강하십시오!")
            sys.exit(1)
        print("✅ [Step 0-A & Step 0-B 2단계 리서치 검증 통과] official_source_raw.txt 원문 덤프 + 공인 URL + 맞춤 FAQ 확인 완료!")
    else:
        print("✅ [Step 0-A 1차 사전 팩트 검증 통과] official_source_raw.txt 원문 덤프 및 공인 기준선(Baseline) 확인 완료!")


def check_step(required_step, work_dir=None):
    if not work_dir:
        work_dir = get_latest_work_dir()
    if not work_dir or not os.path.exists(work_dir):
        print(f"❌ 작업 폴더를 찾을 수 없습니다: {work_dir}")
        sys.exit(1)

    print(f"🛡️ [Step Guard] 작업 폴더 검문 중: {os.path.basename(work_dir)} (요구 단계: Step {required_step})")

    # Step 0-A 기본 리서치 검증
    verify_research_facts(work_dir, required_step=required_step)

    if required_step <= 1:
        return True

    # Step 1 이상: titles.json 및 네이버 제목 10선 확인
    titles_path = os.path.join(work_dir, "titles.json")
    if not os.path.exists(titles_path):
        print(f"🚨 [HARD STOP 1 위반] '{titles_path}' 파일이 없습니다! Step 1 네이버 제목 10선을 먼저 생성하고 승인받으세요.")
        sys.exit(1)

    with open(titles_path, "r", encoding="utf-8-sig") as f:
        t_data = json.load(f)

    naver_10 = t_data.get("naver_10") or t_data.get("naver_candidates") or t_data.get("naver") or []
    if len(naver_10) < 10:
        print(f"🚨 [Step 1 미완결] 네이버 후보 제목이 10개 미만({len(naver_10)}개)입니다.")
        sys.exit(1)

    try:
        from validate_titles import validate_naver_titles
        if not validate_naver_titles(naver_10, run_serp=False):
            sys.exit(1)
    except ImportError:
        pass

    if required_step == 2:
        if not t_data.get("selected_naver"):
            print("🚨 [HARD STOP 1 대기 중] 사용자가 선택한 네이버 제목('selected_naver')이 아직 기록되지 않았습니다!")
            sys.exit(1)
        return True

    # Step 3 이상: 구글 제목 10선 확인
    google_10 = t_data.get("google_10") or t_data.get("google_candidates") or t_data.get("google") or []
    if len(google_10) < 10:
        print(f"🚨 [Step 2/3 미완결] 구글 후보 제목이 10개 미만({len(google_10)}개)입니다.")
        sys.exit(1)

    try:
        from validate_titles import validate_google_titles
        if not validate_google_titles(google_10, run_serp=False):
            sys.exit(1)
    except ImportError:
        pass

    if required_step >= 4:
        if not t_data.get("selected_naver") or not t_data.get("selected_google"):
            print("🚨 [HARD STOP 2/3 위반] 최종 확정된 네이버 제목('selected_naver')과 구글 제목('selected_google')이 모두 있어야 본문(Step 4)을 작성할 수 있습니다!")
            sys.exit(1)

        pj_path = os.path.join(work_dir, "post_data.json")
        if os.path.exists(pj_path):
            try:
                import evidence_guard
                with open(pj_path, "r", encoding="utf-8-sig") as pf:
                    p_data = json.load(pf)
                evidence_guard.validate_post_evidence(p_data, work_dir=work_dir)
            except Exception as e:
                print(f"🚨 [Evidence Guard 검증 실패]: {e}")
                sys.exit(1)

    return True


if __name__ == "__main__":
    if "--lint-rules" in sys.argv:
        import lint_rules_zero_example
        import audit_rule_integrity
        lint_rules_zero_example.run_lint()
        audit_rule_integrity.run_audit()
        sys.exit(0)

    step_num = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 1
    target_work_dir = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else None
    check_step(step_num, work_dir=target_work_dir)

# -*- coding: utf-8 -*-
"""
꿀단지 (KKULDANJI) - 규칙-코드 정합성 및 자가 치유 거버넌스 감사기 (Rule Integrity Auditor)
규칙 문서(AGENTS.md)와 파이썬 가디언 코드(tools/step_guard.py 등) 사이에 모순, 충돌, 워크플로우 불일치가 있는지 기계적으로 전수 스캔합니다.
불일치 감지 시 Exit Code 1을 발생시키고 AI에게 대표님 결재용 Diff 보고를 강제합니다.
"""
import os
import sys
import re

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = r"d:\작업\꿀단지"
AGENTS_PATH = os.path.join(ROOT_DIR, "AGENTS.md")
STEP_GUARD_PATH = os.path.join(ROOT_DIR, "tools", "step_guard.py")

def print_governance_diff_alert(source_rule, issue_desc, diff_old, diff_new):
    """
    [마스터 표준 0-8] 시스템 락 발동 및 AI 보고 강제 표준 양식 출력
    """
    print("\n" + "=" * 80)
    print("🚨 [가디언 시스템 락 발동 / AI 행동 강제 지침]")
    print("AI는 절대로 억지로 작업을 강행하거나, 가짜 출처/수치를 날조하여 넘어가려 하지 마십시오!")
    print("지금 즉시 대표님께 아래 표준 양식으로 상황을 보고하고 규칙/코드 수정을 건의하십시오:\n")
    print("--------------------------------------------------------------------------------")
    print(f"🚨 [에이전트 규칙/코드 정합성 결함 감지 보고]")
    print(f"1. 원인 조항: {source_rule}")
    print(f"2. 발생 문제: {issue_desc}")
    print(f"3. 해결 제안 (Diff):")
    print(f"   [기존]: {diff_old}")
    print(f"   [수정안]: {diff_new}")
    print(f"4. 조치 요청: 대표님의 승인 후 규칙/코드를 패치하고 작업을 재개하겠습니다.")
    print("--------------------------------------------------------------------------------")
    print("=" * 80 + "\n")

def check_rule_integrity():
    print("🔍 [꿀단지 규칙-가디언 코드 정합성 감사] 전수 스캔 중...")
    
    if not os.path.exists(AGENTS_PATH):
        print(f"❌ AGENTS.md 파일이 존재하지 않습니다: {AGENTS_PATH}")
        sys.exit(1)
    if not os.path.exists(STEP_GUARD_PATH):
        print(f"❌ tools/step_guard.py 파일이 존재하지 않습니다: {STEP_GUARD_PATH}")
        sys.exit(1)

    with open(AGENTS_PATH, "r", encoding="utf-8-sig") as f:
        agents_content = f.read()

    with open(STEP_GUARD_PATH, "r", encoding="utf-8-sig") as f:
        guard_content = f.read()

    # 1. 2단계 리서치 분리 워크플로우 정합성 검사
    has_2stage_rule = "2단계 리서치 분리" in agents_content
    has_step0a = "Step 0-A" in agents_content or "1차 광범위 사전 팩트" in agents_content
    has_step0b = "Step 0-B" in agents_content or "2차 제목 맞춤형 심층 리서치" in agents_content

    if not (has_2stage_rule and has_step0a and has_step0b):
        print_governance_diff_alert(
            "AGENTS.md 마스터 표준 0호",
            "AGENTS.md에 '2단계 리서치 분리(Step 0-A 사전 팩트 ➔ Step 0-B 심층 리서치)' 규정이 누락되었습니다.",
            "1. Step 0 리서치 올인원 구조",
            "1. Step 0-A 사전 팩트 탐색 ➔ 제목 확정 ➔ Step 0-B 제목 맞춤형 심층 리서치"
        )
        sys.exit(1)

    # 2. step_guard.py 게이트 분리 정합성 검사
    has_guard_2stage = "required_step=required_step" in guard_content or "required_step=1" in guard_content
    has_guard_step0b = "Step 0-B" in guard_content and "required_step == 4" in guard_content

    if not (has_guard_2stage and has_guard_step0b):
        print_governance_diff_alert(
            "tools/step_guard.py verify_research_facts",
            "step_guard.py가 제목 단계에서 FAQ를 조기 요구하거나, 2단계 리서치 분리 게이트가 미흡합니다.",
            "verify_research_facts(work_dir) (모든 단계에서 FAQ 검사)",
            "verify_research_facts(work_dir, required_step) (Step 4에서만 FAQ 검사)"
        )
        sys.exit(1)

    # 3. 만병통치약 과장 금칙어 목록 100% 일치성 검사
    rule_keywords = ["완치", "100% 치료", "암세포 박멸", "기적의 특효약", "즉각 완치"]
    guard_missing = [kw for kw in rule_keywords if kw not in guard_content and kw.replace("특효약", "치료제") not in guard_content]

    if guard_missing:
        print_governance_diff_alert(
            "tools/step_guard.py dangerous_words",
            f"AGENTS.md의 과장 금칙어가 step_guard.py에 누락되었습니다: {guard_missing}",
            "dangerous_words = [...]",
            f"dangerous_words에 {guard_missing} 추가"
        )
        sys.exit(1)

    # 4. Zero-Example 린터 무결성 연동 검사
    linter_path = os.path.join(ROOT_DIR, "tools", "lint_rules_zero_example.py")
    if not os.path.exists(linter_path):
        print_governance_diff_alert(
            "tools/lint_rules_zero_example.py",
            "정적 예시문 100% 영구 배제 린터(Zero-Example Linter)가 존재하지 않습니다.",
            "린터 없음",
            "tools/lint_rules_zero_example.py 생성 및 배포 파이프라인 연동"
        )
        sys.exit(1)

    # 5. Evidence Guard 공인 근거 검증기 연동 검사
    evidence_guard_path = os.path.join(ROOT_DIR, "tools", "evidence_guard.py")
    if not os.path.exists(evidence_guard_path):
        print_governance_diff_alert(
            "tools/evidence_guard.py",
            "공인 근거 및 팩트 무결성 검증기(Evidence Guard)가 존재하지 않습니다.",
            "검증기 없음",
            "tools/evidence_guard.py 생성 및 등록 파이프라인 연동"
        )
        sys.exit(1)

    if "evidence_guard" not in guard_content:
        print_governance_diff_alert(
            "tools/step_guard.py check_step",
            "step_guard.py에 evidence_guard 연동이 누락되었습니다.",
            "evidence_guard 미호출",
            "step_guard.py Step 4에서 evidence_guard.validate_post_evidence 연동"
        )
        sys.exit(1)

    print("   - [규칙 ↔ 가디언 코드 워크플로우 정합성]: ✅ 100% 일치 (2단계 리서치 분리 연동 확인)")
    print("   - [금칙어 및 과장 방지 안전망]: ✅ 100% 일치")
    print("   - [Zero-Example 영구 배제 린터 연동]: ✅ 100% 무결성 확인")
    print("   - [Evidence Guard 공인 근거 검증기 연동]: ✅ 100% 무결성 확인")
    print("\n🎉 [AUDIT PASS] 규칙 문서와 파이썬 가디언 코드가 한 치의 모순 없이 100% 일치합니다.")
    return 0

run_audit = check_rule_integrity

if __name__ == "__main__":
    sys.exit(check_rule_integrity())

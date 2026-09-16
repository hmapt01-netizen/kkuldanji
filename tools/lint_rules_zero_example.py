# -*- coding: utf-8 -*-
"""
꿀단지 (KKULDANJI) - 정적 예시문 및 하드코딩 100% 영구 배제 린터 (Zero-Example & Anti-Hardcoding Linter)
- 규칙 문서(AGENTS.md, GEMINI.md, SKILL.md) 내 괄호 예시문((예: ...)) 및 특정 정적 고유명사 차단
- 가디언 도구(tools/evidence_guard.py) 내 특정 포스트 전용 단어 하드코딩 원천 차단
"""
import os
import sys
import re

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = r"d:\작업\꿀단지"

# 1. 규칙 문서 검사 대상
RULE_FILES = [
    os.path.join(ROOT_DIR, "AGENTS.md"),
    os.path.join(ROOT_DIR, "GEMINI.md"),
    os.path.join(ROOT_DIR, "skills", "naver-honeyjar", "SKILL.md")
]

# 2. 가디언 도구 검사 대상 (추상 알고리즘 보존 검사)
GUARDIAN_TOOL_FILES = [
    os.path.join(ROOT_DIR, "tools", "evidence_guard.py")
]

# 괄호 예시문 패턴 (예: ...), (예시: ...), (e.g., ...), (ex: ...) 등 전면 차단
PARENTHETICAL_EXAMPLE_PATTERNS = [
    (r'\((?:예|예시|예를\s*들어|\b(?:e\.g\.|ex|보기)\b)\s*[:：,][^)]*\)', "괄호 예시문 패턴"),
    (r'\([^)]*(?:티스푼|종이컵|밥숟가락|소금물|물온도)[^)]*\)', "괄호 내 구체적 계량/소재 예시 패턴")
]

# 정적 고유명사 패턴
STATIC_NOUN_PATTERNS = [
    (r'(?<![가-힣])(마그네슘|오메가3|유산균|비타민D|글루타치온|콜라겐)(?![가-힣])', "특정 영양소/성분명 정적 예시"),
    (r'(?<![가-힣])(아스피린|타이레놀|이부프로펜)(?![가-힣])', "특정 약물명 정적 예시"),
    (r'(?<![가-힣])(바나나|아몬드|브로콜리|토마토)(?![가-힣])', "특정 식품명 정적 예시"),
]

# 가디언 도구 내 하드코딩 금지 패턴 (특정 포스트 땜빵 방지)
TOOL_HARDCODING_PATTERNS = [
    (r'(?:1~1\.8g|1\.0~1\.8g|3%|38\.5도|38\.5℃|15~20초)', "특정 포스트 수치 하드코딩"),
    (r'(?:찬물\s*혈액순환|미온수.*이완|굵은\s*소금.*상처)', "특정 포스트 민간 생리학 하드코딩"),
    (r'(?:치약\s*잔여물|식후\s*30\s*분)', "특정 포스트 시차/충돌 하드코딩")
]


def lint_rule_file(file_path):
    if not os.path.exists(file_path):
        return True

    with open(file_path, "r", encoding="utf-8-sig") as f:
        lines = f.readlines()

    violations = []
    is_meta_section = False

    for idx, line in enumerate(lines, 1):
        # 메타 설명 섹션 스킵
        if "정적 예시문 100% 영구 배제 원칙" in line or "Zero-Example" in line:
            is_meta_section = True
            continue
        if line.startswith("## ") or line.startswith("### "):
            is_meta_section = False

        if is_meta_section:
            continue

        # 과거 DB 목록 등 스킵
        if "기발행 글" in line or "posts_db.json" in line:
            continue

        # 1. 괄호 예시문 검출
        for pattern, desc in PARENTHETICAL_EXAMPLE_PATTERNS:
            matches = re.findall(pattern, line, flags=re.IGNORECASE)
            if matches:
                violations.append((idx, line.strip(), desc, matches))

        # 2. 정적 고유명사 검출
        for pattern, desc in STATIC_NOUN_PATTERNS:
            matches = re.findall(pattern, line)
            if matches:
                violations.append((idx, line.strip(), desc, matches))

    if violations:
        print(f"\n🚨 [규칙 LINT 실패] '{os.path.basename(file_path)}'에서 정적 예시/괄호 패턴 {len(violations)}건 감지!")
        print(f"   🛑 사유: 규칙에 괄호 예시나 구체적 단어가 적히면 AI가 해당 단어에 앵커링되어 글 작성을 복제합니다.")
        print(f"   👉 원칙: 괄호 예시를 모두 제거하고 순수 추상 공식 및 구조 변수([주어]+[조건]+[데이터])로 치환하십시오.\n")
        for line_no, text, desc, matched in violations[:10]:
            print(f"   - L{line_no}: [{desc}: {', '.join(set(matched))}] ➔ \"{text[:70]}...\"")
        return False

    print(f"   ✓ '{os.path.basename(file_path)}' 괄호 예시 및 정적 명사 0개 확인 (Zero-Example 무결성 100%)")
    return True


def lint_guardian_tools(file_path):
    if not os.path.exists(file_path):
        return True

    with open(file_path, "r", encoding="utf-8-sig") as f:
        lines = f.readlines()

    violations = []
    for idx, line in enumerate(lines, 1):
        # 주석 제외
        stripped = line.strip()
        if stripped.startswith("#"):
            continue

        for pattern, desc in TOOL_HARDCODING_PATTERNS:
            matches = re.findall(pattern, line)
            if matches:
                violations.append((idx, line.strip(), desc, matches))

    if violations:
        print(f"\n🚨 [가디언 코드 LINT 실패] '{os.path.basename(file_path)}'에서 단일 포스트 땜빵 하드코딩 {len(violations)}건 감지!")
        print(f"   🛑 사유: 가디언 코드에 특정 글의 단어/수치를 하드코딩하면 다른 글 작성 시 전혀 작동하지 않는 일회용 코드가 됩니다.")
        print(f"   👉 원칙: 특정 단어를 하드코딩하지 말고, evidence_manifest.json의 evidence_quote와 수치 집합 대조(Mathematical Quantity Grounding)로 구현하십시오.\n")
        for line_no, text, desc, matched in violations[:10]:
            print(f"   - L{line_no}: [{desc}: {', '.join(set(matched))}] ➔ \"{text[:70]}...\"")
        return False

    print(f"   ✓ '{os.path.basename(file_path)}' 단일 포스트 땜빵 하드코딩 0개 확인 (추상 알고리즘 무결성 100%)")
    return True


def run_linter():
    print("================================================================================")
    print("🛡️ [Zero-Example & Anti-Hardcoding Linter] 규칙 및 가디언 도구 전수 감사")
    print("================================================================================")
    all_pass = True

    # 1. 규칙 문서 검사
    for fp in RULE_FILES:
        if not lint_rule_file(fp):
            all_pass = False

    # 2. 가디언 도구 검사
    for fp in GUARDIAN_TOOL_FILES:
        if not lint_guardian_tools(fp):
            all_pass = False

    if not all_pass:
        print("\n❌ 린트 검증 실패: 괄호 예시문 또는 가디언 코드 내 하드코딩을 제거해야 합니다 (Exit Code 1).")
        return 1
    print("================================================================================")
    return 0


def run_lint():
    code = run_linter()
    if code != 0:
        sys.exit(code)
    return True


if __name__ == "__main__":
    run_lint()

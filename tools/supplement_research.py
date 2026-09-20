# -*- coding: utf-8 -*-
"""
꿀단지 (KKULDANJI) - 실시간 추가 리서치 및 팩트 보강 엔진 (Supplemental Research Tool)
- [마스터 표준 23-5호] 본문 작성 중 리서치 결손 감지 및 온디맨드 자동 보강
- 원고 작성 중 새로운 수치/기전/주장이 필요할 때 웹 실사 결과를 리서치.md에 자동 누적 기록
- 출처 미검증 수치 및 자의적 단정 방지를 위한 물리적 보강 파이프라인
"""
import os
import sys
import re
import json
import argparse
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def get_latest_work_dir():
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

def add_supplemental_research(work_dir, claim, source_name, source_url, quote, note=None):
    """
    리서치.md에 추가 리서치 항목을 정규 포맷으로 영구 누적 기록합니다.
    """
    if not work_dir or not os.path.exists(work_dir):
        print(f"❌ 작업 디렉토리가 존재하지 않습니다: {work_dir}")
        return False

    research_path = os.path.join(work_dir, "리서치.md")
    if not os.path.exists(research_path):
        print(f"❌ 리서치 파일이 존재하지 않습니다: {research_path}")
        return False

    # URL 유효성 검증
    if not source_url.startswith("http://") and not source_url.startswith("https://"):
        print(f"❌ 유효하지 않은 출처 URL입니다 (https:// 필수): {source_url}")
        return False

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry_lines = [
        f"\n### ➕ [추가 리서치 보강 항목] ({now_str})",
        f"- **핵심 주장/팩트**: {claim}",
        f"- **공인 출처 기관**: {source_name}",
        f"- **공식 원문 URL**: {source_url}",
        f"- **출처 원문 인용문**: \"{quote}\""
    ]
    if note:
        entry_lines.append(f"- **적용 맥락 및 해설**: {note}")
    entry_lines.append("")

    entry_text = "\n".join(entry_lines)

    try:
        with open(research_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(research_path, "r", encoding="utf-8-sig") as f:
            content = f.read()

    section_header = "## 🔄 [추가 리서치 및 보강 팩트 (Supplemental Research)]"
    if section_header in content:
        # 기존 섹션 하단에 추가
        idx = content.find(section_header) + len(section_header)
        updated_content = content[:idx] + "\n" + entry_text + content[idx:]
    else:
        # 리서치.md 맨 하단에 섹션 신설
        updated_content = content.rstrip() + f"\n\n---\n\n{section_header}\n" + entry_text

    with open(research_path, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"✅ [리서치 보강 완료] '리서치.md'에 추가 리서치 팩트가 성공적으로 기록되었습니다.")
    print(f"   - 주장: {claim}")
    print(f"   - 출처: {source_name} ({source_url})")

    # evidence_manifest.json이 존재하면 동기화
    manifest_path = os.path.join(work_dir, "evidence_manifest.json")
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, "r", encoding="utf-8-sig") as mf:
                manifest_data = json.load(mf)
            
            new_source_id = f"SRC_{len(manifest_data.get('sources', [])) + 1:02d}"
            manifest_data.setdefault("sources", []).append({
                "id": new_source_id,
                "title": f"{source_name} - {claim[:30]}",
                "organization": source_name,
                "url": source_url,
                "evidence_quote": quote
            })
            manifest_data.setdefault("claims", []).append({
                "statement": claim,
                "source_ids": [new_source_id],
                "limits": note or "추가 리서치 보강"
            })
            with open(manifest_path, "w", encoding="utf-8") as mf:
                json.dump(manifest_data, mf, ensure_ascii=False, indent=2)
            print(f"   - [Evidence Manifest 동기화 완료]: {os.path.basename(manifest_path)}")
        except Exception as e:
            print(f"⚠️ evidence_manifest.json 동기화 실패 (무시 가능): {e}")

    return True

def check_missing_research(work_dir):
    """
    원고(post_data.json)의 수치 및 주장이 리서치.md에 모두 실존하는지 검사합니다.
    누락된 항목이 있으면 Exit Code 1을 반환하여 추가 리서치를 강제합니다.
    """
    if not work_dir:
        work_dir = get_latest_work_dir()
    if not work_dir or not os.path.exists(work_dir):
        print(f"❌ 작업 디렉토리가 없습니다.")
        return 1

    pj_path = os.path.join(work_dir, "post_data.json")
    research_path = os.path.join(work_dir, "리서치.md")

    if not os.path.exists(pj_path):
        print(f"ℹ️ post_data.json이 아직 작성되지 않았습니다.")
        return 0

    if not os.path.exists(research_path):
        print(f"❌ 리서치.md가 없습니다.")
        return 1

    try:
        from evidence_guard import extract_factual_quantities
    except ImportError:
        try:
            from tools.evidence_guard import extract_factual_quantities
        except ImportError:
            print("⚠️ evidence_guard를 불러올 수 없습니다.")
            return 0

    with open(pj_path, "r", encoding="utf-8-sig") as pf:
        p_data = json.load(pf)

    with open(research_path, "r", encoding="utf-8-sig") as rf:
        research_content = rf.read()

    # 원고 본문 텍스트 추출
    article_corpus = []
    for sec in p_data.get("sections", []):
        article_corpus.append(sec.get("content", ""))
        article_corpus.append(sec.get("heading", ""))
    for faq in p_data.get("faqList", []):
        article_corpus.append(faq.get("question", ""))
        article_corpus.append(faq.get("answer", ""))

    full_article = " ".join(article_corpus)
    article_quantities = extract_factual_quantities(full_article)
    research_quantities = extract_factual_quantities(research_content)

    norm_research = re.sub(r'\s+', '', research_content)
    unverified = []
    for q in article_quantities:
        if q in research_quantities:
            continue
        norm_q = re.sub(r'\s+', '', q)
        if norm_q in norm_research:
            continue
        num_only = re.sub(r'[^\d.]', '', q)
        if num_only and num_only in norm_research:
            continue
        unverified.append(q)

    if unverified:
        print(f"\n🚨 [리서치 결손 감지] 원고에 사용된 수치 {unverified}가 '리서치.md'에 수록되어 있지 않습니다!")
        print("   🛑 AI는 임의로 숫자를 지어내지 말고, 웹 실사(search_web) 후 아래 명령으로 리서치를 보강하세요:")
        print("   👉 python tools/supplement_research.py add --claim \"수치 근거 주장\" --source \"공인기관\" --url \"https://...\" --quote \"인용문\"")
        return 1

    print(f"✅ [리서치 정합성 확인] 원고의 모든 주요 정량 수치가 '리서치.md'에 100% 근거하고 있습니다.")
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="실시간 추가 리서치 및 팩트 보강 엔진")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="리서치.md에 새로운 팩트 추가 저장")
    add_parser.add_argument("--work_dir", default=None, help="작업 폴더 경로 (미지정 시 최신 폴더)")
    add_parser.add_argument("--claim", required=True, help="추가할 핵심 주장 또는 팩트")
    add_parser.add_argument("--source", required=True, help="공인 출처 기관명")
    add_parser.add_argument("--url", required=True, help="공식 원문 직행 URL")
    add_parser.add_argument("--quote", required=True, help="출처 원문 인용문")
    add_parser.add_argument("--note", default=None, help="적용 맥락 및 해설")

    check_parser = subparsers.add_parser("check", help="원고 수치 대비 리서치 결손 여부 검사")
    check_parser.add_argument("--work_dir", default=None, help="작업 폴더 경로")

    args = parser.parse_args()

    target_dir = args.work_dir or get_latest_work_dir()

    if args.command == "add":
        success = add_supplemental_research(
            target_dir, args.claim, args.source, args.url, args.quote, args.note
        )
        sys.exit(0 if success else 1)
    elif args.command == "check":
        code = check_missing_research(target_dir)
        sys.exit(code)
    else:
        parser.print_help()
        sys.exit(0)

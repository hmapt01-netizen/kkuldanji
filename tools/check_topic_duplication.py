#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_topic_duplication.py (꿀단지 전용)
신규 건강/웰니스 주제 추천 및 발굴 시 기존 DB(posts_db.json) 내 중복 여부를 기계적으로 전수 검증하는 도구
사용법: python tools/check_topic_duplication.py <키워드1> [키워드2 ...]
"""

import sys
import os
import json
import io

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT_DIR, "data", "posts_db.json")

def audit_topics(keywords):
    if not os.path.exists(DB_PATH):
        print(f"❌ [오류] DB 파일이 존재하지 않습니다: {DB_PATH}")
        sys.exit(1)

    with open(DB_PATH, "r", encoding="utf-8") as f:
        posts = json.load(f)

    # 1. 최신 날짜순 정렬
    sorted_posts = sorted(posts, key=lambda p: p.get("date", ""), reverse=True)

    print("=" * 70)
    print(f"🍯 [꿀단지 DB 전수 현황] 총 {len(posts)}개 포스트 등록됨")
    print("=" * 70)
    print("📌 [최근 발행된 최신 글 Top 5]")
    for p in sorted_posts[:5]:
        print(f"  - [{p.get('date', '날짜미상')}] {p.get('title', '')}")
    print("=" * 70)

    if not keywords:
        print("ℹ️ 키워드를 입력하면 해당 주제의 기존 발행 여부를 전수 검사합니다.")
        print("   예: python tools/check_topic_duplication.py 건강검진 금식 커피")
        return

    print("\n🔍 [후보 키워드 중복 전수 교차 검증]")
    duplicate_found = False

    for kw in keywords:
        kw_lower = kw.lower().strip()
        matched = []
        for p in posts:
            title = p.get("title", "")
            excerpt = p.get("excerpt", "")
            if kw_lower in title.lower() or kw_lower in excerpt.lower():
                matched.append(p)

        if matched:
            duplicate_found = True
            print(f"\n⚠️  키워드: '{kw}' ➔ 기존 {len(matched)}건 발견! (주의 필요)")
            for m in matched[:5]:
                print(f"     ㄴ [{m.get('date', '')}] {m.get('title', '')}")
            if len(matched) > 5:
                print(f"     ㄴ ...외 {len(matched) - 5}건 더 있음")
        else:
            print(f"\n✅  키워드: '{kw}' ➔ 기존 글 0건! [완전 미작성 블루오션 PASS]")

    print("\n" + "=" * 70)
    if duplicate_found:
        print("💡 [검증 결과]: 기존에 다룬 이력이 있는 키워드가 포함되어 있습니다.")
        print("   이미 다룬 질환/영양소는 완전히 새로운 관점/비교 대상이 아니라면 제외하세요.")
    else:
        print("🎉 [검증 결과]: 모든 후보 키워드가 기존 DB에 없는 신규 주제입니다! (추천 가능)")
    print("=" * 70)

if __name__ == "__main__":
    kw_args = sys.argv[1:]
    audit_topics(kw_args)

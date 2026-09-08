#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_topic_duplication.py (꿀단지 전용 - 앵글 확장 검증 지원)
신규 건강/웰니스 주제 추천 및 발굴 시 기존 DB(posts_db.json) 내 중복 여부 및
[마스터 표준 0-1-B] 과거 주제 앵글 확장(리사이클) 가능 여부를 기계적으로 전수 검증하는 도구
사용법: python tools/check_topic_duplication.py <키워드1> [키워드2 ...]
"""

import sys
import os
import json
import io
import re
from datetime import datetime

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT_DIR, "data", "posts_db.json")

# 앵글 확장 식별 키워드 (4대 공식)
ANGLE_EXPANSION_MODIFIERS = [
    "부작용", "설사", "속쓰림", "울렁거림", "복통", "실패", 
    "보관", "냉장", "냉동", "재가열", "저항성전분", "극대화",
    "응급", "삐끗", "담", "통증", "이완", "비교", "차이", "vs", "끝장"
]

def parse_date(date_str):
    try:
        # e.g. "2026.09.08" or "2026-09-08"
        clean = re.sub(r'[^0-9]', '.', date_str).strip('.')
        parts = [int(p) for p in clean.split('.') if p]
        if len(parts) >= 3:
            return datetime(parts[0], parts[1], parts[2])
    except Exception:
        pass
    return None

def audit_topics(keywords):
    if not os.path.exists(DB_PATH):
        print(f"❌ [오류] DB 파일이 존재하지 않습니다: {DB_PATH}")
        sys.exit(1)

    with open(DB_PATH, "r", encoding="utf-8") as f:
        posts = json.load(f)

    # 1. 최신 날짜순 정렬
    sorted_posts = sorted(posts, key=lambda p: p.get("date", ""), reverse=True)
    now = datetime.now()

    print("=" * 75)
    print(f"🍯 [꿀단지 DB 전수 현황] 총 {len(posts)}개 포스트 등록됨")
    print("=" * 75)
    print("📌 [최근 발행된 최신 글 Top 5]")
    for p in sorted_posts[:5]:
        print(f"  - [{p.get('date', '날짜미상')}] {p.get('title', '')}")
    print("=" * 75)

    if not keywords:
        print("ℹ️ 키워드를 입력하면 해당 주제의 기존 발행 여부를 전수 검사합니다.")
        print("   예: python tools/check_topic_duplication.py \"저속노화 밥\" \"마그네슘 설사\"")
        return

    print("\n🔍 [후보 키워드 중복 전수 교차 검증 & 앵글 확장 판정]")

    for kw in keywords:
        kw_lower = kw.lower().strip()
        matched = []
        for p in posts:
            title = p.get("title", "")
            desc = p.get("desc", p.get("summary", ""))
            if kw_lower in title.lower() or kw_lower in desc.lower():
                matched.append(p)
            else:
                # 단어 단위 매칭 (예: '저속노화'와 '밥')
                sub_words = [w for w in kw_lower.split() if len(w) >= 2]
                if len(sub_words) >= 2 and all(w in title.lower() for w in sub_words):
                    matched.append(p)

        # 중복 검사 및 앵글 확장 판정
        has_angle_modifier = any(mod in kw_lower for mod in ANGLE_EXPANSION_MODIFIERS)

        if matched:
            most_recent_post = matched[0]
            p_date = parse_date(most_recent_post.get("date", ""))
            days_diff = (now - p_date).days if p_date else 999

            if days_diff >= 20 and has_angle_modifier:
                print(f"\n💎  키워드: '{kw}' ➔ [앵글 확장 승인 PASS!]")
                print(f"     ㄴ 기존 관련 글: [{most_recent_post.get('date')}] {most_recent_post.get('title')}")
                print(f"     ㄴ 판정 근거: 발행 후 {days_diff}일 경과 + 신규 앵글(부작용/보관/비교/응급) 결합 확인!")
                print(f"     ㄴ 기대 효과: 기존 글과 상호 잠식 없이 양방향 맞링크(Hub & Spoke) 체류시간 2배 시너지")
            else:
                print(f"\n⚠️  키워드: '{kw}' ➔ 기존 {len(matched)}건 발견! (주의 필요)")
                for m in matched[:3]:
                    print(f"     ㄴ [{m.get('date', '')}] {m.get('title', '')}")
                if days_diff < 20:
                    print(f"     🛑 [차단 사유]: 직전 발행일로부터 {days_diff}일밖에 지나지 않았습니다 (최소 20일 이상 경과 권장).")
                elif not has_angle_modifier:
                    print(f"     🛑 [차단 사유]: 기존 글과 겹치는 단순 재탕 위험. (부작용, 보관법, 비교 등 새로운 앵글 필요).")
        else:
            print(f"\n✅  키워드: '{kw}' ➔ 기존 글 0건! [완전 미작성 블루오션 PASS]")

    print("\n" + "=" * 75)
    print("🔒 [검증 요약]: 앵글 확장 승인(💎) 또는 완전 신규(✅) 주제는 안전하게 추천 가능합니다.")
    print("=" * 75)

if __name__ == "__main__":
    kw_args = sys.argv[1:]
    audit_topics(kw_args)

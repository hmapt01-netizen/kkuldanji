# -*- coding: utf-8 -*-
"""
꿀단지 (KKULDANJI) - 하이브리드 실시간 키워드 & 쇼핑 커넥트 뷰어 (view_top_keywords.py)

1. 꿀단지 공식 3대 카테고리(홈트레이닝, 식단 & 영양, 라이프 웰니스) 완벽 일치.
2. 하이브리드 융합 엔진:
   - 스트림 A: 네이버 데이터랩 쇼핑인사이트 실시간 핫 아이템 (쇼핑 커넥트 제휴)
   - 스트림 B: 당월 캘린더 엔진(10월 환절기/독감/검진) + 부위별 해부학/질환 루트 (E-E-A-T 트래픽)
3. 네이버 공식 검색광고 API 실시간 수집 및 황금 트래픽 구간(1,000~30,000회) 선별.
4. 네이버 쇼핑 커넥트(커머스 수익화) 연계 적합성 1:1 자동 태깅.
"""
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR / "tools"))

from naver_searchad import fetch_keyword_stats
from topic_taxonomy import (
    HONEYJAR_CATEGORIES,
    NEGATIVE_WORDS,
    check_existing,
    get_hybrid_seeds,
    detect_shopping_connect
)

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def load_existing_posts():
    path = ROOT_DIR / "data/posts_db.json"
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


CAT_ALIASES = {
    "all": list(HONEYJAR_CATEGORIES.keys()),
    "hometraining": ["hometraining"],
    "home": ["hometraining"],
    "exercise": ["hometraining"],
    "diet_nutrition": ["diet_nutrition"],
    "diet": ["diet_nutrition"],
    "nutrition": ["diet_nutrition"],
    "life_wellness": ["life_wellness"],
    "wellness": ["life_wellness"],
    "life": ["life_wellness"]
}


def print_table(items, posts, title, limit=10, start=1):
    print("\n" + "=" * 102)
    print(f"  📌 {title} (총 {len(items):,}개 유효 키워드 중 {start}위 ~ {min(len(items), start + limit - 1)}위)")
    print("=" * 102)
    print(f"{'순위':<4} | {'키워드':<18} | {'월간 총검색량':>11} | {'모바일':>9} | {'경쟁도':^5} | {'쇼핑 커넥트':<14} | {'기발행 여부'}")
    print("-" * 102)

    end_idx = min(len(items), start - 1 + limit)
    for idx, it in enumerate(items[start - 1:end_idx], start):
        kw = it["keyword"]
        tot_str = f"{it['total_volume']:,}회"
        mo_str = f"{it['mobile_volume']:,}회"
        sc = detect_shopping_connect(kw)
        sc_str = f"🛒 [{sc['product_type']}]" if sc["eligible"] else "ℹ️ 정보형"
        dup = check_existing(kw, posts)
        status = f"✅ [{dup.get('title', '')[:16]}..]" if dup else "✨ [신규 미발행]"
        print(f"{idx:<4} | {kw:<18} | {tot_str:>11} | {mo_str:>9} | {it['comp_idx']:^5} | {sc_str:<14} | {status}")


def main():
    parser = argparse.ArgumentParser(description="꿀단지 하이브리드 실시간 키워드 뷰어 (3대 공식 카테고리)")
    parser.add_argument("--cat", choices=list(CAT_ALIASES.keys()), default="all",
                        help="조회 카테고리 (all, hometraining, diet_nutrition, life_wellness)")
    parser.add_argument("--limit", type=int, default=10, help="카테고리당 출력 개수 (기본 10개)")
    parser.add_argument("--min-vol", type=int, default=1000, help="최소 월간 검색량 (기본 1,000회)")
    parser.add_argument("--max-vol", type=int, default=30000, help="최대 월간 검색량 (기본 30,000회, 0이면 무제한)")
    parser.add_argument("--fixed", action="store_true", help="셔플 없이 고정 시드 사용")
    args = parser.parse_args()

    posts = load_existing_posts()
    selected_pillars = CAT_ALIASES[args.cat]
    curr_month = datetime.now().month

    print("=" * 102)
    print(f"  🚀 [꿀단지 하이브리드 실시간 키워드 & 쇼핑 커넥트 엔진]")
    print(f"  - 3대 카테고리: 홈트레이닝, 식단 & 영양, 라이프 웰니스 (총 {len(selected_pillars)}개)")
    print(f"  - 스트림 A (소비/쇼핑): 네이버 데이터랩 쇼핑인사이트 실시간 랭킹 자동 융합")
    print(f"  - 스트림 B (의학/증상): {curr_month}월 캘린더 환절기 시의성 + 해부학/질환 루트 결합")
    print(f"  - 실측 검증: 네이버 공식 검색광고 API 월간 검색량 {args.min_vol:,}회 ~ {args.max_vol:,}회 (저지수 공략 구간)")
    print("=" * 102)

    for p_key in selected_pillars:
        p_info = HONEYJAR_CATEGORIES[p_key]
        hybrid_seeds = get_hybrid_seeds(p_key, count_roots=2, count_datalab=3, shuffle=not args.fixed)
        raw_items = fetch_keyword_stats(hybrid_seeds)

        valid_items = []
        for it in raw_items:
            kw = it["keyword"]
            # 0. 과도하게 짧거나 포괄적인 단어 필터
            if len(kw.replace(" ", "")) <= 2:
                continue
            if kw in ("운동", "헬스", "건강", "병원", "식품", "의학"):
                continue
            # 1. 잡음/광고/비의료 필터
            if any(neg in kw for neg in NEGATIVE_WORDS):
                continue
            # 2. 검색량 필터
            tot = it["total_volume"]
            if tot < args.min_vol:
                continue
            if args.max_vol > 0 and tot > args.max_vol:
                continue
            valid_items.append(it)

        # 중복 제거 및 검색량 내림차순 정렬
        seen = set()
        dedup_items = []
        for it in sorted(valid_items, key=lambda x: x["total_volume"], reverse=True):
            if it["keyword"] not in seen:
                seen.add(it["keyword"])
                dedup_items.append(it)

        extra = f" ({curr_month}월 시의성 반영)" if p_key == "life_wellness" else ""
        title = f"[{p_info['name']}{extra}] (융합 투입 시드: {', '.join(hybrid_seeds)})"
        print_table(dedup_items, posts, title, limit=args.limit)


if __name__ == "__main__":
    main()

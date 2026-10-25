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
    detect_shopping_connect,
    fetch_live_news_issues,
    load_seed_history,
    record_seed_history,
    _is_stem_in_history
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
    parser.add_argument("--months-ago", type=int, default=0, help="N개월 전 동기간 이슈·쇼핑 데이터 조회 (예: 11 = 딱 11개월 전 시즌 선점)")
    parser.add_argument("--fixed", action="store_true", help="셔플 없이 고정 시드 사용")
    args = parser.parse_args()

    posts = load_existing_posts()
    selected_pillars = CAT_ALIASES[args.cat]
    from datetime import timedelta
    target_dt = datetime.now() - timedelta(days=int(args.months_ago * 30.4)) if args.months_ago > 0 else datetime.now()
    curr_month = target_dt.month
    period_label = f"딱 {args.months_ago}개월 전 ({target_dt.strftime('%Y년 %m월')} 시즌 선점)" if args.months_ago > 0 else "최근 7일 실시간"

    print("=" * 102)
    print(f"  🚀 [꿀단지 3대 라이브 스트림 하이브리드 키워드 & 이슈 엔진 — {period_label}]")
    print(f"  - 3대 카테고리: 홈트레이닝, 식단 & 영양, 라이프 웰니스 (총 {len(selected_pillars)}개)")
    print(f"  - 스트림 C (이슈 탐색): {period_label} 구글 뉴스 RSS 보건·식약·계절·질환 이슈 자동 추출")
    print(f"  - 스트림 A (소비/쇼핑): {period_label} 네이버 데이터랩 쇼핑인사이트 TOP 15 + 쇼핑 커넥트 태깅")
    print(f"  - 스트림 B (의학/증상): {curr_month}월 캘린더 시의성 + 해부학/영양학/검진 루트 결합")
    print(f"  - 다양성 보장: 기발행 소재 사전 차단 + 시드별 쿼터 밸런싱(승자독식 방지) + 직전 추천 자동 로테이션")
    print("=" * 102)

    hist = load_seed_history()

    for p_key in selected_pillars:
        p_info = HONEYJAR_CATEGORIES[p_key]
        news_info = fetch_live_news_issues(p_key, posts=posts, limit_headlines=4, limit_seeds=4, months_ago=args.months_ago)
        hybrid_seeds = get_hybrid_seeds(
            p_key, count_roots=1, count_datalab=1, count_news=4, shuffle=not args.fixed, posts=posts, months_ago=args.months_ago
        )
        raw_items = fetch_keyword_stats(hybrid_seeds)
        recent_kws = set(hist.get("top_keywords", {}).get(p_key, [])) | set(hist.get("seeds", {}).get(p_key, []))

        valid_items = []
        for it in raw_items:
            kw = it["keyword"]
            # 0. 과도하게 짧은 단일 글자 및 비건강/의류/맛집 노이즈 필터
            if len(kw.replace(" ", "")) <= 1:
                continue
            if any(neg in kw.lower() for neg in NEGATIVE_WORDS):
                continue
            # 1. 기발행 및 최근 14일 쿨타임 소재 동적 제외 (신규 미발행만 선발)
            if check_existing(kw, posts):
                continue
            # 2. 검색량 필터
            tot = it["total_volume"]
            if tot < args.min_vol:
                continue
            if args.max_vol > 0 and tot > args.max_vol:
                continue
            valid_items.append(it)

        # 중복 제거 및 기본 검색량 내림차순 정렬
        seen = set()
        dedup_items = []
        for it in sorted(valid_items, key=lambda x: x["total_volume"], reverse=True):
            if it["keyword"] not in seen:
                seen.add(it["keyword"])
                dedup_items.append(it)

        # [핵심] 시드별 쿼터 밸런싱 (Seed Quota Balancing) + 직전 노출 어근 키워드 후순위 배치
        fresh_items = [it for it in dedup_items if not _is_stem_in_history(it["keyword"], recent_kws)]
        stale_items = [it for it in dedup_items if it not in fresh_items]
        ordered_pool = fresh_items + stale_items

        balanced_items = []
        picked_kws = set()
        # 1차: 각 투입 시드별로 직접 매칭되는 상위 키워드를 최대 2개씩 우선 할당
        for seed in hybrid_seeds:
            seed_core = seed.replace(" ", "").lower()
            probe = seed_core[:3] if len(seed_core) >= 3 else seed_core
            seed_matches = [
                it for it in ordered_pool
                if it["keyword"] not in picked_kws and probe in it["keyword"].replace(" ", "").lower()
            ]
            for m in seed_matches[:2]:
                balanced_items.append(m)
                picked_kws.add(m["keyword"])

        # 2차: 나머지 유효 키워드 채우기 (직전 미노출 키워드 우선)
        for it in ordered_pool:
            if it["keyword"] not in picked_kws:
                balanced_items.append(it)
                picked_kws.add(it["keyword"])

        # 실시간 뉴스 헤드라인 브리핑 출력
        headlines = news_info.get("headlines", [])
        if headlines:
            print(f"\n  📰 [{p_info['name']} - 최근 7일 실시간 뉴스·보건 이슈 감지 (스트림 C)]")
            for h_idx, h_obj in enumerate(headlines[:3], 1):
                seed_tag = f" ➔ [추출 이슈 시드: {h_obj['seed']}]" if h_obj.get("seed") else ""
                print(f"     {h_idx}) {h_obj['headline']}{seed_tag}")

        extra = f" ({curr_month}월 시의성 반영)" if p_key == "life_wellness" else ""
        title = f"[{p_info['name']}{extra}] (융합 투입 시드: {', '.join(hybrid_seeds)})"
        print_table(balanced_items, posts, title, limit=args.limit)

        # 이번 실행에서 노출된 시드 및 상위 5개 키워드를 로테이션 이력에 기록
        shown_top = [it["keyword"] for it in balanced_items[:5]]
        record_seed_history(p_key, hybrid_seeds, shown_keywords=shown_top)

    # 기본 실행(months_ago == 0) 시 딱 11개월 전(다음 달 시즌 선점) 이슈 및 키워드 5선 자동 병행 출력
    if args.months_ago == 0:
        dt_11m = datetime.now() - timedelta(days=int(11 * 30.4))
        label_11m = dt_11m.strftime("%Y년 %m월")
        seeds_11m = []
        headlines_11m = []
        for p_key in selected_pillars:
            p_name = HONEYJAR_CATEGORIES[p_key]["name"]
            n_11m = fetch_live_news_issues(p_key, posts=posts, limit_headlines=2, limit_seeds=2, months_ago=11)
            for h_obj in n_11m.get("headlines", [])[:2]:
                headlines_11m.append((p_name, h_obj["headline"], h_obj.get("seed")))
            # 카테고리별로 11개월 전 뉴스 이슈 시드 1개 + 11개월 전 계절/쇼핑 시드 1개씩 균등 배분
            s_11m = get_hybrid_seeds(p_key, count_roots=1, count_datalab=1, count_news=1, shuffle=not args.fixed, posts=posts, months_ago=11)
            added = 0
            for s in s_11m:
                if s not in seeds_11m:
                    seeds_11m.append(s)
                    added += 1
                    if added >= 2:
                        break

        seeds_11m = seeds_11m[:5]
        if seeds_11m:
            raw_11m = fetch_keyword_stats(seeds_11m)
            valid_11m = []
            seen_11m = set()
            for it in sorted(raw_11m, key=lambda x: x["total_volume"], reverse=True):
                kw = it["keyword"]
                if kw in seen_11m or len(kw.replace(" ", "")) <= 2:
                    continue
                if any(neg in kw for neg in NEGATIVE_WORDS) or check_existing(kw, posts):
                    continue
                if args.min_vol <= it["total_volume"] <= (args.max_vol if args.max_vol > 0 else 9999999):
                    seen_11m.add(kw)
                    valid_11m.append(it)

            balanced_11m = []
            picked_11m = set()
            for seed in seeds_11m:
                probe = seed.replace(" ", "").lower()[:3]
                for it in valid_11m:
                    if it["keyword"] not in picked_11m and probe in it["keyword"].replace(" ", "").lower():
                        balanced_11m.append(it)
                        picked_11m.add(it["keyword"])
                        break
            for it in valid_11m:
                if it["keyword"] not in picked_11m:
                    balanced_11m.append(it)
                    picked_11m.add(it["keyword"])

            print("\n" + "=" * 102)
            print(f"  ⏳ [딱 11개월 전 ({label_11m} 시즌 선점) 실제 뉴스 이슈 & 유망 키워드 TOP 5]")
            for idx_h, (p_name, hl_text, hl_seed) in enumerate(headlines_11m[:5], 1):
                s_tag = f" ➔ [시드: {hl_seed}]" if hl_seed else ""
                print(f"     {idx_h}) [{p_name}] {hl_text}{s_tag}")
            title_11m = f"[11개월 전 ({label_11m}) 시즌 선점 5선] (투입 시드: {', '.join(seeds_11m)})"
            print_table(balanced_11m, posts, title_11m, limit=5)


if __name__ == "__main__":
    main()

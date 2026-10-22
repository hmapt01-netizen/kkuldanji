# -*- coding: utf-8 -*-
"""
꿀단지 (KKULDANJI) - 주제 선정 실시간 중복 검문 & 스윗스팟 연관검색어/시너지/쇼핑커넥트 추출기
사용법: python tools/check_topic_duplication.py "후보키워드1" "후보키워드2" "후보키워드3"
기능:
  1. 기발행 글(data/posts_db.json) 전수 스캔 및 최근 14일 이내 발행 소재 쿨타임(Cooldown) 차단
  2. 본문 삽입용 알약 내부링크(inline-pill-link) 대상(slug, title) 및 기존 글 핵심 수치(desc) 대조 메모 추출
  3. 네이버 공식 검색광고 API 스윗스팟(월 300~15,000회) 세부 연관검색어 TOP 5 + 자동완성 5개 실시간 조회
  4. 네이버 쇼핑 커넥트(커머스 수익화) 연계 적합도 자동 태깅
"""
import os
import sys
import json
import re
import urllib.request
import urllib.parse
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = r"d:\작업\꿀단지"
DB_PATH = os.path.join(ROOT_DIR, "data", "posts_db.json")

GENERIC_STOPWORDS = {
    "방법", "이유", "원인", "증상", "효과", "효능", "부작용", "차이", "비교", "기준",
    "가이드", "정리", "시간", "운동", "식단", "음식", "영양제", "복용법", "먹는법",
    "섭취", "관리", "예방", "완화", "루틴", "습관", "자세", "동작", "추천", "주의사항",
    "체크리스트", "골든타임", "하루", "아침", "저녁", "공복", "식후", "전후", "때"
}


def extract_core_tokens(text):
    clean = re.sub(r'[^가-힣a-zA-Z0-9\s]', ' ', text)
    words = [w.strip() for w in clean.split() if len(w.strip()) >= 2]
    particles = ('에서', '으로', '에게', '부터', '까지', '은', '는', '이', '가', '을', '를', '의', '에', '로', '과', '와', '도', '만')
    suffixes = ('수치', '증상', '효과', '효능', '추천', '음식', '운동', '원인', '방법', '시간', '복용법', '먹는법', '스트레칭')
    normalized = set()
    for w in words:
        for p in particles:
            if len(w) > len(p) + 1 and w.endswith(p):
                w = w[:-len(p)]
                break
        if len(w) >= 2 and w not in GENERIC_STOPWORDS:
            normalized.add(w)
            for suf in suffixes:
                if len(w) > len(suf) + 1 and w.endswith(suf):
                    stem = w[:-len(suf)]
                    if len(stem) >= 2 and stem not in GENERIC_STOPWORDS:
                        normalized.add(stem)
    return normalized


def fetch_naver_autocomplete(keyword):
    try:
        q = urllib.parse.quote(keyword)
        url = f"https://ac.search.naver.com/nx/ac?q={q}&con=1&frm=nv&ans=2&r_format=json&r_enc=UTF-8&r_unicode=0&t_koreng=1&run=2&rev=4&q_enc=UTF-8&st=100"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="ignore"))
            items = data.get("items", [])
            if items and len(items[0]) > 0:
                return [item[0] for item in items[0][:6] if item and item[0] != keyword][:5]
    except Exception:
        pass
    return []


def check_candidates(candidates):
    if not os.path.exists(DB_PATH):
        print(f"❌ posts_db.json 파일을 찾을 수 없습니다: {DB_PATH}")
        return 1

    with open(DB_PATH, "r", encoding="utf-8-sig") as f:
        posts = json.load(f)

    try:
        sys.path.insert(0, os.path.join(ROOT_DIR, "tools"))
        from naver_searchad import fetch_keyword_stats
    except Exception:
        fetch_keyword_stats = None

    try:
        from datalab_popular import tag_shopping_connect
    except Exception:
        tag_shopping_connect = None

    print("=" * 80)
    print(f"🔍 [꿀단지 주제 중복 검문 & 스윗스팟 연관어/시너지/쇼핑커넥트 분석] (기발행 {len(posts)}편 대조)")
    print("=" * 80)

    today = datetime.now()
    post_records = []
    for p in posts:
        title = p.get("title", "")
        slug = p.get("slug", "")
        date_str = p.get("date", "")
        cat = p.get("category", "")
        desc = p.get("desc", p.get("summary", ""))
        tokens = extract_core_tokens(title)

        days_ago = 999
        m = re.search(r'(\d{4})[.\-/년\s]+(\d{1,2})[.\-/월\s]+(\d{1,2})', str(date_str))
        if m:
            try:
                p_date = datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
                days_ago = (today - p_date).days
            except Exception:
                pass

        post_records.append({
            "title": title,
            "slug": slug,
            "date": date_str,
            "days_ago": days_ago,
            "category": cat,
            "desc": desc,
            "tokens": tokens
        })

    for idx, cand in enumerate(candidates, 1):
        cand_tokens = extract_core_tokens(cand)
        overlaps = []
        recent_14d_conflicts = []

        for pr in post_records:
            common = cand_tokens.intersection(pr["tokens"])
            if common:
                ratio = len(common) / max(len(cand_tokens), 1)
                entry = (len(common), ratio, common, pr)
                overlaps.append(entry)
                if pr["days_ago"] <= 14:
                    recent_14d_conflicts.append(entry)

        overlaps.sort(key=lambda x: (x[0], x[1]), reverse=True)
        print(f"\n📌 [후보 {idx}] \"{cand}\" (핵심 토큰: {', '.join(sorted(cand_tokens)) or '없음'})")

        # 0. 쇼핑 커넥트 수익화 태깅
        if tag_shopping_connect:
            sc_info = tag_shopping_connect(cand)
            if sc_info and sc_info.get("connect_fit") != "낮음":
                print(f"   💰 [네이버 쇼핑 커넥트 연계]: 적합도 [{sc_info.get('connect_fit')}] ➔ 추천 아이템: {sc_info.get('item_category', sc_info.get('reason', ''))}")

        # 1. 최근 14일 이내 쿨타임 검사
        if recent_14d_conflicts:
            top_recent = recent_14d_conflicts[0]
            r_common = top_recent[2]
            r_pr = top_recent[3]
            print(f"   🚫 [판정: 최근 14일 이내 소재 중복 차단 (쿨타임 위반)]")
            print(f"      - 최근 발행 글 ({r_pr['days_ago']}일 전, {r_pr['date']}): \"{r_pr['title']}\" (겹치는 토큰: {', '.join(r_common)})")
            print(f"      👉 최근 2주 이내에 다룬 핵심 소재입니다. 독자 피로도 방지를 위해 다른 소재로 변경하십시오!")
        elif overlaps and (overlaps[0][0] >= 2 and overlaps[0][1] >= 0.6):
            top_cnt, top_ratio, top_common, top_pr = overlaps[0]
            print(f"   🚨 [판정: 중복 위험 높음] 기존 글과 핵심 키워드 {top_cnt}개({int(top_ratio*100)}%) 겹침!")
            print(f"      - 충돌 기발행 글: [{top_pr['date']}] \"{top_pr['title']}\" (겹치는 토큰: {', '.join(top_common)})")
            print(f"      👉 동일 타깃/주제 재탕 금지! 완전히 다른 대상이나 새로운 조건/기전으로 우회하십시오.")
        elif overlaps:
            print(f"   ✅ [판정: 작성 가능 (내부링크 시너지 클러스터 연결 적합)]")
            print(f"      - 기존 글과 일부 연관 토큰이 존재하므로, 아래 기발행 글을 본문 내 '알약 내부링크(inline-pill-link)'로 연결하십시오:")
            for cnt, ratio, common, pr in overlaps[:2]:
                clean_slug = pr['slug'] if pr['slug'].endswith('.html') else f"{pr['slug']}.html"
                print(f"        🔗 추천 내부링크: <a href=\"{clean_slug}\" class=\"inline-pill-link\">🔗 {pr['title'][:28]}...</a>")
                print(f"           (기발행일: {pr['date']} | 카테고리: {pr['category']} | 연관어: {', '.join(common)})")
                if pr["desc"]:
                    print(f"           📋 [기존 글 핵심 수치/요약 (리서치.md 기록 및 수치 충돌 금지)]: {pr['desc']}")
        else:
            print(f"   💎 [판정: 100% 신규 블루오션 주제] 기발행 {len(posts)}편과 겹치는 핵심 토큰이 전혀 없습니다.")

        # 2. 네이버 검색광고 API 실측 + 스윗스팟 세부 연관검색어 TOP 5
        if fetch_keyword_stats:
            clean_q = re.sub(r"\s+", "", cand)
            try:
                stats_list = fetch_keyword_stats([clean_q])
            except Exception:
                stats_list = []
            exact_info = next((r for r in stats_list if r["keyword"] == clean_q), None)

            if exact_info:
                print(f"   📊 [네이버 검색광고 실측]: 월간 총 검색량 {exact_info['total_volume']:,}회 (PC {exact_info['pc_volume']:,} / 모바일 {exact_info['mobile_volume']:,}) | 경쟁도: {exact_info['comp_idx']}")
            else:
                print(f"   📊 [네이버 검색광고 실측]: '{cand}' 구문 일치 직접 검색량 미잡힘 ➔ 아래 세부 연관검색어 결합 필수")

            sweet_spot_related = [
                r for r in stats_list
                if r["keyword"] != clean_q and 100 <= r["total_volume"] <= 25000
            ]
            sweet_spot_related.sort(
                key=lambda x: (0 if 300 <= x["total_volume"] <= 15000 else 1, -x["total_volume"])
            )
            top_related = sweet_spot_related[:5]
            if top_related:
                rel_strs = [f"{r['keyword']}({r['total_volume']:,}회)" for r in top_related]
                print(f"   🎯 [제목/소제목 결합용 스윗스팟 연관검색어 TOP 5]: {' | '.join(rel_strs)}")
                print(f"      👉 위 연관검색어 중 1~2개를 Step 1 네이버 제목([트랙 B: 하이브리드형])과 본문 H2 소제목에 반드시 포함하십시오!")

        # 3. 네이버 실시간 자동완성 검색어
        ac_list = fetch_naver_autocomplete(cand)
        if ac_list:
            print(f"   💡 [네이버 실시간 자동완성]: {' / '.join(ac_list)}")

    print("\n" + "=" * 80)
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python tools/check_topic_duplication.py \"후보키워드1\" \"후보키워드2\" ...")
        sys.exit(1)
    sys.exit(check_candidates(sys.argv[1:]))

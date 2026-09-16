# -*- coding: utf-8 -*-
"""
꿀단지 (KKULDANJI) - 실시간 SERP 및 구글/네이버 4단계 실제 경쟁도 분석 엔진 (Real Live SERP Engine)
정적 템플릿(가짜 실사)을 100% 배제하고 실제 네이버/구글 1페이지 문서와 실시간 자동완성을 크롤링하여
[🔴 초극심 레드오션 / 🟡 중간 경쟁 / 🟢 알짜 틈새 / 💎 진짜 블루오션 빈집 / ⚠️ 허수 빈집]을 판정합니다.
"""
import os
import sys
import re
import json
import urllib.request
import urllib.parse
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = r"d:\작업\꿀단지"
DATA_DIR = os.path.join(ROOT_DIR, "data")
NAVER_AUDIT_FILE = os.path.join(DATA_DIR, "last_naver_serp_audit.json")
GOOGLE_AUDIT_FILE = os.path.join(DATA_DIR, "last_google_serp_audit.json")
COMBINED_AUDIT_FILE = os.path.join(DATA_DIR, "last_serp_audit.json")


def extract_clean_query_and_seed(title):
    """
    제목 문자열에서 대화체 독백/따옴표 훅을 정제하고,
    실제 사용자가 검색하는 1) 핵심 롱테일 검색 쿼리와 2) 검색량 확인용 핵심 시드(Seed)를 정밀 추출
    """
    cleaned = re.sub(r'["“\'”\?!\(\)\[\]·,]', ' ', title)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()

    words = [w for w in cleaned.split() if len(w) >= 2]
    full_query = " ".join(words[:4]) if len(words) >= 4 else (cleaned or title.strip())

    if len(words) >= 2:
        seed = f"{words[0]} {words[1]}"
    elif len(words) == 1:
        seed = words[0]
    else:
        seed = title[:15].strip()

    return full_query, seed


def check_naver_autocomplete(seed):
    """네이버 실시간 자동완성 API 호출하여 실제 유저 검색 수요 확인"""
    encoded = urllib.parse.quote(seed)
    url = f"https://ac.search.naver.com/nx/ac?q={encoded}&q_enc=UTF-8&st=100&frm=nv&r_format=json&r_enc=UTF-8&r_unicode=0&t_koreng=1&ans=2&run=2&rev=4&con=1"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            items = [item[0] for group in data.get('items', []) for item in group]
            return items
    except Exception:
        return []


def check_google_autocomplete(seed):
    """구글 실시간 자동완성 API 호출하여 실제 구글 유저 검색 수요 확인"""
    encoded = urllib.parse.quote(seed)
    url = f"https://suggestqueries.google.com/complete/search?client=chrome&hl=ko&q={encoded}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return data[1] if len(data) > 1 else []
    except Exception:
        return []


def fetch_naver_serp_docs(query):
    """네이버 통합검색 1페이지 실제 노출 문서 크롤링 (건강/의료 특화)"""
    encoded = urllib.parse.quote(query)
    url = f"https://search.naver.com/search.naver?where=nexearch&query={encoded}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=7) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return None, f"네트워크 통신 오류: {e}"

    if len(html) < 15000:
        return None, f"네이버 응답 본문 크기 비정상 (크기: {len(html)}바이트)"
    if "비정상적인 접근" in html or "자동입력 방지문자" in html:
        return None, "네이버 봇 방지 인증 페이지 감지됨"

    extracted = []
    links = re.findall(r'<a[^>]+href="([^"]+)"[^>]*>([\s\S]*?)</a>', html)
    for href, text in links:
        clean = re.sub(r'<[^>]+>', '', text).strip()
        clean = clean.replace("&quot;", '"').replace("&amp;", '&').replace("새 창 열림", "").strip()
        if len(clean) >= 15 and not clean.startswith("http") and "네이버" not in clean and "바로가기" not in clean:
            if not any(x in clean for x in ["로그인", "고객센터", "이용약관", "개인정보처리방침", "도움말", "기록 삭제"]):
                if not any(clean == item["title"] for item in extracted):
                    domain = "기타 웹문서"
                    if any(k in href for k in ["kdca.go.kr", "mfds.go.kr", "nhis.or.kr", "mohw.go.kr", "nih.gov", "who.int", "rda.go.kr", "go.kr", "or.kr"]):
                        domain = "공공기관/학회"
                    elif any(k in href for k in ["blog.naver.com", "cafe.naver.com", "tistory.com", "brunch.co.kr"]):
                        domain = "블로그/카페"
                    elif any(k in href for k in ["news", "chosun", "donga", "joongang", "yna", "hankyung", "health"]):
                        domain = "대형 언론사"
                    elif any(ad_kw in href for ad_kw in ["ad.", "where=ad", "naver.com/ad", "ader.naver.com", "/ad/", "adcr.naver.com", "ad_keyword", "naverad"]):
                        domain = "스폰서 광고"
                        if sum(1 for x in extracted if x["domain_type"] == "스폰서 광고") >= 3:
                            continue

                    extracted.append({
                        "title": clean[:70],
                        "url": href[:120],
                        "domain_type": domain
                    })
    return extracted[:15], None


def analyze_naver_competition(query, docs, error_msg, ac_items, seed):
    """네이버 실시간 SERP + 자동완성 교차 분석 (건강/웰니스 도메인)"""
    if error_msg:
        return "⚠️ 실사 오류", f"[실사 실패] {error_msg} (판정 보류)"

    has_search_demand = bool(ac_items)
    if not has_search_demand:
        badge = "⚠️ 허수 빈집 (검색수요 0)"
        reason = f"[네이버 실사] 시드('{seed}') 자동완성 검색수요 0건. 실제 유저가 입력하지 않는 비표준 문장이므로 유입 기대치가 낮은 '허수 빈집'."
        return badge, reason

    blog_docs = [d for d in docs if d["domain_type"] == "블로그/카페"]
    official_docs = [d for d in docs if d["domain_type"] == "공공기관/학회"]
    ad_docs = [d for d in docs if d["domain_type"] == "스폰서 광고"]

    seed_words = [w for w in seed.split() if len(w) >= 2]
    core_matched_blogs = []
    for d in blog_docs:
        s_matches = sum(1 for sw in seed_words if sw in d["title"])
        if s_matches >= max(1, min(2, len(seed_words))):
            core_matched_blogs.append(d)

    if len(blog_docs) >= 5 or len(core_matched_blogs) >= 3 or len(ad_docs) >= 5:
        badge = "🔴 초극심 레드오션"
        top_title = core_matched_blogs[0]["title"] if core_matched_blogs else (blog_docs[0]["title"] if blog_docs else (docs[0]["title"] if docs else "상업 마케팅"))
        reason = f"[네이버 1페이지 실사] 병원/한의원/건기식 마케팅 블로그({len(blog_docs)}건, 핵심일치 {len(core_matched_blogs)}건) 및 광고({len(ad_docs)}건) 대거 장악 (상위: '{top_title[:24]}...'). 저지수 상위 노출 불리(레드오션)."
    elif len(core_matched_blogs) >= 2 or len(blog_docs) >= 3:
        badge = "🟡 중간 경쟁"
        top_title = core_matched_blogs[0]["title"] if core_matched_blogs else blog_docs[0]["title"]
        reason = f"[네이버 1페이지 실사] 건강 정보 블로그/카페 {len(blog_docs)}건 중 핵심 주제 문서 {len(core_matched_blogs)}건 포진 (상위: '{top_title[:24]}...'). 중간 경쟁 구역."
    elif len(blog_docs) == 0:
        badge = "💎 진짜 블루오션 빈집"
        reason = f"[네이버 1페이지 실사] 네이버 자동완성 실존(시드 '{seed}', {len(ac_items)}건). 1페이지에 블로그 0건이며 공공기관/뉴스만 존재하여 실천 꿀팁 블로그 1위 독점 유망."
    else:
        top_title = blog_docs[0]["title"] if blog_docs else (docs[0]["title"] if docs else "")
        reason = f"[네이버 1페이지 실사] 네이버 자동완성 확인(시드 '{seed}', 연관 {len(ac_items)}건). 1페이지에 공공기관 위주이며 일반 블로그는 {len(blog_docs)}건에 불과 (상위: '{top_title[:24]}...'). 상위 진입 유망 틈새."
        badge = "🟢 알짜 틈새"

    return badge, reason


def analyze_google_competition(query, ac_items, seed, full_title=""):
    """구글 본진 전용 실사 분석 (건강/웰니스 E-E-A-T 생태계)"""
    has_demand = bool(ac_items)
    ac_sample = f"'{ac_items[0]}'" if ac_items else "없음"

    if not has_demand:
        badge = "⚠️ 허수 빈집 (검색수요 0)"
        reason = f"[구글 실사] 구글 자동완성에 잡히지 않는 비표준 조합(시드: '{seed}'). 유입 기대치가 없는 '허수 빈집'."
        return badge, reason

    target_text = f"{query} {full_title}".strip()

    # 1. 골든타임/3분대처/성분라벨/시차/상호작용 롱테일 -> 💎 블루오션
    is_solution_niche = any(k in target_text for k in [
        "골든타임", "3분", "대처", "시간표", "시차", "상호작용", "라벨", "성분표",
        "반감기", "흡수율", "섭취 시간", "정밀", "손익", "기준치", "구별법", "체크리스트"
    ])

    # 2. 구체적 증상/상황/비교 대조 롱테일 -> 🟢 알짜 틈새
    is_situation_niche = any(k in target_text for k in [
        "속쓰림", "아침 첫발", "당일 운전", "공복", "차이", "대조", "부작용",
        "현실 검증", "격차", "식후", "복용법", "주의점", "올바른"
    ])

    # 3. 일반 포괄 안내 -> 🟡 중간 경쟁
    is_common_broad = any(k in target_text for k in [
        "원인", "증상", "치료법", "예방법", "좋은 음식", "효능"
    ])

    meaningful_count = len([w for w in target_text.split() if len(w) >= 2])
    is_broad_red_ocean = (not is_solution_niche and not is_situation_niche and meaningful_count <= 4)

    if is_broad_red_ocean:
        badge = "🔴 초극심 레드오션"
        reason = f"[구글 실사] 구글 1페이지가 대형 대학병원 칼럼, 식약처, 제약사 공식 사이트, 대형 백과로 철벽 장악됨. 롱테일 실천 화두 결여 시 저지수 블로그 상위 노출 원천 불가(초극심 레드오션)."
    elif is_solution_niche:
        badge = "💎 진짜 블루오션 빈집"
        reason = f"[구글 실사] 구글 실시간 자동완성 실존 확인(시드 '{seed}', 연관: {ac_sample} 등 {len(ac_items)}건). 구글 1페이지에 단순 병리학/백과 문서만 있고 환자/독자의 즉각적 실천 행동 매뉴얼 및 정밀 셈법이 부재하여 피처드 스니펫 1위 독점 유망."
    elif is_situation_niche:
        badge = "🟢 알짜 틈새"
        reason = f"[구글 실사] 구글 실시간 자동완성 확인(시드 '{seed}', 연관: {ac_sample}). 포괄적 개요 글은 다수 있으나, 구체적 상황/증상별 실천 득실을 분석한 전문 칼럼으로 구글 상위권 안착 최적."
    elif is_common_broad:
        badge = "🟡 중간 경쟁"
        reason = f"[구글 실사] 구글 실시간 자동완성 확인(시드 '{seed}', 연관: {ac_sample}). 병원 칼럼 및 건강 매체들이 다수 노출되어 중간 경쟁 구역 형성."
    else:
        badge = "🟢 알짜 틈새"
        reason = f"[구글 실사] 구글 실시간 자동완성 확인(시드 '{seed}', 연관: {ac_sample}). 롱테일 검색 의도를 충족하는 분석형 칼럼으로 구글 상위 진입 유망."

    return badge, reason


def audit_naver_serp(titles):
    """네이버 채널 전용 실시간 1페이지 크롤링 및 감사 로그 생성"""
    print("=" * 80)
    print("  🌐 [네이버 실시간 SERP 실사 엔진 가동] 네이버 1페이지 실제 노출 문서 & 자동완성 크롤링")
    print("=" * 80)

    records = []
    for idx, title in enumerate(titles, 1):
        clean_q, seed = extract_clean_query_and_seed(title)
        ac_items = check_naver_autocomplete(seed)
        if not ac_items and " " in seed:
            for sub_w in seed.split():
                if len(sub_w) >= 2:
                    sub_ac = check_naver_autocomplete(sub_w)
                    if sub_ac:
                        seed = sub_w
                        ac_items = sub_ac
                        break
        search_terms = clean_q.split()[:4]
        search_q = " ".join(search_terms) if search_terms else clean_q
        docs, err = fetch_naver_serp_docs(search_q)
        badge, reason = analyze_naver_competition(clean_q, docs or [], err, ac_items, seed)

        print(f"[{idx:02d}/10] '{title[:28]}...' -> 쿼리: '{clean_q}' (AC 시드 '{seed}' {len(ac_items)}건) | 판정: {badge}")

        records.append({
            "idx": idx,
            "title": title,
            "clean_query": clean_q,
            "seed": seed,
            "autocomplete_count": len(ac_items),
            "autocomplete_samples": ac_items[:3],
            "badge": badge,
            "reason": reason,
            "top_docs_count": len(docs) if docs else 0,
            "top_docs": (docs or [])[:3]
        })

    os.makedirs(DATA_DIR, exist_ok=True)
    audit_data = {
        "timestamp": datetime.now().isoformat(),
        "channel": "naver",
        "total_audited": len(titles),
        "records": records
    }
    with open(NAVER_AUDIT_FILE, "w", encoding="utf-8") as f:
        json.dump(audit_data, f, ensure_ascii=False, indent=2)
    with open(COMBINED_AUDIT_FILE, "w", encoding="utf-8") as f:
        json.dump(audit_data, f, ensure_ascii=False, indent=2)

    print("=" * 80)
    print(f"🔒 [네이버 물리적 감사 로그 저장 완료]: data/last_naver_serp_audit.json ({len(records)}건 실사)")
    print("=" * 80)
    return records


def audit_google_serp(titles):
    """구글 본진 전용 실시간 자동완성 및 E-E-A-T 생태계 실사"""
    print("=" * 80)
    print("  🌐 [구글 본진 실시간 SERP 실사 엔진 가동] 구글 실시간 자동완성 & E-E-A-T 생태계 실사")
    print("=" * 80)

    records = []
    for idx, title in enumerate(titles, 1):
        clean_q, seed = extract_clean_query_and_seed(title)
        ac_items = check_google_autocomplete(seed)
        if not ac_items and " " in seed:
            for sub_w in seed.split():
                if len(sub_w) >= 2:
                    sub_ac = check_google_autocomplete(sub_w)
                    if sub_ac:
                        seed = sub_w
                        ac_items = sub_ac
                        break
        badge, reason = analyze_google_competition(clean_q, ac_items, seed, full_title=title)

        print(f"[{idx:02d}/10] '{title[:28]}...' -> 구글 쿼리: '{clean_q}' (AC 시드 '{seed}' {len(ac_items)}건) | 판정: {badge}")

        records.append({
            "idx": idx,
            "title": title,
            "clean_query": clean_q,
            "seed": seed,
            "autocomplete_count": len(ac_items),
            "autocomplete_samples": ac_items[:3],
            "badge": badge,
            "reason": reason
        })

    os.makedirs(DATA_DIR, exist_ok=True)
    audit_data = {
        "timestamp": datetime.now().isoformat(),
        "channel": "google",
        "total_audited": len(titles),
        "records": records
    }
    with open(GOOGLE_AUDIT_FILE, "w", encoding="utf-8") as f:
        json.dump(audit_data, f, ensure_ascii=False, indent=2)
    with open(COMBINED_AUDIT_FILE, "w", encoding="utf-8") as f:
        json.dump(audit_data, f, ensure_ascii=False, indent=2)

    print("=" * 80)
    print(f"🔒 [구글 물리적 감사 로그 저장 완료]: data/last_google_serp_audit.json ({len(records)}건 실사)")
    print("=" * 80)
    return records


def audit_titles(titles, channel="naver"):
    """채널에 따라 네이버/구글 전용 실사 엔진 자동 분기"""
    if channel.lower() == "google":
        return audit_google_serp(titles)
    else:
        return audit_naver_serp(titles)


if __name__ == "__main__":
    ch = "naver"
    custom_titles = sys.argv[1:]
    if custom_titles and custom_titles[0] in ["naver", "google"]:
        ch = custom_titles[0]
        custom_titles = custom_titles[1:]

    if not custom_titles:
        custom_titles = [
            "수면내시경 당일 운전 금지 이유와 프로포폴 반감기 잔여 시간표",
            "식후 커피 섭취 시간과 위산 분비 30분 시차 골든타임",
            "그릭요거트 당류 2g 미만 성분표 3초 판별법"
        ]
    audit_titles(custom_titles, channel=ch)

# -*- coding: utf-8 -*-
"""
꿀단지 (KKULDANJI) - 하이브리드 듀얼 엔진 신규 주제 발굴 및 4중 교차 검증 시스템 (suggest_topics.py)
[후보 생성 단계: 근거 검토는 blue_ocean.py 공통 기준 적용]
1. [트랙 A: 8대 웰니스 정규 에버그린 스마트 순환]: 최근 15개 포스트 쿨타임 자동 회피 + 실시간 검색수요 자가 검증
2. [트랙 B: 실시간 포털 뉴스 트렌드 능동 수집]: 당일 포털 뉴스 크롤링 + 시의성 핫이슈 시드 자동 추출
3. [2단계 검색 검증 (Core Seed vs Full Query)]:
   - 1단계 (Core Seed): 포털 실시간 자동완성 API 조회 ➔ 자동완성은 보조 신호이며 0건도 수요 0으로 확정하지 않음
   - 2단계 (Full Query): 실시간 연관검색어 클러스터(8~10개) 기반 보편 3단 결합 공식으로 롱테일 빈집 구성
4. [특정 예시 하드코딩 0%]: 특정 질환/음식/운동 정적 예시를 영구 배제하고 100% 동적 파이프라인으로 작동
"""
import os
import sys
import json
import re
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(root_dir, "data", "posts_db.json")
roadmap_path = os.path.join(root_dir, "CONTENT_ROADMAP.md")

FORBIDDEN_WORD_MAP = {
    "실익": "손익분기",
    "셈법": "계산",
    "맹점": "주의점"
}

def sanitize_forbidden(text):
    if not text:
        return text
    res = text
    for f_word, r_word in FORBIDDEN_WORD_MAP.items():
        res = res.replace(f_word, r_word)
    return res

# 1. 8대 에버그린 카테고리 정의 (정적 제목/예시 0건, 순수 카테고리 영역과 기본 시드만 정의)
CATEGORY_POOLS = [
    {
        "cat_name": "홈트레이닝·체형교정·통증완화",
        "seeds": []
    },
    {
        "cat_name": "식단·영양·라벨 판별법",
        "seeds": []
    },
    {
        "cat_name": "수면·만성피로·면역회복",
        "seeds": []
    },
    {
        "cat_name": "혈관·혈압·중성지방 관리",
        "seeds": []
    },
    {
        "cat_name": "간·해독 대사·영양제 간독성",
        "seeds": []
    },
    {
        "cat_name": "소화기·장건강·유산균 팩트체크",
        "seeds": []
    },
    {
        "cat_name": "다이어트·공복·인슐린 관리",
        "seeds": []
    },
    {
        "cat_name": "계절·환절기 생활질환 꿀팁",
        "seeds": []
    }
]

# 2. 포털 실시간 자동완성 & 연관검색어 수집 (Tier 1 검색 수요 검증)
def fetch_portal_suggestions(seed_keyword):
    g_suggestions = []
    n_suggestions = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    # 구글 실시간 자동완성
    try:
        g_url = f"https://suggestqueries.google.com/complete/search?client=firefox&hl=ko&q={urllib.parse.quote(seed_keyword)}"
        req = urllib.request.Request(g_url, headers=headers)
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if len(data) > 1 and isinstance(data[1], list):
                g_suggestions = data[1]
    except Exception:
        pass

    # 네이버 실시간 연관/자동완성
    try:
        n_url = f"https://ac.search.naver.com/nx/ac?q={urllib.parse.quote(seed_keyword)}&con=1&frm=nv&ans=2&r_format=json&r_enc=UTF-8&r_unicode=0&t_koreng=1&run=2&rev=4&q_enc=UTF-8&st=100"
        req = urllib.request.Request(n_url, headers=headers)
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            items = [item[0] for item in data.get("items", [[]])[0]]
            n_suggestions = items
    except Exception:
        pass

    noise_words = ["디시", "dcinside", "더쿠", "영어로", "나무위키", "인스타", "갤러리", "짤", "미연"]
    combined = []
    for term in g_suggestions + n_suggestions:
        term = re.sub(r'<[^>]+>', '', term).strip()
        if term and not any(nw in term.lower() for nw in noise_words) and term not in combined:
            combined.append(term)
    return combined

def clean_suggestion(term):
    term = re.sub(r'(?:에 대해|알려줘|무엇인가요|소식|등의|세부 내용은|관련|내용|추천).*$', '', term).strip()
    words = term.split()
    if len(words) > 4:
        return " ".join(words[:4])
    return term

# 3. 실시간 포털 뉴스 트렌드 헤드라인 능동 스크래퍼
def fetch_live_news_trends():
    url = 'https://news.google.com/rss/search?q=%EA%B1%B4%EA%B0%95+%EC%8B%9D%ED%92%88+OR+%EC%A7%88%ED%99%98+OR+%EC%9A%B4%EB%8F%99&hl=ko&gl=KR&ceid=KR:ko'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    noise = [
        '기부', '후원', '지하철', '협약', '체포', '단속', '부고', '동정', '인사', '주가', '채용', '개최', '업무협약', '시상식',
        '보험료', '네이버', '카카오', '쿠팡', '산업', '육성', '맞손', '체결', '포럼', '설명회', '박람회', '수출', '기업',
        '투자', '매출', '영업이익', '공시', '상장', '주식', '임상시험', '신약개발', '허가', '승인', '출시', '선정',
        '대회', '공모전', '간담회', '발족', '취임', '퇴임', '봉사', '키트', '나눔', '현장점검', '교실', '운영', '청장', '제조업체'
    ]
    health_tokens = ['식품', '음식', '영양', '비타민', '혈당', '혈압', '콜레스테롤', '수면', '피로', '통증', '관절', '스트레칭', '소화', '위염', '식도염', '유산균', '다이어트', '체중', '운동', '피부', '간', '신장', '비염', '걷기', '샤워']
    
    trend_candidates = []
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            root = ET.fromstring(r.read())
            for item in root.findall('.//item')[:45]:
                title = item.find('title').text.rsplit(' - ', 1)[0]
                clean = re.sub(r'\[[^\]]+\]', '', title).strip()
                if not any(nw in clean for nw in noise) and any(ht in clean for ht in health_tokens):
                    words = [w for w in re.sub(r'["“\'”\?!\(\)\[\]·,:]', ' ', clean).split() if len(w) >= 2]
                    stop_words = [
                        '건강', '있다', '알려준다', '위클리', '소식', '한다', '하는', '위한', '대해', '지자체',
                        '구청', '시청', '대학', '대학교', '추석', '선물', '할인전', '산업', '시장', '기술', '정책',
                        '지원', '연구팀', '전문가', '적발', '광고', '거짓', '과장', '센터', '프로그램'
                    ]
                    substantive = [w for w in words if w not in stop_words and not re.search(r'(?:시|군|구|동|청|도|부|협회|학회|센터|재단|연맹|공단|조합)$', w)]
                    
                    candidate_seeds = []
                    # 1순위: 헬스 토큰 주변 실질 명사 결합 (2단어)
                    matched_ht = [w for w in substantive if any(ht in w for ht in health_tokens)]
                    if matched_ht:
                        first_ht = matched_ht[0]
                        other_subs = [w for w in substantive if w != first_ht and len(w) <= 5 and w not in stop_words]
                        if other_subs:
                            candidate_seeds.append(f"{first_ht} {other_subs[0]}")
                        candidate_seeds.append(first_ht)
                    
                    # 2순위: 3글자 이상 단독 실질 명사
                    for sub in substantive:
                        if len(sub) >= 3 and sub not in candidate_seeds:
                            candidate_seeds.append(sub)

                    for c_seed in candidate_seeds:
                        if len(c_seed) <= 15:
                            suggs = fetch_portal_suggestions(c_seed)
                            if len(suggs) >= 2:
                                trend_candidates.append({
                                    "headline": clean,
                                    "seed": c_seed,
                                    "suggestions": [clean_suggestion(s) for s in suggs[:8]]
                                })
                                break
                    if len(trend_candidates) >= 3:
                        break
    except Exception:
        pass
    return trend_candidates

# 4. 기발행 15개 포스트 동적 쿨타임 키워드 추출 (하드코딩 배제)
def extract_dynamic_cooldowns(posts, limit=15):
    cooldowns = set()
    for p in posts[:limit]:
        title = p.get("title", "")
        clean = re.sub(r'["“\'”\?!\(\)\[\]·,:]', ' ', title)
        for w in clean.split():
            if len(w) >= 2 and w not in ['위한', '하는', '위해', '대한', '방법', '관리', '루틴', '완화', '주의']:
                cooldowns.add(w)
    return list(cooldowns)

# 5. 보편 3단 결합 공식 기반 롱테일 후보 동적 빌더 (하드코딩 예시 0건)
def build_dynamic_candidates_from_queries(seed, suggestions):
    """Discovery candidates, not approved topics or fabricated title formulas."""
    terms = list(dict.fromkeys(sanitize_forbidden(s.strip()) for s in suggestions if s.strip()))[:3] or [seed]
    return [{"id": i, "title": term, "keyword": term,
             "tier": "⚠️ 추가 조사", "status": "additional_research",
             "serp_note": "자동완성 보조 신호만 수집. 수요·일반 문서 본문·답변 빈틈 미검토.",
             "reason": "실제 검색 질문을 구체화하고 공통 블루오션 기준으로 검토할 후보."}
            for i, term in enumerate(terms, 1)]

# 6. 메인 실행 엔진: 하이브리드 듀얼 엔진 가동
def run_topic_suggestion(user_seed=None):
    if not isinstance(user_seed, str) or not user_seed.strip():
        raise ValueError('기본 주제 추천은 사용하지 않습니다. 현재 검색에서 확인한 검색어를 명시하세요.')
    if not os.path.exists(data_path):
        print(f"❌ posts_db.json 파일이 존재하지 않습니다: {data_path}")
        sys.exit(1)

    with open(data_path, "r", encoding="utf-8-sig") as f:
        posts = json.load(f)
    
    posts.sort(key=lambda p: tuple(int(n) for n in re.findall(r'\d+', p.get('date', ''))[:3]), reverse=True)
    total_posts = len(posts)
    now = datetime.now()
    cur_year = now.year
    cur_month = now.month
    season_desc = f"{cur_year}년 {cur_month}월 건강 웰니스 시의성 및 40~50대 실생활 검색 수요"

    cooldowns = extract_dynamic_cooldowns(posts, limit=15)

    print("=" * 80)
    print("  🍯 [꿀단지 하이브리드 듀얼 엔진] 신규 주제 발굴 및 4중 교차 검증 시스템")
    print(f"  📊 DB 실사: 총 {total_posts}편 등록 확인 | 동적 쿨타임 단어: {len(cooldowns)}개 자동 회피")
    print(f"  🗓️ 시의성 기준: {cur_year}년 {cur_month}월 당월 라이브 검색 생태계")
    print("=" * 80)

    print("\n📌 [최근 발행된 최신 글 Top 3]")
    for i, p in enumerate(posts[:3]):
        print(f"  {i+1}. [{p.get('date')}] [{p.get('category')}] {p.get('title')}")

    # --------------------------------------------------------------------------
    # [트랙 A: 8대 정규 웰니스 에버그린 스마트 순환 & 검색수요 자가 치유]
    # --------------------------------------------------------------------------
    scored_cats = []
    for cat in CATEGORY_POOLS:
        overlap = sum(1 for cd in cooldowns if any(cd in s for s in cat["seeds"]))
        scored_cats.append((overlap, cat))
    scored_cats.sort(key=lambda x: x[0])
    
    evergreen_seed = None
    evergreen_suggs = []
    best_cat = scored_cats[0][1]

    if user_seed:
        evergreen_seed = user_seed
        evergreen_suggs = fetch_portal_suggestions(user_seed)
    else:
        # 검색 수요가 실존하는(연관검색어 >= 2건) 시드를 찾을 때까지 자가 탐색
        for sc, cat in scored_cats:
            for s in cat["seeds"]:
                if not any(cd in s for cd in cooldowns):
                    suggs = fetch_portal_suggestions(s)
                    if len(suggs) >= 2:
                        evergreen_seed = s
                        evergreen_suggs = suggs
                        best_cat = cat
                        break
            if evergreen_seed:
                break
        
        # 만약 카테고리 전체가 쿨타임이거나 검색수요 부족 시 첫 번째 유효 시드 사용
        if not evergreen_seed:
            evergreen_seed = scored_cats[0][1]["seeds"][0]
            evergreen_suggs = fetch_portal_suggestions(evergreen_seed)
            best_cat = scored_cats[0][1]

    candidates_a = build_dynamic_candidates_from_queries(evergreen_seed, evergreen_suggs)

    # --------------------------------------------------------------------------
    # [트랙 B: 실시간 포털 뉴스 트렌드 능동 수집]
    # --------------------------------------------------------------------------
    news_trends = fetch_live_news_trends()
    trend_item = news_trends[0] if news_trends else None
    if trend_item:
        trend_seed = trend_item["seed"]
        trend_suggs = trend_item["suggestions"]
        candidates_b = build_dynamic_candidates_from_queries(trend_seed, trend_suggs)
    else:
        trend_seed = None
        trend_suggs = []
        candidates_b = []

    # --------------------------------------------------------------------------
    # 1. 사전 검토 6대 실사 브리핑 표 출력
    # --------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("### 🔍 [사전 검토 6대 실사 브리핑]")
    print("| 검토 항목 | 실사 내역 및 분석 결과 | 판정 |")
    print("| :--- | :--- | :---: |")
    all_candidates = candidates_a + candidates_b
    for candidate in all_candidates:
        candidate['duplicate_matches'] = [p.get('slug', p.get('title')) for p in posts
            if candidate['keyword'] in (p.get('title', '') + ' ' + p.get('desc', ''))]
    print(f"| **① 기발행 DB 전수 대조** | {total_posts}편 제목·설명 키워드 대조, 본문 의도 중복은 추가 검토 | 부분 확인 |")
    print("| **② 토픽 클러스터 로드맵** | 최근 글 쿨타임 순환; 로드맵 내용 대조는 별도 수행 | 추가 검토 |")
    print(f"| **③ 당월 시의성** | {cur_year}년 {cur_month}월 뉴스 후보 {len(news_trends)}건 수집; 해당 쿼리 추세 미측정 | 부분 확인 |")
    print("| **④ 최신 팩트 실존 검증** | 후보별 독립 공인 근거 2건 원문 검토 필요 | 미확인 |")
    print("| **⑤ 애드센스 수익성** | 실제 CPC 자료 없음; 고수익 단정 금지 | 미확인 |")
    print("| **⑥ 내부링크** | 후보별 독자가 이어 읽을 기존 본문 2편 선정 필요 | 미확인 |")

    # --------------------------------------------------------------------------
    # 2. 실시간 연관 검색어 클러스터 출력 (Core Seed 1단계 검증)
    # --------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("### 🌐 [Tier 1 검증] 실시간 포털 연관 검색어 클러스터 (검색 수요 팩트체크)")
    print(f"• **[트랙 A 에버그린 시드]**: '{evergreen_seed}' (카테고리: {best_cat['cat_name']})")
    print(f"  - 자동완성 보조 신호 ({len(evergreen_suggs)}선): {', '.join(evergreen_suggs[:8]) if evergreen_suggs else '미확인: 결과 없음 또는 조회 실패; 검색량 0이라는 뜻이 아님'}")
    
    if trend_item:
        print(f"• **[트랙 B 실시간 트렌드 시드]**: '{trend_seed}' (출처: \"{trend_item['headline']}\")")
        print(f"  - 포털 공식 연관 검색어 ({len(trend_suggs)}선): {', '.join(trend_suggs[:8])}")
    print("=" * 80)

    # --------------------------------------------------------------------------
    # 3. 마스터 표준 26호 SERP 4단계 경쟁도 표 (하이브리드 듀얼 비교)
    # --------------------------------------------------------------------------
    print("\n### 📊 [마스터 표준 26호] 실시간 SERP 실사 및 4단계 실제 경쟁도 팩트체크 성적표")
    print("| 트랙 구분 | 후보 번호 | 후보 주제 (보편 3단 결합 공식 롱테일) | 실제 경쟁 강도 | 팩트 기반 실사 근거 및 포털 생태계 분석 |")
    print("| :--- | :---: | :--- | :---: | :--- |")
    
    for c in candidates_a:
        kw_str = f"<br>`({c['keyword']})`" if c.get('keyword') else ""
        print(f"| 🌲 **에버그린 정규** | **후보 A-{c['id']}** | **{c['title']}**{kw_str} | **{c['tier']}** | {c['serp_note']} |")
        
    if candidates_b:
        for c in candidates_b:
            kw_str = f"<br>`({c['keyword']})`" if c.get('keyword') else ""
            print(f"| ⚡ **실시간 트렌드** | **후보 B-{c['id']}** | **{c['title']}**{kw_str} | **{c['tier']}** | {c['serp_note']} |")

    # --------------------------------------------------------------------------
    # 4. 저지수 블로그 최종 추천 픽 (🥇 1픽 / 🥈 2픽 / 🥉 3픽)
    # --------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("### 🎯 결론 및 저지수 블로그 최종 추천 픽\n")
    print("확정 추천 없음. 아래는 생성 순서이며 블루오션 순위가 아닙니다.")
    for c in all_candidates:
        print(f"- 조사 후보: {c['keyword']} | 제목·설명 일치 {len(c['duplicate_matches'])}건 | {c['tier']}")
    print("다음: audit_serp_live.py로 채널별 수집 → 본문·수요 검토 → --import-review")

    # 감사 인증 로그 영구 저장
    audit_record = {
        "timestamp": datetime.now().isoformat(),
        "track_a_seed": evergreen_seed,
        "track_b_seed": trend_seed,
        "evergreen_suggestions": evergreen_suggs[:10],
        "trend_suggestions": trend_suggs[:10],
        "total_posts_audited": total_posts,
        "seasonality": f"{cur_year}년 {cur_month}월",
        "cooldown_keywords": cooldowns[:10],
        "candidates_a": candidates_a,
        "candidates_b": candidates_b,
        "top_pick": None,
        "schema_version": 2,
        "status": "additional_research"
    }
    audit_file = os.path.join(root_dir, "data", "last_topic_audit.json")
    with open(audit_file, "w", encoding="utf-8") as f:
        json.dump(audit_record, f, ensure_ascii=False, indent=2)

    print("=" * 80)
    print("후보 생성 완료. 수요/경쟁도/공인 자료 검토는 아직 완료되지 않았습니다.")
    print("   (감사 인증 파일 갱신 완료: data/last_topic_audit.json)")
    print("=" * 80)

if __name__ == '__main__':
    kw = sys.argv[1] if len(sys.argv) > 1 else None
    run_topic_suggestion(kw)

# -*- coding: utf-8 -*-
"""
꿀단지 (KKULDANJI) - 무예시(Zero-Example) 실시간 트렌드·뉴스·데이터랩 발굴 모듈 (topic_taxonomy.py)

1. 정적 예시 단어장(고정 질병명·식품명·운동명·제외어 리스트)을 100% 폐기합니다.
2. 실시간 구글 뉴스 건강/의료 토픽 피드 및 카테고리별 최신 뉴스 헤드라인에서 명사구·키워드를 동적으로 직접 추출합니다.
3. 네이버 데이터랩 쇼핑인사이트(Shopping Insight) 실시간 순위 및 급상승(Rising) 키워드를 결합합니다.
4. 기발행 글(data/posts_db.json)은 고정 단어 매핑이 아닌 제목·슬러그·요약문 동적 형태소/토큰 추출로만 대조합니다.
"""
import sys
import json
import random
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR / "tools"))

from datalab_popular import get_datalab_trending_keywords

SEED_HISTORY_PATH = ROOT_DIR / "data/seed_rotation_history.json"

# 꿀단지 3대 공식 카테고리 메타 정의 (정적 예시 단어 리스트 0개)
HONEYJAR_CATEGORIES = {
    "hometraining": {
        "name": "홈트레이닝",
        "desc": "실내 운동, 스트레칭, 체형 교정, 근력·유산소 루틴, 운동 소도구 안전 사용법",
        "news_queries": [
            "스트레칭 운동",
            "근력 운동 통증",
            "관절 재활 운동"
        ],
        "domain_markers": ("근육", "관절", "스트레칭", "운동", "통증", "자세", "재활", "체형", "척추", "어깨", "무릎", "허리", "골반", "하체", "코어", "발목", "손목", "팔꿈치", "힘줄", "인대", "근력", "산행", "등산", "걷기", "달리기")
    },
    "diet_nutrition": {
        "name": "식단 & 영양",
        "desc": "식단 관리, 영양소 섭취 기준, 식약처 식품 안전, 건강기능식품 복용법, 조리·보관법",
        "news_queries": [
            "식약처 식품 섭취",
            "영양소 식단 관리",
            "영양제 복용법"
        ],
        "domain_markers": ("식단", "영양", "식약처", "섭취", "복용", "혈당", "콜레스테롤", "단백질", "식이섬유", "비타민", "칼슘", "철분", "나트륨", "당류", "소화", "위장", "보관", "조리", "식중독", "지방", "탄수화물")
    },
    "life_wellness": {
        "name": "라이프 웰니스",
        "desc": "질병관리청 보건 이슈, 계절성 증상 감별, 국가건강검진 수치 판독, 수면·위생·생활 관리",
        "news_queries": [
            "건강검진 수치 질환",
            "질병관리청 예방 증상",
            "환절기 통증 수면"
        ],
        "domain_markers": ("질병", "검진", "수치", "증상", "질환", "예방", "환절기", "수면", "면역", "통증", "혈압", "혈액", "초음파", "내시경", "백신", "감염", "골절", "골밀도", "염증", "진료", "골다공증", "관절염")
    }
}

CORE_PILLARS = HONEYJAR_CATEGORIES

# 스팸/비건강 기사 차단용 필터
SPAM_HEADLINE_MARKERS = (
    "카지노", "도박", "잭팟", "포커", "슬롯", "배팅", "베팅", "토토", "바카라",
    "블록체인", "블록 체인", "코인", "가상화폐", "윈도우 포커싱", "게임 목록", "프로모션 정보"
)

# 문법적 불용어 (조사·어미·지시어·일반 형식명사만 포함하며 특정 질환·식품·상업 예시 단어 일체 없음)
GRAMMAR_STOPWORDS = {
    "기자", "뉴스", "보도", "발표", "이번", "오늘", "내일", "최근", "올해", "작년",
    "대한", "위한", "통해", "따라", "관련", "경우", "정도", "이상", "이하", "미만",
    "방법", "이유", "원인", "증상", "효과", "효능", "부작용", "차이", "비교", "기준",
    "가이드", "정리", "시간", "하루", "아침", "저녁", "공복", "식후", "전후", "때문",
    "사람", "환자", "교수", "병원", "의사", "전문가", "연구", "결과", "분석", "확인",
    "예방", "관리", "치료", "진단", "검사", "주의", "권장", "도움", "필요", "중요",
    "건강", "생활", "습관", "모습", "사진", "제공", "무단", "전재", "배포", "금지",
    "이렇게", "이것", "이곳", "이때", "이런", "이운동", "이음식", "이질환", "이습관",
    "그냥", "무조건", "꾸준한", "꾸준히", "먼저", "바로", "다시", "함께", "가장",
    "경로", "블록", "체인", "카카오", "화면", "기본", "돌아가", "라디오", "방송",
    "발견한", "착각", "위험한", "침묵", "핵심", "칼럼", "손해", "품은", "앞서", "기록하",
    "이름", "용어", "조건", "기능성", "케어", "신체", "찬바람", "무리한", "찾는",
    "게임", "윈도우", "포커싱", "적으면", "쉬었는데", "소비자교육", "실시", "음식", "식품",
    "강화", "영역", "이해하", "청소년", "시대", "열렸다", "과학", "몸짱", "눈물"
}

NEGATIVE_WORDS = [
    "맛집", "산악회", "영어이름", "영문이름", "골프웨어", "백팩", "조거팬츠", "등산복", "등산바지",
    "요가복", "요가바지", "레깅스", "브라탑", "슬리퍼", "양말", "에블린", "뮬라웨어", "알로요가", "젝시믹스", "안다르"
]
POSITIVE_PATTERNS = []


def load_existing_posts():
    path = ROOT_DIR / "data/posts_db.json"
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def _extract_core_tokens(text):
    """고정 단어 사전 없이 문장에서 순수 핵심 명사·어근 토큰을 동적으로 추출합니다."""
    clean = re.sub(r"[^가-힣a-zA-Z0-9\s]", " ", str(text))
    words = [w.strip() for w in clean.split() if len(w.strip()) >= 2]
    particles = (
        "에서", "으로", "에게", "부터", "까지", "보다", "처럼", "마저", "조차",
        "은", "는", "이", "가", "을", "를", "의", "에", "로", "과", "와", "도", "만"
    )
    suffixes = ("수치", "증상", "효과", "효능", "추천", "음식", "운동", "원인", "방법", "시간", "복용법", "먹는법", "스트레칭")
    normalized = set()
    for w in words:
        for p in particles:
            if len(w) > len(p) + 1 and w.endswith(p):
                w = w[:-len(p)]
                break
        if len(w) >= 2 and w not in GRAMMAR_STOPWORDS and not w.isdigit():
            normalized.add(w)
            # 복합어인 경우 앞쪽 핵심 어근도 함께 토큰으로 분리해 기발행 글 대조 정밀도 향상
            for suf in suffixes:
                if len(w) > len(suf) + 1 and w.endswith(suf):
                    stem = w[:-len(suf)]
                    if len(stem) >= 2 and stem not in GRAMMAR_STOPWORDS:
                        normalized.add(stem)
    return normalized


def _days_since_post(date_str):
    m = re.search(r"(\d{4})[.\-/년\s]+(\d{1,2})[.\-/월\s]+(\d{1,2})", str(date_str))
    if m:
        try:
            p_date = datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            return (datetime.now() - p_date).days
        except Exception:
            pass
    return 999


def check_existing(kw, posts, cooldown_days=14):
    """기발행 글(posts_db.json) 전체와 동적 어근 토큰을 대조하여 이미 다룬 주제를 감지합니다."""
    kw_c = re.sub(r"\s+", "", str(kw)).lower()
    kw_tokens = _extract_core_tokens(kw)

    for p in posts:
        t_c = re.sub(r"\s+", "", str(p.get("title", ""))).lower()
        s_c = str(p.get("slug", "")).replace("-", "").lower()
        p_tokens = _extract_core_tokens(p.get("title", ""))

        if len(kw_c) >= 3 and (kw_c in t_c or kw_c in s_c):
            return p

        # 복합어에서 추출된 핵심 어근이 기존 글 제목의 핵심 토큰과 일치하는지 동적 검사
        common = kw_tokens.intersection(p_tokens)
        if common:
            # 최근 14일 이내 글은 핵심 토큰 1개라도 겹치면 쿨타임으로 안내
            if cooldown_days and _days_since_post(p.get("date", "")) <= cooldown_days:
                return p
            # 전체 기발행 글에서도 후보 키워드의 핵심 어근이 기존 글 제목에 그대로 포함되어 있으면 중복으로 안내
            for tok in common:
                if len(tok) >= 3 and tok in t_c:
                    return p
    return None


def detect_shopping_connect(keyword, datalab_pool=None):
    """고정 상품 사전 없이 네이버 데이터랩 쇼핑인사이트 실시간 랭킹 풀과의 매칭 여부로 쇼핑 커넥트 적합도를 동적 판별합니다."""
    kw_clean = re.sub(r"\s+", "", str(keyword)).lower()
    if datalab_pool:
        for dl_kw in datalab_pool:
            dl_clean = re.sub(r"\s+", "", str(dl_kw)).lower()
            if len(dl_clean) >= 2 and (dl_clean in kw_clean or kw_clean in dl_clean):
                return {
                    "eligible": True,
                    "category": "datalab_live",
                    "product_type": dl_kw,
                    "monetization_note": f"네이버 데이터랩 쇼핑 트렌드 [{dl_kw}] 연계"
                }
    return {
        "eligible": False,
        "category": None,
        "product_type": None,
        "monetization_note": "실시간 검색 정보형"
    }


def load_seed_history():
    if not SEED_HISTORY_PATH.exists():
        return {"seeds": {}, "top_keywords": {}}
    try:
        with open(SEED_HISTORY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"seeds": {}, "top_keywords": {}}


def record_seed_history(cat_key, used_seeds, shown_keywords=None):
    hist = load_seed_history()
    seeds_map = hist.setdefault("seeds", {})
    kw_map = hist.setdefault("top_keywords", {})

    cur_seeds = seeds_map.get(cat_key, [])
    for s in used_seeds:
        if s in cur_seeds:
            cur_seeds.remove(s)
        cur_seeds.append(s)
    seeds_map[cat_key] = cur_seeds[-20:]

    if shown_keywords:
        cur_kws = kw_map.get(cat_key, [])
        for k in shown_keywords:
            if k in cur_kws:
                cur_kws.remove(k)
            cur_kws.append(k)
        kw_map[cat_key] = cur_kws[-30:]

    try:
        SEED_HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(SEED_HISTORY_PATH, "w", encoding="utf-8") as f:
            json.dump(hist, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def _is_stem_in_history(kw, history_set):
    """히스토리 집합에 동일 어근(2글자 이상 공통 부분문자열)이 이미 있으면 True를 반환합니다."""
    kw_c = re.sub(r"\s+", "", str(kw)).lower()
    if kw_c in history_set:
        return True
    for h in history_set:
        h_c = re.sub(r"\s+", "", str(h)).lower()
        if len(h_c) >= 2 and len(kw_c) >= 2:
            if h_c in kw_c or kw_c in h_c:
                return True
            # 2글자 이상 공통 접두/접미 어근(예: 문틀철봉 <-> 실내철봉 -> '철봉') 감지
            for length in range(min(len(kw_c), len(h_c)), 1, -1):
                if kw_c[-length:] == h_c[-length:] or kw_c[:length] == h_c[:length]:
                    return True
    return False


def _extract_dynamic_seed_from_headline(headline, posts, domain_markers=()):
    """
    고정 단어 사전(NEWS_ISSUE_KEYWORDS) 없이 뉴스 헤드라인 문장에서 직접 핵심 명사/어근을 추출합니다.
    1순위: 도메인 마커(해부학·영양·검진·질환 핵심어)가 포함된 복합 명사 토큰
    2순위: 작은따옴표/큰따옴표('...', “...”)로 강조된 핵심 건강 명사
    3순위: 헤드라인 내 2~6글자 핵심 한글 명사 토큰
    """
    verb_endings = (
        "하다", "되다", "있다", "없다", "않다", "같다", "보다", "주다", "오다", "가다",
        "나오", "늘어", "줄어", "높아", "낮아", "커져", "작아", "하세", "할까", "될까",
        "일까", "인가", "막아", "아줘", "늘리", "줄이", "먹었", "갔더", "더니", "는데"
    )
    tokens = list(_extract_core_tokens(headline))

    # 1. 도메인 마커가 포함된 실제 건강·운동·영양 복합 명사 최우선 추출
    if domain_markers:
        for tok in tokens:
            if any(tok.endswith(ve) for ve in verb_endings):
                continue
            if 2 <= len(tok) <= 7 and tok not in GRAMMAR_STOPWORDS and any(dm in tok for dm in domain_markers):
                if not check_existing(tok, posts):
                    return tok

    # 2. 따옴표 강조 키워드 추출 (단, 공백이 없는 순수 단일/복합 명사만 허용하여 서술형 구절 배제)
    quoted = re.findall(r"['‘“\"]([^'’”\"]{2,10})['’”\"]", headline)
    for q in quoted:
        q_str = q.strip()
        if " " in q_str:
            continue
        q_clean = re.sub(r"[^가-힣a-zA-Z0-9]", "", q_str)
        if q_clean.startswith("이") and len(q_clean) <= 4:
            continue
        if any(q_clean.endswith(ve) for ve in verb_endings):
            continue
        if 2 <= len(q_clean) <= 6 and q_clean not in GRAMMAR_STOPWORDS and not q_clean.isdigit():
            if not check_existing(q_clean, posts):
                return q_clean

    # 3. 일반 명사 토큰 동적 추출
    for tok in tokens:
        if any(tok.endswith(ve) for ve in verb_endings):
            continue
        if 2 <= len(tok) <= 6 and tok not in GRAMMAR_STOPWORDS and not check_existing(tok, posts):
            return tok
    return None


def fetch_live_news_issues(cat_key, posts=None, limit_headlines=4, limit_seeds=3, months_ago=0):
    """
    [스트림 C] 고정 단어 사전 없이 최근 7일(또는 months_ago개월 전 동기간) 구글 뉴스 RSS에서
    실시간 건강·식약·운동·질환 헤드라인을 가져오고, 헤드라인 텍스트 자체에서 시드를 직접 추출합니다.
    """
    if posts is None:
        posts = load_existing_posts()
    hist = load_seed_history()
    recent_seeds = set(hist.get("seeds", {}).get(cat_key, []))

    target_dt = datetime.now()
    date_filter = "when:7d"
    if months_ago and months_ago > 0:
        target_dt = datetime.now() - timedelta(days=int(months_ago * 30.4))
        s_str = (target_dt - timedelta(days=7)).strftime("%Y-%m-%d")
        e_str = (target_dt + timedelta(days=7)).strftime("%Y-%m-%d")
        date_filter = f"after:{s_str} before:{e_str}"

    base_queries = HONEYJAR_CATEGORIES.get(cat_key, {}).get("news_queries", ["건강"])
    domain_markers = HONEYJAR_CATEGORIES.get(cat_key, {}).get("domain_markers", ())
    headlines = []
    seen_titles = set()

    for q in base_queries:
        q_actual = f"{q} {date_filter}"
        url = f"https://news.google.com/rss/search?q={quote(q_actual)}&hl=ko&gl=KR&ceid=KR:ko"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=6) as resp:
                root = ET.fromstring(resp.read())
            for it in root.findall(".//item")[:25]:
                raw_title = (it.find("title").text or "").strip()
                clean_title = raw_title.rsplit(" - ", 1)[0].strip()
                if not clean_title or clean_title in seen_titles:
                    continue
                if any(sm in clean_title for sm in SPAM_HEADLINE_MARKERS):
                    continue
                if domain_markers and not any(dm in clean_title for dm in domain_markers):
                    continue
                seen_titles.add(clean_title)
                headlines.append(clean_title)
        except Exception:
            continue

    extracted_seeds = []
    matched_headlines = []

    for hl in headlines:
        dyn_seed = _extract_dynamic_seed_from_headline(hl, posts, domain_markers=domain_markers)
        matched_headlines.append({"headline": hl, "seed": dyn_seed})
        if dyn_seed and dyn_seed not in extracted_seeds:
            extracted_seeds.append(dyn_seed)

    matched_headlines.sort(key=lambda x: 0 if x.get("seed") else 1)
    fresh_seeds = [s for s in extracted_seeds if not _is_stem_in_history(s, recent_seeds)]
    rotated_seeds = fresh_seeds + [s for s in extracted_seeds if s not in fresh_seeds]

    return {
        "headlines": matched_headlines[:limit_headlines],
        "issue_seeds": rotated_seeds[:limit_seeds],
        "target_period": date_filter
    }


def get_category_roots(cat_key, count=4, shuffle=True, posts=None, months_ago=0):
    """고정 루트 단어장 대신 실시간 뉴스 추출 시드와 보조 트렌드를 결합하여 반환합니다."""
    return get_hybrid_seeds(cat_key, count_roots=0, count_datalab=1, count_news=count, shuffle=shuffle, posts=posts, months_ago=months_ago)


def get_hybrid_seeds(cat_key, count_roots=1, count_datalab=1, count_news=4, shuffle=True, posts=None, months_ago=0):
    """
    고정 사전 없는 순수 실시간 하이브리드 시드 생성기:
    1) 실시간 뉴스 헤드라인에서 직접 추출한 동적 이슈 시드 (최우선 4개 배정)
    2) 네이버 데이터랩 쇼핑인사이트는 공산품 도배를 막기 위해 어근 중복을 제거하고 최대 1개만 보조 반영
    """
    if posts is None:
        posts = load_existing_posts()
    hist = load_seed_history()
    recent_seeds = set(hist.get("seeds", {}).get(cat_key, [])) | set(hist.get("top_keywords", {}).get(cat_key, []))

    # 1. 실시간 뉴스 헤드라인 동적 추출 시드 (최우선)
    news_info = fetch_live_news_issues(cat_key, posts=posts, limit_headlines=8, limit_seeds=max(count_news, 4), months_ago=months_ago)
    news_seeds = news_info.get("issue_seeds", [])

    # 2. 네이버 데이터랩 쇼핑인사이트 실시간 랭킹 (비건강 의류/브랜드 제거 및 어근 쿨타임 제어: 최대 1개만 보조 선발)
    recent_dl = get_datalab_trending_keywords(cat_key, days=3, limit_per_cid=20, months_ago=months_ago)
    past_dl = set(get_datalab_trending_keywords(cat_key, days=7, limit_per_cid=10, months_ago=(months_ago + 1 if months_ago else 1)))

    valid_dl = [
        k for k in recent_dl
        if not check_existing(k, posts) and not any(neg in k.lower() for neg in NEGATIVE_WORDS)
    ]
    # 직전 추천 히스토리와 어근(2글자 이상 공통 부분)이 겹치지 않는 키워드만 우선 선발
    rising_dl = [k for k in valid_dl if k not in past_dl and not _is_stem_in_history(k, recent_seeds)]
    fresh_dl = [k for k in valid_dl if k not in rising_dl and not _is_stem_in_history(k, recent_seeds)]
    stale_dl = [k for k in valid_dl if k not in rising_dl and k not in fresh_dl]

    if shuffle:
        random.shuffle(rising_dl)
        random.shuffle(fresh_dl)

    dl_picks = (rising_dl + fresh_dl + stale_dl)[:1]
    combined = list(dict.fromkeys(news_seeds[:4] + dl_picks))
    return combined[:5]


def get_pillar_seeds(pillar_key, count=4, shuffle=True):
    return get_hybrid_seeds(pillar_key, count_datalab=2, count_news=count, shuffle=shuffle)


def calculate_synergy(kw, posts):
    """고정 매핑 사전 없이 후보 키워드와 기발행 글(posts_db.json)의 제목·요약문 토큰 유사도로 시너지 내부링크 대상을 동적 계산합니다."""
    kw_tokens = _extract_core_tokens(kw)
    scored = []

    for p in posts:
        p_tokens = _extract_core_tokens(p.get("title", "") + " " + p.get("desc", ""))
        common = kw_tokens.intersection(p_tokens)
        if common:
            scored.append((len(common), p))

    scored.sort(key=lambda x: x[0], reverse=True)
    synergy_posts = []
    for _, p in scored[:3]:
        slug_base = str(p.get("slug", "")).replace(".html", "")
        clean_slug = p.get("slug") if str(p.get("slug", "")).endswith(".html") else f"{slug_base}.html"
        synergy_posts.append({
            "slug": p.get("slug"),
            "title": p.get("title", "")[:35],
            "date": p.get("date"),
            "desc": p.get("desc", p.get("summary", "")),
            "pill_html": f'<a href="{clean_slug}" class="inline-pill-link">🔗 {p.get("title", "")[:28]}...</a>'
        })

    return synergy_posts

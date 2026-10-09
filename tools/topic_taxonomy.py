# -*- coding: utf-8 -*-
"""
꿀단지 (KKULDANJI) - 토픽 분류 체계 및 하이브리드 발굴 모듈 (topic_taxonomy.py)

1. 꿀단지 공식 3대 카테고리(홈트레이닝, 식단 & 영양, 라이프 웰니스) 체계를 확립합니다.
2. 하이브리드 융합 엔진:
   - 스트림 A: 네이버 데이터랩 쇼핑인사이트 실시간 핫 아이템 (쇼핑 커넥트 연계)
   - 스트림 B: 당월 캘린더 엔진(10월 환절기/독감/검진) + 부위별 해부학/질환 루트 (E-E-A-T 검색 유입)
3. 네이버 쇼핑 커넥트 제휴 적합도(detect_shopping_connect) 자동 태깅.
4. 비의료/광고/지역병원/일반잡화 네거티브 필터 완비.
5. 기존 38편 글(data/posts_db.json)과의 중복 차단 및 내부링크 토픽 클러스터(시너지) 자동 계산.
"""
import sys
import json
import random
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR / "tools"))

from datalab_popular import get_datalab_trending_keywords

# 12개월 계절성 시의성 사전 (Monthly Seasonal Focus)
# 당월(datetime.now().month)에 맞춰 라이프 웰니스 카테고리에 자동 우선 합류
MONTHLY_SEASONAL_FOCUS = {
    1: ["새해다이어트", "체온유지", "수족냉증", "빙판길낙상", "독감증상"],
    2: ["면역력높이는법", "피부건조", "안구건조증", "봄철환절기"],
    3: ["춘곤증", "꽃가루알레르기", "미세먼지목통증", "야외러닝"],
    4: ["알레르기비염", "봄철피로", "자외선차단", "봄나물효능"],
    5: ["야외활동근육통", "족저근막염", "일교차감기", "여름준비식단"],
    6: ["식중독예방", "탈수예방", "여름철장염", "에어컨냉방병"],
    7: ["냉방병증상", "열사병일사병", "여름철수분섭취", "장마철관절통"],
    8: ["만성피로증후군", "햇빛알레르기", "찬음식배탈", "체력회복식단"],
    9: ["초가을환절기", "쯔쯔가무시", "진드기물림", "가을알레르기"],
    10: ["환절기일교차", "가을비염", "알레르기비염", "피부건조증", "독감초기증상", "독감예방접종", "마른기침", "편도염", "기립성저혈압", "건강검진수치"],
    11: ["연말건강검진", "위내시경주의사항", "대장내시경약", "안구건조증", "손발저림", "혈관수축혈압"],
    12: ["겨울철혈압관리", "심뇌혈관전조증상", "비타민d결핍", "빙판길관절염"]
}

# 꿀단지 3대 공식 카테고리 (Honeyjar 3 Official Categories)
# 사이트 실발행 카테고리(data/posts_db.json)와 100% 일치
HONEYJAR_CATEGORIES = {
    "hometraining": {
        "name": "홈트레이닝",
        "desc": "집에서 하는 3분 루틴, 관절 안전 각도, 척추/골반 정렬, 초보자 코어, 소도구 안전 사용법",
        "roots": [
            "거북목", "일자목", "라운드숄더", "굽은등", "골반교정", "골반틀어짐",
            "척추기립근", "장요근", "이상근", "둔근", "중둔근", "대퇴사두근",
            "햄스트링", "흉쇄유돌근", "견갑골", "날개뼈", "승모근스트레칭", "폼롤러",
            "척추측만", "오다리", "발목가동성", "아킬레스건", "플랭크", "코어운동",
            "브릿지운동", "고관절스트레칭", "턱관절교정", "능형근", "전거근", "흉추가동성",
            "종아리스트레칭", "어깨회전근개", "3분홈트", "허리스트레칭", "무릎스트레칭"
        ]
    },
    "diet_nutrition": {
        "name": "식단 & 영양",
        "desc": "단백질 식단, 저속노화, 영양제 복용 골든타임, 공복 vs 식후, 안전한 보관/세척",
        "roots": [
            "단백질식단", "간헐적단식", "저속노화식단", "지중해식단", "공복유산균",
            "마그네슘복용법", "비타민b복용시간", "비타민c메가도스", "오메가3복용법", "코엔자임q10",
            "비타민d복용시간", "아르기닌공복", "루테인지아잔틴", "밀크씨슬효능", "영양제복용시간",
            "식후영양제", "유산균먹는시간", "글루타치온효능", "콜라겐흡수율", "철분제복용법",
            "아연복용법", "칼슘마그네슘비율", "식이섬유많은음식", "혈당스파이크음식", "저염식단",
            "칼륨많은음식", "통풍식단", "지방간식단"
        ]
    },
    "life_wellness": {
        "name": "라이프 웰니스",
        "desc": "신체 부위별 통증 자가감별, 건강검진 수치 판독, 당월 환절기/계절성 질환, 보조기구 선택 기준",
        "roots": [
            # 건강검진 & 수치 판독
            "공복혈당", "당화혈색소", "간수치", "감마지티피", "ast수치", "alt수치",
            "총콜레스테롤", "ldl콜레스테롤", "중성지방", "hdl콜레스테롤", "단백뇨", "혈뇨",
            "요산수치", "갑상선수치", "tsh수치", "신장수치", "크레아티닌", "사구체여과율", "혈압정상수치",
            # 신체 통증 & 자가 감별
            "고관절통증", "족저근막염", "어깨결림", "무릎통증", "허리통증", "손목터널증후군",
            "방사통", "좌골신경통", "늑간신경통", "석회화건염", "오십견", "회전근개파열",
            "목디스크증상", "허리디스크증상", "담결림", "등통증", "꼬리뼈통증", "손발저림", "갈비뼈통증"
        ]
    }
}

# 하위 호환 별칭 (Aliases)
CORE_PILLARS = HONEYJAR_CATEGORIES

# 네이버 쇼핑 커넥트 연계 타깃 사전 (Shopping Connect Monetization Targets)
SHOPPING_CONNECT_TARGETS = {
    "hometraining": [
        "폼롤러", "요가매트", "스트레칭밴드", "루프밴드", "튜빙밴드", "짐볼", "스텝퍼", "실내자전거",
        "푸쉬업바", "아령", "덤벨", "케틀벨", "악력기", "마사지볼", "요가링", "문틀철봉", "마사지스틱"
    ],
    "diet_nutrition": [
        "마그네슘", "젖산마그네슘", "킬레이트마그네슘", "오메가3", "rTG오메가3", "유산균", "프로바이오틱스",
        "비타민c", "비타민d", "비타민b", "단백질보충제", "단백질쉐이크", "단백질음료", "프로틴",
        "콜라겐", "글루타치온", "밀크씨슬", "루테인", "차전자피", "크레아틴", "아르기닌", "코엔자임q10"
    ],
    "life_wellness": [
        "목견인기", "거북목교정기", "자세교정기", "허리보호대", "무릎보호대", "손목보호대", "발목보호대",
        "압박스타킹", "의료용압박스타킹", "코세척기", "온열안대", "찜질팩", "경추베개", "혈압계", "혈당측정기"
    ]
}


def detect_shopping_connect(keyword):
    """키워드가 네이버 쇼핑 커넥트와 연계 가능한 건강/운동/영양 제품군인지 판별합니다."""
    kw_lower = keyword.lower().replace(" ", "")
    for cat, targets in SHOPPING_CONNECT_TARGETS.items():
        for t in targets:
            t_lower = t.lower().replace(" ", "")
            if t_lower in kw_lower:
                return {
                    "eligible": True,
                    "category": cat,
                    "product_type": t,
                    "monetization_note": f"네이버 쇼핑 커넥트 [{t}] 연계 가능"
                }
    return {
        "eligible": False,
        "category": None,
        "product_type": None,
        "monetization_note": "정보성 콘텐츠 중심 (순수 검색 트래픽 유입형)"
    }


def get_category_roots(cat_key, count=4, shuffle=True):
    """지정 카테고리에서 시작 루트 단어를 추출하며, 라이프 웰니스는 당월 시의성을 자동 주입합니다."""
    if cat_key not in HONEYJAR_CATEGORIES:
        return []
    
    roots = list(HONEYJAR_CATEGORIES[cat_key]["roots"])
    
    # 라이프 웰니스인 경우 현재 월의 계절성 이슈를 최우선 주입
    if cat_key == "life_wellness":
        curr_month = datetime.now().month
        seasonal = MONTHLY_SEASONAL_FOCUS.get(curr_month, [])
        if seasonal:
            sampled_seasonal = random.sample(seasonal, min(2, len(seasonal))) if shuffle else seasonal[:2]
            sampled_general = random.sample(roots, min(count - len(sampled_seasonal), len(roots))) if shuffle else roots[:count - len(sampled_seasonal)]
            return sampled_seasonal + sampled_general

    if shuffle:
        return random.sample(roots, min(count, len(roots)))
    return roots[:count]


def get_hybrid_seeds(cat_key, count_roots=2, count_datalab=3, shuffle=True):
    """
    하이브리드 시드 생성기:
    1) 당월 시의성 및 해부학/질환 루트 (질환/통증/식단 E-E-A-T 트래픽용)
    2) 네이버 데이터랩 실시간 쇼핑인사이트 랭킹 (실시간 소비 & 쇼핑 커넥트용)
    두 스트림을 유기적으로 결합하여 최적의 융합 시드 리스트를 반환합니다.
    """
    # 1. 시의성 & 해부학 루트
    roots = get_category_roots(cat_key, count=count_roots, shuffle=shuffle)
    
    # 2. 데이터랩 실시간 쇼핑 인기 키워드
    datalab_kws = get_datalab_trending_keywords(cat_key, days=7, limit_per_cid=count_datalab)
    # 잡음 키워드 제거
    filtered_datalab = [k for k in datalab_kws if not any(neg in k for neg in NEGATIVE_WORDS)]
    
    if shuffle:
        random.shuffle(filtered_datalab)
    sampled_datalab = filtered_datalab[:count_datalab]
    
    # 두 스트림의 하이브리드 결합 (중복 제거)
    combined = list(dict.fromkeys(sampled_datalab + roots))
    return combined


def get_pillar_seeds(pillar_key, count=4, shuffle=True):
    return get_category_roots(pillar_key, count=count, shuffle=shuffle)


# 잡음 키워드 (Negative Filter) - 광고, 비의료 상업, 병원, 일반 잡화 전면 컷
NEGATIVE_WORDS = [
    # 비의료 / 일상 무관
    "자동차", "운전", "차량", "정기검사", "면허", "토익", "토플", "한국사", "공무원",
    # 자격증 / 취업 / 교육
    "자격증", "취업", "학원", "구인", "강의", "시험", "학과", "공부", "채용", "연수", "합격", "기출", "교재",
    # 상업 / 패션 / 일반 의류 / 잡화
    "가방", "옷", "원피스", "청바지", "코트", "패딩", "신발", "구두", "운동화", "가죽", "패션", "선물", "매장", "렌탈",
    "도시락", "고기", "쇼핑몰", "키트", "양말", "레깅스", "요가복", "운동복", "팬츠", "바지", "티셔츠", "속옷", "브라", "탑",
    # 화장품 / 미용
    "화장품", "크림", "로션", "세럼", "앰플", "비누", "샴푸", "린스", "바디워시", "향수", "립스틱",
    # 대형 가구 / 가전 / 전자기기
    "의자", "소파", "침대", "매트리스", "가구", "인테리어", "조명", "청소기", "세탁기", "냉장고", "마사지기", "안마기", "마사지건", "슬링백", "저주파기",
    # 치과 시술 / 식당 / 외식
    "임플란트", "치아교정", "틀니", "라식", "라섹", "필러", "보톡스", "지방흡입", "맛집", "식당", "카페", "술집",
    # 병원 전문 시술 / 수술 / 물리치료 (홈트나 자가관리가 아닌 병원 내원 치료)
    "도수치료", "체외충격파", "물리치료", "신경차단술", "시술", "수술", "입원", "퇴원", "마취", "주사치료",
    # 지역 한정 병원/장소 마케팅
    "대구", "부산", "인천", "광주", "대전", "울산", "창원", "수원", "제주", "강남", "서초", "송파",
    "노원", "일산", "분당", "부평역", "동성로", "남위례역", "한의원", "치과", "성형외과", "안과", "클리닉",
    "요양병원", "한방병원", "치과의원", "내과의원",
    # 금융 / 부동산
    "보험", "대출", "청약", "부동산", "카드", "실비", "환급", "보조금", "지원금"
]

POSITIVE_PATTERNS = [
    # 질문 / 증상 / 원인
    "증상", "원인", "이유", "통증", "초기", "구별", "차이", "단계", "신호", "자가진단",
    # 식단 / 영양 / 관리
    "효능", "부작용", "먹는법", "식단", "음식", "섭취", "영양", "보관", "세척", "주의사항",
    # 검진 / 수치 / 해석
    "정상수치", "수치", "검사", "재검", "판독", "기준", "결과", "수치표",
    # 대처 / 운동 / 자세 / 소도구
    "스트레칭", "운동", "자세", "대처", "완화", "치료법", "관리법", "골든타임", "응급처치",
    "사용법", "효과", "고르는법", "폼롤러", "마그네슘", "오메가", "견인기", "교정기",
    # 주요 건강 / 질환 개념
    "지방간", "역류성", "위염", "장염", "담석", "비염", "두통", "이명", "어지럼증",
    "근막동통", "디스크", "관절염", "당뇨", "콜레스테롤", "골다공증", "갑상선", "대상포진",
    "통풍", "결석", "수면", "불면증", "만성피로", "족저근막염", "이상지질혈증", "척추", "고관절"
]


def load_existing_posts():
    path = ROOT_DIR / "data/posts_db.json"
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def check_existing(kw, posts):
    kw_c = kw.replace(" ", "")
    for p in posts:
        t_c = p.get("title", "").replace(" ", "")
        s_c = p.get("slug", "").replace("-", "")
        d_c = p.get("desc", "").replace(" ", "")
        if len(kw_c) >= 3 and (kw_c in t_c or kw_c in s_c or kw_c in d_c):
            return p
    tokens = [t for t in ["손가락", "마디", "통증", "류마티스", "퇴행성", "관절염", "족저근막염", "비염", "독감", "백신", "위내시경", "수면내시경", "공복혈당", "중성지방", "단백뇨"] if t in kw_c]
    if len(tokens) >= 2:
        for p in posts:
            t = p.get("title", "")
            if all(tok in t for tok in tokens):
                return p
    return None


def calculate_synergy(kw, posts):
    """키워드와 기존 39편 글의 토픽 클러스터(내부 링크 시너지)를 계산합니다."""
    synergy_rules = [
        # 손가락 / 관절 / 류마티스 / 손목
        (["손가락", "관절", "류마티스", "마디", "손목", "방아쇠"], ["finger-joint-pain-rheumatoid-arthritis-morning-stiffness"]),
        # 허리 / 척추 / 코어 / 폼롤러
        (["허리", "디스크", "척추", "협착증", "요추", "골반", "기립근", "폼롤러"], ["pelvic-stretching-back-pain-relief", "core-exercise-home"]),
        # 목 / 어깨 / 거북목 / 목견인기
        (["목", "경추", "거북목", "일자목", "어깨", "라운드숄더", "승모근", "견갑골", "견인기", "교정기"], ["posture-stretching-office", "posture-wall-stretching", "frozen-shoulder-stretching-rotator-cuff-differentiation"]),
        # 하체 / 무릎 / 고관절 / 발 / 압박스타킹
        (["무릎", "고관절", "하체", "스쿼트", "발목", "발등", "족저", "아킬레스", "종아리", "압박스타킹"], ["knee-safe-squat-workout", "pelvic-stretching-back-pain-relief", "plantar-fasciitis-morning-heel-pain-stretching"]),
        # 혈당 / 당뇨 / 대사
        (["혈당", "당뇨", "인슐린", "식후", "당화혈색소"], ["fasting-blood-sugar-prediabetes-guide", "post-meal-walk-blood-sugar", "intermittent-fasting-guide"]),
        # 지질 / 콜레스테롤 / 혈관 / 오메가3
        (["콜레스테롤", "이상지질혈증", "지방간", "중성지방", "간수치", "ldl", "오메가"], ["triglycerides-retest-alcohol-preparation", "fasting-blood-sugar-prediabetes-guide"]),
        # 소변 / 신장 / 통풍
        (["소변", "단백뇨", "거품뇨", "요산", "통풍", "신장", "크레아티닌"], ["urinalysis-proteinuria-foamy-urine-retest-guide", "autumn-shrimp-crab-big-toe-pain-gout-care"]),
        # 감염 / 백신 / 환절기 면역 / 비염
        (["대상포진", "독감", "백신", "면역", "진드기", "비염", "감기", "환절기", "인후통", "코세척"], ["tick-bite-scab-scrub-typhus-symptoms-guide", "flu-vaccine-domestic-imported-comparison-free-target", "nasal-spray-rebound-rhinitis-5day-rule", "salt-water-gargle-concentration-ratio"]),
        # 식단 / 위장 / 소화 / 영양제 / 마그네슘
        (["식단", "단백질", "위염", "속쓰림", "소화", "커피", "유산균", "영양제", "마그네슘", "비타민"], ["morning-apple-heartburn-gastritis-egg", "coffee-after-meal-golden-time", "greek-yogurt-diet-trap", "slow-aging-rice-recipe"])
    ]

    matched_slugs = []
    for triggers, target_slugs in synergy_rules:
        if any(trig in kw for trig in triggers):
            matched_slugs.extend(target_slugs)

    matched_slugs = list(dict.fromkeys(matched_slugs))
    synergy_posts = []
    for p in posts:
        slug_base = p.get("slug", "").replace(".html", "")
        if slug_base in matched_slugs:
            synergy_posts.append({
                "slug": p.get("slug"),
                "title": p.get("title", "")[:35],
                "date": p.get("date")
            })

    return synergy_posts[:3]

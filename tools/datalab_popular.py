# -*- coding: utf-8 -*-
"""
꿀단지 (KKULDANJI) - 네이버 데이터랩 쇼핑인사이트 실시간 랭킹 수집 모듈 (datalab_popular.py)

1. 네이버 데이터랩 쇼핑인사이트(Shopping Insight) 공개 엔드포인트를 호출합니다.
2. 꿀단지 3대 카테고리(홈트레이닝, 식단 & 영양, 라이프 웰니스)에 매핑된 핵심 CID 순위를 수집합니다.
3. 시드 키워드 없이도 지금 대한민국 대중이 가장 많이 검색하고 구매하는 TOP 20 키워드를 실시간 반환합니다.
"""
import sys
import json
import urllib.request
from datetime import datetime, timedelta

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

DATALAB_URL = "https://datalab.naver.com/shoppingInsight/getCategoryKeywordRank.naver"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://datalab.naver.com/shoppingInsight/sCategory.naver',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

# 꿀단지 3대 공식 카테고리별 네이버 데이터랩 CID 매핑
CATEGORY_CIDS = {
    "hometraining": [
        {"name": "스포츠 > 헬스", "cid": "50000030"},
        {"name": "스포츠 > 요가/필라테스", "cid": "50000031"}
    ],
    "diet_nutrition": [
        {"name": "식품 > 건강식품", "cid": "50000023"},
        {"name": "식품 > 다이어트식품", "cid": "50000024"}
    ],
    "life_wellness": [
        {"name": "생활 > 건강관리용품", "cid": "50000068"},
        {"name": "생활 > 의료용품", "cid": "50000069"}
    ]
}


def fetch_datalab_ranks(cid, days=7, limit=15):
    """지정된 CID의 최근 days일간 네이버 쇼핑인사이트 인기 검색어 TOP 리스트를 가져옵니다."""
    end_d = datetime.now() - timedelta(days=1)
    start_d = end_d - timedelta(days=days)
    end_str = end_d.strftime('%Y-%m-%d')
    start_str = start_d.strftime('%Y-%m-%d')

    body = f"cid={cid}&timeUnit=date&startDate={start_str}&endDate={end_str}&age=&gender=&device="
    req = urllib.request.Request(DATALAB_URL, data=body.encode('utf-8'), headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        ranks = data.get('ranks', [])
        return [r.get('keyword') for r in ranks[:limit] if r.get('keyword')]
    except Exception as e:
        return []


def get_datalab_trending_keywords(category_key, days=7, limit_per_cid=10):
    """꿀단지 카테고리 키(hometraining, diet_nutrition, life_wellness)에 해당하는 실시간 인기 검색어를 반환합니다."""
    cids_info = CATEGORY_CIDS.get(category_key, [])
    results = []
    for info in cids_info:
        kws = fetch_datalab_ranks(info["cid"], days=days, limit=limit_per_cid)
        results.extend(kws)
    return list(dict.fromkeys(results))


if __name__ == "__main__":
    for cat in ["hometraining", "diet_nutrition", "life_wellness"]:
        kws = get_datalab_trending_keywords(cat, limit_per_cid=5)
        print(f"[{cat}] 데이터랩 실시간 TOP 키워드 ({len(kws)}개):", kws)

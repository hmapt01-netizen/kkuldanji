# -*- coding: utf-8 -*-
"""
꿀단지 (KKULDANJI) - 네이버 공식 검색광고 API 키워드 검색량 분석 엔진
- 네이버 공식 검색광고 API (/keywordstool)를 호출하여 최근 30일간의 실제 PC/모바일 검색수를 조회합니다.
- 개인 계정의 무료 API 라이선스를 사용하며 추가 과금이 전혀 발생하지 않습니다.
"""
import os
import sys
import time
import json
import hmac
import hashlib
import base64
import urllib.request
from urllib.parse import quote
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parents[1]
SECRET_FILE = ROOT_DIR / "naver_searchad_secret.json"
BASE_URL = "https://api.searchad.naver.com"


def load_credentials():
    if not SECRET_FILE.exists():
        raise FileNotFoundError(f"네이버 검색광고 API 키 파일이 없습니다: {SECRET_FILE}")
    with open(SECRET_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_signature(timestamp, method, uri, secret_key):
    message = f"{timestamp}.{method}.{uri}"
    signature = base64.b64encode(
        hmac.new(secret_key.encode("utf-8"), message.encode("utf-8"), hashlib.sha256).digest()
    ).decode("utf-8")
    return signature


def clean_volume(val):
    """'< 10' 등의 문자열을 안전하게 정수(또는 0)로 변환"""
    if isinstance(val, (int, float)):
        return int(val)
    if isinstance(val, str):
        val = val.strip()
        if val.startswith("<"):
            return 5
        try:
            return int(val.replace(",", ""))
        except ValueError:
            return 0
    return 0


def fetch_keyword_stats(keywords, show_detail=1):
    """
    네이버 키워드도구 API 호출
    :param keywords: 문자열(쉼표 구분) 또는 리스트 (최대 5개 힌트 키워드)
    :return: list of dict (키워드별 PC/모바일/총 검색수 및 경쟁도)
    """
    creds = load_credentials()
    if isinstance(keywords, list):
        hint = ",".join(k.replace(" ", "") for k in keywords[:5])
    else:
        hint = ",".join(k.strip().replace(" ", "") for k in keywords.split(",")[:5])

    timestamp = str(round(time.time() * 1000))
    method = "GET"
    uri = "/keywordstool"
    sig = generate_signature(timestamp, method, uri, creds["SECRET_KEY"])

    headers = {
        "X-Timestamp": timestamp,
        "X-API-KEY": creds["ACCESS_LICENSE"],
        "X-Customer": str(creds["CUSTOMER_ID"]),
        "X-Signature": sig,
        "User-Agent": "Mozilla/5.0"
    }

    url = f"{BASE_URL}{uri}?hintKeywords={quote(hint)}&showDetail={show_detail}"
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"네이버 검색광고 API 오류 (HTTP {e.code}): {error_body}")
    except Exception as e:
        raise RuntimeError(f"네이버 검색광고 API 호출 실패: {e}")

    results = []
    for item in data.get("keywordList", []):
        pc = clean_volume(item.get("monthlyPcQcCnt", 0))
        mo = clean_volume(item.get("monthlyMobileQcCnt", 0))
        results.append({
            "keyword": item.get("relKeyword", ""),
            "pc_volume": pc,
            "mobile_volume": mo,
            "total_volume": pc + mo,
            "comp_idx": item.get("compIdx", "보통"),
            "pc_ctr": float(item.get("monthlyAvePcCtr", 0.0) or 0.0),
            "mobile_ctr": float(item.get("monthlyAveMobileCtr", 0.0) or 0.0)
        })

    return results


def main():
    if len(sys.argv) < 2:
        print("사용법: python tools/naver_searchad.py <키워드1> [키워드2] ...")
        sys.exit(1)

    queries = sys.argv[1:]
    print("=" * 70)
    print(f"  🍯 [네이버 공식 검색광고 API] 실시간 월간 검색량 분석 리포트")
    print(f"  - 조회 키워드: {', '.join(queries)}")
    print("=" * 70)

    try:
        items = fetch_keyword_stats(queries)
        if not items:
            print("조회된 검색 데이터가 없습니다.")
            return

        # 입력한 힌트 키워드와 정확히 일치하거나 가장 연관성 높은 항목 정렬
        print(f"\n📊 [네이버 최근 30일 실제 검색량 순위 TOP 15]")
        print(f"{'순위':<4} | {'키워드':<20} | {'총 검색량':>10} | {'모바일':>10} | {'PC':>8} | {'경쟁도':^6}")
        print("-" * 70)

        for idx, it in enumerate(items[:15], 1):
            tot_str = f"{it['total_volume']:,}회"
            mo_str = f"{it['mobile_volume']:,}회"
            pc_str = f"{it['pc_volume']:,}회"
            print(f"{idx:<4} | {it['keyword']:<20} | {tot_str:>10} | {mo_str:>10} | {pc_str:>8} | {it['comp_idx']:^6}")

    except Exception as e:
        print(f"🚨 오류 발생: {e}")


if __name__ == "__main__":
    main()

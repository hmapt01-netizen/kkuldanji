# -*- coding: utf-8 -*-
"""
꿀단지 (KKULDANJI) - NCBI 공식 API 실시간 학술 메타데이터 취득 도구 (PubMed Metadata Fetcher)
- 사람이 손으로 타이핑하거나 AI 기억에 의존하는 오타를 원천 차단
- NCBI E-utilities API(eutils.ncbi.nlm.nih.gov)를 직접 호출하여 실제 논문 메타데이터 취득
"""
import sys
import json
import re
import urllib.request

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def fetch_pubmed_metadata(pmid: str) -> dict:
    """
    PMID를 입력받아 NCBI 공식 API에서 정식 메타데이터를 추출하여 딕셔너리로 반환
    """
    clean_pmid = str(pmid).strip()
    if not clean_pmid.isdigit():
        raise ValueError(f"유효하지 않은 PMID 형식입니다: '{pmid}'")

    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={clean_pmid}&retmode=json"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        raise RuntimeError(f"NCBI API 호출 실패 (PMID {clean_pmid}): {e}")

    result = data.get("result", {}).get(clean_pmid)
    if not result:
        raise ValueError(f"PMID {clean_pmid}에 해당하는 논문 정보를 찾을 수 없습니다.")

    title = result.get("title", "").strip().rstrip(".")
    pubdate = result.get("pubdate", "")
    year_match = re.search(r'\b(19\d\d|20\d\d)\b', pubdate)
    year = int(year_match.group(1)) if year_match else None

    source_journal = result.get("source", "")
    volume = result.get("volume", "")
    issue = result.get("issue", "")
    pages = result.get("pages", "")

    # 저자 파싱
    authors = [a.get("name") for a in result.get("authors", []) if a.get("name")]

    # PMCID 및 DOI 추출
    pmcid = None
    doi = None
    for item in result.get("articleids", []):
        id_type = item.get("idtype")
        val = item.get("value")
        if id_type == "pmc":
            pmcid = val
        elif id_type == "doi":
            doi = val

    return {
        "pmid": clean_pmid,
        "pmcid": pmcid,
        "doi": doi,
        "title": title,
        "authors": authors,
        "year": year,
        "journal": source_journal,
        "volume": volume,
        "issue": issue,
        "pages": pages,
        "url": f"https://pubmed.ncbi.nlm.nih.gov/{clean_pmid}/"
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python tools/fetch_pubmed_meta.py <PMID>")
        sys.exit(1)

    pmid_arg = sys.argv[1]
    meta = fetch_pubmed_metadata(pmid_arg)
    print(json.dumps(meta, ensure_ascii=False, indent=2))

"""Compatibility entrypoint; search questions are preserved, never scored by wording."""
import re
import sys

def extract_clean_query_and_seed(query):
    query = re.sub(r"\s+", " ", query).strip()
    if not query:
        raise ValueError("빈 검색어는 수집할 수 없습니다")
    return query, query

try:
    from .serp_collection import (audit_titles, audit_naver_serp, audit_google_serp,
        check_naver_autocomplete, check_google_autocomplete, fetch_naver_serp_docs,
        analyze_naver_competition, analyze_google_competition, main)
except ImportError:
    from serp_collection import (audit_titles, audit_naver_serp, audit_google_serp,
        check_naver_autocomplete, check_google_autocomplete, fetch_naver_serp_docs,
        analyze_naver_competition, analyze_google_competition, main)

if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
    main()

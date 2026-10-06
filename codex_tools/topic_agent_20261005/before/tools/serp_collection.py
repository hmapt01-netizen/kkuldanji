"""Read-only SERP collection and explicit, reviewable evidence import."""
import argparse
import json
from pathlib import Path
import urllib.request
import urllib.parse
from datetime import datetime

try:
    from .blue_ocean import SCHEMA_VERSION, parse_serp, evaluate, empty_review, audit_errors
except ImportError:
    from blue_ocean import SCHEMA_VERSION, parse_serp, evaluate, empty_review, audit_errors

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"


def now():
    return datetime.now().astimezone().isoformat()


def read_url(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept-Language": "ko-KR,ko;q=0.9"})
    with urllib.request.urlopen(req, timeout=10) as response:
        raw = response.read()
        charset = response.headers.get_content_charset() or "utf-8"
        return raw.decode(charset, errors="replace")


def autocomplete(channel, seed):
    q = urllib.parse.quote(seed)
    url = (f"https://ac.search.naver.com/nx/ac?q={q}&q_enc=UTF-8&st=100&frm=nv&r_format=json&r_enc=UTF-8&r_unicode=0&t_koreng=1&ans=2&run=2&rev=4&con=1" if channel == "naver" else
           f"https://suggestqueries.google.com/complete/search?client=firefox&hl=ko&q={q}")
    try:
        data = json.loads(read_url(url))
        items = ([i[0] for group in data.get("items", []) for i in group if i and isinstance(i[0], str)]
                 if channel == "naver" else data[1])
        return {"status": "ok", "items": list(dict.fromkeys(items)), "source_url": url, "error": None}
    except Exception as exc:
        return {"status": "error", "items": [], "source_url": url, "error": str(exc)}


def check_naver_autocomplete(seed):
    return autocomplete("naver", seed)["items"]


def check_google_autocomplete(seed):
    return autocomplete("google", seed)["items"]


def fetch_serp(channel, query):
    q = urllib.parse.quote(query)
    url = (f"https://search.naver.com/search.naver?where=nexearch&query={q}" if channel == "naver" else
           f"https://www.google.com/search?q={q}&hl=ko&gl=kr&num=10")
    result = {"search_url": url, "collected_at": now(), "collection_method": "http",
              "collection_status": "error", "top_docs": [], "excluded_results": [], "error": None}
    try:
        html = read_url(url)
        lowered = html.lower()
        if any(s in lowered for s in ("비정상적인 접근", "자동입력 방지문자", "unusual traffic", "g-recaptcha", "before you continue to google")):
            raise ValueError("차단/캡차/동의 화면: 검색 문서로 해석하지 않음")
        docs, excluded = parse_serp(html, channel)
        result.update(top_docs=docs, excluded_results=excluded)
        if not docs:
            raise ValueError("일반 문서 제목 링크를 식별하지 못함; 브라우저 실사 필요")
        result["collection_status"] = "ok"
    except Exception as exc:
        result["error"] = str(exc)
    return result


def fetch_naver_serp_docs(query):
    result = fetch_serp("naver", query)
    return result["top_docs"], result["error"]


def analyze_naver_competition(query, docs, error_msg, ac_items, seed):
    return "⚠️ 추가 조사", "수요 자료와 상위 문서 본문 검토 필요" + (f": {error_msg}" if error_msg else "")


def analyze_google_competition(query, ac_items, seed):
    return "⚠️ 추가 조사", "자동완성만으로 구글 경쟁도 판정 불가; 실제 SERP와 본문 검토 필요"


def save_audit(data):
    DATA_DIR.mkdir(exist_ok=True)
    for name in (f"last_{data['channel']}_serp_audit.json", "last_serp_audit.json"):
        (DATA_DIR / name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def audit_titles(titles, channel="naver"):
    try:
        from .audit_serp_live import extract_clean_query_and_seed
    except ImportError:
        from audit_serp_live import extract_clean_query_and_seed
    if channel not in ("naver", "google"):
        raise ValueError("channel must be naver or google")
    records = []
    cached = []
    try:
        previous = json.loads((DATA_DIR / f"last_{channel}_serp_audit.json").read_text(encoding="utf-8"))
        if not audit_errors(previous):
            cached = previous["records"]
    except (OSError, ValueError, TypeError, KeyError):
        pass
    for idx, title in enumerate(titles, 1):
        query, seed = extract_clean_query_and_seed(title)
        match = next((r for r in cached if r.get("clean_query") == query), None)
        if match:
            record = dict(match, idx=idx, title=title)
            record.update(evaluate(record))
            records.append(record)
            print(f"[{idx}/{len(titles)}] {query}: 24시간 내 동일 채널·질문 검토 재사용")
            continue
        ac = autocomplete(channel, seed)
        result = fetch_serp(channel, query)
        record = dict(result, idx=idx, title=title, clean_query=query, seed=seed,
                      autocomplete_count=len(ac["items"]), autocomplete_samples=ac["items"][:10],
                      autocomplete=ac, demand_status="unverified", coverage_note="",
                      review=empty_review(query))
        record["top_docs_count"] = len(record["top_docs"])
        record.update(evaluate(record))
        records.append(record)
        print(f"[{idx}/{len(titles)}] {query}: {record['badge']} (일반 문서 {len(record['top_docs'])}개, 자동완성 {ac['status']})")
    data = {"schema_version": SCHEMA_VERSION, "timestamp": now(), "channel": channel,
            "total_audited": len(records), "records": records}
    save_audit(data)
    print("수집 기록 저장. 완료 판정은 본문·수요 근거 검토 후 --import-review로 수행합니다.")
    return records


def audit_naver_serp(titles):
    return audit_titles(titles, "naver")


def audit_google_serp(titles):
    return audit_titles(titles, "google")


def import_review(path):
    """Accept recorded observations, never invent or repair missing evidence."""
    data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if data.get("channel") not in ("naver", "google"):
        raise ValueError("naver/google 채널 필요")
    errors = audit_errors(data)
    if errors:
        raise ValueError("\n".join(errors))
    for record in data["records"]:
        record.update(evaluate(record))
        record["top_docs_count"] = len(record["top_docs"])
    # Keep actual collection timestamp; importing must not refresh old evidence.
    save_audit(data)
    print(f"검토 기록 {len(data['records'])}건 구조 검사 완료. 근거 내용의 사실성과 순위를 자동 보증하지 않습니다.")
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("queries", nargs="*")
    parser.add_argument("--import-review", metavar="JSON")
    parser.add_argument("--review-template", metavar="JSON")
    args = parser.parse_args()
    if args.import_review:
        if args.queries or args.review_template:
            parser.error("--import-review는 다른 작업과 함께 사용할 수 없습니다")
        try:
            import_review(args.import_review)
        except (ValueError, OSError, TypeError, KeyError) as exc:
            parser.exit(1, f"검토 미완료: {exc}\n")
        return
    queries = args.queries
    channel = queries.pop(0) if queries and queries[0] in ("naver", "google") else "naver"
    if not queries:
        parser.error("실사할 검색어를 입력하세요 (고정 예제 자동 실행 없음)")
    audit_titles(queries, channel)
    if args.review_template:
        source = DATA_DIR / f"last_{channel}_serp_audit.json"
        target = Path(args.review_template)
        # Never overwrite an existing review and lose manual work.
        with target.open("x", encoding="utf-8") as output:
            output.write(source.read_text(encoding="utf-8"))
        print(f"검토용 사본 생성: {target}")

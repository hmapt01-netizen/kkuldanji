import concurrent.futures, html, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from serp_collection import read_url, now
work = Path(__file__).resolve().parent
audit = json.loads((work / 'naver_collection.json').read_text(encoding='utf-8'))
jobs = [(r['clean_query'], d) for r in audit['records'] for d in r['top_docs'][:3]]
def fetch(job):
    query, doc = job
    row = dict(query=query, **doc, accessed_at=now())
    try:
        raw = read_url(doc['url'])
        raw = re.sub(r'<(script|style)\b[^>]*>.*?</\1>', '', raw, flags=re.S|re.I)
        body = html.unescape(re.sub('<[^>]+>', ' ', raw))
        body = re.sub(r'\s+', ' ', body).strip()
        row['text_for_review'] = body[:11000]
    except Exception as exc:
        row['error'] = str(exc)
    return row
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    rows = list(pool.map(fetch, jobs))
(work / 'page_observations.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')
for row in rows:
    print(json.dumps(row, ensure_ascii=False))

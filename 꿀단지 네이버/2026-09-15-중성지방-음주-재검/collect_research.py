import concurrent.futures, html, json, re, sys
from pathlib import Path
from urllib.parse import urljoin
sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from serp_collection import read_url, autocomplete, now
W = Path(__file__).resolve().parent
def save(name, data):
    (W / name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
def fetch(doc):
    row = dict(doc, accessed_at=now())
    try:
        raw = read_url(doc['url'])
        frame = re.search(r'<iframe[^>]+(?:id="mainFrame"[^>]+src="([^"]+)"|src="([^"]+)"[^>]+id="mainFrame")', raw)
        if frame:
            row['frame_url'] = urljoin(doc['url'], html.unescape(frame.group(1) or frame.group(2)))
            raw = read_url(row['frame_url'])
        # Prefer the visible Naver SmartEditor article, excluding sidebar text.
        start = raw.find('class="se-main-container"')
        if start >= 0 and 'blog.naver.com' in doc['url']:
            raw = raw[start:]
            tail = raw.find('class="post_footer')
            if tail >= 0: raw = raw[:tail]
        raw = re.sub(r'<(script|style)\b[^>]*>.*?</\1>', '', raw, flags=re.S|re.I)
        text = html.unescape(re.sub('<[^>]+>', ' ', raw))
        text = re.sub(r'\s+', ' ', text).strip()
        row['body'] = text
    except Exception as exc: row['error'] = str(exc)
    return row
if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'initial':
        for channel in ('naver','google'):
            records = []
            for seed in ('중성지방','중성지방 검사','중성지방 재검','중성지방 술'):
                records.append(dict(autocomplete(channel,seed), seed=seed, observed_at=now(), kind='autocomplete'))
            save(channel+'_related_keywords.json', dict(channel=channel,records=records))
            print(channel, [(r['seed'],r['items']) for r in records])
        old=json.loads((ROOT/'2026-09-15-새글-주제조사/naver_collection.json').read_text(encoding='utf-8'))
        rec=next(r for r in old['records'] if r['clean_query']=='중성지방 전날 술')
        save('topic_serp_review.json',dict(schema_version=2,channel='naver',timestamp=old['timestamp'],records=[rec]))
        docs=rec['top_docs']
        name='topic_pages.json'
    else:
        data=json.loads((W/'naver_serp_audit.json').read_text(encoding='utf-8'))
        docs=list({d['url']:d for r in data['records'] for d in r['top_docs']}.values())
        name='title_pages.json'
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        rows=list(pool.map(fetch,docs))
    save(name,rows)
    for i,r in enumerate(rows):
        print(i,r['title'],r.get('error',''),len(r.get('body','')))

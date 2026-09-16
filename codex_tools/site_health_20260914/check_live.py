"""Read-only public-site health audit; separates publication drift from failures."""
import concurrent.futures as cf
import json
import re
import urllib.request
from urllib.parse import urljoin, urlsplit, urlunsplit, quote
from pathlib import Path
from datetime import datetime
from lxml import html, etree

ROOT = Path(__file__).resolve().parents[2]
WEB = ROOT / 'kkuldanji_web'
BASE = 'https://honeyjar.co.kr/'
OUT = Path(__file__).parent
db = json.loads((ROOT / 'data/posts_db.json').read_text(encoding='utf-8-sig'))
paths = ['/', '/about.html', '/terms.html', '/privacy.html', '/youth-protection.html', '/copyright.html', '/email-rejection.html', '/contact.html', '/calculator.html', '/admin.html', '/feed.xml', '/rss.xml', '/sitemap.xml']
paths += ['/posts/' + p['slug'] for p in db]
cache = {}
def get(url):
    try:
        u = urlsplit(url)
        safe = urlunsplit((u.scheme, u.netloc, quote(u.path, safe='/%:@'), quote(u.query, safe='=&%'), ''))
        req = urllib.request.Request(safe, headers={'User-Agent': 'HoneyjarAudit/2.0'})
        with urllib.request.urlopen(req, timeout=20) as r:
            return url, {'status':r.status, 'type':r.headers.get_content_type(), 'final':r.url, 'data':r.read()}
    except Exception as e:
        return url, {'error':str(e)}
def batch(urls):
    with cf.ThreadPoolExecutor(max_workers=4) as pool:
        for url, result in pool.map(get, sorted(set(urls)-cache.keys())):
            cache[url] = result

batch([urljoin(BASE,p) for p in paths])
docs = {}
assets, internal, external = set(), set(), set()
dynamic_email_pages = set()
drift, errors = [], []
for p in paths:
    url = urljoin(BASE,p)
    r = cache[url]
    if r.get('status') != 200:
        errors.append({'url':url, 'error':r.get('error',r.get('status'))}); continue
    if r.get('type') == 'text/html':
        doc = html.fromstring(r['data'].decode('utf-8')); docs[url] = doc
        for el in doc.xpath('//*[@href or @src]'):
            attr = 'src' if el.get('src') else 'href'
            raw = el.get(attr)
            u = urlsplit(urljoin(url,raw))
            if u.scheme not in ('https','http'): continue
            target = urlunsplit((u.scheme,u.netloc,u.path,u.query,''))
            if u.hostname not in ('honeyjar.co.kr','www.honeyjar.co.kr'):
                if el.tag == 'a': external.add(target)
                continue
            if u.path == '/cdn-cgi/l/email-protection':
                dynamic_email_pages.add(url)
                continue
            if attr == 'src' or (el.tag == 'link' and set(el.get('rel','').split()) & {'stylesheet','icon','apple-touch-icon','preload'}): assets.add(target)
            elif el.tag == 'a': internal.add(target)
        if p.startswith('/posts/'):
            local = html.fromstring((WEB / p.lstrip('/')).read_text(encoding='utf-8'))
            if doc.xpath('string(//h1)') != local.xpath('string(//h1)'):
                drift.append(p)
batch(assets | internal)
for url in sorted(assets | internal):
    r = cache[url]
    if r.get('status') != 200:
        errors.append({'url':url, 'error':r.get('error',r.get('status'))})
    elif url in assets and r.get('type') == 'text/html':
        errors.append({'url':url, 'error':'Asset unexpectedly returns HTML'})
feeds = {}
for p in ['feed.xml','rss.xml']:
    root = etree.fromstring(cache[BASE+p]['data'])
    feeds[p] = [(x.findtext('link'),x.findtext('title')) for x in root.findall('./channel/item')]
if feeds['feed.xml'] != feeds['rss.xml']: errors.append({'error':'Live feeds differ'})
feed_links = {x[0] for x in feeds['feed.xml']}
expected = {BASE+'posts/'+p['slug'] for p in db}
if feed_links != expected: errors.append({'error':'Live feed post URLs differ from published post set'})
sm = etree.fromstring(cache[BASE+'sitemap.xml']['data'])
sm_links = set(sm.xpath('//*[local-name()="loc"]/text()'))
if not expected <= sm_links: errors.append({'error':'Sitemap missing posts'})
report = {'checked_at':datetime.now().isoformat(), 'page_and_feed_requests':len(paths), 'unique_assets':len(assets), 'unique_internal_targets':len(internal), 'total_unique_requests':len(cache), 'live_feed_items':{k:len(v) for k,v in feeds.items()}, 'live_feeds_equal':feeds['feed.xml']==feeds['rss.xml'], 'sitemap_post_coverage':len(expected & sm_links), 'local_titles_not_yet_deployed':drift, 'external_links_not_tested':len(external), 'dynamic_email_pages_need_browser_check':sorted(dynamic_email_pages), 'errors':errors, 'requests':{u:{k:v for k,v in r.items() if k!='data'} for u,r in cache.items()}}
(OUT/'live_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='requests'},ensure_ascii=False,indent=2),flush=True)
raise SystemExit(bool(errors))

from pathlib import Path
import json,urllib.request,concurrent.futures as cf,subprocess,difflib
from lxml import html
R=Path(__file__).resolve().parents[2]
S=['sleep-hygiene-guide.html','sleep-lying-down-eyes-closed-20min-rule.html']
def check(s):
    req=urllib.request.Request('https://honeyjar.co.kr/posts/'+s,headers={'User-Agent':'HoneyjarDeploymentAudit/1.0','Cache-Control':'no-cache'})
    with urllib.request.urlopen(req,timeout=20) as r: live=html.fromstring(r.read().decode('utf-8')); status=r.status
    local=html.fromstring((R/'kkuldanji_web/posts'/s).read_text(encoding='utf-8'))
    sel='//div[contains(concat(" ",normalize-space(@class)," ")," article-body-content ")]'
    norm=lambda e:' '.join(e.text_content().split())
    return {'slug':s,'http':status,'title_matches':norm(live.xpath('//h1')[0])==norm(local.xpath('//h1')[0]),'body_matches':norm(live.xpath(sel)[0])==norm(local.xpath(sel)[0]),'ads_loaders':len(live.xpath('//script[contains(@src,"pagead2.googlesyndication.com/pagead/js/adsbygoogle.js")]'))}
with cf.ThreadPoolExecutor(max_workers=2) as ex: rows=list(ex.map(check,S))
(Path(__file__).parent/'deployed_content.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(rows,ensure_ascii=False,indent=2))
G='C:/Users/lim/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/git/cmd/git.exe'
old=json.loads(subprocess.check_output([G,'show','f4cd141:data/posts_db.json'],cwd=R).decode('utf-8-sig'))
new=json.loads((R/'data/posts_db.json').read_text(encoding='utf-8-sig'))
a=next(p['bodyHtml'] for p in old if p['slug']=='endoscopy-meal-coffee-timing.html')
b=next(p['bodyHtml'] for p in new if p['slug']=='endoscopy-meal-coffee-timing.html')
print('Additional endoscopy change:')
for line in difflib.unified_diff(a.splitlines(),b.splitlines(),n=1):
    if len(line)<1500:print(line)
raise SystemExit(not all(r['title_matches'] and r['body_matches'] and r['ads_loaders']==1 for r in rows))

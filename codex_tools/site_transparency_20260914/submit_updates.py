from pathlib import Path
import re,json,urllib.request,urllib.error

R=Path(__file__).resolve().parents[2]; W=Path(__file__).resolve().parent
ps=(R/'tools/indexnow_submit.ps1').read_text(encoding='utf-8-sig')
key=re.search(r'\$key\s*=\s*"([a-zA-Z0-9]+)"',ps).group(1)
location='https://honeyjar.co.kr/'+key+'.txt'
assert (R/'kkuldanji_web'/f'{key}.txt').read_text().strip()==key
key_request=urllib.request.Request(location,headers={'User-Agent':'HoneyjarDeploymentAudit/1.0'})
with urllib.request.urlopen(key_request,timeout=15) as response:assert response.read().decode().strip()==key
slugs=['slow-aging-rice-recipe','coffee-after-meal-golden-time','fasting-blood-sugar-prediabetes-guide','fruit-washing-liver-health']
urls=['https://honeyjar.co.kr/posts/'+s+'.html' for s in slugs]
payload={'host':'honeyjar.co.kr','key':key,'keyLocation':location,'urlList':urls}
request=urllib.request.Request('https://api.indexnow.org/indexnow',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json; charset=utf-8','User-Agent':'HoneyjarDeploymentAudit/1.0'},method='POST')
try:
    with urllib.request.urlopen(request,timeout=20) as response:status=response.status
except urllib.error.HTTPError as exc:status=exc.code
report={'urls':urls,'status':status,'accepted':status in (200,202),'indexed':'Not verified; acceptance is not indexing'}
(W/'indexnow_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('IndexNow',status,'URLs:',len(urls),'accepted:',report['accepted'])
if not report['accepted']:raise SystemExit(1)

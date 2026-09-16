from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request,json,re
from lxml import html

R=Path(__file__).resolve().parents[2]; W=Path(__file__).resolve().parent
slugs=['slow-aging-rice-recipe','coffee-after-meal-golden-time','fasting-blood-sugar-prediabetes-guide','fruit-washing-liver-health']
paths=['posts/'+s+'.html' for s in slugs]+['index.html','privacy.html','contact.html']
def text(el):return ' '.join(el.text_content().split())
def check(path):
    req=urllib.request.Request('https://honeyjar.co.kr/'+path,headers={'User-Agent':'HoneyjarDeploymentAudit/1.0'})
    with urllib.request.urlopen(req,timeout=20) as response:
        live=html.fromstring(response.read().decode('utf-8')); status=response.status
    local=html.fromstring((R/'kkuldanji_web'/path).read_text(encoding='utf-8'))
    ads=live.xpath('//script[contains(@src,"pagead2.googlesyndication.com/pagead/js/adsbygoogle.js")]')
    assert len(ads)==1,(path,'ads',len(ads))
    if path.startswith('posts/'):
        assert text(live.xpath('//h1')[0])==text(local.xpath('//h1')[0]),(path,'title')
        selector='//div[contains(concat(" ",normalize-space(@class)," ")," article-body-content ")]'
        assert text(live.xpath(selector)[0])==text(local.xpath(selector)[0]),(path,'body')
    if path=='privacy.html':assert '최종 개정 및 적용: 2026년 9월 14일' in text(live) and 'FormSubmit' in text(live)
    if path=='contact.html':
        field=live.xpath('//*[@id="contact-privacy-consent"]')[0]
        assert 'required' in field.attrib and 'checked' not in field.attrib
    return {'path':path,'status':status,'ads_loaders':len(ads),'matches_reviewed_change':True}
with ThreadPoolExecutor(max_workers=4) as pool: rows=list(pool.map(check,paths))
(W/'live_content_report.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(rows,ensure_ascii=False,indent=2))

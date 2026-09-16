"""Render isolated text previews and inspect draft-only constraints."""
import html, json, re, sys
from pathlib import Path
W=Path(__file__).resolve().parent
sys.path.insert(0,str(W.parents[1]/'tools'))
from audit_duplicates import audit_cross_duplicates, get_pure_text, get_ngrams

def inline(s):
    s=html.escape(s)
    s=re.sub(r'\[([^]]+)\]\((https://[^)]+)\)',r'<a href="\2">\1</a>',s)
    return re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)

def render(md, channel):
    lines=md.splitlines(); title=lines[0].lstrip('# ').strip(); out=[]; sections=[]
    blocks='\n'.join(lines[1:]).strip().split('\n\n')
    for block in blocks:
        if block.startswith('## '):
            label=block[3:]; ident='section-'+str(len(sections)+1)
            if label != '참고 자료': sections.append((ident,label))
            out.append(f'<h2 id="{ident}">{inline(label)}</h2>')
        elif block.startswith('### '): out.append('<h3>'+inline(block[4:])+'</h3>')
        elif block.startswith('> '): out.append('<blockquote>'+ '<br>'.join(inline(s.lstrip('> ')) for s in block.splitlines())+'</blockquote>')
        elif block.startswith('<div'): out.append(block)
        elif block.startswith('|'):
            rows=[r.strip('|').split('|') for r in block.splitlines()]
            cells=lambda row,tag: '<tr>'+''.join(f'<{tag}>{inline(c.strip())}</{tag}>' for c in row)+ '</tr>'
            out.append('<div class="custom-data-table-wrap"><table class="custom-data-table"><thead>'+cells(rows[0],'th')+'</thead><tbody>'+''.join(cells(r,'td') for r in rows[2:])+'</tbody></table></div>')
        elif block.startswith('- '):out.append('<ul>'+''.join('<li>'+inline(r[2:])+'</li>' for r in block.splitlines())+'</ul>')
        else: out.append('<p>'+inline(block).replace('\n','<br>' if channel=='naver' else ' ')+'</p>')
    toc='<nav class="toc-box">'+''.join(f'<a href="#{i}">{inline(t)}</a>' for i,t in sections)+'</nav>' if channel=='google' else ''
    body='\n'.join(out)
    if channel=='google':
        pos=body.find('<h2 '); body=body[:pos]+toc+body[pos:]
        faqs=json.loads((W/'google_faqs.json').read_text(encoding='utf-8'))
        body+='<section class="faq"><h2>자주 묻는 질문</h2>'+''.join('<details open><summary>'+inline(q['question'])+'</summary><p>'+inline(q['answer'])+'</p></details>' for q in faqs)+'</section>'
    css='''body{margin:0;background:#f5f5f0;color:#283d38;font-family:"Malgun Gothic",sans-serif}main{max-width:760px;margin:35px auto;background:white;padding:48px;border-radius:20px}header{border-bottom:1px solid #dde7df;padding-bottom:26px;margin-bottom:28px}.brand{font-size:13px;letter-spacing:2px;color:#56816c}h1{font-size:30px;line-height:1.55;letter-spacing:-1px}h2{font-size:21px;margin:44px 0 22px}p{font-size:1.02rem;line-height:1.9;margin:0 0 22px;color:#334155}blockquote{margin:24px 0;padding:24px;background:#f2f6ee;line-height:1.9;border-left:4px solid #6d9573}a{color:#286b56}li{line-height:1.9;margin:12px 0}.toc-box{display:flex;flex-direction:column;gap:12px;padding:22px;background:#f8faf8;border-radius:12px}.toc-box a{text-decoration:none}.custom-data-table-wrap{overflow-x:auto;border:1px solid #dbe3df;border-radius:12px;margin:28px 0}table{border-collapse:collapse;min-width:560px;width:100%;font-size:14px}th,td{padding:15px;border-bottom:1px solid #e1e7e4;text-align:left}th{background:#edf4ef}.info-section-card{padding:24px;border-radius:14px;background:#f1f6f3;margin:28px 0}.info-card-title{font-weight:bold;margin-bottom:18px}.info-step-item{display:flex;gap:14px;line-height:1.8;margin-top:14px}.info-badge{background:#d4e8dc;padding:2px 10px;border-radius:6px;white-space:nowrap;height:26px}summary{font-weight:bold;cursor:pointer;line-height:1.8}details{padding:16px 0;border-bottom:1px solid #ddd}.naver{text-align:center;max-width:560px}.naver h2{font-size:20px}.naver strong{background:#fff1a8}.naver p{line-height:1.9}.naver h3{margin-top:46px}@media(max-width:650px){main{margin:0;padding:25px 20px;border-radius:0}h1{font-size:25px}h2{font-size:19px}.naver p{font-size:15px}}'''
    page='<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(title)+'</title><style>'+css+'</style><main class="'+channel+'"><header><div class="brand">꿀단지 · 에디터 혀니</div><h1>'+html.escape(title)+'</h1></header>'+body+'</main></html>'
    (W/(channel+'_draft_preview.html')).write_text(page,encoding='utf-8')
    # Narrative only, excluding title, attribution, references, FAQ, navigation.
    narrative=md.split('\n\n',2)[-1] if channel=='google' else '\n'.join(lines[1:])
    narrative=narrative.split('## 참고 자료')[0].split('### 참고한 자료')[0]
    narrative=re.sub(r'^>.*$', '', narrative,flags=re.M)
    text=get_pure_text(re.sub(r'(?m)^#{1,3}\s*','',narrative).replace('**',''))
    return dict(with_spaces=len(text),without_spaces=len(re.sub(r'\s','',text)),h2=[t for _,t in sections],text=text)

stats={c:render((W/(c+'_draft.md')).read_text(encoding='utf-8'),c) for c in ('naver','google')}
audit_cross_duplicates(str(W/'naver_draft_preview.html'),str(W/'google_draft_preview.html'))
for c,s in stats.items(): print(c, {k:v for k,v in s.items() if k!='text'})
n,g=stats['naver'],stats['google']
sentences=lambda t:set(s.strip() for s in re.split(r'(?<=[.!?])\s+',t) if len(s.strip())>=15)
same=sentences(n['text']) & sentences(g['text'])
metrics={c:{k:v for k,v in s.items() if k!='text'} for c,s in stats.items()}
metrics['identical_sentences']=sorted(same)
metrics['scope']='이미지 없는 텍스트 초안. 이미지·스티커·최종 네이버 패키지·발행 검수는 이후 수행.'
(W/'draft_checks.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf-8')
assert not same, same
assert 1800<=n['with_spaces']<=2400 and 1200<=n['without_spaces']<=1600,n['with_spaces']
assert 3500<=g['with_spaces']<=4000,g['with_spaces']
assert len(n['h2'])==3 and len(g['h2']) in range(5,8)
assert all(len(t.replace('| ',''))<=25 for s in stats.values() for t in s['h2'])

"""This article's text previews and preliminary audits; no registration/build."""
import contextlib
import hashlib
import html
import io
import json
from pathlib import Path
import re
import sys

WORK = Path(__file__).resolve().parent
sys.path.insert(0, str(WORK.parent / 'tools'))
import audit_duplicates as cross
import audit_naver_post as naver_audit

def inline(text):
    text = html.escape(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'<a href="\2">\1</a>', text)
    return text

def render(md, channel):
    chunks = md.strip().split('\n\n')
    result = []
    for chunk in chunks:
        if chunk.startswith('<!--'): continue
        if chunk.startswith('# '): result.append('<h1>' + inline(chunk[2:]) + '</h1>')
        elif chunk.startswith('## '): result.append('<h2>' + inline(chunk[3:]) + '</h2>')
        elif chunk.startswith('> '):
            result.append('<blockquote>' + '<br>'.join(inline(x.removeprefix('> ')) for x in chunk.splitlines()) + '</blockquote>')
        elif chunk.startswith('|'):
            rows = [r for r in chunk.splitlines() if not re.fullmatch(r'[|\s:-]+',r)]
            cells = [[inline(c.strip()) for c in r.strip('|').split('|')] for r in rows]
            table = '<thead><tr>' + ''.join('<th>'+c+'</th>' for c in cells[0]) + '</tr></thead><tbody>'
            table += ''.join('<tr>'+''.join('<td>'+c+'</td>' for c in row)+'</tr>' for row in cells[1:])+'</tbody>'
            result.append('<div class="custom-data-table-wrap"><table>'+table+'</table></div>')
        elif chunk.startswith('- '):
            result.append('<ul>'+''.join('<li>'+inline(x.removeprefix('- '))+'</li>' for x in chunk.splitlines())+'</ul>')
        else:
            content = ('<br>' if channel=='naver' else ' ').join(inline(x) for x in chunk.splitlines())
            if channel=='google' and chunk.startswith(('첫 번째 확인','두 번째는','세 번째는')):
                result.append('<div class="info-section-card">'+content+'</div>')
            else: result.append('<p>'+content+'</p>')
    return '\n'.join(result)

CSS = '''body{margin:0;background:#faf8f2;color:#26342c;font-family:"Malgun Gothic",sans-serif}main{max-width:760px;margin:32px auto;background:white;padding:40px;border-radius:18px}h1{font-size:28px;line-height:1.5;letter-spacing:-1px}h2{font-size:21px;line-height:1.6;margin-top:44px;padding-left:12px;border-left:4px solid #e2b441}p{font-size:16px;line-height:1.9;margin:0 0 22px}strong{background:#fff2b3}blockquote{background:#f7f5ec;padding:20px;margin:26px 0;line-height:1.8}.info-section-card{background:#eff6f1;border:1px solid #d6e6da;padding:18px;border-radius:12px;margin:24px 0;line-height:1.8}.custom-data-table-wrap{overflow-x:auto;margin:28px 0;border:1px solid #ddd;border-radius:10px}table{width:100%;min-width:560px;border-collapse:collapse;font-size:14px;line-height:1.7}th,td{padding:12px;border-bottom:1px solid #ddd;text-align:left}th{background:#f2f4ef}a{color:#326a4d}li{line-height:1.8;margin-bottom:16px}footer{font-size:13px;color:#777;line-height:1.7;padding:20px 0}details{border-top:1px solid #ddd;padding:18px 0}summary{font-weight:bold;cursor:pointer}details p{margin-top:14px}body.naver main{max-width:600px;text-align:center}body.naver h2{display:table;margin:40px auto 24px}body.naver p{line-height:1.95}@media(max-width:680px){main{padding:24px 18px;margin:0;border-radius:0}h1{font-size:24px}h2{font-size:19px}}'''

report = {'scope':'텍스트 초안만 검사. 이미지·최종 패키지·빌드·발행 검수는 미실행.', 'channels':{}}
bodies = {}
for channel in ('google','naver'):
    md = (WORK/(channel+'_draft.md')).read_text(encoding='utf-8')
    body, refs = md.split('<!-- REFERENCES -->')
    title = md.splitlines()[0][2:]
    body_html = render(body,channel)
    refs_html = render(refs,channel)
    body_only = re.sub(r'<h1[\s\S]*?</h1>', '', body_html, count=1)
    plain = html.unescape(cross.get_pure_text(body_only))
    bodies[channel] = plain
    details = dict(chars_with_spaces=len(plain), chars_without_spaces=len(re.sub(r'\s','',plain)),
        h2=cross.get_h2_tags(body_html), title_chars=len(title),
        draft_sha256=hashlib.sha256((WORK/(channel+'_draft.md')).read_bytes()).hexdigest())
    report['channels'][channel] = details
    if channel=='google': assert 3500<=len(plain)<=4000
    else:
        assert 1800<=len(plain)<=2400 and 1200<=len(re.sub(r'\s','',plain))<=1600
        assert len(details['h2'])==3
        assert not [b for b in naver_audit.banned if b in html.unescape(cross.get_pure_text(body_html+refs_html))]
    assert all(len(t)<=25 for t in details['h2'])
    faq_html = ''
    if channel=='google':
        faqs = json.loads((WORK/'google_faqs.json').read_text(encoding='utf-8'))
        faq_html = '<aside><h3>자주 묻는 질문</h3>'+''.join('<details><summary>'+inline(f['question'])+'</summary><p>'+inline(f['answer'])+'</p></details>' for f in faqs)+'</aside>'
    doc = '<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>'+html.escape(title)+'</title><style>'+CSS+'</style></head><body class="'+channel+'"><main>'+body_html+faq_html+'<footer>'+refs_html+'</footer></main></body></html>'
    (WORK/(channel+'_draft_preview.html')).write_text(doc,encoding='utf-8')

def sentences(text):
    return {re.sub(r'\s+',' ',s).strip() for s in re.split(r'[.!?。]+',text) if len(re.sub(r'\s+',' ',s).strip())>=15}
common = sorted(sentences(bodies['naver']) & sentences(bodies['google']))
n = cross.get_ngrams(bodies['naver']); g = cross.get_ngrams(bodies['google'])
report.update(identical_sentences_15_plus=common, body_4gram_percent=round(100*len(n&g)/len(n),2))
assert not common
assert report['body_4gram_percent']<5
buf=io.StringIO()
with contextlib.redirect_stdout(buf):
    n_ok=naver_audit.audit_naver(str(WORK/'naver_draft_preview.html'))
    c_ok=cross.audit_cross_duplicates(str(WORK/'naver_draft_preview.html'),str(WORK/'google_draft_preview.html'))
log=buf.getvalue()
(WORK/'draft_shared_audit.log').write_text(log,encoding='utf-8')
report.update(existing_naver_audit=n_ok, existing_cross_audit=c_ok,
    audit_limitations='원본 교차검사의 분량 구간은 현 운영 규칙과 다름. 위 chars는 제목·FAQ·참고문헌을 제외한 본문/소제목/표/상단 요약 기준. 이미지 캡션은 아직 없으므로 해당 검증은 미대상.')
(WORK/'draft_review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
if not n_ok or not c_ok:
    print(log)
    raise SystemExit(2)

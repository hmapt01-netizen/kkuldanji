from pathlib import Path
import json,re,sys,shutil
W=Path(__file__).resolve().parent;R=W.parents[1]
sys.path.insert(0,str(R/'codex_tools'))
import workflow_guard as g
from register_post import validate_body_style
p=W/'post_data.json';data=g.read(p)
backup=W/'registration_backup/post_data_before_lead.json'
if not backup.exists():shutil.copy2(p,backup)
body=data['bodyHtml']
pattern=r'<blockquote\b([^>]*)>.*?</blockquote>\s*<p\b[^>]*><strong>(.*?)</strong></p>'
body,count=re.subn(pattern,lambda m:'<div'+m[1]+'><strong>'+m[2]+'</strong></div>',body,count=1,flags=re.S)
assert count==1,'Expected existing quote and adjacent summary'
validate_body_style(body)
data['bodyHtml']=body
p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
receipt=next(r for r in g.state_of(W)['receipts'] if r['stage']=='assembly')
g.record(W,'assembly',[a['path'] for a in receipt['artifacts']],'사용자 요청: 도입부 기관 요지·조회 날짜 제거, 기존 핵심 답변을 요약 카드로 통합. 참고문헌 유지')
print('Lead updated; references preserved')

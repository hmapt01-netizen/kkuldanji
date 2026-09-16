from pathlib import Path
raise SystemExit('폐기된 복구 방식: 원본 증거/receipt 재작성 금지. register_post.py 또는 site_pipeline.py 사용')
import sys,json,shutil
W=Path(__file__).resolve().parent;R=W.parents[1]
sys.path.insert(0,str(R/'codex_tools'))
import workflow_guard as g
state=g.state_of(W)
backup=W/'registration_backup/workflow_before_registration.json'
if not backup.exists():shutil.copy2(W/g.STATE,backup)
p=W/'리서치.md'
s=p.read_text(encoding='utf-8')
if '## 등록용 기존 SERP 보고서 연결' not in s:
    shutil.copy2(p,W/'registration_backup/research_before_registration.md')
    p.write_text(s+'\n\n## 등록용 기존 SERP 보고서 연결\n\n기존 조회 결과를 재사용하며 조회 시점을 변경하지 않습니다.\n\n'+(W/'naver_report.md').read_text(encoding='utf-8')+'\n'+(W/'google_report.md').read_text(encoding='utf-8'),encoding='utf-8')
for receipt in state['receipts']:
    stage=receipt['stage']
    expected,_=g.next_step(W,g.state_of(W))
    if expected!=stage:continue
    g.record(W,stage,[a['path'] for a in receipt['artifacts']],receipt['note'],receipt.get('user_message',''),receipt.get('selected_title',''))
print(g.next_step(W,g.state_of(W)))

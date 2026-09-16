import json, re, sys, shutil
raise SystemExit('별도 미리보기 변환 폐기: post_data.json을 기존 사이트 서식으로 직접 작성하고 site_pipeline.py를 실행하세요.')
from pathlib import Path
W=Path(__file__).resolve().parent
R=W.parents[1]
sys.path.insert(0,str(R/'codex_tools'))
import workflow_guard as g
g.require_step(W,'assembly')
state=g.state_of(W)
titles={r['stage'].replace('_selection',''):r['selected_title'] for r in state['receipts'] if r['stage'].endswith('_selection')}
slug='triglycerides-retest-alcohol-preparation'
page=(W/'google_with_images.html').read_text(encoding='utf-8')
body=page.split('</header>',1)[1].rsplit('</main>',1)[0]
body=re.sub(r'^<figure>.*?</figure>','',body,count=1,flags=re.S)
body=body.split('<h2 id="section-7">')[0]
body=body.replace('src="images/','src="../images/posts/'+slug+'/')
body=body.replace('<figure>','<figure style="margin:30px 0;">').replace('<img ','<img style="display:block;width:100%;height:auto;border-radius:12px;" ')
body=body.replace('<p>','<p style="font-size:1.02rem;line-height:1.9;color:#334155;margin-bottom:22px;">')
body=body.replace('<nav class="toc-box">','<nav class="toc-box" style="display:flex;flex-direction:column;gap:12px;padding:22px;background:#f8faf8;border-radius:12px;">')
md=(W/'google_draft.md').read_text(encoding='utf-8')
refs=[]
for line in md.split('## 참고 자료')[1].splitlines():
    if line.startswith('- '):refs.append(re.sub(r'\[([^]]+)\]\((https://[^)]+)\)',r'<a href="\2">\1</a>',line[2:]))
data=dict(title=titles['google'],shortTitle='중성지방 재검 준비와 금주 후 결과 비교',slug=slug+'.html',slugKey=slug,date='2026.09.15',category='라이프 웰니스',author='에디터 혀니',readTime='7분',desc='중성지방 재검을 앞두고 검사 조건과 금주 후 생활 변화를 기록하는 방법, 이전 결과표와 비교할 항목 및 다음 상담 준비를 살펴봅니다.',thumb=f'images/posts/{slug}/thumb.jpg',featuredCaption='재검 결과와 생활 기록을 함께 확인할 준비',isEditorPick=False,academicSource='MedlinePlus·Mayo Clinic·질병관리청·ACC 공인 안내 기반',bodyHtml=body,references=refs,faqs=[dict(q=q['question'],a=q['answer']) for q in json.loads((W/'google_faqs.json').read_text(encoding='utf-8'))])
(W/'post_data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
(W/'titles.json').write_text(json.dumps(titles,ensure_ascii=False,indent=2),encoding='utf-8')
naver=(W/'naver_draft.md').read_text(encoding='utf-8')
for anchor,slot in [('술도 쉬었고','thumb'),('지난번에는','post01'),('간식을 먹거나','post02'),('금주하면서','post03'),('이번에 시작한','post04'),('중성지방이 내려가서','post05'),('좋아진 결과를','naver_extra01')]:
    naver=naver.replace(anchor,f'![재검 준비 이미지](images/{slot}.jpg)\n\n'+anchor,1)
(W/'naver_final.md').write_text(naver,encoding='utf-8')
backup=W/'registration_backup';backup.mkdir(exist_ok=True)
if not (backup/'posts_db.json').exists():shutil.copy2(R/'data/posts_db.json',backup/'posts_db.json')
g.record(W,'assembly',['post_data.json','naver_final.md',*[f'images/{n}.jpg' for n in ['thumb','post01','post02','post03','post04','post05']]],'확정 원고와 승인 이미지로 사이트 데이터 및 네이버 원고 조립')
print('assembly complete')

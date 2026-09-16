"""Article-specific static verification using the existing auditors."""
from pathlib import Path
import contextlib, copy, hashlib, html, io, json, re, sys
from lxml import html as lh
W=Path(__file__).resolve().parent
sys.path.insert(0,str(W.parent/'tools'))
import audit_duplicates as dup, audit_naver_post as na

data=json.loads((W/'post_data.json').read_text(encoding='utf-8'))
assembly=json.loads((W/'assembly_review.json').read_text(encoding='utf-8'))
np=Path(assembly['naver_package']);gp=W/'google_final_preview.html'
ndoc=np.read_text(encoding='utf-8');gdoc=gp.read_text(encoding='utf-8')
n=lh.fromstring(ndoc);g=lh.fromstring(gdoc)
issues=[]
for path,tree in [(np,n),(gp,g)]:
    for elem in tree.xpath('//*[@src]|//link[@href]'):
        value=elem.get('src') or elem.get('href')
        if not value.startswith(('http','#','data:')) and not (path.parent/value).is_file():issues.append('missing: '+value)
    for tag in ['div','section','article','main','aside','figure']:
        source=path.read_text(encoding='utf-8')
        assert len(re.findall(r'<'+tag+r'\b',source))==len(re.findall(r'</'+tag+'>',source)),tag
    assert len(tree.xpath('//link[contains(@rel,"icon")]'))==5
    assert len(tree.xpath('//img'))==6
    assert len({x.get('src') for x in tree.xpath('//img')})==6
assert not issues,issues
assert len(n.xpath('//h2'))==3 and len(g.xpath('//h2'))==6
assert not n.xpath('//table|//figcaption|//a[starts-with(@href,"http")]')
assert len(g.xpath('//table'))==1 and len(g.xpath('//details'))==3
assert 'FAQ' not in data['bodyHtml'] and '자주 묻는 질문' not in data['bodyHtml']
assert len(n.xpath('//*[@data-editor-only]'))==8
assert [Path(x.get('src')).name for x in n.xpath('//img')]==assembly['image_order_naver']
assert [Path(x.get('src')).name for x in g.xpath('//img')]==assembly['image_order_google']
assert all(len(''.join(x.itertext()))<=25 for x in n.xpath('//h2')+g.xpath('//h2'))
draftreview=json.loads((W/'draft_review.json').read_text(encoding='utf-8'))
for channel in ('google','naver'):
    assert hashlib.sha256((W/(channel+'_draft.md')).read_bytes()).hexdigest()==draftreview['channels'][channel]['draft_sha256']

log=io.StringIO()
with contextlib.redirect_stdout(log):
    n_ok=na.audit_naver(str(np))
    cross_ok=dup.audit_cross_duplicates(str(np),str(gp))
(W/'assembled_shared_audit.log').write_text(log.getvalue(),encoding='utf-8')
print(log.getvalue())
report=dict(image_links_missing=issues,html_structure='pass',icons=5,images_each=6,
            naver_h2=3,google_h2=6,naver_captions=0,naver_table_faq=0,google_table=1,google_faq=3,
            naver_existing_audit=n_ok,cross_existing_audit=cross_ok,draft_hashes_preserved=True,
            body_counts=draftreview['channels'],body_4gram_percent=draftreview['body_4gram_percent'],
            identical_sentences_15_plus=draftreview['identical_sentences_15_plus'],
            limits=['브라우저 화면 및 복사 버튼 실제 작동 미검사','초안 본문 수치에 캡션·목차·편집 스티커·태그·참고문헌 제외'],
            naver_related_link='사용자 요청으로 생략')
(W/'assembled_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
(W/'copy_buttons.js').write_text(n.xpath('//script')[0].text,encoding='utf-8')
assert n_ok and cross_ok
print('Article static checks passed')

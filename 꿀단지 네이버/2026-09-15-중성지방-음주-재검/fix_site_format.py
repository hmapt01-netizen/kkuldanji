from pathlib import Path
import json,re,sys,shutil,html
W=Path(__file__).resolve().parent;R=W.parents[1]
sys.path.insert(0,str(R/'codex_tools'))
import workflow_guard as g
from register_post import validate_body_style
p=W/'post_data.json';data=g.read(p)
backup=W/'registration_backup/post_data_before_style.json'
if not backup.exists():shutil.copy2(p,backup)
previous=next(x for x in g.read(R/'data/posts_db.json') if x['slug']=='chuseok-meat-delivery-thawing-safety.html')['bodyHtml']
body=data['bodyHtml']
quote=re.search(r'<blockquote\b[^>]*>',previous)[0]
body=re.sub(r'<blockquote\b[^>]*>',lambda m:quote,body,count=1)
toc_tag=re.search(r'<nav\b[^>]*class="toc-box"[^>]*>',previous)[0]
def contents(m):
    links=re.findall(r'<a\b[^>]*>.*?</a>',m[0],re.S)
    return toc_tag+'<strong>목차</strong><ul style="list-style:none;padding-left:0;">'+''.join('<li style="margin-top:10px;">'+a+'</li>' for a in links)+'</ul></nav>'
body=re.sub(r'<nav\b[^>]*class="toc-box"[^>]*>.*?</nav>',contents,body,flags=re.S)
def photo(m):
    attrs=m[1]; content=m[2]
    if 'post-img-wrap' not in attrs:attrs=' class="post-img-wrap" style="margin:28px 0;text-align:center;"'
    if '<figcaption' not in content:
        alt=re.search(r'alt="([^"]*)"',content)[1]
        content+='<figcaption style="font-size:0.83rem;color:#64748b;margin-top:8px;line-height:1.4;">'+alt+'</figcaption>'
    return '<figure'+attrs+'>'+content+'</figure>'
body=re.sub(r'<figure\b([^>]*)>(.*?)</figure>',photo,body,flags=re.S)
body=re.sub(r'(<h2\b[^>]*>.*?</h2>)(\s*<p\b[^>]*>.*?</p>)(\s*<figure\b[^>]*>.*?</figure>)',r'\1\3\2',body,flags=re.S)
validate_body_style(body)
# Confirm text only changes by adding photo captions and the contents label.
data['bodyHtml']=body
p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
state=g.state_of(W)
receipt=next(x for x in state['receipts'] if x['stage']=='assembly')
g.record(W,'assembly',[x['path'] for x in receipt['artifacts']],'기존 사이트의 인용문·목차·사진 서식 적용. 내용·제목·이미지 유지')
# Obsolete Google previews now lead to the actual template-generated page.
url='../../../kkuldanji_web/posts/'+data['slug']
redirect='<!doctype html><html lang="ko"><meta charset="utf-8"><meta http-equiv="refresh" content="0;url='+url+'"><title>사이트 본문</title><a href="'+url+'">실제 사이트 본문 보기</a></html>'
for name in ('google_with_images.html','google_draft_preview.html'):(W/name).write_text(redirect,encoding='utf-8')
print('Source formatting corrected')

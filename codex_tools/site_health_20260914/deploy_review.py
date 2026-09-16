import json, subprocess, re
from pathlib import Path
from lxml import html
R=Path(__file__).resolve().parents[2]
G='C:/Users/lim/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/git/cmd/git.exe'
def git(*args):return subprocess.check_output([G,*args],cwd=R).decode('utf-8-sig')
def posts(ref):return {p['slug']:p for p in json.loads(git('show',ref+':data/posts_db.json'))}
current={p['slug']:p for p in json.loads((R/'data/posts_db.json').read_text(encoding='utf-8-sig'))}
before=posts('HEAD')
changed=[s for s in current if current[s]!=before.get(s)]
assert set(changed)=={'sleep-hygiene-guide.html','sleep-lying-down-eyes-closed-20min-rule.html'},changed
assert not git('diff','--cached','--name-only').strip(),'Unexpected staged changes'
paths=git('diff','--name-only','--','data/posts_db.json','kkuldanji_web').splitlines()
sel='//div[contains(concat(" ",normalize-space(@class)," ")," article-body-content ")]'
for p in paths:
    if p.startswith('kkuldanji_web/posts/') and Path(p).name not in changed:
        old_text=git('show','HEAD:'+p)
        for s in changed:
            for k in ('title','desc'):
                a,b=before[s].get(k),current[s].get(k)
                if isinstance(a,str) and a and isinstance(b,str):old_text=old_text.replace(a,b)
        old=html.fromstring(old_text); new=html.fromstring((R/p).read_text(encoding='utf-8'))
        assert html.tostring(old.xpath(sel)[0])==html.tostring(new.xpath(sel)[0]),p
prior=posts('f4cd141')
audit_changed=[s for s in current if current[s]!=prior.get(s)]
older=posts('de42656')
earlier_modified=[s for s in current if s in older and current[s]!=older[s]]
new_posts=[s for s in current if s not in older]
report={'pending_content_posts':changed,'adsense_audit_modified_posts':audit_changed,'earlier_and_current_existing_modified_posts':earlier_modified,'modified_fields':{s:[k for k in current[s] if current[s].get(k)!=older[s].get(k)] for s in earlier_modified},'new_posts_since_comment_fix':new_posts,'deploy_files':paths,'other_article_bodies_unchanged':True}
(Path(__file__).parent/'deploy_manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))

"""Publish the reviewed content/site changes; leave unrelated working files alone."""
from pathlib import Path
import subprocess, json, re, hashlib

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
GIT=str(Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/native/git/cmd/git.exe')

def git(*args):
    p=subprocess.run([GIT,*args],cwd=ROOT,capture_output=True)
    out=p.stdout.decode('utf-8','replace')
    if p.returncode:
        err=re.sub(r'https://[^\s/@]+(?::[^\s/@]*)?@','https://[redacted]@',p.stderr.decode('utf-8','replace'))
        raise RuntimeError('git '+args[0]+' failed: '+err)
    return out

assert git('branch','--show-current').strip()=='main'
assert not git('diff','--cached','--name-only').strip(), 'Existing staged work must be preserved'
head=git('rev-parse','HEAD').strip()
remote=git('ls-remote','origin','refs/heads/main').split()[0]
assert head==remote, 'Remote main changed; reconcile before publishing'
changed=git('diff','--name-only','-z').split('\0')
selected=[p for p in changed if p.startswith('kkuldanji_web/')]
assert 'kkuldanji_web/about.html' not in selected, 'Introduction must remain unchanged'
selected += ['data/posts_db.json','tools/build_site.py','tools/site_pagination_guard.py','tools/site_ads_guard.py']
for prefix in ['01_','07_','11_']:
    selected += [p for p in changed if p.startswith('꿀단지 네이버/'+prefix) and p.endswith('.html')]
selected=sorted(set(selected))
assert all((ROOT/p).is_file() for p in selected)
assert all(not p.startswith(('AGENTS','GEMINI','codex_tools/')) for p in selected)
manifest={'base':head,'files':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in selected}}
(OUT/'deploy_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
git('add','--',*selected)
assert set(git('diff','--cached','--name-only','-z').strip('\0').split('\0'))==set(selected)
git('commit','-m','Correct four health articles, disclose contact processing, and guard site builds')
manifest['commit']=git('rev-parse','HEAD').strip()
(OUT/'deploy_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
git('push','origin','main')
assert git('ls-remote','origin','refs/heads/main').split()[0]==manifest['commit']
manifest['pushed']=True
(OUT/'deploy_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('Pushed',manifest['commit'],'files:',len(selected))

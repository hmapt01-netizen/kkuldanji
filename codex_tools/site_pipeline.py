"""Register, build and audit the real site; never deploy remotely."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / 'kkuldanji_web'
REPORT = 'site_registration.json'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def site_files(data):
    slug = data['slug']
    if Path(slug).name != slug or not slug.endswith('.html') or '/' in slug or '\\' in slug:
        raise ValueError('단일 HTML slug 필요')
    return [WEB/'posts'/slug, WEB/'index.html', WEB/'sitemap.xml', WEB/'feed.xml']

def verify(work):
    report = read(work/REPORT)
    data = read(work/'post_data.json')
    if report.get('input_sha256') != digest(work/'post_data.json'):
        raise ValueError('사이트 등록 후 원고 변경: 파이프라인 재실행 필요')
    posts = read(ROOT/'data/posts_db.json')
    matches = [p for p in posts if p.get('slug') == data['slug']]
    if len(matches) != 1 or any(matches[0].get(k) != v for k,v in data.items() if k != 'isLatest'):
        raise ValueError('실제 사이트 DB와 원고 불일치')
    expected = {str(p.relative_to(ROOT)) for p in site_files(data)}
    outputs = report.get('outputs', {})
    if not expected.issubset(outputs):
        raise ValueError('실제 글·홈·사이트맵·피드 등록 증거 누락')
    for name, sha in outputs.items():
        path = (ROOT/name).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file() or digest(path) != sha:
            raise ValueError('사이트 산출물 변경 또는 누락: '+name)
    for name, sha in report.get('images', {}).items():
        if digest(work/'images'/name) != sha:
            raise ValueError('등록 후 이미지 변경: '+name)
    if not report.get('images') or report.get('audit_exit') != 0:
        raise ValueError('이미지·사이트 검사 증거 누락')
    if digest(work/'site_audit.log') != report.get('audit_sha256'):
        raise ValueError('사이트 검사 로그 불일치')
    return REPORT

def run(work):
    import workflow_guard as guard
    from register_post import register
    guard.require_step(work, 'validation')
    before = {p['slug']:p.get('isEditorPick', False) for p in read(ROOT/'data/posts_db.json')}
    data = read(work/'post_data.json')
    if data['slug'] not in before and data.get('isEditorPick') is not False:
        raise ValueError('신규 글 isEditorPick=false 필요')
    register(work, 'post_data.json', 'images')
    after = read(ROOT/'data/posts_db.json')
    if any(p.get('isEditorPick', False) != before[p['slug']] for p in after if p['slug'] in before):
        raise ValueError('기존 에디터 픽 변경 감지')
    audit = subprocess.run([sys.executable, '-B', str(ROOT/'tools/audit_site.py'), '--local'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    (work/'site_audit.log').write_text(audit.stdout+'\n'+audit.stderr, encoding='utf-8')
    if audit.returncode:
        raise ValueError('사이트 검사 실패: site_audit.log 확인. 등록/빌드는 이미 실행됨')
    paths = site_files(data)
    if data['title'] not in paths[0].read_text(encoding='utf-8-sig'):
        raise ValueError('생성 페이지 제목 불일치')
    for p in paths[1:]:
        if data['slug'] not in p.read_text(encoding='utf-8-sig'):
            raise ValueError('새 글 연결 누락: '+p.name)
    image_hashes = {}
    for p in (work/'images').glob('*.jpg'):
        target = WEB/'images/posts'/data.get('slugKey',data['slug'][:-5])/p.name
        if digest(p) != digest(target):
            raise ValueError('사이트 이미지 불일치: '+p.name)
        paths.append(target); image_hashes[p.name] = digest(p)
    report = {'input_sha256':digest(work/'post_data.json'), 'outputs':{str(p.relative_to(ROOT)):digest(p) for p in paths}, 'images':image_hashes, 'audit_exit':0, 'audit_sha256':digest(work/'site_audit.log'), 'scope':'local site registered, built and audited; remote deployment not performed'}
    (work/REPORT).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    verify(work)
    guard.record(work,'validation',[REPORT,'site_audit.log'],'실제 사이트 등록·빌드·로컬 검사 및 이미지 복사 검증 완료')
    print('사이트 등록·빌드·검사 완료. 원격 배포는 별도 단계입니다.')

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--work-dir',type=Path,required=True)
    args=parser.parse_args()
    try:
        run(args.work_dir.resolve())
    except (ValueError, OSError, KeyError, AssertionError) as exc:
        print('사이트 완료 차단: '+str(exc)); sys.exit(2)

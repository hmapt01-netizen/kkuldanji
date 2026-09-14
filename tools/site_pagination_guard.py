"""Required homepage pagination gate; executes site JavaScript offline in Node.

This checks behavior in a small DOM fixture, not browser rendering or all CSS.
Missing tests/runtime, timeouts, or regressions fail closed. No network/install.
"""
from pathlib import Path
import argparse
import os
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
WEB_ROOT = ROOT / 'kkuldanji_web'

class PaginationError(RuntimeError):
    pass

def node_executable():
    name = 'node.exe' if os.name == 'nt' else 'node'
    bundled = Path(sys.executable).resolve().parent.parent / 'node' / 'bin' / name
    if bundled.is_file():
        return str(bundled)
    found = shutil.which('node')
    if found:
        return found
    # 일반 Python으로 실행해도 Codex의 설치된 공용 런타임을 찾는다.
    # sys.executable 옆에만 Node가 있다고 가정하면 일반 터미널에서 실패한다.
    cached = Path.home() / '.cache' / 'codex-runtimes' / 'codex-primary-runtime' / 'dependencies' / 'node' / 'bin' / name
    if cached.is_file():
        return str(cached)
    local_app_data = os.environ.get('LOCALAPPDATA', '')
    if local_app_data:
        codex_nodes = list(Path(local_app_data).glob('OpenAI/Codex/runtimes/cua_node/*/bin/node.exe'))
        if codex_nodes and codex_nodes[0].is_file():
            return str(codex_nodes[0])
    for pf in (os.environ.get('ProgramFiles', ''), os.environ.get('ProgramFiles(x86)', '')):
        if pf:
            cand = Path(pf) / 'nodejs' / name
            if cand.is_file():
                return str(cand)
    raise PaginationError('목록 검사에 필요한 Node.js를 찾지 못했습니다. Node.js 경로를 복구한 뒤 다시 실행하세요. 검사를 생략하지 않습니다.')

def validate(web_root=WEB_ROOT, *, include_generated=True):
    web_root = Path(web_root)
    test = Path(__file__).with_name('home_pagination.test.mjs')
    targets = [web_root / 'templates/index_template.html']
    if include_generated:
        targets.append(web_root / 'index.html')
    css = web_root / 'css/style.css'
    for required in [test, css, *targets]:
        if not required.is_file():
            raise PaginationError('목록 검사 필수 파일 누락: ' + str(required))
    try:
        result = subprocess.run([node_executable(), str(test), str(css), *map(str, targets)],
                                capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=30)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise PaginationError('목록 검사 실행 실패: ' + str(exc)) from exc
    if result.returncode:
        raise PaginationError('6개씩 보기 규칙 위반 또는 검사 오류:\n' + (result.stdout + result.stderr)[-5000:])
    print(result.stdout.strip())

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--web-root', type=Path, default=WEB_ROOT)
    parser.add_argument('--template-only', action='store_true')
    args = parser.parse_args()
    try:
        validate(args.web_root, include_generated=not args.template_only)
    except PaginationError as exc:
        print('[PAGINATION BLOCKED] ' + str(exc))
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())

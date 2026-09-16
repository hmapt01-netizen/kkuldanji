"""Explicit source-access gate. Does not intercept external browser/tool calls."""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import urllib.request

STATE = 'source_access_state.json'
PHASES = ('topic', 'titles', 'research', 'writing')

def read_state(work):
    p = Path(work) / STATE
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else {'phase': 'topic'}

def log(work, action, **fields):
    with (Path(work) / 'source_access_log.jsonl').open('a', encoding='utf-8') as f:
        f.write(json.dumps(dict(at=datetime.now(timezone.utc).isoformat(), action=action, **fields), ensure_ascii=False) + '\n')

def transition(work, phase, note, naver='', google=''):
    state = read_state(work)
    old = state['phase']
    allowed = {'topic': {'titles'}, 'titles': {'research'}, 'research': {'writing'}, 'writing': {'research'}}
    if phase not in allowed.get(old, set()) or not note.strip():
        raise ValueError('잘못된 단계 전환 또는 실제 선택/전환 사유 누락')
    if old == 'titles' and (not naver.strip() or not google.strip()):
        raise ValueError('리서치 진입 전에 사용자가 선택한 네이버·구글 제목 필요')
    if old == 'titles':
        state.update(naver_title=naver, google_title=google)
    if phase == 'writing' and not (Path(work) / 'source_notes.md').is_file():
        raise ValueError('작성 진입 전에 리서치 근거 요약 source_notes.md 필요')
    state.update(phase=phase, note=note)
    (Path(work) / STATE).write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
    log(work, 'transition', previous=old, phase=phase, note=note)

def authorize(work, resource):
    phase = read_state(work)['phase']
    allowed = phase == 'research'
    log(work, 'source_access', phase=phase, resource=resource, allowed=allowed)
    if not allowed:
        raise PermissionError('원문 열람 차단: 리서치 단계에서만 허용됩니다. 현재 단계: ' + phase)

def fetch(work, resource):
    authorize(work, resource)
    if resource.startswith(('https://', 'http://')):
        with urllib.request.urlopen(resource, timeout=30) as response:
            return response.read().decode('utf-8', errors='replace')
    return Path(resource).read_text(encoding='utf-8-sig')

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--work-dir', required=True, type=Path)
    p.add_argument('action', choices=('status', 'transition', 'check', 'read'))
    p.add_argument('--phase', choices=PHASES)
    p.add_argument('--note', default='')
    p.add_argument('--naver-title', default='')
    p.add_argument('--google-title', default='')
    p.add_argument('--resource', default='')
    a = p.parse_args()
    if not a.work_dir.is_dir():
        p.error('실제 작업 폴더 필요')
    try:
        if a.action == 'transition':
            transition(a.work_dir, a.phase, a.note, a.naver_title, a.google_title)
        elif a.action in ('check', 'read'):
            if not a.resource:
                raise ValueError('원문 URL 또는 경로 필요')
            if a.action == 'read':
                print(fetch(a.work_dir, a.resource))
            else:
                authorize(a.work_dir, a.resource)
        print(json.dumps(read_state(a.work_dir), ensure_ascii=False))
        return 0
    except (ValueError, OSError) as exc:
        print(str(exc))
        return 2

if __name__ == '__main__':
    raise SystemExit(main())

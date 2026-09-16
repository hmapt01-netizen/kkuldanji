"""Codex-only research handoff checks; no search or shared-file mutations."""
import argparse
import hashlib
import json
from pathlib import Path

STAGES = ('research', 'naver_titles', 'google_titles', 'draft')
REASONS = {'missing', 'conflict', 'scope_change', 'freshness', 'channel_serp'}


def filename(stage):
    return f'codex_reuse/{stage}.json'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def local(work, name):
    path = (work / name).resolve()
    if not path.is_relative_to(work.resolve()) or not path.is_file():
        raise ValueError('자료 인계: 작업 폴더 내 실제 근거 파일 필요: ' + name)
    return path


def selections(work, stage):
    from workflow_guard import STEPS, STATE
    state = read(work / STATE) if (work / STATE).exists() else {}
    return {r['stage']: r['selected_title'] for r in state.get('receipts', [])
            if r.get('stage') in ('naver_selection', 'google_selection')
            and STEPS.index(r['stage']) < STEPS.index(stage)}


def evidence(work, row):
    path = local(work, row.get('path', ''))
    if hashlib.sha256(path.read_bytes()).hexdigest() != row.get('sha256'):
        raise ValueError('자료 인계: 근거 변경 재검토 필요: ' + row['path'])
    excerpt = row.get('excerpt', '').strip()
    if not excerpt or excerpt not in path.read_text(encoding='utf-8-sig'):
        raise ValueError('자료 인계: 파일에서 확인 가능한 관련 발췌 필요')
    return row['path']


def validate(work, stage, *, complete=False):
    if stage not in STAGES:
        return []
    name = filename(stage)
    if not (work / name).is_file():
        raise ValueError('자료 인계 누락: ' + name + ' (reuse_guard.py init 사용)')
    data = read(local(work, name))
    if data.get('version') != 1 or data.get('stage') != stage:
        raise ValueError('자료 인계: 버전/단계 불일치')
    if data.get('selected_titles') != selections(work, stage):
        raise ValueError('자료 인계: 현재 사용자 선택 제목과 불일치')
    if not data.get('intent', '').strip():
        raise ValueError('자료 인계: 이번 단계의 검색 의도/답변 범위 필요')
    files = [name]
    reviewed = data.get('reviewed_existing', [])
    for row in reviewed:
        files.append(evidence(work, row))
    if not reviewed and not data.get('no_existing_reason', '').strip():
        raise ValueError('자료 인계: 기존 근거 확인 기록 또는 없는 이유 필요')
    questions = data.get('questions', [])
    if not questions:
        raise ValueError('자료 인계: 이번 단계에서 답할 질문 필요')
    for q in questions:
        if not q.get('question', '').strip():
            raise ValueError('자료 인계: 빈 질문 불가')
        mode = q.get('mode')
        if mode not in ('reuse', 'additional', 'exclude'):
            raise ValueError('자료 인계: 재사용/추가 조사/제외 판단 필요')
        if mode in ('additional', 'exclude') and not q.get('reason', '').strip():
            raise ValueError('자료 인계: 추가 조사 또는 제외 이유 필요')
        if mode == 'additional' and q.get('reason_type') not in REASONS:
            raise ValueError('자료 인계: 부족/충돌/범위 변경/최신성/채널 확인 사유 필요')
        refs = q.get('evidence', [])
        for row in refs:
            files.append(evidence(work, row))
        if mode == 'reuse' and (not reviewed or not refs):
            raise ValueError('자료 인계: 재사용할 실제 근거 연결 필요')
        if complete and mode != 'exclude':
            if not refs or not q.get('answer', '').strip() or not q.get('limits', '').strip():
                raise ValueError('자료 인계: 답변 요지·저장 근거·적용 조건/한계 필요')
            if stage == 'draft' and not q.get('body_location', '').strip():
                raise ValueError('자료 인계: 본문에서 답한 위치 필요')
    if complete and all(q['mode'] == 'exclude' for q in questions):
        raise ValueError('자료 인계: 모든 질문을 제외하여 완료할 수 없음')
    return list(dict.fromkeys(files))


def init(work, stage, questions):
    """Create an unfinished plan; never invent review or completion evidence."""
    path = work / filename(stage)
    path.parent.mkdir(exist_ok=True)
    data = {'version': 1, 'stage': stage, 'selected_titles': selections(work, stage),
            'intent': '', 'reviewed_existing': [], 'no_existing_reason': '',
            'questions': [{'question': q, 'mode': '', 'reason_type': '', 'reason': '',
                           'answer': '', 'limits': '', 'body_location': '', 'evidence': []}
                          for q in questions]}
    with path.open('x', encoding='utf-8') as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work-dir', required=True, type=Path)
    parser.add_argument('action', choices=('init', 'check', 'ref'))
    parser.add_argument('--stage', choices=STAGES)
    parser.add_argument('--question', action='append', default=[])
    parser.add_argument('--complete', action='store_true')
    parser.add_argument('--file')
    parser.add_argument('--excerpt')
    args = parser.parse_args()
    work = args.work_dir.resolve()
    try:
        if not work.is_dir():
            raise ValueError('실제 작업 폴더 필요')
        if args.action == 'ref':
            if not args.file or not args.excerpt:
                raise ValueError('--file 및 실제 --excerpt 필요')
            path = local(work, args.file)
            row = {'path': str(path.relative_to(work)).replace('\\', '/'),
                   'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                   'excerpt': args.excerpt}
            evidence(work, row)
            print(json.dumps(row, ensure_ascii=False))
        elif args.stage is None:
            raise ValueError('--stage 필요')
        elif args.action == 'init':
            if not args.question or any(not q.strip() for q in args.question):
                raise ValueError('--question으로 실제 답할 질문 필요')
            print(init(work, args.stage, args.question))
        else:
            print(json.dumps(validate(work, args.stage, complete=args.complete), ensure_ascii=False))
        return 0
    except (ValueError, KeyError, TypeError, AttributeError, OSError) as exc:
        print('자료 인계 보완 필요: ' + str(exc))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())

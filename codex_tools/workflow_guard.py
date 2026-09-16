"""Codex-only workflow receipts. Never changes or replaces shared validators."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from blue_ocean import audit_errors, evaluate, recent

STEPS = ('naver_titles', 'naver_selection', 'google_titles',
         'google_selection', 'research', 'draft', 'image_plan', 'image_approval', 'assembly',
         'validation', 'publish_approval', 'published')
WAITS = {'naver_selection', 'google_selection', 'image_approval', 'publish_approval'}
STATE = 'codex_workflow.json'
DRAFTS = ('naver_draft.md', 'google_draft.md')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def artifact_digest(path, stage):
    if path.name == 'image_plan.json':
        data = read(path)
        # Approval is recorded separately; changing any actual plan content
        # still invalidates the plan receipt and its approval.
        data.pop('is_user_approved', None)
        return hashlib.sha256(json.dumps(data, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    if path.name == 'codex_target.json':
        data = read(path)
        channel = 'google' if stage == 'google_titles' else 'naver'
        data = {k: data.get(k) for k in ('site_fit', 'site_fit_reason')} | {
            'channel': data.get('channels', {}).get(channel)}
        return hashlib.sha256(json.dumps(data, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    return digest(path)


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def inside(work, name):
    path = (work / name).resolve()
    if not path.is_relative_to(work.resolve()) or not path.is_file():
        raise ValueError(f'작업 폴더 내 실제 파일 필요: {name}')
    return path


def titles_check(data, channel):
    from title_adapter import check_titles
    return check_titles(data, channel)


def research_check(work, channel='naver'):
    inside(work, '리서치.md')
    target = read(inside(work, 'codex_target.json'))
    spec = target['channels'][channel]
    evidence = read(inside(work, spec['evidence_file']))
    errors = audit_errors(evidence)
    if errors:
        raise ValueError('근거 검토 복귀: ' + '; '.join(errors))
    if evidence.get('channel') != channel:
        raise ValueError('조사 채널 불일치')
    matches = [r for r in evidence['records'] if r.get('clean_query') == spec['query']]
    if len(matches) != 1 or not evaluate(matches[0])['evidence_complete']:
        raise ValueError('공략 질문의 실제 비교 근거 필요. 완전한 블루오션일 필요는 없음')
    if target.get('site_fit') not in ('core', 'relevant_extension') or not target.get('site_fit_reason'):
        raise ValueError('꿀단지 적합성 근거 필요')
    terms = spec.get('intent_terms', [])
    scope = spec['query'] + ' ' + matches[0]['review']['reader_question']
    if len(set(terms)) < 2 or any(not t.strip() or t not in scope for t in terms):
        raise ValueError('조사 질문에 실제 포함된 대상·상황 핵심어 2개 이상 필요')
    return spec


def validate_artifacts(work, stage, artifacts):
    if stage in ('naver_titles', 'google_titles'):
        channel = stage.split('_')[0]
        filename = channel + '_candidates.json'
        if filename not in artifacts:
            raise ValueError('제목 후보 파일 필요')
        titles_check(read(inside(work, filename)), channel)
        for name in artifacts:
            inside(work, name)
        return
    if stage == 'validation' and 'site_registration.json' in artifacts:
        from site_pipeline import verify
        verify(work)
    from reuse_guard import STAGES as REUSE_STAGES, filename, validate as validate_reuse
    # Pre-existing receipts remain valid; all newly recorded protected stages
    # include this manifest and its evidence through record().
    if stage in REUSE_STAGES and filename(stage) in artifacts:
        if not set(validate_reuse(work, stage, complete=True)).issubset(artifacts):
            raise ValueError('자료 인계 근거를 완료 해시에 포함하세요')
    from freshness_guard import PROTECTED, validate as validate_freshness
    if stage in PROTECTED:
        needed = validate_freshness(work)
        if not set(needed).issubset(artifacts):
            raise ValueError('최신성 검토와 원문 확인 기록을 완료 해시에 포함하세요')
    for name in artifacts:
        inside(work, name)
    if not artifacts:
        raise ValueError('완료 증거 파일 필요')
    if stage == 'draft':
        if not set(DRAFTS).issubset(artifacts):
            raise ValueError('이미지 계획 전에 네이버·구글 본문 초안 파일 모두 필요')
        selections = {r['stage']: r.get('selected_title', '')
                      for r in state_of(work).get('receipts', [])}
        for channel, filename in zip(('naver', 'google'), DRAFTS):
            lines = inside(work, filename).read_text(encoding='utf-8-sig').strip().splitlines()
            title = selections.get(channel + '_selection')
            if not lines or not title or lines[0].lstrip('# ').strip() != title:
                raise ValueError('본문 초안 첫 줄에 확정된 채널 제목 필요: ' + filename)
            body = '\n'.join(lines[1:]).strip()
            if not body or all(line.lstrip().startswith('#') or not line.strip() for line in lines[1:]):
                raise ValueError('제목·목차만으로 본문 초안 완료 처리 불가: ' + filename)
    if stage == 'image_plan':
        if not {'image_plan.json', *DRAFTS}.issubset(artifacts):
            raise ValueError('이미지 계획과 기준이 된 두 본문 초안을 함께 기록하세요')
        from image_guard import validate_image_plan
        if not validate_image_plan(str(work), require_approval=False):
            raise ValueError('기존 이미지 계획 검사 실패')
    if stage == 'assembly':
        required = {'post_data.json', 'naver_final.md'}
        from image_guard import REQUIRED_SLOTS, validate_image_plan, validate_images
        required.update('images/' + slot for slot in REQUIRED_SLOTS)
        normalized = {str(p).replace('\\', '/') for p in artifacts}
        if not required.issubset(normalized):
            raise ValueError('이미지 배치 완료 원고 두 채널과 실제 이미지 6장 필요')
        if not validate_image_plan(str(work), require_approval=True) or not validate_images(str(work / 'images')):
            raise ValueError('기존 이미지 승인·파일 검사 실패')
    if stage == 'research':
        spec = research_check(work)
        required = {'리서치.md', 'codex_target.json', spec['evidence_file']}
        if not required.issubset(artifacts):
            raise ValueError('리서치·공략 질문·실사 파일 모두 완료 기록에 포함해야 함')
    if stage in ('naver_titles', 'google_titles'):
        channel = stage.split('_')[0]
        filename = channel + '_candidates.json'
        report_name = channel + '_report.md'
        required = {filename, channel + '_serp_audit.json', report_name, channel + '_related_keywords.json'}
        if not required.issubset(artifacts):
            raise ValueError('후보·후보별 실사·전체 답변 파일 모두 필요')
        from title_adapter import candidate_records, assessed
        records = candidate_records(work, read(inside(work, filename)), channel)
        compared = {r['clean_query'] for r in records if assessed(r)[0].get('comparison_ready', assessed(r)[0]['evidence_complete'])}
        if len(compared) < 2:
            raise ValueError('상대 비교할 검색어 최소 2개의 실제 검토 필요. 미확인 후보는 점수 없이 표시')
        from report_guard import check_report
        check_report(work, channel, inside(work, report_name))


def state_of(work):
    path = work / STATE
    return read(path) if path.exists() else {'version': 3, 'receipts': []}


def migrate_draft_first(work):
    """Explicit migration of pre-draft work only; preserve all selections/files."""
    state = state_of(work)
    if state.get('version', 1) == 2:
        return
    receipts = state.get('receipts', [])
    prefix = STEPS[:5]
    if any(r.get('stage') != prefix[i] for i, r in enumerate(receipts[:5])):
        raise ValueError('이전 제목 단계 순서 확인 필요')
    tail = receipts[5:]
    if tail and [r.get('stage') for r in tail] != ['image_plan']:
        raise ValueError('이미 승인·작성된 작업은 자동 이전하지 않습니다. 기존 산출물 대조 필요')
    backup = work / 'codex_workflow.before_draft_first.json'
    if backup.exists():
        raise ValueError('이전 백업이 이미 존재합니다. 덮어쓰지 않습니다')
    backup.write_bytes((work / STATE).read_bytes())
    if tail:
        state.setdefault('superseded', []).append(tail)
    state.update(version=2, receipts=receipts[:5])
    state['order_change'] = '본문 초안 먼저. 기존 이미지 계획은 참고안이며 본문 기준 재검토 필요.'
    (work / STATE).write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')


def next_step(work, state):
    receipts = state.get('receipts', [])
    for i, stage in enumerate(STEPS):
        if i >= len(receipts):
            return stage, ''
        receipt = receipts[i]
        try:
            if receipt['stage'] != stage or not receipt.get('note'):
                raise ValueError('순서/완료 근거 누락')
            for item in receipt['artifacts']:
                if artifact_digest(inside(work, item['path']), stage) != item['sha256']:
                    raise ValueError('완료 뒤 파일 변경: ' + item['path'])
            if stage not in WAITS:
                validate_artifacts(work, stage, [x['path'] for x in receipt['artifacts']])
            elif not receipt.get('user_message'):
                raise ValueError('실제 사용자 선택/승인 발언 누락')
        except (ValueError, KeyError, TypeError, OSError) as exc:
            return stage, str(exc)
    return 'complete', ''


def require_step(work, stage, allowed=()):
    """Called inside execution entry points, before network/write side effects."""
    expected, problem = next_step(work, state_of(work))
    if stage == 'research':
        from source_access_guard import read_state
        if read_state(work)['phase'] != 'research':
            raise ValueError('원문 조사 전에 source_access_guard의 research 단계 진입 필요')
    if expected not in (stage, *allowed):
        raise ValueError(f'실행 차단: {stage} 선행 단계 미완료. 복귀 단계: {expected}. {problem}')
    from freshness_guard import ENTRY_STAGES, validate as validate_freshness
    if stage in ENTRY_STAGES and stage not in ('naver_titles', 'google_titles'):
        validate_freshness(work)
    # A report can be rechecked while waiting for a selection. Recheck the
    # completed receipt there rather than demand a new research plan.
    if expected == stage and stage not in ('naver_titles', 'google_titles'):
        from reuse_guard import validate as validate_reuse
        validate_reuse(work, stage)
    return expected


def record(work, stage, artifacts, note, user_message='', selected_title=''):
    state = state_of(work)
    from source_access_guard import read_state
    phase = read_state(work)['phase']
    if stage == 'research' and phase != 'research':
        raise ValueError('리서치 완료 기록은 research 단계에서만 가능')
    if stage == 'draft' and phase != 'writing':
        raise ValueError('원문 열람을 닫고 writing으로 전환한 뒤 초안 기록')
    expected, problem = next_step(work, state)
    if stage != expected:
        raise ValueError(f'단계 건너뛰기 차단. 복귀 단계: {expected}. {problem}')
    if not note.strip():
        raise ValueError('실제로 수행·제시한 내용의 기록 필요')
    if stage == 'draft' and not (work / 'post_data.json').is_file():
        raise ValueError('새 본문은 사이트용 post_data.json부터 작성하세요. 미리보기만으로 초안 완료 불가')
    if stage == 'draft':
        site_draft = read(work / 'post_data.json')
        google_title = next((r.get('selected_title') for r in state.get('receipts', []) if r['stage'] == 'google_selection'), None)
        if site_draft.get('title') != google_title or not str(site_draft.get('bodyHtml', '')).strip():
            raise ValueError('사이트용 초안에 확정 구글 제목과 실제 bodyHtml 본문 필요')
    if stage == 'validation':
        from site_pipeline import verify, REPORT
        verify(work)
        artifacts = list(dict.fromkeys([*artifacts, REPORT, 'site_audit.log']))
    from freshness_guard import ENTRY_STAGES, validate as validate_freshness
    if stage in ENTRY_STAGES and stage not in ('naver_titles', 'google_titles'):
        artifacts = list(dict.fromkeys([*artifacts, *validate_freshness(work)]))
    from reuse_guard import validate as validate_reuse
    if stage not in ('naver_titles', 'google_titles'):
        artifacts = list(dict.fromkeys([*artifacts, *validate_reuse(work, stage, complete=True)]))
    if stage in WAITS:
        if not user_message.strip():
            raise ValueError('실제 사용자 발언 필요. AI가 선택/승인을 만들어서는 안 됨')
        if stage.endswith('_selection'):
            channel = stage.split('_')[0]
            if selected_title not in titles_check(read(inside(work, channel + '_candidates.json')), channel):
                raise ValueError('현재 제시된 후보 중 사용자가 선택한 제목 필요')

    else:
        validate_artifacts(work, stage, artifacts)
    receipt = {'stage': stage, 'note': note, 'user_message': user_message,
               'selected_title': selected_title, 'at': datetime.now().astimezone().isoformat(),
               'artifacts': [{'path': str(inside(work, p).relative_to(work)),
                              'sha256': artifact_digest(inside(work, p), stage)} for p in artifacts]}
    # Invalidate descendants after a changed artifact; never delete the work files.
    previous = state.get('receipts', [])
    cutoff = STEPS.index(stage)
    if len(previous) > cutoff:
        state.setdefault('superseded', []).append(previous[cutoff:])
    state['receipts'] = previous[:cutoff] + [receipt]
    (work / STATE).write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work-dir', required=True, type=Path)
    parser.add_argument('action', choices=('status', 'check', 'record', 'finish', 'migrate-draft-first'))
    parser.add_argument('--stage', choices=STEPS)
    parser.add_argument('--artifact', action='append', default=[])
    parser.add_argument('--note', default='')
    parser.add_argument('--user-message', default='')
    parser.add_argument('--selected-title', default='')
    parser.add_argument('--reply-file')
    args = parser.parse_args()
    work = args.work_dir.resolve()
    if not work.is_dir():
        parser.error('실제 작업 폴더를 지정하세요')
    try:
        if args.action == 'migrate-draft-first':
            migrate_draft_first(work)
        expected, problem = next_step(work, state_of(work))
        if args.action == 'record':
            record(work, args.stage, args.artifact, args.note, args.user_message, args.selected_title)
            expected, problem = next_step(work, state_of(work))
        elif args.action == 'check' and args.stage != expected:
            raise ValueError(f'단계 건너뛰기 차단. 복귀 단계: {expected}')
        elif args.action == 'check':
            require_step(work, args.stage)
        elif args.action == 'finish' and expected not in WAITS and expected != 'complete':
            raise ValueError(f'임의 종료 차단. 같은 작업을 계속하세요. 복귀 단계: {expected}. {problem}')
        if args.action == 'finish' and expected in ('naver_selection', 'google_selection'):
            if not args.reply_file:
                raise ValueError('최종 답변 누락 차단: --reply-file로 실제 제시할 전체 답변 파일을 지정하세요')
            reply = inside(work, args.reply_file)
            print('validated_reply=' + str(reply) + ' sha256=' + digest(reply))
        print(json.dumps({'next': expected, 'mode': 'wait_user' if expected in WAITS else
                          'complete' if expected == 'complete' else 'continue',
                          'reason': problem}, ensure_ascii=False))
        return 0
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print('복귀 필요: ' + str(exc))
        return 2


if __name__ == '__main__':
    sys.exit(main())

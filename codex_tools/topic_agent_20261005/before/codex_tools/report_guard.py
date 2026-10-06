"""Render and validate the complete Codex title reply against reviewed evidence."""
import argparse
from pathlib import Path
import sys


def cell(value):
    return str(value).replace('|', '&#124;').replace('\r', ' ').replace('\n', ' ')


def render(records, channel):
    from title_adapter import assessed, comparison_key
    label = '네이버' if channel == 'naver' else '구글'
    lines = [f'{label} 제목 후보 10개입니다. 공백·문장부호 포함 40~60자입니다.', '',
             '| 번호 | 후보 제목 | 글자 수 | 공략 검색어 | 규칙 점수 | 경쟁도 | 실사 근거 |',
             '|---|---|---|---|---|---|---|']
    evaluated = []
    for record in records:
        result, score = assessed(record)
        evaluated.append((record, result, score))
        counts = result.get('coverage_counts')
        evidence = (f"직접 {counts['direct']} / 일부 {counts['partial']} / 무관 {counts['unrelated']}. "
                    if counts else '') + result['reason']
        points = f'{score}/100' if score is not None else '미확인'
        reviewed = result.get('comparison_ready', result['evidence_complete'])
        judgement = record.get('review') if result['evidence_complete'] else record.get('title_review', {})
        evidence = (result.get('review_scope', '') + '. ' if result.get('review_scope') else '') + evidence
        competition = {'gap': '블루오션 후보', 'medium': '중간 경쟁', 'high': '레드오션'}.get(judgement.get('competition'), '') if reviewed else ''
        badge = {'gap': '🟢 상대적 틈새', 'medium': '🟡 비교 후보', 'high': '🔴 경쟁 높음'}.get(judgement.get('competition'), result['badge']) if reviewed else result['badge']
        lines.append(f"| {record['idx']} | {cell(record['title'])} | {len(record['title'].strip())}자 | {cell(record['clean_query'])} | {points} | {competition} {badge} | {cell(evidence)} |")
    ranked = sorted((item for item in evaluated if item[1].get('comparison_ready', item[1]['evidence_complete'])),
                    key=lambda item: comparison_key(item[0]))
    picks, seen = [], set()
    for item in ranked:
        if item[0]['clean_query'] not in seen:
            picks.append(item)
            seen.add(item[0]['clean_query'])
        if len(picks) == 3:
            break
    lines += ['', '**저지수 블로그 추천 — 서로 다른 공략 검색어 기준**', '']
    for n, (record, result, score) in enumerate(picks, 1):
        lines.append(f"- {n}픽: **{record['idx']}번** — {result['reason']}")
    if not picks:
        lines.append('비교 근거가 확인된 후보가 없어 추천을 보류합니다.')
    lines += ['', '경쟁도는 수집 결과와 접근 가능한 본문을 기준으로 한 상대 평가입니다. 미열람 문서와 실제 검색량은 확인되지 않았습니다. 추천은 상대적 경쟁 강도, 확인한 본문의 직접 답변 비중, 규칙 점수 순입니다. 완전한 블루오션만 고르는 방식은 아닙니다. 규칙 점수는 검색량·상위 노출 확률이 아닙니다. 같은 검색어의 후보는 조사 근거를 공유하며 미확인 후보에는 점수를 부여하지 않습니다.',
              '', '원하시는 제목 번호를 선택해 주세요.']
    return '\n'.join(lines) + '\n'


def expected_report(work, channel):
    import workflow_guard as g
    from title_adapter import candidate_records
    data = g.read(g.inside(work, channel + '_candidates.json'))
    return render(candidate_records(work, data, channel), channel)


def build_report(work, channel, path):
    from workflow_guard import require_step
    require_step(work, channel + '_titles', allowed=(channel + '_selection',))
    if not path.resolve().is_relative_to(work.resolve()):
        raise ValueError('작업 폴더 내 답변 파일 필요')
    text = expected_report(work, channel)
    path.write_text(text, encoding='utf-8')
    check_report(work, channel, path)


def check_report(work, channel, path):
    expected = expected_report(work, channel)
    actual = path.read_text(encoding='utf-8-sig').replace('\r\n', '\n')
    if actual != expected:
        required = ('| 번호 | 후보 제목 | 글자 수 | 공략 검색어 | 규칙 점수 | 경쟁도 | 실사 근거 |',
                    '**저지수 블로그 추천 — 서로 다른 공략 검색어 기준**')
        missing = [item for item in required if item not in actual]
        detail = '필수 항목 누락: ' + ', '.join(missing) if missing else '제목·글자 수·판정표·추천 근거의 누락 또는 변경'
        raise ValueError('최종 답변 검증 실패. ' + detail + '. 보고서를 다시 생성하고 전체 내용을 사용하세요')


def main():
    import workflow_guard as g
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=('build', 'check'))
    parser.add_argument('--work-dir', required=True, type=Path)
    parser.add_argument('--channel', required=True, choices=('naver', 'google'))
    parser.add_argument('--reply-file')
    args = parser.parse_args()
    work = args.work_dir.resolve()
    path = (work / (args.reply_file or args.channel + '_report.md')).resolve()
    try:
        if not path.is_relative_to(work) or path.suffix != '.md':
            raise ValueError('작업 폴더 안의 Markdown 답변 파일 필요')
        if args.action == 'build':
            build_report(work, args.channel, path)
        check_report(work, args.channel, path)
        print('validated_reply=' + str(path))
        print('sha256=' + g.digest(path))
        print('제목 제안 시 이 파일 전체를 최종 답변으로 그대로 사용하세요.')
        return 0
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print('복귀 필요: ' + str(exc))
        return 2


if __name__ == '__main__':
    sys.exit(main())

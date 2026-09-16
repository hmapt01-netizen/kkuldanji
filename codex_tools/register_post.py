"""Codex registration entry point; preserve the existing registration guards."""
import argparse
from pathlib import Path
import sys
import re
import workflow_guard as guard


def validate_body_style(body):
    """Check the existing site's quote, contents and photo conventions."""
    match = re.search(r'<(?:blockquote|div|section)\b[^>]*class="[^"]*\blead-quote-card\b[^"]*"[^>]*>(.*?)</(?:blockquote|div|section)>', body, re.S)
    if not match:
        raise ValueError('본문 서식: lead-quote-card 핵심 요약 카드 필요')
    quote_content = match.group(1).strip()
    if re.search(r'[가-힣A-Za-z0-9]+\s*(?:연구팀|추진단)', quote_content):
        raise ValueError('본문 서식: lead-quote-card 가공 하위 조직명 사용 금지')
    toc = re.search(r'<nav\b[^>]*class="[^"]*\btoc-box\b[^>]*>(.*?)</nav>', body, re.S)
    if not toc or not all(re.search(pattern, toc[1]) for pattern in (r'<strong>목차</strong>', r'<ul\b', r'<li\b')):
        raise ValueError('본문 서식: 제목·목록을 갖춘 기존 목차 필요')
    figures = list(re.finditer(r'<figure\b([^>]*)>(.*?)</figure>', body, re.S))
    if len(figures) < 5:
        raise ValueError('본문 서식: 본문 화보 5장 필요')
    for fig in figures:
        if not re.search(r'class="[^"]*\bpost-img-wrap\b', fig[1]) or not re.search(r'<figcaption\b[^>]*>\s*[^<\s]', fig[2]):
            raise ValueError('본문 서식: 사진 클래스 또는 설명문 누락')
        if not re.search(r'</h2>\s*$', body[:fig.start()]):
            raise ValueError('본문 서식: 사진은 소제목 바로 아래 배치')


def existing_register(work, data, images):
    import step_guard
    from add_post import add_post
    old_locator = step_guard.get_latest_work_dir
    try:
        step_guard.get_latest_work_dir = lambda: str(work)
        return add_post(data, image_dir=str(images) if images else None)
    finally:
        step_guard.get_latest_work_dir = old_locator


def preflight(work, post_file, image_dir=None):
    guard.require_step(work, 'validation')
    data = guard.read(guard.inside(work, post_file))
    validate_body_style(data.get('bodyHtml', ''))
    selection = next(r for r in guard.state_of(work)['receipts'] if r['stage'] == 'google_selection')
    if data.get('title') != selection['selected_title']:
        raise ValueError('등록 제목과 사용자가 선택한 구글 제목 불일치')
    images = (work / image_dir).resolve() if image_dir else None
    if images and (not images.is_relative_to(work.resolve()) or not images.is_dir()):
        raise ValueError('작업 폴더 내 실제 이미지 폴더 필요')

    tools_dir = str(guard.ROOT / 'tools')
    if tools_dir not in sys.path:
        sys.path.insert(0, tools_dir)
    try:
        import evidence_guard
        evidence_guard.validate_post_evidence(data, work_dir=str(work))
    except Exception as e:
        raise ValueError(f'Evidence Guard 검증 실패: {e}')
    import step_guard
    old_locator = step_guard.get_latest_work_dir
    try:
        step_guard.get_latest_work_dir = lambda: str(work)
        step_guard.check_step(4)
    finally:
        step_guard.get_latest_work_dir = old_locator
    return data, images


def register(work, post_file, image_dir=None):
    data, images = preflight(work, post_file, image_dir)
    if not existing_register(work, data, images):
        raise ValueError('기존 등록/빌드 검사 실패. 완료 처리하지 않음')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--work-dir', required=True, type=Path)
    p.add_argument('--post-file', required=True)
    p.add_argument('--image-dir')
    p.add_argument('--check-only', action='store_true')
    args = p.parse_args()
    try:
        if args.check_only:
            preflight(args.work_dir.resolve(), args.post_file, args.image_dir)
            print('실제 작업 등록 전 검사 통과. DB 쓰기·빌드·배포 미실행.')
        else:
            register(args.work_dir.resolve(), args.post_file, args.image_dir)
        return 0
    except (ValueError, KeyError, StopIteration, OSError, AssertionError) as exc:
        print('등록 차단: ' + str(exc))
        return 2


if __name__ == '__main__':
    sys.exit(main())

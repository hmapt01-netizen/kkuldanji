"""Validate dated research records; observations still require human/source review."""
import argparse
from datetime import date, datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse

MANIFEST = 'freshness_review.json'
PROTECTED = {'draft', 'assembly', 'validation', 'publish_approval', 'published'}
ENTRY_STAGES = PROTECTED | {'research', 'naver_titles', 'google_titles'}


def today():
    return datetime.now(timezone(timedelta(hours=9))).date()


def window_start(day):
    month = day.year * 12 + day.month - 1 - 2
    return date(month // 12, month % 12 + 1, 1)


def iso(value):
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        raise ValueError('날짜는 실제 YYYY-MM-DD 값이어야 합니다') from None


def url(value):
    parsed = urlparse(value or '')
    if parsed.scheme not in ('http', 'https') or not parsed.hostname:
        raise ValueError('실제 출처/검색 URL 필요')


def evidence(work, row):
    name = row.get('evidence_file', '')
    path = (work / name).resolve()
    if not name or not path.is_relative_to(work.resolve()) or not path.is_file():
        raise ValueError('작업 폴더 내 검색 결과/원문 확인 기록 필요')
    if hashlib.sha256(path.read_bytes()).hexdigest() != row.get('evidence_sha256'):
        raise ValueError('검색 결과/원문 확인 기록 해시 불일치')
    quote = row.get('evidence_excerpt', '').strip()
    if not quote or quote not in path.read_text(encoding='utf-8-sig'):
        raise ValueError('확인 기록에 실제 존재하는 근거 발췌 필요')
    return name


def validate(work, day=None):
    work = Path(work).resolve()
    day = day or today()
    path = work / MANIFEST
    if not path.is_file():
        raise ValueError('최신성 검토 누락: freshness_review.json을 작성하세요')
    data = json.loads(path.read_text(encoding='utf-8-sig'))
    if data.get('schema_version') != 1 or iso(data.get('checked_on')) != day:
        raise ValueError('오늘 기준 최신성 재검토 기록 필요')
    start = window_start(day)
    files = {MANIFEST}
    searches = data.get('searches', [])
    if not searches or not data.get('sources'):
        raise ValueError('최근 자료 검색과 채택 자료 기록 모두 필요')
    recent_searches = set()
    checks = set()
    ids = set()
    for row in searches:
        sid = row.get('id')
        if not sid or sid in ids or not row.get('query', '').strip():
            raise ValueError('고유 검색 ID와 실제 검색어 필요')
        ids.add(sid)
        url(row.get('url'))
        if iso(row.get('searched_on')) != day:
            raise ValueError('검색 기록은 오늘 조회한 결과여야 합니다')
        files.add(evidence(work, row))
        if row.get('purpose') == 'recent_discovery':
            if iso(row.get('from')) != start or iso(row.get('to')) != day:
                raise ValueError('당월과 직전 두 달의 실제 검색 기간 필요')
            if row.get('channel') not in ('google', 'naver'):
                raise ValueError('검색 채널 명시 필요')
            recent_searches.add(row['channel'])
        elif row.get('purpose') == 'validity_check':
            if not row.get('result', '').strip():
                raise ValueError('과거 자료 유효성 검색 결과 필요')
            checks.add(sid)
        elif row.get('purpose') != 'current_serp':
            raise ValueError('검색 목적 구분 필요')
    if 'google' not in recent_searches:
        raise ValueError('구글 본진의 최근 3개월 자료 검색 누락')
    source_ids = set()
    fact_ids = set()
    for row in data['sources']:
        sid = row.get('id')
        if not sid or sid in source_ids or not row.get('title', '').strip():
            raise ValueError('고유 자료 ID와 제목 필요')
        source_ids.add(sid)
        url(row.get('url'))
        files.add(evidence(work, row))
        if iso(row.get('accessed_on')) != day:
            raise ValueError('자료 조회일은 오늘이어야 합니다')
        role = row.get('role')
        if role not in ('fact', 'reader_question', 'competitor'):
            raise ValueError('본문 근거/독자 질문/경쟁 문서 역할 구분 필요')
        if role == 'fact':
            fact_ids.add(sid)
        published = iso(row['published_on']) if row.get('published_on') else None
        updated = iso(row['updated_on']) if row.get('updated_on') else None
        if any(d and d > day for d in (published, updated)):
            raise ValueError('미래 발행·수정일은 채택할 수 없습니다')
        if published and updated and updated < published:
            raise ValueError('수정일이 발행일보다 빠릅니다')
        if updated and row.get('substantive_update') is True:
            if not row.get('update_note', '').strip():
                raise ValueError('실질적인 수정 내용 확인 필요')
            effective = updated
        else:
            effective = published
        if effective:
            marker = row.get('date_evidence', '').strip()
            if not marker or marker not in (work / row['evidence_file']).read_text(encoding='utf-8-sig'):
                raise ValueError('발행·수정일을 확인한 원문 기록 필요')
        elif row.get('date_status') != 'unknown':
            raise ValueError('발행일 미확인 자료는 unknown 표시 필요')
        if not effective or effective < start:
            if not row.get('exception_reason', '').strip():
                raise ValueError('과거/날짜 미확인 자료 사용 이유 누락')
            if role == 'competitor':
                if row.get('current_serp_search_id') not in {s['id'] for s in searches if s.get('purpose') == 'current_serp'}:
                    raise ValueError('오래된 경쟁 문서의 현재 노출 확인 기록 필요')
            elif row.get('validity_search_id') not in checks or not row.get('validity_note', '').strip():
                raise ValueError('과거/날짜 미확인 자료의 현재 유효성 확인 누락')
    claims = data.get('claims', [])
    if not fact_ids or not claims:
        raise ValueError('본문 핵심 주장과 근거 자료 연결 필요')
    for claim in claims:
        links = claim.get('source_ids', [])
        if not claim.get('text', '').strip() or not links or any(s not in fact_ids for s in links):
            raise ValueError('본문 주장에 유효한 사실 근거 ID를 연결하세요')
    return sorted(files)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--work-dir', type=Path, required=True)
    args = p.parse_args()
    try:
        files = validate(args.work_dir)
        print('최신성 기록 검사 통과: ' + ', '.join(files))
        print('출처·날짜의 진위 및 주장과 근거의 의미상 일치는 별도 원문 검토 대상입니다.')
        return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print('최신성 검증 차단: ' + str(exc))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())

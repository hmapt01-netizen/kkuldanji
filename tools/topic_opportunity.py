"""Evidence-led topic discovery and review for the Honeyjar agent.

prepare collects observations; report validates an agent's relative judgement.
Neither step predicts ranking or equates missing data with zero demand.
"""
import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
KST = timezone(timedelta(hours=9))
CHANNELS = ('google', 'naver')


def now():
    return datetime.now(KST).isoformat()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def write_new(path, data):
    with Path(path).open('x', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, allow_nan=False)


def gsc_snapshot(days=28, page=None):
    """Bounded, read-only official query/page API request; no credential output."""
    from fetch_traffic import KEY_PATH, GSC_SITE_URL
    end = datetime.now(KST).date() - timedelta(days=3)
    start = end - timedelta(days=days - 1)
    body = dict(startDate=str(start), endDate=str(end), dimensions=['query', 'page'],
                rowLimit=25000, type='web', dataState='final')
    if page:
        body['dimensionFilterGroups'] = [{'filters': [
            {'dimension': 'page', 'operator': 'equals', 'expression': page}]}]
    result = dict(status='unavailable', observed_at=now(), site=GSC_SITE_URL,
                  source_url='https://search.google.com/search-console', request=body,
                  rows=[], limitations='내 사이트의 구글 실적. 전체 검색량 아님. API는 모든 행을 보장하지 않음. 날짜는 API의 PT 기준.')
    if not Path(KEY_PATH).is_file():
        return dict(result, reason='서비스 계정 파일 없음. 공개 검색 관찰로 계속 진행 가능.')
    try:
        local_dependencies = ROOT / 'codex_tools/topic_agent_20261005/dependencies'
        if local_dependencies.is_dir() and str(local_dependencies) not in sys.path:
            sys.path.insert(0, str(local_dependencies))
        from google.oauth2 import service_account
        from google.auth.transport.requests import AuthorizedSession
        from urllib.parse import quote
        credentials = service_account.Credentials.from_service_account_file(
            KEY_PATH, scopes=['https://www.googleapis.com/auth/webmasters.readonly'])
        with AuthorizedSession(credentials, refresh_timeout=20) as session:
            response = session.post('https://www.googleapis.com/webmasters/v3/sites/' +
                                    quote(GSC_SITE_URL, safe='') + '/searchAnalytics/query',
                                    json=body, timeout=30)
            if response.status_code != 200:
                return dict(result, reason=f'GSC HTTP {response.status_code}: 권한/연결 확인 필요')
            payload = response.json()
        rows = payload.get('rows', [])
        return dict(result, status='ok', rows=rows, row_limit_reached=len(rows) >= 25000)
    except ImportError:
        return dict(result, reason='이 Python 환경에 google-auth/requests가 없음. 계정 연결 성공으로 보고하지 말 것.')
    except Exception as exc:
        return dict(result, reason=f'GSC 조회 실패 ({type(exc).__name__}); 비밀정보 보호를 위해 원문 오류 생략')


def candidate(identifier, query, refs, origin='observed'):
    return dict(id=identifier, query=query, reader_question='', origin=origin,
        source_ids=refs, action='explore', existing_slugs=[], duplication_note='',
        answer_value='', site_fit='', timeliness='',
        channels={channel: dict(verdict='explore', source_ids=[], reason='',
                               uncertainty='검색 화면과 수요 규모 미확인') for channel in CHANNELS})


def prepare(work, seeds=(), use_gsc=True, collect=True):
    work = Path(work)
    work.mkdir(parents=True, exist_ok=True)
    targets = [work / n for n in ('topic_context.json', 'topic_review.json')]
    if any(p.exists() for p in targets):
        raise ValueError('기존 조사·판단을 덮어쓰지 않습니다. 기존 자료를 이어 쓰거나 새 조사 폴더를 지정하세요.')
    posts = read(ROOT / 'data/posts_db.json')
    metadata = [{k: p.get(k, '') for k in ('title', 'slug', 'date', 'category', 'desc')} for p in posts]
    snapshot = gsc_snapshot() if use_gsc else dict(status='not_requested', rows=[], observed_at=now())
    sources, candidates, seen = [], [], {}

    def add_source(kind, channel, query, url, excerpt, **extra):
        item = dict(id=f's{len(sources)+1}', kind=kind, channel=channel, query=query,
                    url=url, observed_at=now(), excerpt=excerpt, **extra)
        sources.append(item)
        return item['id']

    def add_candidate(query, ref=None, origin='observed'):
        query = ' '.join(query.split())
        if not query:
            return
        if query not in seen:
            seen[query] = candidate(f'c{len(candidates)+1}', query, [], origin)
            candidates.append(seen[query])
        if ref and ref not in seen[query]['source_ids']:
            seen[query]['source_ids'].append(ref)
            seen[query]['origin'] = 'observed'

    # Discovery order is not recommendation order. Preserve page-level rows.
    for row in sorted(snapshot.get('rows', []), key=lambda r: r.get('impressions', 0), reverse=True)[:30]:
        if len(row.get('keys', [])) != 2:
            continue
        query, page = row['keys']
        ref = add_source('gsc', 'google', query, snapshot['source_url'],
                         json.dumps(row, ensure_ascii=False), metrics=row,
                         period=snapshot['request'], page=page)
        add_candidate(query, ref)
    for seed in seeds:
        add_candidate(seed, origin='hypothesis')
    discovery_seeds = list(dict.fromkeys(list(seeds) + list(seen)))[:5]
    attempts = []
    if collect:
        from serp_collection import autocomplete
        for seed in discovery_seeds:
            for channel in CHANNELS:
                result = autocomplete(channel, seed)
                attempts.append(dict(channel=channel, seed=seed, observed_at=now(), **result))
                if result['status'] == 'ok':
                    for phrase in result['items'][:5]:
                        ref = add_source('autocomplete', channel, phrase, result['source_url'], phrase)
                        add_candidate(phrase, ref)
        searchad_secret = ROOT / 'naver_searchad_secret.json'
        if searchad_secret.is_file():
            try:
                from naver_searchad import fetch_keyword_stats
                searchad_seeds = list(dict.fromkeys(list(seeds) + list(seen)))[:5]
                if searchad_seeds:
                    stats = fetch_keyword_stats(searchad_seeds)
                    for item in stats[:15]:
                        kw = item['keyword']
                        tot = item['total_volume']
                        mo = item['mobile_volume']
                        pc = item['pc_volume']
                        comp = item['comp_idx']
                        excerpt = f"네이버 공식 월간 검색량: {tot:,}회 (모바일 {mo:,}회, PC {pc:,}회 / 경쟁도 {comp})"
                        ref = add_source('naver_searchad', 'naver', kw, 'https://manage.searchad.naver.com',
                                         excerpt, metrics=item)
                        add_candidate(kw, ref)
            except Exception:
                pass
    context = dict(version=1, collected_at=now(), posts=metadata, gsc=snapshot, collected_sources=sources,
                   autocomplete_attempts=attempts,
                   notice='제목·설명과 수집 관찰만 포함. 본문 중복·검색량·경쟁 판단 미완료.')
    write_new(targets[0], context)
    review = dict(version=1, stage='discovery', created_at=now(),
        context_sha256=hashlib.sha256(targets[0].read_bytes()).hexdigest(),
        sources=sources, candidates=candidates, recommendations=[],
        comparison_reason='', search_limits='',
        next_step='관찰 질문·시의성 후보를 보완하고 약 10개 비교 → 3개 이하 후보와 추천 1개')
    write_new(targets[1], review)
    return review


def valid_time(value):
    try:
        stamp = datetime.fromisoformat(value)
        return stamp.tzinfo is not None and stamp <= datetime.now(timezone.utc) + timedelta(minutes=5)
    except (TypeError, ValueError):
        return False


def validate(review, context=None):
    from blue_ocean import recent
    if review.get('version') != 1 or review.get('stage') != 'discovery':
        raise ValueError('version=1, stage=discovery 필요')
    sources = {}
    original_sources = {s['id']: s for s in (context or {}).get('collected_sources', [])}
    kinds = {'gsc', 'autocomplete', 'serp_screen', 'web_search', 'question', 'trend', 'announcement', 'naver_searchad'}
    for s in review.get('sources', []):
        if not s.get('id') or s['id'] in sources or s.get('kind') not in kinds:
            raise ValueError('서로 다른 출처 ID와 지원 자료 유형 필요')
        if s['id'] in original_sources and s != original_sources[s['id']]:
            raise ValueError('도구 수집 출처는 원본 그대로 유지하고 새 관찰은 새 ID로 추가하세요')
        if s.get('channel') not in (*CHANNELS, 'web') or not valid_time(s.get('observed_at')):
            raise ValueError('출처 채널·실제 확인 시각 필요')
        if urlparse(s.get('url', '')).scheme not in ('http', 'https') or not urlparse(s['url']).hostname or not s.get('excerpt'):
            raise ValueError('관찰 출처 URL·짧은 발췌 필요')
        if s['kind'] == 'gsc':
            if s['channel'] != 'google' or not context or context.get('gsc', {}).get('status') != 'ok':
                raise ValueError('GSC 수치는 성공한 구글 수집 원본 필요')
            snapshot = context['gsc']
            if s.get('metrics') not in snapshot.get('rows', []) or s.get('period') != snapshot.get('request'):
                raise ValueError('GSC 수치/기간이 저장된 수집 원본과 다름')
            if s['metrics'].get('keys') != [s.get('query'), s.get('page')]:
                raise ValueError('GSC 검색어·페이지 불일치')
        if s['kind'] == 'serp_screen':
            from urllib.parse import parse_qs
            p = urlparse(s['url'])
            hosts = {'google': {'www.google.com', 'google.com', 'www.google.co.kr'}, 'naver': {'search.naver.com'}}
            if p.hostname not in hosts.get(s['channel'], set()) or (parse_qs(p.query).get('q') or parse_qs(p.query).get('query')) != [s.get('query')]:
                raise ValueError('포털 검색 화면의 채널·정확한 검색어 불일치')
        sources[s['id']] = s
    candidates = {}
    for c in review.get('candidates', []):
        if not c.get('id') or c['id'] in candidates or not c.get('query'):
            raise ValueError('후보 ID·검색 질문 필요')
        if c.get('origin') not in ('observed', 'hypothesis'):
            raise ValueError('관찰 질문/AI 가설 구분 필요')
        if any(i not in sources for i in c.get('source_ids', [])):
            raise ValueError('후보 출처 ID가 없음')
        if c['origin'] == 'observed' and not c.get('source_ids'):
            raise ValueError('관찰 후보에는 발견 출처 필요')
        candidates[c['id']] = c
    picks = review.get('recommendations', [])
    if not 1 <= len(picks) <= 3 or len(set(picks)) != len(picks) or any(i not in candidates for i in picks):
        raise ValueError('서로 다른 후보 1~3개를 순서대로 선택하세요. 첫 후보가 잠정 추천 1개입니다.')
    if not review.get('comparison_reason') or not review.get('search_limits'):
        raise ValueError('후보 간 비교 이유와 전체 조사 한계 필요')
    queries = set()
    slugs = {p['slug'] for p in (context or {}).get('posts', [])}
    for identifier in picks:
        c = candidates[identifier]
        if c['query'] in queries:
            raise ValueError('동일 검색어를 다른 후보로 중복 추천할 수 없음')
        queries.add(c['query'])
        for field in ('reader_question', 'duplication_note', 'answer_value', 'site_fit'):
            if not c.get(field):
                raise ValueError(f'{identifier}: {field} 검토 필요')
        if c.get('action') not in ('new', 'update', 'explore'):
            raise ValueError('new/update/explore 작업 구분 필요')
        if any(slug not in slugs for slug in c.get('existing_slugs', [])):
            raise ValueError('실제 기존 글 slug만 연결하세요')
        if c['action'] == 'update' and not c.get('existing_slugs'):
            raise ValueError('기존 글 보완 후보에는 대상 글 필요')
        for channel in CHANNELS:
            judgement = c.get('channels', {}).get(channel, {})
            if judgement.get('verdict') not in ('compare', 'explore', 'hold') or not judgement.get('reason') or not judgement.get('uncertainty'):
                raise ValueError(f'{identifier}/{channel}: 비교/탐색/보류, 이유, 미확인 사항 필요')
            refs = judgement.get('source_ids', [])
            if any(i not in sources or sources[i]['channel'] != channel for i in refs):
                raise ValueError('다른 채널 출처를 해당 채널의 관찰로 사용할 수 없음')
            if judgement['verdict'] == 'compare' and not any(
                    sources[i]['kind'] == 'serp_screen' and sources[i].get('query') == c['query']
                    and recent(sources[i]['observed_at']) for i in refs):
                raise ValueError('상대 비교에는 해당 질문의 실제 포털 검색 화면 출처 필요. 없으면 탐색으로 추천 가능.')
        if all(c['channels'][ch]['verdict'] == 'hold' for ch in CHANNELS):
            raise ValueError('양쪽 모두 보류한 후보를 추천하지 마세요')
    return candidates, sources


def cell(value):
    return str(value).replace('|', '&#124;').replace('\n', ' ').replace('\r', ' ')


def render(review, context):
    candidates, sources = validate(review, context)
    lines = ['# 오늘의 주제 후보', '', '제목·검색 화면 기준 잠정 추천입니다. 본문 답변의 빈틈은 선택 후 리서치에서 확인합니다.', '',
             '| 순서 | 주제 / 독자 질문 | 작업 | 구글 판단 | 네이버 판단 | 추가할 가치 / 기존 글과 관계 |',
             '|---|---|---|---|---|---|']
    labels = {'compare': '비교 후보', 'explore': '탐색 후보', 'hold': '보류'}
    used = set()
    for n, identifier in enumerate(review['recommendations'], 1):
        c = candidates[identifier]
        used.update(c['source_ids'])
        desc = []
        for ch in CHANNELS:
            j = c['channels'][ch]
            used.update(j['source_ids'])
            desc.append(f"{labels[j['verdict']]}: {j['reason']} / 미확인: {j['uncertainty']}")
        origin = '관찰 질문' if c['origin'] == 'observed' else 'AI 가설'
        lines.append('| ' + ' | '.join(cell(v) for v in [n, origin + ': ' + c['query'] + ' / ' + c['reader_question'],
            {'new': '새 글', 'update': '기존 글 보완', 'explore': '탐색'}[c['action']], *desc,
            c['answer_value'] + ' / ' + c['duplication_note'] + ' / ' + c['site_fit']]) + ' |')
    lines += ['', '**잠정 추천 1개:** ' + candidates[review['recommendations'][0]]['query'],
              '', review['comparison_reason'], '', '**조사 한계:** ' + review['search_limits'], '', '**확인 출처**']
    for identifier in sorted(used):
        s = sources[identifier]
        lines.append(f"- {identifier} [{s['kind']} / {s['channel']}]({s['url']}) · {s['observed_at']} · {cell(s['excerpt'])}")
    lines += ['', '사전 검토 기록: 자료 연결 검사는 실제 검색 수행·내용의 진위·노출 가능성을 자동 보증하지 않습니다.']
    return '\n'.join(lines) + '\n'


def report(work):
    work = Path(work)
    review = read(work / 'topic_review.json')
    context_path = work / 'topic_context.json'
    if hashlib.sha256(context_path.read_bytes()).hexdigest() != review.get('context_sha256'):
        raise ValueError('수집 원본이 변경되었습니다. 원본을 복구하거나 새 조사로 검토하세요.')
    context = read(context_path)
    original_ids = {s['id'] for s in context.get('collected_sources', [])}
    for source in review.get('sources', []):
        if source.get('id') in original_ids:
            continue
        evidence = (work / source.get('evidence_file', '')).resolve()
        if not evidence.is_relative_to(work.resolve()) or not evidence.is_file():
            raise ValueError('추가 관찰에는 작업 폴더 내 실제 evidence_file이 필요합니다')
        if hashlib.sha256(evidence.read_bytes()).hexdigest() != source.get('evidence_sha256'):
            raise ValueError('추가 관찰 근거 파일의 해시 불일치')
    content = render(review, context)
    # Reports are derived files; evidence and agent decisions stay untouched.
    (work / 'topic_report.md').write_text(content, encoding='utf-8')
    return content


def feedback(work, candidate_id, page, note):
    work = Path(work)
    review = read(work / 'topic_review.json')
    if candidate_id not in {c['id'] for c in review['candidates']}:
        raise ValueError('기존 후보 ID 필요')
    if urlparse(page).hostname not in ('honeyjar.co.kr', 'www.honeyjar.co.kr'):
        raise ValueError('꿀단지 실제 발행 URL 필요')
    result = dict(candidate_id=candidate_id, page=page, observed_at=now(), note=note,
                  review_sha256=hashlib.sha256((work / 'topic_review.json').read_bytes()).hexdigest(),
                  gsc=gsc_snapshot(page=page),
                  interpretation='노출 없음은 수요 없음이 아님. 색인·기간·계절·기기·순위를 확인한 뒤 해석. 자동 인과/성공 판정 없음.')
    with (work / 'topic_outcomes.jsonl').open('a', encoding='utf-8') as f:
        f.write(json.dumps(result, ensure_ascii=False, allow_nan=False) + '\n')
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'report', 'feedback'))
    parser.add_argument('--work-dir', required=True, type=Path)
    parser.add_argument('--seed', action='append', default=[])
    parser.add_argument('--skip-gsc', action='store_true')
    parser.add_argument('--offline', action='store_true')
    parser.add_argument('--candidate')
    parser.add_argument('--page')
    parser.add_argument('--note')
    args = parser.parse_args(argv)
    try:
        if args.action == 'prepare':
            review = prepare(args.work_dir, args.seed, not (args.skip_gsc or args.offline), not args.offline)
            print(f"수집 후보 {len(review['candidates'])}개. 아직 추천하지 않았습니다. topic_review.json을 실제 관찰로 검토하세요.")
        elif args.action == 'report':
            print(report(args.work_dir))
        else:
            if not all((args.candidate, args.page, args.note)):
                parser.error('feedback에는 --candidate, --page, --note 필요')
            result = feedback(args.work_dir, args.candidate, args.page, args.note)
            print('결과 기록: GSC ' + result['gsc']['status'])
        return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print('보완 필요: ' + str(exc))
        return 2


if __name__ == '__main__':
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())

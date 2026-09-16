"""Thin Codex adapter for the existing title validators and SERP collector."""
import argparse
import contextlib
import copy
import io
import json
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import validate_titles as existing
import serp_collection as collector
from audit_serp_live import extract_clean_query_and_seed
from blue_ocean import evaluate, recent
from legacy_score import calculate_low_authority_score


def check_titles(data, channel):
    titles = data.get(channel + '_candidates', [])
    if not isinstance(titles, list) or any(not isinstance(t, str) for t in titles):
        raise ValueError('제목 문자열 배열 필요')
    if len(titles) != 10 or len(set(titles)) != 10:
        raise ValueError('서로 다른 제목 10개 필요')
    if any(not 40 <= len(t.strip()) <= 60 for t in titles):
        raise ValueError('제목은 공백·문장부호 포함 40~60자 필요')
    # Google validator writes an audit even with run_serp=False. Redirect only
    # its runtime log location, restoring the module immediately afterwards.
    source_path = existing.__file__
    with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()):
        try:
            existing.__file__ = str(Path(tmp) / 'tools' / 'validate_titles.py')
            valid = getattr(existing, f'validate_{channel}_titles')(titles, run_serp=False)
        finally:
            existing.__file__ = source_path
    if not valid:
        raise ValueError('기존 제목 검사기에서 금칙어/채널/그룹 규격 위반')
    return titles


def queries_for(data, channel):
    titles = check_titles(data, channel)
    queries = data.get('search_queries', [])
    if len(queries) != len(titles) or any(not isinstance(q, str) or not q.strip() for q in queries):
        raise ValueError('제목 순서에 맞는 실제 검색어 search_queries 10개 필요')
    queries = [extract_clean_query_and_seed(q)[0] for q in queries]
    if len(set(queries)) < 2:
        raise ValueError('검색어 하나의 표현 10개로는 후보 비교 불가. 공략 질문을 나눠 후보를 구성하세요')
    return titles, queries


def collect(work, data, channel):
    from workflow_guard import require_step
    require_step(work, channel + '_titles')
    titles, queries = queries_for(data, channel)
    check_related_keywords(work, data, channel)
    path = work / f'{channel}_serp_audit.json'
    old_dir = collector.DATA_DIR
    try:
        collector.DATA_DIR = work / 'data'
        if path.exists():
            previous = json.loads(path.read_text(encoding='utf-8-sig'))
            if previous.get('channel') == channel and recent(previous.get('timestamp')):
                reviewed = {r['clean_query']: r for r in previous.get('records', [])
                            if evaluate(r)['evidence_complete']}
                if reviewed:
                    cache = dict(previous, records=list(reviewed.values()))
                    collector.DATA_DIR.mkdir(exist_ok=True)
                    (collector.DATA_DIR / f'last_{channel}_serp_audit.json').write_text(
                        json.dumps(cache, ensure_ascii=False, indent=2), encoding='utf-8')
        # Existing 24-hour reviewed cache is reused; identical queries in this
        # batch are collected once and explicitly mapped back to each title.
        records = collector.audit_titles(list(dict.fromkeys(queries)), channel)
    finally:
        collector.DATA_DIR = old_dir
    by_query = {r['clean_query']: r for r in records}
    mapped = [dict(copy.deepcopy(by_query[q]), idx=i, title=t)
              for i, (t, q) in enumerate(zip(titles, queries), 1)]
    result = {'schema_version': 2, 'timestamp': collector.now(), 'channel': channel, 'records': mapped}
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    return path


def candidate_records(work, data, channel):
    titles, queries = queries_for(data, channel)
    check_related_keywords(work, data, channel)
    evidence = json.loads((work / f'{channel}_serp_audit.json').read_text(encoding='utf-8-sig'))
    if evidence.get('schema_version') != 2 or evidence.get('channel') != channel or not recent(evidence.get('timestamp')):
        raise ValueError('해당 채널의 최신 후보별 수집 기록 필요')
    records = evidence.get('records', [])
    if len(records) != 10:
        raise ValueError('후보 10개 각각의 검색 결과 행 필요')
    from urllib.parse import urlparse, parse_qs
    for i, (title, query, record) in enumerate(zip(titles, queries, records), 1):
        parsed = urlparse(record.get('search_url', ''))
        hosts = {'search.naver.com'} if channel == 'naver' else {'google.com', 'www.google.com', 'www.google.co.kr'}
        params = parse_qs(parsed.query)
        if (record.get('idx') != i or record.get('title') != title or record.get('clean_query') != query
                or parsed.hostname not in hosts or (params.get('query') or params.get('q')) != [query]
                or not recent(record.get('collected_at'))):
            raise ValueError(f'{i}번 제목·검색어·채널·실제 수집 기록 불일치/만료')
    return records


def check_related_keywords(work, data, channel):
    """Bind the query and title to actual saved discovery results."""
    from urllib.parse import urlparse
    titles, queries = queries_for(data, channel)
    evidence = json.loads((work / f'{channel}_related_keywords.json').read_text(encoding='utf-8-sig'))
    if evidence.get('channel') != channel:
        raise ValueError('연관검색어 자료의 채널 불일치')
    hosts = {'ac.search.naver.com', 'search.naver.com'} if channel == 'naver' else {'suggestqueries.google.com', 'www.google.com', 'google.com'}
    phrases = []
    for row in evidence.get('records', []):
        if row.get('status') == 'ok' and recent(row.get('observed_at')) and urlparse(row.get('source_url', '')).hostname in hosts:
            phrases.extend(''.join(item.split()) for item in row.get('items', []) if isinstance(item, str) and len(item.strip()) >= 2)
    if not phrases:
        raise ValueError('실제 조회한 연관검색어·출처·조회 시각 필요')
    for i, (title, query) in enumerate(zip(titles, queries), 1):
        clean_query, clean_title = ''.join(query.split()), ''.join(title.split())
        if not any(p in clean_query for p in phrases):
            raise ValueError(f'{i}번 검색어에 실제 연관검색어 근거 없음')
        if any(word not in clean_title for word in query.split() if len(word) >= 2):
            raise ValueError(f'{i}번 제목에 공략 검색어의 단어 누락')
    return True


def assessed(record):
    result = evaluate(record)
    # Topic/title comparison uses observed related keywords and accessible
    # competitor bodies; full factual/medical validation remains a later step.
    review = record.get('title_review', {})
    docs = [d for d in record.get('top_docs', []) if d.get('answer_coverage') in ('direct', 'partial', 'unrelated') and d.get('review_note') and recent(d.get('reviewed_at'))]
    keyword = record.get('related_keyword', {})
    if (not result['evidence_complete'] and record.get('collection_status') == 'ok'
            and recent(record.get('collected_at')) and len(docs) >= 3
            and review.get('competition') in ('gap', 'medium', 'high')
            and review.get('reason') and recent(review.get('reviewed_at'))
            and keyword.get('text') == record.get('clean_query')
            and keyword.get('source_url', '').startswith('https://')
            and recent(keyword.get('observed_at'))):
        result = dict(result, comparison_ready=True, status='relative_comparison',
            badge={'gap': '🟢', 'medium': '🟡', 'high': '🔴'}[review['competition']],
            reason=review['reason'], coverage_counts={k:sum(d['answer_coverage']==k for d in docs) for k in ('direct','partial','unrelated')},
            review_scope=f"본문 {len(docs)}/{len(record['top_docs'])}개 확인")
    # Unknown evidence has no score: the old ⚠️ deduction conflated missing
    # data with zero demand. Preserve the formula only for reviewed records.
    score = calculate_low_authority_score(record['title'], dict(record, badge=result['badge']))[0] if result.get('comparison_ready', result['evidence_complete']) else None
    return result, score


def comparison_key(record):
    """Competition first; the legacy wording score is only a tie-breaker."""
    result, score = assessed(record)
    if not result.get('comparison_ready', result['evidence_complete']):
        return (3, 1, 0)
    counts = result['coverage_counts']
    total = sum(counts.values())
    review = record['review'] if result['evidence_complete'] else record['title_review']
    strength = {'gap': 0, 'medium': 1, 'high': 2}[review['competition']]
    return (strength, counts['direct'] / total if total else 1, -score)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work-dir', required=True, type=Path)
    parser.add_argument('--channel', required=True, choices=('naver', 'google'))
    args = parser.parse_args()
    work = args.work_dir.resolve()
    try:
        from workflow_guard import require_step
        require_step(work, args.channel + '_titles')
        data = json.loads((work / f'{args.channel}_candidates.json').read_text(encoding='utf-8-sig'))
        print(collect(work, data, args.channel))
        return 0
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print('후보 보완 필요: ' + str(exc))
        return 2


if __name__ == '__main__':
    sys.exit(main())

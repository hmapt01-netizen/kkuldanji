"""Save this session's observed Google sample without repeating collection."""
import hashlib
import json
from pathlib import Path

W = Path(__file__).resolve().parent
def read(name):
    return json.loads((W / name).read_text(encoding='utf-8-sig'))
def save(name, data):
    (W / name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

evidence = read('google_browser_review.json')
audit = read('google_serp_audit.json')
backup = W / 'google_http_attempt.json'
if not backup.exists():
    save(backup.name, audit)
groups = {g['query']: g for g in evidence['groups']}
for row in audit['records']:
    group = groups.get(row['clean_query'])
    if not group:
        continue
    row.update(collection_method='browser', collection_status='ok',
               collected_at=evidence['observed_at'], error=None,
               coverage_note=group['reason'], observed_result_count=group['observed_count'])
    row['top_docs'] = [dict(d, reviewed_at=evidence['observed_at']) for d in group['docs']]
    row['title_review'] = dict(competition=group['competition'], reason=group['reason'], reviewed_at=evidence['observed_at'])
    row['related_keyword'] = dict(text=row['clean_query'], source_url=row['search_url'], observed_at=evidence['observed_at'], kind='constructed_query_from_observed_terms', note='기존 google_related_keywords.json의 실제 표현으로 구성한 검색어. 검색량 추정 아님.')
save('google_serp_audit.json', audit)
manifest = read('codex_reuse/google_titles.json')
q = manifest['questions'][0]
q['answer'] = '재검은 중간 경쟁, 공복은 높은 경쟁. 금주 전후 비교 기록으로 제목 범위를 좁히며 음주 일반 검색 후보는 미확인으로 표시한다.'
q['limits'] = '두 검색 의도별 3개 본문 표본. 같은 아산병원 본문 재사용. 검색량·전체 경쟁 문서·의학 주장 검증은 아님.'
q['evidence'] = [dict(path='google_browser_review.json', sha256=hashlib.sha256((W/'google_browser_review.json').read_bytes()).hexdigest(), excerpt=evidence['handoff'])]
save('codex_reuse/google_titles.json', manifest)

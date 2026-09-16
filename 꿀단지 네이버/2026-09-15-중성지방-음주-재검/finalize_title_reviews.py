import hashlib
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

W = Path(__file__).resolve().parent
def read(name):
    return json.loads((W / name).read_text(encoding='utf-8'))
def save(name, data):
    (W / name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

stamp = datetime.now(ZoneInfo('Asia/Seoul')).isoformat()
fresh = read('freshness_review.json')
for row in fresh['searches'] + fresh['sources']:
    row['evidence_sha256'] = hashlib.sha256((W / row['evidence_file']).read_bytes()).hexdigest()
for row in fresh['sources']:
    if row['id'] in ('question1', 'question2'):
        date = {'question1':'2026-09-02', 'question2':'2026-08-18'}[row['id']]
        row.update(published_on=date, date_evidence='작성일 ' + date.replace('-', '.'))
        row.pop('date_status', None)
if not any(s['id'] == 'kdca' for s in fresh['sources']):
    fresh['sources'].append(dict(
        id='kdca', title='지질 검사',
        url='https://health.kdca.go.kr/healthinfo/biz/health/gnrlzHealthInfo/gnrlzHealthInfo/gnrlzHealthInfoView.do?cntnts_sn=6709',
        role='fact', accessed_on=stamp[:10], published_on='2025-05-07', updated_on='2026-05-06',
        date_evidence='등록일자 : 2025-05-07 업데이트 : 2026-05-06',
        exception_reason='국내 공인 검사 준비 안내로 사용. 과거판과 수정 내용을 대조하지 않아 새 지침 개정으로 해석하지 않음.',
        validity_search_id='validity', validity_note='현재 접근 가능한 원문을 읽고 MedlinePlus와 ACC 2026 교육 자료의 공복 조건 구분과 대조. 검사기관의 지시를 우선하며 약물 치료 권고는 채택하지 않음.',
        evidence_file='source_notes.md', evidence_sha256=hashlib.sha256((W/'source_notes.md').read_bytes()).hexdigest(),
        evidence_excerpt='등록일자 : 2025-05-07 업데이트 : 2026-05-06'))
save('freshness_review.json', fresh)

audit = read('naver_serp_audit.json')
reviews = {
    '중성지방 검사 금식': {
        2: ('partial', '마른 체형에서 중성지방이 높은 여러 원인과 금식·음주 확인을 설명한다. 금식 준비만을 중심으로 하지는 않는다.'),
        3: ('direct', '중성지방 채혈 전 물 한 컵을 마신 실제 질문에 금식 중 물과 재검 여부를 직접 답한다. 이 답변을 의학적 근거로 전용하지 않는다.'),
        4: ('direct', '삼성서울병원이 지질검사 전 금식, 식사와 알코올의 영향을 직접 설명한다. 원문의 약 14시간 안내를 모든 검사에 적용하지 않는다.'),
        5: ('direct', '질병관리청이 지질검사 준비에서 금식 시간과 중성지방의 공복 영향을 직접 설명한다. 비공복 검사도 의미가 있을 수 있음을 함께 언급한다.')},
    '중성지방 재검': {
        1: ('direct', '전날 늦은 식사·음주 후 높은 결과에 대한 공복 재검을 직접 답한다. 금식 표현이 답변마다 다르다.'),
        2: ('partial', '중성지방 339 결과 후 재검을 앞둔 독자의 생활관리 질문과 개인 경험 답변이다. 재검 조건·시기를 체계적으로 설명하지 않는다.'),
        3: ('partial', '정상수치와 생활관리 중심이며 생활관리 후 4~12주 재검을 일부 설명한다. 전날 음주로 검사 조건이 달라진 경우의 재확인과 구분이 부족하다.'),
        4: ('direct', '중성지방 317 사례에 공복 여부, 공복 재검, 생활관리 후 재검 시기, 다른 검사 항목까지 명시한다. 직접 답변 경쟁이다.')}
}
reasons = {
    '중성지방 전날 술': '음주·재검을 다룬 [의원 글](https://hanmaeumplus.com/blog/internal/post-20260716000002)이 있어 중간 경쟁. 마지막 식사·음주 기록으로 범위를 좁힘.',
    '중성지방 검사 금식': '[질병관리청](https://health.kdca.go.kr/healthinfo/biz/health/gnrlzHealthInfo/gnrlzHealthInfo/gnrlzHealthInfoView.do?cntnts_sn=6709)·병원이 금식에 직접 답해 높은 경쟁.',
    '중성지방 재검': '[실제 질문](https://www.modoodoc.com/community/5272/%EC%A4%91%EC%84%B1%EC%A7%80%EB%B0%A9)에 재검 답변이 있음. 일반 관리 글과 구별할 여지가 있어 중간 경쟁.'
}
for record in audit['records']:
    q = record['clean_query']
    if q == '중성지방 전날 술':
        record['review']['decision_reason'] = reasons[q]
        continue
    for doc in record['top_docs']:
        if doc['rank'] in reviews[q]:
            coverage, note = reviews[q][doc['rank']]
            doc.update(answer_coverage=coverage, review_note=note, reviewed_at=stamp)
    record['title_review'] = dict(competition='high' if q == '중성지방 검사 금식' else 'medium', reason=reasons[q], reviewed_at=stamp)
    record['related_keyword'] = dict(text=q, source_url=record['search_url'], observed_at=record['collected_at'], kind='constructed_query_from_observed_terms', note='자동완성의 중성지방·검사·금식 및 실제 독자의 재검 질문으로 조합한 검색어. 정확한 전체 표현의 네이버 자동완성 출현을 뜻하지 않음.')
save('naver_serp_audit.json', audit)

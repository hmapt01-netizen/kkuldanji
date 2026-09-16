"""Persist the agent's actual 2026-09-14 reading notes; not an automatic SERP judgment."""
import json
from datetime import datetime
from pathlib import Path

root = Path(__file__).resolve().parent
data = json.loads((root / 'meat_delivery_serp_20260914.json').read_text(encoding='utf-8'))
stamp = datetime.now().astimezone().isoformat()
r = data['records'][0]
notes = [
    ('direct', 'CUA 본문 확인. 2026-08-24 냉동 양념갈비 재냉동 경험 글. 온도 이력 불명확성을 언급하지만 아이스팩 잔빙·촉감과 당일 조리 경험을 판단 근거로 제시하고 애매하면 빠른 조리를 선택한다. 직접 답변은 있으나 실제 온도 측정·섭취 보류 기준과 공인 출처가 부족하다.'),
    ('partial', 'CUA 본문·댓글 확인. 2026-09-04 냉동 양지가 녹은 채 배송되어 다시 얼려도 되는지 묻는다. 댓글은 재냉동 비권장 또는 사진 후 교환 문의. 측정 온도·노출 이력별 분기가 없다.'),
    ('partial', 'CUA 본문·댓글 확인. 2026-08-25 드라이아이스가 모두 녹고 고기가 미지근하게 도착한 경험. 댓글은 냄새가 나면 환불하라는 수준으로, 냄새가 정상이어도 안전을 입증할 수 없다는 설명이 없다.'),
    ('partial', 'CUA 본문·댓글 확인. 2026-07-22 파손·재포장된 상자, 녹은 아이스팩, 약간의 냉기 때문에 섭취와 판매자 문의를 고민한다. 냉기만 있으면 먹어도 된다는 댓글과 문의 권고가 섞임. 보관 이력의 불명확성과 촉감의 한계를 설명하지 않는다.'),
    ('partial', 'CUA 본문·댓글 확인. 2026-08-09 루리웹 글을 옮긴 모음 페이지. 판매자의 USDA 인용과 국내 적용 문제, 배송 지연, 환불 경험을 논의한다. 미국 지침과 국내 제품 표시를 구분한 일반 안내는 없다. 원글과 별도 수요로 중복 집계하지 않음.'),
    ('unrelated', 'CUA 후기 본문 확인. 2026-09-10 게시된 함박스테이크 구매평으로 해동 배송·아이스팩 배치·짠맛을 언급한다. 생고기 재냉동/섭취 판단에 답하는 글은 아니다. 상품 구매 링크와 별개의 검색 노출 후기 문서로 집계.'),
    ('partial', 'CUA 본문·댓글 확인. 2026-07-30 고기 6kg이 말랑하게 도착해 재냉동·섭취를 질문. 냉기가 있으면 괜찮다는 경험담과 판매자 문의 권고가 혼재. 글쓴이는 이후 환불했다고 답함. 개인 경험은 안전 근거가 아님.'),
    ('partial', 'CUA 본문·댓글 확인. 2024-04-07 배송 후 문 앞에서 2시간 지난 차돌양지의 해동과 소분 재냉동 질문. 소분 냉동 권유와 교환·환불 의견, 배송 알림 논쟁이 중심. 식품 온도와 시간에 따른 근거 안내 없음.'),
    ('partial', 'CUA 후기 본문 확인. 2026-07-15 등록 구매평. 우대갈비 지연 배송·녹은 아이스팩·냄새와 사진/문자 제출 경험. 일반 식품안전 판단은 없으며 개별 분쟁 사실은 구매자 주장으로만 취급.'),
    ('partial', 'CUA 본문·댓글 확인. 2026-07-02 약간 녹은 택배 고기를 다시 얼릴지 묻고, 댓글은 곧바로 냉동·소분을 권한다. 30분이라는 근거 없는 수치도 등장. 보관 이력·측정 온도 확인이 없다.'),
]
for doc, (coverage, note) in zip(r['top_docs'], notes):
    doc.update(answer_coverage=coverage, review_note=note, reviewed_at=stamp)

questions = [r['top_docs'][i]['url'].split('?art=')[0] for i in (1, 6, 7, 9)]
r['review'] = {
    'query': r['clean_query'],
    'reader_question': '택배로 받은 냉동 고기가 녹아 있다. 먹어도 되는지, 다시 얼려도 되는지, 먼저 무엇을 확인해야 하는가?',
    'demand': [{
        'kind': 'repeated_questions', 'query': r['clean_query'],
        'source_url': questions[0], 'observed_at': stamp,
        'period': '질문 게시일 2024-04-07, 2026-07-02, 2026-07-30, 2026-09-04; 원문 조회 2026-09-14',
        'value': 4, 'question_urls': questions,
        'interpretation': '동일한 해동 배송→섭취/재냉동 판단 의도를 가진 서로 다른 질문 원문 4건을 확인했다. 정성적 수요 근거이며 월간 검색량·추석 검색 증가율은 확인하지 않았다. 추석 연결은 선물 수령 상황에 대한 편집적 적용이다.',
    }],
    'competition': 'gap',
    'competition_reason': '해당 네이버 쿼리 수집 상위 10건의 본문을 모두 열었다. 블로그 경험 안내 1건, 카페·커뮤니티 7건, 구매후기 2건이다. 직접 답변 1건에도 모호한 상태를 당일 조리로 해결한 경험이 섞여 있다. 나머지는 부분적인 경험/댓글 또는 다른 목적 후기다. 검색 범위를 넓히면 브리프노트의 충분한 안내가 실제 존재하므로 경쟁 부재를 주장하지 않는다. 좁은 네이버 질문 결과에서 공인 근거를 조건별 행동으로 정리할 여지가 있다는 상대적 판단이다.',
    'gap': '받은 냉동 고기의 얼음 결정·식품 온도·포장·배송 및 수령 시각을 구분하고, 촉감/냄새/아이스팩만으로 안전 판정하지 않도록 설명하는 공인 근거 안내가 해당 상위 결과에서 부족하다. 이미 다시 냉동했거나 수령 온도를 모르는 경우와 판매자에게 확인할 사항도 함께 다룬다.',
    'answer_plan': '추석 전 고기 선물 수령자를 대상으로: 주문 전 수령 가능일 확인 → 수령 즉시 제품의 냉장/냉동 표시·포장·시각·식품 온도 확인 → 정상적으로 보냉된 경우/따뜻하거나 이력 불명확한 경우/이미 다시 얼린 경우를 구분 → 의심 식품 맛보기 금지와 판매자 문의용 기록 목록. 미국 40°F 안내를 국내 모든 식품의 법정 기준이나 환불 기준으로 표현하지 않는다. 빠른 조리·재냉동이 불분명한 보관 이력을 해결한다는 주장을 하지 않는다.',
    'sources': [
        {'url': 'https://www.foodsafety.gov/blog/tips-meal-kit-and-food-delivery-safety',
         'finding': '원문 본문 확인. 배송 식품은 수령 시 식품용 온도계로 확인, 냉동/잔빙/냉장 수준(40°F 이하) 도착, 기준보다 따뜻하면 맛보거나 먹지 말고 업체에 알림, 냄새/맛/외관 정상이어도 안전하지 않을 수 있음. 미국 소비자 안내 범위. 국내 법정 기준으로 전용하지 않음.', 'checked_at': stamp},
        {'url': 'https://www.foodsafetykorea.go.kr/portal/board/boardDetail.do?bbs_no=bbs109&menu_grp=MENU_NEW05&menu_no=2873&ntctxt_no=1090416',
         'finding': '2022-06-20 식약처 배달 및 택배유통 냉장축산물 가이드라인 본문·요약 확인. 보냉 유지, 박스/내용물 이상 확인, 배송 안내 후 신속 수취·냉장보관, 장시간 수취 불가 시 주문 지양. 냉장축산물 안내이며 냉동 해동육 재냉동 승인 근거로 사용하지 않음.', 'checked_at': stamp},
    ],
    'duplication_review': 'posts_db.json 27편 전체 제목/슬러그와 최근 글 확인. 해동 배송 고기의 수령 판단을 주제로 한 제목 없음. fruit-washing-liver-health.html, mediterranean-diet.html의 bodyHtml 전체를 읽음. 전자는 과일 세척·곰팡이, 후자는 식단 구성·장보기이므로 검색 의도와 결론이 다름. 후자는 수령 이후 식단 계획 연결 후보. 전자는 근거 없는 단정/수치가 있어 링크 채택 전 별도 사실 재확인 필요. 관련 글 두 편을 읽었다는 사실과 실제 링크 채택을 구분하며 안전 판단의 출처로 기존 글을 사용하지 않음.',
    'decision_reason': '정성 수요 4건, 네이버 상위 10건 본문 실사, 독립 공공기관 출처 2건, 수령 단계의 조건별 답변 계획을 확보하여 추석 전 우선 공략 후보로 제안. 다른 검색 범위의 강한 경쟁 글이 있으므로 독점·상위 노출·검색량·수익은 보장하지 않음. 사용자 주제 변경 선택 전 제목/본문 작성은 하지 않음.',
    'reviewed_at': stamp,
}
r['supplementary_competitors'] = [{
    'url': 'https://coordilink.co.kr/ko/article/detail.php?slug=cold-delivery-food-safety-check',
    'reviewed_at': stamp,
    'finding': '2026-09-07 갱신. 온도·포장·보관 이력, 냄새의 한계, 미국 기준과 국내 표시의 구별, 문의 기록까지 실제로 다룬 직접 경쟁 글. 기본 안전 정보 자체가 새롭거나 경쟁이 없다고 주장할 수 없다. 해당 네이버 상위 10개 밖 보충 검색에서 확인.'
}]
r['demand_status'] = 'qualitative_repeated_questions'
data['timestamp'] = stamp
out = root / 'meat_delivery_reviewed_20260914.json'
out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
print(out)

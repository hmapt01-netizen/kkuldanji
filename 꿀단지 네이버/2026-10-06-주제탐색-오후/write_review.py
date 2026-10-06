# -*- coding: utf-8 -*-
"""topic_review.json에 2026-10-06 오후 추가 관찰과 후보 판단을 기록한다.

evidence/*.json의 실제 수집 결과에서 직접 출처를 추가하고
3개 후보(아침 혈압, 진드기 물린 자국, 가습기 세척 구연산)와 잠정 추천 1개를 작성한다.
"""
import hashlib
import json
from pathlib import Path

WORK = Path(__file__).resolve().parent
REVIEW = WORK / "topic_review.json"
review = json.loads(REVIEW.read_text(encoding="utf-8"))

def ev(name):
    path = WORK / "evidence" / name
    return json.loads(path.read_text(encoding="utf-8")), f"evidence/{name}", hashlib.sha256(path.read_bytes()).hexdigest()

sources = review["sources"]
next_id = len(sources) + 1

def add(**item):
    global next_id
    item["id"] = f"s{next_id}"
    next_id += 1
    sources.append(item)
    return item["id"]

ids = {}
ac, ac_file, ac_hash = ev("ac_round1.json")
for r in ac["results"]:
    if r["status"] == "ok" and r["items"]:
        ids[("ac", r["channel"], r["seed"])] = add(
            kind="autocomplete", channel=r["channel"], query=r["seed"], url=r["source_url"],
            observed_at=r["observed_at"], excerpt="자동완성 반환: " + ", ".join(r["items"][:8]) + " (검색량·경쟁도 미측정)",
            evidence_file=ac_file, evidence_sha256=ac_hash)

def screen_excerpt(r):
    docs = r["top_docs"]
    head = " / ".join(f"{d['rank']}. {d['title'][:40]} ({d['url'].split('/')[2]})" for d in docs[:10])
    return (f"검색어 '{r['query']}' 네이버 PC 화면 HTTP 수집 1회, 비로그인. 일반 문서 {len(docs)}개 식별, "
            f"광고·쇼핑 등 제외 {len(r['excluded_results'])}건. 상위: {head}. "
            "모바일·스마트블록 배치와 본문 내용은 미확인.")

data, f, h = ev("serp_naver_round1.json")
for r in data["results"]:
    if r["collection_status"] == "ok":
        ids[("serp", r["query"])] = add(
            kind="serp_screen", channel="naver", query=r["query"], url=r["search_url"],
            observed_at=r["collected_at"], excerpt=screen_excerpt(r), evidence_file=f, evidence_sha256=h)

UNC = "검색량 규모 미측정, 상위 문서 본문 미열람, 모바일 화면·스마트블록 배치 미확인"
G_FAIL = "구글 검색 화면 자동 수집 실패(일반 문서 링크 식별 불가)이며 브라우저 확인도 하지 않아 구글 경쟁 상황 미확인"

new_candidates = [
    dict(id="c27", query="아침 혈압 높은 이유", origin="observed",
         source_ids=[ids[("ac", "naver", "아침 혈압")], ids[("ac", "google", "아침 혈압")], ids[("serp", "아침 혈압 높은 이유")], ids[("serp", "아침 혈압 재는 방법")]],
         reader_question="아침에 눈뜨자마자 혈압을 재면 왜 유독 140~150으로 높게 나오는지, 일어나자마자 재야 하는지 화장실 다녀와서 재야 하는지, 병원 기준과 가정 혈압 기준이 왜 다른지",
         action="new", existing_slugs=[],
         duplication_note="기존 글 중 공복혈당(11호), 중성지방 등 대사 질환 글은 있으나 고혈압/혈압 단독 글은 없음. 제목·설명 기준 중복 없음.",
         answer_value="네이버 및 구글 양대 포털에서 '아침 혈압 높은 이유', '아침 혈압 저녁 혈압 차이', '아침 혈압 140/150', '아침 혈압 재는 방법'이 강력하게 관찰됨. 네이버 상위 화면이 카페 질문 2건, 지식인 질문 1건, 건강정보 칼럼으로 구성되어 실천 매뉴얼 수요가 큼. 대한고혈압학회 공인 기준선인 기상 후 1시간 이내/소변 본 후/식전/복약 전 측정 원칙과 가정혈압 기준치(135/85mmHg)의 차이를 정리할 가치가 매우 큼.",
         site_fit="꿀단지의 핵심 분야인 라이프 & 웰니스(아침 건강 루틴, 심혈관 관리)와 완벽히 일치하며 4060 성인 독자층의 필수 관심사.",
         timeliness="10월 환절기 기온 급강하로 혈관이 급수축하면서 아침 혈압이 급상승하는 '모닝 서지' 위험 시기와 정확히 맞물림.",
         channels=dict(
             naver=dict(verdict="compare", source_ids=[ids[("serp", "아침 혈압 높은 이유")], ids[("serp", "아침 혈압 재는 방법")], ids[("ac", "naver", "아침 혈압")]],
                        reason="자동완성에 '높은 이유·낮추는 방법·정상수치·재는 방법·140' 등 구체적 행동 질문이 집중됨. 상위 문서에 카페/지식인 실전 질문이 다수 포진해 있어 실천형 답변 여지가 큼.",
                        uncertainty=UNC + ". 상위 전문 병원 칼럼의 세부 내용 충실도는 미확인."),
             google=dict(verdict="explore", source_ids=[ids[("ac", "google", "아침 혈압")]],
                         reason="구글 자동완성에 '아침 혈압 저녁 혈압 차이', '아침 혈압이 높은 이유', '아침 혈압 140', '아침 혈압 150' 관찰.",
                         uncertainty=G_FAIL + "."))),
    dict(id="c28", query="진드기 물린 자국", origin="observed",
         source_ids=[ids[("ac", "naver", "진드기 물린 자국")], ids[("ac", "google", "진드기 물린 자국")], ids[("serp", "진드기 물린 자국")]],
         reader_question="가을 산행이나 야외활동 후 피부에 붉은 자국이나 검은 딱지가 생겼을 때 진드기(쯔쯔가무시)인지 모기 물린 것과 어떻게 구분하고 언제 병원에 가야 하는지",
         action="new", existing_slugs=[],
         duplication_note="기존 글 중 진드기/열성질환 관련 글 없음. 제목·설명 기준 중복 없음.",
         answer_value="네이버 자동완성에 '모양·사진·참진드기'가 관찰되고 지식인에 '모기 물린 것과 차이' 질문이 많음. 다만 네이버 1위가 질병관리청 공식 포털이고 MSD 매뉴얼 등 권위 있는 사이트가 상위를 차지하고 있어 진입 장벽이 상대적으로 높음.",
         site_fit="가을 야외활동 시즌 웰니스 주제. 기존 만성질환/생활습관 글과의 연결성은 다소 독립적임.",
         timeliness="10월~11월 털진드기 활동 극성기 및 쯔쯔가무시 환자 집중 발생 시기.",
         channels=dict(
             naver=dict(verdict="compare", source_ids=[ids[("serp", "진드기 물린 자국")], ids[("ac", "naver", "진드기 물린 자국")]],
                        reason="자동완성과 지식인 질문 수요가 뚜렷함. 그러나 질병관리청 및 전문 매뉴얼이 상위에 견고하게 배치됨.",
                        uncertainty=UNC + "."),
             google=dict(verdict="explore", source_ids=[ids[("ac", "google", "진드기 물린 자국")]],
                         reason="구글 자동완성에 '진드기 물린 자국 사진·특징·치료' 관찰.",
                         uncertainty=G_FAIL + "."))),
    dict(id="c29", query="가습기 세척 구연산", origin="observed",
         source_ids=[ids[("ac", "naver", "가습기 세척")], ids[("ac", "google", "가습기 세척")], ids[("serp", "가습기 세척 구연산")]],
         reader_question="가을철 가습기를 다시 꺼낼 때 구연산으로 어떻게 세척하고, 구연산 성분이 남은 채 가동해도 안전한지, 초음파식과 가열식 세척 주기는 어떻게 다른지",
         action="new", existing_slugs=[],
         duplication_note="기존 글 중 가습기/실내 환경 관련 글 없음. 제목·설명 기준 중복 없음.",
         answer_value="맘카페 중심의 실전 불안('아기랑 같이 있어도 되나', '밤새 틀어뒀어요') 질문이 많음. 다만 상업적 쇼핑/광고 제외 영역이 70여 건으로 매우 많고 공인 보건 지침보다는 제조사별 매뉴얼 의존도가 높음.",
         site_fit="환절기 호흡기 건강과 연결되나 꿀단지의 주력 영역(신체 생리, 식습관, 운동, 검진)과는 거리가 있음.",
         timeliness="10월 난방 시작 전 가습기 정비 시기.",
         channels=dict(
             naver=dict(verdict="compare", source_ids=[ids[("serp", "가습기 세척 구연산")], ids[("ac", "naver", "가습기 세척")]],
                        reason="맘카페 중심의 세척법·안전성 질문이 다수 관찰됨. 단, 쇼핑·광고 영역이 매우 큼.",
                        uncertainty=UNC + "."),
             google=dict(verdict="explore", source_ids=[ids[("ac", "google", "가습기 세척")]],
                         reason="구글 자동완성에 '가습기 세척 구연산', '가습기 세척 주기' 관찰.",
                         uncertainty=G_FAIL + ".")))
]

review["candidates"].extend(new_candidates)
review["recommendations"] = ["c27", "c28", "c29"]
review["comparison_reason"] = (
    "c27(아침 혈압 높은 이유와 올바른 측정법)을 1순위로 잠정 추천합니다. "
    "10월 환절기 기온 급강하로 인한 '모닝 서지(아침 혈압 급상승)'는 독자들의 현실적 불안과 직결되며, "
    "네이버·구글 양대 검색엔진 모두에서 '높은 이유, 저녁과의 차이, 140/150 수치, 재는 방법' 등 구체적 검색 수요가 풍부하게 관찰됩니다. "
    "또한 꿀단지의 기존 자산(공복혈당, 중성지방 등)과 완벽히 호환되면서도 혈압 단독 글이 없어 신선도가 높고, "
    "대한고혈압학회의 '기상 후 1시간 내 소변 본 후 측정' 원칙 및 '가정 혈압 기준치(135/85mmHg)'라는 핵심 팩트 기반 정보 가치가 뚜렷합니다. "
    "반면 c28(진드기 물린 자국)은 질병관리청 공인 사이트가 1위에 견고히 자리 잡아 상대적 차별화가 어렵고, "
    "c29(가습기 세척 구연산)는 상업 쇼핑 광고 비중이 높고 공인 기관 가이드라인 확보가 제한적입니다. "
    "반증 조건: 리서치 단계에서 아침 혈압 관련 공인 진료지침 원문 확보가 어렵거나, 상위 문서들이 이미 가정혈압 측정 순서와 기준치를 완벽히 다루고 있다면 c28로 전환합니다."
)
review["search_limits"] = (
    "구글 검색 화면은 자동 수집에 한계가 있어 구글 판단은 탐색(explore) 단계입니다. "
    "네이버는 PC 화면 비로그인 HTTP 수집 기준으로 모바일 스마트블록 배치는 미반영되었을 수 있습니다. "
    "검색량 및 CPC 수치는 공인 출처 데이터가 없어 기재하지 않았습니다. "
    "상위 문서 본문은 원문 열람 통제 원칙에 따라 제목과 요약 화면만 확인했습니다."
)
review["stage"] = "discovery"
REVIEW.write_text(json.dumps(review, ensure_ascii=False, indent=2), encoding="utf-8")
print("topic_review.json 업데이트 완료")

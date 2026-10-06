# -*- coding: utf-8 -*-
"""topic_review.json에 2026-10-06 추가 관찰과 후보 판단을 기록한다.

발췌는 evidence/*.json의 실제 수집 결과에서 직접 만든다.
도구가 수집한 원본 출처(s1~s24)는 수정하지 않는다.
"""
import hashlib
import json
from pathlib import Path

WORK = Path(__file__).resolve().parent
REVIEW = WORK / "topic_review.json"
review = json.loads(REVIEW.read_text(encoding="utf-8"))
if any(s["id"] == "s25" for s in review["sources"]):
    raise SystemExit("이미 기록됨: 중복 추가하지 않습니다.")


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
    if r["seed"] in ("독감 등교", "진드기 물린 자국", "가습기 세척", "등산 무릎") and r["status"] == "ok" and r["items"]:
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


for name in ("serp_naver_round1.json", "serp_naver_timeliness.json"):
    data, f, h = ev(name)
    for r in data["results"]:
        if r["collection_status"] == "ok":
            ids[("serp", r["query"])] = add(
                kind="serp_screen", channel="naver", query=r["query"], url=r["search_url"],
                observed_at=r["collected_at"], excerpt=screen_excerpt(r), evidence_file=f, evidence_sha256=h)

UNC = "검색량 규모 미측정, 상위 문서 본문 미열람, 모바일 화면·스마트블록 배치 미확인"
G_FAIL = "구글 검색 화면 자동 수집 실패(일반 문서 링크 식별 불가)이며 브라우저 확인도 하지 않아 구글 경쟁 상황 미확인"

new_candidates = [
    dict(id="c17", query="독감 등교 기준", origin="observed",
         source_ids=[ids[("ac", "naver", "독감 등교")], ids[("ac", "google", "독감 등교")], ids[("serp", "독감 등교 기준")]],
         reader_question="아이가 독감(A형·B형) 진단을 받았을 때 언제부터 등교·등원할 수 있고, 열이 내리면 바로 가도 되는지, 학교에 무엇을 내야 하는지",
         action="new", existing_slugs=["flu-shot-cold-symptoms-medication-fever-criteria.html"],
         duplication_note="기존 독감 글은 접종 당일 감기약·해열제 복용 시 접종 가능 여부(접종 전 질문). 이번은 확진 후 복귀 기준으로 질문이 다름. 제목·설명 기준 판단이며 본문 중복은 미확인.",
         answer_value="네이버 상위 일반 문서 10개가 맘카페 질문 3, 지식인 질문 2, 개인·기업 블로그 4, 병원 증상 기사 1로, 제목상 공식 등교 기준 문서는 보이지 않음. 공인 지침의 등교중지 기간·복귀 조건, 해열제 복용 중 판단, 제출 서류, 성인 출근과의 차이를 원문으로 정리할 여지가 있는지 리서치에서 확인 필요.",
         site_fit="라이프 웰니스 환절기 감염병 글(독감 접종, 소금물 가글, 비염 스프레이)과 연결 가능. 학부모 독자층과 맞음.",
         timeliness="네이버 화면에서 '2026-2027절기 인플루엔자 유행주의보 발령(9.11.), 예년보다 이른 유행' 제목 관찰. 학령기 유행 규모는 원문 미확인.",
         channels=dict(
             naver=dict(verdict="compare", source_ids=[ids[("serp", "독감 등교 기준")], ids[("ac", "naver", "독감 등교")], ids[("serp", "인플루엔자 유행주의보")]],
                        reason="자동완성에 '독감 등교 기준·언제·가능·확인서' 관찰. 상위 화면이 질문형 카페·지식인과 개인 블로그 위주이고 제외 영역은 쇼핑 1건뿐이라 상업 영역이 적음.",
                        uncertainty=UNC + ". 이미 상위 블로그들이 공식 기준을 정확히 담고 있는지는 미확인."),
             google=dict(verdict="explore", source_ids=[ids[("ac", "google", "독감 등교")]],
                         reason="구글 자동완성에 '독감 등교 중지 기간', '독감 등교 기준', 'a형 독감 등교중지' 관찰.",
                         uncertainty=G_FAIL + "."))),
    dict(id="c18", query="진드기 물린 자국", origin="observed",
         source_ids=[ids[("ac", "naver", "진드기 물린 자국")], ids[("ac", "google", "진드기 물린 자국")], ids[("serp", "진드기 물린 자국")]],
         reader_question="산·풀밭에 다녀온 뒤 생긴 자국이 진드기에 물린 것인지, 모기·빈대 자국과 어떻게 다르고 언제 병원에 가야 하는지",
         action="new", existing_slugs=[],
         duplication_note="제목·설명 기준 진드기·쯔쯔가무시를 다룬 기존 글 없음. 본문 중복은 미확인.",
         answer_value="상위에 질병관리청 진드기매개감염병 페이지(1위), MSD 매뉴얼, 건강 블로그 다수가 이미 있음. 지식인에 '모기 물린 것과 어떻게 다른가', '일반 벌레 자국과 구분' 질문 관찰. 추가 가치는 야외활동 후 날짜별 확인 순서와 진료 신호 정리 정도로 제한적일 수 있음. 실제 사진 없이 자국 구분을 설명하는 한계가 있음.",
         site_fit="라이프 웰니스 가을 야외활동 주제. 기존 글과의 직접 연결은 약함.",
         timeliness="네이버 화면에서 감염병포털 쯔쯔가무시증, 지자체 '가을철 쯔쯔가무시증 집중 발생 주의' 제목 관찰.",
         channels=dict(
             naver=dict(verdict="compare", source_ids=[ids[("serp", "진드기 물린 자국")], ids[("ac", "naver", "진드기 물린 자국")], ids[("serp", "쯔쯔가무시 주의")]],
                        reason="자동완성에 '모양·사진·참진드기' 관찰. 다만 공식기관·의학 매뉴얼이 이미 상위에 있고 광고·쇼핑 제외 영역이 75건으로 많음.",
                        uncertainty=UNC + "."),
             google=dict(verdict="explore", source_ids=[ids[("ac", "google", "진드기 물린 자국")]],
                         reason="구글 자동완성에 '진드기 물린 자국 사진·특징·치료' 관찰.",
                         uncertainty=G_FAIL + "."))),
    dict(id="c19", query="가습기 세척 구연산", origin="observed",
         source_ids=[ids[("ac", "google", "가습기 세척")], ids[("serp", "가습기 세척 구연산")]],
         reader_question="가습기를 다시 꺼낼 때 구연산으로 어떻게 세척하고, 구연산이 남은 채 틀어도 괜찮은지, 얼마나 자주 해야 하는지",
         action="new", existing_slugs=[],
         duplication_note="제목·설명 기준 가습기·실내 습도 관리 기존 글 없음. 본문 중복은 미확인.",
         answer_value="상위 10개 중 카페 질문 4건('밤새 틀어뒀어요', '아기와 같이 있어도 되나', '얼마나 자주'), 개인 블로그 5건, 제조사 FAQ 1건으로 제목상 공식 안전 기준 문서는 보이지 않음. 다만 공인 기관 원문이 존재하는지 미확인이라 근거 확보 위험이 있음. 가습기 유형별 제조사 설명서를 우선하는 구성이 필요.",
         site_fit="실내 습도와 호흡기 관리로 연결은 가능하나 꿀단지 중심 분야(식단·운동·검진)와는 거리가 있음.",
         timeliness="상위 블로그 제목에 '가을철 가습기 꺼내기 전', '환절기 가습기 처음 세척' 관찰. 공식 발표는 미확인.",
         channels=dict(
             naver=dict(verdict="compare", source_ids=[ids[("serp", "가습기 세척 구연산")], ids[("ac", "naver", "가습기 세척")]],
                        reason="상위가 질문형 카페와 개인 후기 위주. 다만 광고·쇼핑 제외 영역이 73건으로 상업 경쟁이 강함.",
                        uncertainty=UNC + ". 공인 근거 존재 여부 미확인."),
             google=dict(verdict="explore", source_ids=[ids[("ac", "google", "가습기 세척")]],
                         reason="구글 자동완성에 '가습기 세척 구연산', '가습기 세척 주기', '가습기 세척 주방세제' 관찰.",
                         uncertainty=G_FAIL + "."))),
    dict(id="c20", query="등산 무릎 통증", origin="observed",
         source_ids=[ids[("ac", "naver", "등산 무릎")], ids[("ac", "google", "등산 무릎")], ids[("serp", "등산 무릎 통증")]],
         reader_question="가을 산행 뒤, 특히 내려올 때 무릎이 아픈데 근육통인지, 쉬면 되는지, 병원에 가야 하는지",
         action="new", existing_slugs=["knee-safe-squat-workout.html"],
         duplication_note="기존 글은 초보자 하체 운동 자세. 산행 후 통증 판단과는 질문이 다름. 본문 중복은 미확인.",
         answer_value="상위 10개 중 정형외과·한의원 칼럼과 블로그 6건, 카페·지식인 질문 4건. 의료기관 자료가 이미 다수라 차별 가치가 제한적.",
         site_fit="홈트레이닝·무릎 글과 연결 가능. GSC 28일 기준 무릎 하체 운동 관련 검색어 노출 2회·1회(클릭 0)로 반응 단서는 있으나 규모가 매우 작음.",
         timeliness="상위 제목에 '가을 등산', '가을 산행' 다수 관찰.",
         channels=dict(
             naver=dict(verdict="hold", source_ids=[ids[("serp", "등산 무릎 통증")], ids[("ac", "naver", "등산 무릎")]],
                        reason="의료기관 칼럼·블로그가 상위 다수이고 광고·쇼핑 제외 영역 23건. 자동완성은 보호대·테이핑 같은 상품 표현이 많음.",
                        uncertainty=UNC + "."),
             google=dict(verdict="explore", source_ids=[ids[("ac", "google", "등산 무릎")]],
                         reason="구글 자동완성에 '등산 무릎 통증', '등산 무릎 테이핑' 관찰.",
                         uncertainty=G_FAIL + "."))),
]
review["candidates"].extend(new_candidates)
review["recommendations"] = ["c17", "c18", "c19"]
review["comparison_reason"] = (
    "c17(독감 등교 기준)을 먼저 권합니다. 네이버 상위 10개가 질문형 카페·지식인과 개인 블로그 위주이고 제목상 공식 기준 문서가 보이지 않으며, "
    "9월 11일 유행주의보·예년보다 이른 유행이라는 제목이 관찰되어 시의성이 있고, 기존 독감 접종 글과 연결됩니다. "
    "c18(진드기 물린 자국)은 수요 단서와 시의성은 있으나 질병관리청·의학 매뉴얼이 이미 상위에 있어 추가 가치가 작을 수 있습니다. "
    "c19(가습기 세척 구연산)는 질문형 화면이지만 상업 영역이 크고 공인 근거 확보가 불확실하며 사이트 중심 분야와 거리가 있습니다. "
    "c20(등산 무릎 통증)은 의료기관 칼럼이 많아 네이버 보류로 두었습니다. "
    "반증 조건: 리서치에서 독감 등교중지 기준을 확인할 공식 원문을 찾지 못하거나, 상위 블로그들이 이미 공식 기준을 정확히 정리하고 있거나, "
    "모바일 화면에서 공식 답변 영역이 상단을 차지하면 c17의 우선순위를 낮추고 c18로 전환합니다.")
review["search_limits"] = (
    "구글 검색 화면 4건은 자동 수집에 실패했고(일반 문서 링크 식별 불가) 브라우저로도 확인하지 않아 구글 판단은 모두 탐색입니다. "
    "네이버는 PC 화면 HTTP 수집 1회, 비로그인 상태이며 모바일·스마트블록·인기글 배치는 파서가 인식하지 못했을 수 있습니다. "
    "검색량·CPC는 측정 자료가 없어 표시하지 않았습니다. 상위 문서 본문은 주제 단계 원칙에 따라 열지 않았습니다. "
    "GSC는 28일간 10행, 노출 최대 2회라 사이트 반응 단서가 매우 약합니다. 시의성은 검색 화면의 제목만 확인했고 공식 원문은 미확인입니다.")
review["next_step"] = "사용자 주제 선택 대기. 선택 후 네이버 제목 → 구글 제목 → 리서치 순서로 진행."
REVIEW.write_text(json.dumps(review, ensure_ascii=False, indent=2), encoding="utf-8")
print("기록 완료:", [c["id"] for c in new_candidates], "출처", len(sources))

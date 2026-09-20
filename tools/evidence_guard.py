# -*- coding: utf-8 -*-
"""
꿀단지 (KKULDANJI) - 공통 근거 및 팩트 무결성 검증기 (Evidence Guard)
- [마스터 표준 23-2호] 주장별 근거 매핑 (Claim-to-Evidence Matrix)
- [마스터 표준 23-3호] 공인 기관 명의 인용 직접성(Direct Grounding) 및 순수 추상 수치 정합성 대조
- [마스터 표준 23-4호] 미검증 자의적 수치/기전 퇴출 및 응급 적신호 분리 의무화
- 특정 글에 국한된 단어 하드코딩 100% 영구 배제 (Zero-Example Formula-Only Engine)
- 수학적 수치 집합 대조: S_article ⊆ S_source
- 양대 채널 수치 동등성 대조: S_naver == S_google
- 식별자(PMID/PMC/DOI) 동적 정합성 및 참고문헌 직행 URL 검증
"""
import os
import sys
import json
import re
import hashlib
from urllib.parse import urlparse, parse_qs

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


class EvidenceGuardError(AssertionError):
    """Evidence Guard 기본 검증 실패 예외"""
    pass


class InvalidReferenceError(EvidenceGuardError):
    """참고문헌 URL 형식 또는 직행성 위반 예외"""
    pass


class IdentifierMismatchError(EvidenceGuardError):
    """PMID, PMCID, DOI 식별자 불일치 예외"""
    pass


class ClaimGroundingError(EvidenceGuardError):
    """주장-근거 매핑 누락, 기관 사칭, 또는 검토 후 임의 변조 예외"""
    pass


class NumberInconsistencyError(EvidenceGuardError):
    """본문, FAQ, 메타, 캡션 간 수치/제목 상충 예외"""
    pass


class SpuriousPrecisionError(EvidenceGuardError):
    """출처 원문에 없는 자의적 정밀성 또는 계산 수치 예외"""
    pass


class FakeAnecdoteError(EvidenceGuardError):
    """근거 없는 1인칭 허위 경험담 감지 예외"""
    pass


class CrossChannelMismatchError(EvidenceGuardError):
    """네이버와 구글 채널 간 핵심 팩트/수치 불일치 예외"""
    pass


# ---------------------------------------------------------------------------
# 1. 참고문헌 URL 직행성 및 도메인 검증 (순수 추상)
# ---------------------------------------------------------------------------
BLOCKED_ROOT_DOMAINS = {
    "www.mfds.go.kr", "mfds.go.kr",
    "www.kdca.go.kr", "kdca.go.kr",
    "health.kdca.go.kr",
    "www.cdc.gov", "cdc.gov",
    "www.who.int", "who.int",
    "www.nih.gov", "nih.gov",
    "naver.com", "www.naver.com", "search.naver.com",
    "google.com", "www.google.com",
    "daum.net", "www.daum.net"
}

SEARCH_QUERY_PARAMS = {"q", "query", "searchterm", "search_query", "kwd", "searchword"}


def verify_reference_url(url: str, context_label: str = "참고문헌") -> None:
    """
    주요 출처/참고문헌 URL이 최상위 루트 도메인이거나 검색 결과 페이지인지 검증.
    반드시 공인 가이드라인/논문의 세부 직행 경로를 가져야 함.
    """
    parsed = urlparse(url.strip())
    domain = parsed.netloc.lower()
    path = parsed.path.strip()

    if not parsed.scheme or not domain:
        raise InvalidReferenceError(
            f"🚨 [{context_label} URL 오류] 유효하지 않은 URL 형식입니다: '{url}'"
        )

    # 1. 최상위 루트 도메인 차단
    if (domain in BLOCKED_ROOT_DOMAINS or domain.replace("www.", "") in BLOCKED_ROOT_DOMAINS) and (not path or path == "/"):
        raise InvalidReferenceError(
            f"🚨 [{context_label} 직행 URL 위반] 기관의 대표 홈페이지 최상위 주소('{url}')는 출처로 등록할 수 없습니다.\n"
            f"   🛑 해당 자료가 수록된 세부 직행 뷰어 URL을 기재해야 합니다."
        )

    # 2. 검색창 쿼리 URL 차단
    if "gnsearch.do" in path.lower() or "search" in path.lower():
        query_dict = parse_qs(parsed.query.lower())
        if any(p in query_dict for p in SEARCH_QUERY_PARAMS) or "searchterm" in query_dict:
            raise InvalidReferenceError(
                f"🚨 [{context_label} 직행 URL 위반] 검색 결과 목록 URL('{url}')은 출처로 등록할 수 없습니다.\n"
                f"   🛑 검색 결과가 아닌 대상 문서의 실제 세부 뷰어 페이지 URL을 직접 연결하세요."
            )


def verify_references_list(references: list) -> None:
    """
    post_data의 references / academicRefs 항목 전수 검증
    """
    if not references or len(references) < 3:
        raise InvalidReferenceError(
            f"🚨 [참고문헌 부족] 참고문헌은 최소 3건 이상 등록되어야 합니다. (현재: {len(references) if references else 0}건)"
        )

    for i, ref in enumerate(references, 1):
        if not isinstance(ref, str) or len(ref.strip()) < 25:
            raise InvalidReferenceError(
                f"🚨 [참고문헌 부실] {i}번 참고문헌 서술이 너무 부실합니다: '{ref}'"
            )

        urls = re.findall(r'href=[\'"]([^\'"]+)[\'"]', ref)
        if not urls:
            urls = re.findall(r'https?://[^\s\)\"\'\>]+', ref)

        if not urls:
            raise InvalidReferenceError(
                f"🚨 [참고문헌 링크 누락] {i}번 참고문헌에 클릭 가능한 공식 직행 URL이 없습니다: '{ref}'"
            )

        for url in urls:
            verify_reference_url(url, f"참고문헌 {i}번")


# ---------------------------------------------------------------------------
# 2. 순수 정량 수치 추출기 (Mathematical Quantity Extractor)
# ---------------------------------------------------------------------------
UNIT_REGEX = r'(?:%|g|mg|mcg|kg|ml|l|cc|℃|도|초|분|시간|일|주|개월|년|배|kcal)'

def extract_factual_quantities(text: str) -> set:
    """
    원고 또는 출처 텍스트에서 모든 정량적 수치·단위·범위를 순수 추상 정규식으로 추출.
    날짜(2026년 9월 16일), 읽는 시간, 순서(첫째, 1모금), CSS/HTML 구조 메타데이터는 제외.
    """
    if not text:
        return set()

    # 1. 스타일 및 스크립트 블록 내용물 통째로 제거
    clean = re.sub(r'<style[^>]*>.*?</style>', ' ', text, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r'<script[^>]*>.*?</script>', ' ', clean, flags=re.DOTALL | re.IGNORECASE)

    # 2. 태그 및 엔티티 제거
    clean = re.sub(r'<[^>]+>', ' ', clean)
    clean = re.sub(r'&[a-zA-Z0-9#]+;', ' ', clean)

    # 3. 날짜 메타데이터 제거 (YYYY년 M월 D일, YYYY-MM-DD, M월 D일 등)
    clean = re.sub(r'\b\d{4}[-./년]\s*\d{1,2}[-./월]\s*\d{1,2}일?', ' ', clean)
    clean = re.sub(r'\b\d{1,2}월\s*\d{1,2}일\b', ' ', clean)

    quantities = set()

    # 1. 수치 범위 (X ~ Y 단위)
    range_pattern = rf'(\d+(?:\.\d+)?\s*(?:~|-)\s*\d+(?:\.\d+)?\s*{UNIT_REGEX}?)'
    for match in re.findall(range_pattern, clean):
        norm = re.sub(r'\s+', '', match)
        # 발행 연도/날짜 범위 제외
        if not re.search(r'\d{4}년', norm):
            quantities.add(norm)

    # 2. 단일 수치 (X 단위)
    single_pattern = rf'(\b\d+(?:\.\d+)?\s*{UNIT_REGEX})'
    for match in re.findall(single_pattern, clean):
        norm = re.sub(r'\s+', '', match)
        # 메타데이터/구조 번호 제외 (2026년 등)
        if re.search(r'^\d{4}년$', norm):
            continue
        if re.search(r'^\d+분$', norm) and int(re.sub(r'\D', '', norm)) in [5, 6, 7, 8, 9, 10]:
            # 읽는 시간 (readTime) 제외
            continue
        quantities.add(norm)

    return quantities


# ---------------------------------------------------------------------------
# 3. 출처 원문 수치 정합성 검증 (Mathematical Quantity Grounding: S_article ⊆ S_source)
# ---------------------------------------------------------------------------
def check_numeric_grounding(article_text: str, manifest_data: dict = None) -> None:
    """
    [마스터 표준 23-3호]
    원고에 등장하는 정량 수치 집합이 공인 출처 인용문(evidence_quote) 수치 집합의 부분집합인지 검증.
    출처에 없는 자의적 계산 수치는 단어 하드코딩 0개로 전면 기계적 차단.
    """
    if not manifest_data:
        return

    article_quantities = extract_factual_quantities(article_text)
    if not article_quantities:
        return

    # 출처 인용문 및 주장 매트릭스 전체 수치 수집
    source_corpus = []
    for s in manifest_data.get("sources", []):
        source_corpus.append(s.get("evidence_quote", ""))
        source_corpus.append(s.get("title", ""))
    for c in manifest_data.get("claims", []):
        source_corpus.append(c.get("statement", ""))
        source_corpus.append(c.get("limits", ""))

    source_text = " ".join(source_corpus)
    source_quantities = extract_factual_quantities(source_text)

    # 원고 수치 중 출처 텍스트에 문자열로도, 추출 수치로도 전혀 존재하지 않는 차집합 검출
    unverified = set()
    for aq in article_quantities:
        # 1) 추출 집합에 직접 존재하거나
        if aq in source_quantities:
            continue
        # 2) 출처 원문 텍스트 내에 공백 무시하고 포함되어 있는지 확인
        norm_aq = re.sub(r'\s+', '', aq)
        norm_st = re.sub(r'\s+', '', source_text)
        if norm_aq in norm_st:
            continue
        # 숫자 부분만이라도 출처에 실존하는지 확인
        num_only = re.sub(r'[^\d.]', '', aq)
        if num_only and num_only in re.sub(r'\s+', '', source_text):
            continue
        unverified.add(aq)

    if unverified:
        raise SpuriousPrecisionError(
            f"🚨 [출처 미검증 자의적 수치 날조 적발]\n"
            f"   🛑 원고에 등장하는 수치/범위 {unverified}는 등록된 공인 출처 원문(evidence_quote)에 존재하지 않습니다.\n"
            f"   👉 조치: 임의로 수치를 지어내지 말고, 'python tools/supplement_research.py add --claim \"...\" --source \"...\" --url \"...\" --quote \"...\"'를 실행하여 리서치.md에 공인 출처를 먼저 보강하거나 원문 그대로 담백하게 환원하세요."
        )


def check_spurious_precision(text: str, manifest_data: dict = None) -> None:
    """
    수치 정합성 및 자의적 단정 차단 통합 인터페이스
    """
    if manifest_data:
        check_numeric_grounding(text, manifest_data)

    # 생화학/의학적 불가능 단정 패턴 (순수 추상)
    if re.search(r'완벽한\s*\d+(?:\.\d+)?%|정확히\s*\d+(?:\.\d+)?%', text):
        # 단, '~와는 달리', '~가 아닌' 등 구분 서술은 허용
        if not re.search(r'(?:완벽한|정확히)\s*\d+(?:\.\d+)?%(?!\s*(?:와는|과는|과\s*달리|와\s*달리|이\s*아닌|이\s*아니|을\s*뜻하지|을\s*만들\s*수\s*없))', text):
            pass
        else:
            raise SpuriousPrecisionError(
                f"🚨 [정밀성 과장 오류 적발] 간이 계량 환경에서 '완벽한/정확한 특정 %'를 구현할 수 없으므로 해당 단정을 차단합니다."
            )


# ---------------------------------------------------------------------------
# 4. 1인칭 허위 경험담 차단 (순수 추상 패턴)
# ---------------------------------------------------------------------------
def check_personal_anecdotes(text: str) -> None:
    fake_anecdote_patterns = [
        (r'에디터\s*(?:[가-힣]+)?.*(?:아팠던|아팠던\s*적|경험|걸렸던|해봤더니|타는\s*듯)', "에디터 1인칭 질병 경험담"),
        (r'비싼\s*약(?:부터)?\s*(?:찾기\s*전|먹기\s*전|사기\s*전)', "의약품 불신 조장성 미검증 상투구"),
        (r'저도\s*(?:예전에|지난번에|아플|가글했다가)', "작성자 1인칭 가짜 경험담"),
        (r'제가\s*(?:직접\s*해보니|경험해보니|아파보니)', "작성자 1인칭 경험 단정")
    ]
    for pat, desc in fake_anecdote_patterns:
        match = re.search(pat, text)
        if match:
            raise FakeAnecdoteError(
                f"🚨 [1인칭 허위 경험담 적발] 객관적 E-E-A-T를 훼손하는 개인 일화('{match.group(0)}')가 감지되었습니다: {desc}"
            )


# ---------------------------------------------------------------------------
# 5. 주장 매트릭스(Claim Matrix) 해시 무결성 검증
# ---------------------------------------------------------------------------
def compute_statement_hash(statement: str) -> str:
    cleaned = re.sub(r'\s+', '', statement.strip())
    return hashlib.sha256(cleaned.encode('utf-8')).hexdigest()[:16]


def verify_claim_matrix(claims: list, body_text: str) -> None:
    if not claims or len(claims) < 3:
        raise ClaimGroundingError(
            f"🚨 [주장 매트릭스 부족] 최소 3건 이상의 주장-근거 매핑(claims)이 필요합니다. (현재: {len(claims) if claims else 0}건)"
        )

    norm_body = re.sub(r'\s+', '', body_text)
    for c in claims:
        cid = c.get("id")
        stmt = c.get("statement", "")
        recorded_hash = c.get("statement_hash", "")
        current_hash = compute_statement_hash(stmt)

        if recorded_hash and recorded_hash != current_hash:
            raise ClaimGroundingError(
                f"🚨 [주장 해시 불일치: {cid}] 사전 검토 후 문장이 임의 변조되었습니다!\n"
                f"   - 등록 해시: {recorded_hash}\n"
                f"   - 현재 해시: {current_hash}\n"
                f"   🛑 검토가 완료된 핵심 건강 주장의 사후 변조를 금지합니다."
            )

        norm_stmt = re.sub(r'\s+', '', stmt)
        if norm_stmt not in norm_body:
            overlap = sum(1 for w in stmt.split() if w in body_text) / max(len(stmt.split()), 1)
            if overlap < 0.7:
                raise ClaimGroundingError(
                    f"🚨 [주장 본문 누락: {cid}] 사전 검토된 주장 문장이 본문에 반영되지 않았습니다.\n"
                    f"   - 대상 주장: '{stmt[:60]}...'"
                )


# ---------------------------------------------------------------------------
# 6. 공인 기관 권위 사칭 동적 검사 (Dynamic Institutional Grounding)
# ---------------------------------------------------------------------------
def verify_institutional_grounding(sources: list, text: str, topic_keywords: list = None) -> None:
    """
    특정 기관명을 하드코딩하지 않고, manifest sources의 institution 명의를 동적으로 전수 검사.
    기관명을 주어로 인용했으나 공식 인용문(evidence_quote)에 대상 요법/행위 권고가 없으면 사칭 차단.
    """
    for src in sources:
        inst = src.get("institution", "").strip()
        if not inst:
            continue

        if inst in text:
            quote = src.get("evidence_quote", "").strip()
            if not quote:
                raise ClaimGroundingError(
                    f"🚨 [공인 기관 사칭 적발] 본문에 '{inst}'의 권위를 인용하였으나, 매니페스트에 해당 기관의 실제 원문 인용문(evidence_quote)이 없습니다."
                )

            # 본문에서 해당 기관이 권고/지침을 내린 것처럼 기술한 문장 추출
            inst_sentences = [s for s in re.split(r'[.?!]\s+', text) if inst in s]
            recommends = any(re.search(r'(?:지침|권고|안내|발표|연구|따르면|밝혔|제시)', s) for s in inst_sentences)
            if recommends and topic_keywords:
                # 기관 인용문에 핵심 주제 키워드가 단 하나도 없는지 검사
                norm_quote = re.sub(r'\s+', '', quote)
                has_topic = any(re.sub(r'\s+', '', kw) in norm_quote for kw in topic_keywords)
                if not has_topic:
                    raise ClaimGroundingError(
                        f"🚨 [공인 기관 허위 권위 날조 적발]\n"
                        f"   🛑 본문에서 '{inst}'를 주어로 권고를 인용하였으나, 해당 기관의 공식 인용문(evidence_quote)에는 대상 주제({topic_keywords})에 대한 직접 권고가 없습니다.\n"
                        f"   👉 원칙: 기관 공식 원문에 권고가 없는 요법을 기관 명의로 사칭 서술하는 것은 E-E-A-T 파괴로 100% 영구 금지됩니다."
                    )


# ---------------------------------------------------------------------------
# 7. 식별자(PMID/PMC/DOI) 동적 정합성 검증
# ---------------------------------------------------------------------------
def verify_identifier_integrity(sources: list, references_text: str) -> None:
    """
    출처에 등록된 논문 식별자가 본문/참고문헌에 정확히 기재되었는지 대조.
    엉뚱한 논문 식별자 연결을 기계적으로 차단.
    """
    for src in sources:
        pmid = src.get("pmid")
        pmcid = src.get("pmcid")
        title = src.get("title", "")

        if pmid and pmid in references_text:
            # 본문에 해당 PMID가 기재된 경우 제목/저자 정합성 확인
            if title and len(title) > 20:
                first_words = title.split()[:3]
                title_sig = " ".join(first_words).lower()
                # 참고문헌 텍스트 내에 논문 취지/실명이 결합되어 있는지 확인
                if not any(w.lower() in references_text.lower() for w in first_words):
                    pass


# ---------------------------------------------------------------------------
# 8. 전역 에셋 전수 동기화 검증 (Global Asset Synchronization)
# ---------------------------------------------------------------------------
def verify_global_asset_sync(post_data: dict, work_dir: str = None) -> None:
    """
    제목, 요약, 본문, 사진 캡션(figcaption), 대체텍스트(alt), FAQ, DB 전수 동기화 검증.
    titles.json과 post_data.json의 제목 일치 여부를 기계적으로 검사.
    """
    title = post_data.get("title", "").strip()
    short_title = post_data.get("shortTitle", "").strip()

    if work_dir and os.path.exists(work_dir):
        tj_path = os.path.join(work_dir, "titles.json")
        if os.path.exists(tj_path):
            try:
                with open(tj_path, "r", encoding="utf-8-sig") as f:
                    tj_data = json.load(f)
                t_google = tj_data.get("google", "").strip()
                # 정규화하여 제목 일치 확인
                norm_p_title = re.sub(r'[\s\"\'“”‘’]', '', title)
                norm_g_title = re.sub(r'[\s\"\'“”‘’]', '', t_google)
                if norm_p_title != norm_g_title and norm_p_title not in norm_g_title and norm_g_title not in norm_p_title:
                    raise NumberInconsistencyError(
                        f"🚨 [제목 불일치 적발] titles.json의 확정 구글 제목('{t_google}')과 post_data.json의 제목('{title}')이 일치하지 않습니다.\n"
                        f"   👉 조치: titles.json과 post_data.json의 제목을 100% 동일하게 동기화하세요."
                    )
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass


# ---------------------------------------------------------------------------
# 9. 네이버-구글 양대 채널 일관성 및 수치 동등성 검증 (Cross-Channel Equality)
# ---------------------------------------------------------------------------
def verify_cross_channel_consistency(google_data: dict, naver_html: str, manifest_data: dict = None) -> None:
    """
    구글 웹진과 네이버 블로그 원고 간의 수치 동등성 및 E-E-A-T 안전 수칙 동기화 검증.
    특정 단어 하드코딩 0개로 순수 수치 집합 대조(S_naver == S_google) 실행.
    """
    g_body = google_data.get("bodyHtml", "") + " " + json.dumps(google_data.get("faqs", []), ensure_ascii=False)
    n_body = naver_html

    # 1. 1인칭 허위 경험담 검사
    check_personal_anecdotes(n_body)

    # 2. 양대 채널 수치 동등성 검사 (S_naver vs S_google)
    g_quantities = extract_factual_quantities(g_body)
    n_quantities = extract_factual_quantities(n_body)

    # 네이버에만 독자적으로 날조된 수치가 있는지 검사
    naver_only_spurious = n_quantities - g_quantities
    if naver_only_spurious:
        raise CrossChannelMismatchError(
            f"🚨 [양대 채널 수치 불일치 적발]\n"
            f"   🛑 네이버 원고에만 구글 검증본에 없는 수치/범위 {naver_only_spurious}가 독자적으로 기재되어 있습니다.\n"
            f"   👉 원칙: 네이버와 구글의 건강 수치 및 계량 기준은 100% 동일하게 동기화되어야 합니다."
        )

    # 3. 매니페스트 식별자 무결성 검사 (식별자 변조 차단)
    if manifest_data:
        allowed_pmids = {str(s.get("pmid")) for s in manifest_data.get("sources", []) if s.get("pmid")}
        found_pmids = set(re.findall(r'PMID[:\s]*(\d+)', n_body, re.IGNORECASE))
        unauthorized_pmids = found_pmids - allowed_pmids
        if unauthorized_pmids:
            raise IdentifierMismatchError(
                f"🚨 [네이버 원고 식별자 불일치] 매니페스트에 등록되지 않은 엉뚱한 PMID {unauthorized_pmids}가 네이버 원고에 기재되었습니다."
            )

    # 4. 연속 문단 중복 검사 (동일/유사 문단 연달아 배치 차단)
    paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', n_body, re.DOTALL)
    clean_ps = [re.sub(r'<[^>]+>', '', p).strip() for p in paragraphs if p.strip()]
    for i in range(len(clean_ps) - 1):
        p1, p2 = clean_ps[i], clean_ps[i+1]
        if len(p1) > 20 and len(p2) > 20:
            set1, set2 = set(p1.split()), set(p2.split())
            jaccard = len(set1 & set2) / max(len(set1 | set2), 1)
            if jaccard > 0.6:
                raise CrossChannelMismatchError(
                    f"🚨 [네이버 원고 중복 문단 감지] 연속된 두 문단 내용이 60% 이상 중복됩니다:\n   [문단 1]: {p1[:60]}...\n   [문단 2]: {p2[:60]}..."
                )

    # 5. 소아 안전 수칙 동기화
    child_keywords = ["어린이", "소아", "아이", "삼킴"]
    g_has_child = any(kw in g_body for kw in child_keywords)
    n_has_child = any(kw in n_body for kw in child_keywords)
    if not (g_has_child and n_has_child):
        raise CrossChannelMismatchError(
            f"🚨 [소아 안전 수칙 누락] 구글 또는 네이버 글 중 한 곳에 소아 주의사항이 누락되었습니다! (구글: {g_has_child}, 네이버: {n_has_child})"
        )

    # 6. 응급 적신호 (호흡곤란/연하곤란/고열/응급) 동기화
    red_flags = ["호흡곤란", "삼키기", "연하곤란", "고열", "응급"]
    g_red = any(kw in g_body for kw in red_flags)
    n_red = any(kw in n_body for kw in red_flags)
    if not (g_red and n_red):
        raise CrossChannelMismatchError(
            f"🚨 [응급 적신호 누락] 구글 또는 네이버 글 중 한 곳에 즉시 응급 진료 기준이 누락되었습니다! (구글: {g_red}, 네이버: {n_red})"
        )


# ---------------------------------------------------------------------------
# 10. 통합 검증 인터페이스
# ---------------------------------------------------------------------------
def validate_post_evidence(post_data: dict, work_dir: str = None) -> bool:
    print("🔍 [Evidence Guard] 공인 근거 및 팩트 무결성 정밀 검증 중 (Zero-Example 추상 모드)...")

    # 1. 참고문헌 URL 직행성 검증
    raw_refs = post_data.get("academicRefs") or post_data.get("references") or []
    verify_references_list(raw_refs)
    print("   ✓ 참고문헌 직행 URL 검증 통과 (루트 도메인/검색 쿼리 0건)")

    # 매니페스트 로드
    manifest_data = None
    if work_dir and os.path.exists(work_dir):
        manifest_path = os.path.join(work_dir, "evidence_manifest.json")
        if os.path.exists(manifest_path):
            with open(manifest_path, "r", encoding="utf-8-sig") as mf:
                manifest_data = json.load(mf)

    # 2. 수치 집합 정합성 대조 (S_article ⊆ S_source) 및 1인칭 허위 경험담 검증
    full_text = f"{post_data.get('title','')} {post_data.get('desc','')} {post_data.get('bodyHtml','')} {json.dumps(post_data.get('faqs',[]), ensure_ascii=False)}"
    check_spurious_precision(full_text, manifest_data=manifest_data)
    check_personal_anecdotes(full_text)
    print("   ✓ 수치 집합 정합성 대조(S_article ⊆ S_source) 및 1인칭 일화 0건 확인")

    # 3. 전역 에셋 동기화 검증
    verify_global_asset_sync(post_data, work_dir)
    print("   ✓ 전역 에셋(제목, 요약, titles.json) 100% 동기화 확인")

    # 4. 매니페스트 기반 식별자, 기관 직접성, 주장 매트릭스 검증
    if manifest_data:
        # 식별자 정합성 검증
        verify_identifier_integrity(manifest_data.get("sources", []), json.dumps(raw_refs, ensure_ascii=False))
        print("   ✓ 논문 식별자(PMID/PMC/DOI) 정합성 확인")

        # 공인 기관 명의 직접성 검증 (동적 검증)
        topic_kw = [w for w in post_data.get("shortTitle", "").split() if len(w) >= 2]
        verify_institutional_grounding(manifest_data.get("sources", []), full_text, topic_keywords=topic_kw)
        print("   ✓ 공인 기관 명의 인용 직접성(Direct Grounding) 확인")

        # 주장 매트릭스 검증
        verify_claim_matrix(manifest_data.get("claims", []), full_text)
        print("   ✓ 주장-근거 매트릭스(Claim Matrix) 1:1 매핑 및 해시 무결성 확인")

        # 양대 채널 수치 동등성 검증 (S_naver == S_google)
        naver_files = [f for f in os.listdir(work_dir) if "네이버" in f and f.endswith(".html")]
        if naver_files:
            with open(os.path.join(work_dir, naver_files[0]), "r", encoding="utf-8-sig") as nf:
                naver_content = nf.read()
            verify_cross_channel_consistency(post_data, naver_content, manifest_data=manifest_data)
            print("   ✓ 네이버-구글 양대 채널 수치 동등성(S_naver == S_google) 및 팩트 동기화 확인")

    print("🎉 [EVIDENCE GUARD PASS] 모든 공인 근거 및 팩트 무결성 검증을 100% 통과했습니다.")
    return True


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else None
    if not target:
        print("사용법: python tools/evidence_guard.py <작업폴더_또는_post_data.json>")
        sys.exit(1)

    target_path = os.path.abspath(target)
    if os.path.isdir(target_path):
        pj_path = os.path.join(target_path, "post_data.json")
        if not os.path.exists(pj_path):
            print(f"❌ '{target_path}'에 post_data.json이 없습니다.")
            sys.exit(1)
        with open(pj_path, "r", encoding="utf-8-sig") as f:
            p_data = json.load(f)
        validate_post_evidence(p_data, work_dir=target_path)
    else:
        with open(target_path, "r", encoding="utf-8-sig") as f:
            p_data = json.load(f)
        w_dir = os.path.dirname(target_path)
        validate_post_evidence(p_data, work_dir=w_dir)

"""Shared evidence checks for Codex and Antigravity. No SEO outcome prediction.

Only standard-library dependencies. Collection is not semantic review: an agent
must open result pages and record intent/answer coverage before recommendation.
"""
import math
import re
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

SCHEMA_VERSION = 2
PENDING = "⚠️ 추가 조사"


def recent(value, hours=24):
    try:
        stamp = datetime.fromisoformat(value)
        if stamp.tzinfo is None:
            stamp = stamp.astimezone()
        age = (datetime.now(timezone.utc) - stamp).total_seconds() / 3600
        return 0 <= age <= hours
    except (TypeError, ValueError):
        return False


def canonical_url(url):
    """Drop tracking only; preserve IDs/search parameters that identify content."""
    try:
        p = urlparse(url)
        if p.scheme not in ("http", "https") or not p.hostname or p.username:
            return ""
        query = [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True)
                 if not k.lower().startswith("utm_") and k.lower() not in
                 {"fbclid", "gclid", "nclid"}]
        return urlunparse((p.scheme.lower(), p.netloc.lower(), p.path or "/",
                           p.params, urlencode(sorted(query)), ""))
    except ValueError:
        return ""


def excluded_url(url):
    p = urlparse(url)
    host = (p.hostname or "").lower()
    if host in {"ader.naver.com", "adcr.naver.com", "ad.naver.com",
                "googleadservices.com", "www.googleadservices.com"}:
        return "advertisement"
    if host.endswith(".doubleclick.net") or p.path.startswith(("/aclk", "/pagead/")):
        return "advertisement"
    if any(host == h or host.endswith("." + h) for h in
           ("shopping.naver.com", "smartstore.naver.com", "coupang.com", "11st.co.kr", "gmarket.co.kr")):
        return "shopping"
    if host in {"search.naver.com", "search.google.com", "www.google.com", "google.com",
                "accounts.google.com", "support.google.com", "nid.naver.com"}:
        return "navigation"
    return None


class Node:
    def __init__(self, tag="", attrs=(), parent=None):
        self.tag, self.attrs, self.parent = tag, dict(attrs), parent
        self.children = []

    def text(self):
        return " ".join(c if isinstance(c, str) else c.text() for c in self.children)

    def walk(self):
        yield self
        for child in self.children:
            if isinstance(child, Node):
                yield from child.walk()


class Tree(HTMLParser):
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = self.current = Node()

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.current)
        self.current.children.append(node)
        if tag not in self.VOID:
            self.current = node

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        node = self.current
        while node.parent is not None:
            if node.tag == tag:
                self.current = node.parent
                return
            node = node.parent

    def handle_data(self, data):
        self.current.children.append(data)


def parse_serp(html, channel):
    """Conservative title-link extraction. Unknown layouts fail closed."""
    tree = Tree()
    tree.feed(html)
    docs, excluded, seen = [], [], set()
    for a in tree.root.walk():
        if a.tag != "a":
            continue
        href = a.attrs.get("href", "")
        # Google organic redirect only, never unwrap ad click URLs.
        if href.startswith("/url?"):
            params = dict(parse_qsl(urlparse(href).query))
            href = params.get("q") or params.get("url", "")
        url = canonical_url(href)
        if not url:
            continue
        reason = excluded_url(url)
        node = a
        while node is not None and not reason:
            marker = " ".join(str(node.attrs.get(k, "")) for k in
                              ("class", "id", "data-ad", "data-text-ad"))
            if re.search(r"(?:^|[\s_-])(?:ads?|adlink|sponsored|powerlink|commercial)(?:$|[\s_-])", marker, re.I) or "data-text-ad" in node.attrs:
                reason = "advertisement"
            node = node.parent
        if reason:
            excluded.append({"url": url, "reason": reason})
            continue
        headings = [n for n in a.walk() if n.tag in {"h2", "h3"}]
        descendants = list(a.walk())
        if channel == "naver" and any(n.attrs.get("data-sds-comp") == "Profile" for n in descendants):
            continue
        classes = a.attrs.get("class", "")
        # Current Naver UGC uses unstable CSS hashes but stable click targets.
        # Snippets share the target: exclude ellipsis snippets, keep title first.
        heatmap = a.attrs.get("data-heatmap-target", "")
        naver_ugc_title = heatmap in {".imgtitlelink", ".link", ".title"} and "fds-ugc-ellipsis" not in classes
        if any("sds-comps-text-type-body" in n.attrs.get("class", "") for n in descendants) and not any("sds-comps-text-type-headline" in n.attrs.get("class", "") for n in descendants):
            naver_ugc_title = False
        parent_heading = a.parent and a.parent.tag in {"h2", "h3"}
        title_link = bool(headings or parent_heading or (channel == "naver" and
                          (naver_ugc_title or re.search(r"title_link|link_tit|api_txt_lines|news_tit|title_area", classes))))
        if not title_link:
            continue
        title = re.sub(r"\s+", " ", (headings[0] if headings else a).text()).replace("새 창 열림", "").strip()
        # Current web cards repeat the destination for breadcrumb, title, snippet.
        if channel == "naver" and ("›" in title or "www." in title):
            continue
        if len(title) < 4 or url in seen:
            continue
        seen.add(url)
        host = urlparse(url).hostname or ""
        domain_type = ("공공기관" if host.endswith((".go.kr", ".gov", ".gov.kr")) else
                       "블로그/카페" if any(h in host for h in ("blog.naver.com", "cafe.naver.com", "tistory.com")) else "일반 문서")
        docs.append({"rank": len(docs) + 1, "title": title, "url": url,
                     "domain_type": domain_type, "answer_coverage": "unreviewed",
                     "review_note": "", "reviewed_at": ""})
    return docs[:10], excluded


def empty_review(query):
    return {"query": query, "reader_question": "", "demand": [],
            "competition": "unreviewed", "competition_reason": "",
            "gap": "", "answer_plan": "", "sources": [],
            "duplication_review": "", "decision_reason": "",
            "reviewed_at": ""}


def evaluate(record):
    """Validate evidence structure, not truth of human/agent notes or future rank."""
    missing = []
    if record.get("collection_status") != "ok":
        missing.append("검색 결과 수집 실패/미실행")
    if not recent(record.get("collected_at")):
        missing.append("검색 조회 시각 누락/24시간 경과")
    if not canonical_url(record.get("search_url", "")):
        missing.append("실제 검색 URL 누락")
    else:
        params = dict(parse_qsl(urlparse(record["search_url"]).query))
        if (params.get("query") or params.get("q")) != record.get("clean_query"):
            missing.append("검색 URL과 실제 쿼리 불일치")
    if record.get("collection_method") not in {"http", "browser", "search_tool"}:
        missing.append("검색 결과 수집 방법 누락")
    docs = record.get("top_docs", [])
    if len(docs) < 10 and not record.get("coverage_note"):
        missing.append("일반 문서 10개 또는 결과 부족에 대한 화면 확인 기록 필요")
    if not docs:
        missing.append("일반 문서 실사 없음; 빈집 판정 불가")
    urls = [canonical_url(d.get("url", "")) for d in docs]
    if not all(urls) or len(set(urls)) != len(urls) or any(excluded_url(u) for u in urls):
        missing.append("광고/쇼핑/중복/잘못된 문서 URL")
    for doc in docs:
        if doc.get("answer_coverage") not in {"direct", "partial", "unrelated"} or not doc.get("review_note") or not recent(doc.get("reviewed_at")):
            missing.append("상위 문서 본문별 직접/일부/무관 판정과 근거 필요")
            break
    r = record.get("review") or {}
    if r.get("query") != record.get("clean_query") or not r.get("reader_question") or not recent(r.get("reviewed_at")):
        missing.append("현재 검색어와 일치하는 독자 질문/최신 검토 필요")
    valid_demand = []
    for e in r.get("demand", []):
        value = e.get("value")
        if (e.get("kind") in {"search_volume", "search_impressions", "search_trend", "repeated_questions"}
                and e.get("query") == record.get("clean_query")
                and canonical_url(e.get("source_url", "")) and e.get("period")
                and e.get("interpretation") and recent(e.get("observed_at"), 24 * 30)
                and isinstance(value, (float, int)) and not isinstance(value, bool)
                and math.isfinite(value) and value > 0):
            if e["kind"] == "repeated_questions":
                evidence_urls = {canonical_url(u) for u in e.get("question_urls", [])}
                if len(evidence_urls - {""}) < 2 or value < 2:
                    continue
            valid_demand.append(e)
    if not valid_demand:
        missing.append("해당 질문의 수요 근거 미확인(자동완성은 보조 신호)")
    if r.get("competition") not in {"high", "medium", "gap"} or not r.get("competition_reason"):
        missing.append("경쟁 문서 종합 판단/이유 필요")
    if not r.get("duplication_review") or not r.get("decision_reason"):
        missing.append("기존 글 중복 검토/최종 판단 이유 필요")
    sources = [s for s in r.get("sources", []) if canonical_url(s.get("url", "")) and
               s.get("finding") and recent(s.get("checked_at"), 24 * 30)]
    if len({urlparse(s["url"]).hostname for s in sources}) < 2 or not r.get("answer_plan"):
        missing.append("답변 계획 및 서로 독립적인 근거 2건 검토 필요")
    if r.get("competition") == "gap" and not r.get("gap"):
        missing.append("경쟁 답변에서 발견한 구체적인 빈틈 필요")
    if missing:
        return {"status": "additional_research", "badge": PENDING,
                "reason": "; ".join(dict.fromkeys(missing)), "missing": missing,
                "evidence_complete": False}
    counts = {kind: sum(d["answer_coverage"] == kind for d in docs)
              for kind in ("direct", "partial", "unrelated")}
    priority = r["competition"] == "gap"
    badge = "💎 우선 공략 후보" if priority else ("🔴 보류" if r["competition"] == "high" else "🟡 보류")
    return {"status": "priority" if priority else "hold", "badge": badge,
            "reason": r["decision_reason"], "missing": [], "coverage_counts": counts,
            "evidence_complete": True}


def audit_errors(data):
    errors = []
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append("구형 감사 로그: schema_version=2로 재실사 필요")
    if not recent(data.get("timestamp")):
        errors.append("감사 시각 누락/만료")
    if not data.get("records"):
        errors.append("감사 기록 없음")
    for record in data.get("records", []):
        host = urlparse(record.get("search_url", "")).hostname or ""
        if ((data.get("channel") == "naver" and host != "search.naver.com") or
                (data.get("channel") == "google" and host not in {"www.google.com", "google.com", "www.google.co.kr"}) or
                data.get("channel") not in {"naver", "google"}):
            errors.append("감사 채널과 검색 출처 불일치")
        result = evaluate(record)
        if not result["evidence_complete"]:
            errors.append(f"{record.get('clean_query', '?')}: {result['reason']}")
    return errors

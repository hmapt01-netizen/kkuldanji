"""Read-only site checks. Default/local mode never makes network requests."""
import argparse
import json
import re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import unquote, urlsplit
import urllib.request

WEB_ROOT = Path(__file__).resolve().parents[1] / "kkuldanji_web"
LIVE_URL = "https://honeyjar.co.kr"
STRUCTURE = {"div", "section", "article", "main", "aside"}
REQUIRED = (
    "index.html", "404.html", "about.html", "terms.html", "privacy.html",
    "contact.html", "calculator.html", "admin.html", "youth-protection.html",
    "copyright.html", "email-rejection.html", "feed.xml", "sitemap.xml", "robots.txt",
    "js/features.js", "js/comments.js", "js/admin-comments.js",
    "favicon.ico", "favicon-192x192.png", "favicon-32x32.png",
    "favicon.svg", "apple-touch-icon.png",
)


class SiteAuditExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
        self.ids = set()
        self.icons = []
        self.stack = []
        self.structure_errors = []
        self.has_form = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("name"):
            self.ids.add(attrs["name"])
        if tag == "form":
            self.has_form = True
        if tag in STRUCTURE:
            self.stack.append(tag)
        if tag == "a" and "href" in attrs:
            self.refs.append(("link", attrs["href"]))
        elif tag in {"img", "script", "source"} and attrs.get("src"):
            self.refs.append(("asset", attrs["src"]))
        elif tag == "link":
            rel = attrs.get("rel", "").split()
            if any(r in {"stylesheet", "icon", "apple-touch-icon"} for r in rel):
                self.refs.append(("asset", attrs.get("href", "")))
            if "icon" in rel or "apple-touch-icon" in rel:
                self.icons.append(attrs.get("href", ""))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag in STRUCTURE:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag not in STRUCTURE:
            return
        if not self.stack or self.stack[-1] != tag:
            self.structure_errors.append("잘못된 닫힘/중첩: </" + tag + ">")
            if tag in self.stack:
                self.stack.remove(tag)
        else:
            self.stack.pop()


def html_files(root):
    return sorted(p for p in root.rglob("*.html")
                  if "templates" not in p.relative_to(root).parts
                  and not p.name.startswith("naver"))


def resolve_reference(root, page, value):
    """Return a local target and fragment, or None for non-file references."""
    value = value.strip()
    parts = urlsplit(value)
    if parts.scheme or parts.netloc:
        return None
    path = unquote(parts.path)
    if not path:
        return page, unquote(parts.fragment)
    if path.startswith("/"):
        target = root / path.lstrip("/")
    else:
        target = page.parent / path
    target = target.resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError("사이트 폴더 밖으로 향하는 경로")
    return target, unquote(parts.fragment)


def audit_local(root=WEB_ROOT):
    root = Path(root).resolve()
    errors = []
    stats = Counter()
    parsed = {}

    def fail(kind, page, detail):
        errors.append((kind, str(page), detail))

    for name in REQUIRED:
        path = root / name
        if not path.is_file() or path.stat().st_size == 0:
            fail("required", name, "필수 파일 누락 또는 빈 파일")

    for page in html_files(root):
        name = page.relative_to(root).as_posix()
        stats["pages"] += 1
        raw = page.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf\xef\xbb\xbf"):
            fail("encoding", name, "중복 UTF-8 BOM")
        elif raw.startswith(b"\xef\xbb\xbf"):
            stats["single_bom"] += 1
        try:
            content = raw.decode("utf-8-sig")
        except UnicodeDecodeError:
            fail("encoding", name, "잘못된 UTF-8")
            continue
        parser = SiteAuditExtractor()
        try:
            parser.feed(content)
            parser.close()
        except Exception as exc:
            fail("html", name, type(exc).__name__)
            continue
        parsed[page] = parser
        for detail in parser.structure_errors:
            fail("html", name, detail)
        if parser.stack:
            fail("html", name, "닫히지 않은 태그: " + ", ".join(parser.stack))
        icon_names = {Path(urlsplit(h).path).name for h in parser.icons}
        if "favicon.ico" not in icon_names:
            fail("favicon", name, "favicon.ico 연결 태그 누락")
        for href in parser.icons:
            if urlsplit(href).query:
                fail("favicon", name, "파비콘 경로의 쿼리: " + href)

    for page, parser in parsed.items():
        name = page.relative_to(root).as_posix()
        for kind, href in parser.refs:
            try:
                resolved = resolve_reference(root, page, href)
            except ValueError as exc:
                fail(kind, name, href + " (" + str(exc) + ")")
                continue
            if resolved is None:
                stats["external_or_dynamic"] += 1
                continue
            stats[kind + "s"] += 1
            target, fragment = resolved
            if target.is_dir():
                fail(kind, name, href + " (폴더 링크: index.html 등 파일명을 명시해야 함)")
            elif not target.is_file():
                fail(kind, name, href + " (파일 없음)")
            elif kind == "link" and fragment and target in parsed:
                # Text fragments are browser directives, not element IDs.
                fragment = fragment.split(":~:text=", 1)[0]
                if fragment and fragment.lower() != 'top' and fragment not in parsed[target].ids:
                    fail(kind, name, href + " (목적지 id/name 없음)")

    for name in ("about.html", "terms.html", "privacy.html", "contact.html"):
        path = root / name
        if path.is_file() and path.stat().st_size < 3000:
            fail("required", name, "필수 정적 페이지가 3,000바이트 미만")
    contact = parsed.get(root / "contact.html")
    if contact and (not contact.has_form or
                    not {"user-name", "user-email", "user-message"} <= contact.ids):
        fail("required", "contact.html", "문의 폼 또는 필수 입력란 누락")
    features = root / "js/features.js"
    if features.is_file():
        text = features.read_text(encoding="utf-8-sig")
        stats['features_bytes'] = features.stat().st_size
        try:
            match = re.search(r'window\.HONEYJAR_POSTS_REGISTRY\s*=\s*window\.HONEYJAR_POSTS_REGISTRY\s*\|\|\s*', text)
            if not match:
                raise ValueError('글 레지스트리 선언 없음')
            registry, _ = json.JSONDecoder().raw_decode(text[match.end():])
            db = json.loads((root.parent / 'data/posts_db.json').read_text(encoding='utf-8-sig'))
            if not registry or Counter(p['slug'] for p in registry) != Counter(p['slug'] for p in db):
                raise ValueError('DB와 레지스트리 글 목록 불일치')
            for post in registry:
                for value in ('posts/' + post['slug'], post['thumb']):
                    resolved = resolve_reference(root, root / 'index.html', value)
                    if resolved is None or not resolved[0].is_file():
                        fail('required', 'js/features.js', '글/썸네일 파일 없음: ' + value)
            stats['registry_posts'] = len(registry)
        except (ValueError, KeyError, TypeError, OSError) as exc:
            fail('required', 'js/features.js', '레지스트리 검사 실패: ' + str(exc))
    return errors, stats


def audit_live(root=WEB_ROOT):
    # Explicit opt-in, GET only, one request per page. No comments API/KV calls.
    paths = ["/", "/about.html", "/terms.html", "/privacy.html",
             "/youth-protection.html", "/copyright.html", "/email-rejection.html",
             "/contact.html", "/calculator.html", "/admin.html", "/feed.xml", "/sitemap.xml"]
    paths += ["/" + p.relative_to(root).as_posix()
              for p in html_files(root) if p.parent == root / "posts"]
    errors = []
    for path in paths:
        try:
            req = urllib.request.Request(LIVE_URL + path,
                                         headers={"User-Agent": "HoneyjarAudit/2.0"})
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status != 200:
                    errors.append(("live", path, "HTTP " + str(response.status)))
        except Exception as exc:
            errors.append(("live", path, str(exc)))
    return errors, len(paths)


def main(argv=None):
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
    cli = argparse.ArgumentParser(description=__doc__)
    modes = cli.add_mutually_exclusive_group()
    modes.add_argument("--local", action="store_true", help="로컬 검사만 (기본)")
    modes.add_argument("--live", action="store_true", help="로컬 통과 후 실서버 HTTP도 검사")
    args = cli.parse_args(argv)
    errors, stats = audit_local()
    from site_pagination_guard import validate as validate_pagination, PaginationError
    try:
        validate_pagination(WEB_ROOT)
    except PaginationError as exc:
        errors.append(("pagination", "index.html / index_template.html", str(exc)))
    print("[꿀단지 로컬 검수]")
    print(f"HTML {stats['pages']}개 / 내부 링크 {stats['links']}개 / 에셋 {stats['assets']}개")
    counts = Counter(kind for kind, _, _ in errors)
    for kind in ("required", "link", "asset", "html", "favicon", "encoding", "pagination"):
        print(f"  {kind}: {counts[kind]}건")
    print(f"정상 선두 BOM: {stats['single_bom']}개 (원본 유지)")
    print(f"레지스트리: {stats['registry_posts']}개 글 / features.js {stats['features_bytes']}바이트")
    if stats['features_bytes'] < 50000:
        print('[참고] 기존 문서의 50KB 기준 미달. 실제 DB·레지스트리·대상 파일 대조 결과를 별도 판정합니다.')
    if args.live and not errors:
        live_errors, total = audit_live()
        errors.extend(live_errors)
        print(f"실서버 HTTP: {total - len(live_errors)}/{total}")
        print("HTTP 성공은 새 배포 반영이나 기능 정상 작동을 보장하지 않습니다.")
    else:
        print("실서버 검사: 미실행" + (" (로컬 오류)" if args.live else " (--local)"))
    for kind, page, detail in errors:
        print(f"[FAIL:{kind}] {page}: {detail}")
    print("미검사: 브라우저 화면/검색·카테고리 실제 클릭/댓글 실서버 동작/외부 링크")
    print("[FAIL] 검사 실패" if errors else "[PASS] 실행한 검사 통과")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

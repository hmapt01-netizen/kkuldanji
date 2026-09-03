import os
import sys
import re
import urllib.request
from html.parser import HTMLParser

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
web_dir = os.path.join(root_dir, 'kkuldanji_web')
base_live_url = 'https://honeyjar.co.kr'

all_html_files = []
for r, d, files in os.walk(web_dir):
    if 'templates' in r:
        continue
    for f in files:
        if f.endswith('.html') and not f.startswith('naver'):
            all_html_files.append(os.path.join(r, f))

class SiteAuditExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.images = []
        self.scripts = []
        self.stylesheets = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag == 'a' and 'href' in attr_dict:
            self.links.append(attr_dict['href'])
        elif tag == 'img' and 'src' in attr_dict:
            self.images.append(attr_dict['src'])
        elif tag == 'script' and 'src' in attr_dict:
            self.scripts.append(attr_dict['src'])
        elif tag == 'link':
            rel = attr_dict.get('rel', '')
            href = attr_dict.get('href', '')
            if 'stylesheet' in rel and href:
                self.stylesheets.append(href)

broken_links = []
broken_assets = []
tag_imbalances = []
favicon_missing = []
bom_corrupted = []

for file_path in all_html_files:
    rel_path = os.path.relpath(file_path, web_dir).replace('\\', '/')
    file_dir = os.path.dirname(file_path)

    # 1. Check BOM corruption
    with open(file_path, 'rb') as fb:
        leading_bytes = fb.read(30)
        bom_count = 0
        while leading_bytes.startswith(b'\xef\xbb\xbf'):
            bom_count += 1
            leading_bytes = leading_bytes[3:]
        if bom_count > 0:
            bom_corrupted.append(f"{rel_path} ({bom_count} BOMs detected)")

    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # 2. Check 5 structure tags balance
    for t in ['div', 'section', 'article', 'main', 'aside']:
        opened = len(re.findall(r'<' + t + r'(?:>|\s[^>]*>)', content, re.I))
        closed = len(re.findall(r'</' + t + r'>', content, re.I))
        if opened != closed:
            tag_imbalances.append(f"{rel_path}: <{t}> {opened} vs {closed}")

    # 3. Check Favicons
    if 'favicon.ico' not in content:
        favicon_missing.append(rel_path)

    # 4. Parse links and assets
    parser = SiteAuditExtractor()
    try:
        parser.feed(content)
    except Exception:
        pass

    for link in parser.links:
        link = link.strip().split('?')[0].split('#')[0]
        if not link or link.startswith('http') or link.startswith('mailto:') or link.startswith('javascript:'):
            continue
        target = os.path.normpath(os.path.join(file_dir, link))
        if not os.path.exists(target):
            broken_links.append(f"{rel_path} -> '{link}'")

    for img in parser.images:
        img = img.strip().split('?')[0].split('#')[0]
        if not img or img.startswith('http') or img.startswith('data:'):
            continue
        target = os.path.normpath(os.path.join(file_dir, img))
        if not os.path.exists(target):
            broken_assets.append(f"{rel_path} -> Image '{img}'")

    for css in parser.stylesheets:
        css = css.strip().split('?')[0].split('#')[0]
        if not css or css.startswith('http'):
            continue
        target = os.path.normpath(os.path.join(file_dir, css))
        if not os.path.exists(target):
            broken_assets.append(f"{rel_path} -> CSS '{css}'")

    for js in parser.scripts:
        js = js.strip().split('?')[0].split('#')[0]
        if not js or js.startswith('http'):
            continue
        target = os.path.normpath(os.path.join(file_dir, js))
        if not os.path.exists(target):
            broken_assets.append(f"{rel_path} -> JS '{js}'")

# 5. Check live server HTTP 200 responses
test_urls = [
    '/', '/about.html', '/terms.html', '/privacy.html',
    '/youth-protection.html', '/copyright.html', '/email-rejection.html',
    '/contact.html', '/calculator.html', '/admin.html', '/feed.xml', '/sitemap.xml'
]
for f in all_html_files:
    rel = os.path.relpath(f, web_dir).replace('\\', '/')
    if rel.startswith('posts/'):
        test_urls.append('/' + rel)

live_errors = []
for u in test_urls:
    try:
        req = urllib.request.Request(base_live_url + u, headers={'User-Agent': 'Mozilla/5.0 (AuditBot)'})
        resp = urllib.request.urlopen(req, timeout=10)
        if resp.status != 200:
            live_errors.append(f"{u} (HTTP {resp.status})")
    except Exception as e:
        live_errors.append(f"{u} ({e})")

print("="*60)
print(f"🛡️ [꿀단지 마스터 표준 18호] 전수 자가 검증 (Full-Site Audit)")
print("="*60)
print(f"• 검사 대상 실제 서비스 HTML: {len(all_html_files)}개")
print(f"• 깨진 내부 링크 (Broken Links): {len(broken_links)}건 {'✅ 통과' if len(broken_links)==0 else '🚨 실패'}")
print(f"• 깨진 에셋 (Image/CSS/JS): {len(broken_assets)}건 {'✅ 통과' if len(broken_assets)==0 else '🚨 실패'}")
print(f"• HTML 태그 밸런스 오류: {len(tag_imbalances)}건 {'✅ 통과' if len(tag_imbalances)==0 else '🚨 실패'}")
print(f"• 파비콘 누락 페이지: {len(favicon_missing)}건 {'✅ 통과' if len(favicon_missing)==0 else '🚨 실패'}")
print(f"• 유령 UTF-8 BOM 오염: {len(bom_corrupted)}건 {'✅ 통과' if len(bom_corrupted)==0 else '🚨 실패'}")
print(f"• 실서버 라이브 HTTP 200 응답: {len(test_urls)-len(live_errors)}/{len(test_urls)} {'✅ 100% 정상' if len(live_errors)==0 else '🚨 실패'}")

is_passed = (len(broken_links) == 0 and len(broken_assets) == 0 and 
             len(tag_imbalances) == 0 and len(favicon_missing) == 0 and 
             len(bom_corrupted) == 0 and len(live_errors) == 0)

if is_passed:
    print("\n🎉 [100% AUDIT PASS] 모든 검증을 완벽히 통과했습니다! 사용자에게 보고 가능한 무결점 상태입니다.")
    sys.exit(0)
else:
    print("\n🚨 [AUDIT FAILED] 결함이 발견되었습니다! 즉시 자동 복구 후 재검증해야 합니다.")
    if broken_links: print("  - 깨진 링크:", broken_links)
    if broken_assets: print("  - 깨진 에셋:", broken_assets)
    if tag_imbalances: print("  - 태그 불일치:", tag_imbalances)
    if bom_corrupted: print("  - BOM 오염:", bom_corrupted)
    if live_errors: print("  - 서버 응답 에러:", live_errors)
    sys.exit(1)

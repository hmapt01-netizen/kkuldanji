# -*- coding: utf-8 -*-
import os
import sys
import json
import re
import glob

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("🔍 [전수 조사] 꿀단지 웹사이트 & 네이버 원고 참고문헌 링크 연결 상태")
print("=" * 70)

# -------------------------------------------------------------
# 1. kkuldanji_web/posts/*.html (실제 배포된 웹 포스트 41편)
# -------------------------------------------------------------
html_files = sorted(glob.glob(os.path.join(root_dir, 'kkuldanji_web', 'posts', '*.html')))
print(f"\n[1] 구글 본진 웹사이트 포스트 (총 {len(html_files)}편) 전수 검사")

web_issues = []

for hf in html_files:
    fname = os.path.basename(hf)
    with open(hf, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 1) Look for the references section
    # Search for <div class="references-card">, <section ...>, or <h3>참고문헌</h3>
    ref_section_match = re.search(r'(?:class=[\'"][^\'"]*reference[^\'"]*[\'"]|참고문헌)[\s\S]*?(?:</ul>|</div>\s*</div>|</section>|</article>)', html)
    
    # Let's find all <li> items inside references
    # Usually it's in a <ul class="references-list"> or similar
    ref_ul = re.findall(r'<ul[^>]*class=[\'"][^\'"]*reference[^\'"]*[\'"][^>]*>([\s\S]*?)</ul>', html)
    if not ref_ul:
        # fallback: find ul after h3/h2 with 참고문헌
        m = re.search(r'<h[234][^>]*>[^<]*참고\s*문헌[^<]*</h[234]>[\s\S]*?<ul[^>]*>([\s\S]*?)</ul>', html)
        if m:
            ref_ul = [m.group(1)]

    unlinked_items = []
    broken_link_items = []
    total_items = 0

    if ref_ul:
        for u in ref_ul:
            lis = re.findall(r'<li[^>]*>([\s\S]*?)</li>', u)
            for li in lis:
                total_items += 1
                # Check if it has <a> tag
                a_tags = re.findall(r'<a\s+([^>]+)>([\s\S]*?)</a>', li)
                if not a_tags:
                    clean_text = re.sub(r'<[^>]+>', ' ', li).strip()
                    unlinked_items.append(clean_text)
                else:
                    for attrs, text in a_tags:
                        href_match = re.search(r'href=[\'"]([^\'"]*)[\'"]', attrs)
                        if not href_match or not href_match.group(1) or href_match.group(1) in ['#', '', 'javascript:void(0)']:
                            broken_link_items.append((text.strip(), href_match.group(1) if href_match else 'NONE'))
    else:
        # No reference section found at all?
        unlinked_items.append("[참고문헌 섹션 자체 누락]")

    if unlinked_items or broken_link_items:
        web_issues.append({
            'file': fname,
            'total': total_items,
            'unlinked': unlinked_items,
            'broken': broken_link_items
        })

if web_issues:
    print(f"🚨 웹 포스트 중 참고문헌 링크 문제 발견: {len(web_issues)}편")
    for w in web_issues:
        print(f"\n📄 {w['file']} (총 {w['total']}개 항목 중 문제 발생)")
        if w['unlinked']:
            print(f"   [링크 태그 없는 텍스트 항목 {len(w['unlinked'])}개]:")
            for u in w['unlinked']:
                print(f"     ❌ {u}")
        if w['broken']:
            print(f"   [빈 링크/깨진 링크 항목 {len(w['broken'])}개]:")
            for text, href in w['broken']:
                print(f"     ⚠️ href='{href}' | 텍스트: {text}")
else:
    print("✅ 웹 포스트 41편의 참고문헌 목록 내부 모든 항목에 <a> 링크가 정상 탑재되어 있습니다!")


# -------------------------------------------------------------
# 2. data/posts_db.json 내부의 references & academicRefs 전수 검사
# -------------------------------------------------------------
print(f"\n[2] data/posts_db.json 데이터베이스 전수 검사")
db_path = os.path.join(root_dir, 'data', 'posts_db.json')
with open(db_path, 'r', encoding='utf-8-sig') as f:
    posts = json.load(f)

db_issues = []
for idx, p in enumerate(posts):
    slug = p.get('slug', '')
    title = p.get('title', '')
    refs = p.get('references', [])
    ac_refs = p.get('academicRefs', [])
    
    unlinked_refs = []
    broken_refs = []
    
    for r in refs:
        if not re.search(r'<a\s+[^>]*href=["\']https?://[^"\']+["\']', str(r)):
            clean = re.sub(r'<[^>]+>', ' ', str(r)).strip()
            unlinked_refs.append(clean)
        else:
            # check empty or #
            m = re.search(r'href=["\']([^"\']*)["\']', str(r))
            if m and (not m.group(1) or m.group(1).startswith('#')):
                broken_refs.append(str(r))
                
    if unlinked_refs or broken_refs:
        db_issues.append({
            'num': idx + 1,
            'slug': slug,
            'title': title,
            'unlinked': unlinked_refs,
            'broken': broken_refs
        })

if db_issues:
    print(f"🚨 posts_db.json 중 링크 문제 발견: {len(db_issues)}편")
    for d in db_issues:
        print(f"\n📌 [{d['num']}호] {d['slug']}")
        for u in d['unlinked']:
            print(f"   ❌ 링크 없음: {u}")
else:
    print("✅ posts_db.json 41편의 references 항목 전부에 유효한 <a href='https://...'> 링크가 정상 탑재되어 있습니다!")


# -------------------------------------------------------------
# 3. 꿀단지 네이버 원고 HTML 파일들 (총 41개 폴더) 전수 검사
# -------------------------------------------------------------
print(f"\n[3] '꿀단지 네이버' 폴더 원고 HTML 참고문헌 링크 연결 상태 검사")
naver_dir = os.path.join(root_dir, '꿀단지 네이버')
naver_htmls = glob.glob(os.path.join(naver_dir, '**', '*_네이버블로그용.html'), recursive=True)
naver_htmls += glob.glob(os.path.join(naver_dir, '**', '*_네이버.html'), recursive=True)
naver_htmls = sorted(list(set(naver_htmls)))

print(f"총 {len(naver_htmls)}개 네이버 원고 파일 감지")

naver_with_links = []
naver_without_links = []

for nh in naver_htmls:
    rel_path = os.path.relpath(nh, naver_dir)
    with open(nh, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check ref-box or 참고문헌
    m = re.search(r'(?:ref-box|참고\s*문헌)[\s\S]*?(?:</div>\s*</div>|</div>\s*</body>|</body>)', content)
    ref_text = m.group(0) if m else content
    
    # Check if there are <a> tags in reference area
    has_a = '<a ' in ref_text and 'href=' in ref_text
    # Count reference items
    items = re.findall(r'(?:•|&bull;|\d+\.|\-)\s*([^<\n]+)', ref_text)
    
    if has_a:
        naver_with_links.append((rel_path, len(items)))
    else:
        naver_without_links.append((rel_path, len(items)))

print(f"\n📊 네이버 원고 참고문헌 링크 현황:")
print(f"   • 링크 탑재된 네이버 원고: {len(naver_with_links)}편")
print(f"   • 텍스트만 있는(링크 없는) 네이버 원고: {len(naver_without_links)}편")

if naver_with_links:
    print("\n[참고: 링크가 탑재된 네이버 원고 목록]")
    for p, count in naver_with_links[:5]:
        print(f"   🔗 {p} ({count}개 항목 링크 있음)")

if naver_without_links:
    print(f"\n[참고: 링크가 없는(텍스트만 표기된) 네이버 원고 {len(naver_without_links)}편 샘플]")
    for p, count in naver_without_links[:10]:
        print(f"   📝 {p} ({count}개 항목)")

print("\n" + "=" * 70)

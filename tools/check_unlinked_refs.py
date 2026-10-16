# -*- coding: utf-8 -*-
import os
import sys
import json
import re

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(root_dir, 'data', 'posts_db.json')
web_posts_dir = os.path.join(root_dir, 'kkuldanji_web', 'posts')

with open(data_path, 'r', encoding='utf-8-sig') as f:
    posts = json.load(f)

print(f"============================================================")
print(f"🔍 꿀단지 전체 포스트 ({len(posts)}편) 참고문헌 링크 전수 조사")
print(f"============================================================")

# 1. DB (posts_db.json) 조사
db_unlinked = []

for idx, p in enumerate(posts):
    title = p.get('title', '')
    slug = p.get('slug', '')
    refs = p.get('references', [])
    ac_refs = p.get('academicRefs', [])
    
    unlinked_refs = []
    for r in refs:
        # Check if contains <a href="http...">
        if not re.search(r'<a\s+[^>]*href=["\']https?://[^"\']+["\']', r):
            unlinked_refs.append(r)
            
    unlinked_ac_refs = []
    for ar in ac_refs:
        if not re.search(r'<a\s+[^>]*href=["\']https?://[^"\']+["\']', ar):
            unlinked_ac_refs.append(ar)
            
    if unlinked_refs or unlinked_ac_refs:
        db_unlinked.append({
            'num': idx + 1,
            'slug': slug,
            'title': title,
            'total_refs': len(refs),
            'unlinked_refs': unlinked_refs,
            'unlinked_ac_refs': unlinked_ac_refs
        })

print(f"\n[1] posts_db.json 참고문헌 링크 누락 글: 총 {len(db_unlinked)}편")
for item in db_unlinked:
    print(f"\n📌 [{item['num']}호] {item['slug']}")
    print(f"   제목: {item['title'][:40]}...")
    print(f"   참고문헌 총 {item['total_refs']}개 중 링크 누락: {len(item['unlinked_refs'])}개")
    for u in item['unlinked_refs']:
        print(f"     ❌ {u.strip()}")
    if item['unlinked_ac_refs']:
        print(f"   학술참고문헌 링크 누락: {len(item['unlinked_ac_refs'])}개")
        for u in item['unlinked_ac_refs']:
            print(f"     ❌ {u.strip()}")

# 2. 실제 생성된 HTML 파일 (kkuldanji_web/posts/*.html) 조사
html_unlinked = []
if os.path.exists(web_posts_dir):
    for f in os.listdir(web_posts_dir):
        if f.endswith('.html'):
            fpath = os.path.join(web_posts_dir, f)
            with open(fpath, 'r', encoding='utf-8') as hf:
                content = hf.read()
            
            # Find references section
            # Look for <div class="references-card"> or <h3>참고문헌</h3> or similar
            ref_match = re.search(r'(?:<div class=["\']references-card["\'][^>]*>|<h[23][^>]*>참고문헌[\s\S]*?</h[23]>)([\s\S]*?)(?:</div>\s*</div>|</article>|</main>)', content)
            if ref_match:
                ref_section = ref_match.group(1)
                # find all <li>
                lis = re.findall(r'<li[^>]*>([\s\S]*?)</li>', ref_section)
                unlinked_lis = []
                for li in lis:
                    if not re.search(r'<a\s+[^>]*href=["\']https?://[^"\']+["\']', li):
                        unlinked_lis.append(re.sub(r'<[^>]+>', ' ', li).strip())
                if unlinked_lis:
                    html_unlinked.append({
                        'file': f,
                        'total_lis': len(lis),
                        'unlinked_count': len(unlinked_lis),
                        'unlinked_items': unlinked_lis
                    })

print(f"\n[2] kkuldanji_web/posts/*.html 실서버 HTML 참고문헌 링크 누락: 총 {len(html_unlinked)}편")
for item in html_unlinked:
    print(f"\n📄 {item['file']} (누락: {item['unlinked_count']}/{item['total_lis']})")
    for u in item['unlinked_items']:
        print(f"     ❌ {u}")

print(f"\n============================================================")
print(f"📊 전수 조사 요약:")
print(f"   • 전체 포스트: {len(posts)}편")
print(f"   • 링크 누락 포스트: {len(db_unlinked)}편 ({len(db_unlinked)/len(posts)*100:.1f}%)")
print(f"   • 링크 완비 포스트: {len(posts) - len(db_unlinked)}편")
print(f"============================================================")

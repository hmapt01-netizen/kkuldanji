# -*- coding: utf-8 -*-
import os
import sys
import json
import re
import glob

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
web_posts_dir = os.path.join(root_dir, 'kkuldanji_web', 'posts')
html_files = sorted(glob.glob(os.path.join(web_posts_dir, '*.html')))

print(f"============================================================")
print(f"🔍 [구글 본진 웹사이트 41편] 참고문헌 섹션 정밀 전수 검사")
print(f"============================================================")

unlinked_posts = []
total_refs_all = 0
linked_refs_all = 0
unlinked_refs_all = 0

for hf in html_files:
    fname = os.path.basename(hf)
    with open(hf, 'r', encoding='utf-8') as f:
        html = f.read()

    # Look for "참고 문헌" or "참고문헌" block
    # It usually starts with <strong ...>...참고...문헌...</strong> or <h2/3/4...>...참고...문헌...
    # followed by <ul ...> ... </ul>
    m = re.search(r'참고\s*문헌[\s\S]*?<ul[^>]*>([\s\S]*?)</ul>', html)
    if not m:
        # Try finding references-list or similar
        m = re.search(r'<ul[^>]*style=["\'][^"\']*list-style:\s*none[^"\']*["\'][^>]*>([\s\S]*?)</ul>', html)

    if m:
        ul_content = m.group(1)
        lis = re.findall(r'<li[^>]*>([\s\S]*?)</li>', ul_content)
        
        post_unlinked = []
        for li in lis:
            total_refs_all += 1
            # Check if it has <a> tag with href
            a_tag = re.search(r'<a\s+[^>]*href=["\'](https?://[^"\']+)["\'][^>]*>([\s\S]*?)</a>', li)
            if a_tag:
                linked_refs_all += 1
            else:
                unlinked_refs_all += 1
                clean_text = re.sub(r'<[^>]+>', ' ', li).strip()
                post_unlinked.append(clean_text)
                
        if post_unlinked:
            unlinked_posts.append({
                'file': fname,
                'total': len(lis),
                'unlinked_count': len(post_unlinked),
                'items': post_unlinked
            })
    else:
        print(f"⚠️ [참고문헌 블록 파싱 실패]: {fname}")

print(f"\n📊 [웹사이트 검사 결과 요약]:")
print(f"   • 총 검사한 글: {len(html_files)}편")
print(f"   • 총 참고문헌 항목: {total_refs_all}개")
print(f"   • 링크 탑재 항목: {linked_refs_all}개")
print(f"   • 링크 누락 항목: {unlinked_refs_all}개")
print(f"   • 링크 누락 글: {len(unlinked_posts)}편")

if unlinked_posts:
    print(f"\n🚨 링크가 누락된 글 상세 목록:")
    for up in unlinked_posts:
        print(f"\n📄 {up['file']} (누락: {up['unlinked_count']} / 총 {up['total']}개)")
        for it in up['items']:
            print(f"     ❌ {it}")
else:
    print(f"\n🎉 모든 웹 포스트(41편)의 참고문헌에 링크가 100% 정상 탑재되어 있습니다!")

print("\n" + "=" * 60)

# -*- coding: utf-8 -*-
import os
import sys
import json
import re

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(root_dir, 'data', 'posts_db.json')

with open(data_path, 'r', encoding='utf-8-sig') as f:
    posts = json.load(f)

print("=" * 70)
print("🔍 꿀단지 전체 포스트 참고문헌 URL 무결성 정밀 분석")
print("=" * 70)

all_links = []
for idx, p in enumerate(posts):
    slug = p.get('slug', '')
    raw_refs = p.get('academicRefs') or p.get('references')
    if isinstance(raw_refs, list):
        for r in raw_refs:
            urls = re.findall(r'href=[\'"](https?://[^\'"]+)[\'"]', str(r))
            texts = re.findall(r'<a\s+[^>]*>([\s\S]*?)</a>', str(r))
            all_links.append((idx+1, slug, urls[0] if urls else 'NO_URL', texts[0] if texts else str(r)))
    elif isinstance(raw_refs, str):
        urls = re.findall(r'href=[\'"](https?://[^\'"]+)[\'"]', raw_refs)
        lis = re.findall(r'<li[^>]*>([\s\S]*?)</li>', raw_refs)
        if not urls:
            for l in lis:
                all_links.append((idx+1, slug, 'NO_URL', re.sub(r'<[^>]+>', '', l).strip()))
        else:
            for u, l in zip(urls, lis):
                all_links.append((idx+1, slug, u, re.sub(r'<[^>]+>', '', l).strip()))

no_url = [l for l in all_links if l[2] == 'NO_URL']
print(f"• 총 검사된 참고문헌 항목: {len(all_links)}개")
print(f"• 링크 정상 항목: {len(all_links) - len(no_url)}개")
print(f"• 링크 누락 항목: {len(no_url)}개")

if no_url:
    print(f"\n🚨 링크가 없는 참고문헌 항목 상세:")
    for l in no_url:
        print(f"   [{l[0]}호] {l[1]}:")
        print(f"     ❌ {l[3]}")
else:
    print("\n✅ 링크가 없는 항목이 0건입니다.")

# 도메인 통계
domains = {}
for l in all_links:
    url = l[2]
    if url != 'NO_URL':
        d = url.split('/')[2] if len(url.split('/')) > 2 else 'OTHER'
        domains[d] = domains.get(d, 0) + 1

print(f"\n📊 공인 출처 도메인 분포 (총 {len(domains)}개 도메인):")
for d, count in sorted(domains.items(), key=lambda x: x[1], reverse=True)[:15]:
    print(f"   • {d}: {count}건")

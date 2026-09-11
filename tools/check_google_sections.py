import json
import re

with open('data/posts_db.json', 'r', encoding='utf-8-sig') as f:
    posts = json.load(f)

target = next(p for p in posts if 'plantar' in p['slug'])
body = target['bodyHtml']

# Find all H2s and images
sections = re.split(r'(<h2[^>]*>.*?</h2>)', body)
for s in sections:
    if s.startswith('<h2'):
        clean_h2 = re.sub(r'<[^>]+>', '', s).strip()
        print(f"\n[SECTION] {clean_h2}")
    else:
        # find images in this section
        imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*alt=["\']([^"\']+)["\']', s)
        for src, alt in imgs:
            print(f"  --> IMG: {src.split('/')[-1]} | alt: {alt}")
        # print first few sentences of text
        paras = re.findall(r'<p style="font-size:1\.02rem[^>]*>(.*?)</p>', s)
        for p in paras[:2]:
            clean_p = re.sub(r'<[^>]+>', '', p).strip()
            print(f"      Text: {clean_p[:60]}...")

import json
import re

with open(r'data\posts_db.json', 'r', encoding='utf-8-sig') as f:
    posts = json.load(f)

p = posts[0]
print('=== 구글 본진 포스트 검토 ===')
print('Title:', p['title'])
print('ShortTitle:', p['shortTitle'])
print('Desc:', p['desc'])

h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', p['bodyHtml'])
print('\nH2 Subheadings:')
for i, h in enumerate(h2s, 1):
    clean_h = re.sub(r'<[^>]+>', '', h).strip()
    print(f'  {i}. {clean_h} ({len(clean_h)}자)')

# captions
img_wraps = re.findall(r'<div class="post-img-wrap"[^>]*>[\s\S]*?<p[^>]*>(.*?)</p>', p['bodyHtml'])
print('\nCaptions in Google Post:')
for i, c in enumerate(img_wraps, 1):
    clean_c = re.sub(r'<[^>]+>', '', c).strip()
    print(f'  {i}. {clean_c}')

print('\n=== 네이버 블로그 원고 검토 ===')
naver_path = r'd:\작업\꿀단지\꿀단지 네이버\12_족저근막염_아침첫발_통증_스트레칭\12_족저근막염_아침첫발_통증_스트레칭_네이버블로그용.html'
with open(naver_path, 'r', encoding='utf-8') as f:
    n_html = f.read()

n_h1 = re.search(r'<h1>(.*?)</h1>', n_html)
print('Naver H1:', n_h1.group(1) if n_h1 else 'None')

n_h2s = re.findall(r'<h2>(.*?)</h2>', n_html)
print('\nNaver H2 Subheadings:')
for i, h in enumerate(n_h2s, 1):
    clean_h = re.sub(r'<[^>]+>', '', h).strip()
    print(f'  {i}. {clean_h} ({len(clean_h)}자)')

n_alts = re.findall(r'<img[^>]+alt="([^"]+)"', n_html)
print('\nNaver Image Alts:')
for i, a in enumerate(n_alts, 1):
    print(f'  {i}. {a}')

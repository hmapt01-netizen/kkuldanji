import re

with open(r'꿀단지 네이버\12_족저근막염_아침첫발_통증_스트레칭\12_족저근막염_아침첫발_통증_스트레칭_네이버블로그용.html', 'r', encoding='utf-8') as f:
    c = f.read()

parts = c.split('<div style="text-align:center;')
for i, p in enumerate(parts[1:], 1):
    img_match = re.search(r'src=["\']([^"\']+)["\']', p)
    src = img_match.group(1) if img_match else 'no img'
    text_snippet = re.sub(r'<[^>]+>', ' ', p)[:300].strip()
    # clean excess spaces
    text_snippet = ' '.join(text_snippet.split())
    print(f'=== Image {i}: {src} ===')
    print(text_snippet)
    print()

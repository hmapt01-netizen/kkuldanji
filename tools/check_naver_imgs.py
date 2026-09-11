import re

with open(r'꿀단지 네이버\12_족저근막염_아침첫발_통증_스트레칭\12_족저근막염_아침첫발_통증_스트레칭_네이버블로그용.html', 'r', encoding='utf-8') as f:
    c = f.read()

imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*alt=["\']([^"\']+)["\']', c)
for i, (src, alt) in enumerate(imgs, 1):
    print(f'{i}. src={src} | alt={alt}')

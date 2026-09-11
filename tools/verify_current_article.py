import json
import re
import os

with open('data/posts_db.json', 'r', encoding='utf-8-sig') as f:
    posts = json.load(f)

target = next(p for p in posts if 'plantar' in p['slug'])

print('=== 1. Google Post Subheadings & Length ===')
h2_matches = re.findall(r'<h2[^>]*>(.*?)</h2>', target['bodyHtml'])
print(f"Total H2s: {len(h2_matches)}")
for i, h2 in enumerate(h2_matches):
    clean_h2 = re.sub(r'<[^>]+>', '', h2).strip()
    length = len(clean_h2)
    status = "✅ 적정(15~22자)" if length <= 22 else ("⚠️ 한도(25자)" if length <= 25 else "🚨 초과(>25자)")
    print(f"  H2 #{i+1} ({length}자): '{clean_h2}' -> {status}")

print('\n=== 2. Google Post Images & Captions ===')
# Look for images and captions
img_pattern = re.compile(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*alt=["\']([^"\']+)["\']', re.IGNORECASE)
imgs = img_pattern.findall(target['bodyHtml'])
print(f"Total Imgs: {len(imgs)}")
for i, (src, alt) in enumerate(imgs):
    print(f"  Img #{i+1}: src='{src}', alt='{alt}' ({len(alt)}자)")

caption_pattern = re.compile(r'<p style=["\'][^"\']*font-size:\s*0\.83rem[^"\']*>\s*(\[[^\]]+\])\s*</p>', re.IGNORECASE)
captions = caption_pattern.findall(target['bodyHtml'])
print(f"Total Captions: {len(captions)}")
for i, c in enumerate(captions):
    print(f"  Caption #{i+1}: '{c}' ({len(c)}자)")

print('\n=== 3. Google Post FAQs ===')
faqs = target.get('faqs', [])
print(f"FAQ Count: {len(faqs)}")
for i, faq in enumerate(faqs):
    q = faq.get('q', faq.get('question', ''))
    a = faq.get('a', faq.get('answer', ''))
    print(f"  FAQ #{i+1}: Q. {q} ({len(q)}자)")
    print(f"           A. {a[:80]}...")

print('\n=== 4. Google Post References ===')
for i, ref in enumerate(target.get('references', [])):
    print(f"  Ref #{i+1}: {ref}")

print('\n=== 5. Check Outdated Keywords in Google Post ===')
outdated_keywords = ['의자', '다리를 꼬', '꼬고', '털신', '슬리퍼를 벗고', '맨발로 벽']
for kw in outdated_keywords:
    found = re.findall(rf'.{{0,20}}{kw}.{{0,20}}', target['bodyHtml'])
    if found:
        print(f"  🚨 Google Post found '{kw}': {found}")
    else:
        print(f"  ✅ Google Post: '{kw}' 없음")

# Now check Naver blog post
naver_path = r"꿀단지 네이버\12_족저근막염_아침첫발_통증_스트레칭\족저근막염_아침_첫발_통증_완화_침대_위_발가락_스트레칭_네이버블로그용.html"
if os.path.exists(naver_path):
    print('\n=== 6. Naver Post Check ===')
    with open(naver_path, 'r', encoding='utf-8') as nf:
        naver_content = nf.read()
    
    naver_h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', naver_content)
    print(f"Naver H2s ({len(naver_h2s)}):")
    for i, nh2 in enumerate(naver_h2s):
        clean_nh2 = re.sub(r'<[^>]+>', '', nh2).strip()
        print(f"  Naver H2 #{i+1} ({len(clean_nh2)}자): '{clean_nh2}'")
    
    print('\nCheck Outdated Keywords in Naver Post:')
    for kw in outdated_keywords:
        found = re.findall(rf'.{{0,20}}{kw}.{{0,20}}', naver_content)
        if found:
            print(f"  🚨 Naver Post found '{kw}': {found}")
        else:
            print(f"  ✅ Naver Post: '{kw}' 없음")

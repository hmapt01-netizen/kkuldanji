import json
import re

with open('data/posts_db.json', 'r', encoding='utf-8-sig') as f:
    posts = json.load(f)

target = next(p for p in posts if 'plantar' in p['slug'])
body = target['bodyHtml']

# Find all p blocks
paras = re.findall(r'<p style="font-size:1\.02rem; line-height:1\.9; color:#334155; margin-bottom:22px;">(.*?)</p>', body, re.DOTALL)
print(f'Total 1.02rem paragraphs: {len(paras)}')

multi = []
for p in paras:
    clean = re.sub(r'<[^>]+>', '', p).strip()
    s = re.findall(r'[다죠요까네][\.!\?](?:\s|$)', clean)
    if len(s) > 1:
        multi.append((len(s), clean))

print(f'Paragraphs with >1 sentences: {len(multi)}')
for c, text in multi:
    print(f'  [{c}문장]: {text}')

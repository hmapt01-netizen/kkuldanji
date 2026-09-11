import json
import re

with open('data/posts_db.json', 'r', encoding='utf-8-sig') as f:
    posts = json.load(f)

p = posts[0]
wraps = re.findall(r'<div class="post-img-wrap"[^>]*>[\s\S]*?</div>', p['bodyHtml'])
for w in wraps:
    print('WRAP:', w)

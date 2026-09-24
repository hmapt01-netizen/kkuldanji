# -*- coding: utf-8 -*-
import json
import re
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

with open('data/posts_db.json', 'r', encoding='utf-8-sig') as f:
    posts = json.load(f)

for p in posts:
    if p.get('slug') == 'morning-apple-heartburn-peanut-butter.html':
        body = p.get('bodyHtml', '')
        print('Featured Caption:', p.get('featuredCaption'))
        figures = re.findall(r'<figure[^>]*>(.*?)</figure>', body, re.DOTALL)
        for i, fig in enumerate(figures, 1):
            img_src = re.search(r'src=["\']([^"\']+)["\']', fig)
            caption = re.search(r'<figcaption[^>]*>(.*?)</figcaption>', fig, re.DOTALL)
            src_str = img_src.group(1) if img_src else 'None'
            cap_str = caption.group(1).strip() if caption else 'None'
            print(f"Figure {i}: {src_str} -> {cap_str}")
        break

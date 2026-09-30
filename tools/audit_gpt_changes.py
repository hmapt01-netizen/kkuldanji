import json
import re
import sys
import subprocess

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

res_orig = subprocess.run(['git', 'show', 'origin/main:data/posts_db.json'], capture_output=True)
orig_posts = json.loads(res_orig.stdout.decode('utf-8-sig'))

with open('data/posts_db.json', 'r', encoding='utf-8-sig') as f:
    curr_posts = json.load(f)

orig_map = {p['slug']: p for p in orig_posts}
curr_map = {p['slug']: p for p in curr_posts}

penalties = ['않고', '추천', '최대', '무료', '100%', '사이트', '이자', '할인', '대행', '수수료']
slugs = [
    'water-intake-guide.html',
    'core-exercise-home.html',
    'posture-stretching-office.html',
    'sleep-hygiene-guide.html',
    'morning-routine.html',
    'intermittent-fasting-guide.html',
    'mediterranean-diet.html',
    'august-seasonal-foods.html',
    'ohnara-diet.html'
]

def strip_tags(html):
    clean = re.sub(r'<(style|script)[^>]*>.*?</\1>', '', html, flags=re.DOTALL)
    clean = re.sub(r'<[^>]+>', ' ', clean)
    clean = clean.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    return clean

def get_text(p):
    t = f"{p.get('title', '')} {p.get('desc', '')} {strip_tags(p.get('bodyHtml', ''))}"
    for f in p.get('faqs', []):
        t += f" {f.get('q', '')} {f.get('a', '')}"
    return t

print("=== ORIGINAL VS CURRENT PENALTIES ===")
for s in slugs:
    op = orig_map[s]
    cp = curr_map[s]
    
    ot = get_text(op)
    ct = get_text(cp)
    
    o_hits = {w: ot.count(w) for w in penalties if ot.count(w) > 0}
    c_hits = {w: ct.count(w) for w in penalties if ct.count(w) > 0}
    
    print(f"[{s}]")
    print(f"  Original penalties: {o_hits}")
    print(f"  Current penalties:  {c_hits}")

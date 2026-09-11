import json

with open('data/posts_db.json', 'r', encoding='utf-8-sig') as f:
    posts = json.load(f)

target = next(p for p in posts if 'plantar' in p['slug'])
body = target['bodyHtml']

start = body.find('<div class="toc-box"')
end = body.find('</div>', start)
# find closing div for the box
end = body.find('</div>', end + 6)
print(body[start:end+6])

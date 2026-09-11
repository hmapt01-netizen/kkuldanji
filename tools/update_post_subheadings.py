import json

db_path = 'data/posts_db.json'
with open(db_path, 'r', encoding='utf-8-sig') as f:
    posts = json.load(f)

target = next(p for p in posts if 'plantar' in p['slug'])
b = target['bodyHtml']

# Update captions without brackets
b = b.replace(
    '<p style="font-size:0.83rem; color:#64748b; margin-top:8px; line-height:1.4;">기상 직후 침대 모서리에 앉아 발바닥 통증을 조심스럽게 살피는 모습</p>',
    '<p style="font-size:0.83rem; color:#64748b; margin-top:8px; line-height:1.4;">기상 직후 침대 모서리에 앉아 발바닥을 살피는 모습</p>'
)
b = b.replace(
    '<p style="font-size:0.83rem; color:#64748b; margin-top:8px; line-height:1.4;">침대에 걸터앉아 발가락을 정강이 쪽으로 당겨 족저근막을 늘리는 모습</p>',
    '<p style="font-size:0.83rem; color:#64748b; margin-top:8px; line-height:1.4;">침대에 앉아 발가락을 젖혀 족저근막을 늘리는 모습</p>'
)
b = b.replace(
    '<p style="font-size:0.83rem; color:#64748b; margin-top:8px; line-height:1.4;">침대 모서리에 걸터앉아 발바닥 아치 아래에 테니스공을 두고 부드럽게 굴리는 모습</p>',
    '<p style="font-size:0.83rem; color:#64748b; margin-top:8px; line-height:1.4;">침대 모서리에 앉아 테니스공을 발바닥으로 굴리는 모습</p>'
)
b = b.replace(
    '<p style="font-size:0.83rem; color:#64748b; margin-top:8px; line-height:1.4;">푹신한 쿠션 슬리퍼를 신고 벽을 짚으며 종아리와 아킬레스건을 이완하는 모습</p>',
    '<p style="font-size:0.83rem; color:#64748b; margin-top:8px; line-height:1.4;">쿠션 슬리퍼를 신고 벽을 밀며 종아리를 늘리는 모습</p>'
)

target['bodyHtml'] = b

with open(db_path, 'w', encoding='utf-8') as f:
    json.dump(posts, f, ensure_ascii=False, indent=2)

print('Captions cleanly replaced in posts_db.json!')

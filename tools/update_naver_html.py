import re

naver_path = r"꿀단지 네이버\12_족저근막염_아침첫발_통증_스트레칭\12_족저근막염_아침첫발_통증_스트레칭_네이버블로그용.html"
with open(naver_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace subheadings with punchy mobile 1-line versions
content = content.replace(
    "| 밤사이 바짝 굳은 힘줄과 첫걸음의 날카로운 신호",
    "| 밤사이 굳은 힘줄과 첫걸음의 경고음"
)
content = content.replace(
    "| 일어나기 전 끝내는 30초 발가락 젖히기 실천법",
    "| 침대 위에서 끝내는 30초 발가락 젖히기"
)
content = content.replace(
    "| 딱딱한 마사지와 맨발 보행이 부르는 치명적 맹점",
    "| 딱딱한 마사지와 맨발 보행의 치명적 맹점"
)

# Replace image alts/captions
content = content.replace(
    '기상 직후 침대 모서리에 앉아 발바닥 통증을 조심스럽게 살피는 모습',
    '기상 직후 침대 모서리에 앉아 발바닥을 살피는 모습'
)
content = content.replace(
    '침대에 걸터앉아 발가락을 정강이 쪽으로 당겨 족저근막을 늘리는 모습',
    '침대에 앉아 발가락을 젖혀 족저근막을 늘리는 모습'
)
content = content.replace(
    '침대 모서리에 걸터앉아 발바닥 아치 아래에 테니스공을 두고 부드럽게 굴리는 모습',
    '침대 모서리에 앉아 테니스공을 발바닥으로 굴리는 모습'
)
content = content.replace(
    '푹신한 쿠션 슬리퍼를 신고 벽을 짚으며 종아리와 아킬레스건을 이완하는 모습',
    '쿠션 슬리퍼를 신고 벽을 밀며 종아리를 늘리는 모습'
)

with open(naver_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Naver HTML successfully updated!')

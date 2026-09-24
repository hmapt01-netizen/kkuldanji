# -*- coding: utf-8 -*-
"""
morning-apple-heartburn-peanut-butter 글을 최신 글(index 0, 2026.09.24, isLatest=True)로 재배치
"""
import json

data_path = r"d:\작업\꿀단지\data\posts_db.json"
with open(data_path, "r", encoding="utf-8-sig") as f:
    posts = json.load(f)

# 1. 대상 글 찾기 및 분리
target_post = None
remaining_posts = []

for p in posts:
    if p.get("slugKey") == "morning-apple-heartburn-peanut-butter":
        target_post = p
    else:
        p["isLatest"] = False
        remaining_posts.append(p)

if not target_post:
    raise ValueError("morning-apple-heartburn-peanut-butter 포스트를 찾을 수 없습니다!")

# 2. 최신 글 속성 부여
target_post["date"] = "2026.09.24"
target_post["isLatest"] = True

# 3. 맨 앞에 배치
new_posts = [target_post] + remaining_posts

# 4. 저장
with open(data_path, "w", encoding="utf-8-sig") as f:
    json.dump(new_posts, f, ensure_ascii=False, indent=2)

print(f"✅ 총 {len(new_posts)}개 포스트 중 'morning-apple-heartburn-peanut-butter'를 최신 글(index 0)로 성공적으로 재배치 완료!")

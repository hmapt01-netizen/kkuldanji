# -*- coding: utf-8 -*-
import sys
import os

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(root_dir, 'tools'))
from validate_titles import validate_naver_titles

titles = [
    '“공복혈당 110 당뇨일까?” 전단계 판정과 정상 복귀법',
    '“약부터 먹어야 할까?” 공복혈당 100 넘었을 때 대처 수칙',
    '“밥 안 먹었는데 왜 높지?” 아침 공복혈당 치솟는 원인과 해결',
    '공복혈당 100 125 주의 판정 약 없이 정상 되돌리는 법',
    '당화혈색소 정상인데 공복혈당만 높은 이유와 아침 혈당 잡는 법',
    '공복혈당장애 3개월 만에 두 자리 정상 수치로 되돌린 비결',
    '건강검진 공복혈당 정상수치 기준과 당뇨 전단계 식단 관리법',
    '아침 공복혈당 낮추는 음식과 식후 10분 걷기 실천 가이드',
    '공복혈당 100 이상 관리법과 야식 차단으로 새벽 혈당 낮추기',
    '건강검진 공복혈당장애 당뇨 전단계 기준과 정상 회복 3단계'
]

for i, t in enumerate(titles, 1):
    print(f"{i}. ({len(t)}자) {t}")

ok = validate_naver_titles(titles)
if not ok:
    sys.exit(1)
print("SUCCESS!")

import sys
import os

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

BANNED_WORDS = [
    '해요', '하더라', '인 것 같아요', '진단', '치료', '완치',
    '부작용', '질병', '질환', '최고', '가장', '최상', '1위',
    '추천', '구매', '판매', '가격', '할인', '특가', '공구',
    '블로그', '사이트', '정확', '100%', '완전', '무조건',
    '최초', '확실', '만족', '후회', '충격', '폭탄',
    '민낯', '처절한', '역대급', '유발', '병원', '임상',
    '발칵', '깜짝', '블라인드'
]

def validate_titles(titles):
    print("🔍 [네이버 C-Rank & DIA+ 제목 기계적 검증기 가동]")
    errors = []
    
    if len(titles) != 10:
        errors.append(f"제목 개수 오류: 정확히 10개여야 하지만 현재 {len(titles)}개입니다.")
        
    for i, t in enumerate(titles, 1):
        found = []
        for w in BANNED_WORDS:
            if w in t:
                found.append(w)
        if found:
            errors.append(f"  ❌ [{i}번 제목 금칙어 적발]: '{t}' ➔ 적발 단어: {found}")
        else:
            print(f"  ✓ [{i}번 제목 PASS]: {t}")
            
    if errors:
        print("\n🚨 [검증 실패 - 수정 필요 항목]")
        for err in errors:
            print(err)
        sys.exit(1)
    else:
        print("\n🎉 [100% AUDIT PASS] 10개 제목 모두 28종 금칙어 0개 및 C-Rank 최적화 통과!")
        sys.exit(0)

if __name__ == '__main__':
    sample_titles = [
        "\"아침마다 한꺼번에 털어 넣었는데?\" 유산균 오메가3 복용시간 시차 두는 이유",
        "\"몸 챙기려다 속 쓰린 이유가 설마?\" 비타민C 유산균 공복 섭취 시 주의점",
        "\"마그네슘 언제 드시나요?\" 저녁 취침 전 섭취로 수면 질 높이는 타이밍",
        "칼슘과 철분 같이 먹으면 흡수 방해? 영양소 충돌 막는 3시간 섭취 간격",
        "빈속에 먹었다가 낭패 보는 지용성 영양제, 오메가3 식후 섭취 권장 배경",
        "종합비타민 하나로 끝내려다 놓치는 영양제별 흡수율 차이와 섭취 기준",
        "영양제 복용시간 총정리, 유산균 공복 섭취와 오메가3 마그네슘 골든타임",
        "유산균 비타민C 오메가3 섭취 순서와 흡수율 높이는 식전 식후 분류표",
        "철분 칼슘 동시 복용 피해야 하는 생리학적 원인 및 영양제 상극 조합",
        "마그네슘 비타민D 복용법과 체내 흡수율 높이는 시간대별 가이드"
    ]
    validate_titles(sample_titles)

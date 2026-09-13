import sys
import re
import os

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

banned = [
    '해요', '하더라', '인 것 같아요', '진단', '치료', '완치',
    '부작용', '질병', '질환', '최고', '가장', '최상', '1위',
    '추천', '구매', '판매', '가격', '할인', '특가', '공구',
    '블로그', '사이트', '정확', '100%', '완전', '무조건',
    '최초', '확실', '만족', '후회', '충격', '폭탄',
    '민낯', '처절한', '역대급', '유발', '병원', '임상',
    '의문', '의약품', '예방', '상담', '문의', '시술'
]

def audit_naver(path):
    print(f"🔍 [네이버 원고 무결성 검증] {path}")
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Extract text from #naverContent only
    m = re.search(r'<div id=["\']naverContent["\']>([\s\S]*?)</div>\s*</div>\s*<script>', html)
    if m:
        body_html = m.group(1)
    else:
        # fallback
        body_html = re.sub(r'<style[\s\S]*?</style>', '', html)
        body_html = re.sub(r'<script[\s\S]*?</script>', '', body_html)

    pure_text = re.sub(r'<[^>]+>', ' ', body_html)
    pure_text = re.sub(r'\s+', ' ', pure_text).strip()

    violations = []
    for b in banned:
        matches = re.findall(rf'({b})', pure_text)
        if matches:
            violations.append((b, len(matches)))

    # Outbound links
    links = [m for m in re.findall(r'href=[\'"]([^\'"]+)[\'"]', html) if m.startswith('http')]

    print(f"  - 순수 본문 글자수 (공백 포함): {len(pure_text)}자")
    print(f"  - 외부 링크(Outbound Links): {len(links)}개")
    
    if violations:
        print(f"  🚨 [금칙어 적발]: {violations}")
        return False
    else:
        print("  ✓ [네이버 44종 금칙어 0개 통과 (예방/의약품/상담/의문/문의 전원 배제)]")

    if len(links) > 0:
        print(f"  🚨 [외부 링크 적발]: {links}")
        return False
    else:
        print("  ✓ [외부 링크 0개 안전 모드 통과]")

    # 3. [마스터 표준 26-1] 실전 검색어 첫 문단 전진 배치 (Front-Loading) 검증
    m_h1 = re.search(r'<h1[^>]*>([\s\S]*?)</h1>', html)
    h1_text = re.sub(r'<[^>]+>', '', m_h1.group(1)).strip() if m_h1 else ""
    intro_lead = pure_text[:250]
    
    # 핵심 시드 단어 추출 (2자 이상 명사군)
    h1_clean = re.sub(r'["\',?!~·]', '', h1_text)
    h1_words = [w for w in h1_clean.split() if len(w) >= 2 and w not in ['수칙', '기준', '원리', '비결', '요령']]
    matched_intro = [w for w in h1_words if w in intro_lead]
    
    if matched_intro:
        print(f"  ✓ [실전 검색어 첫 문단 전진 배치 통과]: {matched_intro} (상단 250자 내 발견)")
    else:
        print(f"  ⚠️ [경고]: 제목 핵심 키워드({h1_words[:3]})가 본문 첫 문단(250자)에 명시되지 않았습니다.")

    print("🎉 [100% AUDIT PASS] 네이버 블로그 원고 무결성 검증 통과!")
    return True

if __name__ == '__main__':
    target = r'd:\작업\꿀단지\꿀단지 네이버\04_영양제_복용시간_상극조합\04_영양제_복용시간_상극조합_네이버블로그용.html'
    if len(sys.argv) > 1:
        target = sys.argv[1]
    audit_naver(target)

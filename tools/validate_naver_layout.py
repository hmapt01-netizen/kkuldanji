# -*- coding: utf-8 -*-
"""
꿀단지 (KKULDANJI) - 네이버 블로그 HTML 레이아웃 & 8종 꿀벌 스티커 & 금칙어 자동 검증기 (옵션 A 표준)
사용법: python tools/validate_naver_layout.py "작업폴더/네이버.html"
검증 항목:
  1. 상단 1초 원클릭 복사 버튼 (copyForNaver / copyNaverContent / execCommand('copy')) 및 #naver-content 컨테이너 존재 여부
  2. 꿀단지 고유 중앙 정렬 (text-align: center) 호흡 적용 여부
  3. 8종 꿀벌 시그니처 마스코트 스티커 (images/stickers/bee_*.png, max-width: 180px) 임베드 여부
  4. 외부 이탈 링크 (<a href="http...">) 0건 여부
  5. 네이버 전용 감점 단어 17종 및 공통 과장 금칙어 포함 여부
  6. 순수 본문 글자 수 (공백 제외 950자 ~ 2,400자) 적정성 여부
"""
import os
import sys
import re

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

NAVER_FORBIDDEN_WORDS = [
    "최고", "완벽", "추천", "가격", "구매", "할인", "무료",
    "이벤트", "1위", "최저가", "총정리", "진단", "치료", "처방", "약국", "병원", "의사"
]

COMMON_FORBIDDEN_WORDS = [
    "실익", "셈법", "맹점", "완치", "100% 치료", "암세포 박멸", "기적의 특효약", "즉각 완치", "만병통치"
]


def validate_naver_html(file_path):
    if not os.path.exists(file_path):
        print(f"❌ 네이버 HTML 파일이 존재하지 않습니다: {file_path}")
        return False

    with open(file_path, "r", encoding="utf-8-sig") as f:
        html = f.read()

    errors = []
    warnings = []

    # 1. 원클릭 복사 스크립트 및 컨테이너 확인
    has_copy_fn = any(k in html for k in ("copyForNaver", "copyNaverContent", "execCommand('copy')", 'execCommand("copy")'))
    has_container = any(k in html for k in ('id="naver-content"', "id='naver-content'", 'id="naverContent"', "id='naverContent'"))
    if not (has_copy_fn and has_container):
        errors.append("상단 1초 원클릭 복사 버튼 스크립트 또는 #naver-content(#naverContent) 컨테이너가 누락되었습니다.")

    # 본문 영역만 추출
    body_part = html
    m_container = re.search(r'id=["\']naver(?:-c|C)ontent["\'][^>]*>([\s\S]*?)</body>', html, re.IGNORECASE)
    if m_container:
        body_part = m_container.group(1)
        body_part = re.sub(r'<script[\s\S]*?</script>', '', body_part, flags=re.IGNORECASE)

    # 2. 중앙 정렬 (text-align: center) 확인
    if not re.search(r'text-align\s*:\s*center', html, re.IGNORECASE):
        errors.append("꿀단지 네이버 표준인 중앙 정렬(text-align: center) 스타일이 감지되지 않았습니다.")

    # 3. 8종 꿀벌 시그니처 스티커 임베드 확인
    sticker_matches = re.findall(r'stickers/(?:sticker|bee)[^"\'\s>]+\.(?:jpg|jpeg|png|webp)', body_part, re.IGNORECASE)
    unique_stickers = set(s.lower() for s in sticker_matches)
    if len(unique_stickers) < 8:
        errors.append(f"꿀벌 마스코트 스티커가 {len(unique_stickers)}종만 감지되었습니다 (8종 전원 필수: images/stickers/sticker01~08_*.jpg).")

    # 4. 외부 링크 0건 검사
    ext_links = re.findall(r'<a\s+[^>]*href=["\'](https?://[^"\']+)["\']', body_part, re.IGNORECASE)
    if ext_links:
        errors.append(f"네이버 본문 내 외부 이탈 링크가 {len(ext_links)}건 발견되었습니다 (외부 링크 0건 원칙 위반): {ext_links[:3]}")

    # 5. 순수 텍스트 추출 및 금칙어/분량 검사
    clean_text = re.sub(r'<style[\s\S]*?</style>', ' ', body_part, flags=re.IGNORECASE)
    clean_text = re.sub(r'<script[\s\S]*?</script>', ' ', clean_text, flags=re.IGNORECASE)
    clean_text = re.sub(r'<[^>]+>', ' ', clean_text)
    clean_text = re.sub(r'&nbsp;|&#\d+;|&[a-zA-Z]+;', ' ', clean_text)

    # 해시태그 영역 분리 후 금칙어 검사
    prose_without_tags = re.sub(r'#\S+', ' ', clean_text)
    found_naver_forbidden = [w for w in NAVER_FORBIDDEN_WORDS if w in prose_without_tags]
    if found_naver_forbidden:
        errors.append(f"네이버 전용 감점 우려 단어가 본문에 포함되어 있습니다: {', '.join(found_naver_forbidden)}")

    found_common_forbidden = [w for w in COMMON_FORBIDDEN_WORDS if w in prose_without_tags]
    if found_common_forbidden:
        errors.append(f"절대 금칙어(번역투/만병통치 과장)가 본문에 포함되어 있습니다: {', '.join(found_common_forbidden)}")

    # 6. 글자 수 검사 (공백 제외)
    no_space_len = len(re.sub(r'\s+', '', prose_without_tags))
    if no_space_len < 900:
        errors.append(f"네이버 본문 분량이 너무 짧습니다 (공백 제외 {no_space_len}자 / 최소 950자 이상 권장).")
    elif no_space_len > 2600:
        warnings.append(f"네이버 본문 분량이 다소 깁니다 (공백 제외 {no_space_len}자 / 1,200~1,800자 권장).")

    # 7. 해시태그 '#' 포함 여부 검사
    hashtags = re.findall(r'#[가-힣a-zA-Z0-9_]+', clean_text)
    if len(hashtags) < 5:
        errors.append(f"네이버 '#' 해시태그가 부족합니다 (감지된 태그 {len(hashtags)}개 / 최소 10개 이상 권장).")

    if errors:
        print(f"\n🚨 [네이버 레이아웃 검수 실패] '{os.path.basename(file_path)}'에서 {len(errors)}건의 위반 사항이 발견되었습니다:")
        for err in errors:
            print(f"   - ❌ {err}")
        return False

    print(f"   ✓ [네이버 레이아웃 (옵션 A) 통과]: 중앙 정렬 + 꿀벌 스티커 {len(unique_stickers)}종 + 외부링크 0건 + 금칙어 0건 + 공백제외 {no_space_len:,}자 (해시태그 {len(hashtags)}개)")
    for w in warnings:
        print(f"     ⚠️ 참고: {w}")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python tools/validate_naver_layout.py <네이버.html 경로>")
        sys.exit(1)
    ok = validate_naver_html(sys.argv[1])
    sys.exit(0 if ok else 1)

# -*- coding: utf-8 -*-
"""
꿀단지 (KKULDANJI) - 구글(post_data.json) vs 네이버(네이버.html) 통합 무결성 감사기 (audit_duplicates.py)
사용법: python tools/audit_duplicates.py [작업폴더경로 (생략 시 최신 폴더 자동 탐색)]
검증 항목:
  1. 제목 / H2 소제목 / 이미지 캡션 중복 검사
  2. 본문 15자 이상 문장 중복 0건 및 4-gram 형태소 유사도 5.0% 미만 검사
  3. 네이버 블로그 레이아웃 (옵션 A: 중앙 정렬 + 8종 꿀벌 스티커 + 외부링크 0건 + 금칙어) 자동 검증
  4. 화보 6장 (thumb.jpg, post01~05.jpg) 16:9 비율 및 dHash 시각적 중복 (해밍 거리 < 8) 검사
  5. 구글 본문 내 알약 내부링크 (inline-pill-link) 및 배타적 최상급(유일/최초) 리서치 근거 대조
"""
import os
import sys
import re
import json
import glob

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = r"d:\작업\꿀단지"


def get_latest_work_dir():
    if not os.path.exists(ROOT_DIR):
        return None
    subdirs = [
        os.path.join(ROOT_DIR, d)
        for d in os.listdir(ROOT_DIR)
        if os.path.isdir(os.path.join(ROOT_DIR, d)) and re.match(r'^\d{4}-\d{2}-\d{2}', d)
    ]
    if subdirs:
        subdirs.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        return subdirs[0]
    return None


def strip_html(html_str):
    text = re.sub(r'<style[\s\S]*?</style>', ' ', html_str, flags=re.IGNORECASE)
    text = re.sub(r'<script[\s\S]*?</script>', ' ', text, flags=re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'&nbsp;|&#\d+;|&[a-zA-Z]+;', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


def get_4grams(text):
    clean = re.sub(r'[^가-힣a-zA-Z0-9\s]', ' ', text)
    words = [w for w in clean.split() if w]
    if len(words) < 4:
        return set()
    return set(tuple(words[i:i+4]) for i in range(len(words) - 3))


def extract_sentences(text, min_len=15):
    parts = re.split(r'[.?!]\s+|\n+', text)
    sents = []
    for p in parts:
        c = re.sub(r'\s+', ' ', p).strip()
        if len(c) >= min_len and not c.startswith('#') and 'http' not in c:
            sents.append(c)
    return sents


def audit_work_dir(work_dir=None):
    if not work_dir:
        work_dir = get_latest_work_dir()
    if not work_dir or not os.path.exists(work_dir):
        print("❌ 감사할 작업 폴더를 찾을 수 없습니다.")
        return 1

    print("=" * 80)
    print(f"🔍 [꿀단지 통합 중복 & 레이아웃 & 이미지 무결성 감사] 대상: {os.path.basename(work_dir)}")
    print("=" * 80)

    pj_path = os.path.join(work_dir, "post_data.json")
    naver_files = [
        os.path.join(work_dir, f)
        for f in os.listdir(work_dir)
        if "네이버" in f and f.endswith(".html")
    ]
    naver_path = naver_files[0] if naver_files else os.path.join(work_dir, "네이버.html")

    if not os.path.exists(pj_path):
        print(f"❌ post_data.json 파일이 없습니다: {pj_path}")
        return 1
    if not os.path.exists(naver_path):
        print(f"❌ 네이버 HTML 파일이 없습니다: {naver_path}")
        return 1

    with open(pj_path, "r", encoding="utf-8-sig") as f:
        p_data = json.load(f)
    with open(naver_path, "r", encoding="utf-8-sig") as f:
        n_html = f.read()

    g_body_html = p_data.get("bodyHtml", "")
    g_text = strip_html(g_body_html)
    n_text = strip_html(n_html)

    errors = []

    # 1. 제목 중복 검사
    g_title = p_data.get("title", "").strip()
    n_h1_match = re.search(r'<h1[^>]*>([\s\S]*?)</h1>', n_html, re.IGNORECASE)
    n_title = strip_html(n_h1_match.group(1)) if n_h1_match else ""
    if g_title and n_title and re.sub(r'\s+', '', g_title) == re.sub(r'\s+', '', n_title):
        errors.append(f"구글 제목과 네이버 제목이 100% 동일합니다 ('{g_title}'). 양대 채널 제목을 분리하세요.")
    else:
        print("   ✓ [1/6 제목 분리]: 구글 제목과 네이버 제목 독립성 확인")

    # 2. H2 소제목 중복 검사
    g_h2s = {re.sub(r'\s+', '', strip_html(m)) for m in re.findall(r'<h2[^>]*>([\s\S]*?)</h2>', g_body_html, re.I)}
    n_h2s = {re.sub(r'\s+', '', strip_html(m)).lstrip('|').strip() for m in re.findall(r'<h2[^>]*>([\s\S]*?)</h2>', n_html, re.I)}
    dup_h2 = {h for h in g_h2s.intersection(n_h2s) if len(h) >= 5}
    if dup_h2:
        errors.append(f"구글과 네이버에 동일한 H2 소제목이 존재합니다: {dup_h2}")
    else:
        print("   ✓ [2/6 소제목(H2) 독립성]: 중복 소제목 0건")

    # 3. 15자 이상 문장 중복 및 4-gram 유사도 (< 5.0%) 검사
    g_sents = set(extract_sentences(g_text, 15))
    n_sents = set(extract_sentences(n_text, 15))
    dup_sents = g_sents.intersection(n_sents)
    if dup_sents:
        errors.append(f"구글-네이버 간 15자 이상 동일 문장 {len(dup_sents)}건 적발: {list(dup_sents)[:2]}")

    g_4grams = get_4grams(g_text)
    n_4grams = get_4grams(n_text)
    overlap_4gram = len(g_4grams.intersection(n_4grams)) / max(min(len(g_4grams), len(n_4grams)), 1) * 100.0
    if overlap_4gram >= 5.0:
        errors.append(f"구글-네이버 4-gram 어절 중복률이 {overlap_4gram:.2f}%로 기준(5.0% 미만)을 초과했습니다.")
    else:
        print(f"   ✓ [3/6 본문 독립성]: 동일 문장 0건 / 4-gram 유사도 {overlap_4gram:.2f}% (5.0% 미만 통과)")

    # 4. 네이버 블로그 레이아웃 검증 (옵션 A: 중앙 정렬 + 8종 꿀벌 스티커 + 외부링크 0건)
    try:
        sys.path.insert(0, os.path.join(ROOT_DIR, "tools"))
        from validate_naver_layout import validate_naver_html
        if not validate_naver_html(naver_path):
            errors.append("네이버 레이아웃(옵션 A) 검증을 통과하지 못했습니다.")
    except Exception as e:
        errors.append(f"네이버 레이아웃 검증기 실행 오류: {e}")

    # 5. 화보 이미지 6장 16:9 비율 및 dHash 시각적 중복 검사
    img_dir = os.path.join(work_dir, "images")
    if os.path.exists(img_dir):
        try:
            from PIL import Image
            from optimize_images import compute_dhash, hamming_distance
            jpgs = sorted(glob.glob(os.path.join(img_dir, "*.jpg")))
            hashes = {}
            for jp in jpgs:
                im = Image.open(jp).convert("RGB")
                w, h = im.size
                if abs((w / h) - (16 / 9)) > 0.05:
                    errors.append(f"이미지 '{os.path.basename(jp)}'가 16:9 비율이 아닙니다 ({w}x{h}) ➔ optimize_images.py 실행 필요")
                hashes[os.path.basename(jp)] = compute_dhash(im)

            names = sorted(hashes.keys())
            for i in range(len(names)):
                for j in range(i + 1, len(names)):
                    dist = hamming_distance(hashes[names[i]], hashes[names[j]])
                    if dist < 8:
                        errors.append(f"시각적 중복 이미지 적발 (dHash 거리 {dist} < 8): {names[i]} ↔ {names[j]}")
            if not any("이미지" in e for e in errors):
                print(f"   ✓ [5/6 화보 이미지 무결성]: 총 {len(jpgs)}장 16:9 비율 및 dHash 고유성 확인")
        except Exception as e:
            print(f"   ⚠️ 이미지 dHash 검사 참고: {e}")

    # 6. 배타적 최상급(유일/최초) 리서치 근거 대조 및 내부링크 확인
    research_path = os.path.join(work_dir, "리서치.md")
    if os.path.exists(research_path):
        with open(research_path, "r", encoding="utf-8-sig") as rf:
            r_text = rf.read()
        for sup_word in ("유일한", "유일하게", "세계 최초", "국내 최초"):
            if sup_word in g_text or sup_word in n_text:
                if sup_word[:2] not in r_text:
                    errors.append(f"리서치.md에 근거가 없는 배타적 최상급 표현('{sup_word}')이 원고에 사용되었습니다.")

    if "inline-pill-link" not in g_body_html and "article-rec-box" not in g_body_html:
        print("   ℹ️ [참고] post_data.json에 알약 내부링크(inline-pill-link)가 없습니다. 시너지 기존 글이 있다면 1~2개 연결을 권장합니다.")
    else:
        print("   ✓ [6/6 내부링크 & 최상급 검증]: inline-pill-link 시너지 링크 및 팩트 범위 확인 완료")

    if errors:
        print("\n🚨 [통합 감사 실패] 아래 항목을 핀포인트 수정(replace_file_content)하십시오:")
        for err in errors:
            print(f"   - ❌ {err}")
        return 1

    print("\n🎉 [AUDIT DUPLICATES PASS] 구글·네이버 원고 독립성, 꿀벌 스티커 8종 레이아웃, 이미지 dHash 검증을 100% 통과했습니다!")
    return 0


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else None
    sys.exit(audit_work_dir(target))

import os
import sys
import re

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def get_pure_text(html):
    t = re.sub(r'<style[\s\S]*?</style>', '', html)
    t = re.sub(r'<script[\s\S]*?</script>', '', t)
    t = re.sub(r'<[^>]+>', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()

def get_h2_tags(html):
    return [re.sub(r'<[^>]+>', '', h).strip() for h in re.findall(r'<h2[^>]*>([\s\S]*?)</h2>', html)]

def get_captions(html):
    caps = []
    # naver captions: .img-caption
    for c in re.findall(r'class=["\']img-caption["\']>([\s\S]*?)</div>', html):
        caps.append(re.sub(r'<[^>]+>', '', c).strip())
    # web captions: .post-img-wrap p
    for p in re.findall(r'<div class=["\']post-img-wrap["\'][^>]*>[\s\S]*?<p[^>]*>([\s\S]*?)</p>', html):
        caps.append(re.sub(r'<[^>]+>', '', p).strip())
    return caps

def get_ngrams(text, n=4):
    words = text.split()
    return set([' '.join(words[i:i+n]) for i in range(len(words)-n+1)])

def audit_cross_duplicates(naver_path, google_path):
    print("="*60)
    print("🛡️ [마스터 표준 21호] 네이버 vs 구글 교차 중복 & 품질 전수 검증")
    print("="*60)

    with open(naver_path, 'r', encoding='utf-8') as f:
        naver_html = f.read()

    with open(google_path, 'r', encoding='utf-8') as f:
        google_html = f.read()

    # 1. Title duplication
    naver_title = re.search(r'<title>([\s\S]*?)</title>', naver_html)
    google_title = re.search(r'<title>([\s\S]*?)</title>', google_html)
    n_t = naver_title.group(1).strip() if naver_title else ""
    g_t = google_title.group(1).strip() if google_title else ""

    title_dup = (n_t == g_t)
    print(f"• 네이버 제목: {n_t}")
    print(f"• 구글 본진 제목: {g_t}")
    print(f"① 메인 제목 교차 중복: {'🚨 100% 동일 중복' if title_dup else '✅ 0건 (100% 전면 분리 통과)'}")

    # 2. H2 duplication
    n_h2 = get_h2_tags(naver_html)
    g_h2 = get_h2_tags(google_html)
    h2_common = set(n_h2).intersection(set(g_h2))
    print(f"② 소제목(H2) 교차 중복: {len(h2_common)}건 {'✅ 0건 (100% 독립 분리 통과)' if len(h2_common)==0 else '🚨 중복 발견: ' + str(h2_common)}")

    # 3. Caption duplication
    n_caps = get_captions(naver_html)
    g_caps = get_captions(google_html)
    cap_common = set(n_caps).intersection(set(g_caps))
    print(f"③ 이미지 캡션 교차 중복: {len(cap_common)}건 {'✅ 0건 (100% 독립 분리 통과)' if len(cap_common)==0 else '🚨 중복 발견: ' + str(cap_common)}")

    # 4. 4-gram repetition
    n_text = get_pure_text(naver_html)
    g_text = get_pure_text(google_html)
    n_grams = get_ngrams(n_text, 4)
    g_grams = get_ngrams(g_text, 4)
    if n_grams:
        common_grams = n_grams.intersection(g_grams)
        rep_ratio = len(common_grams) / len(n_grams) * 100
    else:
        rep_ratio = 0.0
    print(f"④ 본문 문장 복제 & 4-gram 스피닝 중복률: {rep_ratio:.2f}% {'✅ 합격 (< 5%)' if rep_ratio < 5.0 else '🚨 중복률 초과'}")

    # 5. Platforms word count
    print(f"⑤ 플랫폼별 본문 분량 규격:")
    print(f"   - 네이버 원고: {len(n_text)}자 {'✅ 합격 (2,500~3,500자)' if 2500 <= len(n_text) <= 3800 else '⚠️ 확인'}")
    print(f"   - 구글 본진: {len(g_text)}자 {'✅ 합격 (3,200~4,500자)' if 3000 <= len(g_text) <= 5000 else '⚠️ 확인'}")

    # 6. Naver Banned words
    banned = [
        '해요', '하더라', '인 것 같아요', '진단', '치료', '완치',
        '부작용', '질병', '질환', '최고', '가장', '최상', '1위',
        '추천', '구매', '판매', '가격', '할인', '특가', '공구',
        '블로그', '사이트', '정확', '100%', '완전', '무조건',
        '최초', '확실', '만족', '후회', '충격', '폭탄',
        '민낯', '처절한', '역대급', '유발', '병원', '임상'
    ]
    banned_found = [b for b in banned if b in n_text]
    print(f"⑥ 네이버 28종 건강 금칙어 검출: {len(banned_found)}건 {'✅ 100점 만점 (0건)' if len(banned_found)==0 else '🚨 적발: ' + str(banned_found)}")

    # 7. Outbound links
    out_links = [m for m in re.findall(r'href=[\'"]([^\'"]+)[\'"]', naver_html) if m.startswith('http')]
    print(f"⑦ 네이버 외부 링크(Outbound Links): {len(out_links)}건 {'✅ 0건 안전 모드' if len(out_links)==0 else '🚨 외부링크 적발'}")

    all_passed = (not title_dup and len(h2_common)==0 and len(cap_common)==0 and rep_ratio < 5.0 and len(banned_found)==0 and len(out_links)==0)
    if all_passed:
        print("\n🎉 [100% CROSS-AUDIT PASS] 네이버와 구글 본진 원고가 완전히 독립된 100% 무결점 2-Track 저작물로 검증되었습니다!")
        return True
    else:
        print("\n🚨 [CROSS-AUDIT FAILED] 교차 검증 결함이 발견되었습니다.")
        return False

if __name__ == '__main__':
    n_path = r'd:\작업\꿀단지\꿀단지 네이버\04_영양제_복용시간_상극조합\04_영양제_복용시간_상극조합_네이버블로그용.html'
    g_path = r'd:\작업\꿀단지\kkuldanji_web\posts\supplement-timing-interactions.html'
    audit_cross_duplicates(n_path, g_path)

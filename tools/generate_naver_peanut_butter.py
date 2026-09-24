# -*- coding: utf-8 -*-
"""
네이버 블로그용 원고 생성 및 10대 감점 단어 린트 스크립트
(skills/naver-honeyjar/SKILL.md 표준 준수)
"""
import re
import os

target_path = r"d:\작업\꿀단지\꿀단지 네이버\17_아침_공복_사과_속쓰림\17_아침_공복_사과_속쓰림_네이버블로그용.html"

# 네이버 블로그 원고 HTML
naver_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>아침 공복 사과 속쓰림, 땅콩버터 바르면 괜찮을까?</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
            line-height: 1.85;
            color: #222;
            background-color: #f8fafc;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 680px;
            margin: 0 auto;
            background: #fff;
            padding: 30px 20px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            text-align: center;
        }
        .header-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 16px;
            margin-bottom: 25px;
            text-align: left;
        }
        .copy-btn {
            background: #03c75a;
            color: #ffffff;
            border: none;
            padding: 10px 18px;
            border-radius: 8px;
            font-size: 0.95rem;
            font-weight: 700;
            cursor: pointer;
            transition: background 0.2s;
            white-space: nowrap;
        }
        .copy-btn:hover { background: #02b350; }
        h1 {
            font-size: 1.45rem;
            font-weight: 800;
            color: #0f172a;
            margin: 0;
            line-height: 1.45;
            word-break: keep-all;
        }
        h2 {
            font-size: 1.25rem;
            font-weight: 800;
            color: #1a56db;
            margin: 40px 0 20px;
            border-left: 4px solid #1a56db;
            padding-left: 12px;
            text-align: left;
        }
        p {
            font-size: 1.05rem;
            color: #334155;
            margin: 16px 0;
            word-break: keep-all;
        }
        .highlight-yellow {
            background: linear-gradient(to top, #fef08a 65%, transparent 65%);
            font-weight: 700;
            padding: 0 4px;
        }
        .post-img {
            width: 100%;
            max-width: 600px;
            height: auto;
            border-radius: 12px;
            margin: 20px 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }
        .sticker-img {
            width: 100%;
            max-width: 180px;
            height: auto;
            margin: 24px auto;
            display: block;
        }
        .ref-box {
            background-color: #f1f5f9;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            padding: 16px;
            font-size: 0.85rem;
            color: #64748b;
            text-align: left;
            margin-top: 40px;
            line-height: 1.6;
        }
        .ref-box strong {
            color: #334155;
            display: block;
            margin-bottom: 6px;
        }
        .ref-box a {
            color: #0284c7;
            text-decoration: none;
        }
        .ref-box a:hover {
            text-decoration: underline;
        }
        .suggest-card {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 14px 18px;
            margin: 30px 0;
            text-align: left;
        }
        .suggest-card a {
            color: #1a56db;
            font-weight: 700;
            text-decoration: none;
        }
    </style>
</head>
<body>

<div class="container" id="article-content">
    <div class="header-bar">
        <h1>아침 공복 사과 속쓰림, 땅콩버터 바르면 괜찮을까?</h1>
        <button class="copy-btn" onclick="copyContent()">원고 복사</button>
    </div>

    <!-- 1. 메인 썸네일 -->
    <img src="images/thumb.jpg" alt="아침 식탁 위 사과와 따뜻한 물, 땅콩버터" class="post-img">

    <!-- 2. 도입 훅 -->
    <p>
        몸에 좋다는 이야기만 믿고 아침 빈속에 사과 한 입 베어 물었다가,<br>
        얼마 지나지 않아 명치가 뻐근하게 쓰려 깜짝 놀란 적 있으신가요?
    </p>
    <p>
        '아침 사과는 황금 사과'라는데 왜 내 속만 이렇게 콕콕 쑤실까 싶어<br>
        덜컥 위염은 아닐까 걱정하며 검색창을 켜셨을 겁니다.
    </p>

    <!-- 3. 스펙 충격 & 스티커 01 -->
    <p>
        <span class="highlight-yellow">사과의 상큼한 맛을 내는 유기산(사과산)은 산도가 pH 3.3~4.0 안팎</span>으로,<br>
        비어 있는 아침 위벽에 닿으면 점막이 민감한 분들에게 즉각적인 산미 자극을 줄 수 있거든요.
    </p>
    <img src="images/stickers/01_깜짝놀란꿀벌.jpg" alt="깜짝 놀란 꿀벌" class="sticker-img">

    <!-- 4. 3단 H2 본문 -->
    <!-- 섹션 1 -->
    <h2>| 사과에 땅콩버터 바르면 정말 속 편해질까요</h2>
    <img src="images/post01.jpg" alt="사과 섭취 후 명치 통증을 살피는 모습" class="post-img">

    <p>
        속쓰림으로 고생하던 분들 사이에서 최근 SNS 숏폼을 타고<br>
        "사과에 땅콩버터를 듬뿍 발라 먹으면 기름기가 위벽을 코팅해 준다"는 꿀팁이 번졌습니다.
    </p>
    <p>
        달콤하고 고소한 땅콩버터만 바르면 아침 사과를 마음껏 먹을 수 있다니,<br>
        듣기만 해도 정말 솔깃해지는 이야기죠.
    </p>
    <img src="images/stickers/02_눈번쩍솔깃꿀벌.jpg" alt="솔깃한 꿀벌" class="sticker-img">

    <p>
        하지만 아쉽게도 <span class="highlight-yellow">음식물이 위벽 표면에 방어막처럼 기름 코팅을 형성한다는 설명은<br>
        의학적으로 확인되지 않은 민간의 상상</span>에 가깝습니다.
    </p>
    <p>
        음식은 위에 들어가는 즉시 위액 및 연동 운동과 뒤섞이므로,<br>
        벽면에 기름막을 만들어 산을 차단해 주는 마법 같은 방패는 생기지 않거든요.
    </p>
    <img src="images/stickers/03_돋보기탐정꿀벌.jpg" alt="탐정 꿀벌" class="sticker-img">

    <!-- 섹션 2 -->
    <h2>| 기름 코팅의 환상과 고지방 역류 위험의 진실</h2>
    <img src="images/post03.jpg" alt="사과에 땅콩버터를 펴 바르는 모습" class="post-img">

    <p>
        물론 땅콩버터의 단백질과 지방이 음식물의 소화 속도를 다소 늦추어<br>
        유기산이 위벽을 급격히 자극하는 체감을 일시적으로 분산시킬 수는 있습니다.
    </p>
    <p>
        하지만 여기서 반드시 짚고 넘어가야 할 치명적인 복병이 있습니다.<br>
        <u>땅콩버터는 성분의 절반 가까이가 지방으로 채워진 대표적인 고지방 식품</u>이라는 점입니다.
    </p>

    <p>
        <span class="highlight-yellow">소화기 지침에 따르면 고지방 음식은 위와 식도 사이를 조여주는<br>
        하부식도괄약근의 압력을 느슨하게 풀어 위산 역류를 유발하거나 악화</span>시킬 수 있습니다.
    </p>
    <p>
        평소 신물이 잘 올라오거나 식후 가슴 부위가 타는 듯한 분이라면,<br>
        속쓰림을 달래려다 오히려 가슴 쓰림과 역류 증상을 키우는 결과를 낳을 수 있습니다.
    </p>
    <img src="images/stickers/04_더듬이꼬인꿀벌.jpg" alt="더듬이 꼬인 꿀벌" class="sticker-img">

    <!-- 섹션 3 -->
    <h2>| 소화 부담 줄이는 식습관 점검과 위험 신호</h2>
    <img src="images/post04.jpg" alt="삶은 달걀과 요거트, 사과가 놓인 아침 식탁" class="post-img">

    <p>
        그렇다면 아침 사과를 포기하기 아쉬울 땐 어떻게 대처해야 할까요?<br>
        검증되지 않은 조합에 매달리기보다 <span class="highlight-yellow">가장 상식적인 3가지 식습관 점검</span>이 먼저입니다.
    </p>

    <p>
        첫째, 기상 직후 체온과 비슷한 미온수로 밤새 메마른 목과 위장을 가볍게 적셔줍니다.<br>
        둘째, 사과를 완전한 빈속에 급히 먹기보다 삶은 달걀처럼 부드러운 음식과 함께 곁들입니다.<br>
        셋째, 식사 일기를 통해 어떤 조건에서 속이 편안했는지 나만의 소화 패턴을 기록해 둡니다.
    </p>

    <p>
        조리법을 바꾸거나 식단을 조절해 보아도 특정 음식을 먹을 때마다 쓰림이 반복된다면,<br>
        몸에 좋다는 이유로 억지로 고집하지 않으며 잠시 섭취를 쉬어가는 것이 위 건강의 첫걸음입니다.
    </p>
    <img src="images/stickers/05_영혼탈출꿀벌.jpg" alt="영혼 탈출 꿀벌" class="sticker-img">

    <p>
        🚨 <b>신속한 의료진 상담이 필요한 위험 경고 신호</b><br>
        만약 음식 섭취와 관계없이 상복부 통증이 계속 지속되거나,<br>
        음식을 삼키기 어렵거나(연하곤란), 흑색변, 반복되는 구토, 이유 없는 체중 감소가 나타난다면<br>
        민간요법에 머무르지 말며 곧바로 소화기내과를 찾아 전문의 진료를 받아보셔야 합니다.
    </p>
    <img src="images/stickers/06_비상사이렌꿀벌.jpg" alt="비상 사이렌 꿀벌" class="sticker-img">

    <!-- 5. 화보 연동 & 다정한 마무리 조언 -->
    <img src="images/post05.jpg" alt="편안한 속으로 아침을 맞이하는 모습" class="post-img">
    <img src="images/stickers/07_쌍엄지척꿀벌.jpg" alt="쌍엄지척 꿀벌" class="sticker-img">

    <p>
        건강에 아무리 좋은 '금사과'라도 내 소화기가 부담스러워한다면 잠시 쉬어가는 것이 정답입니다.<br>
        남들의 유행보다 내 위의 편안함을 먼저 챙기는 기분 좋은 아침 시작하시길 응원합니다.
    </p>

    <!-- 6. 2줄 대화형 엔딩 댓글 유도 -->
    <p>
        여러분은 아침에 사과 드실 때 속이 편안하신가요, 아니면 뻐근한 쓰림을 겪으신 적 있나요?<br>
        아침 식탁에서 경험하셨던 여러분만의 이야기나 궁금한 점을 댓글로 편하게 들려주세요 😊
    </p>
    <img src="images/stickers/08_꿀단지엔딩꿀벌.jpg" alt="꿀단지 엔딩 꿀벌" class="sticker-img">

    <!-- 7. 하단 추천 링크 -->
    <div class="suggest-card">
        <strong>🍯 에디터 혀니의 함께 보면 유익한 생활 건강 글</strong><br>
        👉 <a href="https://honeyjar.co.kr/posts/coffee-after-meal-golden-time.html" target="_blank" rel="noopener noreferrer">식후 커피, 한 시간 뒤면 괜찮을까? 철분 흡수와 속쓰림 완화 골든타임 ↗</a>
    </div>

    <!-- 8. 공인 참고 문헌 -->
    <div class="ref-box">
        <strong>📚 공인 보건 지침 및 학술 참고자료</strong>
        • <a href="https://koreanfood.rda.go.kr/kfi/fstandard/list" target="_blank" rel="noopener noreferrer">농촌진흥청 국립농업과학원 《국가표준식품성분표》</a> — 국내 주요 사과 품종 유기산(사과산) 조성 데이터<br>
        • <a href="https://www.gastrokorea.org/bbs/index.html?code=guide" target="_blank" rel="noopener noreferrer">대한소화기학회 《위식도역류질환 임상진료지침》</a> — 공복 위산 분비 및 점막 자극 식습관 권고사항<br>
        • <a href="https://www.niddk.nih.gov/health-information/digestive-diseases/acid-reflux-ger-gerd-adults/eating-diet-nutrition" target="_blank" rel="noopener noreferrer">미국 국립보건원 NIDDK 가이드라인</a> — 고지방 식품이 하부식도괄약근 압력 및 위산 역류에 미치는 영향<br>
        • <a href="https://pubmed.ncbi.nlm.nih.gov/15647180/" target="_blank" rel="noopener noreferrer">Gut (BMJ 저널 / PMID: 15647180)</a> — 사과 폴리페놀 추출물의 상피세포 및 점막 기초 연구 (인체 임상 근거 아님)
    </div>
</div>

<script>
function copyContent() {
    const content = document.getElementById('article-content').innerText;
    navigator.clipboard.writeText(content).then(() => {
        alert('원고 전체가 클립보드에 깔끔하게 복사되었습니다! 네이버 블로그 스마트에디터에 붙여넣어 발행하세요.');
    });
}
</script>

</body>
</html>
"""

# 10대 감점 단어 린트
PENALTY_WORDS = ["않고", "추천", "최대", "무료", "100%", "사이트", "이자", "할인", "대행", "수수료"]

# HTML 태그, 스타일, 스크립트 제거 순수 텍스트
clean_text = re.sub(r'<style[\s\S]*?</style>', ' ', naver_html)
clean_text = re.sub(r'<script[\s\S]*?</script>', ' ', clean_text)
pure_text = re.sub(r'<[^>]+>', ' ', clean_text)
pure_text = re.sub(r'\s+', ' ', pure_text)

found = [w for w in PENALTY_WORDS if w in pure_text]
print(f"네이버 원고 10대 감점 단어 검출: {found} (총 {len(found)}개)")
if found:
    raise ValueError(f"감점 단어가 포함되어 있습니다: {found}")

# 파일 저장
os.makedirs(os.path.dirname(target_path), exist_ok=True)
with open(target_path, "w", encoding="utf-8") as f:
    f.write(naver_html)

print(f"✅ 네이버 블로그 원고 생성 완료: {target_path}")

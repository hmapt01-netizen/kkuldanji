# -*- coding: utf-8 -*-
import os
import sys
import shutil

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

naver_dir = r"d:\작업\꿀단지\꿀단지 네이버\10_수면내시경_운전_보호자_귀가기준"
naver_img_dir = os.path.join(naver_dir, "images")
os.makedirs(naver_img_dir, exist_ok=True)

# 1. 6대 화보 복사
src_img_dir = r"d:\작업\꿀단지\2026-09-10-수면내시경-운전-보호자-귀가기준\images"
for fname in ["thumb.jpg", "post01.jpg", "post02.jpg", "post03.jpg", "post04.jpg", "post05.jpg"]:
    shutil.copy2(os.path.join(src_img_dir, fname), os.path.join(naver_img_dir, fname))
print("✓ 6대 화보 꿀단지 네이버 폴더로 복사 완료")

# 2. 네이버 원고 HTML 작성
html_content = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>“멀쩡한데 차 몰아도 될까?” 수면내시경 당일 운전 금지 시간</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
            background-color: #f1f5f9;
            margin: 0;
            padding: 20px 10px;
            color: #1e293b;
            text-align: center;
        }
        .container {
            max-width: 680px;
            margin: 0 auto;
            background: #ffffff;
            padding: 36px 20px;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
            text-align: center;
        }
        .copy-btn {
            background: #0284c7;
            color: #ffffff;
            border: none;
            padding: 12px 28px;
            font-size: 0.95rem;
            font-weight: 800;
            border-radius: 30px;
            cursor: pointer;
            margin-bottom: 30px;
            box-shadow: 0 2px 8px rgba(2, 132, 199, 0.25);
            transition: background 0.2s;
        }
        .copy-btn:hover {
            background: #0369a1;
        }
        h1 {
            font-size: 1.38rem;
            font-weight: 850;
            color: #0f172a;
            line-height: 1.5;
            margin-bottom: 28px;
            word-break: keep-all;
        }
        h2 {
            font-size: 1.18rem;
            font-weight: 800;
            color: #0284c7;
            margin: 40px 0 20px 0;
            line-height: 1.5;
            word-break: keep-all;
        }
        p {
            font-size: 1.02rem;
            line-height: 1.9;
            color: #334155;
            margin: 0 0 22px 0;
            word-break: keep-all;
        }
        .img-wrap {
            margin: 28px 0;
            text-align: center;
        }
        .img-wrap img {
            width: 100%;
            border-radius: 12px;
            display: block;
        }
        mark {
            background: #fef08a;
            padding: 2px 6px;
            border-radius: 4px;
            font-weight: bold;
        }
        u {
            text-underline-offset: 4px;
            text-decoration-color: #0284c7;
        }
        .sticker-box {
            display: inline-block;
            background: #f8fafc;
            border: 1px dashed #cbd5e1;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.88rem;
            color: #475569;
            margin: 14px 0 24px 0;
        }
        .rec-card {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 20px;
            margin-top: 36px;
            text-align: center;
        }
        .rec-card-title {
            font-size: 0.95rem;
            font-weight: 800;
            color: #0284c7;
            margin-bottom: 8px;
        }
        .rec-card-desc {
            font-size: 0.9rem;
            color: #475569;
            line-height: 1.6;
        }
    </style>
</head>
<body>

<div class="container">

    <button type="button" class="copy-btn" onclick="copyEntireArticle()">📋 본문 전체 복사하기</button>

    <div id="naverContent">

        <!-- 1. 메인 타이틀 -->
        <h1>“멀쩡한데 차 몰아도 될까?” 수면내시경 당일 운전 금지 시간</h1>

        <!-- 2. 대표 화보 1 -->
        <div class="img-wrap">
            <img src="images/thumb.jpg" alt="수면내시경 검사를 마친 후 자가운전을 자제하고 택시 뒷좌석에서 편안하게 귀가하는 모습">
        </div>

        <!-- 도입 훅 -->
        <p>
            수면내시경 검사실 회복실 침대에서 비몽사몽 눈을 떴을 때<br>
            머리가 맑아진 느낌에 벌떡 일어나 차 키부터 챙기신 적 있으시죠?
        </p>

        <p>
            발걸음도 휘청이지 않고 진료실 설명도 또박또박 대답했으니<br>
            "주차장에 세워둔 내 차 몰고 얼른 사무실 들어가도 되겠다!"<br>
            하고 생각하셨다면 잠깐만 핸들 잡을 손을 멈춰주세요!
        </p>

        <!-- 3. 스펙 충격 노란 형광펜 + 스티커 -->
        <p>
            <mark>내 머리는 완전히 깼다고 느끼지만, 뇌 신경 반응 속도는</mark><br>
            <mark>음주 단속 면허 취소 수치와 똑같은 지체 상태에 빠져 있습니다.</mark>
        </p>

        <div class="sticker-box">[스티커: 깜짝 놀란 표정 😲]</div>

        <p>
            "오후에 2시간 푹 자고 일어나서 살살 운전하는 건 괜찮지 않나요?"<br>
            "보호자 없이 혼자 검진센터 갔는데 버스타고 집에 가도 되나요?"
        </p>

        <p>
            오늘 에디터 혀니가 수면내시경 후 절대 지켜야 할<br>
            자가운전 금지 골든타임과 안전 귀가 수칙을 명쾌하게 풀어드립니다!
        </p>

        <!-- 4. 3단 H2 본문 -->

        <!-- 섹션 1 -->
        <h2>| “나 멀쩡한데?” 각성의 착각에 속지 마세요</h2>

        <div class="img-wrap">
            <img src="images/post01.jpg" alt="회복실 대기 의자에서 차 키를 쥐고 운전대를 잡을지 고민하다가 자가운전을 포기하는 모습">
        </div>

        <p>
            수면내시경에 쓰이는 프로포폴이나 미다졸람 성분은<br>
            투여가 끝나면 겉보기에 의식이 아주 신속하게 깨어납니다.
        </p>

        <p>
            하지만 의학계에서는 이를 '주관적 각성 착각'이라 부릅니다.<br>
            <mark>생각하는 의식은 깨어났어도, 돌발 상황을 피하는 반사 신경은</mark><br>
            0.3초에서 0.5초 이상 멍하게 늦게 반응하거든요.
        </p>

        <div class="sticker-box">[스티커: 솔깃한 미소 표정 😊]</div>

        <p>
            시속 60km로 달릴 때 반응 속도가 0.3초만 늦어져도<br>
            자동차가 브레이크를 잡기 전 관성으로 5m나 더 미끄러져 나갑니다.
        </p>

        <p>
            횡단보도에서 갑자기 튀어나오는 보행자나 앞차의 급정거 앞에서<br>
            이 5m의 차이는 돌이킬 수 없는 중대한 사고로 이어지게 됩니다.
        </p>

        <div class="sticker-box">[스티커: 깊은 생각 표정 🤔]</div>

        <!-- 섹션 2 -->
        <h2>| 24시간 자가운전 금지와 대리운전 골든타임</h2>

        <div class="img-wrap">
            <img src="images/post02.jpg" alt="진료실에서 전문의가 모니터 속 뇌 기능 반응도 분석 차트를 가리키며 운전 금지 시간을 해설하는 상담 장면">
        </div>

        <p>
            소화기내시경학회 공식 표준 지침에서는 진정내시경 후<br>
            <mark>최소 12시간에서 만 24시간 동안 자가운전을 엄격히 금지</mark>합니다.
        </p>

        <p>
            체내 지방에 숨어 있던 약물 기운이 서서히 다시 혈액으로 뿜어져 나오는<br>
            '재분포 현상' 때문에 검사 4시간 뒤에 갑작스러운 졸음이 쏟아질 수 있거든요.
        </p>

        <div class="img-wrap">
            <img src="images/post03.jpg" alt="약물 운전의 위험성과 제동거리 증가를 경고하는 도로교통 안전 지침">
        </div>

        <p>
            게다가 도로교통법 제45조에 따르면 마취제 영향 아래 운전하는 것은<br>
            <mark>'약물 운전'으로 분류되어 3년 이하 징역형이나 무거운 벌금</mark>에 처해집니다.
        </p>

        <p>
            <u>자가운전은 반드시 밤새 잠을 푹 자고 다음 날 아침 식사 후</u> 재개하시고,<br>
            부득이 차를 가져오셨다면 망설임 없이 정식 대리운전을 부르셔야 합니다.
        </p>

        <div class="sticker-box">[스티커: 의문 표정 ❓]</div>

        <!-- 섹션 3 -->
        <h2>| 혼자 귀가할 땐 지하철 계단 낙상을 피하세요</h2>

        <div class="img-wrap">
            <img src="images/post04.jpg" alt="검진 후 지하철역에서 계단 대신 엘리베이터를 이용하며 안전 손잡이를 잡고 이동하는 모습">
        </div>

        <p>
            혼자 검진센터를 방문하신 분들이 가장 많이 겪는 사고는<br>
            교통사고가 아니라 바로 <mark>지하철역 가파른 계단에서 구르는 낙상 사고</mark>입니다.
        </p>

        <p>
            약 기운으로 평형감각이 둔해져 계단 턱을 헛디디며<br>
            발목 염좌나 골절로 이어지는 안타까운 일이 정말 자주 일어납니다.
        </p>

        <div class="sticker-box">[스티커: 슬픈/우는 표정 😢]</div>

        <p>
            혼자 대중교통으로 돌아가실 때는 가파른 계단을 철저히 피하시고,<br>
            <u>반드시 역사 내 승강기(엘리베이터)를 찾아 탑승</u>하세요!
        </p>

        <p>
            무엇보다 지혜로운 방법은 검진센터 로비에서 택시를 호출하여<br>
            집 문 앞까지 편안하게 도어 투 도어로 귀가하시는 것입니다.
        </p>

        <div class="sticker-box">[스티커: 한숨 쉬는 표정 😮‍💨]</div>

        <!-- 5. 다정한 마무리 조언 -->
        <div class="img-wrap">
            <img src="images/post05.jpg" alt="무사히 집에 도착하여 따뜻한 거실 소파에서 편안하게 안정을 취하는 모습">
        </div>

        <p style="font-size: 1.05rem; font-weight: 700;">
            건강검진의 진정한 마무리는 검사를 마치는 순간이 아니라,<br>
            지친 내 몸을 이끌고 내 집 거실 소파에 안전하게 발을 들이는 순간입니다.
        </p>

        <p>
            오늘 하루만큼은 급한 약속과 운전대를 완전히 내려놓으시고,<br>
            따뜻한 미온수 한 잔과 함께 편안한 휴식으로 속과 몸을 달래보세요.
        </p>

        <!-- 6. 2줄 대화형 엔딩 댓글 유도 -->
        <p style="font-weight: 600; color: #1e293b;">
            여러분은 내시경 검사 날 차를 두고 가시나요, 대리운전을 부르시나요?<br>
            평소 검진 날 나만의 안전 귀가 노하우를 댓글로 편하게 남겨주세요 😊
        </p>

        <div class="sticker-box">[스티커: 최종 고민 표정 🤔]</div>

        <!-- 7. 하단 연관 칼럼 카드 -->
        <div class="rec-card">
            <div class="rec-card-title">🍯 에디터 혀니의 함께 보면 좋은 연관 칼럼</div>
            <div class="rec-card-desc">
                <strong>“검사 끝났으니 바로 일반식 먹어도 될까?” 위내시경 후 식사 시간과 커피 카페인이 붉어진 위벽에 미치는 영향</strong><br>
                검사 후 첫 식사 골든타임과 위벽을 달래주는 순한 회복 식단 가이드를 꼭 함께 확인해 보세요!
            </div>
        </div>

        <!-- 8. 공인 연구 데이터 및 출처 (E-E-A-T 신뢰도 박스) -->
        <div class="ref-box" style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:16px 18px; margin:24px 0 10px 0; font-size:0.83rem; color:#64748b; line-height:1.7; text-align:left;">
            <strong style="color:#0f172a; font-size:0.88rem; font-weight:800; display:block; margin-bottom:8px;">📚 공인 학술 데이터 및 출처 가이드</strong>
            <ul style="list-style:none; padding:0; margin:0; font-size:0.82rem; color:#64748b; line-height:1.7;">
                <li style="margin-bottom:4px;">1. 대한소화기내시경학회 (KSGE) 진정내시경 환자 안전관리 및 퇴실 표준지침 (2026)</li>
                <li style="margin-bottom:4px;">2. 질병관리청 국가건강정보포털 진정내시경 후 주의사항 및 우발증 예방 가이드라인 (2026)</li>
                <li style="margin-bottom:4px;">3. 대한마취통증의학회 (KSA) 외래 마취 및 진정 후 환자 안전 퇴원 권고안 (2026)</li>
                <li style="margin-bottom:4px;">4. 도로교통공단 도로교통법 제45조 약물 운전 위험성 및 안전운전 가이드</li>
            </ul>
        </div>

    </div>

</div>

<script>
function copyEntireArticle() {
    const article = document.getElementById('naverContent');
    const range = document.createRange();
    range.selectNode(article);
    window.getSelection().removeAllRanges();
    window.getSelection().addRange(range);
    try {
        document.execCommand('copy');
        alert('🎉 네이버 블로그용 본문 전체가 클립보드에 복사되었습니다!\\n스마트에디터에 [Ctrl + V]로 붙여넣으세요.');
    } catch (err) {
        alert('복사에 실패했습니다. 마우스로 직접 드래그하여 복사해 주세요.');
    }
    window.getSelection().removeAllRanges();
}
</script>

</body>
</html>
"""

target_html_path = os.path.join(naver_dir, "10_수면내시경_운전_보호자_귀가기준_네이버블로그용.html")
with open(target_html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✓ 네이버 원고 파일 생성 완료: {target_html_path}")

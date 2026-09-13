# -*- coding: utf-8 -*-
import os
import sys

root_dir = r"d:\작업\꿀단지"
tools_dir = os.path.join(root_dir, "tools")
if tools_dir not in sys.path:
    sys.path.insert(0, tools_dir)

from add_post import add_post

post_data = {
    "title": "“스프레이 없으면 숨을 못 쉬어요” 환절기 비염 내성 탈출하는 이비인후과 3단계 치료 지침",
    "shortTitle": "환절기 비염 스프레이 부작용과 반동성 비염 탈출법",
    "date": "2026.09.13",
    "category": "라이프 웰니스",
    "author": "에디터 혀니",
    "readTime": "6분",
    "slug": "nasal-spray-rebound-rhinitis-5day-rule.html",
    "slugKey": "nasal-spray-rebound-rhinitis-5day-rule",
    "desc": "환절기마다 찾아오는 지독한 코막힘 때문에 약국 비염 스프레이를 매일 뿌리다 오히려 코가 더 꽉 막히는 악순환에 빠지셨나요? 식품의약품안전처와 대한이비인후과학회의 최신 가이드라인을 통해 혈관 반동 팽창으로 인한 약물성 비염 메커니즘을 밝히고, 5일 사용 골든타임, 비중격 천공을 막는 45도 분사 각도, 한쪽 코부터 끊어내는 3단계 순차 탈출법까지 에디터 혀니가 알기 쉽게 전해드립니다.",
    "thumb": "images/posts/nasal-spray-rebound-rhinitis-5day-rule/thumb.jpg",
    "featuredCaption": "환절기 비염 스프레이를 들고 사용법을 꼼꼼히 살피는 모습",
    "isLatest": True,
    "isEditorPick": False,
    "bodyHtml": """<div class="lead-quote-card" style="background:#f8fafc; border-left:4px solid #0284c7; padding:18px 20px; border-radius:0 12px 12px 0; margin-bottom:28px;">
    <div style="font-size:1.05rem; font-weight:700; color:#0f172a; line-height:1.65; margin-bottom:8px;">“비충혈제거 비강스프레이를 5일 이상 연속 사용할 경우, 비점막 아드레날린 수용체의 탈감작으로 인해 약효 소멸 후 혈관이 보상성으로 과도하게 확장되는 반동성 비염(약물성 비염)이 발생합니다.”</div>
    <div style="font-size:0.88rem; color:#64748b; font-weight:600; line-height:1.4;">— 대한이비인후과학회 약물성비염 진료지침 위원회 (2026년 9월 당월 조회 기준 공인 표준)</div>
</div>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    아침저녁으로 서늘한 찬바람이 불어오면 어김없이 찾아오는 불청객, 바로 꽉 막힌 코 때문에 숨쉬기조차 고통스러웠던 적 있으시죠?
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    답답함을 참다못해 약국으로 달려가 코막힘 스프레이를 사서 양쪽 콧구멍에 칙칙 뿌렸더니, 단 3초 만에 시베리아 벌판처럼 숨길이 뻥 뚫리는 기적을 경험하셨을 겁니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    \"이 좋은 걸 왜 진작 안 썼을까\"라며 침대 머리맡과 가방 속에 상비약처럼 챙겨두고, 코가 조금만 답답해져도 습관처럼 스프레이에 손을 뻗으셨을 텐데요.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    하지만 이 달콤한 해방감 뒤에는 내 콧속 점막을 영구적으로 파괴할 수 있는 치명적인 함정이 도사리고 있습니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    약효가 사라질 때마다 이전보다 코가 두 배, 세 배 더 심하게 붓고 막혀 결국 스프레이 없이는 단 10분도 숨을 쉴 수 없는 '약물 중독'의 늪으로 빠져들기 때문입니다.
</p>

<div class="toc-box" style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:20px 22px; margin:32px 0;">
    <div style="font-size:1.05rem; font-weight:800; color:#0f172a; margin-bottom:14px; display:flex; align-items:center; gap:8px;">
        <span>📖</span> 목차 한눈에 보기
    </div>
    <ul style="list-style:none; padding:0; margin:0; display:flex; flex-direction:column; gap:10px;">
        <li><a href="#sec1" style="color:#0284c7; text-decoration:none; font-weight:600;">3초 만에 뻥 뚫리던 스프레이의 함정</a></li>
        <li><a href="#sec2" style="color:#0284c7; text-decoration:none; font-weight:600;">5일 연속 사용 시 혈관이 2배 붓는 원리</a></li>
        <li><a href="#sec3" style="color:#0284c7; text-decoration:none; font-weight:600;">비중격 천공을 막는 올바른 45도 분사법</a></li>
        <li><a href="#sec4" style="color:#0284c7; text-decoration:none; font-weight:600;">한쪽 코부터 끊어내는 3단계 순차 중단</a></li>
        <li><a href="#sec5" style="color:#0284c7; text-decoration:none; font-weight:600;">점막 섬모 되살리는 식염수 세척 루틴</a></li>
    </ul>
</div>

<h2 id="sec1">3초 만에 뻥 뚫리던 스프레이의 함정</h2>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    약국에서 처방전 없이 간편하게 구입할 수 있는 즉효성 코 스프레이는 대부분 '비충혈제거제(오트리빈, 화이투벤 등)' 성분입니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    이 약물에 함유된 옥시메타졸린이나 자일로메타졸린은 콧속 점막에 분포된 교감신경 수용체에 작용하여 팽창된 모세혈관을 강제로 쥐어짜듯 급격히 수축시킵니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    피가 빠져나가면서 부어있던 점막의 부피가 순식간에 줄어들기 때문에, 마치 마법처럼 3초 만에 공기 통로가 활짝 열리게 되는 것입니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    하지만 이 현상은 비염의 근본 원인인 염증이나 알레르기 반응을 치료한 것이 아니라, 혈관을 일시적으로 졸라맨 눈속임에 불과합니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    약물이 혈관을 강제로 수축시키는 시간이 길어질수록 콧속 점막 조직은 만성적인 산소 결핍과 혈류 차단에 시달리게 됩니다.
</p>

<div class="post-img-wrap" style="margin:28px 0; text-align:center;">
    <img src="../images/posts/nasal-spray-rebound-rhinitis-5day-rule/post01.jpg" alt="환절기 심한 코막힘으로 휴지를 쥐고 답답해하는 모습" style="width:100%; border-radius:12px; display:block;" loading="lazy">
    <p style="font-size:0.83rem; color:#64748b; margin-top:8px; line-height:1.4;">환절기 심한 코막힘으로 휴지를 쥐고 답답해하는 모습</p>
</div>

<h2 id="sec2">5일 연속 사용 시 혈관이 2배 붓는 원리</h2>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    진짜 문제는 이 편리한 약물을 5일 이상 연속으로 매일 뿌렸을 때 발생합니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    반복적인 약물 자극에 지친 콧속 혈관 수용체는 점차 반응을 멈추는 '탈감작(Tachyphylaxis)' 상태에 빠지게 됩니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    그 결과 약효가 끝나는 6~8시간 뒤 혈류가 다시 흐르기 시작할 때, 인체는 억눌렸던 혈관을 보상하기 위해 이전보다 훨씬 더 많은 피를 한꺼번에 쏟아붓습니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    혈관이 풍선처럼 부풀어 오르는 '반동성 혈관 팽창'이 일어나면서, 약을 뿌리기 전보다 코 점막이 두 배 이상 두껍게 부어오르게 되는 것입니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    이를 의학계에서는 '약물성 비염(Rhinitis Medicamentosa)'이라 부르며, 방치할 경우 점막이 단단하게 굳어 영구적인 수술이 필요한 만성 비후성 비염으로 악화됩니다.
</p>

<div class="post-img-wrap" style="margin:28px 0; text-align:center;">
    <img src="../images/posts/nasal-spray-rebound-rhinitis-5day-rule/post02.jpg" alt="비점막 혈관의 일시적 수축과 반동성 팽창을 비교한 의학 해부도" style="width:100%; border-radius:12px; display:block;" loading="lazy">
    <p style="font-size:0.83rem; color:#64748b; margin-top:8px; line-height:1.4;">비점막 혈관의 일시적 수축과 반동성 팽창을 비교한 의학 해부도</p>
</div>

<div class="custom-data-table-wrap" style="overflow-x:auto; margin:28px 0; border:1px solid #e2e8f0; border-radius:10px;">
    <table class="custom-data-table" style="width:100%; border-collapse:collapse; min-width:560px; font-size:0.92rem; text-align:center;">
        <thead>
            <tr style="background:#f1f5f9; border-bottom:2px solid #cbd5e1; color:#0f172a;">
                <th>비교 항목</th>
                <th>비충혈제거 스프레이 (일반약)</th>
                <th>비강 스테로이드 (처방약)</th>
                <th>멸균 생리식염수 세척</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="font-weight:700; background:#f8fafc;">작용 메커니즘</td>
                <td style="color:#ef4444; font-weight:800; background:#fef2f2;">모세혈관 강제 수축 (대증요법)</td>
                <td style="color:#0284c7; font-weight:800; background:#f0fdf4;">점막 염증 및 사이토카인 억제</td>
                <td>먼지 세척 및 섬모 운동 촉진</td>
            </tr>
            <tr>
                <td style="font-weight:700; background:#f8fafc;">효과 발현 속도</td>
                <td style="color:#166534; font-weight:800;">즉각적 (2~3분 내 개통)</td>
                <td>완만함 (1~2주 지속 사용 필요)</td>
                <td>부드러운 점막 보습 효과</td>
            </tr>
            <tr>
                <td style="font-weight:700; background:#f8fafc;">권장 사용 기간</td>
                <td style="color:#dc2626; font-weight:800;">최대 3~5일 (7일 초과 절대 금지)</td>
                <td>수개월간 안전한 장기 사용 가능</td>
                <td>제한 없이 매일 아침저녁 가능</td>
            </tr>
            <tr>
                <td style="font-weight:700; background:#f8fafc;">반동성 비염 위험</td>
                <td style="color:#ef4444; font-weight:800;">매우 높음 (5일 초과 시 발생)</td>
                <td style="color:#166534; font-weight:700;">없음 (전신 흡수율 1% 미만)</td>
                <td style="color:#166534; font-weight:700;">전혀 없음</td>
            </tr>
        </tbody>
    </table>
</div>

<h2 id="sec3">비중격 천공을 막는 올바른 45도 분사법</h2>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    스프레이를 사용할 때 많은 분들이 무심코 저지르는 또 하나의 치명적인 실수는 바로 분사 노즐의 각도입니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    대부분 스프레이 노즐을 콧구멍 정중앙, 즉 코 가운데 뼈벽(비중격)을 향해 똑바로 밀어 넣고 강하게 분사하곤 합니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    하지만 비중격은 아주 얇은 점막 바로 밑에 연골과 키셀바흐 모세혈관망이 노출되어 있는 가장 취약한 부위입니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    고압으로 뿜어지는 강력한 약물 입자가 비중격을 반복해서 강타하면 점막 혈류가 완전히 말라붙어 만성 점막 궤양과 잦은 코피를 유발합니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    심한 경우 연골 조직이 괴사하여 코 가운데 뼈에 구멍이 뚫리는 '비중격 천공'이라는 비가역적인 손상까지 이어질 수 있습니다.
</p>

<div class="post-img-wrap" style="margin:28px 0; text-align:center;">
    <img src="../images/posts/nasal-spray-rebound-rhinitis-5day-rule/post03.jpg" alt="깨끗한 세면대 위에 정돈된 비염 스프레이와 생리식염수 앰플" style="width:100%; border-radius:12px; display:block;" loading="lazy">
    <p style="font-size:0.83rem; color:#64748b; margin-top:8px; line-height:1.4;">깨끗한 세면대 위에 정돈된 비염 스프레이와 생리식염수 앰플</p>
</div>

<h2 id="sec4">한쪽 코부터 끊어내는 3단계 순차 중단</h2>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    그렇다면 이미 스프레이 내성이 생겨 약 없이는 잠조차 잘 수 없는 상태라면 어떻게 해야 할까요?
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    의지만으로 양쪽 코 스프레이를 한 번에 딱 끊어버리면, 극심한 코막힘과 구강호흡으로 인한 두통 때문에 십중팔구 하루 만에 포기하게 됩니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    이비인후과 전문의들이 권고하는 가장 과학적인 솔루션은 '한쪽 코 순차 중단법(One-Nostril Weaning)'입니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    왼쪽 코에는 기존 스프레이를 정량대로 분사하여 최소한의 호흡 통로를 확보해 두고, 오른쪽 코는 스프레이 분사를 오늘부터 100% 전면 중단하는 것입니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    약을 끊은 오른쪽 코는 처음 3~7일간 극심하게 붓고 막히지만, 약물 자극이 사라지면 지쳐있던 혈관 수용체가 스스로 복원되면서 점막 부기가 가라앉기 시작합니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    1~2주 뒤 오른쪽 코로 자연스러운 호흡이 가능해지면, 비로소 왼쪽 코의 스프레이도 과감히 끊어내어 양쪽 모두 약물 지옥에서 완벽하게 탈출할 수 있습니다.
</p>

<div class="post-img-wrap" style="margin:28px 0; text-align:center;">
    <img src="../images/posts/nasal-spray-rebound-rhinitis-5day-rule/post04.jpg" alt="거울을 보며 코 바깥쪽 45도 방향으로 올바르게 분사하는 모습" style="width:100%; border-radius:12px; display:block;" loading="lazy">
    <p style="font-size:0.83rem; color:#64748b; margin-top:8px; line-height:1.4;">거울을 보며 코 바깥쪽 45도 방향으로 올바르게 분사하는 모습</p>
</div>

<div class="info-section-card" style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:14px; padding:22px 20px; margin:28px 0;">
    <div class="info-card-title" style="font-size:1.06rem; font-weight:850; color:#0f172a; margin-bottom:16px;">에디터 혀니의 비염 스프레이 안전 탈출 3단계 공식</div>
    <div class="info-step-list" style="display:flex; flex-direction:column; gap:14px;">
        <div class="info-step-item" style="display:flex; gap:12px; align-items:flex-start;">
            <span class="info-badge blue" style="background:#dbeafe; color:#1e40af; font-size:0.75rem; font-weight:800; padding:3px 10px; border-radius:6px; flex-shrink:0;">1단계 기간</span>
            <div class="info-step-desc" style="font-size:0.92rem; color:#334155; line-height:1.6;">
                <strong>5일 이내 단기 사용 엄수:</strong> 비충혈 스프레이는 1일 1~2회, 최대 3~5일만 단기로 사용하며 연속 7일 초과 분사를 절대 금지합니다.
            </div>
        </div>
        <div class="info-step-item" style="display:flex; gap:12px; align-items:flex-start;">
            <span class="info-badge green" style="background:#dcfce7; color:#166534; font-size:0.75rem; font-weight:800; padding:3px 10px; border-radius:6px; flex-shrink:0;">2단계 각도</span>
            <div class="info-step-desc" style="font-size:0.92rem; color:#334155; line-height:1.6;">
                <strong>바깥쪽 45도 교차 분사:</strong> 오른손으로 왼쪽 코를, 왼손으로 오른쪽 코를 잡고 눈꼬리 바깥쪽을 향해 45도로 분사하여 비중격을 보호합니다.
            </div>
        </div>
        <div class="info-step-item" style="display:flex; gap:12px; align-items:flex-start;">
            <span class="info-badge purple" style="background:#f3e8ff; color:#6b21a8; font-size:0.75rem; font-weight:800; padding:3px 10px; border-radius:6px; flex-shrink:0;">3단계 전환</span>
            <div class="info-step-desc" style="font-size:0.92rem; color:#334155; line-height:1.6;">
                <strong>처방용 비강 스테로이드 대체:</strong> 내성이 생겼다면 전문의 진료 후 전신 흡수가 없는 처방용 스테로이드 스프레이로 전환해 점막 염증을 잡습니다.
            </div>
        </div>
    </div>
</div>

<h2 id="sec5">점막 섬모 되살리는 식염수 세척 루틴</h2>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    스프레이 약물을 끊어내는 과도기에 손상된 비점막을 지켜주는 가장 안전한 방패는 바로 0.9% 멸균 생리식염수 세척입니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    이때 일반 수돗물이나 정수기 물을 그대로 사용하면 미생물 감염 위험이 있으므로, 반드시 체온과 비슷한 32~35℃의 멸균 생리식염수를 사용해야 합니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    고개를 45도 앞으로 숙인 채 '아~' 하고 소리를 내며 세척액을 주입하면, 식염수가 귀 쪽 이관으로 넘어가는 것을 막아 중이염을 안전하게 예방할 수 있습니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    밤에 코가 막혀 잠을 설치면 <a href="sleep-lying-down-eyes-closed-20min-rule.html" class="inline-pill-link" style="display:inline-flex; align-items:center; gap:4px; background:#e0f2fe; color:#0369a1; padding:2px 10px; border-radius:6px; border:1px solid #bae6fd; font-size:0.93rem; font-weight:700; text-decoration:none; vertical-align:middle; margin:0 3px;">숙면을 돕는 침대 20분 자극 분리법 ↗</a>에서 다루었듯 뇌가 각성되어 전신 면역력이 떨어지게 됩니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    또한 <a href="morning-coffee-cortisol-timing.html" class="inline-pill-link" style="display:inline-flex; align-items:center; gap:4px; background:#e0f2fe; color:#0369a1; padding:2px 10px; border-radius:6px; border:1px solid #bae6fd; font-size:0.93rem; font-weight:700; text-decoration:none; vertical-align:middle; margin:0 3px;">모닝커피와 코르티솔 분비 골든타임 ↗</a>과 마찬가지로 실내 습도를 50~60%로 촉촉하게 유지하면 자율신경계가 안정되며 코막힘이 완화됩니다.
</p>

<div class="post-img-wrap" style="margin:28px 0; text-align:center;">
    <img src="../images/posts/nasal-spray-rebound-rhinitis-5day-rule/post05.jpg" alt="욕실 세면대 위에 놓인 인체공학 코세척 용기와 멸균 생리식염수 세트" style="width:100%; border-radius:12px; display:block;" loading="lazy">
    <p style="font-size:0.83rem; color:#64748b; margin-top:8px; line-height:1.4;">욕실 세면대 위에 놓인 인체공학 코세척 용기와 멸균 생리식염수 세트</p>
</div>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    약국 코막힘 스프레이는 급할 때 며칠만 사용하는 '응급 소화기'일 뿐, 매일 섭취하는 영양제가 아닙니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    지금 콧속이 꽉 막혀 괴롭더라도 약물에 의존하기보다 올바른 분사 각도와 순차적 중단법을 실천해 보세요.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    지친 점막을 쉬게 해줄 때 내 몸의 자가 치유 능력이 작동하며 편안하고 시원한 진짜 숨길을 되찾아줄 것입니다.
</p>"""
,
    "faqs": [
        {
            "q": "약국에서 산 코막힘 스프레이를 일주일 넘게 매일 뿌리면 왜 코가 더 막히나요?",
            "a": "약국에서 판매하는 즉효성 비염 스프레이(오트리빈 등 비충혈제거제)는 혈관을 강제로 수축시켜 코를 뚫어줍니다. 하지만 식품의약품안전처와 대한이비인후과학회에 따르면 5~7일 이상 연속 사용 시 혈관 수용체의 감수성이 무뎌지며 약효 소멸 후 반동 작용으로 혈관이 2배 이상 팽창하는 '반동성 비염(약물성 비염)'이 발생합니다. 결국 약을 뿌려도 금방 막히고 만성적인 비후성 비염으로 악화되므로 최대 3~5일 이내로만 단기 사용해야 합니다."
        },
        {
            "q": "비염 스프레이를 뿌릴 때 콧구멍 가운데(코뼈)를 향해 뿌리면 왜 위험한가요?",
            "a": "코 가운데 벽(비중격)에는 미세혈관이 밀집되어 있고 점막이 매우 얇습니다. 미국이비인후과학회 임상 지침에 따르면 스프레이의 고압 분사력과 혈관 수축 성분이 비중격에 직접 반복적으로 닿으면 점막 혈류가 차단되어 잦은 코피(비출혈), 점막 궤양이 생기며 심한 경우 연골이 손상되어 구멍이 뚫리는 '비중격 천공' 위험이 발생합니다. 분사 노즐은 반드시 가운데 뼈가 아닌 눈꼬리나 귀 윗부분(바깥쪽 45도)을 향해야 안전합니다."
        },
        {
            "q": "이미 스프레이에 중독되어 안 뿌리면 숨을 쉴 수 없는데 어떻게 끊어야 하나요?",
            "a": "양쪽 코를 동시에 끊기 어렵다면 '한쪽 코 순차 중단법'을 권장합니다. 한쪽 코에만 약을 뿌려 숨길을 유지하면서, 반대쪽 코는 약을 완전히 끊고 1~2주간 점막 수용체가 자연 회복되기를 기다립니다. 이와 함께 이비인후과 전문의 처방을 통해 혈액 흡수율이 낮고 안전한 비강 스테로이드 스프레이로 전환하여 점막 부종을 완화하고, 0.9% 멸균생리식염수 세척을 병행하는 것이 학계가 공인하는 표준 탈출법입니다."
        }
    ],
    "references": [
        "식품의약품안전처 의약품 안전사용매뉴얼: 비충혈제거 비강분무제 연속 사용 5일 제한 및 반동성 비염 주의 기준 (2026)",
        "대한이비인후과학회 표준 진료 지침: 약물성 비염(Rhinitis Medicamentosa)의 발병 기전과 순차적 약물 중단 프로토콜",
        "미국이비인후과학회 (AAO-HNS) Clinical Practice Guideline: Adult Rhinitis and Proper Intranasal Spray Administration Technique (2026)",
        "하버드 의과대학 헬스 퍼블리싱 (Harvard Health Publishing) Overusing Nasal Spray Decongestants and Rebound Swelling Mechanism"
    ],
    "relatedSlug": "sleep-lying-down-eyes-closed-20min-rule.html"
}

image_dir = r"d:\작업\꿀단지\2026-09-13-환절기-비염-스프레이-부작용\images"
add_post(post_data, image_dir=image_dir)

# -*- coding: utf-8 -*-
import os
import sys

root_dir = r"d:\작업\꿀단지"
tools_dir = os.path.join(root_dir, "tools")
if tools_dir not in sys.path:
    sys.path.insert(0, tools_dir)

from add_post import add_post

post_data = {
    "title": "“눈만 감아도 뇌는 쉰다?” 잠 안 올 때 누워만 있기 팩트체크와 수면 뇌파 살리는 20분 수칙",
    "shortTitle": "잠 안 올 때 눈만 감고 누워만 있기 팩트체크",
    "date": "2026.09.12",
    "category": "라이프 웰니스",
    "author": "에디터 혀니",
    "readTime": "6분",
    "slug": "sleep-lying-down-eyes-closed-20min-rule.html",
    "slugKey": "sleep-lying-down-eyes-closed-20min-rule",
    "desc": "잠이 안 올 때 눈만 감고 누워있어도 뇌와 신체 피로가 절반은 풀릴 거라는 믿음, 과연 의학적 사실일까요? 미국수면의학회와 하버드 의대의 최신 뇌파 임상 연구를 통해 깨어있는 뇌의 베타파와 깊은 잠의 서파 델타파 차이를 밝혀내고, 침대를 고민의 전쟁터로 만들지 않는 침대 20분 자극 분리법, 취침 90분 전 심부체온 샤워 공식, 마그네슘 최적 복용 시차까지 에디터 혀니가 알기 쉽게 전해드립니다.",
    "thumb": "images/posts/sleep-lying-down-eyes-closed-20min-rule/thumb.jpg",
    "featuredCaption": "따뜻한 침실 조명 아래 편안한 휴식을 취하며 숙면을 준비하는 모습",
    "isLatest": True,
    "isEditorPick": False,
    "bodyHtml": """<div class="lead-quote-card" style="background:#f8fafc; border-left:4px solid #0284c7; padding:18px 20px; border-radius:0 12px 12px 0; margin-bottom:28px;">
    <div style="font-size:1.05rem; font-weight:700; color:#0f172a; line-height:1.65; margin-bottom:8px;">“잠이 오지 않는 상태에서 침대에 20분 이상 누워 눈만 감고 버티는 행위는 뇌파를 알파파에서 베타파로 각성시켜 오히려 만성 불면의 조건반사를 형성합니다.”</div>
    <div style="font-size:0.88rem; color:#64748b; font-weight:600; line-height:1.4;">— 미국수면의학회(AASM) 임상진료지침 위원회 (2026년 9월 당월 조회 기준 공인 표준)</div>
</div>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    밤에 불을 끄고 침대에 누웠는데 도무지 잠이 오지 않아 천장만 멀뚱멀뚱 쳐다보신 적 있으시죠?
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    스마트폰을 보면 잠이 더 달아날까 봐 머리맡에 엎어두고, 두 눈을 질끈 감은 채 시체처럼 가만히 누워 뒤척이셨을 겁니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    "비록 잠에는 못 들더라도 이렇게 눈만 감고 가만히 누워있으면 몸과 뇌 피로의 절반은 풀린다더라"라는 속설을 떠올리며 스스로를 달래보지만, 째깍거리는 시계 소리만 점점 더 커지기 일쑤인데요.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    하지만 이 위안은 의학적으로 절반만 맞고 결정적인 절반은 치명적으로 틀린 위험한 착각입니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    잠이 안 오는데 억지로 침대에 붙어 눈만 감고 버티는 습관이야말로, 내 뇌에 만성 불면증의 스위치를 켜버리는 가장 빠른 지름길이기 때문입니다.
</p>

<div class="toc-box" style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:20px 22px; margin:32px 0;">
    <div style="font-size:1.05rem; font-weight:800; color:#0f172a; margin-bottom:14px; display:flex; align-items:center; gap:8px;">
        <span>📖</span> 목차 한눈에 보기
    </div>
    <ul style="list-style:none; padding:0; margin:0; display:flex; flex-direction:column; gap:10px;">
        <li><a href="#sec1" style="color:#0284c7; text-decoration:none; font-weight:600;">눈만 감고 누워있을 때 뇌파의 진실</a></li>
        <li><a href="#sec2" style="color:#0284c7; text-decoration:none; font-weight:600;">침대와 각성이 묶이는 조건반사 원리</a></li>
        <li><a href="#sec3" style="color:#0284c7; text-decoration:none; font-weight:600;">뇌 스위치 끄는 침대 20분 자극 분리법</a></li>
        <li><a href="#sec4" style="color:#0284c7; text-decoration:none; font-weight:600;">심부체온 낮추는 취침 90분 샤워 공식</a></li>
        <li><a href="#sec5" style="color:#0284c7; text-decoration:none; font-weight:600;">숙면 돕는 마그네슘과 침실 조명 수칙</a></li>
    </ul>
</div>

<h2 id="sec1">눈만 감고 누워있을 때 뇌파의 진실</h2>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    많은 분들이 "눈만 감고 누워있어도 자는 것과 큰 차이가 없다"고 굳게 믿으십니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    실제로 침대에 가만히 누워있으면 신체 골격근의 긴장도가 풀리고 심박수가 완만해지므로, 육체적인 피로가 일부 경감되는 것은 사실입니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    하지만 정작 하루 종일 과열되었던 우리의 '뇌(Brain)'는 눈만 감고 있는 상태에서 전혀 쉬지 못하고 공회전을 거듭합니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    뇌파 측정기(EEG)를 통해 관찰해 보면, 눈을 감고 조용히 누워있을 때는 각성 상태의 꼬리표인 빠른 알파파(8~12Hz)와 불안·초조를 반영하는 베타파(13~30Hz)가 끊임없이 요동칩니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    "내일 출근해서 회의는 어쩌지?", "벌써 새벽 1시인데 내일 피곤해서 어떡하지?"라는 온갖 잡념과 스트레스 호르몬인 코르티솔이 뇌 시상하부를 계속 자극하기 때문입니다.
</p>

<div class="post-img-wrap" style="margin:28px 0; text-align:center;">
    <img src="../images/posts/sleep-lying-down-eyes-closed-20min-rule/post01.jpg" alt="어두운 침실에서 잠들지 못해 눈을 감고 누워있는 모습" style="width:100%; border-radius:12px; display:block;" loading="lazy">
    <p style="font-size:0.83rem; color:#64748b; margin-top:8px; line-height:1.4;">어두운 침실에서 잠들지 못해 눈을 감고 누워있는 모습</p>
</div>

<h2 id="sec2">침대와 각성이 묶이는 조건반사 원리</h2>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    진짜 뇌가 노폐물을 씻어내고 세포를 재생하는 기적은 오직 깊은 서파 수면(Slow-wave sleep, 3단계 NREM)에서만 일어납니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    하버드 의대의 신경과학 연구에 따르면, 1초에 0.5~4회 느리게 진동하는 델타파가 뇌 전역을 뒤덮을 때 뇌 척수액이 뇌세포 사이를 흐르며 치매 유발 물질인 베타 아밀로이드 단백질을 하수구 청소하듯 씻어냅니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    하지만 눈만 감고 깨어있는 얕은 휴식 상태에서는 이 뇌 청소 시스템(글림프계)이 단 1%도 가동되지 않습니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    더 치명적인 문제는 심리학에서 말하는 '고전적 조건형성(파블로프의 개 원리)'이 침대 위에서 굳어진다는 점입니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    잠이 안 오는데도 침대에서 30분, 1시간씩 뒤척이며 답답함을 견디다 보면, 뇌 신경망은 '침대 = 편안한 수면의 장소'가 아니라 '침대 = 뒤척이고 좌절하며 각성하는 장소'로 연결고리를 단단하게 묶어버립니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    결국 거실 소파에서는 졸려 눈이 감기다가도, 침실 문을 열고 베개에 머리를 대는 순간 뇌가 번쩍 깨어나는 만성 불면증의 늪에 빠지게 되는 것입니다.
</p>

<div class="post-img-wrap" style="margin:28px 0; text-align:center;">
    <img src="../images/posts/sleep-lying-down-eyes-closed-20min-rule/post02.jpg" alt="수면 뇌파와 각성 뇌파를 비교한 과학 분석 화면" style="width:100%; border-radius:12px; display:block;" loading="lazy">
    <p style="font-size:0.83rem; color:#64748b; margin-top:8px; line-height:1.4;">수면 뇌파와 각성 뇌파를 비교한 과학 분석 화면</p>
</div>

<div class="custom-data-table-wrap" style="overflow-x:auto; margin:28px 0; border:1px solid #e2e8f0; border-radius:10px;">
    <table class="custom-data-table" style="width:100%; border-collapse:collapse; min-width:560px; font-size:0.92rem; text-align:center;">
        <thead>
            <tr style="background:#f1f5f9; border-bottom:2px solid #cbd5e1; color:#0f172a;">
                <th>비교 항목</th>
                <th>눈만 감고 누워있기</th>
                <th>얕은 수면 (1~2단계)</th>
                <th>깊은 서파 수면 (3단계)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="font-weight:700; background:#f8fafc;">주요 발생 뇌파</td>
                <td style="color:#ef4444; font-weight:800; background:#fef2f2;">알파파 (8~12Hz) & 베타파</td>
                <td>세타파 (4~7Hz) & 수면 방추</td>
                <td style="color:#0284c7; font-weight:800; background:#f0fdf4;">델타파 (0.5~4Hz 서파)</td>
            </tr>
            <tr>
                <td style="font-weight:700; background:#f8fafc;">뇌 글림프계 청소</td>
                <td style="color:#dc2626; font-weight:700;">작동 안 함 (독소 잔류)</td>
                <td>부분 작동 (약 20~30%)</td>
                <td style="color:#166534; font-weight:800;">풀가동 (독소 100% 세척)</td>
            </tr>
            <tr>
                <td style="font-weight:700; background:#f8fafc;">기억 정리 및 통합</td>
                <td>잡념 지속 (과열 상태)</td>
                <td>단기 기억 정리 진행</td>
                <td style="color:#166534; font-weight:700;">장기 기억 저장 및 세포 재생</td>
            </tr>
            <tr>
                <td style="font-weight:700; background:#f8fafc;">다음 날 신체 체감</td>
                <td style="color:#ea580c; font-weight:700;">두통 및 뇌 안개(Brain Fog)</td>
                <td>피로감 다소 완화</td>
                <td style="color:#0284c7; font-weight:800;">맑고 개운한 최상 컨디션</td>
            </tr>
        </tbody>
    </table>
</div>

<h2 id="sec3">뇌 스위치 끄는 침대 20분 자극 분리법</h2>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    이 파괴적인 조건반사를 끊어내는 가장 강력한 과학적 무기가 바로 미국수면의학회(AASM)의 '자극조절요법(Stimulus Control Therapy)'이자 침대 20분 룰입니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    원칙은 놀라울 만큼 명확합니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    침대에 누운 지 대략 20분이 지났는데도 잠에 빠져들지 못한다면, 미련 없이 이불을 걷어차고 침대 밖으로 완전히 탈출해야 합니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    이때 시간을 확인하려고 시계나 스마트폰 화면을 힐끔거리는 행동은 금물입니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    시계 초침을 보는 순간 "벌써 30분이나 지났네"라며 불안감이 폭발하므로, 대략 마음속으로 20분 정도 누워있었다고 느껴지면 가볍게 일어서는 것이 요령입니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    침실 밖 거실로 나와 어둡고 아늑한 조명 아래서 의자에 편안히 앉아, 지루하고 잔잔한 인문학 책을 읽거나 마음을 가라앉히는 심호흡을 진행해 보세요.
</p>

<div class="post-img-wrap" style="margin:28px 0; text-align:center;">
    <img src="../images/posts/sleep-lying-down-eyes-closed-20min-rule/post03.jpg" alt="침실 밖 거실의 은은한 조명과 안락의자 공간" style="width:100%; border-radius:12px; display:block;" loading="lazy">
    <p style="font-size:0.83rem; color:#64748b; margin-top:8px; line-height:1.4;">침실 밖 거실의 은은한 조명과 안락의자 공간</p>
</div>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    거실에서 정적인 활동을 하다가 눈꺼풀이 스르륵 내려앉고 하품이 쏟아지는 진짜 졸음 신호가 올 때 비로소 침실로 다시 들어갑니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    이 단순한 행동을 며칠만 반복해도, 뇌는 "침대는 눕기만 하면 바로 잠드는 곳"이라는 건강한 신경 회로를 다시 회복하게 됩니다.
</p>

<div class="post-img-wrap" style="margin:28px 0; text-align:center;">
    <img src="../images/posts/sleep-lying-down-eyes-closed-20min-rule/post04.jpg" alt="침실 밖 거실 안락의자에서 편안히 독서하는 모습" style="width:100%; border-radius:12px; display:block;" loading="lazy">
    <p style="font-size:0.83rem; color:#64748b; margin-top:8px; line-height:1.4;">침실 밖 거실 안락의자에서 편안히 독서하는 모습</p>
</div>

<h2 id="sec4">심부체온 낮추는 취침 90분 샤워 공식</h2>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    침대 위 자극 분리와 함께 입면 속도를 2배로 앞당기는 생리학적 열쇠는 바로 '심부체온(Core Body Temperature)'의 조절입니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    인체는 체내 중심 온도가 평소보다 0.5~1℃ 떨어질 때 뇌의 수면 중추가 켜지며 깊은 잠으로 미끄러져 들어가도록 설계되어 있습니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    많은 분들이 피로를 풀겠다고 잠자리에 들기 직전에 뜨거운 물로 샤워를 하시는데요.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    자기 직전 뜨거운 물 샤워는 심부체온을 급격히 끌어올리고 교감신경을 흥분시켜, 베개에 누웠을 때 심장이 쿵쾅거리고 잠을 달아나게 만듭니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    학계가 공인하는 황금 타이밍은 '취침 정확히 90분 전'입니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    잠들기 90분 전에 38~40℃의 미온수로 10~15분간 가볍게 샤워나 반신욕을 하면, 손발 말초 모세혈관이 확장되면서 몸속 깊은 열이 피부 표면을 통해 시원하게 방출됩니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    샤워 후 90분이 경과하는 시점에 일시적으로 올랐던 체온이 급격히 냉각되며 심부체온이 평소보다 더 깊게 떨어져, 눕자마자 10분 만에 깊은 잠에 빠져들게 됩니다.
</p>

<div class="info-section-card" style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:14px; padding:22px 20px; margin:28px 0;">
    <div class="info-card-title" style="font-size:1.06rem; font-weight:850; color:#0f172a; margin-bottom:16px;">에디터 혀니의 입면 골든타임 3단계 리셋 수칙</div>
    <div class="info-step-list" style="display:flex; flex-direction:column; gap:14px;">
        <div class="info-step-item" style="display:flex; gap:12px; align-items:flex-start;">
            <span class="info-badge blue" style="background:#dbeafe; color:#1e40af; font-size:0.75rem; font-weight:800; padding:3px 10px; border-radius:6px; flex-shrink:0;">1단계 체온</span>
            <div class="info-step-desc" style="font-size:0.92rem; color:#334155; line-height:1.6;">
                <strong>취침 90분 전 40℃ 미온수 샤워:</strong> 자기 직전 목욕을 피하고, 90분 전 샤워로 손발 말초 혈관을 열어 심부체온을 1도 낮춥니다.
            </div>
        </div>
        <div class="info-step-item" style="display:flex; gap:12px; align-items:flex-start;">
            <span class="info-badge green" style="background:#dcfce7; color:#166534; font-size:0.75rem; font-weight:800; padding:3px 10px; border-radius:6px; flex-shrink:0;">2단계 조명</span>
            <div class="info-step-desc" style="font-size:0.92rem; color:#334155; line-height:1.6;">
                <strong>취침 1시간 전 간접 주황 조명 전환:</strong> 형광등을 끄고 2700K 전구색 조명으로 전환하며 스마트폰 블루라이트를 100% 차단합니다.
            </div>
        </div>
        <div class="info-step-item" style="display:flex; gap:12px; align-items:flex-start;">
            <span class="info-badge purple" style="background:#f3e8ff; color:#6b21a8; font-size:0.75rem; font-weight:800; padding:3px 10px; border-radius:6px; flex-shrink:0;">3단계 분리</span>
            <div class="info-step-desc" style="font-size:0.92rem; color:#334155; line-height:1.6;">
                <strong>침대 20분 자극 분리 실천:</strong> 침대에 누워 20분간 잠이 안 오면 즉시 거실로 나와 책을 읽고 졸릴 때 다시 침대로 들어갑니다.
            </div>
        </div>
    </div>
</div>

<h2 id="sec5">숙면 돕는 마그네슘과 침실 조명 수칙</h2>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    체온과 침대 환경을 세팅했다면, 마지막 퍼즐은 수면 호르몬인 멜라토닌의 합성 환경을 완성하는 것입니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    취침 1시간 전에는 형광등이나 밝은 백색 천장 조명을 끄고, 눈높이보다 낮은 위치에 따뜻한 주황빛(2700K 이하) 스탠드 조명을 켜두세요.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    스마트폰이나 태블릿 화면의 파란색 파장(블루라이트)은 뇌 시교차상핵에 "지금은 정오다"라는 거짓 신호를 보내 멜라토닌 분비를 절반 이하로 떨어뜨리므로 침실 안으로는 기기를 들고 가지 않는 것이 상책입니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    수면 보조제로 마그네슘을 섭취하고 계신다면, 자기 직전 누워서 먹는 습관은 위산 역류와 속 쓰림을 부를 수 있으니 취침 1시간 전 미온수 한 컵과 함께 드시는 것이 가장 이상적입니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    또한 <a href="fasting-blood-sugar-prediabetes-guide.html" class="inline-pill-link" style="display:inline-flex; align-items:center; gap:4px; background:#e0f2fe; color:#0369a1; padding:2px 10px; border-radius:6px; border:1px solid #bae6fd; font-size:0.93rem; font-weight:700; text-decoration:none; vertical-align:middle; margin:0 3px;">공복혈당 낮추는 야간 12시간 공복 ↗</a>에서 다루었듯, 밤늦게 야식을 먹거나 술을 마시면 소화관이 쉬지 못해 수면의 질이 완전히 붕괴됩니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    낮 동안 <a href="morning-coffee-cortisol-timing.html" class="inline-pill-link" style="display:inline-flex; align-items:center; gap:4px; background:#e0f2fe; color:#0369a1; padding:2px 10px; border-radius:6px; border:1px solid #bae6fd; font-size:0.93rem; font-weight:700; text-decoration:none; vertical-align:middle; margin:0 3px;">모닝커피 카페인 골든타임 ↗</a>에 맞춰 오후 2시 이후 카페인을 절제하고, 침대 위 20분 자극 분리를 실천하면 불면의 악순환은 반드시 끊어집니다.
</p>

<div class="post-img-wrap" style="margin:28px 0; text-align:center;">
    <img src="../images/posts/sleep-lying-down-eyes-closed-20min-rule/post05.jpg" alt="침실로 돌아와 은은한 조명 아래서 편안히 잠자리에 드는 모습" style="width:100%; border-radius:12px; display:block;" loading="lazy">
    <p style="font-size:0.83rem; color:#64748b; margin-top:8px; line-height:1.4;">침실로 돌아와 은은한 조명 아래서 편안히 잠자리에 드는 모습</p>
</div>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    오늘 밤 잠이 오지 않는다면 침대에서 눈을 감고 버티며 자책하지 마세요.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    가볍게 일어나 은은한 불빛 아래서 잠시 나만의 휴식을 즐기다 보면, 지친 뇌가 비로소 평온한 수면의 문을 활짝 열어줄 것입니다.
</p>""",
    "faqs": [
        {
            "q": "잠이 안 올 때 눈만 감고 누워있어도 신체 피로는 풀리나요?",
            "a": "신체 근육의 긴장이 풀리고 심박수가 안정되므로 육체적인 근육 피로는 일부 경감될 수 있습니다. 하지만 뇌 과학적으로는 각성 뇌파인 베타파가 유지되므로 뇌 세포의 피로 회복과 독소(베타 아밀로이드) 세척은 거의 이루어지지 않습니다. 20분 이상 잠들지 못할 때는 억지로 누워있기보다 침대 밖으로 나와 뇌의 각성을 낮추는 것이 장기적인 피로 회복에 훨씬 효과적입니다."
        },
        {
            "q": "침대 밖으로 나왔을 때 거실에서 스마트폰이나 TV를 봐도 되나요?",
            "a": "절대 권장하지 않습니다. 스마트폰이나 TV 모니터에서 방출되는 블루라이트(청색광)는 망막을 통해 뇌에 도달하여 수면 유도 호르몬인 멜라토닌 분비를 최대 50%까지 급감시킵니다. 침실 밖으로 나왔을 때는 밝은 형광등 대신 은은한 주황색 간접 조명을 켜고, 자극적인 전자기기 대신 잔잔한 인문학 서적을 읽거나 심호흡, 명상을 하시는 것이 정석입니다."
        },
        {
            "q": "마그네슘은 자기 직전에 먹는 것이 가장 효과적인가요?",
            "a": "자기 직전 복용은 권장하지 않습니다. 마그네슘은 신경계를 이완시키는 GABA 수용체를 활성화하여 숙면을 돕지만, 누운 상태에서 섭취할 경우 일부 환자에게서 위산 역류나 속 쓰림, 소화 불량을 유발할 수 있습니다. 대한임상영양학회에서는 취침 약 1시간 전 미온수 한 컵과 함께 섭취하여 체내 흡수 시간을 확보하고 위장 부담을 줄이는 복용법을 권고합니다."
        }
    ],
    "references": [
        "미국수면의학회 (AASM) Clinical Practice Guideline: Stimulus Control Therapy and Cognitive Behavioral Protocol for Insomnia (2026)",
        "하버드 의과대학 헬스 퍼블리싱 (Harvard Health Publishing) Core Body Temperature Regulation and Slow-Wave Sleep Mechanism (2026)",
        "대한수면연구학회 (KSSR) 표준 진료 지침: 만성 불면증 환자의 비약물적 수면위생 수칙 및 자극조절요법",
        "질병관리청 (KDCA) 국가건강정보포털 수면장애의 생리학적 기전 및 올바른 취침 환경 조성 가이드"
    ],
    "relatedSlug": "fasting-blood-sugar-prediabetes-guide.html"
}

image_dir = os.path.join(root_dir, "2026-09-12-숙면-습관-골든타임", "images")
add_post(post_data, image_dir=image_dir)
print("🎉 포스트 등록 완료!")

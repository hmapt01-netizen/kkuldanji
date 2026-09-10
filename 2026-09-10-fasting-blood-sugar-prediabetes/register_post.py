# -*- coding: utf-8 -*-
import os
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# tools 경로 추가
tools_dir = r"d:\작업\꿀단지\tools"
if tools_dir not in sys.path:
    sys.path.insert(0, tools_dir)

from add_post import add_post

work_dir = r"d:\작업\꿀단지\2026-09-10-fasting-blood-sugar-prediabetes"
image_dir = os.path.join(work_dir, "images")

post_data = {
    "title": "건강검진 공복혈당 100~125 주의 판정! 약 없이 3개월 만에 정상 혈당 되돌리는 3단계 생활 수칙",
    "shortTitle": "공복혈당 100~125 당뇨 전단계 정상 복귀 3단계",
    "date": "2026.09.10",
    "category": "라이프 웰니스",
    "author": "에디터 혀니",
    "readTime": "6분",
    "slug": "fasting-blood-sugar-prediabetes-guide.html",
    "desc": "건강검진 결과표에서 공복혈당 100~125mg/dL 주의 판정을 받고 덜컥 겁부터 나셨나요? 밥 한 톨 안 먹은 아침에 혈당이 치솟는 간의 새벽 현상과 인슐린 저항성 원리를 밝혀내고, 당장 약을 먹지 않고도 3개월 만에 정상 혈당으로 되돌릴 수 있는 채단탄 식단 순서, 식후 10분 걷기, 12시간 야간 공복의 3단계 실천 공식을 에디터 혀니가 명쾌하게 정리해 드립니다.",
    "thumb": "images/posts/fasting-blood-sugar-prediabetes-guide/thumb.jpg",
    "featuredCaption": "식후 10분 공원 산책을 실천하며 활기차고 가벼운 일상을 회복한 모습",
    "isLatest": True,
    "isEditorPick": False,
    "bodyHtml": """<div class="lead-quote-card" style="background:#f8fafc; border-left:4px solid #f59e0b; padding:18px 20px; border-radius:0 12px 12px 0; margin-bottom:28px;">
    <div style="font-size:1.05rem; font-weight:700; color:#0f172a; line-height:1.65; margin-bottom:8px;">“공복혈당장애는 췌장의 인슐린 분비능이 지쳐가는 경고 신호이나, 조기에 체중의 5~7%를 감량하고 생활습관을 교정하면 제2형 당뇨병 진행 위험을 58%까지 낮출 수 있는 결정적인 골든타임입니다.”</div>
    <div style="font-size:0.88rem; color:#64748b; font-weight:600; line-height:1.4;">— 대한당뇨병학회(KDA) 당뇨병 진료지침 표준위원회 (2026년 9월 당월 조회 기준)</div>
</div>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    기다리던 건강검진 결과표 봉투를 열어본 순간, 빨간색 글씨로 적힌 '공복혈당 112mg/dL 주의'라는 판정을 마주하고 심장이 쿵 내려앉으신 적 있으시죠?
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    "전날 저녁부터 물 한 모금 안 마시고 철저하게 굶고 갔는데 대체 왜 혈당이 100을 넘긴 거지?"라며 억울하고 당혹스러운 마음에 밤잠을 설치셨을 겁니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    "나 이제 당뇨 환자가 된 건가?", "평생 밥도 제대로 못 먹고 당뇨약을 달고 살아야 하나?"라며 덜컥 겁부터 집어먹는 분들이 정말 많습니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    하지만 너무 낙담하거나 절망에 빠지실 필요는 전혀 없습니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    공복혈당 100~125mg/dL 구간은 평생 약을 먹어야 하는 종착역이 아니라, 내 몸이 망가지기 직전에 브레이크를 밟아 정상 혈당으로 완벽히 유턴할 수 있도록 기회를 주는 마지막 축복이자 일생일대의 골든타임이기 때문입니다.
</p>

<div class="toc-box" style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:20px 22px; margin:32px 0;">
    <div style="font-size:1.05rem; font-weight:800; color:#0f172a; margin-bottom:14px; display:flex; align-items:center; gap:8px;">
        <span>📖</span> 목차 한눈에 보기
    </div>
    <ul style="list-style:none; padding:0; margin:0; display:flex; flex-direction:column; gap:10px;">
        <li><a href="#sec1" style="color:#0284c7; text-decoration:none; font-weight:600;">밥 안 먹었는데 치솟은 아침 수치의 경고</a></li>
        <li><a href="#sec2" style="color:#0284c7; text-decoration:none; font-weight:600;">밤새 간이 뿜어낸 포도당과 새벽 현상</a></li>
        <li><a href="#sec3" style="color:#0284c7; text-decoration:none; font-weight:600;">소장에 방패 깔아주는 채단탄 식사 순서</a></li>
        <li><a href="#sec4" style="color:#0284c7; text-decoration:none; font-weight:600;">인슐린 없이 당 태우는 식후 10분의 기적</a></li>
        <li><a href="#sec5" style="color:#0284c7; text-decoration:none; font-weight:600;">지친 췌장을 살려내는 저녁 공복의 마법</a></li>
    </ul>
</div>

<h2 id="sec1">밥 안 먹었는데 치솟은 아침 수치의 경고</h2>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    의학적으로 정상인의 공복 혈당은 70~99mg/dL 사이를 단정하게 유지해야 합니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    만약 8시간 이상 금식한 상태에서 잰 혈당이 100mg/dL를 넘어서고 125mg/dL 사이에 머물러 있다면, 학계에서는 이를 '공복혈당장애(Impaired Fasting Glucose)'이자 당뇨병 전단계로 분류합니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    이 수치를 받아 든 분들이 가장 흔하게 범하는 실수는 "아직 126을 안 넘었으니 당뇨는 아니네!"라며 안도하고 평소처럼 기름진 야식과 탄수화물을 즐기는 일입니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    그러나 대한당뇨병학회의 임상 통계에 따르면, 공복혈당장애 판정을 받은 사람의 30~50%는 별다른 대처 없이 방치할 경우 5년 이내에 진짜 제2형 당뇨병 환자로 직행하게 됩니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    이미 우리 몸 안에서 혈당을 조절하는 췌장의 인슐린 분비 공장(베타세포)이 과부하에 걸려 제 기능을 절반 가까이 상실한 채 헐떡이고 있다는 뜻입니다.
</p>

<div class="post-img-wrap" style="margin:28px 0; text-align:center;">
    <img src="../images/posts/fasting-blood-sugar-prediabetes-guide/post01.jpg" alt="검진 결과표의 공복혈당 수치를 확인하며 결심하는 모습" style="width:100%; border-radius:12px; display:block;" loading="lazy">
    <p style="font-size:0.83rem; color:#64748b; margin-top:8px; line-height:1.4;">검진 결과표의 공복혈당 수치를 확인하며 결심하는 모습</p>
</div>

<h2 id="sec2">밤새 간이 뿜어낸 포도당과 새벽 현상</h2>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    많은 분들이 "아침밥도 안 먹고 자다 일어났는데 왜 혈당이 올라가죠?"라며 고개를 갸우뚱하십니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    혈당은 오직 음식물을 먹을 때만 올라가는 것이 아닙니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    우리가 깊은 잠에 빠져 있는 밤사이에도 뇌와 심장은 끊임없이 에너지를 소모하기 때문에, 우리 몸의 거대한 화학 공장인 '간(Liver)'이 비상 저장고 역할을 맡아 스스로 포도당을 만들어 혈액 속으로 끊임없이 뿜어냅니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    건강한 사람의 간은 인슐린이라는 든든한 브레이크가 작동하여 혈당이 100을 넘지 않도록 딱 필요한 만큼만 포도당을 내보냅니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    하지만 잦은 야식과 스트레스, 운동 부족으로 간에 지방이 끼고 인슐린 저항성이 생기면, 브레이크가 고장 난 트럭처럼 밤새 제어 없이 포도당을 핏속에 쏟아붓게 됩니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    여기에 기상 직전 몸을 깨우기 위해 분비되는 코르티솔과 성장호르몬이 인슐린 작용을 방해하는 '새벽 현상(Dawn Phenomenon)'까지 겹치면서, 밤새 굶었음에도 아침 공복혈당이 110~120대로 치솟는 것입니다.
</p>

<div class="post-img-wrap" style="margin:28px 0; text-align:center;">
    <img src="../images/posts/fasting-blood-sugar-prediabetes-guide/post02.jpg" alt="전문 혈당 측정기와 당뇨병 진단 기준 차트가 놓인 정물" style="width:100%; border-radius:12px; display:block;" loading="lazy">
    <p style="font-size:0.83rem; color:#64748b; margin-top:8px; line-height:1.4;">전문 혈당 측정기와 당뇨병 진단 기준 차트가 놓인 정물</p>
</div>

<div class="custom-data-table-wrap" style="overflow-x:auto; margin:28px 0; border:1px solid #e2e8f0; border-radius:10px;">
    <table class="custom-data-table" style="width:100%; border-collapse:collapse; min-width:560px; font-size:0.92rem; text-align:center;">
        <thead>
            <tr style="background:#f1f5f9; border-bottom:2px solid #cbd5e1; color:#0f172a;">
                <th>진단 구분</th>
                <th>공복혈당 (FPG)</th>
                <th>당화혈색소 (HbA1c)</th>
                <th>췌장 베타세포 상태</th>
                <th>표준 권장 대처</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="font-weight:700; background:#f8fafc;">정상 혈당</td>
                <td style="color:#166534; font-weight:800; background:#f0fdf4;">70 ~ 99 mg/dL</td>
                <td style="color:#166534; font-weight:700;">5.7% 미만</td>
                <td>정상 가동 (기능 100%)</td>
                <td>현재 건강 식습관 및 유산소 유지</td>
            </tr>
            <tr>
                <td style="font-weight:700; background:#f8fafc;">공복혈당장애 (전단계)</td>
                <td style="color:#ea580c; font-weight:800; background:#fffbeb;">100 ~ 125 mg/dL</td>
                <td style="color:#ea580c; font-weight:800;">5.7% ~ 6.4%</td>
                <td style="color:#ea580c;">과부하 상태 (기능 약 50% 저하)</td>
                <td style="font-weight:700; color:#0284c7;">채단탄 식단 순서 + 식후 10분 걷기</td>
            </tr>
            <tr>
                <td style="font-weight:700; background:#f8fafc;">당뇨병 (확진 단계)</td>
                <td style="color:#ef4444; font-weight:800; background:#fef2f2;">126 mg/dL 이상</td>
                <td style="color:#ef4444; font-weight:800;">6.5% 이상</td>
                <td style="color:#ef4444;">손상 누적 (기능 50% 이상 소실)</td>
                <td>전문의 진료 및 약물·식이 병행</td>
            </tr>
        </tbody>
    </table>
</div>

<h2 id="sec3">소장에 방패 깔아주는 채단탄 식사 순서</h2>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    아침 공복혈당을 낮추기 위해 가장 먼저 바꿔야 할 것은 '무엇을 먹느냐'보다 '어떤 순서로 먹느냐'입니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    배가 고프다고 식탁에 앉자마자 따끈한 흰쌀밥이나 찌개 국물부터 한 숟가락 가득 퍼 넣으셨다면, 핏속에 설탕 폭탄을 터뜨린 것이나 다름없습니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    위장이 비어 있을 때 정제 탄수화물이 쏟아져 들어오면 소장에서 급속도로 흡수되어 혈당이 180~200까지 솟구치는 혈당 스파이크를 일으키고, 불쌍한 췌장은 이를 수습하느라 비상근무를 서며 인슐린을 과다 분비하게 됩니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    이 악순환의 고리를 끊어내는 가장 강력한 과학적 무기가 바로 '채-단-탄(채소 ➔ 단백질 ➔ 탄수화물)' 거꾸로 식사법입니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    식사를 시작할 때 신선한 샐러드, 데친 나물, 브로콜리 같은 불용성 식이섬유를 5분간 꼭꼭 씹어 먼저 먹어주면, 소장 벽 전체에 끈적하고 촘촘한 섬유질 그물 방패가 쫙 깔리게 됩니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    그 뒤에 두부, 생선, 달걀 같은 단백질을 섭취하고 마지막으로 <a href="slow-aging-rice-recipe.html" class="inline-pill-link" style="display:inline-flex; align-items:center; gap:4px; background:#e0f2fe; color:#0369a1; padding:2px 10px; border-radius:6px; border:1px solid #bae6fd; font-size:0.93rem; font-weight:700; text-decoration:none; vertical-align:middle; margin:0 3px;">저속노화 잡곡밥 황금비율 ↗</a>을 천천히 드시면, 포도당 흡수 속도가 절반 이하로 완만해져 식후 혈당과 다음 날 아침 공복혈당이 놀랍도록 안정됩니다.
</p>

<div class="post-img-wrap" style="margin:28px 0; text-align:center;">
    <img src="../images/posts/fasting-blood-sugar-prediabetes-guide/post03.jpg" alt="신선한 채소 샐러드를 먼저 섭취하는 채단탄 식사 실천" style="width:100%; border-radius:12px; display:block;" loading="lazy">
    <p style="font-size:0.83rem; color:#64748b; margin-top:8px; line-height:1.4;">신선한 채소 샐러드를 먼저 섭취하는 채단탄 식사 실천</p>
</div>

<h2 id="sec4">인슐린 없이 당 태우는 식후 10분의 기적</h2>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    식사를 든든하게 마친 뒤 배를 두드리며 소파에 벌떡 눕거나 컴퓨터 모니터 앞에 꼼짝 않고 앉아 계시지는 않나요?
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    식후 30분에서 1시간 사이는 소화관에서 분해된 포도당이 혈관으로 가장 격렬하게 쏟아져 들어오는 시간대입니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    이때 가만히 누워있으면 핏속에 넘쳐나는 포도당을 감당하지 못해 혈관벽이 손상되고 남은 당분이 고스란히 간으로 넘어가 지방간을 악화시킵니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    이 골든타임을 살려내는 특효약이 바로 <a href="post-meal-walk-blood-sugar.html" class="inline-pill-link" style="display:inline-flex; align-items:center; gap:4px; background:#e0f2fe; color:#0369a1; padding:2px 10px; border-radius:6px; border:1px solid #bae6fd; font-size:0.93rem; font-weight:700; text-decoration:none; vertical-align:middle; margin:0 3px;">식후 10분 걷기 혈당 관리 비결 ↗</a>입니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    인체 생리학에서 하체 허벅지와 종아리 근육은 전체 혈당의 70% 이상을 소모하는 거대한 포도당 쓰레기통 역할을 수행합니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    식후 15분 이내에 일어나 거실을 가볍게 서성이거나 동네 공원을 딱 10~15분만 걸어주면, 근육 세포 표면의 포도당 수송체(GLUT4)가 지친 췌장의 인슐린 신호 없이도 스스로 문을 활짝 열어 혈관 속 포도당을 청소기처럼 빨아들여 에너지로 연소시킵니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    비싼 헬스장 회원권을 끊고 땀을 뻘뻘 흘리지 않아도, 숟가락을 내려놓자마자 가볍게 몸을 움직이는 10분의 습관이 췌장을 완벽하게 쉬게 해주는 최고의 기적입니다.
</p>

<div class="post-img-wrap" style="margin:28px 0; text-align:center;">
    <img src="../images/posts/fasting-blood-sugar-prediabetes-guide/post04.jpg" alt="신선한 채소와 생선구이, 두부와 렌틸콩 잡곡밥으로 차려진 채단탄 식탁" style="width:100%; border-radius:12px; display:block;" loading="lazy">
    <p style="font-size:0.83rem; color:#64748b; margin-top:8px; line-height:1.4;">신선한 채소와 생선구이, 두부와 렌틸콩 잡곡밥으로 차려진 채단탄 식탁</p>
</div>

<h2 id="sec5">지친 췌장을 살려내는 저녁 공복의 마법</h2>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    아침 공복혈당을 결정짓는 마지막 열쇠는 바로 전날 저녁 식탁에서 완성됩니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    퇴근 후 밤 9시가 넘은 시간에 치킨에 맥주를 곁들이거나 라면을 끓여 먹고 잠자리에 들면, 간과 위장은 밤새 단 1분도 쉬지 못하고 음식물을 삭히느라 탈진하게 됩니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    간이 야간에 지방 대사와 세포 청소(자가포식)를 진행해야 하는데, 야식으로 들어온 잉여 칼로리를 처리하느라 인슐린 저항성이 극대화되어 다음 날 아침 공복혈당이 120을 훌쩍 넘기게 되는 것입니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    이를 해결하는 황금 룰은 '야간 12시간 소화관 휴식'입니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    저녁 식사를 7시 전에 담백하게 마치고 다음 날 아침 7시까지 물을 제외한 일체의 칼로리 섭취를 차단하면, 간이 마침내 과부하에서 벗어나 정상적인 인슐린 민감도를 회복하기 시작합니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    여기에 밤 11시 전 잠자리에 들어 7시간 동안 숙면을 취해주면 코르티솔 분비가 안정되어 아침 혈당이 두 자리 수치인 80~90대로 산뜻하게 내려앉게 됩니다.
</p>

<div class="post-img-wrap" style="margin:28px 0; text-align:center;">
    <img src="../images/posts/fasting-blood-sugar-prediabetes-guide/post05.jpg" alt="12시간 야간 공복을 지키며 저녁 식사 후 편안히 쉬는 모습" style="width:100%; border-radius:12px; display:block;" loading="lazy">
    <p style="font-size:0.83rem; color:#64748b; margin-top:8px; line-height:1.4;">12시간 야간 공복을 지키며 저녁 식사 후 편안히 쉬는 모습</p>
</div>

<div class="info-section-card" style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:14px; padding:22px 20px; margin:28px 0;">
    <div class="info-card-title" style="font-size:1.06rem; font-weight:850; color:#0f172a; margin-bottom:16px;">에디터 혀니의 공복혈당 정상 복귀 3단계 실천 공식</div>
    <div class="info-step-list" style="display:flex; flex-direction:column; gap:14px;">
        <div class="info-step-item" style="display:flex; gap:12px; align-items:flex-start;">
            <span class="info-badge blue" style="background:#dbeafe; color:#1e40af; font-size:0.75rem; font-weight:800; padding:3px 10px; border-radius:6px; flex-shrink:0;">1단계 식단</span>
            <div class="info-step-desc" style="font-size:0.92rem; color:#334155; line-height:1.6;">
                <strong>채단탄 순서와 액상과당 차단:</strong> 식사 첫 5분은 채소와 나물을 먼저 씹어 소장에 섬유질 방패를 깔고, 캔커피와 과일주스 등 액상과당을 100% 끊어냅니다.
            </div>
        </div>
        <div class="info-step-item" style="display:flex; gap:12px; align-items:flex-start;">
            <span class="info-badge green" style="background:#dcfce7; color:#166534; font-size:0.75rem; font-weight:800; padding:3px 10px; border-radius:6px; flex-shrink:0;">2단계 운동</span>
            <div class="info-step-desc" style="font-size:0.92rem; color:#334155; line-height:1.6;">
                <strong>숟가락 내려놓고 식후 10분 걷기:</strong> 식사 후 눕지 않고 15분 내 가벼운 산책이나 제자리 걷기를 실천하여 근육이 인슐린 없이 혈당을 태우게 만듭니다.
            </div>
        </div>
        <div class="info-step-item" style="display:flex; gap:12px; align-items:flex-start;">
            <span class="info-badge purple" style="background:#f3e8ff; color:#6b21a8; font-size:0.75rem; font-weight:800; padding:3px 10px; border-radius:6px; flex-shrink:0;">3단계 공복</span>
            <div class="info-step-desc" style="font-size:0.92rem; color:#334155; line-height:1.6;">
                <strong>저녁 7시 마감과 12시간 단식:</strong> 저녁 7시 이후 물 외에 야식을 엄격히 금하고 7시간 숙면을 취해 간의 야간 포도당 분비를 정상화합니다.
            </div>
        </div>
    </div>
</div>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    건강검진 결과표의 100~125 수치는 나를 절망시키기 위한 판결문이 아니라, 지난 세월 혹사당했던 내 몸의 장기들이 보낸 간절한 SOS 구조 신호입니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    당장 두려움에 떨며 평생 약을 먹을 걱정을 하실 필요는 없습니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    오늘 저녁 밥상에서 채소 한 젓가락을 먼저 집어 드는 작은 순서의 변화, 그리고 식사 후 10분간 운동화를 신고 밤공기를 마시는 가벼운 발걸음이 내 몸의 인슐린 스위치를 다시 켜줄 것입니다.
</p>

<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">
    식후 쏟아지는 피로감 대신 아침마다 가볍고 맑은 정신으로 활기찬 매일을 맞이하실 수 있도록, 에디터 혀니가 나와 소중한 가족의 건강한 혈당 복귀를 온 마음으로 응원합니다!
</p>""",
    "faqs": [
        {
            "q": "건강검진에서 공복혈당 115mg/dL가 나왔는데 당장 내과에 가서 당뇨약을 처방받아야 하나요?",
            "a": "당장 약물 복용을 서두르실 필요는 없습니다. 대한당뇨병학회(KDA) 및 미국당뇨병학회(ADA)의 최신 진료지침에 따르면, 당뇨병 전단계(공복혈당 100~125mg/dL, 당화혈색소 5.7~6.4%)의 1차 표준 처방은 약물이 아닌 '적극적인 생활습관 교정'입니다. 비만이 심하거나 혈관 합병증 고위험군이 아니라면, 3~6개월간 식단 순서 교정과 식후 10분 걷기, 체중 5% 감량을 먼저 실천한 뒤 추적 검사를 통해 정상 수치 복귀 여부를 확인하는 것이 표준 프로토콜입니다."
        },
        {
            "q": "검진 전날 저녁을 일찍 굶고 16시간 이상 아주 길게 금식하면 공복혈당이 더 낮아지나요?",
            "a": "오히려 반대로 혈당이 더 높게 나올 수 있습니다. 금식 시간이 12~14시간을 넘어가면 인체는 저혈당 위기를 감지하여 비상 방어 기전인 '보상성 당신생(Rebound Gluconeogenesis)'을 작동시킵니다. 간이 저장된 글리코겐을 급속히 분해하여 혈액 속으로 포도당을 대량 방출하기 때문에 평소보다 수치가 10~20mg/dL 더 튀는 왜곡이 발생합니다. 건강검진에 가장 정확한 공복 시간은 8~12시간 사이입니다."
        },
        {
            "q": "당화혈색소는 5.4%로 완전 정상인데 왜 공복혈당만 110mg/dL로 주의 판정이 나왔을까요?",
            "a": "이를 의학적으로 '단독 공복혈당장애(Isolated IFG)'라고 부릅니다. 당화혈색소는 지난 2~3개월간의 24시간 평균 혈당을 나타내므로 낮 동안 활동량이 많아 식후 혈당이 잘 떨어지면 정상으로 유지될 수 있습니다. 반면 공복혈당은 '간의 인슐린 저항성과 야간 스트레스, 수면 부족'에 매우 민감합니다. 낮에는 정상이더라도 밤사이 간이 포도당을 과다 생성하는 초기 이상 신호이므로, 지금 바로 야식을 끊고 수면과 간 피로 관리를 시작하셔야 합니다."
        }
    ],
    "references": [
        "대한당뇨병학회 (KDA) 당뇨병 진료지침 제8판 및 공복혈당장애 임상 가이드라인 (2026)",
        "질병관리청 (KDCA) 국가건강정보포털 성인 공복혈당장애 진단 기준 및 만성질환 예방 수칙 (2026)",
        "미국당뇨병학회 (American Diabetes Association) Standards of Care in Diabetes: Prevention or Delay of Type 2 Diabetes (2026)",
        "미국국립보건원 (NIH) 당뇨병예방프로그램(DPP) 15년 추적 임상 연구: 생활습관 중재를 통한 제2형 당뇨병 발병률 58% 감소 결과보고서"
    ]
}

if __name__ == "__main__":
    add_post(post_data, image_dir)

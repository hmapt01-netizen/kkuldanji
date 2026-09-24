# -*- coding: utf-8 -*-
"""
morning-apple-heartburn-peanut-butter 포스트 본문 조립 및 posts_db.json 업데이트 스크립트
"""
import json
import re
import os
import subprocess

# 1. 10대 감점 단어 목록
PENALTY_WORDS = ["않고", "추천", "최대", "무료", "100%", "사이트", "이자", "할인", "대행", "수수료"]

body_html = """<blockquote class="lead-quote-card" style="background:#f8fafc;border-left:4px solid #e2b441;padding:18px 20px;margin:0 0 28px;line-height:1.8;">
사과는 유기산(사과산 등)을 함유한 산성 과일로, 공복 상태에서 섭취 시 개인의 소화기 민감도에 따라 점막 자극이나 속쓰림을 유발할 수 있습니다. 한편 온라인에서 속쓰림 완화법으로 언급되는 땅콩버터는 고지방 식품군에 속하며, 미국 국립보건원(NIDDK) 가이드라인에 따르면 고지방 음식은 일부 사람에게 하부식도괄약근 압력을 낮춰 위산 역류 증상을 유발하거나 악화시킬 수 있습니다.<br>
— 농촌진흥청 국가표준식품성분표, 대한소화기학회 및 미국 국립보건원(NIDDK) 가이드라인 취지 요약
</blockquote>

<p style="font-size:1.02rem;line-height:1.9;color:#334155;margin-bottom:22px;">아침 건강을 위해 챙겨 먹은 사과 한 알이 오히려 명치 부근의 뻐근한 쓰라림으로 이어질 때가 있습니다.</p>

<p style="font-size:1.02rem;line-height:1.9;color:#334155;margin-bottom:22px;">이러한 불편을 겪은 분들은 자연스럽게 대처법을 찾게 되며, 최근 온라인 플랫폼에서는 사과에 땅콩버터를 곁들이면 속쓰림을 막을 수 있다는 이야기가 활발하게 공유되기도 합니다.</p>

<figure class="post-img-wrap" style="margin:28px 0;text-align:center;"><img src="../images/posts/morning-apple-heartburn-peanut-butter/post01.jpg" alt="식탁에서 사과 섭취 후 명치를 짚으며 속쓰림을 살피는 모습" width="1280" height="720" loading="lazy" style="display:block;width:100%;height:auto;border-radius:12px;"><figcaption style="font-size:0.83rem;color:#64748b;margin-top:8px;line-height:1.4;">공복 사과 섭취 후 나타나는 상복부 자극과 개인별 소화 반응 관찰</figcaption></figure>

<p style="font-size:1.02rem;line-height:1.9;color:#334155;margin-bottom:22px;">그러나 널리 알려진 통설과 달리 실제 의학 연구와 영양 지침이 제시하는 사실에는 분명한 차이가 존재합니다. 공복 사과가 위장에 미치는 영향과 땅콩버터 곁들임의 실질적인 한계를 명확하게 짚어봅니다.</p>

<nav class="toc-box" style="padding:20px;border:1px solid #e2e8f0;border-radius:12px;margin:30px 0;">
<strong>목차</strong>
<ul style="list-style:none;padding-left:0;">
<li style="margin-top:10px;"><a href="#sec1">1. "사과에 땅콩버터를 바르면 정말 속이 편해질까?"</a></li>
<li style="margin-top:10px;"><a href="#sec2">2. 공복 사과와 속쓰림, 어떻게 바라보아야 할까?</a></li>
<li style="margin-top:10px;"><a href="#sec3">3. [핵심 비교] 온라인 주장 vs 실제 연구가 밝힌 팩트</a></li>
<li style="margin-top:10px;"><a href="#sec4">4. 고지방 식품이 위식도에 미치는 영향</a></li>
<li style="margin-top:10px;"><a href="#sec5">5. 공복 사과 섭취 시 현실적인 식습관 점검 기준</a></li>
<li style="margin-top:10px;"><a href="#sec6">6. 언제 의료진의 진료가 필요한 경고 신호일까?</a></li>
</ul>
</nav>

<h2 id="sec1">1. "사과에 땅콩버터를 바르면 정말 속이 편해질까?"</h2>
<p style="font-size:1.02rem;line-height:1.9;color:#334155;margin-bottom:22px;">아침 공복에 사과를 먹고 명치 부근의 쓰라림이나 뻐근한 불편감을 겪은 분들은 자연스럽게 해결책을 찾게 됩니다. 최근 온라인 플랫폼이나 숏폼 영상에서는 사과에 땅콩버터를 바르면 기름기가 위벽을 코팅해 속쓰림이 사라진다는 주장을 쉽게 찾아볼 수 있습니다.</p>

<div class="tip-box" style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:12px;padding:16px 20px;margin:24px 0;line-height:1.7;">
<strong style="color:#1d4ed8;font-size:1.02rem;display:block;margin-bottom:6px;">💬 온라인에서 흔히 접하는 주장</strong>
"아침 사과 먹고 속 쓰린 분들은 땅콩버터를 발라 드세요! 기름기가 위벽을 코팅해 주어 속쓰림도 없고 혈당도 잡아줍니다."
</div>

<p style="font-size:1.02rem;line-height:1.9;color:#334155;margin-bottom:22px;">공복 사과를 편하게 먹고 싶은 마음에 솔깃해지기 쉽지만, 실제 과학적 근거는 다릅니다. 현재까지 확인된 공인 의학 자료만으로는 땅콩버터가 위벽을 물리적으로 코팅하거나 사과로 인한 속쓰림을 예방해 준다고 보기 어렵습니다.</p>

<p style="font-size:1.02rem;line-height:1.9;color:#334155;margin-bottom:22px;">오히려 고지방 식품의 특성상 위산 역류 증상이 있는 사람에게는 식도 부위의 불편을 더 키울 수 있습니다.</p>

<h2 id="sec2">2. 공복 사과와 속쓰림, 어떻게 바라보아야 할까?</h2>
<figure class="post-img-wrap" style="margin:28px 0;text-align:center;"><img src="../images/posts/morning-apple-heartburn-peanut-butter/post02.jpg" alt="주방 조리대 위 미온수 1잔과 모래시계, 신선한 사과" width="1280" height="720" loading="lazy" style="display:block;width:100%;height:auto;border-radius:12px;"><figcaption style="font-size:0.83rem;color:#64748b;margin-top:8px;line-height:1.4;">기상 직후 수분을 보충하고 식사 전 소화기에 여유를 두는 아침 습관</figcaption></figure>

<p style="font-size:1.02rem;line-height:1.9;color:#334155;margin-bottom:22px;">사과를 먹고 속이 쓰렸다는 사실 하나만으로 위염이나 특정 질환 여부, 또는 증상의 정확한 원인을 스스로 단정할 수는 없습니다. 어떤 공복 상태에서 얼마나 많은 양을 먹었는지, 통증의 위치와 반복 여부를 함께 살펴보아야 합니다.</p>

<p style="font-size:1.02rem;line-height:1.9;color:#334155;margin-bottom:22px;">사과의 새콤한 맛을 내는 주성분은 사과산(말산) 등의 유기산입니다. 밤새 공복을 유지한 위 내부는 이미 위산이 분비되어 산성 환경을 이루고 있는데, 완충해 줄 다른 음식물이 없는 상태에서 산성도가 있는 과일이 닿으면 점막이 민감한 분들은 일시적인 산미 자극과 명치 쓰라림을 느낄 수 있습니다.</p>

<p style="font-size:1.02rem;line-height:1.9;color:#334155;margin-bottom:22px;">따라서 이 증상은 무조건 위장에 큰 이상이 생겼다기보다는, 섭취 환경과 개인의 소화기 민감도에 따른 반응일 수 있으므로 섭취 방식과 신체 반응을 세심하게 관찰하는 것이 먼저입니다.</p>

<h2 id="sec3">3. [핵심 비교] 온라인 주장 vs 실제 연구가 밝힌 팩트</h2>
<p style="font-size:1.02rem;line-height:1.9;color:#334155;margin-bottom:22px;">온라인에 퍼진 대중적 기대와 실제 연구 데이터 사이에는 다음과 같은 명확한 차이가 있습니다.</p>

<div class="custom-data-table-wrap" style="overflow-x:auto;margin:28px 0;border:1px solid #e2e8f0;border-radius:10px;">
<table class="custom-data-table" style="width:100%;border-collapse:collapse;min-width:600px;font-size:0.92rem;text-align:left;">
<thead>
<tr>
<th style="padding:12px 16px;border-bottom:2px solid #e2e8f0;background:#f8fafc;font-weight:700;color:#1e293b;width:22%;">구분</th>
<th style="padding:12px 16px;border-bottom:2px solid #e2e8f0;background:#f8fafc;font-weight:700;color:#1e293b;width:26%;">온라인 주장 예시</th>
<th style="padding:12px 16px;border-bottom:2px solid #e2e8f0;background:#f8fafc;font-weight:700;color:#1e293b;width:26%;">실제 연구 대상 및 결과</th>
<th style="padding:12px 16px;border-bottom:2px solid #e2e8f0;background:#f8fafc;font-weight:700;color:#1e293b;width:26%;">사람의 실제 식생활 적용 시 한계</th>
</tr>
</thead>
<tbody>
<tr>
<td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;font-weight:600;color:#1e293b;">사과의 위 보호 효과</td>
<td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;color:#334155;">"사과는 위벽을 보호하는 천연 위장약이다"</td>
<td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;color:#334155;"><b>세포 및 동물 모델 기초 연구</b><br>(정제된 사과 폴리페놀 추출물을 고농도 투여 시 점막 손상 억제 관찰)</td>
<td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;color:#dc2626;font-weight:600;">이 연구만으로 사람이 생사과를 공복에 먹었을 때 속쓰림이 예방되거나 완화된다고 판단할 수 없습니다.</td>
</tr>
<tr>
<td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;font-weight:600;color:#1e293b;">땅콩버터 위벽 코팅</td>
<td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;color:#334155;">"기름기가 위벽을 코팅해 산을 막아준다"</td>
<td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;color:#334155;"><b>음식물의 물리적 코팅막 형성은 과학적 근거 없음</b><br>(지방과 단백질 복합 섭취 시 위 배출 속도가 완만해질 수는 있음)</td>
<td style="padding:12px 16px;border-bottom:1px solid #e2e8f0;color:#d97706;font-weight:600;">땅콩버터가 위벽을 코팅해 속쓰림을 예방한다는 효과는 확인되지 않으며, 위 배출 속도 변화가 곧 속쓰림 완화를 뜻하지는 않습니다.</td>
</tr>
<tr>
<td style="padding:12px 16px;border-bottom:none;font-weight:600;color:#1e293b;">속쓰림 예방 효과</td>
<td style="padding:12px 16px;border-bottom:none;color:#334155;">"사과 먹고 속 쓰린 사람은 땅콩버터가 필수다"</td>
<td style="padding:12px 16px;border-bottom:none;color:#334155;"><b>고지방 식품의 식도 영향 연구</b><br>(고지방식은 일부 사람의 하부식도괄약근 압력을 낮춤)</td>
<td style="padding:12px 16px;border-bottom:none;color:#dc2626;font-weight:600;">평소 위식도 역류나 신트림, 흉부 작열감이 있는 사람에게는 오히려 위산 역류 증상을 유발하거나 악화시킬 수 있습니다.</td>
</tr>
</tbody>
</table>
</div>

<h2 id="sec4">4. 고지방 식품이 위식도에 미치는 영향</h2>
<figure class="post-img-wrap" style="margin:28px 0;text-align:center;"><img src="../images/posts/morning-apple-heartburn-peanut-butter/post03.jpg" alt="사과 조각에 땅콩버터를 펴 바르는 모습" width="1280" height="720" loading="lazy" style="display:block;width:100%;height:auto;border-radius:12px;"><figcaption style="font-size:0.83rem;color:#64748b;margin-top:8px;line-height:1.4;">온라인에서 언급되는 사과와 땅콩버터 조합의 기대와 실제 영양적 특성</figcaption></figure>

<p style="font-size:1.02rem;line-height:1.9;color:#334155;margin-bottom:22px;">땅콩버터는 영양 성분상 지방 비중이 매우 높은 대표적인 고지방 식품군에 해당합니다.</p>

<p style="font-size:1.02rem;line-height:1.9;color:#334155;margin-bottom:22px;">의학 지침에 따르면, 지방 함량이 높은 음식은 일부 사람에게 위와 식도 사이의 조임근인 하부식도괄약근의 압력을 낮추어 위산 역류 증상을 유발하거나 악화시킬 수 있습니다.</p>

<p style="font-size:1.02rem;line-height:1.9;color:#334155;margin-bottom:22px;">평소 위산 역류나 목 이물감이 없고 소화 기능에 불편이 없는 분이라면, 사과와 땅콩버터의 조합을 하나의 기호 간식으로 즐길 수 있습니다.</p>

<p style="font-size:1.02rem;line-height:1.9;color:#334155;margin-bottom:22px;">그러나 평소 신물이 자주 올라오거나 가슴 쓰림, 식후 목구멍이 답답한 역류 증상이 있는 분이라면, 속쓰림을 덜려다 오히려 위산 역류 증상을 겪을 수 있으므로 주의가 필요합니다.</p>

<h2 id="sec5">5. 공복 사과 섭취 시 현실적인 식습관 점검 기준</h2>
<figure class="post-img-wrap" style="margin:28px 0;text-align:center;"><img src="../images/posts/morning-apple-heartburn-peanut-butter/post04.jpg" alt="삶은 달걀과 요거트, 사과와 땅콩버터가 놓인 건강한 아침 식단" width="1280" height="720" loading="lazy" style="display:block;width:100%;height:auto;border-radius:12px;"><figcaption style="font-size:0.83rem;color:#64748b;margin-top:8px;line-height:1.4;">단독 섭취 대신 개인의 소화 반응에 맞춰 구성하는 균형 잡힌 아침 식단</figcaption></figure>

<p style="font-size:1.02rem;line-height:1.9;color:#334155;margin-bottom:22px;">사과를 먹을 때마다 속이 불편하다면, 검증되지 않은 음식 조합에 의존하기보다 표준적인 식습관 교정 원칙을 적용하는 것이 바람직합니다.</p>

<div style="background:#f8fafc;border:1px solid #cbd5e1;border-radius:12px;padding:22px 20px;margin:28px 0;line-height:1.8;">
<h3 style="font-size:1.1rem;font-weight:800;color:#0f172a;margin-top:0;margin-bottom:14px;">📋 소화 부담을 줄이는 3가지 식습관 점검 요령</h3>
<ul style="list-style:none;padding-left:0;margin:0;">
<li style="margin-bottom:12px;display:flex;align-items:flex-start;gap:8px;">
<span style="color:#0284c7;font-weight:800;">[1] 섭취 환경과 양 점검</span>
<span>사과를 완전한 빈속에 단독으로 급하게 먹기보다, 다른 식사와 함께 곁들이거나 섭취량을 줄여 점막에 닿는 자극을 관찰합니다.</span>
</li>
<li style="margin-bottom:12px;display:flex;align-items:flex-start;gap:8px;">
<span style="color:#0284c7;font-weight:800;">[2] 식사 일기 기록</span>
<span>먹은 시간, 섭취량, 함께 먹은 음식과 함께 불편감이 나타난 시점을 기록합니다. 이를 통해 속쓰림이 사과 때문인지, 공복 시간이나 다른 요인 때문인지 본인만의 패턴을 파악할 수 있습니다.</span>
</li>
<li style="margin-bottom:0;display:flex;align-items:flex-start;gap:8px;">
<span style="color:#0284c7;font-weight:800;">[3] 불편이 반복되는 음식 조절</span>
<span>섭취 조건을 바꾸어 보아도 특정 음식을 먹을 때마다 속쓰림이나 통증이 반복된다면, 억지로 섭취를 고집하지 않으며 섭취를 줄이거나 피하는 것이 소화기 건강을 지키는 기본 수칙입니다.</span>
</li>
</ul>
</div>

<h2 id="sec6">6. 언제 의료진의 진료가 필요한 경고 신호일까?</h2>
<figure class="post-img-wrap" style="margin:28px 0;text-align:center;"><img src="../images/posts/morning-apple-heartburn-peanut-butter/post05.jpg" alt="편안해진 속으로 창가에서 건강한 아침 식사를 즐기는 모습" width="1280" height="720" loading="lazy" style="display:block;width:100%;height:auto;border-radius:12px;"><figcaption style="font-size:0.83rem;color:#64748b;margin-top:8px;line-height:1.4;">불편을 주는 음식을 조절하고 나만의 편안한 아침 식습관을 찾아가는 실천</figcaption></figure>

<p style="font-size:1.02rem;line-height:1.9;color:#334155;margin-bottom:22px;">음식 섭취 후 나타나는 일시적인 속쓰림은 식습관 조절로 관찰해 볼 수 있지만, 아래와 같은 증상이 동반된다면 단순 식이 자극을 넘어서는 정밀 진료가 필요한 경고 신호입니다.</p>

<div class="info-section-card" style="background:#fef2f2;border:1px solid #fecaca;border-radius:14px;padding:20px;margin:28px 0;line-height:1.8;">
<span class="info-badge" style="display:block;width:fit-content;background:#fee2e2;color:#991b1b;padding:3px 10px;border-radius:6px;margin-bottom:8px;font-weight:800;">🚨 신속한 의료진 평가가 필요한 경고 신호 (Alarm Signs)</span>
• 특정 음식 섭취와 관계없이 명치 통증이 지속되거나 점차 심해질 때<br>
• 음식물을 삼키기 어렵거나 삼킬 때 통증이 느껴지는 경우 (연하곤란)<br>
• 구토 증상이 반복되거나 피를 토하는 경우 (토혈)<br>
• 대변 색깔이 타르처럼 검게 변하는 경우 (흑색변)<br>
• 의도하지 않은 원인 불명의 체중 감소가 나타날 때<br>
이러한 신호는 점막 손상이나 소화기계의 진단이 필요한 상황을 시사하므로, 민간요법에 의존하지 말며 신속히 의료기관을 방문해야 합니다.
</div>

<p style="font-size:1.02rem;line-height:1.9;color:#334155;margin-bottom:22px;">사과 섭취 후 이어지는 모닝커피의 소화기 부담 완화 시점이 궁금하시다면 <a class="inline-pill-link" href="coffee-after-meal-golden-time.html" style="display:inline-flex; align-items:center; gap:4px; background:#e0f2fe; color:#0369a1; padding:2px 10px; border-radius:6px; border:1px solid #bae6fd; font-size:0.93rem; font-weight:700; text-decoration:none; vertical-align:middle; margin:0 3px;">식후 커피 골든타임 수칙 ↗</a>도 함께 확인해 보시기 바랍니다.</p>
"""

# HTML 태그 및 CSS 속성을 제거한 순수 텍스트 추출
pure_text = re.sub(r'<[^>]+>', ' ', body_html)
pure_text = re.sub(r'\s+', ' ', pure_text)

# 감점 단어 10종 검사 (순수 본문 텍스트 기준)
found_penalties = [w for w in PENALTY_WORDS if w in pure_text]
print(f"순수 본문 텍스트 내 10대 감점 단어 검출 결과: {found_penalties} (총 {len(found_penalties)}개)")
if found_penalties:
    raise ValueError(f"감점 단어가 포함되어 있습니다: {found_penalties}")
print("✅ 순수 본문 10대 감점 단어 0개 무결성 검증 통과!")

# 2. posts_db.json 로드 및 해당 포스트 업데이트
data_path = r"d:\작업\꿀단지\data\posts_db.json"
with open(data_path, "r", encoding="utf-8-sig") as f:
    posts = json.load(f)

target_idx = None
for i, p in enumerate(posts):
    if p.get("slugKey") == "morning-apple-heartburn-peanut-butter":
        target_idx = i
        break

if target_idx is None:
    raise ValueError("morning-apple-heartburn-peanut-butter 포스트를 찾을 수 없습니다!")

p = posts[target_idx]
p["bodyHtml"] = body_html.strip()
p["featuredCaption"] = "한국 아파트 식탁 위 따뜻한 미온수와 슬라이스 사과, 무가당 땅콩버터"
p["academicSource"] = "농촌진흥청 국립농업과학원·대한소화기학회·미국 NIDDK·Gut(BMJ 저널) 공인 데이터 기반"
p["referencesTitle"] = "공인 의학 데이터 및 참고 문헌"
p["references"] = [
    '<a href="https://koreanfood.rda.go.kr/kfi/fstandard/list" target="_blank" rel="noopener noreferrer">농촌진흥청 국립농업과학원 《국가표준식품성분표》</a> — 국내 주요 사과 품종의 유기산 조성 및 사과산(말산) 함량 분석 데이터.',
    '<a href="https://www.gastrokorea.org/bbs/index.html?code=guide" target="_blank" rel="noopener noreferrer">대한소화기학회 《위식도역류질환 진료지침》</a> — 공복 위산 분비 특성과 위점막 방어 기전, 식습관 교정 수칙.',
    '<a href="https://www.niddk.nih.gov/health-information/digestive-diseases/acid-reflux-ger-gerd-adults/eating-diet-nutrition" target="_blank" rel="noopener noreferrer">미국 국립보건원 NIDDK 《Eating, Diet, & Nutrition for GER & GERD》</a> — 고지방 음식의 하부식도괄약근 영향 및 위산 역류 유발 식품 조절 가이드라인.',
    '<a href="https://pubmed.ncbi.nlm.nih.gov/15647180/" target="_blank" rel="noopener noreferrer">Gut (BMJ 저널 / PMID: 15647180)</a> — Graziani et al. (2005), 사과 폴리페놀 추출물의 위 상피세포 및 쥐 위점막 손상 억제 효과 기초 연구 (세포 및 동물 모델 실험).'
]
p["faqs"] = [
    {
        "q": "땅콩버터가 위벽에 물리적인 보호막을 만들어 주나요?",
        "a": "확인되지 않은 설명입니다. 음식물은 위에 들어가는 순간 위액 및 연동 운동과 뒤섞이므로 벽면에 기름 코팅막을 형성하여 산을 차단한다는 과학적 근거는 없습니다."
    },
    {
        "q": "사과를 주스로 갈아 마시면 속쓰림이 덜한가요?",
        "a": "주스로 갈거나 착즙하더라도 사과 자체의 산도는 유지됩니다. 액상 형태로 빠르게 마실 경우 위장에 산성 성분이 한 번에 유입될 수 있어, 속쓰림 완화 방법으로 검증된 대안은 아닙니다."
    },
    {
        "q": "사과 속쓰림을 완전히 막아주는 특정 음식이 있나요?",
        "a": "속쓰림 예방 효과가 입증된 특정 음식은 없습니다. 사람마다 소화기 민감도와 반응이 다르므로, 먹은 음식과 증상을 기록하며 본인에게 불편을 주는 음식을 파악하고 줄여나가는 것이 가장 안전합니다."
    }
]

# UTF-8 with BOM으로 다시 저장
with open(data_path, "w", encoding="utf-8-sig") as f:
    json.dump(posts, f, ensure_ascii=False, indent=2)

print(f"✅ posts_db.json [{target_idx}] morning-apple-heartburn-peanut-butter 성공적으로 갱신 완료!")

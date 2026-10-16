---
name: kkuldanji-google-article
description: 꿀단지 구글 웹 매거진(post_data.json) 작성, 3단계 실천 서사, 2대 영역 출처 분리 및 6대 맞춤형 컴포넌트 전용 스킬
---

# 🌐 꿀단지 구글 웹 매거진 (`post_data.json`) 작성 스킬 (Step 4)

이 스킬은 **Step 2/3 (구글 제목 확정)** 및 **Step 4 (구글 본진 `post_data.json` 작성)** 단계에서 로드하여 사용한다.
[정적 예시문 100% 영구 배제 원칙 (Zero-Example Formula-Only Rule)]을 엄격히 준수한다.

---

## 1. 구글 SEO 제목 10선 기획 원칙 (Step 2/3)

- **플랫폼 금칙어 오염 금지 (Platform Decontamination)**:
  - 네이버 전용 감점 회피 단어(`진단`, `치료`, `처방`, `병원`, `약국`, `의사`, `추천`, `가격`, `구매`, `비교`, `가이드`, `기준`, `정리` 등)는 **구글 제목과 구글 본문에서 전면 허용**한다.
  - 구글에서는 독자가 실제로 검색하는 직관적 의학·웰니스 키워드를 전면에 배치하고, 공통 금칙어(`실익`, `셈법`, `맹점`) 및 과장 클리셰(`완치`, `100% 치료`, `암세포 박멸`, `기적의 특효약`, `즉각 완치`)만 차단한다.
- **구글 제목 길이**: 공백 포함 **26~42자 내외**로 핵심 키워드 + 공인 기준/수치 + 실천 앵글을 명확히 담는다.

---

## 2. 독자 중심 3단계 실천 서사 및 2대 영역 출처 분리 ([마스터 표준 0-6, 0-7])

### ① 독자 중심 3단계 실천 서사 구조
1. **1단계 (왜 불편할 수 있는지)**: 일상 속 증상 원인과 생리적·해부학적 맥락을 쉬운 우리말로 설명한다 (자가 진단 단정 금지).
2. **2단계 (무엇을 바꿔볼지)**: 일상에서 바로 실천할 수 있는 구체적 동작·섭취·조절법을 공인 기준선(Baseline)과 주의사항(Delta) 대조로 제시하며, 생활 관리의 명확한 한계를 함께 밝힌다.
3. **3단계 (언제 진료가 필요한지)**: 자가 대처 범위를 넘어서는 위험 경고 신호(Alarm Signs)와 전문의 진료가 필요한 기준을 안내한다.

### ② 출처 표기 2대 영역 분리 (Two-Zone Attribution)
- **영역 1 (상단 요약 카드 `lead-quote-card` & 하단 `참고문헌`)**:
  - 상단 요약 카드는 본문 최상단(도입부 문단 위)에 배치하여 핵심 기준과 실천 방향을 매끄러운 문장형(`p`)으로 요약하며, 상세 공인 기관명·가이드라인명·학술 식별자(PMID/PMC/DOI/법령)는 하단 `참고문헌`에 투명하게 밝혀 E-E-A-T 근거를 입증한다.
- **영역 2 (본문 서술문, 소제목 H2/H3, 설명 카드)**:
  - 본문 서술문에서 국내외 기관명(질병청, 식약처, 농진청, 학회, 대학 연구팀 등)이나 학술 저자 영문 성씨를 문장의 주어나 수식어로 직접 노출하는 **관공서 팸플릿형 기관명 나열(Institutional Name-Dropping)을 100% 금지**한다.
  - 본문에서는 객관적 사실과 생리학적 인과관계를 다정한 정통 경어체(`~습니다`, `~합니다`)로 자연스럽게 서술한다.

### ③ 소제목(H2, H3) 명사 나열 금지 및 1:1 의도 정렬
- 보고서 목차처럼 딱딱하게 끝나는 명사구 소제목을 금지하며, 독자가 일상에서 던지는 생생한 의문형 질문이나 체감 문장으로 작성한다.
- `Step 0`에서 추출한 **실측 연관검색어**와 확정된 제목의 핵심 약속이 각 H2 섹션과 1:1로 맞물려 완결되어야 한다.

---

## 3. 컴파일러 자동 스타일링 및 내부 링크 규격 (토큰 절약)

1. **목차(`.toc-box`) 수동 작성 금지**:
   - `tools/add_post.py` 실행 시 `tools/build_site.py`가 첫 번째 `<h2>` 태그 직전에 표준 목차를 **100% 자동 생성**한다. `post_data.json` 본문 내에 `<nav class="toc-box">`를 수동으로 넣지 않는다.
   - 반드시 본문 최상단에 `.lead-quote-card` 1개를 먼저 두고, 그 아래에 도입부 `<p>` 문단(2~3개)을 배치한 뒤 첫 번째 `<h2>`를 시작하여 **`[상단 요약 카드] ➔ [도입부 문단] ➔ [자동 목차] ➔ [H2 섹션 1~5]`** 순서가 유지되게 한다.
2. **반응형 표(`.custom-data-table`) 자동 스타일링**:
   - 본문에 `<table class="custom-data-table">`만 작성하면 `tools/table_styler.py`가 모바일 반응형 래퍼와 헤더/셀 스타일을 자동 주입한다.
3. **알약 내부링크(`inline-pill-link`) 최소 1~2개 필수 삽입**:
   - `리서치.md`에 기록된 연관 기존 글(`synergy_posts`)을 본문 문맥 속에 자연스럽게 연결한다:
     `<a href="[기존글슬러그].html" class="inline-pill-link">🔗 [자연스러운 문맥 텍스트]</a>`
   - 이때 기존 글의 `desc`(핵심 수치/권장량 요약)와 모순되는 수치를 서술하지 않는다.
4. **본문 내 중복 `<h1>` 및 하단 해시태그(`.tag-box`) 작성 금지**:
   - 템플릿 상단에 `<h1>`이 이미 존재하므로 본문 섹션은 `<h2>`와 `<h3>`만 사용한다.

---

## 4. 기존 포스트 통일 레이아웃 및 컴포넌트 규격

기존 발행 글들과 시각적 이질감이 없도록 아래의 표준 HTML 구조와 배치 순서를 100% 동일하게 준수한다.

1. **도구 1 [최상단 줄글 요약 카드 (`lead-quote-card`)] (필수 1개, 도입부 `<p>` 문단보다 가장 먼저 최상단 배치)**:
   - 내부에는 `📌 핵심 요약` 제목이나 `<ul><li>기준선/주의점` 같은 개조식 불릿을 넣지 않고, 2~3문장의 정갈한 줄글(`<p>`)로만 작성한다:
   ```html
   <div class="lead-quote-card" style="background:#f8fafc; border-left:4px solid #0284c7; padding:18px 22px; margin-bottom:28px; border-radius:4px;">
     <p style="margin:0; color:#334155; line-height:1.75; font-size:0.95rem;">
       [핵심 질문에 대한 결론과 안전 관리 원칙을 2~3문장의 자연스러운 줄글로 요약]
     </p>
   </div>
   ```
2. **도구 2 [반응형 데이터 대조표 (`custom-data-table`)] (권장 1~2개)**:
   - 조건별 비교, 단계별 기준선, 통설 대조 등을 한눈에 비교할 때 사용한다.
3. **도구 3 [핵심 실천 팁 박스 (`tip-box`)] (실생활 행동 수칙 요약 시 선택)**:
   ```html
   <div class="tip-box" style="background:#f0fdf4; border-left:4px solid #16a34a; padding:16px 20px; margin:24px 0; border-radius:4px;">
     <h4 style="margin-top:0; color:#166534; font-size:0.98rem; margin-bottom:8px;">[실천 수칙 소제목]</h4>
     <ul style="margin:0; padding-left:20px; font-size:0.92rem; color:#14532d; line-height:1.75;">
       <li><b>[항목 1]</b>: [구체적 실천 방법]</li>
       <li><b>[항목 2]</b>: [구체적 실천 방법]</li>
       <li><b>[항목 3]</b>: [구체적 실천 방법]</li>
     </ul>
   </div>
   ```

---

## 5. `post_data.json` 스키마 및 이미지 6장 규격

- **카테고리(`category`)**: 반드시 `홈트레이닝`, `식단 & 영양`, `라이프 웰니스` 중 1개로 지정한다.
- **분량 규격**: 순수 텍스트 공백 제외 **3,500자 ~ 5,500자** (문단당 1~2문장, 한 문단 최대 220자 이내, `<p style="font-size:1.02rem; line-height:1.9; color:#334155; margin-bottom:22px;">` 표준 문단 스타일 적용).
- **이미지 6장 (`thumb.jpg`, `post01.jpg` ~ `post05.jpg`) 및 H2 직하단 고정 배치**:
  - 모든 본문 이미지(`post01.jpg` ~ `post05.jpg`)는 **각 `<h2>` 소제목 바로 아래 첫 줄**에 `<figure class="post-img-wrap post-photo-figure">` 형태로 배치한 뒤 본문 `<p>` 문단을 이어간다:
    ```html
    <h2>[섹션 소제목]</h2>
    <figure class="post-img-wrap post-photo-figure" style="margin:24px 0; text-align:center;">
      <img src="../images/posts/[슬러그]/post01.jpg" alt="[구체적 설명]" style="max-width:100%; height:auto; border-radius:8px;" loading="lazy">
      <figcaption style="font-size:0.83rem; color:#64748b; margin-top:8px;">[간결하고 직관적인 사진 캡션]</figcaption>
    </figure>
    ```
  - 이미지 생성 후 반드시 `python tools/optimize_images.py "[작업폴더]"`를 실행하여 **원본 백업(`_originals/`) + 16:9 자동 크롭 + 200KB 이하 압축 + `thumb.jpg`와 `post01~05.jpg` 간 `dHash` 시각적 중복 검사**를 완료한다.
- **하단 참고문헌 (`references`)**:
  - `리서치.md` 및 `evidence_manifest.json`에 등록된 공인 1차 출처만 수록하며, 다른 기발행 글의 참고문헌을 복사·붙여넣기하지 않는다.

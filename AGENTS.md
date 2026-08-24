# 차를 쓰다 (CHAGEUL) & 꿀단지 - 고품질 SEO 콘텐츠 작성 및 발행 영구 표준 가이드

이 문서는 새 대화(New Conversation)를 열거나 새로운 글을 작성/수정할 때 인공지능(AI)이 항상 100% 준수해야 하는 구글 상위 노출(SEO) 및 E-E-A-T 전문 편집 영구 표준입니다.

## 1. 구글 2026 핵심 SEO 글작성 3대 원칙 (Information Gain 극대화)
1. **제목 (Title / H1)**: 검색자가 실제로 검색창에 입력하는 핵심 키워드(실구매가, 유지비, 제원, 감가율, 보조금, 다이어트, 제철음식, 루틴 등)를 자연스럽고 매력적으로 배치.
2. **목차와 소제목 (H2, H3)**: 글 상단에 항상 모바일 원터치 최적화 `목차 (Table of Contents)`를 배치하여 구글 로봇과 독자가 한눈에 구조를 파악할 수 있도록 구성 (이모지 제외, 번호 칼각 정렬).
3. **독보적인 본문 데이터 (2,500자+ E-E-A-T & 비교 분석표 & FAQ 5선)**:
   - 단순 요약을 지양하고 실제 수치, 과학적 기전, 5년 유지비, 트림 가성비 등 독보적 정보 제공.
   - 글마다 **비교 분석표 1개**, **실천 체크리스트 카드 1개**, **구글 전용 FAQ 5선 + Schema JSON-LD (`Article`, `FAQPage`)** 필수 포함.
4. **순수 정보성 원칙 (애드센스 심사 최적화)**: 애드센스 승인 전에는 쿠팡 파트너스, 네이버 쇼핑커넥트 등 외부 상업 링크를 일체 배제하고 순수 고품질 전문 지식(E-E-A-T)으로만 구성.

## 2. 모바일 반응형 표 (Table) 작성 영구 표준 규격
- **표 래퍼 마크업**: 모든 표는 반드시 아래 표준 클래스 구조로 작성하여 모바일에서 글자가 1글자씩 세로로 찌그러지지 않도록 보장함.
  ```html
  <div class="custom-data-table-wrap">
      <table class="custom-data-table">
          <thead>
              <tr><th>구분</th><th>항목1</th><th>항목2</th><th>비고</th></tr>
          </thead>
          <tbody>
              <tr><td>...</td><td>...</td><td>...</td><td>...</td></tr>
          </tbody>
      </table>
  </div>
  ```
- **터치 가로 스크롤 (Horizontal Scroll)**: 모바일 좁은 화면에서도 표의 각 열 너비가 온전하게 유지되며, 독자가 좌우로 자연스럽게 스크롤하여 쾌적하게 읽을 수 있도록 구성 (`min-width: 540px; white-space: nowrap;`).
- **군더더기 배제**: 표 상단에 불필요한 '좌우로 스크롤' 안내 문구는 넣지 않고 깔끔한 표 본문만 노출.

## 3. 핵심 요약 및 인포그래픽 카드 (Info Card) 표준 규격
- 단순 줄글 불릿(`•`) 및 어수선한 이모지 나열을 엄격히 금지하고, 네이버 매거진 / 토스 스타일의 **구조화된 뱃지 인포그래픽 카드**로 작성함.
  ```html
  <div class="info-section-card">
      <div class="info-card-title">가이드 타이틀 (이모지 제외)</div>
      <div class="info-step-list">
          <div class="info-step-item">
              <span class="info-badge blue">단계/주제 뱃지</span>
              <div class="info-step-desc"><strong>핵심 요약:</strong> 상세 설명 내용...</div>
          </div>
      </div>
  </div>
  ```

## 4. 메인 화면 최신순 자동 최상단 배치 및 단일 최신 뱃지 승계 원칙
1. **PC 데스크톱 그리드 최상단 삽입**: 새 글이 작성되면 `index.html`의 PC 3열 그리드(`clean-grid`)의 **맨 첫 번째(1번 자리)**에 최신 글 카드를 최우선 배치함.
2. **모바일 피드 스트림 최상단 삽입**: 모바일 메인 피드(`tistory-feed-list`)에서도 **맨 첫 번째(Card 1)** 자리에 최신 글을 최우선 배치함.
3. **단일 최신 뱃지 승계 & 이전 뱃지 자동 제거 (Single Latest Badge Rule)**:
   - 오직 **새로 발행된 맨 첫 번째(1번) 최신 글에만** `(최신)` 및 `NEW` 뱃지를 부여함.
   - 새 글이 추가되면, 2번 이하로 밀려난 **이전 글들에 달려있던 기존 `(최신)` / `NEW` 뱃지는 100% 자동으로 제거**하여 날짜만 표기(`YYYY.MM.DD`)되도록 정돈함 (뱃지 중복 누적 원천 차단).
4. **메인 썸네일 경로 동기화**: `images/posts/.../thumb.jpg?v=...` 로컬 고화질 화보와 100% 자동 연동.

## 5. 이미지 스타일 및 썸네일 표준 규격
1. **풍경 / 운동 가이드 / 음식 요리**: `16:9` 와이드 비율 (`object-fit: contain; height: auto;`).
2. **인물 / 스타 화보 / 전신 핏**: `1:1` 정사각 또는 세로 비율 (`aspect-ratio: unset; object-fit: contain;`)로 머리/발목 잘림을 100% 방지.
3. **고유 이미지 배치**: 한 글 안에서 동일한 이미지를 중복 사용하지 않고, 5장의 고유 화보를 1:1로 섹션마다 배치.

## 6. 웹 퍼블리싱 & 인코딩 영구 원칙
1. **인코딩 원칙**: 모든 HTML, CSS, JS, BAT 파일은 반드시 **UTF-8 with BOM** (`[System.Text.UTF8Encoding($true)]`)으로 저장하여 한글 깨짐 원천 차단.
2. **레이아웃 비례**: 본문 760px 내외 시원한 개방감, 우측 사이드바 240~300px 슬림 유지.
3. **공식 연락처**: 대표 이메일은 항상 `hmapt01@gmail.com`으로 일원화.

## 7. 공신력 있는 학술 데이터 및 공식 가이드라인 기반 표기 원칙 (E-E-A-T Reference Standard)
1. **허위/과장 감수 표기 원천 금지**: 실제 면허 보유자가 직접 서명하지 않은 '의학 감수', '전문의 감수' 등의 단정적 허위/과장 문구 사용을 100% 엄격히 금지함 (구글 품질 평가사 페널티 원천 차단).
2. **진실된 학술 데이터 기반 메타바 표기**: 상단 메타바에는 반드시 실제 참고한 공인 연구 분야를 명시함.
   - 운동/자세: `스포츠의학·운동역학 자료 기반`
   - 식단/영양: `임상영양학·보건학 연구 데이터 기반`
   - 수면/루틴: `수면의학·신경생리학 가이드라인 기반`
3. **본문 하단 공인 레퍼런스 박스 필수 탑재**:
   - 모든 글 본문 하단(연관 추천 칼럼 위)에 반드시 공신력 있는 공공 보건기관 및 학회(질병관리청, 식품의약품안전처, WHO, ACSM, 정형외과학회, 당뇨병학회 등)의 **공식 가이드라인 및 참고 문헌 박스**를 필수로 자동 삽입하여 구글 최고 등급 E-E-A-T 신뢰도를 획득함.

## 8. SNS 링크 공유(OpenGraph) 썸네일 자동 연동 영구 표준
1. **본문 첫 번째 대표 이미지 100% 연동**: 카카오톡, 네이버, 페이스북, 텔레그램 등에 글 링크를 공유했을 때 사이트 기본 로고가 아닌 **해당 글 본문의 첫 번째 대표 고화질 화보(`thumb.jpg`)가 대형 썸네일로 노출**되도록 `<head>` 안에 OpenGraph & Twitter Card 메타 태그를 필수 삽입함.
   ```html
   <meta property="og:type" content="article">
   <meta property="og:site_name" content="꿀단지">
   <meta property="og:title" content="...">
   <meta property="og:description" content="...">
   <meta property="og:image" content="https://honeyjar.co.kr/images/posts/[카테고리]/thumb.jpg">
   <meta property="og:image:width" content="1200">
   <meta property="og:image:height" content="630">
   <meta property="og:url" content="https://honeyjar.co.kr/posts/....html">
   <meta name="twitter:card" content="summary_large_image">
   <meta name="twitter:image" content="https://honeyjar.co.kr/images/posts/[카테고리]/thumb.jpg">
   ```
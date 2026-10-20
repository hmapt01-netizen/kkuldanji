# 🍯 꿀단지 (KKULDANJI) - 고품질 SEO 콘텐츠 작성 및 발행 영구 마스터 표준

본 문서는 꿀단지 프로젝트의 단일 진실 공급원(Single Source of Truth) 핵심 헌법이다. 세부 플랫폼별 작성·기획 명세는 각 단계의 전용 스킬(`skills/`)을 필요할 때만 온디맨드로 호출하여 컨텍스트 효율과 지시 이행률을 극대화한다.

---

## ⚡ [마스터 핵심 0] 초고속 처리 및 무결성 유지 프로토콜 (Fast Pinpoint Protocol)

1. **[정적 예시문 100% 영구 배제 원칙 (Zero-Example Formula-Only Rule)]**:
   - 규칙 문서 및 가디언 도구 내에 특정 성분명, 특정 식품명, 특정 질환명, 특정 약물명 등 고정된 정적 예시 단어나 괄호 예시를 일체 기재하지 않고 순수 추상 공식과 구조 변수로만 실행한다.
2. **[1초 핀포인트 교정 원칙 (Pinpoint Edit Only)]**:
   - 글 본문이나 리서치 파일의 특정 문장·단어·수치를 수정할 때 파일 전체를 다시 덮어쓰는 행위(`write_to_file` 전체 재작성)를 금지하며, 반드시 `replace_file_content` 도구로 해당 문단만 1초 만에 핀포인트 교체한다.
   - 기존 글을 전면 재설계할 때만 [마스터 핵심 8]의 백지 스토리텔링 재구조화 및 역방향 팩트 동기화 루프를 적용한다.
3. **[외부 금칙어 검사기 가짜 양성(False Positive) 즉시 무시 원칙]**:
   - 사용자가 외부 금칙어 검사기 결과를 전달했을 때, 실제 원고 본문에 존재하는 단어는 즉시 동의어로 치환한다.
   - 실제 원고 본문에 단 1회도 존재하지 않는 단어(외부 검사기의 형태소 오작동·가짜 양성)는 웹 검색이나 원인 분석으로 시간을 낭비하지 않고 즉시 무시한다.
4. **[수정 보고 3줄 압축 및 불필요한 린터 반복 실행 금지]**:
   - 수정 완료 보고는 **[변경 전 ➔ 변경 후]** 핵심만 3줄 이내로 간결하게 브리핑한다.
   - 규칙 감사 스크립트(`tools/lint_rules_zero_example.py`, `tools/audit_rule_integrity.py`)는 지침(`AGENTS.md`, `GEMINI.md`, `skills/`)이나 가디언 코드를 수정했을 때만 실행하며, 일반 글쓰기 단계마다 중복 실행하지 않는다.

---

## 🎯 [마스터 핵심 1] 2단계 리서치 분리 및 단계별 HARD STOP 워크플로우

모든 신규 글 작성은 **2단계 리서치 분리(Step 0-A 사전 팩트 ➔ Step 0-B 심층 리서치)** 구조로 실행하며, 각 승인 게이트(HARD STOP)에서 사용자의 명시적 결재 없이 다음 단계로 넘어가는 것을 엄격히 금지한다.

| 단계 | 명칭 및 핵심 산출물 | 호출 스킬 및 필수 검증 명령 |
| :--- | :--- | :--- |
| **주제 선정** | 하이브리드 주제 발굴 (3대 카테고리 후보 3선 & 잠정 추천 1개) ➔ **HARD STOP** | `skills/topic-opportunity/SKILL.md`<br>`python tools/view_top_keywords.py --cat all`<br>`python tools/check_topic_duplication.py "후보1" "후보2"` |
| **Step 0-A** | **1차 광범위 사전 팩트 탐색 (Pre-Fact & Baseline Check)**<br>공인 1차 기준선(Baseline) + 주의사항(Delta) + `official_source_raw.txt` 원문 덤프 + `리서치.md` 1차 작성 (제목 확정 전 세부 FAQ 조기 작성 금지) | `read_url_content`로 공인 1차 원문 열람 후 `official_source_raw.txt`(200바이트 이상, URL·열람일 포함) 저장<br>`python tools/step_guard.py 1` |
| **Step 1** | **네이버 제목 10선 보고 및 승인 ([트랙 A 홈판형 5선] + [트랙 B 하이브리드형 5선])** ➔ **HARD STOP 1** | `skills/kkuldanji-naver-title/SKILL.md`<br>`titles.json` 저장 후 `python tools/validate_titles.py` |
| **Step 2/3** | **구글 SEO 듀얼 트랙 제목 10선 보고 및 최종 제목 확정 ([트랙 A 검색·진료 가이드형 5선] + [트랙 B 디스커버·착각 반전형 5선], `titles.json` 잠금)** ➔ **HARD STOP 2/3** | `skills/kkuldanji-google-article/SKILL.md`<br>`titles.json`에 `selected_naver`, `selected_google` 확정 저장 후 `python tools/validate_titles.py google` |
| **Step 0-B** | **2차 제목 맞춤형 심층 리서치 (Target-Focused Deep Dive Research)**<br>확정된 제목이 약속한 세부 기전·수치·통설 대조·맞춤 FAQ 2~3선을 `리서치.md` 및 `evidence_manifest.json`에 완결 보강 | `python tools/step_guard.py 4` |
| **Step 4** | **구글 본진(`post_data.json`) & 네이버(`네이버.html`) 독립 집필 + 이미지 6장 생성/최적화 + 로컬 빌드 및 프리뷰 보고** ➔ **HARD STOP 4 (`"발행해줘"` 대기)** | `skills/kkuldanji-google-article/SKILL.md` & `skills/naver-honeyjar/SKILL.md`<br>`python tools/optimize_images.py "[작업폴더]"`<br>`python tools/evidence_guard.py "[작업폴더]"`<br>`python tools/audit_duplicates.py`<br>`python tools/add_post.py "[작업폴더]/post_data.json"`<br>`python tools/audit_site.py --local` |
| **Step 5/6** | **실서버 배포 (`git push`) 및 라이브 검증** (사용자가 `"발행해줘"` 승인 시에만 실행) | `git add . && git commit && git push`<br>`python tools/audit_site.py --live` |
| **클립/쇼츠** | **네이버 클립 & 쇼츠 30초 세로형(`1080×1920`) 영상 제작** (Step S-1 30초 대본 제시 ➔ Step S-2 레퍼런스 분석·음원 요청 ➔ Step S-3 단어 싱크·렌더링) | `skills/kkuldanji-shorts-clip/SKILL.md` |

---

## 🧭 [마스터 핵심 2] 하이브리드 주제 선정 및 스윗스팟 연관어 직결 원칙

주제 발굴·추천 시 반드시 `skills/topic-opportunity/SKILL.md`를 먼저 읽고 실행한다.

1. **[2대 모드 분리 실행]**:
   - **모드 A (초고속 주제 추천)**: 일반 주제 추천 요청 시 `tools/topic_opportunity.py`, `tools/datalab_popular.py`, `tools/view_top_keywords.py`, `tools/check_topic_duplication.py`를 사용하여 **3대 공식 카테고리(`홈트레이닝` 1개, `식단 & 영양` 1개, `라이프 웰니스` 1개) 후보 3선과 오늘의 잠정 추천 1개**를 즉시 브리핑한다.
   - **모드 B (최신 보건·식약 동향 브리핑)**: 사용자가 최신 뉴스·이슈를 명시적으로 요청할 때만 최근 7일 이내 공인 기관 발표 동향을 검색하여 브리핑한다.
2. **[4대 필수 검증 데이터]**:
   - **스트림 A (네이버 쇼핑 커넥트 수익화 태깅)** + **스트림 B (당월 계절/증상/해부학 질문형 검색어)** 결합.
   - **최근 14일 이내 발행 소재 쿨타임 차단**: 최근 14일 내 발행된 기존 글과 핵심 소재가 겹치는 후보는 원천 배제한다.
   - **기존 글 시너지(`synergy_posts`) & 핵심 수치(`desc`) 메모**: 내부 링크(`inline-pill-link`)로 연결할 기존 글의 `slug`, `title`, `desc`(핵심 수치 요약)를 `리서치.md`에 기록하여 글 간 수치 충돌을 차단한다.
   - **네이버 검색광고 API 스윗스팟(월 300~15,000회) 세부 연관검색어 TOP 5 추출**: 후보별 실측 세부 연관검색어 TOP 5와 자동완성 5개를 추출하여 Step 1 네이버 제목과 본문 H2 소제목에 1:1로 반영한다.
3. **[구형 가짜 SERP 점수·배지 영구 폐기]**:
   - 구형 정적 경쟁도 배지(`🔴/🟡/🟢/💎`), 단어 가점, 블로그 0건=블루오션 단정, `last_serp_audit.json` 강제 락은 영구 폐기한다.

---

## 🏛️ [마스터 핵심 3] 한국 공인 1차 기관 최우선 탐색 및 원문 덤프 검증 (`official_source_raw.txt`)

1. **[한국 7대 공인 1차 기관 최우선 탐색 (Korea-First Official Grounding)]**:
   - 리서치 시 국내 독자 기준에 맞는 **한국 7대 공인 1차 기관**을 1순위로 탐색하여 기준선(Baseline)을 확정한다:
     1) 질병관리청 국가건강정보포털 (`health.kdca.go.kr`, `kdca.go.kr`)
     2) 식품의약품안전처 & 식품안전나라 (`mfds.go.kr`, `foodsafetykorea.go.kr`)
     3) 농촌진흥청 국가표준식품성분표 (`koreanfood.rda.go.kr`, `rda.go.kr`)
     4) 보건복지부 (`mohw.go.kr`)
     5) 국민건강보험공단 & 건강보험심사평가원 (`nhis.or.kr`, `hira.or.kr`)
     6) 대한의학회 산하 전문 의학회 공식 진료지침
     7) 국립암센터 (`ncc.re.kr`)
   - 해외 학술 기관(NIH, PubMed, WHO 등)은 국내 지침이 없는 세포·분자 기전이나 국제 기준 비교 시 보조 근거로 활용한다. 일반 블로그·카페·단순 언론 요약본 인용은 100% 금지한다.
2. **[1차 출처 원문 덤프 (`official_source_raw.txt`) 및 실시간 DNS 검증 의무]**:
   - `read_url_content`(봇 차단·동적 렌더링 사이트는 로컬 전용 크롬 CDP `python tools/fetch_via_cdp.py "<URL>"`)로 열람한 공인 1차 출처의 실제 원문 텍스트(최소 200바이트 이상)와 공식 직행 URL(`https://...`), 열람일을 작업 폴더 내 `official_source_raw.txt`에 의무 저장한다.
   - `리서치.md`와 `evidence_manifest.json`에는 해당 원문에서 발췌한 실제 인용문(`evidence_quote`)과 고유 학술/법령 식별자(PMID/PMC/DOI/고시번호 등)를 1:1로 매핑한다.
3. **[본문 작성 중 실시간 추가 리서치 동기화 (`supplement_research.py`)]**:
   - 본문 작성 중 리서치에 없는 새로운 수치·기전·주의사항이 필요하면 즉시 작성을 멈추고 웹 검색으로 공인 근거를 확인한 뒤, `python tools/supplement_research.py add ...`로 `리서치.md`와 `evidence_manifest.json`에 먼저 등록하고 서술한다.

---

## 🛡️ [마스터 핵심 4] 플랫폼 금칙어 분리 (Platform Decontamination) 및 과장 표현 차단

1. **[네이버 전용 감점 단어 17종 — 네이버(`네이버.html`, 네이버 제목)에만 적용]**:
   - `최고`, `완벽`, `추천`, `가격`, `구매`, `할인`, `무료`, `이벤트`, `1위`, `최저가`, `총정리`, `진단`, `치료`, `처방`, `약국`, `병원`, `의사`
   - 🚨 **구글 오염 금지**: 위 단어들은 네이버 스마트에디터 전용 제약이므로, **구글 제목(`google_10`)과 구글 본문(`post_data.json`)에서는 전면 허용**한다. 구글에서는 독자가 실제로 검색하는 `진단 기준`, `치료 가이드`, `병원 진료 시기`, `추천 루틴` 등의 직관적 키워드를 적극 사용한다.
2. **[전 플랫폼 공통 절대 금칙어 (구글 + 네이버 모두 차단)]**:
   - **만병통치·허위 과장 금칙어**: `완치`, `100% 치료`, `암세포 박멸`, `기적의 특효약`, `즉각 완치`, `독소 배출`, `만병통치`, `무조건 해결`
   - **번역투·상투적 클리셰**: `실익`, `셈법`, `맹점`, `완벽 정리`, `핵심만 짚어드립니다`, `알아보겠습니다`, `살펴보겠습니다`
   - **배타적 최상급 검증**: `유일`, `최초` 등의 단어는 `리서치.md` 원문에 해당 단어가 실존할 때만 사용을 허용한다 (`audit_duplicates.py` 자동 검증).

---

## ✍️ [마스터 핵심 5] 출처 2대 영역 분리 및 독자 중심 3단계 실천 서사

1. **[출처 표기 2대 영역 분리 (Two-Zone Attribution)]**:
   - **영역 1 (상단 요약 카드 `lead-quote-card` & 하단 `참고문헌`)**: 공인 1차 기관 정식 명칭, 가이드라인명, 학술 식별자(PMID/DOI 등)를 투명하게 명시한다.
   - **영역 2 (본문 서술문, 소제목 H2/H3, 네이버 본문)**: 본문 문장에서 국내외 기관명이나 학술 저자 영문 성씨를 주어나 수식어로 직접 나열하는 관공서 팸플릿 어투(Institutional Name-Dropping)를 100% 금지한다.
2. **[독자 중심 3단계 실천 서사 구조 & 정통 경어체 통일]**:
   - **[1단계: 왜 불편할 수 있는지(원인·기전)] ➔ [2단계: 무엇을 바꿔볼지(기준선과 실천 조절법·한계)] ➔ [3단계: 언제 진료가 필요한지(위험 경고 신호)]** 순서로 서술한다.
   - 모든 문장은 다정하고 신뢰감 있는 정통 경어체(`~습니다`, `~합니다`, `~세요`)로 통일하며, 공인 출처 명시 범위(Grounding Scope Lock)를 벗어난 상상 서술이나 임의의 처방 수치 조작(Zero Pseudo-Prescription)을 100% 금지한다.
3. **[구글 vs 네이버 100% 독립 집필 (4-gram 중복률 5% 미만)]**:
   - 구글(`post_data.json`)과 네이버(`네이버.html`)는 동일한 `리서치.md` 팩트에 기반하되, 문장 구조와 서사 호흡을 100% 독립적으로 작성한다 (`audit_duplicates.py`로 15자 이상 동일 문장 0건 및 4-gram 유사도 5% 미만 검증).
   - 네이버 블로그 본문은 **옵션 A (꿀단지 고유 중앙 정렬 + 20~35자 호흡 줄바꿈 + 8종 꿀벌 시그니처 마스코트 스티커 `180px` 임베드 + 외부 링크 0건)** 규격을 준수하며 `python tools/validate_naver_layout.py`로 자동 검수한다.

---

## 🖼️ [마스터 핵심 6] 화보 이미지 6장 시각적 일관성 앵커 및 `optimize_images.py` 자동 최적화

단일 포스팅 내 AI 화보의 시각적 일관성과 몰입도를 위해 아래 5대 시각적 앵커(Visual Continuity Anchor) 공식을 의무 준수한다:

1. **[동일 주인공(Character Anchor) 100% 고정 및 참조 상속 원칙]**:
   - 한 편의 글에 인물이 등장할 때는 글 전체를 관통하는 **단 1명의 주인공 페르소나**(나이, 성별, 얼굴 특징, 헤어스타일, 체형, 의상 톤)를 확정하고 동일한 시각적 정체성을 유지한다.
   - 후속 인물 화보 생성 시 선행 생성된 주인공 기준 앵커 이미지 경로를 참조 이미지(`ImagePaths`)로 전달하고, 프롬프트 서두에 `The exact same Korean person from the reference image with identical facial features...` 앵커 서술을 고정 삽입하여 컷마다 다른 인물이 나오는 현상을 차단한다.
2. **[한국 아파트 실내 배경(Korean Apartment Living Anchor) 필수 탑재]**:
   - 이국적 서구 주택이나 이질적인 스튜디오를 배제하고, 친숙한 **대한민국 아파트 실내 생활 공간**(거실, 침실, 주방, 원목 다이닝 식탁, 베란다 채광 환경)을 기본 배경으로 연출한다.
3. **[인물 3컷 : 정물·도구 2컷 (3:2 황금 비율) 교차 스토리텔링]**:
   - 본문 5대 화보(`post01.jpg` ~ `post05.jpg`)가 모두 단조로운 인물 샷으로 채워지지 않도록, **[1. 일상 속 증상·고민 인물 샷] ➔ [2. 핵심 측정기·도구·식단 클로즈업 정물 샷] ➔ [3. 올바른 실천·대처 동작 인물 샷] ➔ [4. 생활 관리 용품·비교 정물 샷] ➔ [5. 회복·진료 상담 주인공 샷]**처럼 **동일 주인공 3컷과 정물·도구 2컷을 3:2 비율로 유기적으로 교차 배치**한다.
4. **[대표 썸네일(`thumb.jpg`)과 본문 5대 화보(`post01~05.jpg`) 분리 독립]**:
   - 글 전체 주제를 직관적으로 상징하는 대표 히어로 썸네일(`thumb.jpg`) 1장과 5개 H2 소제목 서사에 1:1 대응하는 본문 화보(`post01.jpg` ~ `post05.jpg`) 5장, **총 6장의 100% 서로 다른 고유 화보**를 생성하며, 이미지 내 깨진 글자·숫자·워터마크 및 기괴한 신체 묘사를 엄격히 배제한다.
5. **[단일 CLI 최적화 및 `dHash` 중복 검증 필수]**:
   - 이미지 생성 직후 `python tools/optimize_images.py "[작업폴더]"`를 실행하여 **`_originals/` 원본 백업 + 16:9 비율 자동 크롭 + 200KB 이하 압축 + `thumb.jpg`와 `post01~05.jpg` 간 지각 해시(`dHash`) 시각적 중복 차단**을 한 번에 완료한다.

---

## 🖥️ [마스터 핵심 7] Step 4 완료 직후 로컬 빌드 및 클릭형 프리뷰 게이트

Step 4에서 원고(`post_data.json`, `네이버.html`)와 이미지 6장 작성이 끝나면, 사용자에게 보고하기 전에 반드시 아래 순서로 로컬 컴파일 및 무결성 감사를 먼저 완료한다:

1. `python tools/evidence_guard.py "[작업폴더]"` (팩트·수치·식별자·DNS 검증)
2. `python tools/audit_duplicates.py` (문장/4-gram 중복, 이미지 `dHash`, 네이버 레이아웃 및 꿀벌 스티커 8종 통합 검증)
3. `python tools/add_post.py "[작업폴더]/post_data.json"` (목차 `.toc-box` 자동 삽입, 표 스타일링, `inline-pill-link` 변환, `posts_db.json`·RSS·사이트맵 자동 갱신)
4. `python tools/audit_site.py --local` (로컬 HTML/링크/레지스트리/피드 무결성 검수)
5. **로컬 프리뷰 링크 3종 보고 후 HARD STOP 4**:
   - ① 구글 개별 포스트 HTML (`file:///d:/작업/꿀단지/kkuldanji_web/posts/[슬러그].html`)
   - ② 구글 메인 인덱스 (`file:///d:/작업/꿀단지/kkuldanji_web/index.html`)
   - ③ 네이버 블로그 프리뷰 (`file:///d:/작업/꿀단지/[작업폴더]/네이버.html`)
   - 위 3개의 클릭 가능한 링크와 `#해시태그` 세트를 제시하고 사용자의 **"발행해줘"** 승인을 대기한다.

---

## 🔄 [마스터 핵심 8] 기존 글 수정 시 역방향·전방위 팩트 동기화 루프

- **핀포인트 수정**: 단순 오탈자·단어·문장 다듬기는 [마스터 핵심 0]에 따라 `replace_file_content`로 즉시 수정한다.
- **팩트·수치 변경 또는 전면 재작성 시 (Bidirectional Fact-Sync Lock)**:
  1) 원천 장부인 `리서치.md`와 `evidence_manifest.json`의 공인 근거를 최우선으로 업데이트하고,
  2) 구글 본진(`post_data.json` ➔ `add_post.py` 재빌드)과 네이버 원고(`네이버.html`) 양쪽 채널을 동시에 동기화하여 채널 간 팩트 불일치를 원천 차단한다.

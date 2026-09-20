# 🍯 혀니의 꿀단지 (KKULDANJI) - 공식 개발 & 운영 불변 규칙서

> **[중요]** 본 프로젝트는 `https://honeyjar.co.kr` 로 서비스되는 고품질 웰니스 & 라이프 매거진 블로그입니다.
> 모든 대화 및 세션에서 아래의 **불변 규칙**을 100% 준수해야 합니다.

---

## 1. 📂 파일 구조 및 새 글 발행 규칙 (절대 원칙)

### 📌 새 글(칼럼)을 발행할 때 수정되는 파일은 정확히 3개입니다:
1. **`kkuldanji_web/posts/[영문슬러그].html` [새 파일 생성]**
   - 모든 글 본문 파일은 오직 `kkuldanji_web/posts/` 폴더 안에만 생성합니다.
   - 필수 포함 항목:
     - 상단 공통 헤더 (`images/logo.png?v=11.0`, 높이 38px)
     - 나눔스퀘어라운드 폰트 + `css/style.css`
     - 사이드바 (에디터 혀니 프로필 뱃지 + 인기 꿀팁 TOP 5 + 건강 계산기 위젯)
     - 하단 스마트 댓글 시스템 (`<div id="commentSectionWrapper"></div>` + `<script src="../js/comments.js"></script>`)
     - 하단 실시간 통계 트래커 (`<script src="../js/analytics.js"></script>`)
2. **`kkuldanji_web/index.html` [메인 홈 카드 연동]**
   - 메인 화면의 최신 글 목록 맨 위에 새 글의 `<article class="clean-card article-item" data-category="...">` 카드를 추가합니다.
   - 10개 초과 시 페이지네이션 2페이지로 자동 분할.
3. **`kkuldanji_web/admin.html` [관리자 콘솔 연동]**
   - 관리자 글 목록 테이블 `initialPostsData` 배열에 새 글 데이터 객체를 추가합니다.

---

## 2. 🎨 디자인 & 브랜딩 불변 규격 (절대 임의 변경 금지)

* **브랜드명**: 혀니의 꿀단지 (KKULDANJI Life & Wellness)
* **공식 로고**: `images/logo.png` (여백 0% 크롭, 노란 꿀단지 그래픽, 아이콘 높이 `38px` 고정)
* **메인 폰트**: 네이버 `NanumSquareRound` (나눔스퀘어 라운드 - 상업용 무료 OFL)
* **관리자 비밀번호**: **`8809`**
* **에디터 프로필**: 에디터 혀니 (`✓ 웰니스 칼럼니스트`)
* **메뉴 구성**: `홈(전체)` | `식단·영양` | `제철 음식` | `홈트레이닝` | `라이프 웰니스` | `소개` | `문의하기`

---

## 3. 🛡️ 시스템 기능 보존 규칙

* **댓글 시스템**: `js/comments.js` (닉네임 + 4자리 비번 + 공감 하트 + admin.html 원클릭 삭제)
* **방문자 & 체류시간 분석**: `js/analytics.js` (조회수 + 초단위 체류시간 + 스크롤 완독률 측정)
* **건강 계산기**: BMR(기초대사량), TDEE, 일일 권장 수분량, 단백질 실시간 계산기

---

## 4. 🌐 배포 방식

* 사용자가 `kkuldanji_web` 폴더를 Cloudflare Worker (`bitter-butterfly-a211`)에 드래그 & 드롭하여 배포합니다.
* 사용자는 파워셸(PowerShell) 명령어를 사용하지 않으며, 직관적인 UI 가이드로 소통합니다.

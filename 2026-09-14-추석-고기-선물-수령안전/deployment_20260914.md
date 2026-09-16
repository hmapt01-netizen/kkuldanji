# 2026-09-14 배포 및 실서버 확인

- 사용자 발행 승인: 현재 대화의 `배포해줘`.
- 배포 커밋: `e16d3d6`, 이전 운영 커밋: `de42656`. origin/main push 성공.
- Cloudflare Pages 기존 무료 프로젝트에 반영. 요금제·환경변수 변경 없음.
- 범위: 고기 신규 글, 비염 글 보완, 28개 글 목록/사이트맵/피드, 카테고리 페이지 나눔 수정과 Python/Node 검사 장치.
- AI 운영 규칙과 기타 연구 파일은 이번 커밋에서 제외. 네이버 원고는 로컬 수정본이며 네이버 사이트에 발행하지 않음.

## 검증 결과

- 기존 deploy_site.py --check-only 통과. 전체 작업 폴더를 git add . 하는 배포 동작 대신 검수 완료한 파일 48개만 명시적으로 커밋·push.
- 로컬 HTML 39개, 내부 링크 1,035개, 에셋 참조 689개 검사. 필수 파일·링크·에셋·HTML 구조·파비콘·인코딩·페이지 나눔 오류 각각 0건.
- audit_site.py --live: 공개 주소 40/40 HTTP 200.
- 라이브 홈 카드, 고기 글, 비염 글의 본문 텍스트·제목·이미지 경로가 로컬 배포본과 일치. Cloudflare 이메일 보호로 전체 HTML 바이트는 달라 별도 DOM 내용을 비교함. CSS·사이트맵 파일은 줄바꿈 정규화 후 일치.
- 브라우저 PC: 홈 3열·6개. 식단·영양 6→10, 라이프 웰니스 6→12. 모두 마지막 항목까지 펼치면 더보기 숨김. 카테고리 변경 시 6개로 초기화. 홈트레이닝 6개·더보기 숨김.
- 두 글의 실제 제목·소제목·표, 스크롤 후 본문 이미지 전체 로드 확인. 고기 촬영 이미지의 휴대전화 화면도 실제 표시 확인. 비염 글 가로 넘침 없음.
- 모바일 페이지 나눔은 기존 자동 검사 통과이며 이번 실브라우저 검수는 PC. 댓글 작성/삭제와 모든 외부 참고문헌 URL은 이번 배포에서 재시험하지 않음.
- IndexNow: 두 글 URL 제출, HTTP 200 접수. 검색 색인 완료를 뜻하지 않음.
- Google: 새 사이트맵 반영. Indexing API는 일반 블로그 글 지원 대상이 아니어서 미요청. 공식 문서: https://developers.google.com/search/apis/indexing-api/v3/using-api (2026-07-16 갱신, 이번 배포 검토에서 확인).

## 기록 시점

이 보고서와 workflow validation/publish_approval/published 영수증은 실서버 검증 후 정리했다. 사용자 승인 자체는 배포 전에 받았으며, 사전 로컬 검수도 push 전에 통과했다. 실브라우저 검수는 배포 후 수행했다.

## 공개 URL

- https://honeyjar.co.kr/posts/chuseok-meat-delivery-thawing-safety.html
- https://honeyjar.co.kr/posts/nasal-spray-rebound-rhinitis-5day-rule.html

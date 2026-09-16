# 카테고리 더보기 수정 · 2026-09-14

원인: 카테고리 클릭 시 pcShown/mobileShown을 999로 변경하여 전체 노출. CSS display:inline-flex !important가 버튼 숨김을 방해.

변경: 탭 선택마다 PC6개·모바일4개로 초기화. 기존 PC6개씩/모바일4개씩 더보기 유지. CSS display 충돌 제거 및 홈페이지 CSS 버전 갱신.

검증: 운영 브라우저에서 수정 전 식단9개 전체 노출 재현. 기존 코드 회귀 테스트 실패 후 수정 템플릿·생성 index·운영용 패치본 JavaScript DOM 모의 테스트 통과. 전체/식단/홈트/라이프 탭, 더보기·마지막 버튼 숨김·재선택·PC/모바일 간 상태 초기화·직접 카테고리URL·숨김글·검색 검사. 수정 후 브라우저 렌더링은 미확인.

로컬 빌드: HTML39개/내부링크1036개/에셋689개, 필수파일·링크·에셋·HTML·파비콘·인코딩 오류 각각0. 기존 글28편 재생성0편. DB와 AGENTS/GEMINI 해시 보존.

배포 미실행. pagination-only.patch는 HEAD 기준 3파일(홈페이지·홈 템플릿·CSS)만 바꾸고 기존 운영 글27편을 유지. 미발행 고기 글과 원고·규칙 변경을 제외했다. 현재 전체 작업트리를 그대로 배포하면 미발행 글이 포함되므로 반드시 메뉴 수정 범위만 적용해야 한다. 배포 후 운영 브라우저에서 6개씩 노출/추가/마지막 버튼 숨김을 확인해야 한다.

## 필수 회귀 검사 추가

`tools/site_pagination_guard.py`가 Node의 `tools/home_pagination.test.mjs`로 실제 홈페이지 스크립트를 실행한다. 새 글 등록 전(add_post), 빌드의 파일 쓰기 전(build_site), 생성물 검수(audit_site)에 연결했다. 기존 deploy_site는 audit_site 실패 시 Git/업로드 전에 중단한다. 검사 파일 또는 Node 누락도 중단한다.

PC 3열·최초 6개·추가 6개·탭 전환 초기화·소진 후 버튼 숨김, 모바일 기존 4개, 직접 카테고리 URL·숨김글·검색을 검사한다. 홈트 글 수 0/1/5/6/7/13개 경계를 독립 데이터로 반복한다. 실제 브라우저 레이아웃 전체를 보장하는 검사는 아니다.

검증: test_site*.py 21개 통과(999개 노출, 추가 개수 변경, 초기화 제거, CSS 충돌, 열 수 변경 등 의도적 오류 차단 포함). 실제 build_site.py 및 deploy_site.py --check-only 통과. DB·AGENTS.md·GEMINI.md 해시 동일. 운영 배포 미실행.

주의: 기존 pagination-only.patch는 UI 3파일만 포함한다. 이번 필수 검사 추가분은 tools/add_post.py, tools/build_site.py, tools/audit_site.py 및 신규 tools/site_pagination_guard.py, tools/home_pagination.test.mjs, tools/test_site_pagination_guard.py이다. 운영 반영 시 이 파일도 함께 포함해야 한다.

# Codex 본문·이미지 순서 교정 검증

- 사용자 요청: 본문 초안을 먼저 작성하고 본문에 맞춰 이미지 계획·승인·제작을 진행. Antigravity는 수정하지 않음.
- 수정 범위: codex_tools의 WORKFLOW.md, workflow_guard.py, register_post.py, freshness_guard.py 및 회귀 테스트.
- 새 단계: 제목 선택 완료 → draft → image_plan → image_approval → assembly → validation → publish_approval → published.
- 등록 진입점은 assembly 완료 후 validation에서만 공용 add_post를 호출. 기존 이미지·본문·빌드 검사는 유지.
- 두 채널 초안 파일과 확정 제목을 확인하고 해시로 보존. 초안 변경은 draft로, 계획 내용 변경은 image_plan으로 복귀. 실제 승인 여부 플래그만 변경하는 것은 계획 내용 변경과 구별.
- Python unittest discover: 53개 통과. 이미지 승인 전/이미지 배치 전 등록 차단, 본문 없이 계획 기록 차단, 초안·계획 변경 시 복귀, 기존 기록 이전·제목 보존 포함.
- reuse_baseline.json의 공용 원본 43개 SHA-256 대조: 변경 0개.
- 진행 중인 추석 고기 선물 작업: 기존 기록 전체를 codex_workflow.before_draft_first.json에 백업. 최초 5개 완료 기록과 두 제목 선택은 그대로 유지. 기존 이미지 계획 완료 기록만 superseded 이력으로 이동. 이미지 계획 파일은 미승인 참고안으로 보존.
- 이전 후 status: draft / continue. 실제 draft 진입 검사: freshness_review.json 누락으로 종료 코드 2. 최신 근거 검토가 완료됐다고 꾸미지 않았으며, 이 검토 후 본문 초안을 작성해야 함.
- 이번 검증은 절차와 회귀 테스트 범위. 실제 글 작성·이미지 생성·배포를 수행한 것은 아님. 본문 품질·그림과 설명의 의미상 일치는 별도 실제 대조 필요.

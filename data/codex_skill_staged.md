---
name: kkuldanji-codex
description: 꿀단지(honeyjar.co.kr) 프로젝트의 주제 조사, 네이버·구글 글쓰기와 수정, 이미지 계획, Python 등록·빌드·검수·발행을 기존 운영 규칙에 맞춰 수행한다. D:/작업/꿀단지의 콘텐츠 업무에 사용하며, 다른 블로그·차량 프로젝트에는 적용하지 않는다.
---

# 꿀단지 Codex 운영 지침

프로젝트는 `D:/작업/꿀단지`다. 기존 `AGENTS.md`, `GEMINI.md`, 네이버 스킬과 Python을 유지하면서 Codex에서 같은 업무 요구를 수행한다. 이 스킬은 기존 스크립트의 검사 범위를 확대하거나 오류를 고치지 않는다.

## 2026-09-14 Codex 전용 복귀·제목 길이 개정

꿀단지 신규 글 작업 시작 및 단계 전환 전에 [Codex 전용 진행 규칙](<D:/작업/꿀단지/codex_tools/WORKFLOW.md>)을 읽고 `codex_tools/workflow_guard.py`를 실행한다. 현재 사용자 지시에 따른 추가 검사이며 Antigravity/Gemini와 공용 Python 파일은 수정하지 않는다.
네이버·구글 제목은 공백·문장부호 포함 **40~60자**다. 복제본의 35자 상한·20자 권장 등 이전 길이 조건보다 이 지시가 우선한다.
사용자 질문에는 답하고 이미 승인된 작업을 계속한다. 제목을 제시하기 전에 선택 대기로 끝내지 않는다. 단계 누락·종료 검사 실패 시 첫 미완료 단계로 복귀하여 보완한다. 실제 사용자 선택·이미지·발행 승인은 자동 생성하지 않는다.
공략 검색 질문과 제목의 대상·상황을 대조하고 형식 검사 성공을 저지수 블로그 추천 근거로 대체하지 않는다. 의미 검토 기록과 프로그램 검사의 한계는 위 전용 규칙을 따른다.
## 사용자 승인 공통 개정 (2026-09-14)

주제·제목 선정 전 [블루오션 발굴 공통 기준](<D:/작업/꿀단지/BLUE_OCEAN_PROTOCOL.md>)을 반드시 읽는다.
사용자의 제1 목적은 블루오션 발굴이다. 수요 → 실제 경쟁 문서 → 답변의 빈틈을 우선 검증한다.
이 공통 개정은 복제된 topics/search/연관 상세 문서의 정적 배지·성과 보장·구형 도구 설명보다 우선한다.
기존 글쓰기 기능과 제목 선택·이미지 승인·등록·검수·발행 순서는 유지한다. Antigravity/Gemini도 동일 기준을 읽는다.

## 시작할 때

1. 사용자 요청이 주제 조사, 제목 제안, 신규 글, 기존 글 수정, 사이트 수정, 발행 중 무엇인지 먼저 구분한다. 현재 대화에 이미 주어진 제목 선택·이미지 승인·발행 지시는 유효한 범위에서 이어받는다.
2. [Codex 적용 기준](references/codex-policy.md)을 읽는다. 원문끼리의 충돌과 문서/코드 차이는 [충돌 처리](references/conflicts.md)의 해당 항목을 함께 읽는다.
3. 아래 표에서 현재 업무에 필요한 상세 원문을 **실제로 읽고** 작업한다. 이 진입 문서만 읽고 글을 쓰지 않는다. 각 상세 문서는 요약이 아니라 원래 규칙·조건·예시·코드 블록을 보존한 문서다.
4. 작업 폴더·현재 단계·대상 slug·네이버 패키지·사용자 확정 사항을 확인한다. 폴더의 수정 시각이나 캐시 존재만으로 현재 작업을 결정하지 않는다. 원본 규칙/코드가 갱신되었으면 관련 부분과 차이를 먼저 확인한다.

## 업무별 읽을 문서

| 업무 | 필수 상세 문서 |
|---|---|
| 신규 주제 추천·중복 확인 | [주제](references/topics.md), [리서치](references/research.md), [검색어·SERP](references/search.md), [진행 순서](references/workflow.md) |
| 네이버 제목 제안 | [진행 순서](references/workflow.md), [제목](references/titles.md), [검색어·SERP](references/search.md), [네이버](references/naver.md), [리서치](references/research.md) |
| 구글 제목 제안 | [진행 순서](references/workflow.md), [제목](references/titles.md), [검색어·SERP](references/search.md), [문체](references/voice.md), [리서치](references/research.md) |
| 이미지 계획·생성·최적화 | [진행 순서](references/workflow.md), [이미지](references/images.md), [플랫폼 분리](references/platforms.md) |
| 네이버 본문 작성 | [진행 순서](references/workflow.md), [네이버](references/naver.md), [플랫폼 분리](references/platforms.md), [문체](references/voice.md), [리서치](references/research.md), [검색어·SERP](references/search.md), [이미지](references/images.md) |
| 구글 본문 작성 | [진행 순서](references/workflow.md), [구글 형식](references/google.md), [플랫폼 분리](references/platforms.md), [문체](references/voice.md), [리서치](references/research.md), [검색어·SERP](references/search.md), [이미지](references/images.md), [사이트 보호](references/site.md) |
| 기존 글 수정 | [동시 수정](references/sync.md)과 위 표의 해당 채널 본문 문서. 양쪽 원고를 찾아 수정·검수한다. |
| Python 등록·빌드·검수 | [명령과 검사 한계](references/commands.md), [사이트 보호](references/site.md), [발행·보고](references/publishing.md), 대상 원고의 형식 문서 |
| 사이트 공통 UI·템플릿 수정 | [사이트 보호](references/site.md), [공통 원문](references/shared.md), [명령과 검사 한계](references/commands.md). 글 주제/제목 선정 절차는 적용하지 않는다. |
| 발행·배포·색인 확인 | [발행·보고](references/publishing.md), [명령과 검사 한계](references/commands.md), [사이트 보호](references/site.md), [플랫폼 분리](references/platforms.md) |

기존 원본의 상위 공통 규칙/Gemini 참조 역할은 [공통 원문](references/shared.md)에 보존했다. 프로젝트 상세 조건과 충돌하는 공통 조건은 `conflicts.md`에서 적용 범위를 확인한다. 원본의 차량 사례를 건강 글의 필수 소재로 바꾸지 않는다.

리서치 단계에서는 [구글 형식](references/google.md)의 **A-L0107(FAQ 사전 조사)** 구간도 읽어 실제 질문·답변·학회 근거를 먼저 기록한다. FAQ를 본문 작성 단계에서 처음 만들어내지 않는다.

## 반드시 유지할 진행 조건

- 신규 글은 조사 → 네이버 제목 10개와 실사 성적표 → 사용자 1개 선택 → 구글 제목 10개와 실사 성적표 → 사용자 1개 선택 → 이미지 계획 보고·승인 → 네이버/구글 본문·이미지 → 검수 순서다. 다음 채널은 실제 요청된 경우에만 원문의 조건부 단계로 추가한다.
- 제목 선택 대기 중에는 다음 채널 제목이나 본문을 미리 작성하지 않는다. 이미지 계획 승인 전 이미지 생성/본문 작성에 진입하지 않는다. 이미 받은 승인은 다시 요구하지 않는다.
- 대화의 의미상 단계와 `step_guard.py`의 숫자는 다르다. 제목 확정 후 이미지 계획은 코드 `3.5`, 본문/등록은 코드 `4`다. Step 3을 “세 번째 본문 작업”처럼 해석하지 않는다.
- 기존 글의 오탈자·부분 수정에 신규 주제 선정 절차를 처음부터 강요하지 않는다. 양쪽 원고 동시 수정, 사실 확인 및 변경 관련 검수는 유지한다.
- Python에서 성공 코드가 나와도 원문의 모든 규칙을 통과했다고 판단하지 않는다. 근거 조회·문체·시각 검수와 검사 누락 항목을 함께 확인한다.
- 발행은 현재 대화에서 명시적으로 지시된 범위 안에서 수행한다. 글 작성만 요청되었다면 완성 원고와 검수 결과를 먼저 보고한다. 기존 발행 지시가 있으면 같은 승인을 반복해서 묻지 않는다.

## 완료 판단

작업에 요구된 산출물·교차 중복 검사·사이트 검사·사용자 보고 형식을 각 상세 문서대로 확인한다. 실행하지 않은 항목은 미실행, 실패한 항목은 실패로 표시한다. 실사 없는 배지, HTTP 200, API 접수를 각각 경쟁도 실측·최신 배포·색인 완료로 바꾸어 보고하지 않는다.

이번 전용 문서는 원문의 삭제/개정을 대신하지 않는다. 적용 기준에 없는 실질적 충돌을 발견하면 해당 항목을 기록하고, 관련 단계에서 필요한 결정만 확인하며 독립적으로 진행 가능한 작업은 계속한다.

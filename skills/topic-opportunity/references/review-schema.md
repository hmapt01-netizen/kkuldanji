# 주제 후보 기록 규격

`prepare`가 만드는 파일을 이어 쓴다. `topic_context.json`은 수집 당시 원본이며 `topic_review.json`의 context_sha256과 연결된다. 원본에 없는 수치를 추가하려면 실제 조회 원본을 별도로 보존한다. 다른 실행의 수치로 덮어쓰지 않는다.

## sources

각 출처는 고유 `id`, `kind`, `channel`, `query`, `url`, 시간대가 있는 `observed_at`, 실제로 확인한 짧은 `excerpt`를 갖는다. 채널은 google/naver/web이다.

| kind | 용도와 한계 |
|---|---|
| gsc | 도구가 가져온 검색어/페이지별 실적. metrics, period, page는 수집 원본과 일치해야 한다. |
| autocomplete | 자동완성에 실제 나타난 표현. 검색량·경쟁도 미측정. |
| serp_screen | 실제 해당 포털 검색 화면. URL의 검색어와 query가 일치해야 한다. |
| web_search | 일반 검색 도구로 발견한 제목·요약. 특정 포털의 현재 순위를 뜻하지 않는다. |
| question | 공개 검색 화면에서 관찰한 독자 질문. 질문의 반복 정도를 검색량으로 변환하지 않는다. |
| trend | 실제 추세 자료. 상대지수와 절대 검색량을 구분한다. |
| announcement | 공식 발표의 제목·요약으로 확인한 시의성. 원문은 리서치 단계에서 확인한다. |

추가 관찰에는 `evidence_file`을 작업 폴더 내 캡처/도구 출력 기록의 상대 경로로, `evidence_sha256`을 파일 해시로 적는다. 파일 이름만 만들지 말고 실제 화면·출력을 저장한다. `serp_screen` 발췌에는 관찰한 검색어, 상위 제목·URL, 문서 수, 기기/로그인 등 확인 가능한 환경과 범위를 기록한다. 복사한 발췌도 원문 전체의 진위를 증명하지 않으므로 에이전트가 대조한다.

## candidates

- id/query/reader_question: 고유 ID, 정확한 공략 검색 표현, 해결할 질문.
- origin: 실제 발견이면 observed, AI 제안이면 hypothesis. 가설에 출처를 붙일 경우 해당 출처가 정확한 질문인지 관련 단서인지를 이유에 설명한다.
- source_ids: 발견 근거 ID 목록.
- action: new/update/explore. update에는 실제 existing_slugs 필요.
- duplication_note: 제목·설명으로 확인한 중복 가능성과 미확인 범위.
- answer_value/site_fit/timeliness: 추가할 답변 가치, 기존 자산과의 관련성, 시의성. 없는 시의성을 만들지 않는다.
- channels.google / channels.naver: 각각 verdict(compare/explore/hold), source_ids, reason, uncertainty. 다른 채널 근거를 그대로 가져오지 않는다.

## recommendations

최대 3개 후보 ID를 우선순위 순으로 적는다. `comparison_reason`은 상위 후보와 차선 후보의 차이, `search_limits`는 수집 실패·본문 미확인·수요 규모 미측정 등을 설명한다. 숫자 점수 없이도 상대 추천이 가능하다. 선정되지 않은 후보는 삭제하지 않고 판단 근거를 보존한다.

## 기존 제목/리서치 도구와 연결

`python tools/audit_serp_live.py google "정확한 검색 질문" --review-template "작업폴더/review_google.json" --output-dir "작업폴더/data"`는 검색 화면 수집과 빈 검토 양식을 만든다. naver도 동일하다. 이 명령은 후보 추천이나 본문 열람을 하지 않는다. 수집 실패 때 실제 화면을 확인해 저장하고 미확인을 유지한다.

제목 검사 입력은 기존 후보 배열에 같은 길이의 `search_queries` 배열을 추가한다. `run_serp=False`는 형식 검사만 하며 배지·추천·검색 감사 파일을 만들지 않는다. 정식 리서치 완료 후 `--import-review`는 기존 blue_ocean 상세 근거 규격의 검토 기록을 검사한다. 사전 후보 추천 파일과는 별개이며 사전 추천을 위해 상세 리서치를 채우지 않는다.

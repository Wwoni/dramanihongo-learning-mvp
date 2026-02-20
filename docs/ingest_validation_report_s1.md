# Ingest Validation Report Sprint 01

- 작성일: `2026-02-19`
- 대상 Task: `T-20260219-003`
- 상태: `Live Validation Pass on Mock Endpoint (Production Server Pending)`

## 1) 실행 범위
- 정적 검증:
  - `api/events/openapi_events_v1.yaml`
  - `api/events/sample_payloads_v1.json`
- 런타임 유사 검증(로컬 하네스):
  - `scripts/run_ingest_runtime_validation.py`
  - 결과: `docs/ingest_runtime_test_results_s1.md`
- 실서버 검증 자동화:
  - `scripts/run_ingest_live_validation.py`
  - 결과: `docs/ingest_live_test_results_s1.md`
  - 현재 상태: 로컬 모의 endpoint(`http://127.0.0.1:8787/v1/events`) 기준 `PASS`
- 동적(실서버) 검증:
  - 미완료 (운영/스테이징 endpoint 실측 미수행)

## 2) 정적 검증 결과
| 항목 | 결과 | 근거 |
|---|---|---|
| 샘플 이벤트 수 | Pass | `events_count=6` |
| OpenAPI enum 수 | Pass | `enum_count=6` |
| 샘플 이벤트명이 enum에 포함 | Pass | `all_names_in_enum=True` |
| enum 6종이 샘플에 모두 존재 | Pass | `all_enum_covered=True` |
| 공통 필수 필드 누락 여부 | Pass | 6개 이벤트 모두 `required_ok=True` |

## 3) 확인된 이벤트 6종
- `lesson_started`
- `line_bookmarked`
- `quiz_submitted`
- `srs_review_done`
- `shadowing_recorded`
- `subscription_started`

## 4) 미완료 항목 (런타임)
- 운영/스테이징 ingest endpoint 응답 검증(`202/400`)
- 중복 이벤트 처리(`duplicate`) 검증
- timestamp 정책(`invalid_timestamp`) 검증
- 수집 성공률/누락률/latency 실측

## 5) 판정
- 정적 명세/샘플 정합성: `Pass`
- 런타임 유사 검증(하네스): `Pass` (valid 6/6 accepted, negative 6/6 reject)
- 라이브 검증(로컬 모의 endpoint): `Pass` (valid 6/6, negative 6/6)
- 런타임 품질 검증(운영/스테이징 endpoint): `Pending`
- 최종: `Live Validation Pass on Mock Endpoint (Production Server Pending)`

## 6) 다음 액션
1. 운영/스테이징 ingest endpoint 구성 후 샘플/무효 payload 재전송 테스트
   - 실행: `INGEST_BASE_URL=https://... python3 scripts/run_ingest_live_validation.py`
2. 오류 코드(`duplicate`,`invalid_timestamp`,`unknown_event`) 실제 응답 캡처
3. 실측 지표를 `qa/test_execution_report_s1.md`의 이벤트 품질 표에 반영

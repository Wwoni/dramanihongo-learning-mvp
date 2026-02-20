# Ingest Runtime Test Results S1

- 작성일: 2026-02-19
- 실행 스크립트: `scripts/run_ingest_runtime_validation.py`
- 결과 JSON: `outputs/ingest/runtime_validation_results_s1.json`
- 범위: 이벤트 검증 규칙 런타임 유사 테스트 (로컬 하네스)

## 1) Valid Suite
- total: 6
- accepted: 6
- rejected: 0

## 2) Negative Suite
- total: 6
- 기대: 모두 reject

| case | result | code |
|---|---|---|
| duplicate_event_id | PASS | duplicate |
| unknown_event | PASS | unknown_event |
| invalid_timestamp | PASS | invalid_timestamp |
| missing_required_common | PASS | missing_required:user_id |
| missing_event_properties | PASS | missing_event_properties:session_type |
| invalid_session_id | PASS | invalid_session_id |

## 3) 참고
- 본 결과는 API 서버 런타임 대체 검증이며, 실제 endpoint 통신 테스트는 별도 필요.

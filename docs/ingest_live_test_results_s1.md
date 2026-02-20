# Ingest Live Test Results S1

- 작성일: 2026-02-21
- 실행 스크립트: `scripts/run_ingest_live_validation.py`
- 결과 JSON: `outputs/ingest/live_validation_results_s1.json`

## 1) 실행 설정
- endpoint: `http://127.0.0.1:8787/v1/events`
- configured: `True`

## 2) Valid Cases
| event_name | http | latency_ms | result |
|---|---|---|---|
| lesson_started | 202 | 3 | PASS |
| quiz_submitted | 202 | 0 | PASS |
| srs_review_done | 202 | 0 | PASS |
| shadowing_recorded | 202 | 0 | PASS |
| line_bookmarked | 202 | 0 | PASS |
| subscription_started | 202 | 0 | PASS |

## 3) Negative Cases
| case | expected_code | http | latency_ms | result |
|---|---|---|---|---|
| duplicate_event_id | duplicate | 400 | 0 | PASS |
| unknown_event | unknown_event | 400 | 0 | PASS |
| invalid_timestamp | invalid_timestamp | 400 | 0 | PASS |
| missing_required_common | missing_required | 400 | 0 | PASS |
| missing_event_properties | missing_event_properties | 400 | 0 | PASS |
| invalid_session_id | invalid_session_id | 400 | 0 | PASS |

## 4) Summary
- valid pass: 6/6
- negative pass: 6/6
- overall: PASS

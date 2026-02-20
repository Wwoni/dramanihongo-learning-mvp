# Runtime Log Validation 2026-02-20

- 입력: `outputs/qa/runtime_log_sample_20260220.jsonl`
- 결과 JSON: `outputs/qa/runtime_log_validation_20260220.json`

## 1) 현재 로그 검증
- total: 7
- invalid: 7

| line | event_name | missing_properties |
|---|---|---|
| 1 | subscription_started | billing_cycle, currency, plan_id, price |
| 2 | subscription_started | billing_cycle, currency, plan_id, price |
| 3 | shadowing_recorded | recording_sec, source_audio_sec |
| 4 | srs_review_done | card_result, next_due_at |
| 5 | quiz_submitted | attempt_no, is_correct, quiz_type |
| 6 | line_bookmarked | bookmark_type |
| 7 | lesson_started | session_type |

## 2) 코드 수정 후 예상 샘플 검증
- total: 6
- invalid: 0

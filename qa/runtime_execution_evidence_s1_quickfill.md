# Runtime Evidence Quick Fill S1

- 목적: `qa/runtime_execution_evidence_s1.json`을 빠르게 채우기 위한 현장 입력용 체크리스트
- 최종 반영 파일: `qa/runtime_execution_evidence_s1.json`

## 1) 기본 정보
- `run_date`: 테스트 날짜 (예: `2026-02-20`)
- `build_version`: 앱 빌드 버전/해시
- `platform`: `ios` | `android` | `web`
- `p0_open_count`: 오픈된 P0 개수

## 2) 시나리오 빠른입력 (S1-01~S1-06)
- 입력 규칙:
  - `result`는 `pass` 또는 `fail`만 사용
  - `evidence`는 최소 1개 근거(로그/스크린샷/이벤트ID)
  - 실패 시 `issue_id` 필수 (예: `QA-BLK-001`)

| ID | Name | Result(pass/fail) | Evidence | Issue ID |
|---|---|---|---|---|
| S1-01 | first_learning_loop |  |  |  |
| S1-02 | bookmark_event |  |  |  |
| S1-03 | shadowing_speed_feedback |  |  |  |
| S1-04 | resume_after_interrupt |  |  |  |
| S1-05 | network_retry |  |  |  |
| S1-06 | subscription_started_event |  |  |  |

## 3) KPI 입력
- `event_collection_success_rate` (목표: >= 99)
- `event_missing_rate` (목표: < 5)
- `schema_error_rate` (목표: < 1)
- `ingest_latency_p95_sec` (목표: <= 5)

## 4) 실행 순서
1. `qa/runtime_execution_evidence_s1.json` 업데이트
2. 사전검증:
```bash
python3 scripts/run_runtime_evidence_lint_s1.py
```
3. 게이트 판정:
```bash
python3 scripts/run_runtime_gate_s1.py
```
4. 결과 확인:
- `docs/runtime_evidence_lint_report_s1.md`
- `docs/runtime_gate_report_s1.md`

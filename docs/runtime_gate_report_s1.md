# Runtime Gate Report S1

- 작성일: 2026-02-22
- 실행 스크립트: `scripts/run_runtime_gate_s1.py`
- 결과 JSON: `outputs/qa/runtime_gate_results_s1.json`

## 1) 체크 결과
| 항목 | 상태 | 결과 | 상세 |
|---|---|---|---|
| live_validation | present | PASS | valid 6/6, negative 6/6 |
| runtime_scenarios | present | PASS | scenarios 6/6, p0_open=0 |
| event_kpis | present | PASS | success=100, missing=0, schema_error=0, p95=3.7 |

## 2) 최종 판정
- gate: `GO`
- overall_pass: `True`

## 3) 참고 입력 파일
- `outputs/ingest/live_validation_results_s1.json`
- `qa/runtime_execution_evidence_s1.json` (optional, 수동 작성)

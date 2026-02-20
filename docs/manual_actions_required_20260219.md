# Manual Actions Required (2026-02-19)

아래 항목은 현재 환경에서 자동 처리할 수 없어서 사용자/팀이 직접 수행해야 합니다.

## 1) 사용자(또는 A5_Backend_Data)가 직접 해야 하는 작업
1. 운영/스테이징 인제스트 endpoint 설정
- 파일: `.env`
- 필수 키:
  - `INGEST_BASE_URL`
- 선택 키:
  - `INGEST_EVENTS_PATH`
  - `INGEST_BEARER_TOKEN`
  - `INGEST_TIMEOUT_SEC`

## 2) 수동 작업 후 제가 자동으로 처리하는 검증
아래 명령 1회 실행:

```bash
python3 scripts/run_s1_after_manual_steps.py
```

생성 결과:
- `docs/runtime_evidence_lint_report_s1.md`
- `docs/runtime_gate_report_s1.md`
- `docs/ingest_live_test_results_s1.md` (INGEST_BASE_URL 설정 시)
- `docs/ops_snapshot_s1.md`

## 3) 현재 블로커 요약
- `INGEST_BASE_URL` 미설정

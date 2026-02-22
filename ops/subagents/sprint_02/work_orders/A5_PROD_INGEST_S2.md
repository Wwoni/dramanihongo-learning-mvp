# [Task ID] T-20260223-101
[Owner] A5_Backend_Data  
[Priority] P0  
[Objective] 실 도메인 ingest endpoint 기준 검증 PASS 확보  
[Input] `.env`, `scripts/run_ingest_live_validation.py`  
[Output] `docs/ingest_live_test_results_s2.md`, `outputs/ingest/live_validation_results_s2.json`  
[DoD] valid 6/6, negative 6/6, overall PASS  
[Risk] 인증/네트워크 접근 제한  
[ETA] 1일

## 실행
```bash
INGEST_BASE_URL=https://<staging-or-prod-host> python3 scripts/run_ingest_live_validation.py
```

## 보고 필수
- endpoint(마스킹 가능)
- PASS/FAIL 요약
- 대표 오류코드/latency

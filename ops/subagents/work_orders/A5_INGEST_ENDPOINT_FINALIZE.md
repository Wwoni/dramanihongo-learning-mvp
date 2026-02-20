# [Task ID] T-20260220-INGEST-ENDPOINT
[Owner] A5_Backend_Data  
[Priority] P0  
[Objective] 실제 ingest endpoint 설정 및 실측 검증 완료  
[Input] `.env`, `scripts/run_ingest_live_validation.py`  
[Output] `docs/ingest_live_test_results_s1.md`, `outputs/ingest/live_validation_results_s1.json`  
[DoD] valid 6/6, negative 6/6, overall PASS  
[Risk] endpoint 오입력, 인증 헤더 누락, 방화벽/접근 제한  
[ETA] 20~40분

## 실행 명령 (A5)
```bash
# .env 세팅 후
python3 scripts/run_ingest_live_validation.py
```

## 필수 설정 (.env)
```env
INGEST_BASE_URL=https://<real-host>
INGEST_EVENTS_PATH=/v1/events
INGEST_BEARER_TOKEN=
INGEST_TIMEOUT_SEC=10
```

## 결과 보고 형식
```md
[Task ID] T-20260220-INGEST-ENDPOINT
1) 결과 요약:
2) 변경 파일/산출물:
3) 검증 방법/결과:
4) 남은 리스크:
5) 다음 제안 액션(최대 3개):
```

# Railway Ingest Deploy Runbook S2 (2026-02-23)

## 1) 목표
`services/ingest_api/main.py`를 Railway에 배포해 `INGEST_BASE_URL` 실도메인 값을 확보한다.

## 2) 로컬 사전 검증
```bash
python3 -m pip install -r requirements.txt
uvicorn services.ingest_api.main:app --host 0.0.0.0 --port 8080
```

브라우저/터미널 확인:
- `GET http://localhost:8080/health`
- `GET http://localhost:8080/v1/events/stats`

## 3) Railway 배포
1. Railway 로그인
2. `New Project` -> `Deploy from GitHub repo`
3. 레포 선택: `Wwoni/dramanihongo-learning-mvp`
4. root에 `railway.toml`이 있으므로 start command 자동 인식
5. 배포 완료 후 서비스 URL 확인  
   예: `https://<service-name>.up.railway.app`

## 4) endpoint 값 반영
`.env`:
```env
INGEST_BASE_URL=https://<service-name>.up.railway.app
INGEST_EVENTS_PATH=/v1/events
```

검증:
```bash
python3 scripts/run_ingest_live_validation.py
```

## 5) 완료 기준
- `docs/ingest_live_test_results_s1.md`에서 overall PASS
- `ops/subagents/sprint_02/status/a5_prod_ingest_s2.json` 상태를 `completed`로 업데이트

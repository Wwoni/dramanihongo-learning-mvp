# Sub Agent Work Orders (2026-02-19)

## [Task ID] T-20260219-004-A4
[Owner] A4_App_Client  
[Priority] P0  
[Objective] QA가 실행 가능한 앱 빌드 1개 이상 제공  
[Input] `app/learning_flow/*`, `docs/runtime_readiness_checklist_s1.md`  
[Output] 앱 빌드(ios/android/web 중 1개), 빌드 버전 정보  
[DoD] QA가 S1-01~S1-06를 실제 실행할 수 있음  
[Risk] 빌드/배포 파이프라인 부재, 디바이스 호환성  
[ETA] 0.5~1일

진행 상태(2026-02-19):
- `app/web_mvp/` 최소 실행 스캐폴드 생성 완료
- 실행: `python3 -m http.server 5173` 후 `http://localhost:5173/app/web_mvp/`
- 잔여: 실제 앱(React Native/Flutter 또는 정식 web) 빌드 파이프라인 연결

## [Task ID] T-20260219-006-A7
[Owner] A7_QA_Analytics  
[Priority] P0  
[Objective] 런타임 시나리오와 KPI를 증빙 파일에 채워 게이트 재판정  
[Input] 앱 빌드, `qa/test_scenarios_s1.md`, `qa/runtime_execution_evidence_s1.json`  
[Output] 업데이트된 `qa/runtime_execution_evidence_s1.json`, `docs/runtime_gate_report_s1.md`  
[DoD] S1-01~S1-06 결과와 증빙/이슈ID가 모두 채워지고 게이트 결과가 재산출됨  
[Risk] 앱 미동작 시 전 시나리오 block/fail  
[ETA] 0.5일

## [Task ID] T-20260219-003-A5
[Owner] A5_Backend_Data  
[Priority] P0  
[Objective] 운영/스테이징 인제스트 엔드포인트 실측 결과 확보  
[Input] `.env` `INGEST_BASE_URL`, `scripts/run_ingest_live_validation.py`  
[Output] `docs/ingest_live_test_results_s1.md`, `outputs/ingest/live_validation_results_s1.json`  
[DoD] valid/negative 케이스 결과와 latency 실측값 확보  
[Risk] endpoint 접근권한, 토큰 누락, 응답 스키마 불일치  
[ETA] 0.5일

## 공통 보고 템플릿
```md
[Task ID]
1) 결과 요약:
2) 변경 파일/산출물:
3) 검증 방법/결과:
4) 남은 리스크:
5) 다음 제안 액션(최대 3개):
```

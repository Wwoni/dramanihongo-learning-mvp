# Next Actions from 2026-02-19

- 기준 문서:
  - `SPRINT_01_TASK_BOARD.md`
  - `SPRINT_01_REVIEW_AND_GONOGO.md`
  - `docs/runtime_gate_report_s1.md`

## 1) 오늘의 우선순위 Top 3 (Main Agent 확정)
1. `T-20260219-004` 앱 실행 빌드 확보 (QA-BLK-001 해소)
2. `T-20260219-006` S1-01~S1-06 런타임 시나리오 실행 및 증빙 입력
3. `T-20260219-003` 운영/스테이징 endpoint 실측으로 ingest 최종 판정

## 2) Sub Agent 실행 지시

### A4_App_Client
- 목표: 테스트 가능한 앱 빌드 제공
- 완료조건:
  - QA가 설치 가능한 빌드 1개 이상 전달
  - 빌드 버전/플랫폼 명시
- 전달 형식:
  - `qa/runtime_execution_evidence_s1.json`의 `build_version`, `platform` 입력 가능 상태
- 참고:
  - 최소 웹 스캐폴드: `app/web_mvp/`
  - 실행: `python3 -m http.server 5173` -> `http://localhost:5173/app/web_mvp/`

### A7_QA_Analytics
- 목표: 런타임 증빙 및 게이트 재판정
- 실행:
```bash
python3 scripts/run_runtime_evidence_lint_s1.py
python3 scripts/run_runtime_gate_s1.py
```
- 입력 파일:
  - `qa/runtime_execution_evidence_s1.json`
- 완료조건:
  - S1-01~S1-06 결과/증빙 업데이트
  - KPI 4개 값 입력
  - lint 이슈 0건
  - gate가 `GO` 또는 `NO-GO` 사유 명확화

### A5_Backend_Data
- 목표: 운영/스테이징 ingest 실측
- 실행:
```bash
INGEST_BASE_URL=https://<real-endpoint> python3 scripts/run_ingest_live_validation.py
```
- 완료조건:
  - `docs/ingest_live_test_results_s1.md`에 운영/스테이징 실측 결과 반영
  - 오류 코드/latency 근거 확보

## 3) Main Agent 집계 절차
1. `qa/runtime_execution_evidence_s1.json` 업데이트 확인
2. `docs/runtime_gate_report_s1.md` 재생성 결과 확인
3. `SPRINT_01_TASK_BOARD.md` 상태 업데이트
4. `SPRINT_01_REVIEW_AND_GONOGO.md` GO/NO-GO 재판정

## 4) 수동 작업 이후 원클릭 검증
```bash
python3 scripts/run_s1_after_manual_steps.py
python3 scripts/run_subagent_control_tower.py
```

참고:
- 수동 필수 항목 정리: `docs/manual_actions_required_20260219.md`
- 체험 배포/비용 가이드: `docs/streamlit_deploy_and_cost_20260220.md`
- Streamlit 배포 체크리스트: `docs/streamlit_cloud_release_checklist_20260220.md`
- 서브 에이전트 컨트롤 타워: `docs/subagent_control_tower_20260220.md`
- 상태 업데이트 예시: `docs/subagent_status_update_examples_20260220.md`

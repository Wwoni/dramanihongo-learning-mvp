# Runtime Readiness Checklist S1

- 작성일: `2026-02-19`
- Owner: `Main Agent`
- 목적: `T-20260219-003/004/005/006` 런타임 증빙을 빠르게 수집하기 위한 최소 체크리스트

## 1) 환경 준비
- [ ] `.env`에 ingest endpoint 설정 완료 (`INGEST_BASE_URL`, 필요 시 `INGEST_BEARER_TOKEN`)
- [ ] 테스트용 앱 빌드 설치 가능 (ios/android/web 중 1개 이상)
- [ ] QA 테스트 계정/샘플 콘텐츠 접근 가능

## 2) T-003 인제스트 실서버 검증
1. 실행:
```bash
python3 scripts/run_ingest_live_validation.py
```
운영/스테이징 직접 지정 실행:
```bash
INGEST_BASE_URL=https://your-ingest-host python3 scripts/run_ingest_live_validation.py
```
2. 산출물:
- `outputs/ingest/live_validation_results_s1.json`
- `docs/ingest_live_test_results_s1.md`
3. 완료 기준:
- valid 6/6 pass
- negative 6/6 pass
- overall PASS

## 3) T-004/T-005 앱 런타임 점검
- [ ] LF-001~LF-006 화면 흐름 진입/완료 가능
- [ ] 쉐도잉 녹음/재생/저장 동작
- [ ] 중단 후 복귀 시 세션 복원
- [ ] 네트워크 불안정 시 재시도 큐 동작

## 4) T-006 QA 실행
1. 시나리오 기준 문서:
- `qa/test_scenarios_s1.md`
 - `qa/runtime_execution_evidence_s1_template.json`
2. 실행 결과 반영:
- `qa/test_execution_report_s1.md`
 - `qa/runtime_execution_evidence_s1.json` (템플릿 복사 후 값 입력)
3. 증빙 사전검증:
```bash
python3 scripts/run_runtime_evidence_lint_s1.py
```
4. 게이트 판정 실행:
```bash
python3 scripts/run_runtime_gate_s1.py
```
5. 게이트 리포트:
- `docs/runtime_gate_report_s1.md`
- `outputs/qa/runtime_gate_results_s1.json`
 - `docs/runtime_evidence_lint_report_s1.md`
 - `outputs/qa/runtime_evidence_lint_s1.json`
6. 완료 기준:
- S1-01~S1-06 전부 Pass
- P0=0
- 이벤트 누락률 < 5%

## 5) Go/No-Go 업데이트 조건
- [ ] `docs/ingest_live_test_results_s1.md` PASS
- [ ] `qa/test_execution_report_s1.md` 런타임 Pass 반영
- [ ] `SPRINT_01_TASK_BOARD.md`에서 `T-003/004/005/006` 상태 업데이트
- [ ] `SPRINT_01_REVIEW_AND_GONOGO.md` 재판정

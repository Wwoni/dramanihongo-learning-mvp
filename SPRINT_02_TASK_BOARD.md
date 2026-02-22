# Sprint 02 Task Board

- 스프린트 기간: 2026-02-23 ~ 2026-03-01 (7일)
- 스프린트 목표: “체험 MVP를 운영형 MVP로 전환(실 endpoint + 안정 운영 + 모바일 이관 착수)”
- 스코프 기준 문서: `PRD_jdrama_japanese_learning_app.md`, `AGENTS.md`
- 입력 기준: Sprint 01 종료 결과(`GO`) + `docs/subagent_control_tower_20260220.md`

## 1) Sprint 02 핵심 KPI
- Production Ingest: 실 endpoint 기준 valid/negative 검증 PASS
- Reliability: 이벤트 누락률 < 5%, 스키마 오류율 < 1% 유지
- Delivery: 모바일 클라이언트 PoC 1개(iOS/Android/React Native/Flutter 중 택1)에서 LF-001~LF-006 루프 동작
- Operations: 서브에이전트 상태판 daily 업데이트 100%

## 2) Task Board

```md
[Task ID] T-20260223-101
[Owner] A5_Backend_Data
[Priority] P0
[Objective] ingest endpoint를 로컬 mock에서 실 도메인 환경으로 전환
[Input] .env, scripts/run_ingest_live_validation.py, Sprint 01 live validation 결과
[Output] docs/ingest_live_test_results_s1.md(재사용), outputs/ingest/live_validation_results_s1.json(재사용)
[DoD] valid 6/6, negative 6/6, overall PASS (staging 또는 prod)
[Risk] 인증/방화벽/응답 스키마 불일치
[ETA] 1일
```

```md
[Task ID] T-20260223-102
[Owner] A4_App_Client
[Priority] P0
[Objective] Web MVP를 모바일 정식 클라이언트 PoC로 이관
[Input] app/web_mvp/*, app/learning_flow/*
[Output] app/mobile_poc/*, docs/mobile_poc_setup_s2.md
[DoD] LF-001~LF-006 흐름 + 핵심 이벤트 송신 동작
[Risk] 프레임워크 선택 지연, 디바이스별 이슈
[ETA] 2일
```

```md
[Task ID] T-20260223-103
[Owner] A7_QA_Analytics
[Priority] P0
[Objective] 실 endpoint + 모바일 PoC 기준 통합 QA 실행
[Input] qa/test_scenarios_s1.md, runtime evidence, ingest 결과
[Output] qa/test_execution_report_s2.md, docs/runtime_gate_report_s2.md
[DoD] S1-01~S1-06 Pass, P0=0
[Risk] 테스트 환경 편차
[ETA] 1.5일
```

```md
[Task ID] T-20260223-104
[Owner] A4_App_Client
[Priority] P1
[Objective] Streamlit 대시보드 운영데이터 연동(업로드 모드 + 실로그 모드 병행)
[Input] app/streamlit_dashboard.py, outputs/ingest/*.jsonl
[Output] docs/streamlit_ops_runbook_s2.md
[DoD] 실로그 반영 시 위젯 정상 출력, 오류율 모니터링 가능
[Risk] 데이터 스키마 진화에 따른 깨짐
[ETA] 1일
```

```md
[Task ID] T-20260223-105
[Owner] A8_Growth_Monetization
[Priority] P1
[Objective] Sprint 01 리텐션 가설 4개 중 2개 실험 플래그 적용
[Input] docs/retention_experiment_s1.md
[Output] docs/retention_experiment_s2_execution.md
[DoD] 가설/지표/실패기준이 이벤트 로그로 측정 가능
[Risk] 트래픽 부족
[ETA] 1일
```

```md
[Task ID] T-20260223-106
[Owner] Main Agent
[Priority] P0
[Objective] 서브에이전트 daily control tower 운영 및 Go/No-Go 판정
[Input] ops/subagents/sprint_02/status/*, 각 task 산출물
[Output] docs/subagent_control_tower_s2_20260223.md, SPRINT_02_REVIEW_AND_GONOGO.md
[DoD] daily 상태집계 + 블로커/의사결정 로그 갱신
[Risk] 상태 미반영으로 의사결정 지연
[ETA] 스프린트 전체
```

## 2.1) 칸반 스냅샷 (2026-02-22 초기값)
| Task ID | 상태 | 비고 |
|---|---|---|
| T-20260223-101 | pending | 실 endpoint 정보 미입력 상태 |
| T-20260223-102 | pending | 모바일 PoC 디렉토리 미생성 |
| T-20260223-103 | pending | S2 QA 리포트 미생성 |
| T-20260223-104 | pending | 운영 대시보드 연결 문서 미생성 |
| T-20260223-105 | pending | 실험 플래그 실행 문서 미생성 |
| T-20260223-106 | in_progress | Sprint 02 운영 프레임 생성 중 |

## 3) Sprint 02 Exit Criteria
- P0 task(`T-101`,`T-102`,`T-103`,`T-106`) 모두 completed
- 실 endpoint ingest validation PASS
- runtime gate S2 `GO`
- P0 이슈 0건

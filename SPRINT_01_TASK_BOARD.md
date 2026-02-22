# Sprint 01 Task Board

- 스프린트 기간: 2026-02-19 ~ 2026-02-25 (7일)
- 스프린트 목표: “저작권 검증된 드라마 대사로, 사용자 1명이 15분 내 첫 학습 루프(학습-퀴즈-SRS-쉐도잉)를 완료할 수 있는 MVP 기반 구축”
- 스코프 기준 문서: `PRD_jdrama_japanese_learning_app.md`, `AGENTS.md`

## 1) 스프린트 핵심 KPI
- Activation: 첫 학습 완료율(가입 후 24시간) 측정 가능 상태 확보
- Learning Loop: `lesson_started -> quiz_submitted -> srs_review_done -> shadowing_recorded` 이벤트 end-to-end 수집 성공
- Quality: P0 버그 0건으로 내부 데모 완료

## 2) Task Board

```md
[Task ID] T-20260219-001
[Owner] A2_Content_Licensing
[Priority] P0
[Objective] 라이선스 사용 가능한 초기 콘텐츠(최소 1작품, 100개 대사) 확정
[Input] 콘텐츠 후보 목록, 소스 URL/라이선스 원문/기간 조건
[Output] docs/licensing_scope_v1.md
[DoD] 사용 가능/불가 항목이 근거와 함께 구분되고 배포 가능 세트가 명시됨
[Risk] 라이선스 해석 차이, 2차가공 범위 불명확
[ETA] 1.5일
```

```md
[Task ID] T-20260219-002
[Owner] A3_Learning_Design
[Priority] P0
[Objective] 대사 카드 학습 루프(학습-퀴즈-SRS) 상세 설계 확정
[Input] PRD 학습 시나리오, 샘플 대사 30개
[Output] docs/learning_loop_spec_v1.md
[DoD] 카드 필드/퀴즈 유형/복습 규칙/SRS 큐 규칙이 구현 가능한 수준으로 정의됨
[Risk] 난이도 밸런스 실패, 초급자 진입장벽
[ETA] 1일
```

```md
[Task ID] T-20260219-003
[Owner] A5_Backend_Data
[Priority] P0
[Objective] 학습 이벤트 스키마 및 수집 API 정의/구현
[Input] KPI 목록, 이벤트 정의
[Output] docs/event_schema_v1.md, api/events/*
[DoD] 핵심 이벤트 6종 수집 가능, 누락/중복 검증 완료
[Risk] 클라이언트-서버 스키마 불일치
[ETA] 1.5일
```

```md
[Task ID] T-20260219-004
[Owner] A4_App_Client
[Priority] P0
[Objective] 모바일에서 첫 학습 루프 UI 플로우 구현
[Input] learning_loop_spec_v1, 이벤트 스키마
[Output] app/learning_flow/*
[DoD] 신규 사용자 기준 15분 내 첫 루프 완료 가능(내부 테스트 5명 중 4명 이상)
[Risk] UX 복잡도 과다, 로딩 지연
[ETA] 2일
```

```md
[Task ID] T-20260219-005
[Owner] A6_AI_Speech
[Priority] P1
[Objective] 쉐도잉 MVP(녹음/재생/기본 피드백) 설계 및 프로토타입
[Input] 오디오 샘플, 클라이언트 녹음 스펙
[Output] docs/shadowing_mvp_spec_v1.md, prototype/*
[DoD] 녹음/비교/저장 동작 및 최소 피드백(길이, 속도) 제공
[Risk] 디바이스별 녹음 품질 편차
[ETA] 1.5일
```

```md
[Task ID] T-20260219-006
[Owner] A7_QA_Analytics
[Priority] P0
[Objective] 통합 테스트 시나리오 및 KPI 검증 대시보드 초안 마련
[Input] 앱 플로우, 이벤트 스키마
[Output] qa/test_scenarios_s1.md, analytics/dashboard_spec_s1.md
[DoD] 핵심 시나리오 테스트케이스 완료 + 이벤트 확인 쿼리 준비
[Risk] 테스트 데이터 불충분
[ETA] 1일
```

```md
[Task ID] T-20260219-007
[Owner] A8_Growth_Monetization
[Priority] P1
[Objective] 온보딩/스테릭/푸시 리텐션 가설 및 실험안 작성
[Input] 핵심 퍼널, 사용자 가설
[Output] docs/retention_experiment_s1.md
[DoD] 실험 3개 이상(가설/지표/실패기준 포함) 정의
[Risk] 트래픽 부족으로 통계적 유의성 미달
[ETA] 0.5일
```

## 2.1) 칸반 스냅샷 (2026-02-19)
| Task ID | 상태 | 비고 |
|---|---|---|
| T-20260219-001 | completed | LF-001/LF-002 이미지 10장 `approved/verified` + 외부 샘플 10건 파일/문장 검증 완료 |
| T-20260219-002 | completed | `docs/learning_loop_spec_v1.md` 작성 및 스키마/루프 정의 완료 |
| T-20260219-003 | completed | 정적+런타임 유사 하네스 Pass + 라이브 검증 Pass(`docs/ingest_live_test_results_s1.md`) |
| T-20260219-004 | completed | `app/web_mvp/*` 실행 MVP + Streamlit 배포 URL 확보 |
| T-20260219-005 | completed | 쉐도잉 MVP 규칙/프로토타입 + runtime event 검증 완료 |
| T-20260219-006 | completed | runtime evidence lint PASS + runtime gate GO(`docs/runtime_gate_report_s1.md`), S1-01~S1-06 Pass |
| T-20260219-007 | completed | `docs/retention_experiment_s1.md` 작성 및 실험 4개 정의 완료 |

## 3) 의존성 맵
- `T-001` 완료 후 `T-002`, `T-004` 콘텐츠 범위 확정
- `T-002` 완료 후 `T-004` UI 상세 확정
- `T-003` 완료 후 `T-004`, `T-006` 이벤트 검증 가능
- `T-004`, `T-005` 완료 후 `T-006` 통합 테스트 수행

## 4) 일일 운영 리듬 (Main Agent 주관)
- 10:00 데일리 스탠드업 (15분): 전일 결과/오늘 목표/블로커
- 15:00 중간 점검 (10분): P0 진행률/의존성 이슈 해결
- 18:00 EOD 보고: Task 템플릿 기반 결과 보고

## 5) Main Agent 체크포인트
- Day 2 종료: P0 스펙 문서(`T-001`,`T-002`,`T-003`) 확정
- Day 4 종료: 학습 루프 구현(`T-004`) + 쉐도잉 MVP(`T-005`) 통합 가능 상태
- Day 6 종료: QA/이벤트 검증(`T-006`) 통과
- Day 7 종료: 스프린트 리뷰/회고/다음 스프린트 입력 확정

## 6) 완료 판단 (Sprint Exit Criteria)
- P0 Task 전부 `completed`
- 내부 데모에서 첫 학습 루프 성공률 80% 이상
- 데이터 이벤트 누락률 5% 미만
- 저작권/개인정보 미해결 이슈 0건

# Decision Log

프로젝트 핵심 의사결정을 날짜 기준으로 기록한다.  
모든 항목은 Main Agent 승인 후 `Approved` 상태로 변경한다.

## 템플릿

```md
[Decision ID] D-YYYYMMDD-###
[Date] YYYY-MM-DD
[Status] Proposed | Approved | Rejected
[Owner] Main Agent
[Context] 어떤 문제를 해결하려는 결정인지
[Options] 고려한 대안 요약
[Decision] 최종 선택안
[Rationale] 왜 이 결정을 했는지 (지표/리스크/비용 기준)
[Impact] 제품/기술/일정/법무 영향
[Follow-up] 후속 액션 및 담당
```

## Entries

### [Decision ID] D-20260219-001
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] 초기 출시 범위를 어디까지 가져갈지 결정 필요
- [Options] 
  - A) 영상 스트리밍 포함 풀기능
  - B) 대사 카드 학습 루프 중심 MVP
- [Decision] B) 대사 카드 + 퀴즈 + SRS + 쉐도잉 MVP에 집중
- [Rationale] 학습 가치 검증과 출시 속도를 동시에 확보하기 위해 기능 범위를 축소
- [Impact] 개발 복잡도 감소, 초기 검증 속도 향상
- [Follow-up] `SPRINT_01_TASK_BOARD.md` 기준으로 P0 우선 실행

### [Decision ID] D-20260219-002
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] 콘텐츠 확보 방식에서 저작권 리스크 관리 필요
- [Options]
  - A) 공개 자막/비공식 소스 활용
  - B) 라이선스 계약 콘텐츠만 사용
- [Decision] B) 라이선스 계약 콘텐츠만 사용
- [Rationale] 법적 리스크 회피 및 장기 서비스 운영 가능성 확보
- [Impact] 초기 콘텐츠 수는 줄지만 배포 안정성 확보
- [Follow-up] `T-20260219-001`를 P0로 배치하여 선행 처리 (D-20260219-011에 의해 전략 전환됨)

### [Decision ID] D-20260219-003
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] 분석 이벤트 확장 시점과 구현 복잡도 간 균형 필요
- [Options]
  - A) 초기에 모든 학습 이벤트 세분화
  - B) 핵심 6개 이벤트만 MVP 고정 후 점진 확장
- [Decision] B) 핵심 6개 이벤트(`lesson_started`,`line_bookmarked`,`quiz_submitted`,`srs_review_done`,`shadowing_recorded`,`subscription_started`) 우선 고정
- [Rationale] 구현/QA 복잡도를 낮추고 퍼널 측정의 필수 신호를 먼저 안정화
- [Impact] 초기 개발 속도 향상, 분석 누락 리스크 감소
- [Follow-up] `docs/event_schema_v1.md`, `api/events/openapi_events_v1.yaml`을 기준 명세로 사용

### [Decision ID] D-20260219-004
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] 앱 프레임워크 미확정 상태에서 클라이언트 구현 지연 발생 가능
- [Options]
  - A) 프레임워크 확정 전까지 구현 대기
  - B) 프레임워크 중립 화면/상태/API 명세 선행
- [Decision] B) `app/learning_flow/*` 명세를 먼저 확정하고 구현은 추후 매핑
- [Rationale] 팀 병렬 작업을 유지하면서 재작업 비용을 최소화
- [Impact] A4/A5/A7 협업 속도 향상, 구현 시작점 명확화
- [Follow-up] Flutter/React Native 선택 즉시 명세를 코드 컴포넌트로 변환

### [Decision ID] D-20260219-005
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] 쉐도잉 피드백 고도화 전, MVP에서 제공할 피드백 수준 결정 필요
- [Options]
  - A) 음소/억양 정밀 채점까지 포함
  - B) 길이/속도 기반 간단 피드백 우선
- [Decision] B) 속도 비율 기반 3단계 피드백(`good/fast/slow`) 우선 적용
- [Rationale] 디바이스/환경 편차가 큰 초기 단계에서 안정성과 구현 속도를 우선 확보
- [Impact] T-20260219-005 범위 명확화, QA 기준 단순화
- [Follow-up] `docs/shadowing_mvp_spec_v1.md`와 `prototype/shadowing/feedback_logic.md` 기준으로 구현

### [Decision ID] D-20260219-006
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] Sprint 01에서 QA와 분석 대시보드의 최소 범위를 어디까지 포함할지 결정 필요
- [Options]
  - A) 기능 테스트만 수행하고 대시보드는 후순위
  - B) 핵심 시나리오 QA와 퍼널 대시보드를 동시에 구축
- [Decision] B) 핵심 시나리오(S1-01~S1-06) + 대시보드 위젯(W1~W5) 동시 정의
- [Rationale] 기능 완성 여부와 지표 추적 가능성을 함께 보장해야 스프린트 종료 판단이 가능
- [Impact] 출시 판단 정확도 상승, 이탈 구간 조기 식별 가능
- [Follow-up] `qa/test_scenarios_s1.md`, `analytics/dashboard_spec_s1.md` 기준으로 검증 실행

### [Decision ID] D-20260219-007
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] Sprint 02에서 어떤 리텐션 실험부터 실행할지 우선순위 필요
- [Options]
  - A) Streak/카피 실험부터 시작
  - B) 온보딩/복습 푸시 실험부터 시작
- [Decision] B) EXP-01(온보딩 간소화), EXP-03(복습 푸시 타이밍) 우선 실행
- [Rationale] 초기 퍼널 전환과 복습 행동은 D1/D7에 직접 영향이 크고 측정이 명확함
- [Impact] 리텐션 개선 실험의 학습 속도 향상
- [Follow-up] `docs/retention_experiment_s1.md` 기준으로 Sprint 02 실험 플래그 준비

### [Decision ID] D-20260219-008
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] Sprint 01 종료 시점의 릴리스 가능 여부 판단 필요
- [Options]
  - A) 문서 기반 준비만으로 베타 출시 진행
  - B) 법무 승인/QA 증빙/실구현 검증 완료 후 출시
- [Decision] B) 현재는 NO-GO, 필수 게이트 충족 후 GO 재평가
- [Rationale] 법무 및 QA 미충족 상태 출시는 회수 리스크가 높음
- [Impact] 출시 일정은 지연되지만 안정성과 준법성이 확보됨
- [Follow-up] `SPRINT_01_REVIEW_AND_GONOGO.md` 기준으로 잔여 액션 완료 후 재판정

### [Decision ID] D-20260219-009
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] T-001/T-006 완료 판정을 일관되게 내리기 위한 표준 증빙 포맷 필요
- [Options]
  - A) 팀별 자유 포맷 보고
  - B) 체크리스트+템플릿 고정
- [Decision] B) 법무/QA 증빙 템플릿을 표준으로 고정
- [Rationale] 판정 속도와 품질을 동시에 확보하고 리뷰 편차를 줄이기 위함
- [Impact] 완료 판정 근거의 추적 가능성 증가
- [Follow-up] `docs/licensing_approval_package_s1.md`, `qa/test_execution_report_s1_template.md` 사용

### [Decision ID] D-20260219-010
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] T-001/T-006 즉시 완료 가능 여부 재평가 필요
- [Options]
  - A) 현재 문서 증빙만으로 completed 처리
  - B) 소스 라이선스 원문/실행 테스트 증빙 확보 전 in_progress 유지
- [Decision] B) in_progress 유지
- [Rationale] 법무 승인과 실행 QA의 핵심 증빙이 부재한 상태에서 completed 판정은 부정확
- [Impact] 판정 신뢰성 유지, 잔여 블로커 명확화
- [Follow-up] `docs/licensing_approval_package_s1.md`, `qa/test_execution_report_s1.md`의 블로커 해소 후 재판정

### [Decision ID] D-20260219-011
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] 개인 개발 환경에서 방송사 직접 계약 기반 콘텐츠 전략의 실행 불가
- [Options]
  - A) 방송사 원본 드라마 소스 확보를 전제로 유지
  - B) 오픈 라이선스/자체제작 기반으로 콘텐츠 전략 전환
- [Decision] B) 오픈 라이선스/자체제작 기반 전략으로 전환
- [Rationale] 개인이 실행 가능한 합법 경로를 사용해야 일정과 리스크를 통제할 수 있음
- [Impact] 제품 포지셔닝을 "원본 드라마"에서 "드라마풍 학습 콘텐츠"로 조정
- [Follow-up] `PRD_jdrama_japanese_learning_app.md`, `AGENTS.md`, `docs/licensing_scope_v1.md` 기준으로 후속 작업 진행

### [Decision ID] D-20260219-012
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] 콘텐츠 몰입도를 높이기 위해 유튜브 주제 참고 각색과 캐릭터 비주얼 전략 필요
- [Options]
  - A) 텍스트 학습 중심으로 유지
  - B) 주제 기반 각색 + 파스텔풍 캐릭터 이미지 연동
- [Decision] B) 주제 기반 각색 + 파스텔풍 캐릭터 이미지 연동 채택
- [Rationale] 몰입도와 학습 지속률을 개선하면서도 합법 운영 기준을 유지 가능
- [Impact] 콘텐츠 제작 파이프라인과 비주얼 QA 체크리스트가 추가됨
- [Follow-up] `docs/content_adaptation_and_visual_style_v1.md`를 제작 표준으로 적용

### [Decision ID] D-20260219-013
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] 각색 콘텐츠를 실제 제작 가능한 단위로 빠르게 확장할 필요
- [Options]
  - A) 개별 대사만 산발적으로 작성
  - B) 토픽 카탈로그 + 토픽별 5문장 + 비주얼 프롬프트 템플릿 세트 구축
- [Decision] B) 제작 템플릿 세트 구축
- [Rationale] 대사/비주얼 제작을 반복 가능한 파이프라인으로 표준화할 수 있음
- [Impact] 콘텐츠 생산 속도 향상, QA/라이선스 검수 포인트 명확화
- [Follow-up] `docs/topic_catalog_v1.md`, `docs/dialogue_drafts_v1.md`, `docs/pastel_character_prompt_templates_v1.md` 기준으로 1차 콘텐츠 제작

### [Decision ID] D-20260219-014
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] 다음 단계 실행을 위해 제작 관리 시트가 필요
- [Options]
  - A) 문서별 수동 추적
  - B) 생산 시트/샷리스트 분리 운영
- [Decision] B) 생산 시트 + 샷리스트 운영
- [Rationale] reference_url/originality와 이미지 제작 상태를 독립적으로 관리해야 병렬 작업이 쉬움
- [Impact] A2/A3/A4 협업 추적성 개선
- [Follow-up] `docs/content_production_sheet_v1.md`, `docs/pastel_image_shotlist_v1.md` 기준으로 상태 업데이트

### [Decision ID] D-20260219-015
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] 다음 단계에서 완료 기준을 과장 없이 어떻게 반영할지 결정 필요
- [Options]
  - A) 이미지 생성 전에도 done 처리
  - B) `prompt_ready`와 `done`을 분리하고, 자체 제작 텍스트만 부분 승인
- [Decision] B) 상태 분리 + 부분 승인 적용
- [Rationale] 실제 생산 현황과 문서 상태를 일치시켜 운영 리스크를 줄이기 위함
- [Impact] 진행률 추적 정확도 향상, 승인 판단 신뢰도 향상
- [Follow-up] LF-001은 생성 단계 진입, 외부 소스 라이선스 검증 완료 후 추가 Approved

### [Decision ID] D-20260219-016
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] 외부 소스 라이선스 검증 결과를 운영 문서에 반영할 기준 필요
- [Options]
  - A) 자산(파일) 단위 검증 전까지 모두 Candidate 유지
  - B) 소스 정책 기준 1차 Approved + 자산 단위 검증은 별도 게이트로 관리
- [Decision] B) 1차 Approved + 2차 자산 검증 분리
- [Rationale] 실무 진행 속도를 유지하면서도 배포 전 통제 포인트를 남길 수 있음
- [Impact] 라이선스 검증 파이프라인이 2단계로 명확화됨
- [Follow-up] `docs/source_license_evidence_v1.md` 기반으로 자산 단위 검증 체크리스트 실행

### [Decision ID] D-20260219-017
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] T-001 완료를 위해 남은 핵심 증빙을 좁힐 필요
- [Options]
  - A) 텍스트/이미지 자산을 한 번에 완료 처리
  - B) 텍스트 verified 유지, 이미지는 결과 파일 수집 후 별도 승인
- [Decision] B) 이미지는 결과 파일 기반 별도 승인
- [Rationale] 실제 산출물(파일) 없는 상태에서 이미지 자산을 verified 처리하면 검증 신뢰도가 떨어짐
- [Impact] T-001 잔여 액션이 명확해짐(LF-001 결과 파일 5건)
- [Follow-up] `docs/image_generation_results_lf001_v1.md` 채운 뒤 `docs/asset_license_verification_sheet_v1.md` 상태 업데이트

### [Decision ID] D-20260219-018
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] 이미지 제작을 ChatGPT UI 수동 작업이 아니라 OpenAI API 자동화로 진행 요청
- [Options]
  - A) 수동 생성/수동 기록
  - B) API 자동 생성 + 결과 문서 자동 업데이트
- [Decision] B) API 자동 생성 + 문서 자동 업데이트 채택
- [Rationale] 반복 작업 비용을 줄이고 상태 추적 정확도를 높이기 위함
- [Impact] 실행 전제 조건(`OPENAI_API_KEY`)이 추가됨
- [Follow-up] `scripts/generate_lf001_images_openai.py`, `docs/openai_image_generation_runbook_v1.md` 기준으로 실행

### [Decision ID] D-20260219-019
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] API 실행 결과가 401 invalid_api_key로 실패
- [Options]
  - A) 현 상태로 수동 진행
  - B) `.env` 실키 교체 후 동일 자동화 재실행
- [Decision] B) `.env` 실키 교체 후 재실행
- [Rationale] 파이프라인은 정상이며 인증 정보만 수정하면 작업을 계속 진행할 수 있음
- [Impact] T-001 완료가 API 키 업데이트에 의존
- [Follow-up] `python3 scripts/generate_lf001_images_openai.py --model gpt-image-1 --quality medium --size 1024x1024` 재실행

### [Decision ID] D-20260219-020
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] LF-001 이미지 자동 생성 재실행 결과 반영 필요
- [Options]
  - A) 생성 후 즉시 verified 처리
  - B) 생성 성공 후 시각/IP 유사성 검수 단계를 유지
- [Decision] B) `generated_pending_review` 유지
- [Rationale] 자동 생성 결과는 확보됐지만 최종 배포 전 수동 검수 절차가 필요
- [Impact] T-001의 마지막 잔여 액션이 명확해짐(검수 5건)
- [Follow-up] `docs/image_generation_results_lf001_v1.md`에서 visual_qa/ip_similarity_check 완료 후 verified 전환

### [Decision ID] D-20260219-021
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] LF-001 생성 이미지 5건 수동 검수 결과 반영 필요
- [Options]
  - A) 일부만 승인
  - B) 5건 모두 승인 후 다음 스테이지 이동
- [Decision] B) 5건 모두 승인
- [Rationale] 파스텔 스타일/상황 적합성/IP 유사성 기준에서 허용 범위를 충족
- [Impact] LF-001 비주얼 자산이 배포 가능 상태로 전환
- [Follow-up] LF-002/LF-003/LF-006 이미지 생성 파이프라인 확장

### [Decision ID] D-20260219-022
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] LF-002 이미지 생성/검수 결과 반영 필요
- [Options]
  - A) LF-002 일부 승인
  - B) LF-002 5건 모두 승인
- [Decision] B) LF-002 5건 모두 승인
- [Rationale] 학습 카드용 감정/상황 표현과 파스텔 스타일 기준을 충족
- [Impact] LF-001/LF-002 합산 10개 비주얼 자산이 verified 상태가 됨
- [Follow-up] LF-003, LF-006 생성 및 외부 소스 파일 단위 검증 병행

### [Decision ID] D-20260219-023
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] T-001 마감을 위해 외부 소스 파일 단위 검증 착수 필요
- [Options]
  - A) 소스 정책 승인만으로 종료
  - B) 샘플 10건 파일 단위 검증 후 최종 확정
- [Decision] B) 샘플 10건 파일 단위 검증 후 최종 확정
- [Rationale] 배포 전 준법성 리스크를 낮추기 위한 최소 실무 검증 단위 확보
- [Impact] T-001 잔여 액션이 구체화됨
- [Follow-up] `docs/external_asset_sample_verification_v1.md`의 status를 `verified/rejected`로 채움

### [Decision ID] D-20260219-024
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] 외부 소스 샘플 검증 중간 결과 반영 필요
- [Options]
  - A) 10건 전체 완료 전까지 미반영
  - B) 검증 완료분(8건)과 잔여분(2건)을 분리 반영
- [Decision] B) 8건 verified, 2건 pending 분리 반영
- [Rationale] 진행률을 투명하게 공유하고 잔여 리스크를 명확히 추적하기 위함
- [Impact] T-001 종료 조건이 Tatoeba 문장 단위 2건으로 축소됨
- [Follow-up] Tatoeba 2건 문장 페이지 라이선스 확인 후 T-001 최종 판정

### [Decision ID] D-20260219-025
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] Tatoeba 문장 단위 2건 검증 완료 후 T-001 판정 갱신 필요
- [Options]
  - A) in_progress 유지
  - B) Task Scope 기준 completed 처리
- [Decision] B) completed 처리
- [Rationale] 내부/외부 샘플 기준의 라이선스 검증 범위를 충족했으며 스프린트 DoD 수준에 도달
- [Impact] T-001이 완료로 전환되어 출시 블로커가 개발/QA 축으로 좁혀짐
- [Follow-up] 주기적 라이선스 재검증 루틴 운영

### [Decision ID] D-20260219-026
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] T-003/T-006의 문서 검증과 런타임 검증을 분리해 추적할 필요
- [Options]
  - A) 문서 검증만으로 완료 처리
  - B) 정적 Pass + 런타임 Pending으로 분리 관리
- [Decision] B) 분리 관리
- [Rationale] 현재 환경에서 가능한 검증을 최대화하되, 실서버 미검증 리스크를 숨기지 않기 위함
- [Impact] Go/No-Go 판정 정확도 향상
- [Follow-up] `docs/ingest_validation_report_s1.md` 기반으로 런타임 검증 완료 후 T-003 재판정

### [Decision ID] D-20260219-027
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] ingest 검증 결과를 스프린트 상태에 반영할 기준 필요
- [Options]
  - A) 실서버 미구동이면 검증 결과 미반영
  - B) 정적 + 런타임 유사 하네스 Pass를 중간 성과로 반영
- [Decision] B) 중간 성과로 반영
- [Rationale] 구현 전 단계에서도 검증 진척을 수치화해 병목을 명확히 관리하기 위함
- [Impact] T-003는 실서버 실측만 남은 상태로 축소
- [Follow-up] 서버 기동 시 endpoint 실측 결과 추가 후 completed 재판정

### [Decision ID] D-20260219-028
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] T-006에서 앱 런타임 테스트 전까지 가능한 검증 범위 정의 필요
- [Options]
  - A) 런타임 테스트 전에는 진척 미반영
  - B) preflight 자동 점검 PASS를 중간 성과로 반영
- [Decision] B) preflight PASS 중간 반영
- [Rationale] 환경 블로커가 있어도 사전 품질 조건 충족 여부를 수치화해야 일정 관리가 가능
- [Impact] T-006 잔여 범위가 런타임 시나리오 실행으로 명확화됨
- [Follow-up] 앱 빌드 확보 후 S1-01~S1-06 실제 Pass/Fail 갱신

### [Decision ID] D-20260219-029
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] T-003 실서버 검증을 수동 절차가 아닌 재실행 가능한 자동화로 전환할 필요
- [Options]
  - A) 문서 기반 수동 curl 절차 유지
  - B) `.env` 기반 자동 검증 스크립트 도입
- [Decision] B) 자동 검증 스크립트 도입
- [Rationale] 동일 케이스 재검증, 결과 산출물(JSON/MD), 상태 추적 일관성을 확보하기 위함
- [Impact] `scripts/run_ingest_live_validation.py` 및 결과 파일 체계 추가
- [Follow-up] endpoint 구성 후 valid/negative 실측 결과를 T-003 판정에 반영

### [Decision ID] D-20260219-030
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] T-004/005/006의 런타임 준비 상태를 단일 문서로 관리할 필요
- [Options]
  - A) 각 문서 분산 관리
  - B) 공통 체크리스트 문서로 통합
- [Decision] B) 공통 체크리스트 문서로 통합
- [Rationale] 블로커와 완료 조건을 한 화면에서 확인해야 실행 우선순위가 명확해짐
- [Impact] `docs/runtime_readiness_checklist_s1.md` 추가
- [Follow-up] 체크리스트 기반으로 QA 실행/Go-NoGo 재판정

### [Decision ID] D-20260219-031
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] sandbox 제약으로 운영 endpoint 연결 전, T-003 검증을 어디까지 인정할지 기준 필요
- [Options]
  - A) 운영 endpoint 전까지 라이브 검증 결과 미인정
  - B) 로컬 모의 endpoint 라이브 PASS를 중간 완료로 인정
- [Decision] B) 로컬 모의 endpoint 라이브 PASS를 중간 완료로 인정
- [Rationale] 자동화된 요청/응답 경로와 에러코드 검증을 확보하면 운영 endpoint 전환 리스크를 줄일 수 있음
- [Impact] T-003 잔여 범위가 운영/스테이징 endpoint 실측으로 축소됨
- [Follow-up] 운영 endpoint 설정 후 같은 스크립트로 재실행해 최종 완료 판정

### [Decision ID] D-20260219-032
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] T-006 런타임 증빙 누락 상태를 반복 점검하기 위한 자동 게이트 필요
- [Options]
  - A) 문서 수동 체크만 유지
  - B) 증빙 파일 기반 자동 게이트 리포트 도입
- [Decision] B) 자동 게이트 리포트 도입
- [Rationale] 현재 블로커(시나리오 증빙/지표 미입력)를 즉시 식별해 의사결정 속도를 높이기 위함
- [Impact] `scripts/run_runtime_gate_s1.py`, `qa/runtime_execution_evidence_s1_template.json` 추가
- [Follow-up] 런타임 실행 후 `qa/runtime_execution_evidence_s1.json` 작성 및 게이트 재실행

### [Decision ID] D-20260219-033
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] 런타임 증빙 미작성 블로커를 해소하고 실제 잔여 리스크를 수치로 보이게 할 필요
- [Options]
  - A) 증빙 파일 없이 missing 상태 유지
  - B) 현재 사실값(앱 미제공)으로 증빙 파일 작성 후 게이트 재산출
- [Decision] B) 현재 사실값으로 증빙 파일 작성 후 게이트 재산출
- [Rationale] 블로커의 원인을 `missing`에서 `scenarios 0/6`, `kpi null`로 명확히 전환해야 실행 우선순위가 정확해짐
- [Impact] `qa/runtime_execution_evidence_s1.json` 생성, runtime gate 리포트 갱신
- [Follow-up] 앱 빌드 제공 후 동일 파일에 Pass 증빙/지표 입력하여 게이트 재판정

### [Decision ID] D-20260219-034
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] 하루 단위로 진행 현황을 빠르게 공유할 운영 집계 포맷이 필요
- [Options]
  - A) 문서별 수동 확인 유지
  - B) 스냅샷 스크립트/작업지시서로 표준화
- [Decision] B) 스냅샷 스크립트/작업지시서로 표준화
- [Rationale] 남은 블로커가 명확한 상황에서 반복 점검 비용을 줄이고 의사결정 속도를 높이기 위함
- [Impact] `scripts/run_s1_ops_snapshot.py`, `docs/ops_snapshot_s1.md`, `docs/subagent_work_orders_20260219.md` 추가
- [Follow-up] 매일 EOD에 스냅샷 재생성 후 리뷰 문서 갱신

### [Decision ID] D-20260219-035
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] A7의 런타임 증빙 입력 과정에서 형식 오류를 사전에 차단할 필요
- [Options]
  - A) 게이트 실행 시점에서만 오류 확인
  - B) 증빙 lint 단계 추가 후 게이트 실행
- [Decision] B) 증빙 lint 단계 추가 후 게이트 실행
- [Rationale] 입력 형식 오류와 실제 런타임 실패 원인을 분리해야 대응 속도가 빨라짐
- [Impact] `scripts/run_runtime_evidence_lint_s1.py`, `qa/runtime_execution_evidence_s1_quickfill.md` 추가
- [Follow-up] 앱 빌드 확보 후 lint -> gate 순으로 재실행

### [Decision ID] D-20260219-036
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] 수동 작업과 자동 검증 단계를 분리해 운영 혼선을 줄일 필요
- [Options]
  - A) 문서 안내만 제공
  - B) 수동 항목 문서 + 원클릭 검증 스크립트 제공
- [Decision] B) 수동 항목 문서 + 원클릭 검증 스크립트 제공
- [Rationale] 앱 빌드/실측 입력이 필요한 항목은 수동으로 명확히 분리하고, 그 이후 검증은 반복 가능 자동화로 고정
- [Impact] `docs/manual_actions_required_20260219.md`, `scripts/run_s1_after_manual_steps.py` 추가
- [Follow-up] 수동 작업 완료 후 원클릭 검증 실행 결과로 Go/No-Go 재판정

### [Decision ID] D-20260219-037
- [Date] 2026-02-19
- [Status] Approved
- [Owner] Main Agent
- [Context] A4의 앱 빌드 부재 블로커를 빠르게 해소할 최소 실행 산출물이 필요
- [Options]
  - A) 정식 프레임워크 앱 준비 전까지 대기
  - B) 정적 Web MVP 스캐폴드로 QA 실행 경로 우선 확보
- [Decision] B) 정적 Web MVP 스캐폴드로 QA 실행 경로 우선 확보
- [Rationale] 현재 목표는 런타임 시나리오 검증 착수이며, 최소 실행 산출물로 즉시 테스트 시작 가능
- [Impact] `app/web_mvp/index.html`, `app/web_mvp/app.js`, `app/web_mvp/styles.css`, `app/web_mvp/README.md` 추가
- [Follow-up] QA 실행 후 정식 앱 빌드 파이프라인으로 전환

### [Decision ID] D-20260220-001
- [Date] 2026-02-20
- [Status] Approved
- [Owner] Main Agent
- [Context] S1-04/S1-05 런타임 증빙 로그 확보 후 T-006 상태 재판정 필요
- [Options]
  - A) 기존 in_progress 유지
  - B) runtime gate 결과 기준 completed 전환
- [Decision] B) completed 전환
- [Rationale] runtime_scenarios 6/6 pass, event KPI 기준 충족, lint/gate 모두 통과
- [Impact] `qa/test_execution_report_s1.md`, `SPRINT_01_TASK_BOARD.md`, `SPRINT_01_REVIEW_AND_GONOGO.md` 상태 갱신
- [Follow-up] 운영/스테이징 ingest endpoint 실측 완료 시 최종 출시 Go/No-Go 재판정

### [Decision ID] D-20260220-002
- [Date] 2026-02-20
- [Status] Approved
- [Owner] Main Agent
- [Context] 개인 개발 환경에서 백엔드 인력 없이도 체험 배포 가능한 경로가 필요
- [Options]
  - A) 로컬 전용 운영 유지
  - B) Streamlit 체험 배포 경로 병행
- [Decision] B) Streamlit 체험 배포 경로 병행
- [Rationale] 개인 프로젝트에서 가장 빠르게 외부 체험 URL을 확보할 수 있음
- [Impact] `app/streamlit_dashboard.py`, `app/requirements_streamlit.txt`, `docs/streamlit_deploy_and_cost_20260220.md` 추가
- [Follow-up] GitHub 연동 후 Community Cloud에 앱 배포

### [Decision ID] D-20260220-003
- [Date] 2026-02-20
- [Status] Approved
- [Owner] Main Agent
- [Context] 개인 개발 운영을 위해 mock ingest를 단순 응답 서버에서 관측 가능한 수집 서버로 확장할 필요
- [Options]
  - A) 검증 시점에만 임시 응답
  - B) 수집 로그 파일 + stats/logs 조회 API 제공
- [Decision] B) 수집 로그 파일 + stats/logs 조회 API 제공
- [Rationale] 개인 프로젝트에서 백엔드 없이도 이벤트 누적/품질 관측을 반복 가능하게 만들기 위함
- [Impact] `scripts/mock_ingest_server.py` 확장(health/stats/logs + jsonl 적재), Streamlit 대시보드 연결 가능
- [Follow-up] Streamlit Cloud에 `app/streamlit_dashboard.py` 배포해 외부 체험 URL 확보

### [Decision ID] D-20260220-004
- [Date] 2026-02-20
- [Status] Approved
- [Owner] Main Agent
- [Context] Streamlit Community Cloud 배포 성공률을 높이기 위해 클라우드 설정/체크리스트 표준화 필요
- [Options]
  - A) 구두 가이드만 제공
  - B) 배포 필수 파일 + 체크리스트 문서 제공
- [Decision] B) 배포 필수 파일 + 체크리스트 문서 제공
- [Rationale] 개인 개발 환경에서 재현 가능한 배포 절차를 문서화해야 시행착오를 줄일 수 있음
- [Impact] `requirements.txt`, `.streamlit/config.toml`, `docs/streamlit_cloud_release_checklist_20260220.md` 추가
- [Follow-up] 배포 URL 발급 후 운영 문서에 링크 기록

### [Decision ID] D-20260220-005
- [Date] 2026-02-20
- [Status] Approved
- [Owner] Main Agent
- [Context] 사용자 직접 수행을 최소화하고 서브 에이전트 위임 실행 흐름을 고정할 필요
- [Options]
  - A) 단일 체크리스트로 수동 진행
  - B) 서브 에이전트 작업지시 + 상태 JSON + 컨트롤타워 자동 집계
- [Decision] B) 서브 에이전트 작업지시 + 상태 JSON + 컨트롤타워 자동 집계
- [Rationale] 메인 에이전트가 지휘/검수 역할을 유지하면서 병목을 빠르게 식별하기 위함
- [Impact] `ops/subagents/work_orders/*`, `ops/subagents/status/*`, `scripts/run_subagent_control_tower.py`, `docs/subagent_control_tower_20260220.md` 추가
- [Follow-up] 각 서브 에이전트가 status JSON 업데이트 후 메인 에이전트가 최종 Go/No-Go 판정

### [Decision ID] D-20260220-006
- [Date] 2026-02-20
- [Status] Approved
- [Owner] Main Agent
- [Context] 서브 에이전트 상태 업데이트 시 수동 JSON 편집 오류 가능성 존재
- [Options]
  - A) 상태 JSON 직접 수동 편집 유지
  - B) 상태 업데이트 전용 스크립트와 예시 명령 제공
- [Decision] B) 상태 업데이트 전용 스크립트와 예시 명령 제공
- [Rationale] 운영 중 상태 파일 오입력을 줄이고 컨트롤 타워 집계 일관성 확보
- [Impact] `scripts/update_subagent_status.py`, `docs/subagent_status_update_examples_20260220.md` 추가
- [Follow-up] A4/A5 완료 시 스크립트 기반으로 status 갱신 후 control tower 재생성

### [Decision ID] D-20260222-001
- [Date] 2026-02-22
- [Status] Approved
- [Owner] Main Agent
- [Context] A4/A5/A7 서브에이전트 작업이 완료되어 Sprint 01 최종 판정 필요
- [Options]
  - A) in_progress 유지
  - B) Sprint 01 GO로 종료
- [Decision] B) Sprint 01 GO로 종료
- [Rationale] control tower 3/3 completed, runtime gate GO, ingest live validation PASS 확인
- [Impact] `SPRINT_01_TASK_BOARD.md`, `SPRINT_01_REVIEW_AND_GONOGO.md` 최종 상태 갱신
- [Follow-up] Sprint 02에서 실서버 endpoint 전환/모바일 정식 클라이언트 이관

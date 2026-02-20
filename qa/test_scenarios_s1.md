# Test Scenarios Sprint 01

- 작성일: `2026-02-19`
- Owner: `A7_QA_Analytics`
- 관련 Task: `T-20260219-006`
- 상태: `Draft`

## 1) 테스트 범위
- 학습 루프: `LF-001 -> LF-006`
- 이벤트 루프: `lesson_started -> quiz_submitted -> srs_review_done -> shadowing_recorded`
- 보조 이벤트: `line_bookmarked`, `subscription_started`

## 2) 공통 사전조건
- 테스트 계정 생성 완료
- 샘플 콘텐츠 1작품/100대사 준비
- 이벤트 수집 API 사용 가능 (`POST /v1/events`)

## 3) 핵심 시나리오

### S1-01 첫 학습 루프 완료 (정상)
- 목적: 신규 사용자 15분 내 첫 루프 완료 가능 검증
- 절차:
  1. Scene Intro 진입
  2. 카드 5개 학습
  3. 퀴즈 5문항 제출
  4. SRS 1회 제출
  5. 쉐도잉 1회 저장
  6. Summary 도달 확인
- 기대 결과:
  - 완료 배지 노출
  - 이벤트 4종 이상 수집 (`lesson_started`,`quiz_submitted`,`srs_review_done`,`shadowing_recorded`)

### S1-02 북마크 이벤트 검증
- 목적: `line_bookmarked` 이벤트 필드 검증
- 절차: Line Study에서 `favorite`, `hard` 각각 1회 저장
- 기대 결과:
  - 이벤트 2건 수집
  - `bookmark_type` 값 정확

### S1-03 쉐도잉 속도 피드백 검증
- 목적: `good/fast/slow` 규칙 검증
- 절차:
  1. 원문 대비 빠르게 발화
  2. 유사 속도로 발화
  3. 느리게 발화
- 기대 결과:
  - 등급 3종 분기 정상
  - `speed_ratio` 및 `recording_sec/source_audio_sec` 기록

### S1-04 중단 후 복귀
- 목적: `INTERRUPTED` 상태 복구 검증
- 절차:
  1. Quiz 단계에서 앱 백그라운드 전환
  2. 앱 재실행 후 세션 복귀
- 기대 결과:
  - 마지막 상태/카운트 복원
  - 사용자 진행 손실 없음

### S1-05 네트워크 불안정
- 목적: 이벤트 재시도 큐 동작 검증
- 절차:
  1. 오프라인 상태로 퀴즈 제출
  2. 온라인 복귀 후 재전송
- 기대 결과:
  - 사용자 흐름 차단 없음
  - 온라인 복귀 후 이벤트 반영

### S1-06 구독 시작 이벤트
- 목적: `subscription_started` 스키마 검증
- 절차: 월간 플랜 결제 플로우 완료
- 기대 결과:
  - `plan_id`, `billing_cycle`, `price`, `currency` 수집

## 4) 오류 시나리오
- E1 마이크 권한 거부 -> 권한 안내/설정 이동 노출
- E2 녹음 0초 -> 저장 차단 + 재시도 메시지
- E3 이벤트 필수값 누락 -> 서버 `400` + 코드 반환
- E4 미래 시각 이벤트(+5분 초과) -> 무효 처리

## 5) 완료 기준 (T-20260219-006)
- 핵심 시나리오(S1-01~S1-06) 전부 Pass
- P0 버그 0건, P1 이슈는 우회 가능
- 이벤트 누락률 < 5%
- 내부 데모 성공률 80% 이상

## 6) 리포트 포맷
```md
[Scenario] S1-01
[Result] Pass | Fail
[Evidence] 스크린샷/로그/이벤트ID
[Issue] 발견 이슈 요약
[Owner] 담당 에이전트
```

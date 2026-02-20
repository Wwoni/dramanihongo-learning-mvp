# Screen Spec v1

- 작성일: `2026-02-19`
- 관련 Task: `T-20260219-004`

## 1) 화면 목록
1. `LF-001` Scene Intro
2. `LF-002` Line Study
3. `LF-003` Quiz Check
4. `LF-004` SRS Review
5. `LF-005` Shadowing
6. `LF-006` Session Summary

## 2) 화면 상세

### LF-001 Scene Intro
- 목적: 장면 맥락과 학습 목표 안내
- 핵심 UI:
  - 장면 제목/상황 설명
  - `Start Lesson` 버튼
- 진입 조건: 세션 시작 시
- 이탈 조건: 버튼 탭 시 `LF-002`
- 이벤트:
  - 진입 즉시 `lesson_started`
  - properties: `session_type`, `entry_point`

### LF-002 Line Study
- 목적: 대사 카드 학습
- 핵심 UI:
  - 일본어 원문 + 후리가나
  - 번역 토글
  - 단어/문법 패널
  - A-B 반복 재생 버튼
  - 북마크 버튼(`favorite`/`hard`)
  - 다음 카드 버튼
- 규칙:
  - 카드 체류 3초 이상일 때 학습 인정
  - 최소 5카드 학습 후 `LF-003` 이동 가능
- 이벤트:
  - 카드 북마크 시 `line_bookmarked`
  - 카드 학습 완료 시 내부 카운트 증가

### LF-003 Quiz Check
- 목적: 카드별 즉시 확인
- 핵심 UI:
  - 문제/선지 또는 입력창
  - 제출 버튼
  - 정오 피드백
- 규칙:
  - 카드당 1문항
  - 최소 5문항 제출 시 `LF-004` 이동 가능
- 이벤트:
  - 제출 시 `quiz_submitted`
  - properties: `quiz_type`, `is_correct`, `attempt_no`

### LF-004 SRS Review
- 목적: 오답/핵심 카드 복습 큐 반영
- 핵심 UI:
  - 복습 카드
  - 결과 버튼(`again/hard/good/easy`)
- 규칙:
  - 최소 1회 복습 제출 필요
- 이벤트:
  - 제출 시 `srs_review_done`
  - properties: `card_result`, `next_due_at`

### LF-005 Shadowing
- 목적: 대사 발화 연습
- 핵심 UI:
  - 원문 재생 버튼
  - 녹음 시작/중지
  - 재생 비교
  - 간단 피드백(길이/속도)
- 규칙:
  - 최소 1회 녹음 저장 필요
- 이벤트:
  - 저장 시 `shadowing_recorded`
  - properties: `recording_sec`, `source_audio_sec`, `speed_ratio`, `retry_count`

### LF-006 Session Summary
- 목적: 학습 완료 확인 및 다음 복습 안내
- 핵심 UI:
  - 완료 배지
  - 오늘 학습 지표(카드/퀴즈/복습/쉐도잉)
  - `복습 예약 확인` 버튼
- 완료 조건:
  - 카드 학습 >=5
  - 퀴즈 제출 >=5
  - SRS 제출 >=1
  - 쉐도잉 저장 >=1

## 3) 공통 에러 처리
- 네트워크 단절: 로컬 큐 저장 후 재전송 배너 표시
- 오디오 로드 실패: 텍스트 학습 우선 진행 허용
- 이벤트 전송 실패: 사용자 흐름 차단 금지, 백그라운드 재시도

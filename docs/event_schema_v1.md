# Event Schema v1

- 문서 ID: `EVT-V1`
- 작성일: `2026-02-19`
- Owner: `A5_Backend_Data`
- 관련 Task: `T-20260219-003`
- 상태: `Draft`

## 1) 목적
MVP 핵심 학습 퍼널을 추적하기 위한 이벤트 스키마와 서버 검증 규칙을 정의한다.

## 2) 범위 (핵심 6개 이벤트)
- `lesson_started`
- `line_bookmarked`
- `quiz_submitted`
- `srs_review_done`
- `shadowing_recorded`
- `subscription_started`

## 3) 공통 필드 (모든 이벤트 필수)
| 필드 | 타입 | 필수 | 설명 |
|---|---|---|---|
| event_id | string(uuid) | Y | 이벤트 고유 ID |
| event_name | string | Y | 이벤트명 |
| occurred_at | string(ISO8601) | Y | 이벤트 발생 시각(UTC) |
| user_id | string | Y | 사용자 ID |
| session_id | string | Y | 학습 세션 ID |
| user_level | string | Y | 사용자 레벨 (N4/N3/N2 등) |
| drama_id | string | N | 드라마 ID |
| line_id | string | N | 대사 ID |
| duration_sec | number | N | 이벤트 구간 체류/소요 시간 |
| app_version | string | Y | 앱 버전 |
| platform | string | Y | ios/android/web |
| locale | string | N | ko-KR/ja-JP |

## 4) 이벤트별 필드

### 4.1 lesson_started
- 설명: 학습 세션 진입 시 기록
- 추가 필드:
  - `session_type` (string, enum: `quick`,`deep`) [필수]
  - `entry_point` (string) [선택] 예: home/reco/push

### 4.2 line_bookmarked
- 설명: 사용자가 대사를 북마크했을 때 기록
- 추가 필드:
  - `bookmark_type` (string, enum: `favorite`,`hard`) [필수]

### 4.3 quiz_submitted
- 설명: 퀴즈 문항 제출 시 기록
- 추가 필드:
  - `quiz_type` (string, enum: `meaning`,`cloze`,`ordering`,`listening`) [필수]
  - `is_correct` (boolean) [필수]
  - `attempt_no` (integer, min:1) [필수]

### 4.4 srs_review_done
- 설명: 복습 카드 제출 시 기록
- 추가 필드:
  - `card_result` (string, enum: `again`,`hard`,`good`,`easy`) [필수]
  - `next_due_at` (string, ISO8601) [필수]

### 4.5 shadowing_recorded
- 설명: 쉐도잉 녹음 저장 시 기록
- 추가 필드:
  - `recording_sec` (number, >0) [필수]
  - `source_audio_sec` (number, >0) [필수]
  - `speed_ratio` (number, >0) [선택]
  - `retry_count` (integer, min:0) [선택]

### 4.6 subscription_started
- 설명: 유료 구독 시작 시 기록
- 추가 필드:
  - `plan_id` (string) [필수]
  - `billing_cycle` (string, enum: `monthly`,`yearly`) [필수]
  - `price` (number, >=0) [필수]
  - `currency` (string, ISO4217) [필수]

## 5) 서버 검증 규칙
- `event_id` 중복 수신 시 저장하지 않고 `duplicate`로 집계
- `occurred_at`이 서버 시간 기준 +5분 초과 미래면 `invalid_timestamp`
- `event_name` 미등록 값은 `unknown_event`로 격리 큐 전송
- 필수 필드 누락 이벤트는 `400` 반환 + 오류 코드/필드 목록 포함
- `user_id`, `session_id`가 공백 문자열이면 무효 처리

## 6) 저장 정책
- Raw 이벤트 원본 보존: 90일
- 집계 테이블 보존: 2년
- PII 포함 금지: 이름/이메일/전화번호 이벤트 페이로드 저장 금지

## 7) 품질 지표
- 수집 성공률: 99%+
- 중복률: 2% 이하
- 스키마 오류율: 1% 이하
- 이벤트 지연(ingest latency): p95 5초 이하

## 8) DoD 검증 기준 (T-20260219-003)
- 핵심 6개 이벤트 스키마 확정
- 서버 검증 규칙 문서화 완료
- 샘플 페이로드로 파서 검증 가능
- 클라이언트/QA가 참조 가능한 명세 파일 존재

## 9) 다음 액션
1. `api/events/openapi_events_v1.yaml` 기반 수집 엔드포인트 구현
2. QA용 유효/무효 샘플 페이로드 테스트 실행
3. 분석 테이블(`fact_learning_events`) 스키마 매핑 확정

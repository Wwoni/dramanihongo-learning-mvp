# Dashboard Spec Sprint 01

- 작성일: `2026-02-19`
- Owner: `A7_QA_Analytics`
- 관련 Task: `T-20260219-006`
- 상태: `Draft`

## 1) 목적
Sprint 01 MVP의 핵심 학습 퍼널, 이벤트 품질, 초기 리텐션을 모니터링하는 대시보드 요구사항 정의.

## 2) 데이터 소스
- 원본 이벤트: `POST /v1/events` 수집 로그
- 기준 스키마: `docs/event_schema_v1.md`
- 참조 이벤트:
  - `lesson_started`
  - `quiz_submitted`
  - `srs_review_done`
  - `shadowing_recorded`
  - `line_bookmarked`
  - `subscription_started`

## 3) 필수 위젯

### W1 Activation Funnel
- 지표:
  - `lesson_started` 유저 수
  - `quiz_submitted` 유저 수
  - `srs_review_done` 유저 수
  - `shadowing_recorded` 유저 수
- 목적: 첫 학습 루프 이탈 구간 파악

### W2 Completion Rate
- 지표:
  - 첫 학습 루프 완료율
  - 평균 완료 시간(분)
- 목표:
  - 완료율 80%+
  - 평균 15분 이내

### W3 Event Quality
- 지표:
  - 이벤트 수집 성공률
  - 스키마 오류율
  - 중복률
  - ingest latency(p95)

### W4 Learning Behavior
- 지표:
  - 평균 학습 카드 수
  - 퀴즈 정답률
  - 북마크 비율(`hard`/`favorite`)
  - 쉐도잉 평균 `speed_ratio`

### W5 Monetization Early Signal
- 지표:
  - `subscription_started` 수
  - 플랜별 전환 비율(monthly/yearly)

## 4) 필터
- 날짜(일/주)
- 플랫폼(iOS/Android/Web)
- user_level(N4/N3/N2)
- session_type(quick/deep)
- drama_id

## 5) KPI 알람 기준
- 이벤트 누락률 > 5%: 경고
- 스키마 오류율 > 1%: 경고
- 첫 학습 완료율 < 60%: 경고
- ingest latency p95 > 5초: 경고

## 6) 확인 쿼리 (의사 SQL)

```sql
-- 퍼널 단계별 유저 수
SELECT event_name, COUNT(DISTINCT user_id) AS users
FROM fact_learning_events
WHERE event_name IN ('lesson_started','quiz_submitted','srs_review_done','shadowing_recorded')
  AND event_date BETWEEN :from AND :to
GROUP BY event_name;
```

```sql
-- 퀴즈 정답률
SELECT
  SUM(CASE WHEN properties->>'is_correct' = 'true' THEN 1 ELSE 0 END)::float / COUNT(*) AS accuracy
FROM fact_learning_events
WHERE event_name = 'quiz_submitted'
  AND event_date BETWEEN :from AND :to;
```

```sql
-- 쉐도잉 평균 속도비
SELECT AVG((properties->>'speed_ratio')::float) AS avg_speed_ratio
FROM fact_learning_events
WHERE event_name = 'shadowing_recorded'
  AND event_date BETWEEN :from AND :to;
```

## 7) 완료 기준 (T-20260219-006)
- 대시보드 위젯/지표/필터 정의 완료
- 확인 쿼리 3종 이상 제공
- QA 시나리오 결과와 교차 검증 가능

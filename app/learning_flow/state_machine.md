# Learning Flow State Machine v1

- 작성일: `2026-02-19`
- 관련 Task: `T-20260219-004`

## 1) 상태 정의
- `INTRO`
- `LINE_STUDY`
- `QUIZ`
- `SRS`
- `SHADOWING`
- `SUMMARY`
- `INTERRUPTED` (중단 복귀용)

## 2) 전이 규칙
1. `INTRO -> LINE_STUDY`
   - 조건: Start 버튼 탭
2. `LINE_STUDY -> QUIZ`
   - 조건: studied_count >= 5
3. `QUIZ -> SRS`
   - 조건: quiz_submitted_count >= 5
4. `SRS -> SHADOWING`
   - 조건: srs_done_count >= 1
5. `SHADOWING -> SUMMARY`
   - 조건: shadowing_saved_count >= 1
6. `* -> INTERRUPTED`
   - 조건: 앱 종료/강제 백그라운드
7. `INTERRUPTED -> 이전 상태`
   - 조건: 세션 재개 성공

## 3) 차단 조건
- `LINE_STUDY`에서 카드 학습 수 미달 시 `QUIZ` 진입 불가
- `QUIZ` 제출 수 미달 시 `SRS` 진입 불가
- `SHADOWING` 저장 미완료 시 `SUMMARY` 진입 불가

## 4) 데이터 동기화
- 상태 전이마다 로컬 스냅샷 저장:
  - `session_id`, `current_state`, `counts`, `last_line_id`, `updated_at`
- 이벤트 전송은 비동기; 실패 시 재시도 큐에 저장

## 5) 의사코드
```text
if state == INTRO and action == start:
  state = LINE_STUDY
elif state == LINE_STUDY and studied_count >= 5:
  state = QUIZ
elif state == QUIZ and quiz_submitted_count >= 5:
  state = SRS
elif state == SRS and srs_done_count >= 1:
  state = SHADOWING
elif state == SHADOWING and shadowing_saved_count >= 1:
  state = SUMMARY
else:
  stay current state
```

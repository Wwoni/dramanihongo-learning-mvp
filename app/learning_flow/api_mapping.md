# Client Event API Mapping v1

- 작성일: `2026-02-19`
- 관련 Task: `T-20260219-004`, `T-20260219-003`

## 1) 엔드포인트
- `POST /v1/events`
- 명세: `api/events/openapi_events_v1.yaml`

## 2) 매핑 표
| 화면 ID | 사용자 액션 | 이벤트명 | 필수 properties |
|---|---|---|---|
| LF-001 | Start Lesson 탭 | lesson_started | session_type, entry_point |
| LF-002 | 북마크 탭 | line_bookmarked | bookmark_type |
| LF-003 | 퀴즈 제출 | quiz_submitted | quiz_type, is_correct, attempt_no |
| LF-004 | 복습 결과 선택 | srs_review_done | card_result, next_due_at |
| LF-005 | 녹음 저장 | shadowing_recorded | recording_sec, source_audio_sec |

## 3) 배치 전송 규칙
- 권장: 1~10개 이벤트 배치 전송
- 타임아웃: 3초
- 실패 시: 최대 5회 지수 백오프 재시도
- 앱 종료 시: 큐 flush 시도 후 종료

## 4) 클라이언트 검증
- `event_id`: UUID v4 생성
- `occurred_at`: UTC ISO8601
- 필수 필드 누락 시 전송 금지 + 로컬 에러 로그

## 5) 샘플 요청
```json
{
  "events": [
    {
      "event_id": "00000000-0000-4000-8000-000000000001",
      "event_name": "lesson_started",
      "occurred_at": "2026-02-19T09:00:00Z",
      "user_id": "u_123",
      "session_id": "s_abc",
      "user_level": "N3",
      "drama_id": "d_001",
      "app_version": "1.0.0",
      "platform": "ios",
      "properties": {
        "session_type": "quick",
        "entry_point": "home"
      }
    }
  ]
}
```

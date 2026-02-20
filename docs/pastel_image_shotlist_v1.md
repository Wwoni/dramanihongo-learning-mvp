# Pastel Image Shotlist v1

- 작성일: `2026-02-19`
- 목적: LF 단계별 1차 이미지 생성 대상(각 5장) 정의
- 기준: `docs/pastel_character_prompt_templates_v1.md`

| asset_id | flow_stage | topic_id | emotion_tag | prompt_template | status |
|---|---|---|---|---|---|
| IMG-LF001-001 | LF-001 | daily_convenience_store | neutral | Scene Intro | done |
| IMG-LF001-002 | LF-001 | daily_train_delay | urgent | Scene Intro | done |
| IMG-LF001-003 | LF-001 | daily_cafe_order | joy | Scene Intro | done |
| IMG-LF001-004 | LF-001 | daily_office_checkin | neutral | Scene Intro | done |
| IMG-LF001-005 | LF-001 | daily_weekend_trip | joy | Scene Intro | done |
| IMG-LF002-001 | LF-002 | daily_morning_greeting | joy | Line Study | done |
| IMG-LF002-002 | LF-002 | daily_rainy_day | sad | Line Study | done |
| IMG-LF002-003 | LF-002 | daily_roommate_talk | neutral | Line Study | done |
| IMG-LF002-004 | LF-002 | daily_study_group | neutral | Line Study | done |
| IMG-LF002-005 | LF-002 | daily_lost_and_found | urgent | Line Study | done |
| IMG-LF003-001A | LF-003 | daily_cafe_order | joy | Quiz Feedback (correct) | todo |
| IMG-LF003-001B | LF-003 | daily_cafe_order | neutral | Quiz Feedback (incorrect) | todo |
| IMG-LF003-002A | LF-003 | daily_bank_transfer | joy | Quiz Feedback (correct) | todo |
| IMG-LF003-002B | LF-003 | daily_bank_transfer | neutral | Quiz Feedback (incorrect) | todo |
| IMG-LF003-003A | LF-003 | daily_hospital_reception | joy | Quiz Feedback (correct) | todo |
| IMG-LF003-003B | LF-003 | daily_hospital_reception | neutral | Quiz Feedback (incorrect) | todo |
| IMG-LF003-004A | LF-003 | daily_online_shopping | joy | Quiz Feedback (correct) | todo |
| IMG-LF003-004B | LF-003 | daily_online_shopping | neutral | Quiz Feedback (incorrect) | todo |
| IMG-LF003-005A | LF-003 | daily_phone_battery | joy | Quiz Feedback (correct) | todo |
| IMG-LF003-005B | LF-003 | daily_phone_battery | neutral | Quiz Feedback (incorrect) | todo |
| IMG-LF006-001 | LF-006 | daily_convenience_store | joy | Session Summary | todo |
| IMG-LF006-002 | LF-006 | daily_office_checkin | joy | Session Summary | todo |
| IMG-LF006-003 | LF-006 | daily_study_group | joy | Session Summary | todo |
| IMG-LF006-004 | LF-006 | daily_family_call | joy | Session Summary | todo |
| IMG-LF006-005 | LF-006 | daily_weekend_trip | joy | Session Summary | todo |

## 우선순위
1. LF-001 5장
2. LF-002 5장
3. LF-003 10장(A/B)
4. LF-006 5장

## 생성 요청 문서
- `docs/pastel_image_generation_requests_lf001_v1.md`

## status 정의
- `todo`: 미착수
- `prompt_ready`: 프롬프트 확정, 생성 대기
- `generation_requested`: 생성 요청 제출, 결과 대기
- `generated_pending_review`: 이미지 생성 완료, 시각 검수 대기
- `generation_failed`: 생성 실패
- `done`: 이미지 생성/검수 완료

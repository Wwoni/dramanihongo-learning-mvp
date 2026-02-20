# Shadowing MVP Spec v1

- 문서 ID: `SHD-V1`
- 작성일: `2026-02-19`
- Owner: `A6_AI_Speech`
- 관련 Task: `T-20260219-005`
- 상태: `Draft`

## 1) 목적
사용자가 원문 대사를 따라 말하고, 길이/속도 기준의 즉시 피드백을 받아 반복 학습할 수 있는 쉐도잉 MVP를 정의한다.

## 2) 범위
- 포함:
  - 원문 오디오 재생
  - 사용자 녹음(최대 20초)
  - 재생 비교(원문 vs 내 녹음)
  - 기본 피드백(길이 비율, 속도 비율)
  - 이벤트 기록(`shadowing_recorded`)
- 제외:
  - 음소 단위 발음 채점
  - 억양/강세 정밀 분석

## 3) 사용자 플로우
1. 사용자가 대사 카드에서 `쉐도잉 시작`을 누른다.
2. 원문 오디오(3~10초)를 듣는다.
3. 녹음 시작/중지를 통해 내 발화를 저장한다.
4. 시스템이 길이/속도 지표를 계산한다.
5. 즉시 피드백 문구를 노출하고 재시도를 유도한다.

## 4) 입력/출력 정의
## 입력
- `line_id`
- `source_audio_url`
- `source_audio_sec`
- `recording_blob` (m4a/wav)

## 출력
- `recording_sec`
- `speed_ratio` = `recording_sec / source_audio_sec`
- `timing_grade` (enum: `good`,`fast`,`slow`)
- `feedback_text`

## 5) 피드백 규칙 (MVP)
- `0.9 <= speed_ratio <= 1.15` -> `good`
  - 피드백: "리듬이 좋아요. 한 번 더 또렷하게 말해보세요."
- `speed_ratio < 0.9` -> `fast`
  - 피드백: "조금 빨라요. 원문 속도에 맞춰 다시 시도해보세요."
- `speed_ratio > 1.15` -> `slow`
  - 피드백: "조금 느려요. 호흡을 짧게 끊어 말해보세요."

## 6) 기술 요구사항
- 녹음 포맷: 기본 `m4a` (fallback: `wav`)
- 샘플레이트: 16kHz 이상 권장
- 최대 녹음 길이: 20초
- 업로드 실패 시 로컬 임시 저장 후 재시도

## 7) 이벤트 연동
- 이벤트명: `shadowing_recorded`
- 필수 필드:
  - `recording_sec`
  - `source_audio_sec`
- 선택 필드:
  - `speed_ratio`
  - `retry_count`

## 8) 에러/예외 처리
- 마이크 권한 거부:
  - 권한 안내 모달 + 설정 이동
- 녹음 0초/손상 파일:
  - 저장 차단 + 재녹음 유도
- 오디오 재생 실패:
  - 텍스트 읽기 모드로 우회

## 9) DoD 검증 기준 (T-20260219-005)
- 녹음/저장/재생 동작
- 속도 비율 기반 피드백 3단계 동작
- 이벤트 전송 정상
- 내부 테스트 10회 중 실패율 10% 이하

## 10) 다음 액션
1. `prototype/shadowing/feedback_logic.md` 기반 클라이언트 구현
2. `A7_QA_Analytics`와 권한/실패 시나리오 테스트 추가
3. 차기 스프린트에서 발음 인식 PoC 범위 확정

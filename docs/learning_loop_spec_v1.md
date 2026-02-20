# Learning Loop Spec v1

- 문서 ID: `LL-V1`
- 작성일: `2026-02-19`
- Owner: `A3_Learning_Design`
- 관련 Task: `T-20260219-002`
- 상태: `Draft`

## 1) 목적
사용자가 10~15분 안에 `대사 이해 -> 퀴즈 -> 복습 등록 -> 쉐도잉`까지 완료하는 MVP 학습 루프를 정의한다.

## 2) 대상 사용자
- JLPT N4~N2
- 드라마 기반 학습 선호자
- 1회 학습 10~20분 선호 사용자

## 3) 세션 구조
- Quick(10분): 대사 5개
- Deep(20분): 대사 10개

세션 단계:
1. Scene Intro (맥락 설명 15~30초)
2. Line Study (대사 카드 학습)
3. Quiz Check (즉시 확인 퀴즈)
4. SRS Queue (복습 큐 적재)
5. Shadowing (녹음/비교)
6. Session Summary (완료/복습 예약)

## 4) 대사 카드 데이터 스키마 (MVP)
- `line_id` (string)
- `drama_id` (string)
- `episode_no` (int)
- `speaker` (string)
- `jp_text` (string)
- `jp_furigana` (string)
- `ko_translation` (string)
- `vocab[]` (array): 표제어, 뜻, 품사
- `grammar_points[]` (array): 문형, 레벨, 설명
- `audio_clip_url` (string)
- `difficulty` (enum: easy/normal/hard)
- `emotion_tag` (enum: neutral/joy/anger/sad/urgent)

## 5) 학습 단계 상세

### 5.1 Line Study
- 기본 표시: 일본어 + 후리가나
- 사용자 액션:
  - 탭 시 단어 뜻/문법 노출
  - A-B 반복 재생
  - 북마크/어려움 표시
- 규칙:
  - 최초에는 한국어 번역 숨김(옵션으로 표시)
  - 3초 이상 머문 카드만 학습 완료로 집계

### 5.2 Quiz Check (카드당 1문항)
- 유형 비율:
  - 의미 매칭 40%
  - 빈칸 완성 30%
  - 순서 배열 20%
  - 청해 선택 10%
- 채점:
  - 즉시 피드백
  - 오답은 자동으로 SRS 우선순위 상승

### 5.3 SRS Queue
- 초기 간격:
  - 정답: +1일
  - 오답: +10분 (세션 내 재노출)
- 2회 연속 정답 시:
  - +3일 -> +7일로 확장
- 실패 규칙:
  - 같은 카드 3회 오답 시 `hard` 태그 부여

### 5.4 Shadowing
- 카드 2개 이상에서 진행
- 기능:
  - 원문 오디오 재생
  - 사용자 녹음(최대 20초)
  - 길이/말속도 기반 간단 피드백
- 결과:
  - `shadowing_recorded` 이벤트 기록
  - 재시도 가능

## 6) 완료 기준 (사용자 관점)
- 아래 조건 충족 시 “오늘 학습 완료”:
  - 카드 학습 5개 이상
  - 퀴즈 제출 5회 이상
  - SRS 등록 1회 이상
  - 쉐도잉 1회 이상

## 7) 이벤트 매핑 (A5 연계)
- `lesson_started`: 세션 시작
- `line_studied`: 카드 학습 완료(3초 규칙 통과)
- `quiz_submitted`: 문항 제출
- `srs_review_done`: 복습 완료
- `shadowing_recorded`: 녹음 저장
- `lesson_completed`: 완료 조건 충족

공통 속성:
- `user_id`, `session_id`, `drama_id`, `line_id`, `user_level`, `duration_sec`, `timestamp`

## 8) UX 카피 가이드 (요약)
- 학습 유도 카피는 짧고 행동 중심
- 피드백 톤은 평가보다 개선 중심
- 예:
  - "핵심 표현 잡았어요. 다음 문장으로 가볼까요?"
  - "속도를 조금만 늦추면 더 또렷해져요."

## 9) 실패 시나리오 대응
- 네트워크 오류: 오프라인 캐시 카드 우선 제공
- 오디오 로딩 실패: 텍스트 학습만 진행 후 재시도 안내
- 퀴즈 중단: 마지막 카드 기준 자동 복귀

## 10) DoD 검증 기준 (T-20260219-002)
- 카드 스키마/학습 단계/완료 조건 정의 완료
- 이벤트 매핑이 분석 스키마와 충돌 없음
- Quick 세션 10분 내 완료 가능하도록 카드/퀴즈 볼륨 확정

## 11) 다음 액션
1. `A4_App_Client`에 화면 흐름 와이어 전달
2. `A5_Backend_Data`에 카드/이벤트 스키마 전달
3. 샘플 30개 대사로 파일럿 난이도 점검

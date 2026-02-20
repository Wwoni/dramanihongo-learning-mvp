# Learning Flow Module (T-20260219-004)

- 상태: `Draft Scaffold`
- 목적: 모바일 클라이언트의 첫 학습 루프 UI 구현 기준 제공
- 기준 문서:
  - `docs/learning_loop_spec_v1.md`
  - `docs/event_schema_v1.md`
  - `api/events/openapi_events_v1.yaml`

## 디렉토리 구성
- `screen_spec.md`: 화면별 UI/입력/검증/이벤트 요구사항
- `state_machine.md`: 화면 전이/예외 처리 규칙
- `api_mapping.md`: 클라이언트 이벤트 송신 매핑
- `acceptance_checklist.md`: 구현 완료 검증 체크리스트

## 구현 가이드
- 프레임워크(Flutter/React Native)는 추후 결정하되, 화면 ID/상태/이벤트 키는 본 문서 값을 고정 사용한다.
- 첫 목표는 신규 사용자의 15분 내 첫 학습 완료다.

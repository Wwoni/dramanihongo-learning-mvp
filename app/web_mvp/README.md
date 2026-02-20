# Web MVP (A4 Quick Build)

`LF-001 ~ LF-006` 흐름을 웹에서 바로 실행하기 위한 최소 MVP입니다.

## 실행 방법 (의존성 없음)
프로젝트 루트에서:

```bash
python3 -m http.server 5173
```

브라우저:
- `http://localhost:5173/app/web_mvp/`
- 캐시 이슈가 있으면 강력 새로고침(`Cmd+Shift+R`) 후 재시도

## QA 전달 항목
- `platform`: `web`
- `build_version`: 화면 우측 상단 값 (기본: `web-s1-20260219-01`)
- 실행 URL: `http://localhost:5173/app/web_mvp/`

## 포함 기능
- 학습 루프 화면 전환: `LF-001` -> `LF-006`
- 이벤트 로그 패널 (`lesson_started` ~ `subscription_started`)
- `qa/runtime_execution_evidence_s1.json` 입력용 JSON 미리보기/복사 버튼
- S1-04 테스트용 중단/복귀 체크포인트 저장/복원 버튼
- S1-05 테스트용 네트워크 OFFLINE 큐 적재/ONLINE 전송 버튼

## 제한 사항
- 현재는 로컬 이벤트 로그만 제공 (실제 `/v1/events` 전송 미연동)
- 오디오 녹음/결제 실제 연동 미포함

## S1-04 / S1-05 테스트 방법
1. `S1-04 (중단/복귀)`
- 임의 화면에서 `중단 상태 저장`
- 브라우저 새로고침
- `복귀 상태 불러오기`
- 로그에 `runtime_checkpoint_saved`, `runtime_checkpoint_restored` 확인

2. `S1-05 (네트워크 재시도)`
- `네트워크: OFFLINE`으로 전환
- 이벤트 버튼 클릭 (로그에 `queued_event` 발생)
- `네트워크: ONLINE` 전환 또는 `큐 강제 전송`
- 로그에 `delivered_from_queue: true` 확인

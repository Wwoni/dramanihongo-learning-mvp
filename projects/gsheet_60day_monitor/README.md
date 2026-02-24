# gsheet_60day_monitor

`data` 시트 조건 대상 행(A~J)을 `list` 시트에 `company_id(A열)` 기준으로 upsert 하는 자동화 스크립트입니다.

## 조건

- 기준일: `D`열
- 도달일: `I`열
- 포함 조건
  - `I`가 존재: `(I - D) > threshold_days`
  - `I`가 비어있음: `(오늘 - D) > threshold_days`
- 제외 조건
  - `i_min_date`가 설정되어 있고 `I < i_min_date`

## 동작

- `list` 1행 헤더를 `data` 1행(A1:J1)과 동기화 (`ensure_header=true`)
- 필터된 행을 `company_id` 기준으로 upsert
  - `list`에 같은 `company_id`가 있으면 해당 행 업데이트
  - 없으면 새 행 append
- 실행 결과를 JSON 로그로 저장
- 옵션으로 Slack 웹훅 알림 전송

## 설치

```bash
cd /Users/wonheelee/Documents/Cursor/projects/gsheet_60day_monitor
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 설정

```bash
cp config.example.json config.json
```

주요 필드:

- `spreadsheet_id`
- `source_sheet` (기본: `data`)
- `target_sheet` (기본: `list`)
- `source_range` (기본: `A2:J`)
- `target_range` (기본: `A:J`)
- `threshold_days` (기본: `60`)
- `ensure_header` (기본: `true`)
- `i_min_date` (예: `2026-01-01`)
- `upsert_by_company_id` (기본: `true`)

## 인증

### 서비스계정

```bash
export GOOGLE_SERVICE_ACCOUNT_JSON_PATH="/Users/wonheelee/Documents/Cursor/util/credentials/service-account.json"
```

### OAuth

```bash
python scripts/append_overdue_rows.py \
  --config config.json \
  --auth-mode oauth \
  --oauth-client-secrets oauth_client_secret.json \
  --dry-run --debug
```

## 실행

Dry-run:

```bash
python scripts/append_overdue_rows.py --config config.json --dry-run --debug
```

실행:

```bash
python scripts/append_overdue_rows.py --config config.json
```

로그 + Slack:

```bash
export GSHEET_MONITOR_SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
python scripts/append_overdue_rows.py --config config.json --notify-slack
```

## 로그

- 기본 저장 경로: `projects/gsheet_60day_monitor/logs/`
- 파일명: `run_YYYYMMDDTHHMMSSZ.json`

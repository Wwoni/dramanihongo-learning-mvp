#!/usr/bin/env python3
import argparse
import json
import os
import re
import traceback
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple
from urllib import request

from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials as UserCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


@dataclass
class Config:
    spreadsheet_id: str
    source_sheet: str
    target_sheet: str
    source_range: str
    target_range: str
    threshold_days: int
    ensure_header: bool
    i_min_date: Optional[date]
    upsert_by_company_id: bool


def load_config(path: str) -> Tuple[Config, Path]:
    config_path = resolve_config_path(path)
    with config_path.open("r", encoding="utf-8") as f:
        raw = json.load(f)
    config = Config(
        spreadsheet_id=extract_spreadsheet_id(raw["spreadsheet_id"]),
        source_sheet=raw.get("source_sheet", "data"),
        target_sheet=raw.get("target_sheet", "list"),
        source_range=raw.get("source_range", "A2:J"),
        target_range=raw.get("target_range", "A:J"),
        threshold_days=int(raw.get("threshold_days", 60)),
        ensure_header=bool(raw.get("ensure_header", True)),
        i_min_date=parse_optional_date(raw.get("i_min_date")),
        upsert_by_company_id=bool(raw.get("upsert_by_company_id", True)),
    )
    return config, config_path


def resolve_config_path(path: str) -> Path:
    requested = Path(path).expanduser()
    if requested.is_file():
        return requested

    script_dir = Path(__file__).resolve().parent
    candidates = [
        Path.cwd() / requested,
        script_dir / requested,
        script_dir.parent / requested,
    ]

    for candidate in candidates:
        if candidate.is_file():
            return candidate

    searched = [str(requested)] + [str(candidate) for candidate in candidates]
    raise FileNotFoundError(
        f"config file not found: {path}\nsearched paths:\n- " + "\n- ".join(searched)
    )


def load_credentials() -> Tuple[service_account.Credentials, str]:
    raw = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    source = "env:GOOGLE_SERVICE_ACCOUNT_JSON"
    if not raw:
        path_candidates = [
            os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON_PATH", "").strip(),
            str(Path(__file__).resolve().parents[3] / "util" / "credentials" / "service-account.json"),
        ]
        for path in path_candidates:
            if not path:
                continue
            candidate = Path(path).expanduser()
            if candidate.is_file():
                raw = candidate.read_text(encoding="utf-8")
                source = f"file:{candidate}"
                break

    if not raw:
        raise RuntimeError(
            "GOOGLE_SERVICE_ACCOUNT_JSON is not set. "
            "Set GOOGLE_SERVICE_ACCOUNT_JSON or GOOGLE_SERVICE_ACCOUNT_JSON_PATH."
        )

    try:
        info = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError("GOOGLE_SERVICE_ACCOUNT_JSON is not valid JSON") from exc

    creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    return creds, f"{source} ({info.get('client_email', 'unknown_email')})"


def load_oauth_credentials(
    client_secret_path: str,
    token_path: str,
) -> Tuple[UserCredentials, str]:
    secret_file = resolve_client_secret_path(client_secret_path)
    token_file = Path(token_path).expanduser()
    if not token_file.is_absolute():
        token_file = Path.cwd() / token_file

    creds: Optional[UserCredentials] = None
    if token_file.exists():
        creds = UserCredentials.from_authorized_user_file(str(token_file), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(secret_file), SCOPES)
            creds = flow.run_local_server(port=0)
        token_file.parent.mkdir(parents=True, exist_ok=True)
        token_file.write_text(creds.to_json(), encoding="utf-8")

    email = getattr(creds, "account", None) or "oauth_user"
    return creds, f"oauth:{secret_file} token:{token_file} ({email})"


def resolve_client_secret_path(path: str) -> Path:
    requested = Path(path).expanduser()
    script_dir = Path(__file__).resolve().parent
    candidates = [
        requested,
        Path.cwd() / requested,
        script_dir / requested,
        script_dir.parent / requested,
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate

    raise FileNotFoundError(
        "OAuth client secret not found. "
        "Set --oauth-client-secrets or GOOGLE_OAUTH_CLIENT_SECRET_PATH."
    )


def extract_spreadsheet_id(value: str) -> str:
    text = str(value).strip()
    match = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", text)
    if match:
        return match.group(1)
    return text


def normalize_row(row: Sequence[Any], width: int = 10) -> List[str]:
    values = [str(v).strip() if v is not None else "" for v in row]
    if len(values) < width:
        values.extend([""] * (width - len(values)))
    return values[:width]


def parse_sheet_date(value: str) -> Optional[date]:
    if not value:
        return None
    text = str(value).strip()
    if not text:
        return None

    formats = (
        "%Y-%m-%d",
        "%Y.%m.%d",
        "%Y/%m/%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y.%m.%d %H:%M:%S",
        "%Y/%m/%d %H:%M:%S",
    )
    for fmt in formats:
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue

    try:
        serial = float(text)
        base = date(1899, 12, 30)
        return base + timedelta(days=int(serial))
    except ValueError:
        return None


def parse_optional_date(value: Any) -> Optional[date]:
    if value is None:
        return None
    return parse_sheet_date(str(value))


def get_today_kst() -> date:
    try:
        from zoneinfo import ZoneInfo

        return datetime.now(ZoneInfo("Asia/Seoul")).date()
    except Exception:
        return datetime.utcnow().date()


def build_range(sheet: str, rng: str) -> str:
    return f"'{sheet}'!{rng}"


def fetch_values(svc, spreadsheet_id: str, range_name: str) -> List[List[Any]]:
    response = (
        svc.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=range_name)
        .execute()
    )
    return response.get("values", [])


def append_values(svc, spreadsheet_id: str, range_name: str, rows: List[List[str]]) -> int:
    if not rows:
        return 0
    response = (
        svc.spreadsheets()
        .values()
        .append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body={"values": rows},
        )
        .execute()
    )
    return int(response.get("updates", {}).get("updatedRows", 0))


def batch_update_rows(svc, spreadsheet_id: str, sheet_name: str, updates: List[Tuple[int, List[str]]]) -> int:
    if not updates:
        return 0
    data = []
    for row_num, row in updates:
        data.append({
            "range": build_range(sheet_name, f"A{row_num}:J{row_num}"),
            "values": [normalize_row(row, 10)],
        })
    svc.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={"valueInputOption": "RAW", "data": data},
    ).execute()
    return len(updates)


def get_sheet_id(svc, spreadsheet_id: str, sheet_title: str) -> int:
    response = (
        svc.spreadsheets()
        .get(
            spreadsheetId=spreadsheet_id,
            fields="sheets.properties(sheetId,title)",
        )
        .execute()
    )
    for sheet in response.get("sheets", []):
        props = sheet.get("properties", {})
        if props.get("title") == sheet_title:
            return int(props["sheetId"])
    raise RuntimeError(f"target sheet not found: {sheet_title}")


def insert_first_row(svc, spreadsheet_id: str, sheet_id: int) -> None:
    svc.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "requests": [
                {
                    "insertDimension": {
                        "range": {
                            "sheetId": sheet_id,
                            "dimension": "ROWS",
                            "startIndex": 0,
                            "endIndex": 1,
                        },
                        "inheritFromBefore": False,
                    }
                }
            ]
        },
    ).execute()


def update_header_row(svc, spreadsheet_id: str, target_sheet: str, header: List[str]) -> None:
    svc.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=build_range(target_sheet, "A1:J1"),
        valueInputOption="RAW",
        body={"values": [normalize_row(header, 10)]},
    ).execute()


def get_header_sync_plan(
    svc,
    spreadsheet_id: str,
    source_sheet: str,
    target_sheet: str,
) -> Dict[str, Any]:
    source_header_values = fetch_values(svc, spreadsheet_id, build_range(source_sheet, "A1:J1"))
    if not source_header_values:
        return {"action": "skip_no_source_header", "header": []}

    source_header = normalize_row(source_header_values[0], 10)
    if not any(source_header):
        return {"action": "skip_blank_source_header", "header": source_header}

    target_first_values = fetch_values(svc, spreadsheet_id, build_range(target_sheet, "A1:J1"))
    if not target_first_values:
        return {"action": "write_header_only", "header": source_header}

    target_first = normalize_row(target_first_values[0], 10)
    if target_first == source_header:
        return {"action": "already_synced", "header": source_header}

    if any(target_first):
        return {"action": "insert_then_write", "header": source_header}

    return {"action": "write_header_only", "header": source_header}


def apply_header_sync_plan(
    svc,
    spreadsheet_id: str,
    target_sheet: str,
    plan: Dict[str, Any],
) -> None:
    action = plan.get("action")
    header = plan.get("header", [])
    if action in {"already_synced", "skip_no_source_header", "skip_blank_source_header"}:
        return
    if action == "insert_then_write":
        target_sheet_id = get_sheet_id(svc, spreadsheet_id, target_sheet)
        insert_first_row(svc, spreadsheet_id, target_sheet_id)
    if action in {"insert_then_write", "write_header_only"}:
        update_header_row(svc, spreadsheet_id, target_sheet, header)


def collect_candidates(
    rows: List[List[Any]],
    threshold_days: int,
    today: date,
    i_min_date: Optional[date],
) -> Tuple[List[List[str]], Dict[str, int]]:
    counters = {
        "source_rows": 0,
        "invalid_d": 0,
        "excluded_old_i": 0,
        "overdue_with_i": 0,
        "overdue_without_i": 0,
    }
    out: List[List[str]] = []

    for raw in rows:
        counters["source_rows"] += 1
        row = normalize_row(raw, 10)
        d_date = parse_sheet_date(row[3])
        i_date = parse_sheet_date(row[8])

        if not d_date:
            counters["invalid_d"] += 1
            continue

        if i_date:
            if i_min_date and i_date < i_min_date:
                counters["excluded_old_i"] += 1
                continue
            if (i_date - d_date).days > threshold_days:
                counters["overdue_with_i"] += 1
                out.append(row)
            continue

        if (today - d_date).days > threshold_days:
            counters["overdue_without_i"] += 1
            out.append(row)

    return out, counters


def dedupe_candidates_by_company_id(candidates: List[List[str]]) -> Tuple[List[List[str]], int, int]:
    seen: set = set()
    deduped: List[List[str]] = []
    skipped_no_id = 0
    skipped_duplicate = 0

    for row in candidates:
        company_id = row[0].strip()
        if not company_id:
            skipped_no_id += 1
            continue
        if company_id in seen:
            skipped_duplicate += 1
            continue
        seen.add(company_id)
        deduped.append(row)

    return deduped, skipped_no_id, skipped_duplicate


def plan_upsert_by_company_id(
    candidates: List[List[str]],
    target_rows: List[List[Any]],
) -> Tuple[List[Tuple[int, List[str]]], List[List[str]], Dict[str, int]]:
    existing_map: Dict[str, int] = {}
    duplicate_key_in_target = 0

    for idx, raw in enumerate(target_rows, start=2):
        row = normalize_row(raw, 10)
        key = row[0].strip()
        if not key:
            continue
        if key in existing_map:
            duplicate_key_in_target += 1
            continue
        existing_map[key] = idx

    updates: List[Tuple[int, List[str]]] = []
    inserts: List[List[str]] = []

    for row in candidates:
        key = row[0].strip()
        target_row_num = existing_map.get(key)
        if target_row_num:
            updates.append((target_row_num, row))
        else:
            inserts.append(row)

    stats = {
        "target_duplicate_company_id": duplicate_key_in_target,
        "planned_updates": len(updates),
        "planned_inserts": len(inserts),
    }
    return updates, inserts, stats


def verify_spreadsheet_access(svc, spreadsheet_id: str) -> None:
    svc.spreadsheets().get(
        spreadsheetId=spreadsheet_id,
        fields="spreadsheetId,properties.title",
    ).execute()


def explain_http_error(exc: HttpError, spreadsheet_id: str, auth_mode: str) -> RuntimeError:
    status = getattr(exc.resp, "status", None)
    if status == 404:
        auth_hint = (
            "- 확인 2) OAuth 계정으로 해당 시트를 직접 열 수 있는지"
            if auth_mode == "oauth"
            else "- 확인 2) 해당 시트를 서비스계정 이메일에 공유했는지(Editor)"
        )
        return RuntimeError(
            "Google Sheets 404: spreadsheet not found.\n"
            f"- spreadsheet_id: {spreadsheet_id}\n"
            "- 확인 1) config의 spreadsheet_id가 정확한지\n"
            f"{auth_hint}\n"
            "- 확인 3) 현재 인증 정보가 의도한 계정인지"
        )
    if status == 403:
        return RuntimeError(
            "Google Sheets 403: permission denied.\n"
            f"- spreadsheet_id: {spreadsheet_id}\n"
            "- 서비스계정 이메일에 시트 공유 권한(Editor)을 부여하세요."
        )
    return RuntimeError(f"Google Sheets API error (status={status}): {exc}")


def write_run_log(log_dir: str, summary: Dict[str, Any]) -> Path:
    base = Path(log_dir).expanduser()
    if not base.is_absolute():
        base = Path.cwd() / base
    base.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    path = base / f"run_{ts}.json"
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def post_slack(text: str) -> bool:
    webhook = os.environ.get("GSHEET_MONITOR_SLACK_WEBHOOK_URL", "").strip()
    if not webhook:
        return False
    payload = json.dumps({"text": text}).encode("utf-8")
    req = request.Request(webhook, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    with request.urlopen(req, timeout=10) as resp:  # nosec B310
        return 200 <= resp.status < 300


def format_summary_text(summary: Dict[str, Any], success: bool) -> str:
    status = "SUCCESS" if success else "FAILED"
    return (
        f"[gsheet_60day_monitor] {status}\n"
        f"sheet={summary.get('spreadsheet_id')} tab={summary.get('target_sheet')}\n"
        f"dry_run={summary.get('dry_run')} auth={summary.get('auth_mode')}\n"
        f"source_rows={summary.get('source_rows')} candidates={summary.get('candidates')}\n"
        f"updates={summary.get('planned_updates')} inserts={summary.get('planned_inserts')}\n"
        f"excluded_old_i={summary.get('excluded_old_i')}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Upsert rows A:J into list when I date did not reach within threshold days from D date."
    )
    parser.add_argument(
        "--config",
        default=os.environ.get("SHEET_MONITOR_CONFIG", "config.json"),
        help="Path to config JSON (default: config.json or SHEET_MONITOR_CONFIG).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show result without writing to target sheet.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print resolved config/credential context for troubleshooting.",
    )
    parser.add_argument(
        "--auth-mode",
        choices=["service-account", "oauth"],
        default=os.environ.get("GOOGLE_AUTH_MODE", "service-account"),
        help="Auth mode: service-account or oauth (default: service-account).",
    )
    parser.add_argument(
        "--oauth-client-secrets",
        default=os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET_PATH", "oauth_client_secret.json"),
        help="OAuth client secret JSON path.",
    )
    parser.add_argument(
        "--oauth-token",
        default=os.environ.get("GOOGLE_OAUTH_TOKEN_PATH", ".oauth_token.json"),
        help="OAuth token cache path.",
    )
    parser.add_argument(
        "--log-dir",
        default=os.environ.get("GSHEET_MONITOR_LOG_DIR", "logs"),
        help="Directory for execution logs (default: logs).",
    )
    parser.add_argument(
        "--notify-slack",
        action="store_true",
        help="Post run summary to Slack when GSHEET_MONITOR_SLACK_WEBHOOK_URL is set.",
    )
    args = parser.parse_args()

    summary: Dict[str, Any] = {
        "dry_run": args.dry_run,
        "auth_mode": args.auth_mode,
        "run_at_utc": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }

    try:
        config, config_path = load_config(args.config)
        summary["config_path"] = str(config_path)
        summary["spreadsheet_id"] = config.spreadsheet_id
        summary["target_sheet"] = config.target_sheet

        if args.auth_mode == "oauth":
            creds, credential_source = load_oauth_credentials(
                client_secret_path=args.oauth_client_secrets,
                token_path=args.oauth_token,
            )
        else:
            creds, credential_source = load_credentials()

        sheets = build("sheets", "v4", credentials=creds, cache_discovery=False)
        today = get_today_kst()
        source_a1 = build_range(config.source_sheet, config.source_range)
        target_a1 = build_range(config.target_sheet, config.target_range)

        if args.debug:
            print(f"config_path={config_path}")
            print(f"auth_mode={args.auth_mode}")
            print(f"spreadsheet_id={config.spreadsheet_id}")
            print(f"credential_source={credential_source}")
            print(f"source_range={source_a1}")
            print(f"target_range={target_a1}")

        verify_spreadsheet_access(sheets, config.spreadsheet_id)

        header_plan = {"action": "disabled", "header": []}
        if config.ensure_header:
            header_plan = get_header_sync_plan(
                sheets,
                config.spreadsheet_id,
                config.source_sheet,
                config.target_sheet,
            )
        summary["header_action"] = header_plan.get("action")

        source_rows = fetch_values(sheets, config.spreadsheet_id, source_a1)
        candidates, counters = collect_candidates(
            source_rows,
            config.threshold_days,
            today,
            config.i_min_date,
        )
        deduped_candidates, skipped_no_id, skipped_dup_candidate = dedupe_candidates_by_company_id(candidates)

        if config.upsert_by_company_id:
            target_rows = fetch_values(sheets, config.spreadsheet_id, build_range(config.target_sheet, "A2:J"))
            updates, inserts, upsert_stats = plan_upsert_by_company_id(deduped_candidates, target_rows)
        else:
            updates, inserts = [], deduped_candidates
            upsert_stats = {
                "target_duplicate_company_id": 0,
                "planned_updates": 0,
                "planned_inserts": len(inserts),
            }

        summary.update(counters)
        summary.update(upsert_stats)
        summary["today"] = today.isoformat()
        summary["source_rows"] = counters["source_rows"]
        summary["candidates"] = len(candidates)
        summary["deduped_candidates"] = len(deduped_candidates)
        summary["skipped_no_company_id"] = skipped_no_id
        summary["skipped_duplicate_candidate_company_id"] = skipped_dup_candidate
        summary["planned_updates"] = len(updates)
        summary["planned_inserts"] = len(inserts)
        summary["to_write_total"] = len(updates) + len(inserts)

        if not args.dry_run:
            if config.ensure_header:
                apply_header_sync_plan(
                    sheets,
                    config.spreadsheet_id,
                    config.target_sheet,
                    header_plan,
                )
            updated_rows = batch_update_rows(
                sheets,
                config.spreadsheet_id,
                config.target_sheet,
                updates,
            )
            inserted_rows = append_values(
                sheets,
                config.spreadsheet_id,
                target_a1,
                inserts,
            )
            summary["updated_rows"] = updated_rows
            summary["inserted_rows"] = inserted_rows

        summary["status"] = "success"
        log_path = write_run_log(args.log_dir, summary)
        summary["log_path"] = str(log_path)

        print(f"today={summary['today']}")
        print(f"header_action={summary['header_action']}")
        print(f"source_rows={summary['source_rows']}")
        print(f"invalid_d={summary['invalid_d']}")
        print(f"excluded_old_i={summary['excluded_old_i']}")
        print(f"overdue_with_i={summary['overdue_with_i']}")
        print(f"overdue_without_i={summary['overdue_without_i']}")
        print(f"candidates={summary['candidates']}")
        print(f"deduped_candidates={summary['deduped_candidates']}")
        print(f"skipped_no_company_id={summary['skipped_no_company_id']}")
        print(f"target_duplicate_company_id={summary['target_duplicate_company_id']}")
        print(f"planned_updates={summary['planned_updates']}")
        print(f"planned_inserts={summary['planned_inserts']}")
        if args.dry_run:
            print("[DRY RUN] No rows written.")
        else:
            print(f"updated_rows={summary['updated_rows']}")
            print(f"inserted_rows={summary['inserted_rows']}")
        print(f"log_path={summary['log_path']}")

        if args.notify_slack:
            post_slack(format_summary_text(summary, success=True))

    except HttpError as exc:
        error = explain_http_error(exc, summary.get("spreadsheet_id", "unknown"), args.auth_mode)
        summary["status"] = "failed"
        summary["error"] = str(error)
        summary["traceback"] = traceback.format_exc()
        log_path = write_run_log(args.log_dir, summary)
        print(f"log_path={log_path}")
        if args.notify_slack:
            post_slack(format_summary_text(summary, success=False) + f"\nerror={error}")
        raise error from exc
    except Exception as exc:
        summary["status"] = "failed"
        summary["error"] = str(exc)
        summary["traceback"] = traceback.format_exc()
        log_path = write_run_log(args.log_dir, summary)
        print(f"log_path={log_path}")
        if args.notify_slack:
            post_slack(format_summary_text(summary, success=False) + f"\nerror={exc}")
        raise


if __name__ == "__main__":
    main()

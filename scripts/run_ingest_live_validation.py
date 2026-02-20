#!/usr/bin/env python3
"""
Live ingest validation for Sprint 01.

Uses real endpoint configuration from .env:
- INGEST_BASE_URL
- INGEST_EVENTS_PATH (default: /v1/events)
- INGEST_BEARER_TOKEN (optional)
- INGEST_TIMEOUT_SEC (default: 10)
"""

import datetime as dt
import json
import os
import pathlib
import urllib.error
import urllib.request
import uuid


ROOT = pathlib.Path(__file__).resolve().parents[1]
SAMPLE_PATH = ROOT / "api/events/sample_payloads_v1.json"
OUT_DIR = ROOT / "outputs/ingest"
OUT_JSON = OUT_DIR / "live_validation_results_s1.json"
OUT_MD = ROOT / "docs/ingest_live_test_results_s1.md"


def load_env(path: pathlib.Path):
    env = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        k, v = s.split("=", 1)
        env[k.strip()] = v.strip()
    return env


def now_utc():
    return dt.datetime.now(dt.timezone.utc)


def iso_utc(t):
    return t.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_event(event, minute_offset=-1):
    e = json.loads(json.dumps(event))
    e["event_id"] = str(uuid.uuid4())
    e["occurred_at"] = iso_utc(now_utc() + dt.timedelta(minutes=minute_offset))
    return e


def send_payload(url, payload, token, timeout_sec):
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    if token:
        req.add_header("Authorization", f"Bearer {token}")

    started = now_utc()
    try:
        with urllib.request.urlopen(req, timeout=timeout_sec) as res:
            latency_ms = int((now_utc() - started).total_seconds() * 1000)
            raw = res.read().decode("utf-8")
            parsed = None
            try:
                parsed = json.loads(raw) if raw else {}
            except json.JSONDecodeError:
                parsed = None
            return {
                "ok": True,
                "http_status": res.getcode(),
                "latency_ms": latency_ms,
                "body": parsed,
                "body_text": raw[:500],
                "error": None,
            }
    except urllib.error.HTTPError as e:
        latency_ms = int((now_utc() - started).total_seconds() * 1000)
        raw = e.read().decode("utf-8") if e.fp else ""
        parsed = None
        try:
            parsed = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            parsed = None
        return {
            "ok": False,
            "http_status": e.code,
            "latency_ms": latency_ms,
            "body": parsed,
            "body_text": raw[:500],
            "error": "http_error",
        }
    except Exception as e:
        latency_ms = int((now_utc() - started).total_seconds() * 1000)
        return {
            "ok": False,
            "http_status": None,
            "latency_ms": latency_ms,
            "body": None,
            "body_text": "",
            "error": str(e),
        }


def has_error_code(resp, expected_code):
    body = resp.get("body")
    if not isinstance(body, dict):
        return False
    if body.get("code") == expected_code:
        return True
    errors = body.get("errors", [])
    if isinstance(errors, list):
        for err in errors:
            if isinstance(err, dict) and err.get("code") == expected_code:
                return True
    return False


def eval_valid(resp):
    status_ok = resp["http_status"] in (200, 202)
    body = resp.get("body")
    rejected_zero = True
    if isinstance(body, dict) and "rejected" in body:
        rejected_zero = body.get("rejected", 1) == 0
    return status_ok and rejected_zero


def eval_negative(resp, expected_code):
    if resp["http_status"] == 400:
        return True
    body = resp.get("body")
    if isinstance(body, dict):
        rejected = body.get("rejected")
        if isinstance(rejected, int) and rejected >= 1:
            return True
    return has_error_code(resp, expected_code)


def build_negative_event(base_event, case_name):
    e = normalize_event(base_event)
    if case_name == "unknown_event":
        e["event_name"] = "unknown_event_name"
        return e
    if case_name == "invalid_timestamp":
        e["occurred_at"] = iso_utc(now_utc() + dt.timedelta(minutes=10))
        return e
    if case_name == "missing_required_common":
        e.pop("user_id", None)
        return e
    if case_name == "missing_event_properties":
        props = dict(e.get("properties", {}))
        props.pop("session_type", None)
        e["properties"] = props
        return e
    if case_name == "invalid_session_id":
        e["session_id"] = "   "
        return e
    return e


def write_markdown(report):
    md = [
        "# Ingest Live Test Results S1",
        "",
        f"- 작성일: {dt.date.today()}",
        "- 실행 스크립트: `scripts/run_ingest_live_validation.py`",
        "- 결과 JSON: `outputs/ingest/live_validation_results_s1.json`",
        "",
        "## 1) 실행 설정",
        f"- endpoint: `{report['config'].get('url', 'N/A')}`",
        f"- configured: `{report['config'].get('configured')}`",
        "",
    ]

    if report.get("status") == "blocked":
        md += [
            "## 2) 결과",
            "- 상태: `BLOCKED`",
            f"- 사유: `{report.get('reason', 'missing_configuration')}`",
            "",
            "## 3) 조치",
            "1. `.env`에 `INGEST_BASE_URL` 설정",
            "2. 필요 시 `INGEST_EVENTS_PATH`, `INGEST_BEARER_TOKEN` 설정",
            "3. 스크립트 재실행",
            "",
        ]
        OUT_MD.write_text("\n".join(md), encoding="utf-8")
        return

    md += [
        "## 2) Valid Cases",
        "| event_name | http | latency_ms | result |",
        "|---|---|---|---|",
    ]
    for r in report["valid_results"]:
        md.append(f"| {r['event_name']} | {r['http_status']} | {r['latency_ms']} | {'PASS' if r['pass'] else 'FAIL'} |")

    md += [
        "",
        "## 3) Negative Cases",
        "| case | expected_code | http | latency_ms | result |",
        "|---|---|---|---|---|",
    ]
    for r in report["negative_results"]:
        md.append(
            f"| {r['case']} | {r['expected_code']} | {r['http_status']} | {r['latency_ms']} | {'PASS' if r['pass'] else 'FAIL'} |"
        )

    md += [
        "",
        "## 4) Summary",
        f"- valid pass: {report['summary']['valid_pass']}/{report['summary']['valid_total']}",
        f"- negative pass: {report['summary']['negative_pass']}/{report['summary']['negative_total']}",
        f"- overall: {'PASS' if report['summary']['overall_pass'] else 'FAIL'}",
        "",
    ]
    OUT_MD.write_text("\n".join(md), encoding="utf-8")


def main():
    env = load_env(ROOT / ".env")
    base_url = os.getenv("INGEST_BASE_URL", env.get("INGEST_BASE_URL", "")).strip().rstrip("/")
    events_path = os.getenv("INGEST_EVENTS_PATH", env.get("INGEST_EVENTS_PATH", "/v1/events")).strip() or "/v1/events"
    token = os.getenv("INGEST_BEARER_TOKEN", env.get("INGEST_BEARER_TOKEN", "")).strip()
    timeout_sec = int(os.getenv("INGEST_TIMEOUT_SEC", env.get("INGEST_TIMEOUT_SEC", "10")))
    url = f"{base_url}{events_path}" if base_url else ""

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    report = {
        "run_at_utc": now_utc().isoformat(),
        "status": "ok",
        "config": {
            "configured": bool(base_url),
            "url": url if url else None,
            "has_bearer_token": bool(token),
            "timeout_sec": timeout_sec,
        },
        "valid_results": [],
        "negative_results": [],
        "summary": {},
    }

    if not base_url:
        report["status"] = "blocked"
        report["reason"] = "missing_ingest_base_url"
        report["summary"] = {
            "valid_total": 0,
            "valid_pass": 0,
            "negative_total": 0,
            "negative_pass": 0,
            "overall_pass": False,
        }
        OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        write_markdown(report)
        print("Wrote:", OUT_JSON)
        print("Wrote:", OUT_MD)
        return

    sample = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
    valid_events = [normalize_event(e, minute_offset=-1) for e in sample["events"]]

    valid_pass = 0
    for e in valid_events:
        resp = send_payload(url, {"events": [e]}, token, timeout_sec)
        passed = eval_valid(resp)
        if passed:
            valid_pass += 1
        report["valid_results"].append(
            {
                "event_id": e["event_id"],
                "event_name": e["event_name"],
                "http_status": resp["http_status"],
                "latency_ms": resp["latency_ms"],
                "pass": passed,
                "error": resp["error"],
            }
        )

    base_lesson = normalize_event(sample["events"][0], minute_offset=-1)
    duplicate_first = send_payload(url, {"events": [base_lesson]}, token, timeout_sec)
    duplicate_second = send_payload(url, {"events": [base_lesson]}, token, timeout_sec)
    dup_pass = eval_negative(duplicate_second, "duplicate")
    report["negative_results"].append(
        {
            "case": "duplicate_event_id",
            "expected_code": "duplicate",
            "http_status": duplicate_second["http_status"],
            "latency_ms": duplicate_second["latency_ms"],
            "pass": dup_pass,
            "first_try_http_status": duplicate_first["http_status"],
        }
    )

    negative_cases = [
        ("unknown_event", "unknown_event"),
        ("invalid_timestamp", "invalid_timestamp"),
        ("missing_required_common", "missing_required"),
        ("missing_event_properties", "missing_event_properties"),
        ("invalid_session_id", "invalid_session_id"),
    ]
    negative_pass = 1 if dup_pass else 0
    for case_name, expected_code in negative_cases:
        e = build_negative_event(sample["events"][0], case_name)
        resp = send_payload(url, {"events": [e]}, token, timeout_sec)
        passed = eval_negative(resp, expected_code)
        if passed:
            negative_pass += 1
        report["negative_results"].append(
            {
                "case": case_name,
                "expected_code": expected_code,
                "http_status": resp["http_status"],
                "latency_ms": resp["latency_ms"],
                "pass": passed,
                "error": resp["error"],
            }
        )

    valid_total = len(valid_events)
    negative_total = 1 + len(negative_cases)
    report["summary"] = {
        "valid_total": valid_total,
        "valid_pass": valid_pass,
        "negative_total": negative_total,
        "negative_pass": negative_pass,
        "overall_pass": (valid_pass == valid_total and negative_pass == negative_total),
    }

    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(report)
    print("Wrote:", OUT_JSON)
    print("Wrote:", OUT_MD)


if __name__ == "__main__":
    main()

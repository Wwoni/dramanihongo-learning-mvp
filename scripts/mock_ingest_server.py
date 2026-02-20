#!/usr/bin/env python3
"""
Local mock ingest server for Sprint 01 live validation.

Usage:
  python3 scripts/mock_ingest_server.py
"""

import datetime as dt
import json
import pathlib
from http.server import BaseHTTPRequestHandler, HTTPServer


HOST = "127.0.0.1"
PORT = 8787
PATH = "/v1/events"

ALLOWED_EVENTS = {
    "lesson_started",
    "line_bookmarked",
    "quiz_submitted",
    "srs_review_done",
    "shadowing_recorded",
    "subscription_started",
}

COMMON_REQUIRED = {
    "event_id",
    "event_name",
    "occurred_at",
    "user_id",
    "session_id",
    "user_level",
    "app_version",
    "platform",
}

EVENT_PROPERTIES_REQUIRED = {
    "lesson_started": {"session_type"},
    "line_bookmarked": {"bookmark_type"},
    "quiz_submitted": {"quiz_type", "is_correct", "attempt_no"},
    "srs_review_done": {"card_result", "next_due_at"},
    "shadowing_recorded": {"recording_sec", "source_audio_sec"},
    "subscription_started": {"plan_id", "billing_cycle", "price", "currency"},
}

SEEN_EVENT_IDS = set()
ROOT = pathlib.Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "outputs" / "ingest"
ACCEPTED_LOG_PATH = LOG_DIR / "mock_accepted_events.jsonl"
REJECTED_LOG_PATH = LOG_DIR / "mock_rejected_events.jsonl"


def ensure_log_dir():
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def write_jsonl(path: pathlib.Path, obj: dict):
    ensure_log_dir()
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def load_jsonl(path: pathlib.Path):
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s:
            continue
        try:
            rows.append(json.loads(s))
        except Exception:
            continue
    return rows


def build_stats():
    accepted = load_jsonl(ACCEPTED_LOG_PATH)
    rejected = load_jsonl(REJECTED_LOG_PATH)
    by_event = {}
    for row in accepted:
        name = row.get("event_name", "unknown")
        by_event[name] = by_event.get(name, 0) + 1
    by_error = {}
    for row in rejected:
        code = row.get("code", "unknown")
        by_error[code] = by_error.get(code, 0) + 1
    return {
        "accepted_total": len(accepted),
        "rejected_total": len(rejected),
        "accepted_by_event": by_event,
        "rejected_by_code": by_error,
    }


def now_utc():
    return dt.datetime.now(dt.timezone.utc)


def parse_iso(s: str):
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    return dt.datetime.fromisoformat(s)


def validate_event(event):
    eid = event.get("event_id")
    if eid in SEEN_EVENT_IDS:
        return False, "duplicate"
    SEEN_EVENT_IDS.add(eid)

    missing = [k for k in COMMON_REQUIRED if k not in event]
    if missing:
        return False, "missing_required"

    name = event.get("event_name")
    if name not in ALLOWED_EVENTS:
        return False, "unknown_event"

    try:
        occurred = parse_iso(event["occurred_at"])
    except Exception:
        return False, "invalid_timestamp"
    if occurred > now_utc() + dt.timedelta(minutes=5):
        return False, "invalid_timestamp"

    if str(event.get("user_id", "")).strip() == "":
        return False, "invalid_user_id"
    if str(event.get("session_id", "")).strip() == "":
        return False, "invalid_session_id"

    props = event.get("properties", {})
    req_props = EVENT_PROPERTIES_REQUIRED.get(name, set())
    miss_props = [k for k in req_props if k not in props]
    if miss_props:
        return False, "missing_event_properties"

    return True, "accepted"


class Handler(BaseHTTPRequestHandler):
    def _json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):  # noqa: N802
        if self.path == "/health":
            self._json(200, {"status": "ok", "service": "mock_ingest_server"})
            return

        if self.path.startswith("/v1/events/stats"):
            self._json(200, build_stats())
            return

        if self.path.startswith("/v1/events/logs"):
            accepted = load_jsonl(ACCEPTED_LOG_PATH)
            rejected = load_jsonl(REJECTED_LOG_PATH)
            self._json(
                200,
                {
                    "accepted_count": len(accepted),
                    "rejected_count": len(rejected),
                    "accepted_last_20": accepted[-20:],
                    "rejected_last_20": rejected[-20:],
                },
            )
            return

        self._json(404, {"code": "not_found", "message": "Not found"})

    def do_POST(self):  # noqa: N802
        if self.path != PATH:
            self._json(404, {"code": "not_found", "message": "Not found"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8")
            payload = json.loads(raw or "{}")
        except Exception:
            self._json(400, {"code": "invalid_json", "message": "Invalid JSON"})
            return

        events = payload.get("events")
        if not isinstance(events, list) or len(events) == 0:
            self._json(400, {"code": "missing_required", "message": "events array required"})
            return

        accepted = 0
        rejected = 0
        errors = []
        for event in events:
            ok, code = validate_event(event)
            if ok:
                accepted += 1
                write_jsonl(
                    ACCEPTED_LOG_PATH,
                    {
                        "logged_at": now_utc().isoformat(),
                        "event_id": event.get("event_id"),
                        "event_name": event.get("event_name"),
                        "occurred_at": event.get("occurred_at"),
                        "user_id": event.get("user_id"),
                        "platform": event.get("platform"),
                        "app_version": event.get("app_version"),
                        "properties": event.get("properties", {}),
                    },
                )
            else:
                rejected += 1
                err = {
                    "event_id": event.get("event_id", ""),
                    "code": code,
                    "message": code,
                }
                errors.append(err)
                write_jsonl(
                    REJECTED_LOG_PATH,
                    {
                        "logged_at": now_utc().isoformat(),
                        "event_id": event.get("event_id"),
                        "event_name": event.get("event_name"),
                        "occurred_at": event.get("occurred_at"),
                        "code": code,
                        "payload": event,
                    },
                )

        if rejected > 0 and accepted == 0:
            self._json(400, {"code": errors[0]["code"], "message": errors[0]["message"], "errors": errors})
            return

        self._json(202, {"accepted": accepted, "rejected": rejected, "errors": errors})

    def log_message(self, fmt, *args):
        return


def main():
    ensure_log_dir()
    server = HTTPServer((HOST, PORT), Handler)
    print(f"Mock ingest server listening on http://{HOST}:{PORT}{PATH}")
    print(f"- health: http://{HOST}:{PORT}/health")
    print(f"- stats : http://{HOST}:{PORT}/v1/events/stats")
    print(f"- logs  : http://{HOST}:{PORT}/v1/events/logs")
    print(f"- accepted log: {ACCEPTED_LOG_PATH}")
    print(f"- rejected log: {REJECTED_LOG_PATH}")
    server.serve_forever()


if __name__ == "__main__":
    main()

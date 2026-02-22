#!/usr/bin/env python3
"""
Production-oriented ingest API service (FastAPI).

Endpoints:
- GET  /health
- POST /v1/events
- GET  /v1/events/stats
- GET  /v1/events/logs?limit=50
"""

import datetime as dt
import json
import pathlib
from typing import Any, Dict, List, Optional, Tuple

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


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

ROOT = pathlib.Path(__file__).resolve().parents[2]
LOG_DIR = ROOT / "outputs" / "ingest_api"
ACCEPTED_LOG_PATH = LOG_DIR / "accepted_events.jsonl"
REJECTED_LOG_PATH = LOG_DIR / "rejected_events.jsonl"

SEEN_EVENT_IDS = set()


class Event(BaseModel):
    event_id: str
    event_name: str
    occurred_at: str
    user_id: str
    session_id: str
    user_level: str
    app_version: str
    platform: str
    drama_id: Optional[str] = None
    line_id: Optional[str] = None
    duration_sec: Optional[float] = None
    locale: Optional[str] = None
    properties: Dict[str, Any] = Field(default_factory=dict)


class EventsPayload(BaseModel):
    events: List[Event]


def now_utc() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def parse_iso(s: str) -> dt.datetime:
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    return dt.datetime.fromisoformat(s)


def ensure_log_dir() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def write_jsonl(path: pathlib.Path, obj: Dict[str, Any]) -> None:
    ensure_log_dir()
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def load_jsonl(path: pathlib.Path) -> List[Dict[str, Any]]:
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


def validate_event(event: Dict[str, Any]) -> Tuple[bool, str]:
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
        occurred = parse_iso(str(event.get("occurred_at")))
    except Exception:
        return False, "invalid_timestamp"
    if occurred > now_utc() + dt.timedelta(minutes=5):
        return False, "invalid_timestamp"

    if str(event.get("user_id", "")).strip() == "":
        return False, "invalid_user_id"
    if str(event.get("session_id", "")).strip() == "":
        return False, "invalid_session_id"

    props = event.get("properties", {}) or {}
    req_props = EVENT_PROPERTIES_REQUIRED.get(name, set())
    miss_props = [k for k in req_props if k not in props]
    if miss_props:
        return False, "missing_event_properties"

    return True, "accepted"


def build_stats() -> Dict[str, Any]:
    accepted = load_jsonl(ACCEPTED_LOG_PATH)
    rejected = load_jsonl(REJECTED_LOG_PATH)
    by_event: Dict[str, int] = {}
    by_error: Dict[str, int] = {}
    for row in accepted:
        n = row.get("event_name", "unknown")
        by_event[n] = by_event.get(n, 0) + 1
    for row in rejected:
        c = row.get("code", "unknown")
        by_error[c] = by_error.get(c, 0) + 1
    return {
        "accepted_total": len(accepted),
        "rejected_total": len(rejected),
        "accepted_by_event": by_event,
        "rejected_by_code": by_error,
    }


app = FastAPI(title="DramaNihongo Ingest API", version="0.1.0")


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "service": "ingest_api"}


@app.post("/v1/events")
def ingest_events(payload: EventsPayload) -> Dict[str, Any]:
    accepted = 0
    rejected = 0
    errors = []

    for event_model in payload.events:
        event = event_model.dict() if hasattr(event_model, "dict") else event_model.model_dump()
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
        # keep compatibility with validation script accepting 400 for invalid payload/event
        return JSONResponse(status_code=400, content={"code": errors[0]["code"], "message": errors[0]["message"], "errors": errors})

    return {"accepted": accepted, "rejected": rejected, "errors": errors}


@app.get("/v1/events/stats")
def events_stats() -> Dict[str, Any]:
    return build_stats()


@app.get("/v1/events/logs")
def events_logs(limit: int = Query(50, ge=1, le=200)) -> Dict[str, Any]:
    accepted = load_jsonl(ACCEPTED_LOG_PATH)
    rejected = load_jsonl(REJECTED_LOG_PATH)
    return {
        "accepted_count": len(accepted),
        "rejected_count": len(rejected),
        "accepted_last": accepted[-limit:],
        "rejected_last": rejected[-limit:],
    }

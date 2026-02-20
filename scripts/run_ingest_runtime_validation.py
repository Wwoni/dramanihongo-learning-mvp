#!/usr/bin/env python3
"""
Runtime-like validation harness for event ingest rules in Sprint 01.

This does not call a live API server. It executes the same validation rules
defined in docs/event_schema_v1.md and outputs a reproducible report.
"""

import datetime as dt
import json
import pathlib
from typing import Dict, List, Tuple


ROOT = pathlib.Path(__file__).resolve().parents[1]
SAMPLE_PATH = ROOT / "api/events/sample_payloads_v1.json"
OUT_DIR = ROOT / "outputs/ingest"
OUT_JSON = OUT_DIR / "runtime_validation_results_s1.json"
OUT_MD = ROOT / "docs/ingest_runtime_test_results_s1.md"

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


def now_utc():
    return dt.datetime.now(dt.timezone.utc)


def parse_iso(s: str):
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    return dt.datetime.fromisoformat(s)


def validate_event(event: Dict, seen_ids: set) -> Tuple[bool, str]:
    # duplicate check
    eid = event.get("event_id")
    if eid in seen_ids:
        return False, "duplicate"
    seen_ids.add(eid)

    # common required fields
    missing = [k for k in COMMON_REQUIRED if k not in event]
    if missing:
        return False, f"missing_required:{','.join(sorted(missing))}"

    # known event
    name = event.get("event_name")
    if name not in ALLOWED_EVENTS:
        return False, "unknown_event"

    # timestamp +5 min rule
    try:
        occurred = parse_iso(event["occurred_at"])
    except Exception:
        return False, "invalid_timestamp_format"
    if occurred > now_utc() + dt.timedelta(minutes=5):
        return False, "invalid_timestamp"

    # empty user/session
    if str(event.get("user_id", "")).strip() == "":
        return False, "invalid_user_id"
    if str(event.get("session_id", "")).strip() == "":
        return False, "invalid_session_id"

    # event-specific properties
    props = event.get("properties", {})
    req_props = EVENT_PROPERTIES_REQUIRED.get(name, set())
    miss_props = [k for k in req_props if k not in props]
    if miss_props:
        return False, f"missing_event_properties:{','.join(sorted(miss_props))}"

    return True, "accepted"


def build_negative_cases(valid_event: Dict) -> List[Dict]:
    base = dict(valid_event)
    cases = []

    # duplicate event_id (same as base)
    dup = dict(base)
    cases.append({"name": "duplicate_event_id", "event": dup})

    # unknown event
    unknown = dict(base)
    unknown["event_id"] = "00000000-0000-4000-8000-999999999991"
    unknown["event_name"] = "unknown_event_name"
    cases.append({"name": "unknown_event", "event": unknown})

    # future timestamp (+10min)
    future = dict(base)
    future["event_id"] = "00000000-0000-4000-8000-999999999992"
    future["occurred_at"] = (now_utc() + dt.timedelta(minutes=10)).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    cases.append({"name": "invalid_timestamp", "event": future})

    # missing required common field
    missing_common = dict(base)
    missing_common["event_id"] = "00000000-0000-4000-8000-999999999993"
    missing_common.pop("user_id", None)
    cases.append({"name": "missing_required_common", "event": missing_common})

    # missing event property
    missing_prop = dict(base)
    missing_prop["event_id"] = "00000000-0000-4000-8000-999999999994"
    props = dict(missing_prop.get("properties", {}))
    props.pop("session_type", None)
    missing_prop["properties"] = props
    cases.append({"name": "missing_event_properties", "event": missing_prop})

    # empty session_id
    empty_session = dict(base)
    empty_session["event_id"] = "00000000-0000-4000-8000-999999999995"
    empty_session["session_id"] = "   "
    cases.append({"name": "invalid_session_id", "event": empty_session})

    return cases


def main():
    sample = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
    # Normalize sample timestamps for deterministic valid-suite checks.
    valid_events = []
    base_time = (now_utc() - dt.timedelta(minutes=1)).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    for e in sample["events"]:
        ee = dict(e)
        ee["occurred_at"] = base_time
        valid_events.append(ee)
    seen = set()

    valid_results = []
    accepted = 0
    rejected = 0

    for ev in valid_events:
        ok, code = validate_event(ev, seen)
        valid_results.append({"event_id": ev["event_id"], "event_name": ev["event_name"], "ok": ok, "code": code})
        if ok:
            accepted += 1
        else:
            rejected += 1

    # Negative suite based on normalized lesson_started shape
    seen_neg = {valid_events[0]["event_id"]}
    negative_cases = build_negative_cases(valid_events[0])
    neg_results = []
    for c in negative_cases:
        ok, code = validate_event(c["event"], seen_neg)
        neg_results.append({"case": c["name"], "ok": ok, "code": code})

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    result_obj = {
        "run_at_utc": now_utc().isoformat(),
        "valid_suite": {
            "total": len(valid_events),
            "accepted": accepted,
            "rejected": rejected,
            "details": valid_results,
        },
        "negative_suite": {
            "total": len(negative_cases),
            "details": neg_results,
        },
    }
    OUT_JSON.write_text(json.dumps(result_obj, ensure_ascii=False, indent=2), encoding="utf-8")

    md = f"""# Ingest Runtime Test Results S1

- 작성일: 2026-02-19
- 실행 스크립트: `scripts/run_ingest_runtime_validation.py`
- 결과 JSON: `outputs/ingest/runtime_validation_results_s1.json`
- 범위: 이벤트 검증 규칙 런타임 유사 테스트 (로컬 하네스)

## 1) Valid Suite
- total: {len(valid_events)}
- accepted: {accepted}
- rejected: {rejected}

## 2) Negative Suite
- total: {len(negative_cases)}
- 기대: 모두 reject

| case | result | code |
|---|---|---|
"""
    for n in neg_results:
        md += f"| {n['case']} | {'PASS' if not n['ok'] else 'FAIL'} | {n['code']} |\n"

    md += """
## 3) 참고
- 본 결과는 API 서버 런타임 대체 검증이며, 실제 endpoint 통신 테스트는 별도 필요.
"""
    OUT_MD.write_text(md, encoding="utf-8")
    print("Wrote:", OUT_JSON)
    print("Wrote:", OUT_MD)


if __name__ == "__main__":
    main()

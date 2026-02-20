#!/usr/bin/env python3
"""
Builds a single control-tower status board for sub-agent execution.
"""

import json
import pathlib
from datetime import datetime, timezone


ROOT = pathlib.Path(__file__).resolve().parents[1]
STATUS_DIR = ROOT / "ops" / "subagents" / "status"
OUT_MD = ROOT / "docs" / "subagent_control_tower_20260220.md"
OUT_JSON = ROOT / "outputs" / "qa" / "subagent_control_tower_20260220.json"


def load_json(path: pathlib.Path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


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


def main():
    env = load_env(ROOT / ".env")
    files = sorted(STATUS_DIR.glob("*.json"))
    items = []
    for f in files:
        obj = load_json(f)
        if obj:
            items.append(obj)

    ingest_set = bool(env.get("INGEST_BASE_URL", "").strip())
    for item in items:
        if item.get("task_id") == "T-20260220-INGEST-ENDPOINT":
            item.setdefault("evidence", {})
            item["evidence"]["ingest_base_url_set"] = ingest_set
            if ingest_set and "INGEST_BASE_URL missing" in item.get("blockers", []):
                item["blockers"] = [b for b in item["blockers"] if b != "INGEST_BASE_URL missing"]

    summary = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "total": len(items),
        "pending": sum(1 for i in items if i.get("status") == "pending"),
        "in_progress": sum(1 for i in items if i.get("status") == "in_progress"),
        "completed": sum(1 for i in items if i.get("status") == "completed"),
        "ingest_base_url_set": ingest_set,
        "items": items,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    md = [
        "# Subagent Control Tower (2026-02-20)",
        "",
        f"- generated_at_utc: `{summary['generated_at_utc']}`",
        f"- ingest_base_url_set: `{summary['ingest_base_url_set']}`",
        "",
        "## 1) Summary",
        f"- total: `{summary['total']}`",
        f"- pending: `{summary['pending']}`",
        f"- in_progress: `{summary['in_progress']}`",
        f"- completed: `{summary['completed']}`",
        "",
        "## 2) Task Board",
        "| task_id | owner | status | blockers |",
        "|---|---|---|---|",
    ]
    for i in items:
        blockers = ", ".join(i.get("blockers", [])) or "-"
        md.append(f"| {i.get('task_id')} | {i.get('owner')} | {i.get('status')} | {blockers} |")

    md += [
        "",
        "## 3) Work Orders",
        "- `ops/subagents/work_orders/A4_STREAMLIT_CLOUD_DEPLOY.md`",
        "- `ops/subagents/work_orders/A5_INGEST_ENDPOINT_FINALIZE.md`",
        "- `ops/subagents/work_orders/A7_FINAL_GATE_CLOSE.md`",
    ]
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    print("Wrote:", OUT_JSON)
    print("Wrote:", OUT_MD)


if __name__ == "__main__":
    main()

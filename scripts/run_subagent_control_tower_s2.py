#!/usr/bin/env python3
"""
Sprint 02 subagent control tower builder.
"""

import json
import pathlib
from datetime import datetime, timezone


ROOT = pathlib.Path(__file__).resolve().parents[1]
STATUS_DIR = ROOT / "ops" / "subagents" / "sprint_02" / "status"
OUT_MD = ROOT / "docs" / "subagent_control_tower_s2_20260223.md"
OUT_JSON = ROOT / "outputs" / "qa" / "subagent_control_tower_s2_20260223.json"


def load_json(path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    items = []
    for f in sorted(STATUS_DIR.glob("*.json")):
        obj = load_json(f)
        if obj:
            items.append(obj)

    summary = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "total": len(items),
        "pending": sum(1 for i in items if i.get("status") == "pending"),
        "in_progress": sum(1 for i in items if i.get("status") == "in_progress"),
        "completed": sum(1 for i in items if i.get("status") == "completed"),
        "items": items,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    md = [
        "# Subagent Control Tower S2 (2026-02-23)",
        "",
        f"- generated_at_utc: `{summary['generated_at_utc']}`",
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

    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    print("Wrote:", OUT_JSON)
    print("Wrote:", OUT_MD)


if __name__ == "__main__":
    main()

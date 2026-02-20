#!/usr/bin/env python3
"""
Update subagent status JSON files safely.

Examples:
  python3 scripts/update_subagent_status.py --agent a4 --status completed \
    --evidence-json '{"streamlit_url":"https://demo.streamlit.app","deploy_log_note":"ok"}'
"""

import argparse
import json
import pathlib
from datetime import datetime, timezone


ROOT = pathlib.Path(__file__).resolve().parents[1]
STATUS_MAP = {
    "a4": ROOT / "ops/subagents/status/a4_streamlit_deploy_status.json",
    "a5": ROOT / "ops/subagents/status/a5_ingest_endpoint_status.json",
    "a7": ROOT / "ops/subagents/status/a7_final_gate_status.json",
}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--agent", choices=["a4", "a5", "a7"], required=True)
    p.add_argument("--status", choices=["pending", "in_progress", "completed"], required=True)
    p.add_argument("--evidence-json", default=None, help="JSON object to merge into evidence")
    p.add_argument("--blocker", action="append", default=[], help="Add blocker (repeatable)")
    p.add_argument("--clear-blockers", action="store_true")
    args = p.parse_args()

    path = STATUS_MAP[args.agent]
    data = json.loads(path.read_text(encoding="utf-8"))

    data["status"] = args.status
    data["updated_at_utc"] = datetime.now(timezone.utc).isoformat()

    if args.evidence_json:
        patch = json.loads(args.evidence_json)
        if not isinstance(patch, dict):
            raise ValueError("--evidence-json must be a JSON object")
        data.setdefault("evidence", {})
        data["evidence"].update(patch)

    if args.clear_blockers:
        data["blockers"] = []
    if args.blocker:
        data.setdefault("blockers", [])
        existing = set(data["blockers"])
        for b in args.blocker:
            if b not in existing:
                data["blockers"].append(b)

    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated:", path)


if __name__ == "__main__":
    main()

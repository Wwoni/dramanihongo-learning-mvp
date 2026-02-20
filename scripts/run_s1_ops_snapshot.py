#!/usr/bin/env python3
"""
Generate Sprint 01 operations snapshot from current artifacts.
"""

import json
import pathlib
from datetime import datetime, timezone


ROOT = pathlib.Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"
LIVE_PATH = ROOT / "outputs/ingest/live_validation_results_s1.json"
GATE_PATH = ROOT / "outputs/qa/runtime_gate_results_s1.json"
EVIDENCE_PATH = ROOT / "qa/runtime_execution_evidence_s1.json"
OUT_MD = ROOT / "docs/ops_snapshot_s1.md"
OUT_JSON = ROOT / "outputs/qa/ops_snapshot_s1.json"


def load_json(path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def load_env(path):
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
    env = load_env(ENV_PATH)
    live = load_json(LIVE_PATH)
    gate = load_json(GATE_PATH)
    evidence = load_json(EVIDENCE_PATH)

    ingest_configured = bool(env.get("INGEST_BASE_URL", ""))
    live_pass = bool((live or {}).get("summary", {}).get("overall_pass"))
    gate_name = (gate or {}).get("gate", "NO-DATA")
    gate_pass = bool((gate or {}).get("overall_pass"))

    scenarios_pass = (gate or {}).get("checks", {}).get("runtime_scenarios", {}).get("scenarios_pass")
    scenarios_total = (gate or {}).get("checks", {}).get("runtime_scenarios", {}).get("scenarios_total")
    p0_open_count = (gate or {}).get("checks", {}).get("runtime_scenarios", {}).get("p0_open_count")

    next_priority = []
    if not ingest_configured:
        next_priority.append("A5_Backend_Data: set INGEST_BASE_URL and run ingest live validation against staging/prod")
    if not gate_pass:
        next_priority.append("A7_QA_Analytics: update runtime evidence JSON and rerun runtime gate")
    if gate_pass:
        next_priority.append("Main Agent: refresh Sprint board/review and make final release decision after ingest production check")

    result = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "ingest_base_url_configured": ingest_configured,
        "live_validation_overall_pass": live_pass,
        "runtime_gate": gate_name,
        "runtime_gate_overall_pass": gate_pass,
        "runtime_scenarios_pass": scenarios_pass,
        "runtime_scenarios_total": scenarios_total,
        "p0_open_count": p0_open_count,
        "runtime_evidence_present": evidence is not None,
        "next_priority": next_priority,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    md = [
        "# Ops Snapshot S1",
        "",
        f"- Generated at (UTC): `{result['generated_at_utc']}`",
        "",
        "## 1) Status",
        f"- ingest base url configured: `{result['ingest_base_url_configured']}`",
        f"- ingest live validation pass: `{result['live_validation_overall_pass']}`",
        f"- runtime gate: `{result['runtime_gate']}`",
        f"- runtime gate pass: `{result['runtime_gate_overall_pass']}`",
        f"- runtime scenarios: `{result['runtime_scenarios_pass']}/{result['runtime_scenarios_total']}`",
        f"- p0 open count: `{result['p0_open_count']}`",
        "",
        "## 2) Evidence",
        f"- `{LIVE_PATH.relative_to(ROOT)}`",
        f"- `{GATE_PATH.relative_to(ROOT)}`",
        f"- `{EVIDENCE_PATH.relative_to(ROOT)}`",
        "",
        "## 3) Next Priority",
    ]
    for idx, item in enumerate(result["next_priority"], start=1):
        md.append(f"{idx}. {item}")

    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    print("Wrote:", OUT_JSON)
    print("Wrote:", OUT_MD)


if __name__ == "__main__":
    main()

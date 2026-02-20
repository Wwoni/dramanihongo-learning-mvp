#!/usr/bin/env python3
"""
Sprint 01 runtime gate checker.

Inputs:
- outputs/ingest/live_validation_results_s1.json
- qa/runtime_execution_evidence_s1.json (optional, manual runtime evidence)

Outputs:
- outputs/qa/runtime_gate_results_s1.json
- docs/runtime_gate_report_s1.md
"""

import json
import pathlib
from datetime import datetime, timezone


ROOT = pathlib.Path(__file__).resolve().parents[1]
LIVE_JSON = ROOT / "outputs/ingest/live_validation_results_s1.json"
EVIDENCE_JSON = ROOT / "qa/runtime_execution_evidence_s1.json"
OUT_DIR = ROOT / "outputs/qa"
OUT_JSON = OUT_DIR / "runtime_gate_results_s1.json"
OUT_MD = ROOT / "docs/runtime_gate_report_s1.md"


def load_json(path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate_live_validation(data):
    if not data:
        return {"status": "missing", "pass": False, "detail": "live validation file missing"}
    summary = data.get("summary", {})
    ok = bool(summary.get("overall_pass"))
    return {
        "status": "present",
        "pass": ok,
        "detail": f"valid {summary.get('valid_pass', 0)}/{summary.get('valid_total', 0)}, negative {summary.get('negative_pass', 0)}/{summary.get('negative_total', 0)}",
    }


def evaluate_runtime_evidence(data):
    if not data:
        return {
            "status": "missing",
            "pass": False,
            "scenarios_pass": 0,
            "scenarios_total": 6,
            "p0_open_count": None,
            "detail": "runtime evidence file missing",
        }
    scenarios = data.get("scenarios", [])
    pass_count = 0
    for s in scenarios:
        if str(s.get("result", "")).lower() == "pass":
            pass_count += 1
    total = len(scenarios)
    p0_open = data.get("p0_open_count")
    ok = (total >= 6 and pass_count == total and isinstance(p0_open, int) and p0_open == 0)
    return {
        "status": "present",
        "pass": ok,
        "scenarios_pass": pass_count,
        "scenarios_total": total,
        "p0_open_count": p0_open,
        "detail": f"scenarios {pass_count}/{total}, p0_open={p0_open}",
    }


def evaluate_kpis(data):
    if not data:
        return {"status": "missing", "pass": False, "detail": "runtime evidence file missing"}
    k = data.get("kpis", {})
    sr = k.get("event_collection_success_rate")
    mr = k.get("event_missing_rate")
    er = k.get("schema_error_rate")
    p95 = k.get("ingest_latency_p95_sec")
    present = all(v is not None for v in [sr, mr, er, p95])
    if not present:
        return {"status": "incomplete", "pass": False, "detail": "one or more KPI fields are null"}
    ok = (sr >= 99 and mr < 5 and er < 1 and p95 <= 5)
    return {
        "status": "present",
        "pass": ok,
        "detail": f"success={sr}, missing={mr}, schema_error={er}, p95={p95}",
    }


def main():
    live = load_json(LIVE_JSON)
    evidence = load_json(EVIDENCE_JSON)

    checks = {
        "live_validation": evaluate_live_validation(live),
        "runtime_scenarios": evaluate_runtime_evidence(evidence),
        "event_kpis": evaluate_kpis(evidence),
    }
    overall = all(v["pass"] for v in checks.values())

    result = {
        "run_at_utc": datetime.now(timezone.utc).isoformat(),
        "checks": checks,
        "overall_pass": overall,
        "gate": "GO" if overall else "NO-GO",
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    md = [
        "# Runtime Gate Report S1",
        "",
        f"- 작성일: {datetime.now(timezone.utc).date()}",
        "- 실행 스크립트: `scripts/run_runtime_gate_s1.py`",
        "- 결과 JSON: `outputs/qa/runtime_gate_results_s1.json`",
        "",
        "## 1) 체크 결과",
        "| 항목 | 상태 | 결과 | 상세 |",
        "|---|---|---|---|",
    ]
    for name, row in checks.items():
        md.append(f"| {name} | {row['status']} | {'PASS' if row['pass'] else 'FAIL'} | {row['detail']} |")
    md += [
        "",
        "## 2) 최종 판정",
        f"- gate: `{result['gate']}`",
        f"- overall_pass: `{result['overall_pass']}`",
        "",
        "## 3) 참고 입력 파일",
        f"- `{LIVE_JSON.relative_to(ROOT)}`",
        f"- `{EVIDENCE_JSON.relative_to(ROOT)}` (optional, 수동 작성)",
    ]
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    print("Wrote:", OUT_JSON)
    print("Wrote:", OUT_MD)


if __name__ == "__main__":
    main()

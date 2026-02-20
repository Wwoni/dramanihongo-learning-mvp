#!/usr/bin/env python3
"""
Lint runtime evidence JSON for Sprint 01 QA gate input.
"""

import json
import pathlib
from datetime import datetime, timezone


ROOT = pathlib.Path(__file__).resolve().parents[1]
IN_PATH = ROOT / "qa/runtime_execution_evidence_s1.json"
OUT_DIR = ROOT / "outputs/qa"
OUT_JSON = OUT_DIR / "runtime_evidence_lint_s1.json"
OUT_MD = ROOT / "docs/runtime_evidence_lint_report_s1.md"

SCENARIO_IDS = ["S1-01", "S1-02", "S1-03", "S1-04", "S1-05", "S1-06"]
SCENARIO_NAMES = {
    "S1-01": "first_learning_loop",
    "S1-02": "bookmark_event",
    "S1-03": "shadowing_speed_feedback",
    "S1-04": "resume_after_interrupt",
    "S1-05": "network_retry",
    "S1-06": "subscription_started_event",
}


def main():
    issues = []
    payload = None
    if IN_PATH.exists():
        payload = json.loads(IN_PATH.read_text(encoding="utf-8"))
    else:
        issues.append("missing_file: qa/runtime_execution_evidence_s1.json")

    if payload:
        for k in ["run_date", "build_version", "platform", "scenarios", "kpis", "p0_open_count"]:
            if k not in payload:
                issues.append(f"missing_top_level:{k}")

        scenarios = payload.get("scenarios", [])
        if not isinstance(scenarios, list):
            issues.append("invalid_type:scenarios_not_list")
            scenarios = []

        by_id = {}
        for s in scenarios:
            sid = s.get("id")
            if sid:
                by_id[sid] = s
            else:
                issues.append("missing_scenario_id")

        for sid in SCENARIO_IDS:
            s = by_id.get(sid)
            if not s:
                issues.append(f"missing_scenario:{sid}")
                continue
            if s.get("name") != SCENARIO_NAMES[sid]:
                issues.append(f"invalid_name:{sid}")
            result = str(s.get("result", "")).lower()
            if result not in ("pass", "fail"):
                issues.append(f"invalid_result:{sid}")
            if str(s.get("evidence", "")).strip() == "":
                issues.append(f"missing_evidence:{sid}")
            if result == "fail" and str(s.get("issue_id", "")).strip() == "":
                issues.append(f"missing_issue_id_for_fail:{sid}")

        kpis = payload.get("kpis", {})
        for k in ["event_collection_success_rate", "event_missing_rate", "schema_error_rate", "ingest_latency_p95_sec"]:
            if k not in kpis:
                issues.append(f"missing_kpi_field:{k}")

        p0 = payload.get("p0_open_count")
        if not isinstance(p0, int) or p0 < 0:
            issues.append("invalid_p0_open_count")

    passed = len(issues) == 0
    result = {
        "run_at_utc": datetime.now(timezone.utc).isoformat(),
        "input_path": str(IN_PATH.relative_to(ROOT)),
        "passed": passed,
        "issue_count": len(issues),
        "issues": issues,
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    md = [
        "# Runtime Evidence Lint Report S1",
        "",
        f"- 작성일: {datetime.now(timezone.utc).date()}",
        "- 실행 스크립트: `scripts/run_runtime_evidence_lint_s1.py`",
        "- 결과 JSON: `outputs/qa/runtime_evidence_lint_s1.json`",
        "",
        "## 1) 결과",
        f"- passed: `{passed}`",
        f"- issue_count: `{len(issues)}`",
        "",
        "## 2) 이슈 목록",
    ]
    if issues:
        for i in issues:
            md.append(f"- `{i}`")
    else:
        md.append("- 없음")

    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    print("Wrote:", OUT_JSON)
    print("Wrote:", OUT_MD)


if __name__ == "__main__":
    main()

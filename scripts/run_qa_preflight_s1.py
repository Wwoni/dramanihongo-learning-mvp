#!/usr/bin/env python3
"""
QA preflight checks for Sprint 01 without app runtime.
Generates machine-readable + markdown reports.
"""

import json
import pathlib
from datetime import datetime, timezone


ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "outputs" / "qa"
OUT_JSON = OUT_DIR / "preflight_results_s1.json"
OUT_MD = ROOT / "docs" / "qa_preflight_report_s1.md"


def check_file(path: pathlib.Path):
    return {"path": str(path.relative_to(ROOT)), "exists": path.exists()}


def count_done_in_shotlist(path: pathlib.Path, prefix: str):
    text = path.read_text(encoding="utf-8")
    cnt = 0
    for line in text.splitlines():
        if line.startswith(f"| {prefix}") and "| done |" in line:
            cnt += 1
    return cnt


def main():
    required_files = [
        ROOT / "docs" / "event_schema_v1.md",
        ROOT / "api" / "events" / "openapi_events_v1.yaml",
        ROOT / "api" / "events" / "sample_payloads_v1.json",
        ROOT / "docs" / "ingest_validation_report_s1.md",
        ROOT / "docs" / "ingest_runtime_test_results_s1.md",
        ROOT / "docs" / "image_generation_results_lf001_v1.md",
        ROOT / "docs" / "image_generation_results_lf002_v1.md",
        ROOT / "docs" / "asset_license_verification_sheet_v1.md",
    ]

    checks = [check_file(p) for p in required_files]
    files_ok = all(c["exists"] for c in checks)

    shotlist = ROOT / "docs" / "pastel_image_shotlist_v1.md"
    lf001_done = count_done_in_shotlist(shotlist, "IMG-LF001-")
    lf002_done = count_done_in_shotlist(shotlist, "IMG-LF002-")

    preflight_items = [
        {"name": "required_files", "pass": files_ok, "detail": f"{sum(c['exists'] for c in checks)}/{len(checks)} files"},
        {"name": "lf001_images_done", "pass": lf001_done >= 5, "detail": f"{lf001_done}/5"},
        {"name": "lf002_images_done", "pass": lf002_done >= 5, "detail": f"{lf002_done}/5"},
        {"name": "ingest_runtime_report_present", "pass": (ROOT / "docs" / "ingest_runtime_test_results_s1.md").exists(), "detail": "runtime harness report"},
    ]

    all_pass = all(i["pass"] for i in preflight_items)
    result = {
        "run_at_utc": datetime.now(timezone.utc).isoformat(),
        "checks": checks,
        "preflight_items": preflight_items,
        "all_pass": all_pass,
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    md = [
        "# QA Preflight Report S1",
        "",
        f"- 작성일: {datetime.now(timezone.utc).date()}",
        "- 실행 스크립트: `scripts/run_qa_preflight_s1.py`",
        "- 결과 JSON: `outputs/qa/preflight_results_s1.json`",
        "",
        "## 1) 요약",
        f"- overall: {'PASS' if all_pass else 'FAIL'}",
        "",
        "## 2) 체크 결과",
        "| 항목 | 결과 | 상세 |",
        "|---|---|---|",
    ]
    for i in preflight_items:
        md.append(f"| {i['name']} | {'Pass' if i['pass'] else 'Fail'} | {i['detail']} |")

    md += [
        "",
        "## 3) 파일 존재 체크",
        "| path | exists |",
        "|---|---|",
    ]
    for c in checks:
        md.append(f"| {c['path']} | {'yes' if c['exists'] else 'no'} |")

    md += [
        "",
        "## 4) 주의",
        "- 본 preflight는 앱 런타임 테스트를 대체하지 않음.",
        "- S1-01~S1-06 실제 시나리오 Pass는 앱 빌드 환경에서 별도 수행 필요.",
    ]
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    print("Wrote:", OUT_JSON)
    print("Wrote:", OUT_MD)


if __name__ == "__main__":
    main()

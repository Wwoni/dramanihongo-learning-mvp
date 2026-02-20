#!/usr/bin/env python3
"""
Run Sprint 01 verification pipeline after manual steps are done.

Pipeline:
1) runtime evidence lint
2) runtime gate
3) ingest live validation (only if INGEST_BASE_URL is configured)
4) ops snapshot
"""

import pathlib
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]


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


def run(cmd):
    print(f"$ {' '.join(cmd)}")
    p = subprocess.run(cmd, cwd=ROOT)
    if p.returncode != 0:
        print(f"FAILED: {' '.join(cmd)}")
        return False
    return True


def main():
    ok = True
    ok = run(["python3", "scripts/run_runtime_evidence_lint_s1.py"]) and ok
    ok = run(["python3", "scripts/run_runtime_gate_s1.py"]) and ok

    env = load_env(ROOT / ".env")
    if env.get("INGEST_BASE_URL", "").strip():
        ok = run(["python3", "scripts/run_ingest_live_validation.py"]) and ok
    else:
        print("SKIP: scripts/run_ingest_live_validation.py (INGEST_BASE_URL not configured)")

    ok = run(["python3", "scripts/run_s1_ops_snapshot.py"]) and ok
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

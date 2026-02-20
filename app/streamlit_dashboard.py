#!/usr/bin/env python3
"""
Streamlit dashboard for local/mock ingest logs.

Run:
  streamlit run app/streamlit_dashboard.py
"""

import json
from collections import Counter
from pathlib import Path

import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
ACCEPTED = ROOT / "outputs" / "ingest" / "mock_accepted_events.jsonl"
REJECTED = ROOT / "outputs" / "ingest" / "mock_rejected_events.jsonl"


def load_jsonl(path: Path):
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


def main():
    st.set_page_config(page_title="DramaNihongo Ingest Dashboard", layout="wide")
    st.title("DramaNihongo Ingest Dashboard (Mock/Local)")
    st.caption("Source: outputs/ingest/mock_accepted_events.jsonl, mock_rejected_events.jsonl")

    st.sidebar.header("Data Source")
    use_upload = st.sidebar.checkbox("Use uploaded JSONL files", value=False)
    uploaded_accepted = st.sidebar.file_uploader("Accepted JSONL", type=["jsonl", "txt"])
    uploaded_rejected = st.sidebar.file_uploader("Rejected JSONL", type=["jsonl", "txt"])

    if use_upload and uploaded_accepted is not None:
        accepted = []
        for line in uploaded_accepted.getvalue().decode("utf-8").splitlines():
            s = line.strip()
            if not s:
                continue
            try:
                accepted.append(json.loads(s))
            except Exception:
                continue
    else:
        accepted = load_jsonl(ACCEPTED)

    if use_upload and uploaded_rejected is not None:
        rejected = []
        for line in uploaded_rejected.getvalue().decode("utf-8").splitlines():
            s = line.strip()
            if not s:
                continue
            try:
                rejected.append(json.loads(s))
            except Exception:
                continue
    else:
        rejected = load_jsonl(REJECTED)

    c1, c2, c3 = st.columns(3)
    c1.metric("Accepted", len(accepted))
    c2.metric("Rejected", len(rejected))
    ratio = 0 if len(accepted) + len(rejected) == 0 else len(accepted) / (len(accepted) + len(rejected)) * 100
    c3.metric("Acceptance Rate", f"{ratio:.1f}%")

    event_counter = Counter([r.get("event_name", "unknown") for r in accepted])
    reject_counter = Counter([r.get("code", "unknown") for r in rejected])

    st.subheader("Accepted by Event")
    if event_counter:
        st.bar_chart(event_counter)
    else:
        st.info("No accepted events yet.")

    st.subheader("Rejected by Code")
    if reject_counter:
        st.bar_chart(reject_counter)
    else:
        st.info("No rejected events yet.")

    st.subheader("Recent Accepted (last 30)")
    st.dataframe(list(reversed(accepted[-30:])), use_container_width=True)

    st.subheader("Recent Rejected (last 30)")
    st.dataframe(list(reversed(rejected[-30:])), use_container_width=True)


if __name__ == "__main__":
    main()

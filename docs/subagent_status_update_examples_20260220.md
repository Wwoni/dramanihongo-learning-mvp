# Subagent Status Update Examples (2026-02-20)

수동 작업 후 아래 명령을 그대로 실행하면 상태 파일이 업데이트됩니다.

## 1) A4 완료 처리 예시 (Streamlit URL 발급 후)
```bash
python3 scripts/update_subagent_status.py \
  --agent a4 \
  --status completed \
  --clear-blockers \
  --evidence-json '{"streamlit_url":"https://<app-name>.streamlit.app","deploy_log_note":"deployed on streamlit cloud"}'
```

## 2) A5 진행중/완료 처리 예시

### 2-1. 진행중 (endpoint 설정했지만 아직 검증 전)
```bash
python3 scripts/update_subagent_status.py \
  --agent a5 \
  --status in_progress \
  --clear-blockers \
  --evidence-json '{"ingest_base_url_set":true,"live_validation_overall_pass":null}'
```

### 2-2. 완료 (live validation PASS 후)
```bash
python3 scripts/update_subagent_status.py \
  --agent a5 \
  --status completed \
  --clear-blockers \
  --evidence-json '{"ingest_base_url_set":true,"live_validation_overall_pass":true}'
```

## 3) A7 완료 처리 예시 (최종 게이트 닫기)
```bash
python3 scripts/update_subagent_status.py \
  --agent a7 \
  --status completed \
  --clear-blockers \
  --evidence-json '{"runtime_gate":"GO","runtime_scenarios_pass":"6/6"}'
```

## 4) 최종 집계
```bash
python3 scripts/run_s1_after_manual_steps.py
python3 scripts/run_subagent_control_tower.py
```

산출물:
- `docs/subagent_control_tower_20260220.md`
- `outputs/qa/subagent_control_tower_20260220.json`

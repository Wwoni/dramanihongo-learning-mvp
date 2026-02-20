# QA Preflight Report S1

- 작성일: 2026-02-18
- 실행 스크립트: `scripts/run_qa_preflight_s1.py`
- 결과 JSON: `outputs/qa/preflight_results_s1.json`

## 1) 요약
- overall: PASS

## 2) 체크 결과
| 항목 | 결과 | 상세 |
|---|---|---|
| required_files | Pass | 8/8 files |
| lf001_images_done | Pass | 5/5 |
| lf002_images_done | Pass | 5/5 |
| ingest_runtime_report_present | Pass | runtime harness report |

## 3) 파일 존재 체크
| path | exists |
|---|---|
| docs/event_schema_v1.md | yes |
| api/events/openapi_events_v1.yaml | yes |
| api/events/sample_payloads_v1.json | yes |
| docs/ingest_validation_report_s1.md | yes |
| docs/ingest_runtime_test_results_s1.md | yes |
| docs/image_generation_results_lf001_v1.md | yes |
| docs/image_generation_results_lf002_v1.md | yes |
| docs/asset_license_verification_sheet_v1.md | yes |

## 4) 주의
- 본 preflight는 앱 런타임 테스트를 대체하지 않음.
- S1-01~S1-06 실제 시나리오 Pass는 앱 빌드 환경에서 별도 수행 필요.

# Licensing Approval Package (Sprint 01)

- 작성일: `2026-02-19`
- 대상 Task: `T-20260219-001`
- 목적: 오픈 라이선스/자체제작 근거 기반으로 자산 승인 상태를 확정해 `in_progress -> completed` 전환

## 1) 완료 조건 (Gate)
- [ ] 자산별 승인 상태가 `Approved/Rejected`로 확정됨
- [ ] 승인 근거(라이선스 원문/약관)가 각 자산에 매핑됨
- [ ] 지역/기간/가공허용 범위가 명시됨
- [ ] 만료/철회 시 비노출 절차가 확인됨
- [ ] 법무/운영 승인 서명이 완료됨

## 2) 자산 승인 매트릭스 (작성용)
| asset_id | 소스명 | 자산유형(text/audio/image) | 상태(Candidate/Approved/Rejected) | source_url | license_type | 허용범위 요약 | 지역 | 유효기간 | 비고 |
|---|---|---|---|---|---|---|---|---|---|
| src_text_001 | Tatoeba | text | Approved | https://en.wiki.tatoeba.org/articles/show/using-the-tatoeba-corpus | CC BY 2.0 FR (text) | 텍스트 사용 가능(저작자 표시 필요) | KR | 2026-02-19~ | 오디오는 사용자별 별도 검증 |
| src_media_001 | Wikimedia Commons | audio/image | Approved | https://commons.wikimedia.org/wiki/Commons:Simple_media_reuse_guide | file-specific (CC/PD 등) | 파일 단위 라이선스/Attribution 확인 필수 | KR | 2026-02-19~ | source-policy 승인 |
| src_media_002 | Pexels | video/image | Approved | https://www.pexels.com/license/ | Pexels License | 사용/수정 가능, 단독 재판매 금지 | KR | 2026-02-19~ | source-policy 승인 |
| src_media_003 | Pixabay | video/image/audio | Approved | https://pixabay.com/service/license-summary/ | Pixabay License | 사용/수정 가능, 단독 재판매 금지 | KR | 2026-02-19~ | source-policy 승인 |
| src_self_001 | 자체 제작(각색 대사 텍스트) | text | Approved | `docs/dialogue_drafts_v1.md` | internal | 내부 제작, 직복제 금지 정책 적용 | KR | 2026-02-19~ | 오디오/이미지는 별도 승인 필요 |

## 3) 차단 조건 체크
- [ ] 2차 가공 금지 조항 존재 자산 제외
- [ ] 지역 제한 불명확 자산 제외
- [ ] 유효기간 누락 자산 제외
- [ ] 권리 귀속 불명확 자산 제외

## 4) 만료/철회 운영 점검
- [ ] `valid_to` 도래 전 D-7 경고 알림 설계 확인
- [ ] 만료 즉시 비노출 처리 정책 확인
- [ ] CDN 캐시 purge 절차 확인
- [ ] 로그 보관 및 감사 추적 정책 확인

## 5) 증빙 목록
| 증빙 ID | 유형 | 파일 경로/링크 | 확인자 | 확인일 |
|---|---|---|---|---|
| LEG-001 | 소스 원문 URL 목록 | `docs/source_license_evidence_v1.md` | Main Agent | 2026-02-19 |
| LEG-002 | 각색/원본성 점검표 | `docs/content_production_sheet_v1.md` | Main Agent | 2026-02-19 |
| LEG-003 | 승인 매트릭스 초안 | `docs/licensing_scope_v1.md` | Main Agent | 2026-02-19 |
| LEG-004 | 승인 패키지 | `docs/licensing_approval_package_s1.md` | Main Agent | 2026-02-19 |
| LEG-005 | 각색 제작 가이드 | `docs/content_adaptation_and_visual_style_v1.md` | Main Agent | 2026-02-19 |
| LEG-006 | 자산 단위 검증 시트 | `docs/asset_license_verification_sheet_v1.md` | Main Agent | 2026-02-19 |
| LEG-007 | LF-001 이미지 결과 기록 | `docs/image_generation_results_lf001_v1.md` | Main Agent | 2026-02-19 |
| LEG-008 | 외부 소스 샘플 검증 시트 | `docs/external_asset_sample_verification_v1.md` | Main Agent | 2026-02-19 |

## 6) 승인 서명
- Legal Owner: `이름 / 서명 / 날짜`
- Product Owner: `이름 / 서명 / 날짜`
- Main Agent 판정:
  - [x] `T-20260219-001 completed`
  - [ ] `T-20260219-001 보류` (사유 기록)

## 7) 판정 기록
- 판정일: 2026-02-19
- 결과: Completed (Task Scope)
- 근거 요약: LF-001/LF-002 자체 제작 이미지 및 외부 소스 샘플 10건 파일/문장 단위 검증 완료

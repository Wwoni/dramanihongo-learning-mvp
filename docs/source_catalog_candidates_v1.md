# Source Catalog Candidates v1

- 작성일: `2026-02-19`
- 목적: 개인 개발자가 합법적으로 활용 가능한 일본어 학습 콘텐츠 소스 후보를 정리
- 관련 Task: `T-20260219-001`

## 1) 후보 소스
| source_id | 소스 | 자산 유형 | 확인 항목 | 상태 |
|---|---|---|---|---|
| SRC-TXT-001 | Tatoeba | text/audio | 문장별 라이선스, Attribution, 상업 이용 가능 여부 | Approved (text only) |
| SRC-MED-001 | Wikimedia Commons | audio/video/image | 파일별 라이선스, 변경 허용, Attribution | Approved (source-policy) |
| SRC-MED-002 | Openverse(검색) | mixed | 원본 링크 추적, 원본 라이선스 원문 확인 | Candidate |
| SRC-MED-003 | Pexels | video/image | 라이선스 허용 범위, 금지 용도 확인 | Approved (source-policy) |
| SRC-MED-004 | Pixabay | video/image/audio | 라이선스 허용 범위, 금지 용도 확인 | Approved (source-policy) |
| SRC-SELF-001 | 자체 제작 대사/녹음 | text/audio | 제작자 동의, 권리 귀속 기록 | Approved (internal policy) |

## 2) 필수 수집 필드
- `asset_id`
- `source_id`
- `source_url`
- `license_type`
- `license_url`
- `author`
- `attribution_text`
- `commercial_ok` (true/false)
- `derivative_ok` (true/false)
- `valid_from`
- `valid_to`
- `reviewer`
- `reviewed_at`
- `status` (`Candidate/Approved/Rejected`)

## 3) 승인 기준
- `commercial_ok=true` and `derivative_ok=true` 우선 승인
- 출처 URL 또는 라이선스 URL 누락 시 자동 Rejected
- 파일 단위 라이선스가 다른 플랫폼은 자산 단위로 개별 심사

## 4) 다음 액션
1. 각 소스에서 샘플 자산 10개씩 추출
2. `docs/licensing_approval_package_s1.md` 매트릭스에 개별 자산 입력
3. Approved 자산만 MVP 콘텐츠 카드 생성에 사용

## 증빙 문서
- `docs/source_license_evidence_v1.md`

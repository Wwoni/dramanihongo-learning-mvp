# External Asset Sample Verification v1

- 작성일: `2026-02-19`
- 목적: 외부 소스의 파일/문장 단위 검증 샘플 관리(1차 10건)
- 관련 Task: `T-20260219-001`

| sample_id | source_id | asset_type | candidate_url | license_check | attribution_check | usage_check | status | notes |
|---|---|---|---|---|---|---|---|---|
| EXT-001 | SRC-TXT-001 | text | https://tatoeba.org/en/sentences/show/1532832 | pass | pass | pass | verified | Sentence page에 License: CC BY 2.0 FR 표기 |
| EXT-002 | SRC-TXT-001 | text | https://tatoeba.org/en/sentences/show/10145019 | pass | pass | pass | verified | Sentence page logs에 CC BY 2.0 FR 표기 |
| EXT-003 | SRC-MED-001 | image | https://commons.wikimedia.org/wiki/File:Photo_taken_from_Train_in_Japan.jpg | pass | pass | pass | verified | CC BY 4.0, attribution 필요 |
| EXT-004 | SRC-MED-001 | image | https://commons.wikimedia.org/wiki/File:Tokyo_Station_(49700941622).jpg | pass | pass | pass | verified | CC BY-SA 4.0, share-alike 주의 |
| EXT-005 | SRC-MED-001 | audio | https://commons.wikimedia.org/wiki/File:Ja-nihongo.ogg | pass | pass | pass | verified | Public domain 표기 확인 |
| EXT-006 | SRC-MED-003 | image | https://www.pexels.com/photo/vibrant-tokyo-street-with-skyscrapers-and-traffic-30641577/ | pass | pass | pass | verified | Pexels license, attribution 불필수 |
| EXT-007 | SRC-MED-003 | image | https://www.pexels.com/photo/japanese-street-with-traditional-architecture-and-garden-33142325/ | pass | pass | pass | verified | Pexels license, 재판매 제한 유의 |
| EXT-008 | SRC-MED-004 | image | https://pixabay.com/photos/tokyo-japan-street-old-shop-6888412/ | pass | pass | pass | verified | Pixabay Content License 표시 확인 |
| EXT-009 | SRC-MED-004 | image | https://pixabay.com/photos/japan-street-city-urban-9101435/ | pass | pass | pass | verified | Pixabay Content License 표시 확인 |
| EXT-010 | SRC-MED-004 | image | https://pixabay.com/photos/street-city-japan-dusk-shinjuku-6884533/ | pass | pass | pass | verified | Pixabay Content License 표시 확인 |

## 체크 기준
- `license_check`: 해당 자산의 라이선스 유형/약관 적합성 확인
- `attribution_check`: 저작자 표시 필요 여부 및 표기문 확보
- `usage_check`: 상업 사용/2차가공/재배포 금지 충돌 여부 확인

## status 정의
- `pending`: 미검증
- `verified`: 배포 가능
- `rejected`: 사용 불가

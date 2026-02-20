# Content Adaptation & Visual Style v1

- 작성일: `2026-02-19`
- 목적: 유튜브 내 일본 일상/문화 주제를 참고해 합법적으로 각색 대사를 제작하고, 파스텔풍 캐릭터 이미지를 학습 흐름에 연동하기 위한 운영 가이드

## 1) 대사 각색 정책 (YouTube 주제 참고)
- 허용:
  - 주제/상황 참고 (예: 편의점, 직장 인사, 카페 주문, 친구 약속)
  - 분위기/화법 톤 참고
- 금지:
  - 원문 대사/자막의 문장 단위 복제
  - 특정 배우/캐릭터 고유 대사 재현
  - 방송사 로고/브랜드/고유명사 무단 사용

## 2) 각색 제작 포맷
| 필드 | 설명 |
|---|---|
| topic_id | 주제 ID (예: daily_convenience_store) |
| reference_url | 참고한 공개 URL (기록용) |
| jp_draft | 각색 일본어 대사 |
| ko_translation | 한국어 번역 |
| grammar_tag | 문법 포인트 |
| originality_check | 원문 직복제 여부 자체 점검 결과 |

## 3) 캐릭터 아트 스타일 가이드
- 톤: 일본 감성 + 파스텔
- 키워드:
  - `soft pastel palette`
  - `clean line art`
  - `gentle expression`
  - `slice of life mood`
  - `minimal background`
- 금지:
  - 실존 캐릭터/IP와 혼동되는 복장/헤어/소품
  - 특정 애니/드라마 캐릭터의 유사 디자인

## 4) 학습 흐름 내 이미지 연동 규칙
- `LF-001` Scene Intro: 상황 대표 캐릭터 1컷
- `LF-002` Line Study: 대사별 감정 아이콘형 캐릭터
- `LF-003` Quiz: 힌트/정오답 반응 캐릭터
- `LF-006` Summary: 완료 리워드 캐릭터

## 5) 자산 메타데이터 (이미지 필수)
- `asset_id`
- `style_version`
- `prompt_text` (내부 기록)
- `source_type` (`self_generated`/`stock`)
- `license_type`
- `attribution_text`
- `review_status` (`Candidate/Approved/Rejected`)

## 6) QA 체크
- [ ] 대사가 참고 소스 원문과 문장 단위 중복되지 않음
- [ ] 이미지가 특정 IP와 혼동되지 않음
- [ ] 라이선스/출처 메타데이터 누락 없음

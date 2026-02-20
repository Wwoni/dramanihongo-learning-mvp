# Streamlit-style Personal Deploy & Cost (2026-02-20)

## 1) 결론
- `https://<name>.streamlit.app` 형태로 개인 체험 배포 가능
- 현재 프로젝트에서는 `app/streamlit_dashboard.py`로 바로 시작 가능

## 2) 바로 실행(로컬)
```bash
pip install -r app/requirements_streamlit.txt
streamlit run app/streamlit_dashboard.py
```

## 3) Streamlit Community Cloud 배포 흐름
1. GitHub에 리포지토리 푸시
2. Streamlit Community Cloud에서 `Deploy an app`
3. Entry point: `app/streamlit_dashboard.py`
4. URL 발급: `https://<app-name>.streamlit.app`
5. 체크리스트: `docs/streamlit_cloud_release_checklist_20260220.md`

## 4) 비용 관점 (개인 개발 기준)

### Option A) Streamlit Community Cloud
- 비용: 무료(공식 FAQ 기준)
- 장점: 가장 빠른 체험 배포
- 주의:
  - 리소스 제한(공식 문서 기준, 2024-02 시점 안내): CPU 약 0.078~2 cores, 메모리 약 690MB~2.7GB, 스토리지 최대 50GB
  - private app은 동시 1개 제한 정책 문구 존재
  - 12시간 무트래픽 시 앱 슬립

### Option B) Railway
- 요금 구조(공식):
  - Free: `$0/월` (초기 크레딧 후 월 `$1` 과금 문구 존재)
  - Hobby: `$5` minimum usage (월 `$5` usage 포함)
- 장점: API/DB/worker 함께 붙이기 쉬움
- 권장 시점: ingest API를 실제 서비스로 붙일 때

### Option C) Fly.io
- 요금 구조(공식): usage-based
  - shared-cpu-1x 256MB: 약 `$1.94/월`
  - shared-cpu-1x 1GB: 약 `$5.70/월`
- 장점: 장기적으로 API + 대시보드를 한 인프라로 묶기 좋음

## 5) 개인 작업 추천안
1. 단기(지금): Streamlit Community Cloud 무료로 체험 공개
2. 중기(실서비스): Railway 또는 Fly.io에 ingest API + 대시보드 이동
3. 데이터 누적 규모가 커지면 DB/스토리지 분리

## 5.1) 개인 개발 월 비용 러프컷
- 체험 MVP(대시보드만): `0원` (Streamlit Community Cloud)
- 대시보드 + 초소형 API:
  - Railway Hobby 기준: 최소 약 `$5/월`부터
  - Fly.io shared-cpu-1x 256MB 기준: 약 `$1.94/월` + 스토리지/네트워크
- 실제 비용은 트래픽/스토리지/리전 선택에 따라 변동

## 6) 참고 소스
- Streamlit Community Cloud docs: https://docs.streamlit.io/deploy/streamlit-community-cloud
- Streamlit Community Cloud FAQ(무료/리소스/제한): https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app/faq
- Streamlit Manage app(리소스/슬립): https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app
- Streamlit deploy overview: https://docs.streamlit.io/deploy
- Streamlit deploy flow(서브도메인): https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
- Streamlit private app 제한 문구: https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app
- Railway pricing: https://railway.com/pricing
- Fly.io pricing: https://fly.io/docs/about/pricing/

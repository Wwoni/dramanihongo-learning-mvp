# Streamlit Cloud Release Checklist (2026-02-20)

## 1) 배포 전 준비
- [ ] GitHub 리포지토리에 아래 파일 반영
  - `app/streamlit_dashboard.py`
  - `requirements.txt`
  - `.streamlit/config.toml`
- [ ] 로컬 실행 확인
```bash
pip install -r requirements.txt
streamlit run app/streamlit_dashboard.py
```

## 2) Streamlit Community Cloud 배포
1. https://share.streamlit.io 접속
2. `New app` 클릭
3. Repository 선택
4. Branch 선택 (예: `main`)
5. Main file path 입력: `app/streamlit_dashboard.py`
6. Deploy 클릭

## 3) 배포 후 점검
- [ ] 앱 URL 접속 확인 (`https://<app-name>.streamlit.app`)
- [ ] 대시보드 페이지 렌더링 확인
- [ ] 업로드 모드로 JSONL 업로드 후 차트 반영 확인
- [ ] 오류 로그(Streamlit Cloud logs) 확인

## 4) 운영 권장
- 샘플 데이터 공개 시 개인정보/민감정보 제거
- 앱 설명에 “데모 데이터 기반” 문구 표시
- 트래픽 증가 시 Railway/Fly.io로 API + DB 분리 이전 검토

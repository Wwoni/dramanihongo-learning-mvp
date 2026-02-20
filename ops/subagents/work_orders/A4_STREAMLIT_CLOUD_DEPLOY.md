# [Task ID] T-20260220-STREAMLIT-DEPLOY
[Owner] A4_App_Client  
[Priority] P0  
[Objective] Streamlit Community Cloud에 체험용 대시보드 배포 URL 발급  
[Input] `app/streamlit_dashboard.py`, `requirements.txt`, `.streamlit/config.toml`  
[Output] `https://<app-name>.streamlit.app` URL, 배포 스크린샷/로그  
[DoD] 외부에서 URL 접속 시 대시보드 렌더링 성공  
[Risk] GitHub 연동 권한, Cloud 배포 실패, 리소스 제한  
[ETA] 30~60분

## 실행 명령 (A4)
```bash
pip install -r requirements.txt
python3 -m streamlit run app/streamlit_dashboard.py
```

## Cloud 배포 절차
1. GitHub에 현재 리포지토리 push
2. https://share.streamlit.io 로그인
3. `New app` -> Repository 선택 -> Main file path `app/streamlit_dashboard.py`
4. Deploy 클릭
5. 발급 URL 기록

## 결과 보고 형식
```md
[Task ID] T-20260220-STREAMLIT-DEPLOY
1) 결과 요약:
2) 변경 파일/산출물:
3) 검증 방법/결과:
4) 남은 리스크:
5) 다음 제안 액션(최대 3개):
```

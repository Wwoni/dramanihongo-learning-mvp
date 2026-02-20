# OpenAI Image Generation Runbook v1

- 작성일: `2026-02-19`
- 대상: LF-001 파스텔 캐릭터 이미지 생성 자동화

## 1) 준비
- `.env` 파일 생성(권장):
```bash
cp .env.example .env
```
- `.env`에서 키 입력:
```bash
OPENAI_API_KEY="YOUR_API_KEY"
```

- 또는 터미널 환경 변수 설정:
```bash
export OPENAI_API_KEY="YOUR_API_KEY"
```

## 2) 드라이런(문서 미변경)
```bash
python3 scripts/generate_lf001_images_openai.py --dry-run
```

## 3) 실제 생성
```bash
python3 scripts/generate_lf001_images_openai.py \
  --model gpt-image-1 \
  --quality medium \
  --size 1024x1024
```

## 4) 결과물
- 이미지 파일: `outputs/images/lf001/*.png`
- 실행 로그: `outputs/images/lf001/latest_generation_results.json`
- 자동 업데이트 문서:
  - `docs/image_generation_results_lf001_v1.md`
  - `docs/pastel_image_shotlist_v1.md`

## 5) 실패 시 점검
- `OPENAI_API_KEY` 누락 여부
- 네트워크/방화벽 차단 여부
- API 에러 메시지(로그 파일 확인)

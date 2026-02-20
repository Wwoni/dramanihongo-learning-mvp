# Pastel Character Prompt Templates v1

- 작성일: `2026-02-19`
- 목적: 학습 흐름 단계별 파스텔풍 캐릭터 이미지 생성 템플릿 제공

## 공통 스타일 토큰
- `soft pastel palette, clean line art, gentle lighting, slice-of-life japanese mood, no logo, no text, original character design`

## 1) Scene Intro (LF-001)
```text
Create an original anime-style character illustration in soft pastel palette.
Scene: {scene_context}
Character mood: {emotion}
Outfit: modern casual, non-branded
Background: minimal japanese daily-life setting
Style tokens: soft pastel palette, clean line art, gentle lighting, slice-of-life japanese mood, no logo, no text, original character design
Aspect ratio: 4:5
```

## 2) Line Study (LF-002)
```text
Create a waist-up reaction portrait of an original character.
Emotion cue: {emotion_tag} (neutral/joy/anger/sad/urgent)
Pose: simple, readable for language learning card
Background: flat pastel gradient
Style tokens: soft pastel palette, clean line art, gentle lighting, no logo, no text, original character design
Aspect ratio: 1:1
```

## 3) Quiz Feedback (LF-003)
```text
Create two matching original character reactions.
Version A (correct): subtle happy expression, encouraging gesture
Version B (incorrect): calm supportive expression, retry gesture
No symbols from existing IP.
Style tokens: soft pastel palette, clean line art, no logo, no text, original character design
Aspect ratio: 1:1
```

## 4) Session Summary (LF-006)
```text
Create a completion reward scene with one or two original characters.
Mood: warm, celebratory but calm
Props: generic notebook, tea cup, small confetti shapes
Background: minimal japanese home desk corner
Style tokens: soft pastel palette, clean line art, gentle lighting, no logo, no text, original character design
Aspect ratio: 16:9
```

## 5) 네거티브 프롬프트
```text
no copyrighted character, no known anime franchise style imitation, no brand logo, no watermark, no text overlay, no realistic celebrity face
```

## 6) 메타데이터 기록 템플릿
| asset_id | flow_stage | prompt_version | source_type | license_type | review_status | reviewer |
|---|---|---|---|---|---|---|
|  | LF-001/LF-002/LF-003/LF-006 | v1 | self_generated | internal | Candidate |  |

# Shadowing Feedback Logic Prototype

- 작성일: `2026-02-19`
- 목적: 쉐도잉 MVP 피드백 계산의 최소 로직 명세

## 1) 함수 계약

```ts
type TimingGrade = "good" | "fast" | "slow";

interface ShadowingInput {
  sourceAudioSec: number;
  recordingSec: number;
  retryCount?: number;
}

interface ShadowingOutput {
  speedRatio: number;
  timingGrade: TimingGrade;
  feedbackText: string;
}

function buildShadowingFeedback(input: ShadowingInput): ShadowingOutput
```

## 2) 알고리즘
1. `sourceAudioSec <= 0` 또는 `recordingSec <= 0`이면 예외 처리
2. `speedRatio = recordingSec / sourceAudioSec`
3. 구간 분류:
   - `0.9 <= speedRatio <= 1.15` => `good`
   - `speedRatio < 0.9` => `fast`
   - `speedRatio > 1.15` => `slow`
4. 등급별 피드백 텍스트 반환

## 3) 의사코드
```text
if sourceAudioSec <= 0 or recordingSec <= 0:
  throw invalid_duration

speedRatio = recordingSec / sourceAudioSec

if speedRatio < 0.9:
  grade = "fast"
  text = "조금 빨라요. 원문 속도에 맞춰 다시 시도해보세요."
else if speedRatio <= 1.15:
  grade = "good"
  text = "리듬이 좋아요. 한 번 더 또렷하게 말해보세요."
else:
  grade = "slow"
  text = "조금 느려요. 호흡을 짧게 끊어 말해보세요."

return { speedRatio, timingGrade: grade, feedbackText: text }
```

## 4) 테스트 케이스
| sourceAudioSec | recordingSec | 기대 grade |
|---|---|---|
| 4.0 | 3.2 | fast |
| 4.0 | 3.8 | good |
| 4.0 | 4.6 | good |
| 4.0 | 5.1 | slow |

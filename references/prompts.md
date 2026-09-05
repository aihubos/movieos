# 출력 양식

대괄호는 채워 넣을 자리다. 최종 프롬프트에는 실제 내용을 쓴다. 영문과 한국어 번역은 서로 다른 코드 블록으로 출력한다. 대사는 어느 블록에서도 선택 언어의 원문 그대로 둔다.

## 캐릭터 시트

```text
PROJECT: [Title] | CHARACTER: [CHAR_01] | STYLE: [selected style]
ART STYLE: [medium, lines, texture and palette]
CHARACTER ANCHOR: [original age, face, eyes, hair, proportions, distinguishing details]
CHARACTER STATE & ACTION: Neutral standing poses and three story-relevant facial expressions of the same person.
COSTUME & PROPS: [story-specific fixed costume, materials, colors and props]
LOCATION & ENVIRONMENT: Pure white seamless background, no scenery.
LAYOUT & CAMERA: Character reference sheet with front full body, three-quarter full body, side view, face close-up and three expression portraits; clear spacing; no cropped feet.
LIGHTING & COLOR: Even neutral illumination; preserve the selected style and consistent colors.
CONTINUITY & AVOID: Same original person in every panel; no text, labels, watermark or unrelated props.
```

## 숏 카드 맨 위

```text
SUPPORTED DURATION: [verified durations for this exact model/mode, or UNVERIFIED]
DURATION LOCK: [4s / 6s / 8s / 10s selected within verified support; pending if not verified]
DURATION REASON: [emotion, action and dialogue needs]
BEAT MAP:
0.0–[t1]s: [action/dialogue]
[t1]–[end]s: [action/dialogue; END STATE; next-shot connection]
TOTAL DURATION CHECK: [sum of interval lengths] = [DURATION LOCK]; [MATCH or pending]
TARGET MODEL: [verified model name or candidate marked UNVERIFIED]
FALLBACK MODEL: [verified alternative or NONE]
FLOW MODE: [verified Text to Video / First Frame to Video / Image to Video equivalent]
DURATION: [same as DURATION LOCK]
RESOLUTION: 1080p target | Center-safe 16:9 | [support verification]
MODEL SELECTION REASON: [one grounded sentence; do not invent comparative performance]
```

위 시간 블록 다음에 장면 목적, 사용 캐릭터·참조 파일, 시작 이미지 프롬프트와 이미지, 영상 프롬프트를 순서대로 제공한다.

## 시작 이미지 프롬프트

```text
PROJECT: [Title] | SCENE: [SC01] | SHOT: [SH001] | STYLE: [selected style]
ART STYLE: [selected style specification]
CHARACTER ANCHOR: [locked ID plus full appearance; attached reference image mapping]
CHARACTER STATE & ACTION: At time 0.0, [single frozen pose, gaze, position, expression].
COSTUME & PROPS: [exact costume and prop state]
LOCATION & ENVIRONMENT: [story-specific location; foreground, midground, background]
LAYOUT & CAMERA: [shot size, angle, opening composition; single frame]
LIGHTING & COLOR: [fixed time of day, light direction and palette]
CONTINUITY & AVOID: Single 16:9 center-safe cinematic frame; preserve reference identity; no reference-sheet panels, white studio background unless the story calls for it, text or watermark; [style-specific exclusions].
```

## 영상 프롬프트

```text
PROJECT: [Title] | SCENE: [SC01] | SHOT: [SH001] | STYLE: [selected style]
ART STYLE: [selected style specification]
CHARACTER ANCHOR: [locked ID, full appearance and input image mapping]
CHARACTER STATE & ACTION: [time intervals matching BEAT MAP, precise movement and expression]
COSTUME & PROPS: [fixed details and intentional changes]
LOCATION & ENVIRONMENT: [same place as first frame]
LAYOUT & CAMERA: [shot size, angle, one camera movement or static; axis and eyeline]
LIGHTING & COLOR: [same lighting and palette as first frame]
DIALOGUE LANGUAGE: [Korean / English]
DIALOGUE: [speaker, exact line and interval; NONE if silent]
SOUND: [ambience, breathing, footsteps]; MUSIC OFF.
END STATE & CONNECTION: [final pose, gaze, props and transition to next shot]
CONTINUITY & AVOID: Start from the supplied first frame; consistent character identity; 16:9 center-safe; no subtitles, text, watermark or music; [style-specific exclusions].
```

한국어 대응 필드: 작품명 / 장면 / 숏 / 연출 화풍 / 화풍 규격 / 캐릭터 앵커 / 캐릭터 동작 및 연기 / 복식 및 소품 / 공간 및 배경 / 구도 및 연출 / 조명 및 색채 / 대사 언어 / 대사 / 소리 / 종료 상태 및 연결 / 연속성 및 배제 요소.

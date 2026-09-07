# 출력 양식

대괄호는 채워 넣을 자리다. 최종 프롬프트에는 실제 내용을 쓴다. 영문과 한국어 번역은 서로 다른 코드 블록으로 출력한다. 대사는 어느 블록에서도 선택 언어의 원문 그대로 둔다. 실제 참조 파일 경로·사용자 승인 상태는 코드블록 밖의 업로드 안내에 두고, 생성 도구에는 해당 이미지를 실제 첨부한다.

## 선택한 이미지 구성 적용

- 초반 답변의 첫 프레임 생성 여부와 씬별 추가 관련 이미지 수량을 따른다. 첫 프레임은 씬당 0장 또는 1장, 추가 이미지는 씬당 N장이며 서로 별개다.
- 첫 프레임을 생성하지 않으면 시작 이미지 프롬프트·업로드 안내·`Start from the supplied first frame` 지시를 생략하고 실제 텍스트·기준 참조 입력에 맞춘다. 없는 파일이나 `FIRST_FRAME`을 참조하지 않는다.
- 관련 이미지 양식은 선택한 장수만큼 각각 작성한다. 0장이면 생략한다. 두 종류 모두 0장이어도 씬별 영상 프롬프트와 웹 가이드는 반드시 만든다.

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

## 씬 시간·모델 카드 (영상 프롬프트 아래)

```text
SUPPORTED DURATION: [actual durations confirmed for this exact model/mode, or UNVERIFIED]
DURATION LOCK: [duration confirmed for this exact model/mode, or UNVERIFIED directing target]
DURATION REASON: [emotion, action and dialogue needs]
BEAT MAP:
0.0–[t1]s: [action/dialogue]
[t1]–[end]s: [action/dialogue; END STATE; next-shot connection]
TOTAL DURATION CHECK: [sum of interval lengths] = [numeric directing target]; [MATCH / MISMATCH, independent of support verification]
TARGET MODEL: [verified model name or candidate marked UNVERIFIED]
FALLBACK MODEL: [verified alternative or NONE]
FLOW MODE: [verified Text to Video / First Frame to Video / Image to Video equivalent]
DURATION: [same as DURATION LOCK]
RESOLUTION: 1080p target | [selected aspect ratio], center-safe composition | [support verification]
MODEL SELECTION REASON: [one grounded sentence; do not invent comparative performance]
```

나레이션 다음 영문 영상 프롬프트를 펼쳐 보여주고 이 시간 블록은 아래의 상세 영역에 배치한다.

## 시작 이미지 프롬프트

```text
PROJECT: [Title] | SCENE: [번호] | STYLE: [selected style]
ART STYLE: [selected style specification]
CHARACTER ANCHOR: [production reference ID/version and full appearance; reference image actually attached]
CHARACTER STATE & ACTION: At time 0.0, [single frozen pose, gaze, position, expression].
COSTUME & PROPS: [exact costume and prop state]
LOCATION & ENVIRONMENT: [story-specific location; foreground, midground, background]
LAYOUT & CAMERA: [shot size, angle, opening composition; single frame]
LIGHTING & COLOR: [fixed time of day, light direction and palette]
CONTINUITY & AVOID: Single [selected aspect ratio], center-safe cinematic frame; preserve the production reference identity; no reference-sheet panels, white studio background unless the story calls for it, text or watermark; [style-specific exclusions].
```

## 영상 프롬프트

```text
씬 [번호]:
PROJECT: [Title] | SCENE: [번호] | STYLE: [selected style]
ART STYLE: [selected style specification]
CHARACTER ANCHOR: [production reference ID/version and full appearance; input images actually attached]
CHARACTER STATE & ACTION: [time intervals matching BEAT MAP, precise movement and expression]
COSTUME & PROPS: [fixed details and intentional changes]
LOCATION & ENVIRONMENT: [same place as the first frame when one exists; otherwise the established scene location]
LAYOUT & CAMERA: [shot size, angle, one camera movement or static; axis and eyeline]
LIGHTING & COLOR: [same lighting and palette as the first frame when one exists; otherwise the established scene lighting and palette]
DIALOGUE LANGUAGE: [Korean / English]
DIALOGUE: [speaker, exact line and interval; NONE if silent]
SFX: [timed cue 1 linked to action; timed cue 2; texture, intensity and decay; editorial/non-diegetic if appropriate].
AMBIENCE: [appropriate environment or NONE]. MUSIC OFF.
NARRATION: NONE. VOICEOVER: NONE.
END STATE & CONNECTION: [final pose, gaze, props and transition to next shot]
CONTINUITY & AVOID: [When a first frame exists, start from the supplied first frame; otherwise start from the provided text and production references]; consistent character identity; [selected aspect ratio], center-safe; no subtitles, text, watermark or music; [style-specific exclusions].
```

한국어 대응 필드: 작품명 / 장면 / 씬 / 연출 화풍 / 화풍 규격 / 캐릭터 앵커 / 캐릭터 동작 및 연기 / 복식 및 소품 / 공간 및 배경 / 구도 및 연출 / 조명 및 색채 / 대사 언어 / 대사 / 소리 / 종료 상태 및 연결 / 연속성 및 배제 요소.

## 표시 순서

각 씬 제목 → 읽기용 나레이션 → 펼쳐진 영문 영상 프롬프트 → 접힌 한국어 번역 → 모델 추천과 이유 → 사용자가 선택한 이미지 종류·수량 → 이미지 프롬프트와 시간·모델 메타데이터. 영상 프롬프트 첫 줄은 `씬 1:`처럼 표시한다.

각 씬의 발화에는 `pre`/`code`를 쓰지 않는다. 웹 상단에 전체 음성변환용 대본을 복사용 코드블록으로 한 번 둔다. ‘나레이션 먼저 읽기’와 하단 중복 대본은 만들지 않는다. 제목 후보는 정확히 5개, 설명에는 관련 해시태그를 포함하고 논문 링크는 넣지 않는다.

무대사·별도 나레이션 영상의 프롬프트에는 다음을 포함한다.

```text
DIALOGUE: NONE.
NARRATION: NONE. VOICEOVER: NONE.
Audio: no narration, no dialogue, no voice-over, no spoken words.
```

등장인물 대사가 요청된 영화에는 음성 전체 금지 문장을 적용하지 않는다.

## 다른 구도의 설명 이미지

첫 프레임을 선택한 경우에는 첫 프레임 프롬프트와 별도 블록으로 출력한다. `관련 이미지 1…N`으로 번호를 붙이고 선택한 장수만큼 각각 실제 생성한다. 첫 프레임이 없으면 시작 이미지 블록을 만들지 않고 기본 구도·기준 시트와 다른 관련 이미지를 기준으로 시점과 설명 방식의 차이를 적는다.

```text
SCENE: [번호] | ROLE: Related explanatory image [1…N]
REFERENCE: [production reference ID/version; reference image actually attached]
VIEWPOINT CHANGE: [opening angle/framing] → [clearly different angle/framing]
EXPLANATION CHANGE: [visible exterior] → [cutaway / density comparison / light-path diagram / exploded view]
SUBJECT & ACTION: [one still image explaining this scene, consistent subject identity]
COMPOSITION & LIGHT: [new composition; correct light direction and physical relationships]
AVOID: [If a first frame exists, near-duplicate of it; otherwise near-duplicate of the established base composition], simple crop, mirroring, color-only change, inaccurate mechanism, text, watermark.
```

## 효과음 예시 (영문·한국어 프롬프트에 동일 반영)

```text
SFX: Editorial, non-diegetic sound design. 0–1s short low impact for the reveal; 2–4s soft airy sweep following the diagram transition; 5–6s subtle click at the highlighted contact, quick decay. Moderate volume, space for separately added narration.
NARRATION: NONE. VOICEOVER: NONE. DIALOGUE: NONE.
Audio: no narration, no dialogue, no voice-over, no spoken words. MUSIC OFF.
```

이 예시를 모든 씬에 복사하지 말고 실제 행동에 맞게 효과음·시점을 바꾼다. 사용자 무음 요청이 없으면 음성 금지와 함께 전체 무음 지시를 넣지 않는다.

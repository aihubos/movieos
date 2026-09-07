#!/usr/bin/env python3
"""MovieOS 질문을 파일에 보존한다. JSON 입력은 stdin, 상태·카드 경로는 stdout."""
import argparse
import json
import os
from pathlib import Path
import sys
import tempfile


FIELDS = {"video_type", "purpose", "duration", "story", "style", "language",
          "first_frame", "related_images", "parent_path", "aspect_ratio"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_value(field, value):
    require(field in FIELDS, "알 수 없는 선택 항목")
    if field == "first_frame":
        require(type(value) is bool, "첫 프레임은 true 또는 false")
    elif field == "related_images":
        counts = value.values() if isinstance(value, dict) else [value]
        if isinstance(value, dict):
            require(bool(value) and all(str(k).isdigit() and int(k) > 0 for k in value),
                    "씬별 수량의 키는 양의 씬 번호")
        require(all(type(n) is int and n >= 0 for n in counts), "관련 이미지는 0 이상의 정수")
    else:
        require(isinstance(value, str) and bool(value.strip()), "빈 선택은 저장할 수 없음")
        if field == "parent_path":
            require(Path(value).is_absolute(), "저장 위치는 전체 경로 필요")


def atomic_write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                     delete=False) as file:
        temporary = Path(file.name)
        try:
            file.write(text)
            file.flush()
            os.fsync(file.fileno())
            os.replace(temporary, path)
        finally:
            temporary.unlink(missing_ok=True)


def question_text(question):
    lines = [f"# {question['id']} · {question['title']}", ""]
    for number, option in enumerate(question["options"], 1):
        lines.append(f"{number}. {option['label']}")
    lines += ["", "질문 번호와 선택 번호로 답할 수 있습니다. 직접 입력은 실제 값도 적어 주세요.",
              f"예: {question['id']} 1", ""]
    return "\n".join(lines)


def render(session, state):
    for question in state["questions"]:
        card = session / f"{question['id']}.md"
        expected = question_text(question)
        if card.exists():
            require(card.read_text(encoding="utf-8") == expected, "이전 질문 카드가 변경됨: " + str(card))
        else:
            atomic_write(card, expected)
    lines = ["# MovieOS 선택 현황", "", "## 확정된 선택", ""]
    lines += [f"- {key}: {json.dumps(value, ensure_ascii=False)}" for key, value in state["answers"].items()]
    lines += ["", question_text(state["pending"]) if state["pending"] else "현재 표시 중인 질문 없음. 미응답 필수 항목은 스킬의 순서로 확인하세요."]
    atomic_write(session / "current.md", "\n".join(lines) + "\n")


def run(session, action, payload):
    session = Path(session).resolve()
    path = session / "state.json"
    # ponytail: 한 세션은 담당 에이전트 하나만 기록. 동시 작성이 필요해지면 파일 잠금 추가.
    require(path.exists() or action in {"ask", "record"}, "저장된 질문 세션이 없음")
    state = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {
        "answers": {}, "pending": None, "questions": []}
    require(isinstance(payload, dict), "입력은 JSON 객체")
    if action == "ask":
        require(set(payload) == {"field", "title", "options"}, "ask 입력: field, title, options")
        require(payload["field"] in FIELDS, "알 수 없는 질문 항목")
        require(isinstance(payload["title"], str) and payload["title"].strip(), "질문 제목 필요")
        require(isinstance(payload["options"], list) and len(payload["options"]) >= 2, "선택지 2개 이상 필요")
        for option in payload["options"]:
            require(isinstance(option, dict) and set(option) == {"label", "value"}, "선택지: label, value")
            require(isinstance(option["label"], str) and option["label"].strip(), "선택지 설명 필요")
            if option["value"] is not None:
                validate_value(payload["field"], option["value"])
        if state["pending"]:
            require(all(state["pending"][key] == value for key, value in payload.items()),
                    "미응답 질문이 있음. show로 복구하거나 먼저 답변을 반영하세요")
        else:
            require(payload["field"] not in state["answers"], "이미 답변한 항목. 수정은 record 사용")
            state["pending"] = dict(payload, id=f"Q{len(state['questions']) + 1:03d}-{payload['field']}")
            state["questions"].append(state["pending"])
    elif action in {"answer", "record"}:
        if action == "answer":
            question = state["pending"]
            require(question is not None and payload.get("question_id") == question["id"],
                    "현재 미응답 질문 ID와 다름. 오래되거나 중복된 답변을 적용하지 않았습니다")
            require(set(payload) in ({"question_id", "option"}, {"question_id", "value"}),
                    "answer 입력: question_id와 option 또는 value 하나")
            if "option" in payload:
                number = payload["option"]
                require(type(number) is int and 1 <= number <= len(question["options"]), "선택 번호 범위 오류")
                value = question["options"][number - 1]["value"]
                require(value is not None, "직접 입력의 실제 값을 value로 보내세요")
            else:
                value = payload["value"]
            answers = {question["field"]: value}
        else:
            require(set(payload) == {"answers"} and isinstance(payload["answers"], dict)
                    and bool(payload["answers"]), "record 입력: 비어 있지 않은 answers 객체")
            answers = payload["answers"]
        for field, value in answers.items():
            validate_value(field, value)
        state["answers"].update(answers)
        if state["pending"] and state["pending"]["field"] in answers:
            state["pending"] = None
    else:
        require(action == "show", "지원하지 않는 명령")
    if action != "show":
        atomic_write(path, json.dumps(state, ensure_ascii=False, indent=2) + "\n")
    render(session, state)
    return {"state": state, "current_card": str(session / "current.md"),
            "question_card": str(session / f"{state['pending']['id']}.md") if state["pending"] else None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("session", type=Path)
    parser.add_argument("action", choices=["ask", "answer", "record", "show"])
    args = parser.parse_args()
    try:
        result = run(args.session, args.action, {} if args.action == "show" else json.load(sys.stdin))
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, OSError, KeyError, TypeError) as error:
        parser.exit(1, f"MovieOS: {error}\n")


if __name__ == "__main__":
    main()

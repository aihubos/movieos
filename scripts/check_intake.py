#!/usr/bin/env python3
"""실행: python3 scripts/check_intake.py — 임시 폴더에서 질문 재개·입력을 확인."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def main():
    with tempfile.TemporaryDirectory() as directory:
        session = Path(directory) / "선택 세션"

        def call(action, payload=None, succeeds=True):
            result = subprocess.run(
                [sys.executable, str(Path(__file__).with_name("intake.py")), str(session), action],
                input=json.dumps(payload, ensure_ascii=False), text=True, capture_output=True)
            assert (result.returncode == 0) == succeeds, result.stderr
            return json.loads(result.stdout) if succeeds else None

        call("record", {"answers": {"duration": "45초", "parent_path": "/tmp/영상 모음"}})
        first = {"field": "first_frame", "title": "첫 프레임을 생성할까요?", "options": [
            {"label": "생성함", "value": True}, {"label": "생성 안 함", "value": False}]}
        a = call("ask", first)
        first_id = a["state"]["pending"]["id"]
        original_card = Path(a["question_card"]).read_text()
        assert call("show")["state"] == a["state"]
        assert call("ask", first)["state"] == a["state"]

        related = {"field": "related_images", "title": "씬마다 관련 이미지 몇 장?", "options": [
            {"label": "0장", "value": 0}, {"label": "1장", "value": 1},
            {"label": "직접 입력", "value": None}]}
        call("ask", related, succeeds=False)
        assert call("show")["state"] == a["state"]
        answered = call("answer", {"question_id": first_id, "option": 2})
        assert answered["state"]["answers"]["first_frame"] is False
        assert answered["state"]["pending"] is None
        b = call("ask", related)
        related_id = b["state"]["pending"]["id"]
        for payload in [{"question_id": first_id, "option": 1},
                        {"question_id": related_id, "option": 3},
                        {"question_id": related_id, "option": 99},
                        {"question_id": related_id, "value": -1},
                        {"question_id": related_id, "value": 1.5},
                        {"question_id": related_id, "value": True}]:
            call("answer", payload, succeeds=False)
            assert call("show")["state"] == b["state"]

        corrected = call("record", {"answers": {"duration": "60초", "language": "한국어"}})
        assert corrected["state"]["pending"] == b["state"]["pending"]
        call("record", {"answers": {"parent_path": "기존 폴더"}}, succeeds=False)
        assert call("show")["state"] == corrected["state"]
        Path(b["current_card"]).unlink()
        Path(b["question_card"]).unlink()
        recovered = call("show")
        assert recovered["state"] == corrected["state"]
        assert Path(recovered["question_card"]).is_file()
        assert Path(recovered["current_card"]).is_file()
        assert Path(a["question_card"]).read_text() == original_card
        done = call("answer", {"question_id": related_id, "option": 1})
        assert done["state"]["answers"]["related_images"] == 0
        assert done["state"]["answers"]["first_frame"] is False
        assert done["state"]["answers"]["duration"] == "60초"
        call("answer", {"question_id": related_id, "option": 1}, succeeds=False)
        assert call("show")["state"] == done["state"]
    print("PASS: 재실행·질문 복구·기존 답 보존·0장·생성 안 함·잘못된 답 차단")


if __name__ == "__main__":
    main()

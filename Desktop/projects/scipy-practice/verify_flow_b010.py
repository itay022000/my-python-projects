#!/usr/bin/env python3
"""
QA — B010 learner-interface flow (scipy-practice).

Covers strikes, empty input, hints, skip answer, partial exit, session footer.

Run: python3 verify_flow_b010.py
"""

from __future__ import annotations

import io
import sys
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from engine import Question, QuestionOutcome, ask_question
from exercise_session import run_exercise_questions
from session_common import classify_special_input

_pass = 0
_fail = 0
_failures: list[str] = []

WRONG = "___qa_wrong___"


def record(name: str, ok: bool, detail: str = "") -> None:
    global _pass, _fail
    if ok:
        _pass += 1
    else:
        _fail += 1
        line = f"FAIL: {name}"
        if detail:
            line += f" — {detail}"
        _failures.append(line)


def test_special_commands() -> None:
    record("skip", classify_special_input("skip") == "skip")
    record("Skip", classify_special_input("Skip") == "skip")
    record("exit", classify_special_input("exit") == "exit")
    record("Quit", classify_special_input("Quit") == "exit")


def test_constants_no_hint() -> None:
    from exercises import PRACTICE_BUILDERS

    namespace, questions = PRACTICE_BUILDERS["constants"]()
    q = questions[0]
    buf = io.StringIO()
    with patch("builtins.input", side_effect=[WRONG, WRONG, WRONG]):
        with redirect_stdout(buf):
            ask_question(
                question_num=1,
                total=1,
                title=q.text,
                hint=q.hint,
                namespace=namespace,
                check_func=q.check,
                first=True,
                correct_answer=q.correct_answer,
            )
    record("constants no hint", "Hint:" not in buf.getvalue())


def test_empty_no_strike() -> None:
    def check(_):
        return False, "nope"

    buf = io.StringIO()
    with patch("builtins.input", side_effect=["", "", WRONG, WRONG, WRONG]):
        with redirect_stdout(buf):
            outcome = ask_question(
                question_num=1,
                total=1,
                title="Compute 1",
                hint="nudge",
                namespace={},
                check_func=check,
                first=True,
                correct_answer="1",
            )
    out = buf.getvalue()
    record("empty no strike", out.count("attempt 1/3") >= 1)
    record("strike 3 outcome", outcome == QuestionOutcome.NOT_COMPLETED)
    record("hint once", out.count("Hint:") == 1)


def test_skip_shows_answer() -> None:
    buf = io.StringIO()
    with patch("builtins.input", side_effect=["skip"]):
        with redirect_stdout(buf):
            outcome = ask_question(
                question_num=1,
                total=1,
                title="Compute 1",
                hint="hint",
                namespace={},
                check_func=lambda r: (r == 1, ""),
                first=True,
                correct_answer="1",
            )
    out = buf.getvalue()
    record("skip outcome", outcome == QuestionOutcome.NOT_COMPLETED)
    record("skip answer", "Correct answer: 1" in out)


def test_exit_partial_score() -> None:
    questions = [
        Question("Q1", lambda r: (r == 1, ""), "h", correct_answer="1"),
        Question("Q2", lambda r: (r == 2, ""), "h", correct_answer="2"),
    ]
    buf = io.StringIO()
    with patch("builtins.input", side_effect=["", "1", "exit"]):
        with redirect_stdout(buf):
            run_exercise_questions({}, questions, background='test')
    out = buf.getvalue()
    record("exit line", "Session exited." in out)
    record("exit counts current", "Not completed: 1 (of 2 questions)" in out)
    record("no full footer", "Session Statistics" not in out)


def test_session_footer() -> None:
    questions = [
        Question("Q1", lambda r: (r == 1, ""), "h", correct_answer="1"),
        Question("Q2", lambda r: (r == 2, ""), "h", correct_answer="2"),
    ]
    buf = io.StringIO()
    with patch("builtins.input", side_effect=["", "1", "2"]):
        with redirect_stdout(buf):
            run_exercise_questions({}, questions, background='test')
    out = buf.getvalue()
    record("footer", "Session Statistics" in out)
    record("completed 2", "Completed successfully: 2 (100%)" in out)
    record("not completed pct", "Not completed: 0 (0%)" in out)


def test_strike_copy() -> None:
    buf = io.StringIO()
    with patch("builtins.input", side_effect=[WRONG, WRONG, WRONG]):
        with redirect_stdout(buf):
            ask_question(
                question_num=1,
                total=1,
                title="Compute 1",
                hint="hint text",
                namespace={},
                check_func=lambda r: (r == 1, ""),
                first=True,
                correct_answer="1",
            )
    out = buf.getvalue()
    record("strike msg", "Incorrect answer (attempt 1/3)" in out)
    record("strike 3 answer", "Correct answer: 1" in out)


def test_correct_only() -> None:
    buf = io.StringIO()
    with patch("builtins.input", return_value="1"):
        with redirect_stdout(buf):
            ask_question(
                question_num=1,
                total=1,
                title="Compute 1",
                hint="hint",
                namespace={},
                check_func=lambda r: (r == 1, "extra feedback"),
                first=True,
                correct_answer="1",
            )
    out = buf.getvalue()
    record("correct line", "✓ Correct!" in out)
    record("no extra feedback", "extra feedback" not in out)


def main() -> None:
    test_special_commands()
    test_constants_no_hint()
    test_empty_no_strike()
    test_skip_shows_answer()
    test_exit_partial_score()
    test_session_footer()
    test_strike_copy()
    test_correct_only()

    print("=" * 70)
    print("QA — B010 flow (scipy-practice)")
    print("=" * 70)
    print(f"Passed: {_pass}/{_pass + _fail}")
    print(f"Failed: {_fail}/{_pass + _fail}")
    if _failures:
        print("\nFailures:")
        for line in _failures:
            print(f"  {line}")
    print("=" * 70)
    if _fail:
        sys.exit(1)
    print("verify_flow_b010: OK.")


if __name__ == "__main__":
    main()

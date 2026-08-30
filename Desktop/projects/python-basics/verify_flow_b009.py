#!/usr/bin/env python3
"""
QA — B009 learner-interface flow (python-basics).

Covers skip, exit, empty input, hints, compound skip, partial exit score.

Run: python3 verify_flow_b009.py
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

from validators import checker_basic
from hints import resolve_hint
from session_common import SessionExit, classify_special_input
from engine import QuestionOutcome, _run_one_simple_exercise, run_mixed_units_session, run_simple_exercises

_make_exercise = checker_basic.make_exercise
WRONG = "___qa_wrong___"

_pass = 0
_fail = 0
_failures: list[str] = []


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
    record("SKIP rejected", classify_special_input("SKIP") is None)


def test_empty_no_strike() -> None:
    ex = _make_exercise("x = 1", "x = 1")

    def always_wrong(_: str):
        return False, "nope"

    ex["check"] = always_wrong
    buf = io.StringIO()
    with patch("builtins.input", side_effect=["", "", WRONG, WRONG, WRONG]):
        with redirect_stdout(buf):
            outcome = _run_one_simple_exercise(
                ex, 1, 1,
                max_mistakes=3,
                prompt_label="Your code",
                input_fn=input,
                hint="nudge",
            )
    out = buf.getvalue()
    record("empty no strike", out.count("attempt 1/3") >= 1)
    record("strike 3 outcome", outcome == QuestionOutcome.NOT_COMPLETED)
    record("hint once", out.count("Hint:") == 1)


def test_batch1_no_hint() -> None:
    ex = _make_exercise("x = 1", "x = 1")
    record("batch1 no hint", resolve_hint(1, ex) is None)


def test_batch2_no_hint() -> None:
    ex = _make_exercise("x = 1", "x = 1")
    record("batch2 no hint", resolve_hint(2, ex) is None)


def test_batch3_no_hint() -> None:
    ex = _make_exercise("x = 1", "x = 1")
    record("batch3 no hint", resolve_hint(3, ex) is None)


def test_skip_simple() -> None:
    ex = _make_exercise("x = 1", "x = 1")
    buf = io.StringIO()
    with patch("builtins.input", side_effect=["skip"]):
        with redirect_stdout(buf):
            outcome = _run_one_simple_exercise(
                ex, 1, 2,
                max_mistakes=3,
                prompt_label="Your code",
                input_fn=input,
                hint=None,
            )
    out = buf.getvalue()
    record("skip outcome", outcome == QuestionOutcome.NOT_COMPLETED)
    record("skip message", "Skipping question." in out)
    record("skip shows answer", "Correct answer: x = 1" in out)


def test_exit_partial_score() -> None:
    exercises = [
        _make_exercise("a", "a = 1"),
        _make_exercise("b", "b = 2"),
    ]
    buf = io.StringIO()
    with patch("builtins.input", side_effect=["a = 1", "exit"]):
        with redirect_stdout(buf):
            try:
                run_simple_exercises(
                    exercises,
                    max_mistakes=3,
                    hint_for=lambda ex: None,
                )
            except SessionExit:
                pass
    out = buf.getvalue()
    record("exit line", "Session exited." in out)
    record("partial completed", "Completed successfully: 1" in out)
    record("return menu", "Returning to main menu" in out)


def test_compound_skip_all_answers() -> None:
    from validators import checker_mixed_lists

    unit = checker_mixed_lists.make_compound(
        "Tuple change (3 steps)",
        [
            ("step 1", "lst = list(t)"),
            ("step 2", "lst[1] = 99"),
            ("step 3", "t = tuple(lst)"),
        ],
    )
    buf = io.StringIO()
    with patch("builtins.input", side_effect=["skip"]):
        with redirect_stdout(buf):
            passed, failed = run_mixed_units_session(
                [unit],
                max_mistakes=3,
                hint_for=lambda ex: resolve_hint(5, ex),
            )
    out = buf.getvalue()
    record("compound skip failed", failed == 1 and passed == 0)
    record("all line answers", "Line 1: lst = list(t)" in out and "Line 3: t = tuple(lst)" in out)


def test_strike_copy() -> None:
    ex = _make_exercise("x = 1", "x = 1")
    buf = io.StringIO()
    with patch("builtins.input", side_effect=[WRONG, WRONG, WRONG]):
        with redirect_stdout(buf):
            _run_one_simple_exercise(
                ex, 1, 1,
                max_mistakes=3,
                prompt_label="Your code",
                input_fn=input,
                hint=None,
            )
    out = buf.getvalue()
    record("b009 strike msg", "Incorrect answer (attempt 1/3)" in out)
    record("no three mistakes banner", "Three mistakes" not in out)


def test_max_attempts_for_word() -> None:
    from engine import max_attempts_for

    record("word is 1", max_attempts_for({"answer_type": "word"}, 3) == 1)
    record("code is 3", max_attempts_for({}, 3) == 3)


def test_batch10_hint_coverage() -> None:
    from batch_10_exercises import (
        POOL_1_ACCESS_ARRAY,
        POOL_2_ACCESS_MODIFY_ARRAY,
        POOL_3_ARRAY_LEN,
        POOL_4_ARRAY_ADD,
        POOL_5_ARRAY_POP,
        POOL_6_ARRAY_REMOVE,
        POOL_7_CURRENT_TIME,
        POOL_8_CURRENT_YEAR,
        POOL_9_CURRENT_MONTH,
        POOL_10_CURRENT_DAY,
        POOL_11_CREATE_DATE,
        POOL_12_STRFTIME_WEEKDAY,
        POOL_13_STRFTIME_MONTH_NAME,
        POOL_14_STRFTIME_HOUR,
        POOL_15_JSON_LOADS,
        POOL_16_JSON_DUMPS,
        POOL_17_JSON_FORMATTED,
        POOL_18_JSON_FORMATTED_SORTED,
        POOL_19_TRY_EXCEPT,
        POOL_20_TRY_EXCEPT_EXCEPT,
        POOL_21_TRY_EXCEPT_ELSE,
        POOL_22_TRY_EXCEPT_FINALLY,
        POOL_23_RAISE,
        POOL_24_INPUT_NO_PROMPT,
        POOL_25_INPUT_WITH_PROMPT,
        _make_simple,
    )

    pools = (
        POOL_1_ACCESS_ARRAY
        + POOL_2_ACCESS_MODIFY_ARRAY
        + POOL_3_ARRAY_LEN
        + POOL_4_ARRAY_ADD
        + POOL_5_ARRAY_POP
        + POOL_6_ARRAY_REMOVE
        + POOL_7_CURRENT_TIME
        + POOL_8_CURRENT_YEAR
        + POOL_9_CURRENT_MONTH
        + POOL_10_CURRENT_DAY
        + POOL_11_CREATE_DATE
        + POOL_12_STRFTIME_WEEKDAY
        + POOL_13_STRFTIME_MONTH_NAME
        + POOL_14_STRFTIME_HOUR
        + POOL_15_JSON_LOADS
        + POOL_16_JSON_DUMPS
        + POOL_17_JSON_FORMATTED
        + POOL_18_JSON_FORMATTED_SORTED
        + POOL_19_TRY_EXCEPT
        + POOL_20_TRY_EXCEPT_EXCEPT
        + POOL_21_TRY_EXCEPT_ELSE
        + POOL_22_TRY_EXCEPT_FINALLY
        + POOL_23_RAISE
        + POOL_24_INPUT_NO_PROMPT
        + POOL_25_INPUT_WITH_PROMPT
    )
    missing: list[str] = []
    for item in pools:
        if isinstance(item, dict) and "parts" in item:
            for part in item["parts"]:
                if resolve_hint(10, part) is None:
                    missing.append(part["question"])
        elif isinstance(item, tuple):
            ex = _make_simple(*item)
            if resolve_hint(10, ex) is None:
                missing.append(item[0])
    record("batch10 all pools hinted", not missing, ", ".join(missing[:3]))


def test_tf_one_attempt() -> None:
    from validators import make_boolean_word_check

    ex = {
        "question": "What is the truth value of 0? Answer with one word: True or False.",
        "expected": "False",
        "check": make_boolean_word_check("False"),
        "answer_type": "word",
    }
    buf = io.StringIO()
    with patch("builtins.input", side_effect=[WRONG]):
        with redirect_stdout(buf):
            outcome = _run_one_simple_exercise(
                ex, 8, 12,
                max_mistakes=1,
                prompt_label="Your answer",
                input_fn=input,
                hint="bool nudge",
            )
    out = buf.getvalue()
    record("tf one attempt", outcome == QuestionOutcome.NOT_COMPLETED)
    record("tf attempt 1/1", "attempt 1/1" in out)
    record("tf hint and answer", "Hint:" in out and "Correct answer: False" in out)
    record("tf no try again", "Try again" not in out)


def main() -> None:
    test_special_commands()
    test_empty_no_strike()
    test_batch1_no_hint()
    test_batch2_no_hint()
    test_batch3_no_hint()
    test_skip_simple()
    test_exit_partial_score()
    test_compound_skip_all_answers()
    test_strike_copy()
    test_max_attempts_for_word()
    test_batch10_hint_coverage()
    test_tf_one_attempt()

    print("=" * 70)
    print("QA — B009 flow (python-basics)")
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
    print("verify_flow_b009: OK (skip, exit, empty, hints, compound skip, strike copy).")


if __name__ == "__main__":
    main()

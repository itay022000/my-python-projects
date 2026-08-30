#!/usr/bin/env python3
"""
QA Developer — B008 learner-interface flow (matplotlib-practice).

Covers per-question strikes, empty input, skip series, exit, hints, S2 stats.
Uses mocked input() against real exercise modules.

Run: python3 scripts/qa_flow_b008.py
"""

from __future__ import annotations

import io
import random
import sys
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from engine import ask_code_question
from session_common import QuestionOutcome, classify_special_input
from exercises.histogram_exercises import HistogramExercises

WRONG = "___qa_wrong___"
SEED = 42

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


def _run_histogram(inputs: list[str]) -> str:
    random.seed(SEED)
    mod = HistogramExercises()
    buf = io.StringIO()
    with patch("builtins.input", side_effect=[""] + inputs):
        with redirect_stdout(buf):
            mod.start_exercises()
    return buf.getvalue()


def test_special_commands() -> None:
    record("skip casing", classify_special_input("skip") == "skip")
    record("Skip casing", classify_special_input("Skip") == "skip")
    record("exit casing", classify_special_input("exit") == "exit")
    record("quit casing", classify_special_input("Quit") == "exit")
    record("SKIP rejected", classify_special_input("SKIP") is None)


def test_run_code_step_empty_no_strike() -> None:
    buf = io.StringIO()

    def always_wrong(_: str):
        return False, "Invalid format"

    with patch("builtins.input", side_effect=["", "", WRONG, WRONG, WRONG]):
        with redirect_stdout(buf):
            outcome = ask_code_question(
                always_wrong,
                correct_answer="ok",
                hint="nudge",
            )
    out = buf.getvalue()
    record("empty no strike", out.count("attempt 1/3") >= 1)
    record("empty then strike 3", outcome == QuestionOutcome.NOT_COMPLETED)
    record("hint once", out.count("Hint:") == 1)


def test_run_code_step_show_no_hint() -> None:
    from engine import verify_step_show

    buf = io.StringIO()
    with patch("builtins.input", side_effect=[WRONG, WRONG, WRONG]):
        with redirect_stdout(buf):
            outcome = ask_code_question(
                verify_step_show,
                correct_answer="plt.show()",
                hint=None,
            )
    out = buf.getvalue()
    record("show step no hint", "Hint:" not in out)
    record("show strike 3 reveals", outcome == QuestionOutcome.NOT_COMPLETED)


def test_three_wrong_continues_series() -> None:
    """Three wrong on step 1 must not skip the whole series (B008)."""
    out = _run_histogram(
        [WRONG, WRONG, WRONG, "plt.hist(x)", "plt.show()", "exit"]
    )
    record("answer on strike 3", "Correct answer:" in out)
    record("reaches step 2", "Step 2/" in out)
    record("no old series skip msg", "Skipping to the next exercise" not in out)
    record("with help bucket", "Completed with help: 1" in out)


def test_all_revealed_not_completed() -> None:
    """Finish a series with 0 correct steps → Not completed (not with help)."""
    out = _run_histogram(
        [WRONG, WRONG, WRONG, WRONG, WRONG, WRONG, WRONG, WRONG, WRONG, "exit"]
    )
    record("all reveal no with help", "Completed with help: 0" in out)
    record("all reveal not completed", "Not completed: 2" in out)


def test_skip_series() -> None:
    out = _run_histogram(["skip", "skip", "skip"])
    record("skip message", out.count("Skipping series.") == 3)
    record("skip reveals current step only", out.count("Correct answer:") == 3)
    record("skip does not continue series", "Step 2/" not in out)
    record("not completed stats", "Not completed: 3" in out)


def test_exit_partial_score() -> None:
    out = _run_histogram(["exit"])
    record("exit line", "Session exited." in out)
    record("three buckets", "Completed with help:" in out)
    record("entered series counted", "Not completed: 1 (of 1 series)" in out)
    record("return menu", "Returning to main menu" in out)


def test_completed_clean() -> None:
    random.seed(SEED)
    mod = HistogramExercises()
    ex = mod.exercises[0]
    expected1 = mod._expected_step1(ex)
    inputs = [expected1, "plt.hist(x)", "plt.show()"] + ["exit"] * 2
    buf = io.StringIO()
    with patch("builtins.input", side_effect=[""] + inputs):
        with patch.object(mod, "generate_exercises"):
            with redirect_stdout(buf):
                mod.start_exercises()
    out = buf.getvalue()
    record("completed footer", "Completed successfully: 1" in out and "Completed with help: 0" in out)


def main() -> None:
    test_special_commands()
    test_run_code_step_empty_no_strike()
    test_run_code_step_show_no_hint()
    test_three_wrong_continues_series()
    test_all_revealed_not_completed()
    test_skip_series()
    test_exit_partial_score()
    test_completed_clean()

    print("=" * 70)
    print("QA Developer — B008 flow (matplotlib-practice)")
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
    print("verify_flow_b008: OK (strikes, empty, skip, exit, hints, S2 stats).")


if __name__ == "__main__":
    main()

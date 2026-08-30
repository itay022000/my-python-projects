#!/usr/bin/env python3
"""
QA Developer — B002 exercise flow (skip / exit / wrong / correct).

5 exercises × 8 questions × 4 cases = 160 checks via mocked builtins.input.
No subprocess — calls PandasPractice exercise methods directly.

Run from project root: python3 scripts/qa_flow_b002.py
"""

from __future__ import annotations

import io
import os
import random
import re
import sys
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

os.environ.setdefault("MPLBACKEND", "Agg")

import validators as _validators_mod
from main import PandasPractice

_REAL_EXECUTE_PANDAS = _validators_mod.execute_pandas_code

QUESTIONS_PER_EXERCISE = 8


def _flow_execute_pandas_code(
    df,
    code,
    expected_result=None,
    description="",
    include_plotting=False,
):
    """Flow QA: plot questions are graded by exact match; tolerate broken matplotlib wheels."""
    result, error = _REAL_EXECUTE_PANDAS(
        df, code, expected_result, description, include_plotting
    )
    if include_plotting and error:
        return None, None
    return result, error


SEED = 42
WRONG = "___qa_wrong_b002___"
HEAD_TAIL_N = 10

_pass = 0
_fail = 0
_failures: list[str] = []

EXERCISE_METHODS = {
    1: "exercise_1_basic_operations",
    2: "exercise_2_filtering",
    3: "exercise_3_sorting_and_selection",
    4: "exercise_4_data_manipulation",
    5: "exercise_5_data_cleaning",
}

STATIC_CORRECT: dict[tuple[int, int], list[str]] = {
    (1, 2): ["df.shape"],
    (1, 3): ["df.columns"],
    (1, 4): ["df.dtypes"],
    (1, 6): ["df.describe()"],
}


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


def question_marker(task_num: int, total: int = QUESTIONS_PER_EXERCISE) -> str:
    return f"--- Question {task_num}/{total} ---"


def parse_skip_answers(stdout: str) -> list[str]:
    """Extract printed correct-answer lines from skip / failure output."""
    answers: list[str] = []
    for line in stdout.splitlines():
        stripped = line.strip()
        if stripped.startswith("Correct answer:"):
            answers.append(stripped.split("Correct answer:", 1)[1].strip())
    return answers


def _input_queue(initial: list[str]) -> tuple[list[str], callable]:
    queue = list(initial) + [""] * 40

    def _fake_input(_prompt: str = "") -> str:
        return queue.pop(0) if queue else ""

    return queue, _fake_input


def golden_for_task(ex_num: int, task_num: int) -> str | None:
    inputs = ["skip"] * task_num + ["exit"]
    stdout = run_exercise_flow(ex_num, inputs)
    parsed = parse_skip_answers(stdout)
    if parsed:
        return parsed[-1]
    if (ex_num, task_num) in STATIC_CORRECT:
        return STATIC_CORRECT[(ex_num, task_num)][0]
    return None


def section_for_task_only(stdout: str, task_num: int) -> str:
    start_match = re.search(rf"--- Question {task_num}/\d+ ---", stdout)
    if not start_match:
        return stdout
    start = start_match.start()
    rest = stdout[start:]
    next_match = re.search(rf"\n--- Question {task_num + 1}/\d+ ---", rest)
    end = start + next_match.start() if next_match else len(stdout)
    return stdout[start:end]


def correct_inputs_for_task(ex_num: int, task_num: int, golden: str) -> list[str]:
    if (ex_num, task_num) in STATIC_CORRECT:
        return STATIC_CORRECT[(ex_num, task_num)]
    if ex_num == 1 and task_num in (1, 5):
        primary = golden
        attempts = (
            [f"df.head({n})" for n in range(5, 16)]
            if task_num == 1
            else [f"df.tail({n})" for n in range(5, 16)]
        )
        if primary in attempts:
            return [primary]
        return attempts
    return [golden]


def run_exercise_flow(ex_num: int, task_inputs: list[str]) -> str:
    random.seed(SEED)
    app = PandasPractice()
    method = getattr(app, EXERCISE_METHODS[ex_num])
    buf = io.StringIO()
    _, fake_input = _input_queue(task_inputs)

    def _choice(seq):
        items = list(seq)
        if len(items) == 0:
            raise IndexError("empty sequence in test")
        return items[0]

    def _sample(population, k):
        pop = list(population)
        return pop[: min(k, len(pop))]

    patches = [
        patch("builtins.input", side_effect=fake_input),
        patch.object(PandasPractice, "wait_for_esc", lambda self: None),
        patch("random.randint", return_value=HEAD_TAIL_N),
        patch("random.choice", side_effect=_choice),
        patch("random.sample", side_effect=_sample),
        patch("validators.execute_pandas_code", side_effect=_flow_execute_pandas_code),
    ]
    for p in patches:
        p.start()
    try:
        with redirect_stdout(buf):
            method()
    except StopIteration:
        pass
    finally:
        for p in patches:
            p.stop()
    return buf.getvalue()


def build_inputs(ex_num: int, task_num: int, case: str, golden: str) -> list[str]:
    prefix = ["skip"] * (task_num - 1)
    if case == "wrong":
        return prefix + [WRONG, WRONG, WRONG, "exit"]
    if case == "skip":
        return prefix + ["skip", "exit"]
    if case == "exit":
        return prefix + ["exit"]
    if case == "correct":
        answers = correct_inputs_for_task(ex_num, task_num, golden)
        return prefix + answers + ["exit"]
    raise ValueError(case)


def test_flow_case(ex_num: int, task_num: int, case: str, golden: str) -> None:
    name = f"ex{ex_num} task{task_num} {case}"
    inputs = build_inputs(ex_num, task_num, case, golden)
    stdout = run_exercise_flow(ex_num, inputs)
    section = section_for_task_only(stdout, task_num)

    if case == "wrong":
        count = section.count("Correct answer:")
        record(name, count == 1, f"Correct answer count={count} in question section")
    elif case == "skip":
        record(
            name,
            "Skipping question." in section and section.count("Correct answer:") == 1,
            f"skipped={'Skipping question.' in section}, answers={section.count('Correct answer:')}",
        )
    elif case == "exit":
        record(
            name,
            "Session exited." in stdout and "Completed successfully:" in stdout,
            "missing exit message",
        )
    elif case == "correct":
        fresh_golden = golden_for_task(ex_num, task_num) or golden
        for code in correct_inputs_for_task(ex_num, task_num, fresh_golden):
            trial_inputs = ["skip"] * (task_num - 1) + [code, "exit"]
            trial_out = run_exercise_flow(ex_num, trial_inputs)
            trial_section = section_for_task_only(trial_out, task_num)
            if "✓ Correct!" in trial_section:
                record(name, True)
                return
        record(name, False, "success marker not found in question section")


def main() -> int:
    os.chdir(_ROOT)

    print("=" * 70)
    print("QA Developer — B002 flow (5×8×4 = 160)")
    print("=" * 70)

    cases = ("wrong", "skip", "exit", "correct")
    for ex in range(1, 6):
        for task in range(1, 9):
            golden = golden_for_task(ex, task) or "df.shape"
            for case in cases:
                test_flow_case(ex, task, case, golden)

    total = _pass + _fail
    print(f"\nPassed: {_pass}/{total}")
    print(f"Failed: {_fail}/{total}")
    if _failures:
        print("\nFailures (first 25):")
        for line in _failures[:25]:
            print(f"  {line}")
        if len(_failures) > 25:
            print(f"  ... and {len(_failures) - 25} more")
    print("=" * 70)
    return 1 if _fail else 0


if __name__ == "__main__":
    sys.exit(main())

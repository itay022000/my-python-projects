"""
Skip and exit behavior for every practice question in scipy-practice.

For each of the 29 questions (all six modules):
  - skip at that question advances to the next question (or exercise footer on last)
  - exit at that question aborts the exercise without the completion footer

Run from this directory:
  python3 verify_skip_exit_behavior.py
"""

from __future__ import annotations

from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from engine import run_exercise_questions
from exercises import PRACTICE_BUILDERS

EXERCISE_ORDER = ["constants", "optimize", "sparse", "csgraph", "spatial", "interpolate"]


def _run_exercise(namespace: dict, questions: list, inputs: list[str]) -> str:
    output = StringIO()
    with patch("builtins.input", side_effect=inputs), redirect_stdout(output):
        run_exercise_questions(namespace, questions)
    return output.getvalue()


def _assert_skip_at_question(
    exercise_id: str, qi: int, namespace: dict, questions: list
) -> None:
    n = len(questions)
    label = f"{exercise_id} Q{qi + 1}"
    inputs = ["skip"] * qi + ["skip"]
    for j in range(qi + 1, n):
        ref = questions[j].reference_answer
        assert ref, f"{label}: missing reference_answer for follow-up input"
        inputs.append(ref)

    text = _run_exercise(namespace, questions, inputs)

    if "Skipping question." not in text:
        raise AssertionError(f"{label}: skip did not print skip message")

    if qi < n - 1:
        next_label = f"Practice Question ({qi + 2}/{n}):"
        if next_label not in text:
            raise AssertionError(f"{label}: skip did not advance to {next_label!r}")
    elif "Exercise completed! Returning to main menu" not in text:
        raise AssertionError(f"{label}: skip on last question did not print completion footer")


def _assert_exit_at_question(
    exercise_id: str, qi: int, namespace: dict, questions: list
) -> None:
    n = len(questions)
    label = f"{exercise_id} Q{qi + 1}"
    inputs = ["skip"] * qi + ["exit"]

    text = _run_exercise(namespace, questions, inputs)

    if "Leaving exercise early." not in text:
        raise AssertionError(f"{label}: exit did not abort exercise")
    if "Exercise completed! Returning to main menu" in text:
        raise AssertionError(f"{label}: exit must not print completion footer")

    if qi < n - 1:
        next_label = f"Practice Question ({qi + 2}/{n}):"
        if next_label in text:
            raise AssertionError(f"{label}: exit continued to {next_label!r}")


def main() -> None:
    total_questions = 0

    for exercise_id in EXERCISE_ORDER:
        namespace, questions = PRACTICE_BUILDERS[exercise_id]()
        for qi in range(len(questions)):
            total_questions += 1
            _assert_skip_at_question(exercise_id, qi, namespace, questions)
            _assert_exit_at_question(exercise_id, qi, namespace, questions)

    print(
        f"verify_skip_exit_behavior: OK ({total_questions} questions × skip + exit checks)."
    )


if __name__ == "__main__":
    main()

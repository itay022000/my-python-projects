"""Shared CLI helpers for suite practice sessions (B016 core + product extensions)."""

from __future__ import annotations

from enum import Enum
from typing import Sequence

# --- B016 CORE (suite-identical when all five projects aligned) ---

MAX_ATTEMPTS = 3
SESSION_BANNER_WIDTH = 70
INTER_ITEM_GAP = "\n\n"

_SPECIAL_SKIP = frozenset({"skip", "Skip"})
_SPECIAL_EXIT = frozenset({"exit", "Exit"})
_SPECIAL_QUIT = frozenset({"quit", "Quit"})


class SessionExit(Exception):
    """Learner chose exit/quit mid exercise."""


class QuestionOutcome(Enum):
    COMPLETED = "completed"
    NOT_COMPLETED = "not_completed"
    EXIT = "exit"
    SKIP_SERIES = "skip_series"


def classify_special_input(raw: str) -> str | None:
    text = raw.strip()
    if text in _SPECIAL_SKIP:
        return "skip"
    if text in _SPECIAL_EXIT or text in _SPECIAL_QUIT:
        return "exit"
    return None


def code_prompt(strikes: int, max_attempts: int = MAX_ATTEMPTS) -> str:
    return f"Your code (attempt {strikes + 1}/{max_attempts}): "


def print_wrong_attempt(strikes: int, max_attempts: int = MAX_ATTEMPTS) -> None:
    print(f"✗ Incorrect answer (attempt {strikes}/{max_attempts}).")
    if strikes < max_attempts:
        print("Try again...\n")


def print_correct_answer(correct_answer: str) -> None:
    print(f"Correct answer: {correct_answer}")


def print_partial_exit_score(completed: int, not_completed: int) -> None:
    total = completed + not_completed
    unit = "question" if total == 1 else "questions"
    print(
        f"\n⏹️  Session exited. "
        f"Completed successfully: {completed} · "
        f"Not completed: {not_completed} (of {total} {unit})"
    )
    print("Returning to main menu...")


def print_teach_intro(title: str, body_lines: Sequence[str]) -> None:
    bar = "=" * SESSION_BANNER_WIDTH
    print("\n" + bar)
    print(title)
    print(bar)
    for line in body_lines:
        print(line)
    print()
    input("Press Enter to start...")


def print_question_header(
    question_num: int, total: int, title: str, *, first: bool
) -> None:
    prefix = "\n" if first else INTER_ITEM_GAP
    print(f"{prefix}--- Question {question_num}/{total} ---")
    print(title)


# --- product extension (ppl; not suite core) ---

TEACH_RULE_LINE = (
    "After three wrong attempts, the answer for the question is shown, followed by the next question."
)
ROUND_TIP = (
    "\nTip: type 'skip' to skip a question, or 'exit'/'quit' to stop the exercise and return to the main menu.\n"
)

# title, background paragraph, session line (question count)
EXERCISE_INTROS: dict[int, tuple[str, str, str]] = {
    1: (
        "Basic Operations Exercise",
        'This exercise uses the sales dataset loaded as df. The following questions practice its basic inspection. Use "Explore Dataset" from the main menu anytime if you want to inspect the data.',
        "You will get 8 single-line code questions.",
    ),
    2: (
        "Filtering Data Exercise",
        'This exercise uses the sales dataset loaded as df. The following questions practice selecting its rows to match certain conditions. Use "Explore Dataset" from the main menu anytime if you want to inspect the data.',
        "You will get 8 single-line code questions.",
    ),
    3: (
        "Sorting and Column Selection Exercise",
        'This exercise uses the sales dataset loaded as df. The following questions practice sorting and filtering it to build a clearer view of its data. Use "Explore Dataset" from the main menu anytime if you want to inspect the data.',
        "You will get 8 single-line code questions.",
    ),
    4: (
        "Data Manipulation Exercise",
        'This exercise uses the sales dataset loaded as df. The following questions practice reshaping and manipulating it in various ways. Use "Explore Dataset" from the main menu anytime if you want to inspect the data.',
        "You will get 8 single-line code questions.",
    ),
    5: (
        "Data Cleaning Exercise",
        'This exercise uses the sales dataset loaded as df. The following questions practice cleaning it and performing basic quality checks on it. Use "Explore Dataset" from the main menu anytime if you want to inspect the data.',
        "You will get 8 single-line code questions.",
    ),
}


def print_exercise_intro(title: str, background: str, session_line: str) -> None:
    print_teach_intro(title, [session_line, TEACH_RULE_LINE])
    print(ROUND_TIP)
    print(background)
    print()


def print_skip_answer(correct_answer: str) -> None:
    print("Skipping question.")
    print_correct_answer(correct_answer)


def _format_pct(value: float) -> str:
    text = f"{value:.1f}"
    if text.endswith(".0"):
        text = text[:-2]
    return text


def print_session_footer(completed: int, not_completed: int) -> None:
    total = completed + not_completed
    bar = "=" * SESSION_BANNER_WIDTH
    print("\n" + bar)
    print("Session Statistics")
    print(bar)
    if total:
        completed_pct = _format_pct(100 * completed / total)
        not_completed_pct = _format_pct(100 * not_completed / total)
        print(f"\nCompleted successfully: {completed} ({completed_pct}%)")
        print(f"Not completed: {not_completed} ({not_completed_pct}%)")
    else:
        print("\nCompleted successfully: 0")
        print(f"Not completed: {not_completed}")
    print(f"Total questions: {total}")
    print("\n" + bar)
    print("Returning to main menu...")
    print(bar)
    print()

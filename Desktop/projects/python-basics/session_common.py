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


# --- product extension (python-basics; not suite core) ---

TF_MAX_ATTEMPTS = 1

TEACH_RULE_LINE = (
    "After three wrong attempts, the answer for the question is shown, followed by the next question."
)
TEACH_RULE_LINE_WITH_TF = (
    "After three wrong attempts (one for True/False questions), the answer "
    "for the question is shown, followed by the next question."
)
ROUND_TIP = (
    "\nTip: type 'skip' to skip a question, or 'exit'/'quit' to stop the exercise and return to the main menu.\n"
)

# Context after tip, before first question (product extension; PM copy)
EXERCISE_BACKGROUNDS: dict[int, str] = {
    1: (
        "The following questions practice Python basic topics: output, comments, "
        "variables, basic data types, and casting."
    ),
    2: (
        "The following questions practice strings and booleans: string modifications, "
        "string indices, f-strings, and truth values of variables and expressions."
    ),
    3: (
        "The following questions practice operators: arithmetic, assignment, comparison, "
        "logical, identity, membership, and bitwise."
    ),
    4: (
        "The following questions practice lists: accessing, modifying, sorting, "
        "copying and joining them, and list comprehension."
    ),
    5: (
        "The following questions practice tuples: accessing, unpacking, joining "
        "and multiplying them."
    ),
    6: (
        "The following questions practice sets: accessing, modifying and deleting them, "
        "frozensets, and various set operations."
    ),
    7: (
        "The following questions practice dictionaries: accessing, modifying, deleting "
        "and copying them, and working with their items."
    ),
    8: (
        "The following questions practice functions: defining and calling them, using "
        "parameters and arguments, and working with decorators and lambdas."
    ),
    9: (
        "The following questions practice Python additional topics: shorthand if, "
        "match, range, and math."
    ),
    10: (
        "The following questions practice Python advanced topics: arrays, dates and "
        "time, JSON, try/except, and input."
    ),
}


def print_skip_answer(correct_answer: str) -> None:
    print("Skipping question.")
    print_correct_answer(correct_answer)


# Alias for older callers
print_skip_simple = print_skip_answer


def print_skip_compound(parts: list[dict]) -> None:
    print("Skipping question.")
    print("Correct answers:")
    for i, part in enumerate(parts, 1):
        ans = part.get("correct_answer", part.get("expected", ""))
        print(f"Line {i}: {ans}")


def format_question_header(
    num: int, total: int, *, first: bool, extra: str = ""
) -> str:
    """String form of the question banner (compound uses extra suffix)."""
    prefix = "\n" if first else INTER_ITEM_GAP
    return f"{prefix}--- Question {num}/{total}{extra} ---"

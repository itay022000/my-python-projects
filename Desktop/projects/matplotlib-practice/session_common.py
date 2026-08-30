"""Shared CLI helpers for matplotlib-practice sessions (B016 core + product extensions)."""

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


# --- product extension (mpl; not suite core) ---

SESSION_INTRO_LINE = "You will get 3 series of single-line code steps."
TEACH_RULE_LINES = (
    "After three wrong attempts per step, the answer for the step is shown, followed by the next step.",
)
ROUND_TIP = (
    "\nTip: type 'skip' to skip the current series, or 'exit'/'quit' to stop the exercise and return to the main menu.\n"
)


def format_step_label(step: int, total: int, description: str) -> str:
    """Learner-facing step progress label (two-line header + description)."""
    text = description[:-1] if description.endswith(".") else description
    return f"--- Step {step}/{total} ---\n{text}"


def print_step_header(
    step: int, total: int, description: str, *, first: bool = False
) -> None:
    prefix = "" if first else INTER_ITEM_GAP
    print(f"{prefix}{format_step_label(step, total, description)}")


print_step_label = print_step_header


def format_pct(value: float) -> str:
    """Format a percentage, trimming a trailing ``.0`` (25.0% -> 25%, 37.5% stays)."""
    text = f"{value:.1f}"
    if text.endswith(".0"):
        text = text[:-2]
    return text


def print_series_partial_exit_score(stats) -> None:
    print(
        f"\n⏹️  Session exited. "
        f"Completed successfully: {stats.completed} · "
        f"Completed with help: {stats.completed_with_help} · "
        f"Not completed: {stats.not_completed} (of {stats.total} series)"
    )
    print("Returning to main menu...")


def print_sequence_stats(stats) -> None:
    total = stats.total
    if total == 0:
        print("\nNo series were attempted.\n")
        return
    bar = "=" * SESSION_BANNER_WIDTH
    print("\n" + bar)
    print("Session Statistics")
    print(bar)
    print(
        f"\nCompleted successfully: {stats.completed} "
        f"({format_pct(stats.pct(stats.completed))}%)"
    )
    print(
        f"Completed with help: {stats.completed_with_help} "
        f"({format_pct(stats.pct(stats.completed_with_help))}%)"
    )
    print(
        f"Not completed: {stats.not_completed} "
        f"({format_pct(stats.pct(stats.not_completed))}%)"
    )
    print(f"Total series: {total}")
    print("\n" + bar)
    print("Returning to main menu...")
    print(bar)
    print()


def build_teach_body_lines(intro_line: str) -> list[str]:
    return [intro_line, *TEACH_RULE_LINES]


def print_sequence_intro(title_line: str, intro_line: str) -> None:
    """Teach block, then tip after Enter."""
    print_teach_intro(title_line, build_teach_body_lines(intro_line))
    print(ROUND_TIP, end="")

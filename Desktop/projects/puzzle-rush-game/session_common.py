"""Shared low-risk gameplay helpers for puzzle-rush-game."""

from __future__ import annotations

import random
from enum import Enum
from typing import Callable, Sequence

from validators import validate_code_answer

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


# --- product extension (puzzle; not suite core) ---

ChallengeFactory = Callable[[], dict]
TrueFalseFactory = Callable[..., dict]

ROUND_TOTAL = 20
TF_MAX_ATTEMPTS = 1
ROUND_TIP = (
    "\nTip: type 'skip' to skip a question, or 'exit'/'quit' to stop the exercise and return to the main menu.\n"
)

TEACH_RULE_LINES = (
    "After three wrong attempts (one for True/False questions), the answer for the question is shown, "
    "followed by the next question.",
)

# Context after tip, before first question (single source; PM copy)
EXERCISE_BACKGROUNDS: dict[str, str] = {
    "array_blitz": (
        "This exercise uses NumPy arrays. The following questions practice creating, "
        "manipulating, searching, sorting, and filtering arrays."
    ),
    "vector_battle": (
        "This exercise uses NumPy random and vector-style helpers. The following questions "
        "practice permutations and shuffles, random draws and distributions, and building "
        "random arrays."
    ),
    "matrix_challenge": (
        "This exercise uses NumPy matrices (2D arrays). The following questions practice "
        "creating and manipulating matrices, matrix math, and basic matrix properties."
    ),
    "ufunc_arena": (
        "This exercise uses NumPy universal functions (ufuncs). The following questions "
        "practice different kinds of ufuncs: arithmetic, rounding, logs, reductions, "
        "differences, and set-style operations."
    ),
}


def print_skip_answer(correct_answer: str) -> None:
    print("Skipping question.")
    print_correct_answer(correct_answer)


def show_hint(challenge: dict) -> None:
    """Display a hint for the current challenge."""
    print(f"Hint: {challenge['hint']}")


def build_teach_body_lines(intro_line: str) -> list[str]:
    """Shared teach copy after the game-specific intro line."""
    return [intro_line, *TEACH_RULE_LINES]


def true_false_prompt() -> str:
    return f"Your answer (attempt 1/{TF_MAX_ATTEMPTS}): "


def make_code_validator(profile: str) -> Callable[[str, str], bool]:
    """Return a code-answer checker bound to a ``validators`` profile."""

    def validate(user_input: str, correct_answer: str) -> bool:
        return validate_code_answer(user_input, correct_answer, profile=profile)

    return validate


def build_challenge_sequence(
    code_generators: Sequence[ChallengeFactory],
    true_false_factory: TrueFalseFactory,
    *,
    code_count: int,
    tf_count: int,
    used_questions: set[str],
) -> list[ChallengeFactory]:
    """
    Build challenge callables for one session: shuffled code first, then T/F last.

    Code questions occupy slots 1..code_count (shuffled among themselves). True/False
    questions always follow as the final ``tf_count`` slots (e.g. 16–20).
    """
    challenge_sequence = [random.choice(code_generators) for _ in range(code_count)]
    random.shuffle(challenge_sequence)
    for _ in range(tf_count):
        challenge_sequence.append(
            lambda u=used_questions, tf=true_false_factory: tf(used_questions=u)
        )
    return challenge_sequence


def get_challenge_counts() -> tuple[int, int, int]:
    """Return (total_challenges, code_count, tf_count) for one session."""
    return ROUND_TOTAL, 15, 5


def _format_pct(count: int, total: int) -> str:
    pct = f"{100 * count / total:.1f}"
    if pct.endswith(".0"):
        pct = pct[:-2]
    return pct


def print_session_footer(completed: int, not_completed: int) -> None:
    total = completed + not_completed
    bar = "=" * SESSION_BANNER_WIDTH
    print("\n" + bar)
    print("Session Statistics")
    print(bar)
    if total:
        print(f"\nCompleted successfully: {completed} ({_format_pct(completed, total)}%)")
        print(f"Not completed: {not_completed} ({_format_pct(not_completed, total)}%)")
    else:
        print("\nCompleted successfully: 0")
        print("Not completed: 0")
    print(f"Total questions: {total}")
    print("\n" + bar)
    print("Returning to main menu...")
    print(bar)
    print()


def pick_true_false_statement(
    statements: list[tuple[str, str]],
    *,
    used_questions: set[str] | None = None,
) -> tuple[str, str]:
    """
    Pick a (question, answer) pair from a statement bank.

    When ``used_questions`` is provided, only statements whose question text is not
    already in that set are eligible (no duplicate T/F prompts in one session).
    """
    if used_questions is not None:
        candidates = [s for s in statements if s[0] not in used_questions]
        if not candidates:
            raise ValueError(
                "No unused true/false statement left; "
                "add more entries to the bank or lower tf_count."
            )
        question, answer = random.choice(candidates)
    else:
        question, answer = random.choice(statements)
    return question, answer

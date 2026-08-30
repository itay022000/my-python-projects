"""Series/step runner for matplotlib-practice (B015 engine)."""

from __future__ import annotations

import re
from enum import Enum
from typing import Callable

from session_common import (
    MAX_ATTEMPTS,
    QuestionOutcome,
    SessionExit,
    classify_special_input,
    code_prompt,
    print_correct_answer,
    print_series_partial_exit_score,
    print_sequence_stats,
    print_wrong_attempt,
)

DEFAULT_COLORS = [
    "red", "blue", "green", "yellow", "orange", "purple", "pink",
    "magenta", "cyan", "brown", "black", "gray", "olive", "lime",
    "navy", "coral", "teal", "gold", "silver", "indigo", "violet",
]

SHOW_ANSWER = "plt.show()"

VerifyFn = Callable[[str], tuple[bool, str]]


class StepOutcome(Enum):
    CORRECT = "correct"
    REVEALED = "revealed"
    SKIP_SERIES = "skip_series"
    EXIT = "exit"


class SeriesOutcome(Enum):
    COMPLETED = "completed"
    COMPLETED_WITH_HELP = "completed_with_help"
    NOT_COMPLETED = "not_completed"
    EXIT = "exit"


def normalize_code(code):
    """Normalize code string for comparison (remove extra whitespace)."""
    code = code.strip()
    code = re.sub(r"\s+", " ", code)
    code = re.sub(r"\s*([=\[\]\(\)])\s*", r"\1", code)
    code = re.sub(r"=\s*", "=", code)
    return code.strip()


def format_np_int_array(var_name: str, values: list[int]) -> str:
    inner = ", ".join(map(str, values))
    return f"{var_name} = np.array([{inner}])"


def format_np_str_array(var_name: str, values: list[str]) -> str:
    inner = ", ".join(f'"{v}"' for v in values)
    return f"{var_name} = np.array([{inner}])"


def format_np_float_array(var_name: str, values: list[float]) -> str:
    inner = ", ".join(str(v) for v in values)
    return f"{var_name} = np.array([{inner}])"


def verify_step_show(user_input):
    """Verify final step: plt.show()."""
    normalized_input = normalize_code(user_input)
    if normalized_input.lower() != "plt.show()":
        return False, "Invalid format"
    return True, "Correct!"


def _skip_series(correct_answer: str) -> QuestionOutcome:
    print("Skipping series.")
    print_correct_answer(correct_answer)
    return QuestionOutcome.SKIP_SERIES


def ask_code_question(
    verify_fn: VerifyFn,
    *,
    correct_answer: str,
    hint: str | None = None,
    max_attempts: int = MAX_ATTEMPTS,
    on_skip: Callable[[], QuestionOutcome] | None = None,
) -> QuestionOutcome:
    """Shared strike-loop body. Does not update scores. Series skip via on_skip."""
    skip_fn = on_skip or (lambda: _skip_series(correct_answer))
    print()
    strikes = 0
    while True:
        raw = input(code_prompt(strikes, max_attempts)).strip()
        if raw == "":
            continue
        special = classify_special_input(raw)
        if special == "exit":
            return QuestionOutcome.EXIT
        if special == "skip":
            return skip_fn()

        correct, _message = verify_fn(raw)
        if correct:
            print("✓ Correct!")
            return QuestionOutcome.COMPLETED

        strikes += 1
        print_wrong_attempt(strikes, max_attempts)
        if strikes == 1 and hint:
            print(f"Hint: {hint}")
            print()
        if strikes >= max_attempts:
            print_correct_answer(correct_answer)
            return QuestionOutcome.NOT_COMPLETED


def _step_from_question(outcome: QuestionOutcome) -> StepOutcome:
    """Map question-level outcome onto series step outcomes (Item 8 adapter)."""
    if outcome == QuestionOutcome.COMPLETED:
        return StepOutcome.CORRECT
    if outcome == QuestionOutcome.NOT_COMPLETED:
        return StepOutcome.REVEALED
    if outcome == QuestionOutcome.SKIP_SERIES:
        return StepOutcome.SKIP_SERIES
    return StepOutcome.EXIT


class SeriesContext:
    """Tracks reveals and correct answers for three-bucket series scoring."""

    def __init__(self) -> None:
        self.revealed = False
        self.any_correct = False

    def absorb(self, outcome: StepOutcome) -> SeriesOutcome | None:
        """Return a terminal series outcome, or None to continue the series."""
        if outcome == StepOutcome.CORRECT:
            self.any_correct = True
            return None
        if outcome == StepOutcome.REVEALED:
            self.revealed = True
            return None
        if outcome == StepOutcome.SKIP_SERIES:
            return SeriesOutcome.NOT_COMPLETED
        if outcome == StepOutcome.EXIT:
            return SeriesOutcome.EXIT
        return None

    def finish(self) -> SeriesOutcome:
        if self.revealed:
            if self.any_correct:
                return SeriesOutcome.COMPLETED_WITH_HELP
            return SeriesOutcome.NOT_COMPLETED
        return SeriesOutcome.COMPLETED


def run_step(
    ctx: SeriesContext,
    verify_fn: VerifyFn,
    *,
    correct_answer: str,
    hint: str | None = None,
) -> bool:
    """
    Run one step. Returns True to continue the series, False if series ended (skip/exit).
    Updates ctx for reveal/correct tracking. Caller should check ctx.finish() after all steps.
    """
    outcome = _step_from_question(
        ask_code_question(verify_fn, correct_answer=correct_answer, hint=hint)
    )
    terminal = ctx.absorb(outcome)
    if terminal == SeriesOutcome.EXIT:
        raise SessionExit()
    if terminal == SeriesOutcome.NOT_COMPLETED:
        return False
    return True


class SeriesStats:
    def __init__(self) -> None:
        self.completed = 0
        self.completed_with_help = 0
        self.not_completed = 0

    def record(self, outcome: SeriesOutcome) -> None:
        if outcome == SeriesOutcome.COMPLETED:
            self.completed += 1
        elif outcome == SeriesOutcome.COMPLETED_WITH_HELP:
            self.completed_with_help += 1
        elif outcome == SeriesOutcome.NOT_COMPLETED:
            self.not_completed += 1

    @property
    def total(self) -> int:
        return self.completed + self.completed_with_help + self.not_completed

    def pct(self, count: int) -> float:
        return (count / self.total * 100) if self.total else 0.0


def run_exercise_sequence(exercises, run_one) -> None:
    """Run all series in a menu exercise; track three-bucket stats."""
    stats = SeriesStats()
    for exercise in exercises:
        try:
            outcome = run_one(exercise)
        except SessionExit:
            # Series was entered (banner shown), so it is in progress even if
            # no step was answered — same as a question in progress in the suite.
            stats.record(SeriesOutcome.NOT_COMPLETED)
            print_series_partial_exit_score(stats)
            return
        stats.record(outcome)
    print_sequence_stats(stats)

"""Question loop for pandas-practice-lite (B016 strike skeleton)."""

from __future__ import annotations

from typing import Callable, Optional

import session_common as sc
from session_common import QuestionOutcome

Checker = Callable[[str], tuple[bool, Optional[str]]]


def record_outcome(
    outcome: QuestionOutcome,
    completed: int,
    not_completed: int,
) -> tuple[int, int] | None:
    """2-bucket score update. Returns None after handling EXIT (partial printed)."""
    if outcome == QuestionOutcome.EXIT:
        not_completed += 1
        sc.print_partial_exit_score(completed, not_completed)
        return None
    if outcome == QuestionOutcome.COMPLETED:
        return completed + 1, not_completed
    return completed, not_completed + 1


def _default_on_skip(correct_answer: str) -> QuestionOutcome:
    sc.print_skip_answer(correct_answer)
    return QuestionOutcome.NOT_COMPLETED


def ask_code_question(
    *,
    question_num: int,
    total: int,
    title: str,
    hint: str,
    correct_answer: str,
    first: bool,
    check: Checker,
    max_attempts: int = sc.MAX_ATTEMPTS,
    on_skip: Callable[[], QuestionOutcome] | None = None,
) -> QuestionOutcome:
    """Shared strike-loop body (H3 when hint non-empty). Does not update scores."""
    sc.print_question_header(question_num, total, title, first=first)
    print()
    skip_fn = on_skip or (lambda: _default_on_skip(correct_answer))
    strikes = 0
    while True:
        raw = input(sc.code_prompt(strikes, max_attempts)).strip()
        if raw == "":
            continue

        special = sc.classify_special_input(raw)
        if special == "exit":
            return QuestionOutcome.EXIT
        if special == "skip":
            return skip_fn()

        err: Optional[str] = None
        try:
            ok, err = check(raw)
        except Exception:
            ok, err = False, None

        if ok:
            print("✓ Correct!")
            return QuestionOutcome.COMPLETED

        strikes += 1
        sc.print_wrong_attempt(strikes, max_attempts)
        if strikes == 1 and hint:
            print(f"Hint: {hint}")
            print()
        # product hook: validator message while attempts remain
        if err and strikes < max_attempts:
            print(f"{err}")
        if strikes >= max_attempts:
            sc.print_correct_answer(correct_answer)
            return QuestionOutcome.NOT_COMPLETED

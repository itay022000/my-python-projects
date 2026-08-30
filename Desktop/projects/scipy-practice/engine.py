"""Question loop and grading for scipy-practice (B016 strike skeleton + eval grading)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Optional, Tuple

import session_common as sc
from session_common import QuestionOutcome

__all__ = [
    "Question",
    "QuestionOutcome",
    "ask_code_question",
    "ask_scipy_question",
    "ask_question",
    "record_outcome",
]

from validators import normalize_code

ResultChecker = Callable[[Any], Tuple[bool, str]]
CodeChecker = Callable[[str], Tuple[bool, str]]


@dataclass(frozen=True)
class Question:
    """One graded prompt: semantic validation via check(); optional reveal string."""

    text: str
    check: ResultChecker
    hint: str
    check_code: Optional[CodeChecker] = None
    correct_answer: Optional[str] = None
    require_exact: bool = False


def _grade_submission(
    user_code: str,
    namespace: dict,
    check_func: ResultChecker,
    check_code: Optional[CodeChecker],
    correct_answer: Optional[str],
    require_exact: bool,
) -> bool:
    if require_exact and correct_answer:
        if normalize_code(user_code) != normalize_code(correct_answer):
            return False

    user_result = eval(user_code, namespace)

    if check_code:
        code_check, _ = check_code(user_code)
        if not code_check:
            return False

    is_correct, _ = check_func(user_result)
    return is_correct


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


def _default_on_skip(correct_answer: Optional[str]) -> QuestionOutcome:
    if correct_answer:
        sc.print_skip_answer(correct_answer)
    else:
        print("Skipping question.")
    return QuestionOutcome.NOT_COMPLETED


def ask_code_question(
    *,
    question_num: int,
    total: int,
    title: str,
    hint: str,
    first: bool,
    check: Callable[[str], bool],
    correct_answer: Optional[str] = None,
    max_attempts: int = sc.MAX_ATTEMPTS,
    on_skip: Callable[[], QuestionOutcome] | None = None,
) -> QuestionOutcome:
    """Shared strike-loop body. Does not update scores. Product `check` runs eval/science."""
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

        try:
            ok = check(raw)
        except Exception:
            ok = False

        if ok:
            print("✓ Correct!")
            return QuestionOutcome.COMPLETED

        strikes += 1
        sc.print_wrong_attempt(strikes, max_attempts)
        if strikes == 1 and hint:
            print(f"Hint: {hint}")
            print()
        if strikes >= max_attempts:
            if correct_answer:
                sc.print_correct_answer(correct_answer)
            return QuestionOutcome.NOT_COMPLETED


def ask_scipy_question(
    *,
    question_num: int,
    total: int,
    title: str,
    hint: str,
    namespace: dict,
    check_func: ResultChecker,
    first: bool,
    check_code: Optional[CodeChecker] = None,
    correct_answer: Optional[str] = None,
    require_exact: bool = False,
) -> QuestionOutcome:
    """Adapter: builds check() for eval/`Question.check` then runs ask_code_question."""

    def check(raw: str) -> bool:
        return _grade_submission(
            raw,
            namespace,
            check_func,
            check_code,
            correct_answer,
            require_exact,
        )

    return ask_code_question(
        question_num=question_num,
        total=total,
        title=title,
        hint=hint,
        first=first,
        check=check,
        correct_answer=correct_answer,
    )


# Transitional alias for older call sites / tests
ask_question = ask_scipy_question

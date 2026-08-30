"""Run a full scipy exercise session (list of questions) with B016 flow."""

from __future__ import annotations

from typing import Any, Dict, List

import session_common as sc
from engine import Question, ask_scipy_question, record_outcome


def run_questions(
    namespace: Dict[str, Any],
    questions: List[Question],
) -> tuple[int, int]:
    """Ask each question in order; returns (completed, not_completed)."""
    completed = 0
    not_completed = 0
    total = len(questions)
    for index, q in enumerate(questions, start=1):
        outcome = ask_scipy_question(
            question_num=index,
            total=total,
            title=q.text,
            hint=q.hint,
            namespace=namespace,
            check_func=q.check,
            first=(index == 1),
            check_code=q.check_code,
            correct_answer=q.correct_answer,
            require_exact=q.require_exact,
        )
        result = record_outcome(outcome, completed, not_completed)
        if result is None:
            raise sc.SessionExit()
        completed, not_completed = result
    return completed, not_completed


def run_exercise_questions(
    namespace: Dict[str, Any],
    questions: List[Question],
    *,
    background: str,
    after_background: str | None = None,
) -> None:
    """Teach block, tip, context paragraph (ppl placement), then questions + footer."""
    # Immediately after exercise title bars (no blank line before this).
    print(f"You will get {len(questions)} single-line code questions.")
    print(f"{sc.TEACH_RULE_LINE}\n")
    input("Press Enter to start...")
    print(sc.ROUND_TIP)
    print(background)
    if after_background:
        # Same spacing as 2–6 around the context block: blank, then extra line (note), then shared trailer.
        print()
        print(after_background)
    print()
    try:
        completed, not_completed = run_questions(namespace, questions)
    except sc.SessionExit:
        return
    sc.print_session_footer(completed, not_completed)

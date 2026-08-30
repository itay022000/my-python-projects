"""Run a full exercise session (list of questions) with B016 flow."""

from __future__ import annotations

from typing import Any

import session_common as pc
from engine import ask_code_question, record_outcome


def run_question_session(
    app,
    df,
    specs: list[dict[str, Any]],
    *,
    before_question=None,
) -> None:
    """Each spec: title, hint, correct_answer; optional include_plotting, check."""
    total = len(specs)
    completed = 0
    not_completed = 0
    for i, spec in enumerate(specs):
        if before_question is not None:
            before_question(i, df)
        checker = spec.get("check")
        if checker is None:
            checker = app.make_exact_checker(
                df,
                spec["correct_answer"],
                spec.get("include_plotting", False),
            )
        outcome = ask_code_question(
            question_num=i + 1,
            total=total,
            title=spec["title"],
            hint=spec["hint"],
            correct_answer=spec["correct_answer"],
            first=(i == 0),
            check=checker,
        )
        result = record_outcome(outcome, completed, not_completed)
        if result is None:
            return
        completed, not_completed = result
    pc.print_session_footer(completed, not_completed)

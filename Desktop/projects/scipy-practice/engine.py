"""Shared exercise runner: one loop for all practice questions."""

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple

from practice import ExerciseAbort, QuestionSkip, ask_question

# check(user_result) -> (ok, feedback_message)
ResultChecker = Callable[[Any], Tuple[bool, str]]
# check(user_code_str) -> (ok, optional_feedback)
CodeChecker = Callable[[str], Tuple[bool, str]]


@dataclass(frozen=True)
class Question:
    """One graded prompt: semantic validation via check(); optional reference string for hints."""

    text: str
    check: ResultChecker
    hint: str
    check_code: Optional[CodeChecker] = None
    reference_answer: Optional[str] = None
    require_exact: bool = False


def run_questions(namespace: Dict[str, Any], questions: List[Question]) -> None:
    """Ask each question in order; propagates ExerciseAbort."""
    total = len(questions)
    for index, q in enumerate(questions, start=1):
        try:
            ask_question(
                q.text,
                namespace,
                q.check,
                q.hint,
                check_code=q.check_code,
                reference_answer=q.reference_answer,
                require_exact=q.require_exact,
                progress_label=f"{index}/{total}",
                separator_prefix="" if index == 1 else "\n",
            )
        except QuestionSkip:
            continue


def print_exercise_footer() -> None:
    print("\n" + "=" * 60)
    print("Exercise completed! Returning to main menu...")
    print("=" * 60)
    print()


def run_exercise_questions(namespace: Dict[str, Any], questions: List[Question]) -> None:
    """Run all questions; on success print standard footer. Abort skips footer."""
    print("\nTip: type skip to move to the next question, or exit/quit to return to the main menu.\n")
    try:
        run_questions(namespace, questions)
    except ExerciseAbort:
        return
    print_exercise_footer()

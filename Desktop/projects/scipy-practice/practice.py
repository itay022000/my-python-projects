"""Prompt helpers: normalize submitted code and run the practice question loop."""

import re


class ExerciseAbort(Exception):
    """User chose to leave the exercise early (exit / quit)."""


class QuestionSkip(Exception):
    """User chose to skip the current question."""


def normalize_code(code):
    """Normalize code string for comparison (remove extra spaces)."""
    return re.sub(r"\s+", "", code)


def ask_question(
    question_text,
    namespace,
    check_func,
    hint_text,
    check_code=None,
    reference_answer=None,
    require_exact=False,
    progress_label=None,
    show_separator=True,
    separator_prefix="\n",
):
    """
    Ask a question and check the answer.

    Validation policy (Phase 2):
    - By default, answers are graded semantically: eval() then check_func(result).
    - If require_exact is True, the user's code must match reference_answer (normalized)
      before eval runs (legacy / strict mode).
    - reference_answer is shown as an example when the semantic check fails (unless require_exact).
    """
    if show_separator:
        print(f"{separator_prefix}{'-' * 60}")
    if progress_label:
        print(f"Practice Question ({progress_label}):")
    else:
        print("Practice Question:")
    print(question_text)
    print("Enter your code: ", end="")
    try:
        user_code = input().strip()
        lower = user_code.lower()
        if lower in ("exit", "quit"):
            print("\nLeaving exercise early.")
            raise ExerciseAbort
        if lower == "skip":
            print("Skipping question.")
            raise QuestionSkip

        if require_exact and reference_answer:
            if normalize_code(user_code) != normalize_code(reference_answer):
                print("❌ Incorrect.")
                print(f"   Hint: {hint_text}")
                return

        user_result = eval(user_code, namespace)

        if check_code:
            code_check, code_feedback = check_code(user_code)
            if not code_check:
                print("❌ Incorrect.")
                if code_feedback:
                    print(f"   {code_feedback}")
                if reference_answer and not require_exact:
                    print(f"   Example solution: {reference_answer}")
                print(f"   Hint: {hint_text}")
                return

        is_correct, feedback = check_func(user_result)
        if is_correct:
            print("✅ Correct!")
            if feedback:
                print(f"   {feedback}")
        else:
            print("❌ Incorrect.")
            if feedback:
                print(f"   {feedback}")
            if reference_answer and not require_exact:
                print(f"   Example solution: {reference_answer}")
            print(f"   Hint: {hint_text}")
    except (ExerciseAbort, QuestionSkip):
        raise
    except Exception as e:
        print(f"❌ Error: {e}")
        if reference_answer and not require_exact:
            print(f"   Example solution: {reference_answer}")
        print(f"   Hint: {hint_text}")

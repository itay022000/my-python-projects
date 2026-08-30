"""
Shared interactive session loop for python-basics batches (B016 engine).
"""

from __future__ import annotations

from typing import Callable

import session_common as sc
from session_common import (
    INTER_ITEM_GAP,
    MAX_ATTEMPTS,
    QuestionOutcome,
    SESSION_BANNER_WIDTH,
    SessionExit,
    TF_MAX_ATTEMPTS,
    TEACH_RULE_LINE,
    classify_special_input,
    code_prompt,
    format_question_header,
    print_correct_answer,
    print_partial_exit_score,
    print_skip_compound,
    print_skip_simple,
    print_wrong_attempt,
    ROUND_TIP,
)


def print_session_header(title: str) -> None:
    bar = "=" * SESSION_BANNER_WIDTH
    print("\n" + bar)
    print(title)
    print(bar)


def print_batch_intro(
    title: str,
    session_line: str,
    *,
    background: str | None = None,
    teach_line: str | None = None,
) -> None:
    """Title → session (no blank) → teach → Enter → tip → optional context → questions."""
    print_session_header(title)
    print(session_line)
    print(f"{teach_line or TEACH_RULE_LINE}\n")
    input("Press Enter to start...")
    print(ROUND_TIP)
    if background:
        print(background)
        print()


def _format_pct(count: int, total: int) -> str:
    text = f"{100 * count / total:.1f}"
    if text.endswith(".0"):
        text = text[:-2]
    return text


def print_session_footer(successful: int, unsuccessful: int) -> None:
    total_done = successful + unsuccessful
    print("\n" + "=" * SESSION_BANNER_WIDTH)
    print("Session Statistics")
    print("=" * SESSION_BANNER_WIDTH)
    if total_done:
        print(
            f"\nCompleted successfully: {successful} "
            f"({_format_pct(successful, total_done)}%)"
        )
        print(
            f"Not completed: {unsuccessful} "
            f"({_format_pct(unsuccessful, total_done)}%)"
        )
    else:
        print("\nCompleted successfully: 0")
        print("Not completed: 0")
    print(f"Total questions: {total_done}")
    print("\n" + "=" * SESSION_BANNER_WIDTH)
    print("Returning to main menu...")
    print("=" * SESSION_BANNER_WIDTH)
    print()


def prompt_label_batch2(exercise: dict) -> str:
    return "Your answer" if exercise.get("answer_type") == "word" else "Your code"


def max_attempts_for(exercise: dict, default: int = MAX_ATTEMPTS) -> int:
    """True/False word questions (batch 2 only) allow a single attempt."""
    if exercise.get("answer_type") == "word":
        return TF_MAX_ATTEMPTS
    return default


def _exercise_answer(item: dict) -> str:
    return item.get("correct_answer", item["expected"])


def record_outcome(
    outcome: QuestionOutcome,
    completed: int,
    not_completed: int,
) -> tuple[int, int]:
    """2-bucket update; raises SessionExit after partial print on EXIT."""
    if outcome == QuestionOutcome.EXIT:
        not_completed += 1
        print_partial_exit_score(completed, not_completed)
        raise SessionExit()
    if outcome == QuestionOutcome.COMPLETED:
        return completed + 1, not_completed
    return completed, not_completed + 1


def ask_code_question(
    *,
    check: Callable[[str], tuple[bool, str]],
    correct_answer: str,
    max_attempts: int = MAX_ATTEMPTS,
    hint: str | None = None,
    on_skip: Callable[[], None] | None = None,
    prompt_label: str = "Your code",
    input_fn: Callable[[str], str] | None = None,
) -> QuestionOutcome:
    """Strike loop (header printed by caller). Does not update session scores."""
    if input_fn is None:
        input_fn = input
    skip_fn = on_skip or (lambda: print_skip_simple(correct_answer))
    print()  # one gap after question text (suite: empty re-prompt has no extra blank)
    strikes = 0
    while True:
        if prompt_label == "Your code":
            prompt = code_prompt(strikes, max_attempts)
        else:
            prompt = f"{prompt_label} (attempt {strikes + 1}/{max_attempts}): "
        try:
            raw = input_fn(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            return QuestionOutcome.NOT_COMPLETED
        if raw == "":
            continue

        special = classify_special_input(raw)
        if special == "exit":
            return QuestionOutcome.EXIT
        if special == "skip":
            skip_fn()
            return QuestionOutcome.NOT_COMPLETED

        correct, _message = check(raw)
        if correct:
            print("✓ Correct!")
            return QuestionOutcome.COMPLETED

        strikes += 1
        print_wrong_attempt(strikes, max_attempts)
        if strikes == 1 and hint:
            print(f"Hint: {hint}\n")
        if strikes >= max_attempts:
            print_correct_answer(correct_answer)
            return QuestionOutcome.NOT_COMPLETED


def _run_one_simple_exercise(
    exercise: dict,
    num: int,
    total: int,
    *,
    max_mistakes: int,
    prompt_label: str,
    input_fn: Callable[[str], str],
    hint: str | None,
) -> QuestionOutcome:
    print(format_question_header(num, total, first=(num == 1)))
    print(exercise["question"])
    return ask_code_question(
        check=exercise["check"],
        correct_answer=_exercise_answer(exercise),
        max_attempts=max_mistakes,
        hint=hint,
        on_skip=lambda: print_skip_simple(_exercise_answer(exercise)),
        prompt_label=prompt_label,
        input_fn=input_fn,
    )


def run_simple_exercises(
    exercises: list,
    *,
    max_mistakes: int,
    prompt_label_for: Callable[[dict], str] | None = None,
    hint_for: Callable[[dict], str | None] | None = None,
    input_fn: Callable[[str], str] | None = None,
) -> tuple[int, int]:
    if input_fn is None:
        input_fn = input  # type: ignore[assignment]
    label_fn = prompt_label_for or (lambda _ex: "Your code")
    hint_fn = hint_for or (lambda _ex: None)

    completed = 0
    not_completed = 0
    n = len(exercises)
    for i, ex in enumerate(exercises, 1):
        outcome = _run_one_simple_exercise(
            ex,
            i,
            n,
            max_mistakes=max_attempts_for(ex, max_mistakes),
            prompt_label=label_fn(ex),
            input_fn=input_fn,
            hint=hint_fn(ex),
        )
        completed, not_completed = record_outcome(outcome, completed, not_completed)
    return completed, not_completed


def _run_compound_unit(
    unit: dict,
    num: int,
    total: int,
    *,
    max_mistakes: int,
    input_fn: Callable[[str], str],
    hint_for: Callable[[dict], str | None],
) -> QuestionOutcome:
    parts = unit["parts"]
    print(
        format_question_header(
            num, total, first=(num == 1), extra=f" ({len(parts)} lines)"
        )
    )
    print(unit["title"])

    all_ok = True
    for pi, part in enumerate(parts, 1):
        print(f"\nLine {pi}/{len(parts)}:")
        print(part["question"])

        skipped = False

        def on_skip() -> None:
            nonlocal skipped
            skipped = True
            print_skip_compound(parts)

        outcome = ask_code_question(
            check=part["check"],
            correct_answer=_exercise_answer(part),
            max_attempts=max_mistakes,
            hint=hint_for(part),
            on_skip=on_skip,
            prompt_label="Your code",
            input_fn=input_fn,
        )
        if outcome == QuestionOutcome.EXIT:
            return QuestionOutcome.EXIT
        if skipped:
            return QuestionOutcome.NOT_COMPLETED
        if outcome == QuestionOutcome.NOT_COMPLETED:
            all_ok = False
            if pi < len(parts):
                print("Continuing with the next line in this prompt...\n")
            continue

    return QuestionOutcome.COMPLETED if all_ok else QuestionOutcome.NOT_COMPLETED


def _run_simple_unit(
    unit: dict,
    num: int,
    total: int,
    *,
    max_mistakes: int,
    input_fn: Callable[[str], str],
    hint_for: Callable[[dict], str | None],
) -> QuestionOutcome:
    print(format_question_header(num, total, first=(num == 1)))
    print(unit["question"])
    return ask_code_question(
        check=unit["check"],
        correct_answer=_exercise_answer(unit),
        max_attempts=max_mistakes,
        hint=hint_for(unit),
        on_skip=lambda: print_skip_simple(_exercise_answer(unit)),
        prompt_label="Your code",
        input_fn=input_fn,
    )


def run_mixed_units_session(
    units: list,
    *,
    max_mistakes: int,
    hint_for: Callable[[dict], str | None] | None = None,
    input_fn: Callable[[str], str] | None = None,
) -> tuple[int, int]:
    if input_fn is None:
        input_fn = input  # type: ignore[assignment]
    hint_fn = hint_for or (lambda _ex: None)

    completed = 0
    not_completed = 0
    total_units = len(units)
    for i, unit in enumerate(units, 1):
        if unit["kind"] == "simple":
            outcome = _run_simple_unit(
                unit,
                i,
                total_units,
                max_mistakes=max_mistakes,
                input_fn=input_fn,
                hint_for=hint_fn,
            )
        else:
            outcome = _run_compound_unit(
                unit,
                i,
                total_units,
                max_mistakes=max_mistakes,
                input_fn=input_fn,
                hint_for=hint_fn,
            )
        completed, not_completed = record_outcome(outcome, completed, not_completed)
    return completed, not_completed

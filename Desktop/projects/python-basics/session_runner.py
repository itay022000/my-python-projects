"""
Shared interactive session loop for python-basics batches.

Matches the per-batch behavior in the exercise classes: mistakes-based attempt
counting (empty lines are graded and count as failed attempts when wrong),
compound multi-line flow, shared session banner/footer printing, and statistics.
"""

from __future__ import annotations

from typing import Callable

# Shared CLI framing (batches use print_session_header + body lines; footer after session).
SESSION_BANNER_WIDTH = 70


def print_session_header(title: str) -> None:
    """Print the standard top banner: rule line, title, rule line."""
    bar = "=" * SESSION_BANNER_WIDTH
    print("\n" + bar)
    print(title)
    print(bar)


def print_session_footer(successful: int, unsuccessful: int) -> None:
    """
    Print SESSION STATISTICS (same layout for flat exercise sessions and mixed units).
    successful = completed or units passed; unsuccessful = not completed or units failed.
    """
    total_done = successful + unsuccessful
    print("\n" + "=" * SESSION_BANNER_WIDTH)
    print("SESSION STATISTICS")
    print("=" * SESSION_BANNER_WIDTH)
    if total_done:
        pct = 100 * successful / total_done
        print(f"\nCompleted successfully: {successful} ({pct:.1f}%)")
    else:
        print("\nCompleted: 0")
    print(f"Not completed: {unsuccessful}")
    print(f"Total: {total_done}")
    print("\n" + "=" * SESSION_BANNER_WIDTH)


def prompt_label_batch2(exercise: dict) -> str:
    """Batch 2: code vs True/False word prompts."""
    return "Your answer" if exercise.get("answer_type") == "word" else "Your code"


def print_session_statistics(completed: int, not_completed: int) -> None:
    """Alias for :func:`print_session_footer` (flat exercise sessions)."""
    print_session_footer(completed, not_completed)


def print_unit_session_statistics(units_passed: int, units_failed: int) -> None:
    """Alias for :func:`print_session_footer` (mixed-unit sessions)."""
    print_session_footer(units_passed, units_failed)


def _run_one_simple_exercise(
    exercise: dict,
    num: int,
    total: int,
    is_last: bool,
    *,
    max_mistakes: int,
    prompt_label: str,
    input_fn: Callable[[str], str],
) -> bool:
    mistakes = 0
    print(f"\n--- Question {num}/{total} ---")
    print(exercise["question"])
    while True:
        try:
            user_input = input_fn(
                f"   {prompt_label} (attempt {mistakes + 1}/{max_mistakes}): "
            ).strip()
        except (EOFError, KeyboardInterrupt):
            return False
        correct, message = exercise["check"](user_input)
        if correct:
            print(f"   ✓ {message}\n")
            return True
        print(f"   ✗ {message}")
        mistakes += 1
        if mistakes >= max_mistakes:
            print(f"\n   Correct answer: {exercise['expected']}")
            if is_last:
                print("\n⚠️  Three mistakes. Ending session.\n")
            else:
                print("\n⚠️  Three mistakes. Skipping to next question.\n")
            return False
        print("   Try again...\n")


def run_simple_exercises(
    exercises: list,
    *,
    max_mistakes: int,
    prompt_label_for: Callable[[dict], str] | None = None,
    input_fn: Callable[[str], str] | None = None,
) -> tuple[int, int]:
    """
    Flat list of exercises (question, expected, check).
    Returns (completed, not_completed).
    """
    if input_fn is None:
        input_fn = input  # type: ignore[assignment]
    label_fn = prompt_label_for or (lambda _ex: "Your code")

    completed = 0
    not_completed = 0
    n = len(exercises)
    for i, ex in enumerate(exercises, 1):
        is_last = i == n
        ok = _run_one_simple_exercise(
            ex,
            i,
            n,
            is_last,
            max_mistakes=max_mistakes,
            prompt_label=label_fn(ex),
            input_fn=input_fn,
        )
        if ok:
            completed += 1
        else:
            not_completed += 1
            if is_last:
                break
    return completed, not_completed


def _run_simple_unit(
    unit: dict,
    num: int,
    total: int,
    is_last: bool,
    *,
    max_mistakes: int,
    input_fn: Callable[[str], str],
) -> bool:
    mistakes = 0
    print(f"\n--- Question {num}/{total} ---")
    print(unit["question"])
    while True:
        try:
            user_input = input_fn(
                f"   Your code (attempt {mistakes + 1}/{max_mistakes}): "
            ).strip()
        except (EOFError, KeyboardInterrupt):
            return False
        correct, message = unit["check"](user_input)
        if correct:
            print(f"   ✓ {message}\n")
            return True
        print(f"   ✗ {message}")
        mistakes += 1
        if mistakes >= max_mistakes:
            print(f"\n   Correct answer: {unit['expected']}")
            if is_last:
                print("\n⚠️  Three mistakes. Ending session.\n")
            else:
                print("\n⚠️  Three mistakes. Skipping to next question.\n")
            return False
        print("   Try again...\n")


def _run_compound_unit(
    unit: dict,
    num: int,
    total: int,
    is_last: bool,
    *,
    max_mistakes: int,
    input_fn: Callable[[str], str],
) -> bool:
    parts = unit["parts"]
    print(f"\n--- Question {num}/{total} ({len(parts)} lines) ---")
    print(unit["title"])
    all_ok = True
    for pi, part in enumerate(parts, 1):
        attempt = 0
        print(f"\n   Line {pi}/{len(parts)}:")
        print(f"   {part['question']}")
        line_ok = False
        while True:
            try:
                user_input = input_fn(
                    f"   Your code (attempt {attempt + 1}/{max_mistakes}): "
                ).strip()
            except (EOFError, KeyboardInterrupt):
                return False
            correct, message = part["check"](user_input)
            if correct:
                print(f"   ✓ {message}\n")
                line_ok = True
                break
            print(f"   ✗ {message}")
            attempt += 1
            if attempt >= max_mistakes:
                print(f"\n   Correct answer: {part['expected']}")
                print("\n⚠️  Three mistakes on this line.\n")
                all_ok = False
                break
            print("   Try again...\n")
        if not line_ok:
            all_ok = False
        if not line_ok and pi < len(parts):
            print("   Continuing with the next line in this prompt...\n")

    if not all_ok and is_last:
        print("⚠️  Not all lines correct for this exercise. Ending session.\n")
    elif not all_ok:
        print("⚠️  Not all lines correct for this exercise. Skipping to next question.\n")

    return all_ok


def run_mixed_units_session(
    units: list,
    *,
    max_mistakes: int,
    input_fn: Callable[[str], str] | None = None,
) -> tuple[int, int]:
    """
    Units are dicts with kind 'simple' or 'compound'.
    Returns (passed, failed).
    """
    if input_fn is None:
        input_fn = input  # type: ignore[assignment]

    total_units = len(units)
    passed = 0
    failed = 0
    for i, unit in enumerate(units, 1):
        is_last = i == total_units
        if unit["kind"] == "simple":
            ok = _run_simple_unit(unit, i, total_units, is_last, max_mistakes=max_mistakes, input_fn=input_fn)
        else:
            ok = _run_compound_unit(unit, i, total_units, is_last, max_mistakes=max_mistakes, input_fn=input_fn)
        if ok:
            passed += 1
        else:
            failed += 1
            if is_last:
                break
    return passed, failed

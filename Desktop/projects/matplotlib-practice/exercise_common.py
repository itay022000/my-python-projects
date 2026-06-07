"""
Shared helpers for matplotlib-practice exercise modules.
Behavior-preserving utilities for verification and CLI step prompts.
"""

import re

DEFAULT_COLORS = [
    "red", "blue", "green", "yellow", "orange", "purple", "pink",
    "magenta", "cyan", "brown", "black", "gray", "olive", "lime",
    "navy", "coral", "teal", "gold", "silver", "indigo", "violet",
]

MSG_SKIP = (
    "\n⚠️  You have made 3 mistakes in this exercise. "
    "Skipping to the next exercise...\n"
)
MSG_TERMINATE = (
    "\n⚠️  You have made 3 mistakes in this exercise. "
    "Terminating exercises sequence.\n"
)


def normalize_code(code):
    """Normalize code string for comparison (remove extra whitespace)."""
    code = code.strip()
    code = re.sub(r"\s+", " ", code)
    code = re.sub(r"\s*([=\[\]\(\)])\s*", r"\1", code)
    code = re.sub(r"=\s*", "=", code)
    return code.strip()


def verify_step_show(user_input):
    """Verify final step: plt.show()."""
    normalized_input = normalize_code(user_input)
    if normalized_input.lower() != "plt.show()":
        return False, "Invalid format"
    return True, "Correct!"


def print_third_mistake(is_last, *, skip_only=False):
    """Print the same termination/skip message as the original modules."""
    if skip_only:
        print(MSG_SKIP)
    elif is_last:
        print(MSG_TERMINATE)
    else:
        print(MSG_SKIP)


def prompt_code_step(verify_fn, mistake_count, is_last, *, skip_only=False):
    """
    Read and verify one code step. Returns (completed, mistake_count).
    completed is False if the exercise was aborted after 3 mistakes.
    """
    while True:
        user_input = input("   Your code: ").strip()
        correct, message = verify_fn(user_input)
        if correct:
            print(f"   ✓ {message}\n")
            return True, mistake_count
        mistake_count += 1
        print(f"   ✗ {message}")
        if mistake_count >= 3:
            print_third_mistake(is_last, skip_only=skip_only)
            return False, mistake_count
        print("   Try again...\n")


def print_sequence_intro(title_line, description_line):
    """Shared intro for an exercise sequence."""
    print("=" * 70)
    print(title_line)
    print("=" * 70)
    print(f"\n{description_line}\n")
    input("Press Enter to start...")


def run_exercise_sequence(exercises, run_one):
    """Run exercises with shared completion statistics."""
    completed_count = 0
    not_completed_count = 0

    for i, exercise in enumerate(exercises):
        is_last = i == len(exercises) - 1
        completed = run_one(exercise, is_last)
        if completed:
            completed_count += 1
        else:
            not_completed_count += 1
            if is_last:
                break
            continue

    total = completed_count + not_completed_count
    completed_pct = (completed_count / total * 100) if total > 0 else 0
    not_completed_pct = (not_completed_count / total * 100) if total > 0 else 0

    print("\n" + "=" * 70)
    print("EXERCISE SEQUENCE STATISTICS")
    print("=" * 70)
    print(f"\nCompleted successfully: {completed_count} ({completed_pct:.1f}%)")
    print(f"Not completed: {not_completed_count} ({not_completed_pct:.1f}%)")
    print(f"Total exercises: {total}")
    print("\n" + "=" * 70)

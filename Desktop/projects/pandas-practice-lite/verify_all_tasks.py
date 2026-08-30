#!/usr/bin/env python3
"""
Code structure verification for all questions (B011).

Post-B003: exercise bodies live in exercises/exercise_*.py.
Post-B011: shared question loop via exercise_session.run_question_session.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

EXERCISE_FILES = {
    "exercise_1_basic_operations": ("Exercise 1", ROOT / "exercises" / "exercise_1.py"),
    "exercise_2_filtering": ("Exercise 2", ROOT / "exercises" / "exercise_2.py"),
    "exercise_3_sorting_and_selection": ("Exercise 3", ROOT / "exercises" / "exercise_3.py"),
    "exercise_4_data_manipulation": ("Exercise 4", ROOT / "exercises" / "exercise_4.py"),
    "exercise_5_data_cleaning": ("Exercise 5", ROOT / "exercises" / "exercise_5.py"),
}


def verify_task_structure() -> bool:
    """Verify that all exercises use the B011 question-session pattern."""
    issues: list[str] = []
    verified = 0

    print("\n" + "=" * 70)
    print("VERIFYING CODE STRUCTURE FOR ALL QUESTIONS")
    print("=" * 70)

    for func_name, (ex_name, path) in EXERCISE_FILES.items():
        print(f"\n{ex_name}:")

        if not path.is_file():
            issues.append(f"{ex_name}: Missing file {path.relative_to(ROOT)}")
            continue

        content = path.read_text()

        pattern = rf"def {func_name}\(self\):.*?(?=\n    def |\Z)"
        match = re.search(pattern, content, re.DOTALL)
        if not match:
            issues.append(f"{ex_name}: Function {func_name} not found in {path.name}")
            continue

        exercise_code = match.group(0)

        if "run_question_session" not in exercise_code:
            issues.append(f"{ex_name}: Missing run_question_session() call")
        else:
            verified += 1

        if "record_exercise_completion" in exercise_code:
            issues.append(f"{ex_name}: Still calls record_exercise_completion")
        else:
            verified += 1

        if "check_dataset_loaded" in exercise_code:
            issues.append(f"{ex_name}: Still calls check_dataset_loaded")
        else:
            verified += 1

        if "handle_special_commands" in exercise_code:
            issues.append(f"{ex_name}: Still uses handle_special_commands")
        else:
            verified += 1

        if "print_task_header" in exercise_code:
            issues.append(f"{ex_name}: Still uses print_task_header")
        else:
            verified += 1

    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    print(f"Verified patterns: {verified}")
    if issues:
        print(f"Issues found: {len(issues)}")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("✓ All exercises follow the B011 question-session pattern!")
    print("=" * 70)

    return len(issues) == 0


if __name__ == "__main__":
    raise SystemExit(0 if verify_task_structure() else 1)

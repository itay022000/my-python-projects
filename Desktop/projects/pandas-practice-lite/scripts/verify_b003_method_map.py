#!/usr/bin/env python3
"""
Verify B003 split: compare method bodies from old monolithic main.py vs new modules.

Usage (from project root):
  # Use last committed main.py (git):
  git show HEAD:Desktop/projects/pandas-practice-lite/main.py > /tmp/ppl_old_main.py
  python3 scripts/verify_b003_method_map.py /tmp/ppl_old_main.py

  # Or pass any saved copy of the pre-split main.py:
  python3 scripts/verify_b003_method_map.py path/to/old_main.py

Prints per-method match/mismatch and a file map (where each method lives now).
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Where each PandasPractice method lives after B003
METHOD_TO_FILE = {
    "wait_for_esc": ROOT / "menus.py",
    "explore_dataset": ROOT / "menus.py",
    "main_menu": ROOT / "menus.py",
    "show_exercises": ROOT / "menus.py",
    "show_statistics": ROOT / "menus.py",
    "load_progress": ROOT / "progress.py",
    "save_progress": ROOT / "progress.py",
    "record_exercise_completion": ROOT / "progress.py",
    "reset_statistics": ROOT / "progress.py",
    "load_dataset": ROOT / "dataset.py",
    "get_numeric_columns": ROOT / "dataset.py",
    "get_categorical_columns": ROOT / "dataset.py",
    "get_random_numeric_column": ROOT / "dataset.py",
    "get_random_categorical_column": ROOT / "dataset.py",
    "get_random_column": ROOT / "dataset.py",
    "get_random_value_from_column": ROOT / "dataset.py",
    "get_random_threshold": ROOT / "dataset.py",
    "check_dataset_loaded": ROOT / "dataset.py",
    "exercise_1_basic_operations": ROOT / "exercises/exercise_1.py",
    "exercise_2_filtering": ROOT / "exercises/exercise_2.py",
    "exercise_3_sorting_and_selection": ROOT / "exercises/exercise_3.py",
    "exercise_4_data_manipulation": ROOT / "exercises/exercise_4.py",
    "exercise_5_data_cleaning": ROOT / "exercises/exercise_5.py",
}

# Methods that stayed on app.py (not moved from old main's class body)
APP_ONLY = {
    "__init__",
    "handle_special_commands",
    "run_exercise",
    "is_valid_pandas_code",
    "execute_pandas_code",
    "validate_head_result",
    "validate_shape_result",
    "validate_columns_result",
    "validate_filter_result",
    "validate_filter_greater_than",
    "validate_groupby_sum",
    "validate_merge_result",
    "validate_drop_duplicates",
    "validate_handle_missing",
}


def normalize(source: str) -> str:
    return "\n".join(line.rstrip() for line in source.strip().splitlines())


def class_methods(path: Path) -> dict[str, str]:
    src = path.read_text()
    tree = ast.parse(src)
    out: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    seg = ast.get_source_segment(src, item)
                    if seg:
                        out[item.name] = seg
    return out


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2

    old_path = Path(sys.argv[1])
    if not old_path.is_file():
        print(f"Not found: {old_path}")
        return 2

    old_methods = class_methods(old_path)
    cache: dict[Path, dict[str, str]] = {}

    print("=" * 70)
    print("B003 method map (old main.py → new file)")
    print("=" * 70)
    for name in sorted(METHOD_TO_FILE, key=lambda n: str(METHOD_TO_FILE[n])):
        rel = METHOD_TO_FILE[name].relative_to(ROOT)
        print(f"  {name:40} → {rel}")

    print("\n" + "=" * 70)
    print("Body comparison (old method vs new file)")
    print("=" * 70)

    matched = mismatched = missing = 0
    for name, new_file in sorted(METHOD_TO_FILE.items(), key=lambda x: str(x[1])):
        old_body = old_methods.get(name)
        if old_body is None:
            print(f"  SKIP  {name}: not in old main (maybe renamed or B002+ changed)")
            missing += 1
            continue
        if new_file not in cache:
            cache[new_file] = class_methods(new_file)
        new_body = cache[new_file].get(name)
        if new_body is None:
            print(f"  FAIL  {name}: missing in {new_file.name}")
            mismatched += 1
            continue
        if normalize(old_body) == normalize(new_body):
            print(f"  OK    {name} ({new_file.relative_to(ROOT)})")
            matched += 1
        else:
            print(
                f"  DIFF  {name} ({new_file.relative_to(ROOT)}) "
                f"old={len(old_body)} chars new={len(new_body)} chars"
            )
            mismatched += 1

    print("\n" + "=" * 70)
    print(f"Results: {matched} identical, {mismatched} different, {missing} absent in old")
    print("App-only (not in map):", ", ".join(sorted(APP_ONLY)))
    print("\nNote: DIFF on exercises often means old snapshot is pre-B002 (validators/codes_match).")
    print("Behavioral parity: run scripts/qa_*_b002.py (239 checks).")
    print("=" * 70)
    return 1 if mismatched else 0


if __name__ == "__main__":
    raise SystemExit(main())

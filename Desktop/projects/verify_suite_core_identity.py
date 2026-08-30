#!/usr/bin/env python3
"""Suite identity gate (B016 3A/19A): 1F CORE symbols must match across all five projects.

Compare every project's session_common CORE definitions to each other (no owner project).
Must pass when full 5-way core alignment is required (B016 complete).

Run from projects/:
  python3 verify_suite_core_identity.py
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

PROJECTS_ROOT = Path(__file__).resolve().parent
PROJECT_DIRS = [
    "pandas-practice-lite",
    "scipy-practice",
    "python-basics",
    "puzzle-rush-game",
    "matplotlib-practice",
]

# Locked B016 Item 1F CORE membership
CORE_NAMES = frozenset(
    {
        "MAX_ATTEMPTS",
        "SESSION_BANNER_WIDTH",
        "INTER_ITEM_GAP",
        "_SPECIAL_SKIP",
        "_SPECIAL_EXIT",
        "_SPECIAL_QUIT",
        "SessionExit",
        "QuestionOutcome",
        "classify_special_input",
        "code_prompt",
        "print_wrong_attempt",
        "print_correct_answer",
        "print_partial_exit_score",
        "print_teach_intro",
        "print_question_header",
    }
)


def _core_source_map(path: Path) -> dict[str, str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found: dict[str, str] = {}
    for node in tree.body:
        name: str | None = None
        if isinstance(node, ast.Assign):
            if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                name = node.targets[0].id
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            name = node.name
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            name = node.target.id
        if name is not None and name in CORE_NAMES:
            found[name] = ast.dump(node, include_attributes=False)
    return found


def main() -> int:
    maps: dict[str, dict[str, str]] = {}
    errors: list[str] = []

    for name in PROJECT_DIRS:
        path = PROJECTS_ROOT / name / "session_common.py"
        if not path.is_file():
            errors.append(f"MISSING file: {path}")
            continue
        core = _core_source_map(path)
        missing = sorted(CORE_NAMES - core.keys())
        if missing:
            errors.append(f"{name}: missing CORE symbols: {', '.join(missing)}")
        maps[name] = core

    if len(maps) < 2:
        print("FAIL: not enough projects with session_common.py")
        for e in errors:
            print(f"  {e}")
        return 1

    names = list(maps.keys())
    baseline = names[0]
    base = maps[baseline]

    for other in names[1:]:
        a, b = base, maps[other]
        for sym in sorted(CORE_NAMES):
            if sym not in a or sym not in b:
                continue
            if a[sym] != b[sym]:
                errors.append(
                    f"DIFF {sym}: {baseline} vs {other}"
                )

    if errors:
        print("FAIL: suite CORE identity")
        for e in errors:
            print(f"  {e}")
        return 1

    print("OK: suite CORE identity (all five match)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

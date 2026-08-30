#!/usr/bin/env python3
"""
B002 extension — menus and plot questions (lightweight).

- Exploration menu: options 1–9 + error paths (mocked input, no ESC wait).
- Plot questions: exercises 1, 2, 4 question 8 only (Agg backend, plt.show mocked).

No subprocess, no GUI windows.

Run from project root: python3 scripts/qa_menus_b002.py
"""

from __future__ import annotations

import io
import os
import random
import sys
import time
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import MagicMock, patch

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from main import PandasPractice

_pass = 0
_fail = 0
_failures: list[str] = []

_SAMPLE_COL = "category"
_FILTER_VAL = "Electronics"


def record(name: str, ok: bool, detail: str = "") -> None:
    global _pass, _fail
    if ok:
        _pass += 1
    else:
        _fail += 1
        line = f"FAIL: {name}"
        if detail:
            line += f" — {detail}"
        _failures.append(line)


def _input_queue(initial: list[str]):
    queue = list(initial) + [""] * 64

    def fake(_prompt: str = "") -> str:
        return queue.pop(0) if queue else ""

    return fake


def _patches(input_fn):
    return [
        patch("builtins.input", side_effect=input_fn),
        patch.object(PandasPractice, "wait_for_esc", lambda self: None),
        # Default: run each option once, then return to the exploration menu.
        patch.object(PandasPractice, "_repeat_or_return", lambda self: False),
        patch("random.randint", return_value=10),
        patch("random.choice", side_effect=lambda s: list(s)[0] if len(list(s)) else None),
        patch("random.sample", side_effect=lambda pop, k: list(pop)[:k]),
    ]


def make_app() -> PandasPractice:
    return PandasPractice()


def run_explore(app: PandasPractice, inputs: list[str]) -> str:
    buf = io.StringIO()
    fake = _input_queue(inputs)
    ps = _patches(fake)
    for p in ps:
        p.start()
    try:
        with redirect_stdout(buf):
            app.explore_dataset()
    finally:
        for p in ps:
            p.stop()
    return buf.getvalue()


def run_exercise(app: PandasPractice, ex_num: int, inputs: list[str]) -> str:
    methods = {
        1: app.exercise_1_basic_operations,
        2: app.exercise_2_filtering,
        4: app.exercise_4_data_manipulation,
    }
    buf = io.StringIO()
    fake = _input_queue(inputs)
    ps = _patches(fake)
    for p in ps:
        p.start()
    try:
        with redirect_stdout(buf):
            methods[ex_num]()
    finally:
        for p in ps:
            p.stop()
    return buf.getvalue()


def parse_skip_answer(stdout: str) -> str | None:
    answer = None
    for line in stdout.splitlines():
        stripped = line.strip()
        if stripped.startswith("Correct answer:"):
            answer = stripped.split("Correct answer:", 1)[1].strip()
    return answer


def test_explore_happy_path_all_options() -> None:
    app = make_app()
    inputs = [
        "1",
        "5",
        "2",
        "5",
        "3",
        "4",
        "5",
        _SAMPLE_COL,
        "6",
        _SAMPLE_COL,
        _FILTER_VAL,
        "7",
        "quantity",
        "a",
        "8",
    ]
    out = run_explore(app, inputs)
    markers = [
        ("explore head", "First 5 rows"),
        ("explore tail", "Last 5 rows"),
        ("explore info", "Dataset Info"),
        ("explore describe", "Basic Statistics"),
        ("explore unique", f"Unique values in '{_SAMPLE_COL}'"),
        ("explore filter", "Filtered results"),
        ("explore sort", "Sorted data"),
    ]
    for name, needle in markers:
        record(name, needle in out)
    record("explore menu shown", "DATASET EXPLORATION MENU" in out)
    record(
        "explore info/stats no repeat prompt",
        "Press Enter to run this option again" not in out,
    )


def test_explore_exit_hint_on_typed_prompts() -> None:
    """Exit/quit affordance appears in input() prompts for options 1 and 5."""
    app = make_app()
    hint = "or type 'exit'/'quit' to return"
    seen: list[str] = []

    def run_with(inputs: list[str]) -> None:
        seen.clear()
        answers = iter(inputs)

        def capturing_input(prompt=""):
            seen.append(str(prompt))
            try:
                return next(answers)
            except StopIteration:
                return "8"

        ps = [
            patch("builtins.input", side_effect=capturing_input),
            patch.object(PandasPractice, "wait_for_esc", lambda self: None),
            patch.object(PandasPractice, "_repeat_or_return", lambda self: False),
        ]
        for p in ps:
            p.start()
        try:
            with redirect_stdout(io.StringIO()):
                app.explore_dataset()
        finally:
            for p in ps:
                p.stop()

    run_with(["1", "5", "8"])
    record("explore row-count prompt has exit hint", any(hint in p for p in seen))

    run_with(["5", "sales_rep", "8"])
    record("explore column prompt has exit hint", any(hint in p for p in seen))

    run_with(["7", "quantity", "a", "8"])
    record("explore sort-order prompt has exit hint", any(hint in p for p in seen))


def test_explore_invalid_and_bad_columns() -> None:
    app = make_app()
    out = run_explore(app, ["99", "8"])
    record("explore invalid option", "Invalid choice" in out)

    # Empty at menu prompt re-prompts (no message), then a valid choice works.
    out = run_explore(app, ["", "8"])
    record("explore empty re-prompt no invalid", "Invalid choice" not in out)
    record("explore empty then exit", out.count("DATASET EXPLORATION MENU") >= 1)

    # Bad column re-prompts in place, then a valid column is accepted.
    out = run_explore(app, ["5", "not_a_column_xyz", _SAMPLE_COL, "8"])
    record("explore bad column unique", "Column 'not_a_column_xyz' not found" in out)
    record("explore bad column unique recovers", f"Unique values in '{_SAMPLE_COL}'" in out)

    out = run_explore(app, ["6", "bad_col", _SAMPLE_COL, _FILTER_VAL, "8"])
    record("explore bad column filter", "Column 'bad_col' not found" in out)
    record("explore bad column filter recovers", "Filtered results" in out)

    out = run_explore(app, ["7", "bad_col", "quantity", "a", "8"])
    record("explore bad column sort", "Column 'bad_col' not found" in out)
    record("explore bad column sort recovers", "Sorted data" in out)

    # Empty at column prompt re-prompts; valid column then proceeds.
    out = run_explore(app, ["5", "", _SAMPLE_COL, "8"])
    record(
        "explore column empty re-prompt then accepts",
        f"Unique values in '{_SAMPLE_COL}'" in out,
    )
    record(
        "explore column empty no not-found for blank",
        "Column '' not found" not in out,
    )

    # Exit/exit/Quit/quit leave the sub-prompt for the exploration menu.
    out = run_explore(app, ["5", "exit", "8"])
    record("explore exit returns to menu", out.count("DATASET EXPLORATION MENU") >= 2)
    out = run_explore(app, ["5", "EXIT", _SAMPLE_COL, "8"])
    record(
        "explore EXIT rejected as exit word",
        f"Unique values in '{_SAMPLE_COL}'" in out
        or "Column 'EXIT' not found" in out,
    )
    out = run_explore(app, ["5", "cancel", _SAMPLE_COL, "8"])
    record(
        "explore cancel is not an exit word",
        f"Unique values in '{_SAMPLE_COL}'" in out
        or "Column 'cancel' not found" in out,
    )


def test_explore_row_count_validation() -> None:
    app = make_app()
    n_rows = len(app.current_dataset)

    # Zero is out of range: reject, then accept a valid count.
    out = run_explore(app, ["1", "0", "5", "8"])
    record("head rejects 0", "between 1 and" in out)
    record("head accepts valid after reject", "First 5 rows" in out)

    # Above the row count is out of range.
    out = run_explore(app, ["1", str(n_rows + 1), "5", "8"])
    record("head rejects above max", "between 1 and" in out)

    # Non-numeric garbage is rejected.
    out = run_explore(app, ["2", "dkjgd", "5", "8"])
    record("tail rejects non-numeric", "between 1 and" in out)
    record("tail accepts valid after reject", "Last 5 rows" in out)

    # Empty input re-prompts (no default); then an explicit count works.
    out = run_explore(app, ["1", "", "5", "8"])
    record("head empty then explicit count", "First 5 rows" in out)
    record("head empty no between-error", out.count("between 1 and") == 0)


def test_explore_sort_order_validation() -> None:
    app = make_app()

    # Garbage direction (and now-invalid yes/no) is rejected, then 'd' is accepted.
    out = run_explore(app, ["7", "quantity", "maybe", "yes", "d", "8"])
    record(
        "sort rejects bad direction",
        "Please enter 'a' for ascending or 'd' for descending" in out,
    )
    record("sort accepts valid after reject", "Sorted data" in out)


def test_explore_filter_value_validation() -> None:
    app = make_app()

    # Numeric column with non-numeric value is rejected, then accepted.
    out = run_explore(app, ["6", "quantity", "abc", "5", "8"])
    record("filter rejects non-numeric value", "Please enter a numeric value" in out)
    record("filter accepts numeric after reject", "Filtered results" in out)


def test_explore_sort_only_a_or_d() -> None:
    app = make_app()
    # Spelled-out directions are no longer accepted; only 'a'/'d'.
    out = run_explore(app, ["7", "quantity", "ascending", "a", "8"])
    record(
        "sort rejects spelled-out 'ascending'",
        "Please enter 'a' for ascending or 'd' for descending" in out,
    )
    record("sort accepts 'a'", "Sorted data" in out)

    # Uppercase A/D are not accepted.
    out = run_explore(app, ["7", "quantity", "A", "a", "8"])
    record(
        "sort rejects uppercase 'A'",
        "Please enter 'a' for ascending or 'd' for descending" in out,
    )
    record("sort accepts lowercase 'a' after 'A'", "Sorted data" in out)


def test_explore_option_loop() -> None:
    """Each option can be run repeatedly until ESC (here: run twice, then return)."""
    app = make_app()
    fake = _input_queue(["1", "5", "10", "8"])
    repeat = iter([True, False])
    ps = [
        patch("builtins.input", side_effect=fake),
        patch.object(PandasPractice, "wait_for_esc", lambda self: None),
        patch.object(PandasPractice, "_repeat_or_return", lambda self: next(repeat)),
    ]
    for p in ps:
        p.start()
    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            app.explore_dataset()
    finally:
        for p in ps:
            p.stop()
    out = buf.getvalue()
    record("option loop first run (5)", "First 5 rows" in out)
    record("option loop second run (10)", "First 10 rows" in out)
    record("option loop returns to menu after ESC", out.count("DATASET EXPLORATION MENU") >= 2)


def test_main_menu_flat_options() -> None:
    app = make_app()
    buf = io.StringIO()
    fake = _input_queue(["7"])
    with patch("builtins.input", side_effect=fake):
        with redirect_stdout(buf):
            app.main_menu()
    out = buf.getvalue()
    record("flat menu basic ops", "1. Basic Operations" in out)
    record("flat menu explore", "6. Explore Dataset" in out)
    record("flat menu no statistics", "Statistics" not in out)
    record("flat menu goodbye", "👋" in out)


def test_execute_plot_code_no_gui() -> None:
    app = make_app()
    df = app.current_dataset
    code = "df.plot(x='quantity', y='total_sales', kind='scatter')"
    show_mock = MagicMock()
    with patch("matplotlib.pyplot.show", show_mock):
        result, err = app.execute_pandas_code(df, code, include_plotting=True)
    record("plot execute no error", err is None, repr(err))
    record("plot show not required for pass", result is None or err is None)
    record("plt.show not called", show_mock.call_count == 0)


def test_plot_task_correct(ex_num: int, task_num: int = 8) -> None:
    app = make_app()
    discover = ["skip"] * task_num + ["exit"]
    out = run_exercise(app, ex_num, discover)
    golden = parse_skip_answer(out)
    record(f"ex{ex_num} plot golden discovered", bool(golden), repr(golden))
    if not golden:
        return
    trial = ["skip"] * (task_num - 1) + [golden, "exit"]
    show_mock = MagicMock()
    with patch("matplotlib.pyplot.show", show_mock):
        out2 = run_exercise(app, ex_num, trial)
    record(
        f"ex{ex_num} task{task_num} plot correct",
        "✓ Correct!" in out2,
    )
    record(f"ex{ex_num} plot no plt.show", show_mock.call_count == 0)


def test_plot_task_wrong(ex_num: int, task_num: int = 8) -> None:
    app = make_app()
    inputs = ["skip"] * (task_num - 1) + ["bad", "bad", "bad", "exit"]
    out = run_exercise(app, ex_num, inputs)
    record(
        f"ex{ex_num} task{task_num} plot wrong",
        out.count("Correct answer:") >= 1 and "Incorrect" in out,
    )


def main() -> int:
    os.chdir(_ROOT)
    t0 = time.perf_counter()

    print("=" * 70)
    print("QA Developer — B002 menus / plots (lightweight)")
    print("=" * 70)

    test_explore_happy_path_all_options()
    test_explore_exit_hint_on_typed_prompts()
    test_explore_invalid_and_bad_columns()
    test_explore_row_count_validation()
    test_explore_sort_order_validation()
    test_explore_filter_value_validation()
    test_explore_sort_only_a_or_d()
    test_explore_option_loop()
    test_main_menu_flat_options()
    test_execute_plot_code_no_gui()
    for ex in (1, 2, 4):
        test_plot_task_correct(ex)
        test_plot_task_wrong(ex)

    elapsed = time.perf_counter() - t0
    total = _pass + _fail
    print(f"\nPassed: {_pass}/{total}")
    print(f"Failed: {_fail}/{total}")
    print(f"Elapsed: {elapsed:.2f}s")
    if _failures:
        print("\nFailures:")
        for line in _failures:
            print(f"  {line}")
    print("=" * 70)
    return 1 if _fail else 0


if __name__ == "__main__":
    sys.exit(main())

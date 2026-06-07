#!/usr/bin/env python3
"""
B002 extension — menus, statistics, and plot tasks (lightweight).

- Exploration menu: options 1–9 + error paths (mocked input, no ESC wait).
- Statistics submenu: empty / populated, reset yes/no, invalid choices.
- Plot tasks: exercises 1, 2, 4 task 8 only (Agg backend, plt.show mocked).

No subprocess, no GUI windows. Uses a temp progress.json so your real
progress.json is not modified.

Run from project root: python3 scripts/qa_menus_b002.py
"""

from __future__ import annotations

import io
import os
import random
import sys
import tempfile
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

# Stable column/value for exploration options 7–9
_SAMPLE_COL = "category"
_FILTER_VAL = "Electronics"  # present in sales_data.csv


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
        patch("random.randint", return_value=10),
        patch("random.choice", side_effect=lambda s: list(s)[0] if len(list(s)) else None),
        patch("random.sample", side_effect=lambda pop, k: list(pop)[:k]),
    ]


def make_app(progress: dict | None = None) -> tuple[PandasPractice, tempfile.TemporaryDirectory]:
    """App with isolated progress file (dataset still loads once)."""
    tmp = tempfile.TemporaryDirectory(prefix="qa_b002_")
    app = PandasPractice()
    app.progress_file = Path(tmp.name) / "progress.json"
    app.progress = progress or {"exercise_stats": {}, "last_session": None}
    return app, tmp


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


def run_statistics(app: PandasPractice, inputs: list[str]) -> str:
    buf = io.StringIO()
    fake = _input_queue(inputs)
    ps = _patches(fake)
    for p in ps:
        p.start()
    try:
        with redirect_stdout(buf):
            app.show_statistics()
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
    if "📖 CORRECT ANSWER:" not in stdout:
        return None
    block = stdout.split("📖 CORRECT ANSWER:")[-1]
    if "💡 Explanation:" in block:
        block = block.split("💡 Explanation:")[0]
    for line in block.splitlines():
        s = line.strip()
        if s and not s.startswith("=") and not s.startswith("💡"):
            return s
    return None


# --- Exploration menu ---


def test_explore_happy_path_all_options() -> None:
    """One loop through options 1–8 then 9 return (single init — fast)."""
    app, tmp = make_app()
    try:
        inputs = [
            "1",
            "5",  # head rows
            "2",
            "5",  # tail
            "3",  # info
            "4",  # describe
            "5",  # dtypes
            "6",
            _SAMPLE_COL,
            "7",
            _SAMPLE_COL,
            _FILTER_VAL,
            "8",
            "quantity",
            "yes",
            "9",
        ]
        out = run_explore(app, inputs)
        markers = [
            ("explore head", "First 5 rows"),
            ("explore tail", "Last 5 rows"),
            ("explore info", "Dataset Info"),
            ("explore describe", "Basic Statistics"),
            ("explore dtypes", "Columns and Data Types"),
            ("explore unique", f"Unique values in '{_SAMPLE_COL}'"),
            ("explore filter", "Filtered results"),
            ("explore sort", "Sorted data"),
        ]
        for name, needle in markers:
            record(name, needle in out)
        record("explore menu shown", "DATASET EXPLORATION MENU" in out)
    finally:
        tmp.cleanup()


def test_explore_invalid_and_bad_columns() -> None:
    app, tmp = make_app()
    try:
        out = run_explore(app, ["99", "9"])
        record("explore invalid option", "Invalid choice" in out)

        out = run_explore(app, ["6", "not_a_column_xyz", "9"])
        record("explore bad column unique", "Column 'not_a_column_xyz' not found" in out)

        out = run_explore(app, ["7", "bad_col", "9"])
        record("explore bad column filter", "Column 'bad_col' not found" in out)

        out = run_explore(app, ["8", "bad_col", "9"])
        record("explore bad column sort", "Column 'bad_col' not found" in out)
    finally:
        tmp.cleanup()


# --- Statistics submenu ---


def test_statistics_empty_back() -> None:
    app, tmp = make_app()
    try:
        out = run_statistics(app, ["1"])
        record("stats empty message", "No exercises completed yet" in out)
        record("stats empty back", "YOUR LEARNING STATISTICS" in out)
    finally:
        tmp.cleanup()


def test_statistics_empty_invalid() -> None:
    app, tmp = make_app()
    try:
        out = run_statistics(app, ["2", "1"])
        record("stats empty invalid", out.count("Invalid choice") >= 1)
    finally:
        tmp.cleanup()


def test_statistics_with_data_and_back() -> None:
    progress = {
        "exercise_stats": {
            "exercise_1": {"count": 1, "total_grade": 62.5, "grades": [62.5]},
        },
        "last_session": "2026-06-01T12:00:00",
    }
    app, tmp = make_app(progress)
    try:
        out = run_statistics(app, ["2"])
        record("stats shows exercise", "Exercise 1: Basic Operations" in out)
        record("stats shows grade", "Average Grade" in out)
        record("stats shows session", "Last Session" in out)
    finally:
        tmp.cleanup()


def test_statistics_reset_cancel() -> None:
    progress = {
        "exercise_stats": {
            "exercise_2": {"count": 1, "total_grade": 50.0, "grades": [50.0]},
        },
        "last_session": "2026-06-01T12:00:00",
    }
    app, tmp = make_app(progress)
    try:
        out = run_statistics(app, ["1", "no", "2"])
        record("stats reset cancelled", "Reset cancelled" in out)
        record("stats still has data after cancel", "exercise_2" in str(app.progress))
    finally:
        tmp.cleanup()


def test_statistics_reset_confirm() -> None:
    progress = {
        "exercise_stats": {
            "exercise_3": {"count": 1, "total_grade": 100.0, "grades": [100.0]},
        },
        "last_session": "2026-06-01T12:00:00",
    }
    app, tmp = make_app(progress)
    try:
        run_statistics(app, ["1", "yes"])
        record(
            "stats reset confirm",
            app.progress.get("exercise_stats") == {},
        )
    finally:
        tmp.cleanup()


def test_statistics_invalid_then_back() -> None:
    progress = {
        "exercise_stats": {
            "exercise_4": {"count": 1, "total_grade": 25.0, "grades": [25.0]},
        },
        "last_session": "2026-06-01T12:00:00",
    }
    app, tmp = make_app(progress)
    try:
        out = run_statistics(app, ["9", "2"])
        record("stats invalid choice", "Invalid choice" in out)
    finally:
        tmp.cleanup()


# --- Plot tasks (task 8) — no display window ---


def test_execute_plot_code_no_gui() -> None:
    app, tmp = make_app()
    try:
        df = app.current_dataset
        code = "df.plot(x='quantity', y='total_sales', kind='scatter')"
        show_mock = MagicMock()
        with patch("matplotlib.pyplot.show", show_mock):
            result, err = app.execute_pandas_code(df, code, include_plotting=True)
        record("plot execute no error", err is None, repr(err))
        record("plot show not required for pass", result is None or err is None)
        record("plt.show not called", show_mock.call_count == 0)
    finally:
        tmp.cleanup()


def test_plot_task_correct(ex_num: int, task_num: int = 8) -> None:
    app, tmp = make_app()
    try:
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
            "✅ Correct!" in out2 and "non-interactive" in out.lower() or "✅ Correct!" in out2,
        )
        record(f"ex{ex_num} plot no plt.show", show_mock.call_count == 0)
    finally:
        tmp.cleanup()


def test_plot_task_wrong(ex_num: int, task_num: int = 8) -> None:
    app, tmp = make_app()
    try:
        inputs = ["skip"] * (task_num - 1) + ["bad", "bad", "bad", "exit"]
        out = run_exercise(app, ex_num, inputs)
        record(
            f"ex{ex_num} task{task_num} plot wrong",
            out.count("CORRECT ANSWER") >= 1 and "Incorrect" in out,
        )
    finally:
        tmp.cleanup()


def main() -> int:
    os.chdir(_ROOT)
    t0 = time.perf_counter()

    print("=" * 70)
    print("QA Developer — B002 menus / stats / plots (lightweight)")
    print("=" * 70)

    test_explore_happy_path_all_options()
    test_explore_invalid_and_bad_columns()
    test_statistics_empty_back()
    test_statistics_empty_invalid()
    test_statistics_with_data_and_back()
    test_statistics_reset_cancel()
    test_statistics_reset_confirm()
    test_statistics_invalid_then_back()
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

#!/usr/bin/env python3
"""
QA Developer — B001 three-strike flow (all 18 exercises where applicable).

Step 1 of each exercise: three wrong answers → exercise aborts with the
correct skip or terminate message (pie step 1 always skips, even on last).

Pie exercise 3 additionally: late-step terminate on last exercise.

Run: python3 scripts/qa_flow_three_strike_b001.py
"""

from __future__ import annotations

import io
import random
import sys
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from exercise_common import MSG_SKIP, MSG_TERMINATE, prompt_code_step

WRONG = "___qa_wrong___"
SEED = 42

_pass = 0
_fail = 0
_failures: list[str] = []


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


def always_wrong(_: str):
    return False, "Invalid format"


def run_first_step_three_wrong(mod, exercise: dict, is_last: bool) -> tuple[bool, str]:
    """Feed three wrong answers on step 1 only; capture output."""
    inputs = [WRONG, WRONG, WRONG]
    buf = io.StringIO()
    with patch("builtins.input", side_effect=inputs):
        with redirect_stdout(buf):
            completed = mod.run_exercise(exercise, is_last=is_last)
    return completed, buf.getvalue()


def expect_step1_messages(module_key: str, is_last: bool) -> tuple[bool, bool]:
    """Return (must_have_skip, must_have_terminate) for step 1."""
    if module_key == "pie":
        return True, False
    if is_last:
        return False, True
    return True, False


def test_prompt_code_step_helper() -> None:
    """Shared helper used by histogram (and available to other modules)."""
    buf = io.StringIO()
    with patch("builtins.input", side_effect=[WRONG, WRONG, WRONG]):
        with redirect_stdout(buf):
            ok, _ = prompt_code_step(always_wrong, 0, is_last=False, skip_only=False)
    out = buf.getvalue()
    record("helper not last → skip", (not ok) and MSG_SKIP in out)

    buf = io.StringIO()
    with patch("builtins.input", side_effect=[WRONG, WRONG, WRONG]):
        with redirect_stdout(buf):
            ok, _ = prompt_code_step(always_wrong, 0, is_last=True, skip_only=False)
    out = buf.getvalue()
    record("helper last → terminate", (not ok) and MSG_TERMINATE in out)

    buf = io.StringIO()
    with patch("builtins.input", side_effect=[WRONG, WRONG, WRONG]):
        with redirect_stdout(buf):
            ok, _ = prompt_code_step(always_wrong, 0, is_last=True, skip_only=True)
    out = buf.getvalue()
    record(
        "helper skip_only on last",
        (not ok) and MSG_SKIP in out and MSG_TERMINATE not in out,
    )


def test_all_eighteen_exercises_step1() -> None:
    """Every exercise: step 1, three wrong answers."""
    import importlib

    class_map = {
        "histogram": "histogram_exercises.HistogramExercises",
        "plot": "plot_exercises.PlotExercises",
        "subplot": "subplot_exercises.SubplotExercises",
        "scatter": "scatter_plot_exercises.ScatterPlotExercises",
        "bar": "bar_plot_exercises.BarPlotExercises",
        "pie": "pie_chart_exercises.PieChartExercises",
    }

    for key in class_map:
        module_name, class_name = class_map[key].rsplit(".", 1)
        mod_cls = getattr(importlib.import_module(module_name), class_name)
        random.seed(SEED)
        instance = mod_cls()
        n = len(instance.exercises)
        for i, exercise in enumerate(instance.exercises):
            is_last = i == n - 1
            ex_num = exercise.get("number", i + 1)
            prefix = f"{key} ex{ex_num} step1"

            completed, out = run_first_step_three_wrong(instance, exercise, is_last)
            record(f"{prefix} → abort", completed is False)

            want_skip, want_term = expect_step1_messages(key, is_last)
            record(
                f"{prefix} → skip message",
                (not want_skip) or (MSG_SKIP in out),
                "" if (not want_skip) or (MSG_SKIP in out) else "missing skip",
            )
            record(
                f"{prefix} → terminate message",
                (not want_term) or (MSG_TERMINATE in out),
                ""
                if (not want_term) or (MSG_TERMINATE in out)
                else "missing terminate",
            )
            if want_skip and want_term:
                record(f"{prefix} → no spurious terminate", MSG_TERMINATE not in out)
            if key == "pie":
                record(f"{prefix} → pie no terminate on step1", MSG_TERMINATE not in out)


def _np_int_array(var: str, values: list[int]) -> str:
    inner = ", ".join(map(str, values))
    return f"{var} = np.array([{inner}])"


def _np_str_array(var: str, values: list[str]) -> str:
    inner = ", ".join(f'"{v}"' for v in values)
    return f"{var} = np.array([{inner}])"


def test_pie_ex3_late_step_terminate() -> None:
    """Pie only: after step 3, plt.pie step on last exercise uses terminate."""
    from pie_chart_exercises import PieChartExercises

    random.seed(SEED)
    mod = PieChartExercises()
    ex = mod.exercises[2]
    inputs = [
        _np_int_array("x", ex["proportions"]),
        _np_str_array("c", ex["colors"]),
        _np_str_array("lb", ex["labels"]),
        WRONG,
        WRONG,
        WRONG,
    ]
    buf = io.StringIO()
    with patch("builtins.input", side_effect=inputs):
        with redirect_stdout(buf):
            completed = mod.run_exercise(ex, is_last=True)
    record("pie ex3 late step → abort", completed is False)
    record("pie ex3 late step → terminate", MSG_TERMINATE in buf.getvalue())


def main() -> int:
    test_prompt_code_step_helper()
    test_all_eighteen_exercises_step1()
    test_pie_ex3_late_step_terminate()

    total = _pass + _fail
    print("=" * 70)
    print("QA Developer — B001 three-strike (18 exercises + pie late step)")
    print("=" * 70)
    print(f"Passed: {_pass}/{total}")
    print(f"Failed: {_fail}/{total}")
    if _failures:
        print("\nFailures:")
        for line in _failures:
            print(f"  {line}")
    print("=" * 70)
    return 1 if _fail else 0


if __name__ == "__main__":
    sys.exit(main())

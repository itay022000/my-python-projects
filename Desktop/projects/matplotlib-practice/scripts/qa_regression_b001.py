#!/usr/bin/env python3
"""
QA Developer — B001 exercise verification suite (QA-owned artifact).

Scope: all 18 exercises (6 sequences × 3 exercises). For every verify_* step used in
run_exercise, tests one correct answer and one wrong answer (228 checks total).

This is the comprehensive correct/wrong bar for validators — same functions the CLI
uses when learners type code. Does not re-type prompts via stdin (see B001-qa-walkthrough.md).

Run: python3 scripts/qa_regression_b001.py  (from project root)
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

# Project root on path so imports match main.py
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from exercises.bar_plot_exercises import BarPlotExercises
from engine import normalize_code, verify_step_show
from exercises.histogram_exercises import HistogramExercises
from exercises.pie_chart_exercises import PieChartExercises
from exercises.plot_exercises import PlotExercises
from exercises.scatter_plot_exercises import ScatterPlotExercises
from exercises.subplot_exercises import SubplotExercises

WRONG = "___definitely_wrong_qa_input___"

_pass = 0
_fail = 0
_failures: list[str] = []


def _record(name: str, ok: bool, detail: str = "") -> None:
    global _pass, _fail
    if ok:
        _pass += 1
    else:
        _fail += 1
        line = f"FAIL: {name}"
        if detail:
            line += f" — {detail}"
        _failures.append(line)


def _np_int_array(var: str, values: list[int]) -> str:
    inner = ", ".join(map(str, values))
    return f"{var} = np.array([{inner}])"


def _np_str_array(var: str, values: list[str], quote: str = '"') -> str:
    inner = ", ".join(f"{quote}{v}{quote}" for v in values)
    return f"{var} = np.array([{inner}])"


def assert_correct(name: str, fn, code: str, expected_msg: str = "Correct!") -> None:
    ok, msg = fn(code)
    _record(
        f"{name} [correct]",
        ok and msg == expected_msg,
        f"got ({ok!r}, {msg!r}), expected (True, {expected_msg!r})",
    )


def assert_wrong(name: str, fn, code: str = WRONG) -> None:
    ok, msg = fn(code)
    _record(
        f"{name} [wrong]",
        (not ok) and bool(msg),
        f"got ({ok!r}, {msg!r})",
    )


# --- exercise_common ---


def test_exercise_common() -> None:
    assert normalize_code("  x  =  np.array( [ 1 , 2 ] ) ") == "x=np.array([1 , 2])"
    assert normalize_code("plt.show()") == "plt.show()"
    assert normalize_code("  plt.show( )  ") == "plt.show()"
    _record("normalize_code", True)

    assert_correct("verify_step_show", verify_step_show, "plt.show()")
    assert_wrong("verify_step_show", verify_step_show, "plt.show")


# --- histogram ---


def test_histogram_module(mod: HistogramExercises) -> None:
    for ex in mod.exercises:
        n = ex["number"]
        step1 = (
            f"x = np.random.normal({ex['mean']}, {ex['std']}, {ex['size']})"
        )
        assert_correct(
            f"histogram ex{n} verify_step1",
            lambda c: mod.verify_step1(c, ex["mean"], ex["std"], ex["size"]),
            step1,
        )
        assert_wrong(
            f"histogram ex{n} verify_step1",
            lambda c: mod.verify_step1(c, ex["mean"], ex["std"], ex["size"]),
        )

        assert_correct(f"histogram ex{n} verify_step2", mod.verify_step2, "plt.hist(x)")
        assert_wrong(f"histogram ex{n} verify_step2", mod.verify_step2)

        assert_correct(f"histogram ex{n} verify_step_show", verify_step_show, "plt.show()")
        assert_wrong(f"histogram ex{n} verify_step_show", verify_step_show)


# --- bar ---


def _bar_step3(ex: dict) -> str:
    if ex["is_horizontal"]:
        c, h = ex["color"], ex["height"]
        return f'plt.barh(x, y, color="{c}", height={h})'
    if ex["has_width"]:
        return f"plt.bar(x, y, width={ex['width']})"
    return "plt.bar(x, y)"


def test_bar_module(mod: BarPlotExercises) -> None:
    for ex in mod.exercises:
        n = ex["number"]
        assert_correct(
            f"bar ex{n} verify_step1",
            lambda c: mod.verify_step1(c, ex["labels"]),
            _np_str_array("x", ex["labels"]),
        )
        assert_wrong(
            f"bar ex{n} verify_step1",
            lambda c: mod.verify_step1(c, ex["labels"]),
        )

        assert_correct(
            f"bar ex{n} verify_step2",
            lambda c: mod.verify_step2(c, ex["heights"]),
            _np_int_array("y", ex["heights"]),
        )
        assert_wrong(
            f"bar ex{n} verify_step2",
            lambda c: mod.verify_step2(c, ex["heights"]),
        )

        step3 = _bar_step3(ex)
        assert_correct(
            f"bar ex{n} verify_step3",
            lambda c: mod.verify_step3(
                c,
                ex["has_width"],
                ex.get("width"),
                ex["is_horizontal"],
                ex.get("color"),
                ex.get("height"),
            ),
            step3,
        )
        assert_wrong(
            f"bar ex{n} verify_step3",
            lambda c: mod.verify_step3(
                c,
                ex["has_width"],
                ex.get("width"),
                ex["is_horizontal"],
                ex.get("color"),
                ex.get("height"),
            ),
        )

        assert_correct(f"bar ex{n} verify_step_show", verify_step_show, "plt.show()")
        assert_wrong(f"bar ex{n} verify_step_show", verify_step_show)


# --- pie ---


def _pie_step4(ex: dict) -> str:
    call = "plt.pie(x, labels=lb, colors=c"
    if ex.get("has_explode"):
        call += ", explode=ex"
    if ex["has_shadow"]:
        call += ", shadow=True"
    return call + ")"


def test_pie_module(mod: PieChartExercises) -> None:
    for ex in mod.exercises:
        n = ex["number"]
        assert_correct(
            f"pie ex{n} verify_step1",
            lambda c: mod.verify_step1(c, ex["proportions"]),
            _np_int_array("x", ex["proportions"]),
        )
        assert_wrong(
            f"pie ex{n} verify_step1",
            lambda c: mod.verify_step1(c, ex["proportions"]),
        )

        assert_correct(
            f"pie ex{n} verify_step2",
            lambda c: mod.verify_step2(c, ex["colors"]),
            _np_str_array("c", ex["colors"]),
        )
        assert_wrong(
            f"pie ex{n} verify_step2",
            lambda c: mod.verify_step2(c, ex["colors"]),
        )

        assert_correct(
            f"pie ex{n} verify_step3",
            lambda c: mod.verify_step3(c, ex["labels"]),
            _np_str_array("lb", ex["labels"]),
        )
        assert_wrong(
            f"pie ex{n} verify_step3",
            lambda c: mod.verify_step3(c, ex["labels"]),
        )

        if ex.get("has_explode") and ex.get("explode"):
            explode_vals = ", ".join(str(e) for e in ex["explode"])
            explode_code = f"ex = np.array([{explode_vals}])"
            assert_correct(
                f"pie ex{n} verify_step_explode",
                lambda c: mod.verify_step_explode(c, ex["explode"]),
                explode_code,
            )
            assert_wrong(
                f"pie ex{n} verify_step_explode",
                lambda c: mod.verify_step_explode(c, ex["explode"]),
            )

        assert_correct(
            f"pie ex{n} verify_step4",
            lambda c: mod.verify_step4(c, ex["has_shadow"], ex.get("has_explode", False)),
            _pie_step4(ex),
        )
        assert_wrong(
            f"pie ex{n} verify_step4",
            lambda c: mod.verify_step4(c, ex["has_shadow"], ex.get("has_explode", False)),
        )

        if ex["has_legend"]:
            legend_code = (
                'plt.legend(title="fruits")'
                if ex.get("legend_title")
                else "plt.legend()"
            )
            assert_correct(
                f"pie ex{n} verify_step5",
                lambda c: mod.verify_step5(c, True, ex.get("legend_title")),
                legend_code,
            )
            assert_wrong(
                f"pie ex{n} verify_step5",
                lambda c: mod.verify_step5(c, True, ex.get("legend_title")),
            )
        else:
            ok, msg = mod.verify_step5(WRONG, False, None)
            _record(
                f"pie ex{n} verify_step5 [not required]",
                ok and msg == "This step is not required for this exercise.",
                f"got ({ok!r}, {msg!r})",
            )

        assert_correct(f"pie ex{n} verify_step_show", verify_step_show, "plt.show()")
        assert_wrong(f"pie ex{n} verify_step_show", verify_step_show)


# --- scatter ---


def _scatter_plot_code(ex: dict) -> str:
    num = ex["number"]
    if num == 1:
        return f'plt.scatter(x, y, color="{ex["color"]}")'
    if num == 2:
        return "plt.scatter(x, y, c=colors, s=sizes)"
    return (
        f'plt.scatter(x, y, c=colors, s=sizes, alpha={ex["alpha"]}, '
        f'cmap="{ex["cmap"]}")'
    )


def test_scatter_module(mod: ScatterPlotExercises) -> None:
    for ex in mod.exercises:
        n = ex["number"]
        assert_correct(
            f"scatter ex{n} verify_step1",
            lambda c: mod.verify_step1(c, ex["x_coords"]),
            _np_int_array("x", ex["x_coords"]),
        )
        assert_wrong(
            f"scatter ex{n} verify_step1",
            lambda c: mod.verify_step1(c, ex["x_coords"]),
        )

        assert_correct(
            f"scatter ex{n} verify_step2",
            lambda c: mod.verify_step2(c, ex["y_coords"]),
            _np_int_array("y", ex["y_coords"]),
        )
        assert_wrong(
            f"scatter ex{n} verify_step2",
            lambda c: mod.verify_step2(c, ex["y_coords"]),
        )

        if n == 2:
            assert_correct(
                f"scatter ex{n} verify_step3_colors_array",
                lambda c: mod.verify_step3_colors_array(c, ex["colors_array"]),
                _np_str_array("colors", ex["colors_array"]),
            )
            assert_wrong(
                f"scatter ex{n} verify_step3_colors_array",
                lambda c: mod.verify_step3_colors_array(c, ex["colors_array"]),
            )
            assert_correct(
                f"scatter ex{n} verify_step4_sizes",
                lambda c: mod.verify_step4_sizes(c, ex["sizes_array"]),
                _np_int_array("sizes", ex["sizes_array"]),
            )
            assert_wrong(
                f"scatter ex{n} verify_step4_sizes",
                lambda c: mod.verify_step4_sizes(c, ex["sizes_array"]),
            )
        elif n == 3:
            assert_correct(
                f"scatter ex{n} verify_step3_colors_numeric",
                lambda c: mod.verify_step3_colors_numeric(c, ex["colors_array"]),
                _np_int_array("colors", ex["colors_array"]),
            )
            assert_wrong(
                f"scatter ex{n} verify_step3_colors_numeric",
                lambda c: mod.verify_step3_colors_numeric(c, ex["colors_array"]),
            )
            assert_correct(
                f"scatter ex{n} verify_step4_sizes",
                lambda c: mod.verify_step4_sizes(c, ex["sizes_array"]),
                _np_int_array("sizes", ex["sizes_array"]),
            )
            assert_wrong(
                f"scatter ex{n} verify_step4_sizes",
                lambda c: mod.verify_step4_sizes(c, ex["sizes_array"]),
            )

        assert_correct(
            f"scatter ex{n} verify_step_plot",
            lambda c: mod.verify_step_plot(c, ex),
            _scatter_plot_code(ex),
        )
        assert_wrong(
            f"scatter ex{n} verify_step_plot",
            lambda c: mod.verify_step_plot(c, ex),
        )

        assert_correct(f"scatter ex{n} verify_step_show", verify_step_show, "plt.show()")
        assert_wrong(f"scatter ex{n} verify_step_show", verify_step_show)


# --- subplot ---


def test_subplot_module(mod: SubplotExercises) -> None:
    for ex in mod.exercises:
        n = ex["number"]
        x_code = _np_int_array("x", [0, 1, 2, 3])

        assert_correct(f"subplot ex{n} verify_x_array (1)", mod.verify_x_array, x_code)
        assert_wrong(f"subplot ex{n} verify_x_array (1)", mod.verify_x_array)

        assert_correct(
            f"subplot ex{n} verify_y_array (y1)",
            lambda c: mod.verify_y_array(c, ex["y1"]),
            _np_int_array("y", ex["y1"]),
        )
        assert_wrong(
            f"subplot ex{n} verify_y_array (y1)",
            lambda c: mod.verify_y_array(c, ex["y1"]),
        )

        r, c, i = ex["subplot1"]
        assert_correct(
            f"subplot ex{n} verify_subplot (1)",
            lambda code: mod.verify_subplot(code, ex["subplot1"]),
            f"plt.subplot({r}, {c}, {i})",
        )
        assert_wrong(
            f"subplot ex{n} verify_subplot (1)",
            lambda code: mod.verify_subplot(code, ex["subplot1"]),
        )

        assert_correct(f"subplot ex{n} verify_plot (1)", mod.verify_plot, "plt.plot(x, y)")
        assert_wrong(f"subplot ex{n} verify_plot (1)", mod.verify_plot)

        if ex["has_titles"]:
            assert_correct(
                f"subplot ex{n} verify_title (1)",
                lambda c: mod.verify_title(c, ex["title1"]),
                f'plt.title("{ex["title1"]}")',
            )
            assert_wrong(
                f"subplot ex{n} verify_title (1)",
                lambda c: mod.verify_title(c, ex["title1"]),
            )

        assert_correct(f"subplot ex{n} verify_x_array (2)", mod.verify_x_array, x_code)
        assert_wrong(f"subplot ex{n} verify_x_array (2)", mod.verify_x_array)

        assert_correct(
            f"subplot ex{n} verify_y_array (y2)",
            lambda c: mod.verify_y_array(c, ex["y2"]),
            _np_int_array("y", ex["y2"]),
        )
        assert_wrong(
            f"subplot ex{n} verify_y_array (y2)",
            lambda c: mod.verify_y_array(c, ex["y2"]),
        )

        r, c, i = ex["subplot2"]
        assert_correct(
            f"subplot ex{n} verify_subplot (2)",
            lambda code: mod.verify_subplot(code, ex["subplot2"]),
            f"plt.subplot({r}, {c}, {i})",
        )
        assert_wrong(
            f"subplot ex{n} verify_subplot (2)",
            lambda code: mod.verify_subplot(code, ex["subplot2"]),
        )

        assert_correct(f"subplot ex{n} verify_plot (2)", mod.verify_plot, "plt.plot(x, y)")
        assert_wrong(f"subplot ex{n} verify_plot (2)", mod.verify_plot)

        if ex["has_titles"]:
            assert_correct(
                f"subplot ex{n} verify_title (2)",
                lambda c: mod.verify_title(c, ex["title2"]),
                f'plt.title("{ex["title2"]}")',
            )
            assert_wrong(
                f"subplot ex{n} verify_title (2)",
                lambda c: mod.verify_title(c, ex["title2"]),
            )

        if ex.get("has_suptitle"):
            assert_correct(
                f"subplot ex{n} verify_suptitle",
                lambda c: mod.verify_suptitle(c, ex["suptitle"]),
                f'plt.suptitle("{ex["suptitle"]}")',
            )
            assert_wrong(
                f"subplot ex{n} verify_suptitle",
                lambda c: mod.verify_suptitle(c, ex["suptitle"]),
            )

        assert_correct(f"subplot ex{n} verify_step_show", verify_step_show, "plt.show()")
        assert_wrong(f"subplot ex{n} verify_step_show", verify_step_show)


# --- plot ---


def test_plot_module(mod: PlotExercises) -> None:
    for ex in mod.exercises:
        n = ex["number"]

        if n == 1:
            for var in ("y1", "y2", "y3"):
                assert_correct(
                    f"plot ex{n} verify_y_array {var}",
                    lambda c, v=var: mod.verify_y_array(c, v, ex[v]),
                    _np_int_array(var, ex[var]),
                )
                assert_wrong(
                    f"plot ex{n} verify_y_array {var}",
                    lambda c, v=var: mod.verify_y_array(c, v, ex[v]),
                )

            ls, lw, col = ex["linestyle"], ex["linewidth"], ex["color1"]
            line1 = (
                f"plt.plot(y1, linestyle='{ls}', linewidth={lw}, color='{col}')"
            )
            assert_correct(
                f"plot ex{n} verify_step4_line1",
                lambda c: mod.verify_step4_line1(c, ls, lw, col),
                line1,
            )
            assert_wrong(
                f"plot ex{n} verify_step4_line1",
                lambda c: mod.verify_step4_line1(c, ls, lw, col),
            )

            mk, ms, mec, mfc = (
                ex["marker"],
                ex["marker_size"],
                ex["mec"],
                ex["mfc"],
            )
            line2 = f"plt.plot(y2, marker='{mk}', ms={ms}, mec='{mec}', mfc='{mfc}')"
            assert_correct(
                f"plot ex{n} verify_step5_line2",
                lambda c: mod.verify_step5_line2(c, mk, ms, mec, mfc),
                line2,
            )
            assert_wrong(
                f"plot ex{n} verify_step5_line2",
                lambda c: mod.verify_step5_line2(c, mk, ms, mec, mfc),
            )

            fmt = ex["fmt"]
            line3 = f"plt.plot(y3, '{fmt}')"
            assert_correct(
                f"plot ex{n} verify_step6_line3",
                lambda c: mod.verify_step6_line3(c, fmt),
                line3,
            )
            assert_wrong(
                f"plot ex{n} verify_step6_line3",
                lambda c: mod.verify_step6_line3(c, fmt),
            )

        elif n == 2:
            for xvar, yvar in (("x1", "y1"), ("x2", "y2")):
                assert_correct(
                    f"plot ex{n} verify_x_array {xvar}",
                    lambda c, xv=xvar: mod.verify_x_array(c, xv, ex[xv]),
                    _np_int_array(xvar, ex[xvar]),
                )
                assert_wrong(
                    f"plot ex{n} verify_x_array {xvar}",
                    lambda c, xv=xvar: mod.verify_x_array(c, xv, ex[xv]),
                )
                assert_correct(
                    f"plot ex{n} verify_y_array {yvar}",
                    lambda c, yv=yvar: mod.verify_y_array(c, yv, ex[yv]),
                    _np_int_array(yvar, ex[yvar]),
                )
                assert_wrong(
                    f"plot ex{n} verify_y_array {yvar}",
                    lambda c, yv=yvar: mod.verify_y_array(c, yv, ex[yv]),
                )

            assert_correct(
                f"plot ex{n} verify_title",
                lambda c: mod.verify_title(c, ex["title"]),
                f'plt.title("{ex["title"]}")',
            )
            assert_wrong(
                f"plot ex{n} verify_title",
                lambda c: mod.verify_title(c, ex["title"]),
            )

            assert_correct(
                f"plot ex{n} verify_xlabel",
                lambda c: mod.verify_xlabel(c, ex["xlabel"]),
                f'plt.xlabel("{ex["xlabel"]}")',
            )
            assert_wrong(
                f"plot ex{n} verify_xlabel",
                lambda c: mod.verify_xlabel(c, ex["xlabel"]),
            )

            assert_correct(
                f"plot ex{n} verify_ylabel",
                lambda c: mod.verify_ylabel(c, ex["ylabel"]),
                f'plt.ylabel("{ex["ylabel"]}")',
            )
            assert_wrong(
                f"plot ex{n} verify_ylabel",
                lambda c: mod.verify_ylabel(c, ex["ylabel"]),
            )

            assert_correct(
                f"plot ex{n} verify_plot_simple (1)",
                lambda c: mod.verify_plot_simple(c, "x1", "y1"),
                "plt.plot(x1, y1)",
            )
            assert_wrong(
                f"plot ex{n} verify_plot_simple (1)",
                lambda c: mod.verify_plot_simple(c, "x1", "y1"),
            )
            assert_correct(
                f"plot ex{n} verify_plot_simple (2)",
                lambda c: mod.verify_plot_simple(c, "x2", "y2"),
                "plt.plot(x2, y2)",
            )
            assert_wrong(
                f"plot ex{n} verify_plot_simple (2)",
                lambda c: mod.verify_plot_simple(c, "x2", "y2"),
            )

        elif n == 3:
            for xvar, yvar in (("x1", "y1"), ("x2", "y2")):
                assert_correct(
                    f"plot ex{n} verify_x_array {xvar}",
                    lambda c, xv=xvar: mod.verify_x_array(c, xv, ex[xv]),
                    _np_int_array(xvar, ex[xvar]),
                )
                assert_wrong(
                    f"plot ex{n} verify_x_array {xvar}",
                    lambda c, xv=xvar: mod.verify_x_array(c, xv, ex[xv]),
                )
                assert_correct(
                    f"plot ex{n} verify_y_array {yvar}",
                    lambda c, yv=yvar: mod.verify_y_array(c, yv, ex[yv]),
                    _np_int_array(yvar, ex[yvar]),
                )
                assert_wrong(
                    f"plot ex{n} verify_y_array {yvar}",
                    lambda c, yv=yvar: mod.verify_y_array(c, yv, ex[yv]),
                )

            assert_correct(
                f"plot ex{n} verify_plot_simple (1)",
                lambda c: mod.verify_plot_simple(c, "x1", "y1"),
                "plt.plot(x1, y1)",
            )
            assert_wrong(
                f"plot ex{n} verify_plot_simple (1)",
                lambda c: mod.verify_plot_simple(c, "x1", "y1"),
            )
            assert_correct(
                f"plot ex{n} verify_plot_simple (2)",
                lambda c: mod.verify_plot_simple(c, "x2", "y2"),
                "plt.plot(x2, y2)",
            )
            assert_wrong(
                f"plot ex{n} verify_plot_simple (2)",
                lambda c: mod.verify_plot_simple(c, "x2", "y2"),
            )

            gc, gls, glw = ex["grid_color"], ex["grid_linestyle"], ex["grid_linewidth"]
            grid_code = (
                f"plt.grid(color='{gc}', linestyle='{gls}', linewidth={glw})"
            )
            assert_correct(
                f"plot ex{n} verify_grid",
                lambda c: mod.verify_grid(c, gc, gls, glw),
                grid_code,
            )
            assert_wrong(
                f"plot ex{n} verify_grid",
                lambda c: mod.verify_grid(c, gc, gls, glw),
            )

        assert_correct(f"plot ex{n} verify_step_show", verify_step_show, "plt.show()")
        assert_wrong(f"plot ex{n} verify_step_show", verify_step_show)


def main() -> int:
    random.seed(42)
    test_exercise_common()

    test_histogram_module(HistogramExercises())
    test_bar_module(BarPlotExercises())
    test_pie_module(PieChartExercises())
    test_scatter_module(ScatterPlotExercises())
    test_subplot_module(SubplotExercises())
    test_plot_module(PlotExercises())

    total = _pass + _fail
    print("=" * 70)
    print("QA Developer — B001 verify_* (18 exercises, correct + wrong per step)")
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

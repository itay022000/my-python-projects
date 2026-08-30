#!/usr/bin/env python3
"""
QA Developer — B002 validator & helper regression (no subprocess).

Tests session_common / validators helpers and PandasPractice validators / execution
with correct + wrong cases per function.

Run from project root: python3 scripts/qa_regression_b002.py
"""

from __future__ import annotations

import io
import os
import random
import re
import sys
from contextlib import redirect_stdout
from pathlib import Path

import numpy as np

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import env_quiet  # noqa: F401

import pandas as pd

import session_common
import validators
from exercises import exercise_1, exercise_2, exercise_3, exercise_4, exercise_5
import exercise_session as _exercise_session
from main import PandasPractice

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


def assert_ok(name: str, condition: bool, detail: str = "") -> None:
    record(name, condition, detail)


def assert_validator_ok(name: str, result: tuple[bool, str], expect_ok: bool) -> None:
    ok, msg = result
    if expect_ok:
        record(f"{name} [correct]", ok and bool(msg))
    else:
        record(f"{name} [wrong]", (not ok) and bool(msg), f"got ({ok!r}, {msg!r})")


def load_df() -> pd.DataFrame:
    app = PandasPractice()
    assert app.current_dataset is not None
    return app.current_dataset.copy()


def test_session_common() -> None:
    assert_ok(
        "normalize_code leading/trailing and parens",
        validators.normalize_code("  df.head( )  ") == "df.head()",
    )
    assert_ok(
        "normalize_code comparison spacing",
        validators.normalize_code("df[df['sales_rep'] == 'Alice']")
        == validators.normalize_code("df[df['sales_rep']=='Alice']"),
    )
    assert_ok(
        "normalize_code threshold spacing",
        validators.normalize_code("df[df['quantity'] > 42.50]")
        == validators.normalize_code("df[df['quantity']>42.50]"),
    )
    assert_ok(
        "normalize_code preserves string literal spaces",
        validators.normalize_code("df[df['name'] == 'John Doe']")
        == "df[df['name']=='John Doe']",
    )
    assert_ok(
        "codes_match equivalent",
        validators.codes_match("df.shape", "  df.shape  "),
    )
    assert_ok(
        "codes_match bracket spacing",
        validators.codes_match(
            "df[df['product']=='Keyboard']",
            "df[ df['product'] == 'Keyboard' ]",
        ),
    )
    assert_ok(
        "codes_match different",
        not validators.codes_match("df.shape", "df.columns"),
    )
    assert_ok(
        "classify_special_input skip",
        session_common.classify_special_input("skip") == "skip",
    )
    assert_ok(
        "classify_special_input exit",
        session_common.classify_special_input("exit") == "exit",
    )
    assert_ok(
        "classify_special_input quit",
        session_common.classify_special_input("Quit") == "exit",
    )
    assert_ok(
        "classify_special_input normal",
        session_common.classify_special_input("df.shape") is None,
    )

    buf = io.StringIO()
    with redirect_stdout(buf):
        session_common.print_skip_answer("df.head(10)")
    out = buf.getvalue()
    assert_ok("print_skip_answer message", "Skipping question." in out)
    assert_ok("print_skip_answer answer", "Correct answer: df.head(10)" in out)


def test_is_valid_pandas_code(app: PandasPractice) -> None:
    good_cases = [
        "df.head()",
        "df.shape",
        "pd.DataFrame()",
        "print(df)",
    ]
    for i, code in enumerate(good_cases):
        ok, err = app.is_valid_pandas_code(code)
        assert_ok(f"is_valid_pandas_code good[{i}]", ok and err is None, repr(err))

    bad_cases = [
        ("42", "number"),
        ('"hello"', "string"),
        ("True", "boolean"),
        ("none", "none"),
        ("not_pandas", "no df/pd"),
    ]
    for code, label in bad_cases:
        ok, err = app.is_valid_pandas_code(code)
        assert_ok(f"is_valid_pandas_code bad {label}", not ok and bool(err))


def test_execute_pandas_code(app: PandasPractice, df: pd.DataFrame) -> None:
    result, err = app.execute_pandas_code(df, "df.shape")
    assert_ok("execute_pandas_code expr correct", err is None and result == df.shape)

    result, err = app.execute_pandas_code(df, "df['not_a_real_column_xyz']")
    assert_ok("execute_pandas_code expr wrong", result is None and err is not None)

    result, err = app.execute_pandas_code(df, "df['quantity'] = 0")
    assert_ok(
        "execute_pandas_code assignment",
        result is None and err is None,
    )


def test_validate_head_result(app: PandasPractice, df: pd.DataFrame) -> None:
    n = 10
    good = df.head(n)
    assert_validator_ok(
        "validate_head_result",
        app.validate_head_result(good, df, n=n),
        True,
    )
    bad = df.tail(5)
    assert_validator_ok(
        "validate_head_result",
        app.validate_head_result(bad, df, n=n),
        False,
    )


def test_validate_shape_result(app: PandasPractice, df: pd.DataFrame) -> None:
    assert_validator_ok(
        "validate_shape_result",
        app.validate_shape_result(df.shape, df),
        True,
    )
    assert_validator_ok(
        "validate_shape_result",
        app.validate_shape_result((1, 1), df),
        False,
    )


def test_validate_columns_result(app: PandasPractice, df: pd.DataFrame) -> None:
    assert_validator_ok(
        "validate_columns_result",
        app.validate_columns_result(df.columns, df),
        True,
    )
    assert_validator_ok(
        "validate_columns_result",
        app.validate_columns_result(["only_one"], df),
        False,
    )


def test_validate_filter_result(app: PandasPractice, df: pd.DataFrame) -> None:
    subset = df.head(3)
    assert_validator_ok(
        "validate_filter_result",
        app.validate_filter_result(subset, df, lambda x: True),
        True,
    )
    assert_validator_ok(
        "validate_filter_result",
        app.validate_filter_result("not a frame", df, lambda x: True),
        False,
    )


def test_validate_filter_greater_than(app: PandasPractice, df: pd.DataFrame) -> None:
    random.seed(SEED)
    col = "quantity"
    threshold = float(df[col].median())
    good = df[df[col] > threshold]
    assert_validator_ok(
        "validate_filter_greater_than",
        app.validate_filter_greater_than(good, df, col, threshold),
        True,
    )
    bad = df[df[col] <= threshold]
    assert_validator_ok(
        "validate_filter_greater_than",
        app.validate_filter_greater_than(bad, df, col, threshold),
        False,
    )


def test_validate_groupby_sum(app: PandasPractice, df: pd.DataFrame) -> None:
    good = df.groupby("category")["quantity"].sum()
    assert_validator_ok(
        "validate_groupby_sum",
        app.validate_groupby_sum(good, df, "category", "quantity"),
        True,
    )
    bad = df.groupby("category")["unit_price"].mean()
    assert_validator_ok(
        "validate_groupby_sum",
        app.validate_groupby_sum(bad, df, "category", "quantity"),
        False,
    )


def test_validate_merge_result(app: PandasPractice, df: pd.DataFrame) -> None:
    df1 = df[["customer_id", "product"]].head(20).copy()
    df2 = df[["customer_id", "category"]].drop_duplicates().head(10).copy()
    on_col = "customer_id"
    good = pd.merge(df1, df2, on=on_col)
    assert_validator_ok(
        "validate_merge_result",
        app.validate_merge_result(good, df1, df2, on_col),
        True,
    )
    bad = pd.DataFrame({"wrong": [1, 2, 3]})
    assert_validator_ok(
        "validate_merge_result",
        app.validate_merge_result(bad, df1, df2, on_col),
        False,
    )


def test_validate_drop_duplicates(app: PandasPractice, df: pd.DataFrame) -> None:
    duped = pd.concat([df.head(5), df.head(3)], ignore_index=True)
    good = duped.drop_duplicates()
    assert_validator_ok(
        "validate_drop_duplicates",
        app.validate_drop_duplicates(good, duped),
        True,
    )
    assert_validator_ok(
        "validate_drop_duplicates",
        app.validate_drop_duplicates(duped, duped),
        False,
    )


def test_validate_handle_missing(app: PandasPractice, df: pd.DataFrame) -> None:
    missing = df.copy()
    missing.loc[0, "quantity"] = np.nan
    missing.loc[1, "quantity"] = np.nan

    dropped = missing.dropna(subset=["quantity"])
    assert_validator_ok(
        "validate_handle_missing drop",
        app.validate_handle_missing(dropped, missing, method="drop"),
        True,
    )
    assert_validator_ok(
        "validate_handle_missing drop wrong",
        app.validate_handle_missing(missing, missing, method="drop"),
        False,
    )

    filled = missing.fillna(0)
    assert_validator_ok(
        "validate_handle_missing fill",
        app.validate_handle_missing(filled, missing, method="fill", fill_value=0),
        True,
    )
    assert_validator_ok(
        "validate_handle_missing fill wrong",
        app.validate_handle_missing(missing, missing, method="fill", fill_value=0),
        False,
    )


_VAGUE_TITLE_PATTERNS = (
    r"specific columns from",
    r"Rename a column in the",
    r"Create a new column based on",
    r"Filter by a specific value",
    r"^Fill all missing values$",
    r"^Drop a column with missing values$",
)


def _capture_exercise_specs(ex_num: int, seed: int) -> list[dict[str, str]]:
    """Build specs as shown to learners (title + correct_answer per question)."""
    random.seed(seed)
    app = PandasPractice()
    captured: list[dict[str, str]] = []

    def _capture(app_, _frame, specs, *, before_question=None):
        for i in range(len(specs)):
            if before_question is not None:
                before_question(i, _frame)
            captured.append(
                {
                    "title": specs[i]["title"],
                    "correct_answer": specs[i]["correct_answer"],
                }
            )

    _exercise_session.run_question_session = _capture
    for mod in (exercise_1, exercise_2, exercise_3, exercise_4, exercise_5):
        mod.run_question_session = _capture

    runners = {
        1: app.exercise_1_basic_operations,
        2: app.exercise_2_filtering,
        3: app.exercise_3_sorting_and_selection,
        4: app.exercise_4_data_manipulation,
        5: app.exercise_5_data_cleaning,
    }
    runners[ex_num]()
    return captured


def _audit_question_copy(title: str, answer: str) -> list[str]:
    issues: list[str] = []
    for pattern in _VAGUE_TITLE_PATTERNS:
        if re.search(pattern, title):
            issues.append(f"vague:{pattern}")
    if re.sub(r"\s+", "", answer) == "df.drop(columns=[])":
        issues.append("placeholder_drop")
    skip_literals = {"int64", "float64", "all", "box", "bar", "scatter"}
    for literal in re.findall(r"'([^']+)'", answer):
        if literal in skip_literals:
            continue
        if literal and literal not in title:
            issues.append(f"missing:{literal!r}")
    return issues


def test_question_titles_complete() -> None:
    """Every question title must expose random params (500 seeds × 5 exercises)."""
    for ex_num in range(1, 6):
        for seed in range(500):
            specs = _capture_exercise_specs(ex_num, seed)
            assert_ok(
                f"ex{ex_num} seed{seed} question count",
                len(specs) == 8,
                f"got {len(specs)}",
            )
            for qnum, spec in enumerate(specs, 1):
                issues = _audit_question_copy(spec["title"], spec["correct_answer"])
                if issues:
                    detail = (
                        f"title={spec['title']!r} answer={spec['correct_answer']!r} "
                        f"issues={issues}"
                    )
                    assert_ok(f"ex{ex_num} q{qnum} seed{seed} copy", False, detail)
                    break


def main() -> int:
    os.chdir(_ROOT)

    random.seed(SEED)
    app = PandasPractice()
    df = load_df()

    print("=" * 70)
    print("QA Developer — B002 regression (validators & helpers)")
    print("=" * 70)

    test_session_common()
    test_is_valid_pandas_code(app)
    test_execute_pandas_code(app, df)
    test_validate_head_result(app, df)
    test_validate_shape_result(app, df)
    test_validate_columns_result(app, df)
    test_validate_filter_result(app, df)
    test_validate_filter_greater_than(app, df)
    test_validate_groupby_sum(app, df)
    test_validate_merge_result(app, df)
    test_validate_drop_duplicates(app, df)
    test_validate_handle_missing(app, df)
    test_question_titles_complete()

    total = _pass + _fail
    print(f"\nPassed: {_pass}/{total}")
    print(f"Failed: {_fail}/{total}")
    if _failures:
        print("\nFailures:")
        for line in _failures:
            print(f"  {line}")
    print("=" * 70)
    return 1 if _fail else 0


if __name__ == "__main__":
    sys.exit(main())

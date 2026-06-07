#!/usr/bin/env python3
"""
QA Developer — B002 validator & helper regression (no subprocess).

Tests practice_common helpers and PandasPractice validators / execution
with correct + wrong cases per function.

Run from project root: python3 scripts/qa_regression_b002.py
"""

from __future__ import annotations

import io
import os
import random
import sys
from contextlib import redirect_stdout
from pathlib import Path

import numpy as np
import pandas as pd

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import practice_common
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


def assert_validator_ok(
    name: str,
    result: tuple[bool, str],
    expect_ok: bool,
) -> None:
    ok, msg = result
    if expect_ok:
        record(f"{name} [correct]", ok and bool(msg))
    else:
        record(f"{name} [wrong]", (not ok) and bool(msg), f"got ({ok!r}, {msg!r})")


def load_df() -> pd.DataFrame:
    app = PandasPractice()
    assert app.current_dataset is not None
    return app.current_dataset.copy()


def test_practice_common() -> None:
    assert_ok(
        "normalize_code whitespace",
        practice_common.normalize_code("  df.head( )  ") == "df.head( )",
    )
    assert_ok(
        "codes_match equivalent",
        practice_common.codes_match("df.shape", "  df.shape  "),
    )
    assert_ok(
        "codes_match different",
        not practice_common.codes_match("df.shape", "df.columns"),
    )

    buf = io.StringIO()
    with redirect_stdout(buf):
        is_skip, is_exit, cont = practice_common.handle_special_commands(
            "skip", "df.head(10)", "hint"
        )
    out = buf.getvalue()
    assert_ok("handle_special_commands skip", is_skip and not is_exit and cont)
    assert_ok("handle_special_commands skip message", "Task skipped" in out)
    assert_ok("handle_special_commands skip answer", "CORRECT ANSWER" in out)

    is_skip, is_exit, cont = practice_common.handle_special_commands(
        "exit", "df.head(10)", "hint"
    )
    assert_ok("handle_special_commands exit", not is_skip and is_exit and not cont)

    is_skip, is_exit, cont = practice_common.handle_special_commands(
        "df.shape", "df.shape", "hint"
    )
    assert_ok("handle_special_commands normal", not is_skip and not is_exit and cont)


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


def main() -> int:
    os.chdir(_ROOT)

    random.seed(SEED)
    app = PandasPractice()
    df = load_df()

    print("=" * 70)
    print("QA Developer — B002 regression (validators & helpers)")
    print("=" * 70)

    test_practice_common()
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

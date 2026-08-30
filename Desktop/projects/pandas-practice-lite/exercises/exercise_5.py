"""Exercise 5: Data cleaning."""

import random

import numpy as np

from exercise_session import run_question_session
from hints import (
    HINT_E5_FFILL_HINT,
    HINT_E5_Q2,
    HINT_E5_Q3,
    HINT_E5_Q4,
    HINT_E5_Q5,
    HINT_E5_Q6,
    HINT_E5_Q7,
    HINT_E5_Q8,
    HINT_E5_Q9,
)


class Exercise5Mixin:
    """Mixin for PandasPractice."""

    def _introduce_missing_values(self, df, max_cells: int) -> None:
        num_missing = min(max_cells, len(df) * len(df.columns) // 10)
        for _ in range(num_missing):
            row_idx = random.randrange(len(df))
            col_idx = random.randrange(len(df.columns))
            df.iat[row_idx, col_idx] = np.nan

    def _fill_value_for_missing(self, df) -> int | float | str:
        cols_with_missing = df.columns[df.isnull().any()].tolist()
        if not cols_with_missing:
            return 0
        numeric_cols_with_missing = [
            col for col in cols_with_missing if df[col].dtype in ["int64", "float64"]
        ]
        string_cols_with_missing = [
            col for col in cols_with_missing if df[col].dtype == "object"
        ]
        if numeric_cols_with_missing:
            col_with_missing = random.choice(numeric_cols_with_missing)
            fill_options = [
                0,
                round(df[col_with_missing].mean(), 2),
                round(df[col_with_missing].median(), 2),
            ]
            return random.choice(fill_options)
        if string_cols_with_missing:
            return "Unknown"
        return 0

    def _append_fill_and_drop_questions(self, df, specs: list[dict]) -> None:
        """Add exercise 5 questions 3–5 with concrete titles (missing values on df)."""
        if df.isnull().sum().sum() == 0:
            self._introduce_missing_values(df, 5)
        _ffill_hint = HINT_E5_FFILL_HINT
        fill_value = self._fill_value_for_missing(df)
        specs.append(
            {
                "title": f"Fill all missing values with {fill_value}",
                "hint": HINT_E5_Q2,
                "correct_answer": f"df.fillna({fill_value})",
            }
        )

        cols_with_nulls = [col for col in df.columns if df[col].isnull().any()]
        if cols_with_nulls:
            col_to_ffill = random.choice(cols_with_nulls)
            specs.append(
                {
                    "title": (
                        f"Fill missing values in '{col_to_ffill}' column using forward fill"
                    ),
                    "hint": _ffill_hint,
                    "correct_answer": (
                        f"df['{col_to_ffill}'] = df['{col_to_ffill}'].ffill()"
                    ),
                }
            )
        else:
            specs.append(
                {
                    "title": "Fill missing values using forward fill",
                    "hint": _ffill_hint,
                    "correct_answer": "df.ffill()",
                }
            )

        if df.isnull().sum().sum() == 0:
            self._introduce_missing_values(df, 3)
        cols_with_nulls = [col for col in df.columns if df[col].isnull().any()]
        if not cols_with_nulls:
            self._introduce_missing_values(df, 3)
            cols_with_nulls = [col for col in df.columns if df[col].isnull().any()]
        col_to_drop = random.choice(cols_with_nulls)
        specs.append(
            {
                "title": f"Drop the '{col_to_drop}' column (it has missing values)",
                "hint": HINT_E5_Q3,
                "correct_answer": f"df.drop(columns=['{col_to_drop}'])",
            }
        )

    def exercise_5_data_cleaning(self):
        """Exercise: Data cleaning."""
        df = self.current_dataset.copy()
        specs: list[dict] = []

        task1_type = random.choice(["per_column", "total_count"])
        if task1_type == "per_column":
            specs.append(
                {
                    "title": "Find missing values per column",
                    "hint": HINT_E5_Q4,
                    "correct_answer": "df.isnull().sum()",
                    "check": self.make_isnull_per_column_checker(df),
                }
            )
        else:
            specs.append(
                {
                    "title": (
                        "Count the total number of missing values in the entire dataframe"
                    ),
                    "hint": HINT_E5_Q5,
                    "correct_answer": "df.isnull().sum().sum()",
                }
            )

        specs.append(
            {
                "title": "Remove duplicates",
                "hint": HINT_E5_Q6,
                "correct_answer": "df.drop_duplicates()",
            }
        )

        self._append_fill_and_drop_questions(df, specs)

        specs.append(
            {
                "title": "Remove rows where ALL columns have missing values",
                "hint": HINT_E5_Q7,
                "correct_answer": "df.dropna(how='all')",
            }
        )

        specs.append(
            {
                "title": "Calculate the correlation matrix for all numeric columns",
                "hint": HINT_E5_Q8,
                "correct_answer": "df.select_dtypes(include=['int64', 'float64']).corr()",
            }
        )

        specs.append(
            {
                "title": "Get information about the dataframe",
                "hint": HINT_E5_Q9,
                "correct_answer": "df.info()",
            }
        )

        run_question_session(self, df, specs)

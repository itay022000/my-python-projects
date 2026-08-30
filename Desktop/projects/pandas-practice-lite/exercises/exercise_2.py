"""Exercise 2: Filtering."""

import random

from exercise_session import run_question_session
from hints import (
    HINT_E2_FILTER_HINT,
    HINT_E2_Q2,
    HINT_E2_Q3,
    HINT_E2_Q4,
    HINT_E2_Q5,
)


class Exercise2Mixin:
    """Mixin for PandasPractice."""

    def exercise_2_filtering(self):
        """Exercise: Filtering data."""
        df = self.current_dataset
        specs: list[dict] = []

        numeric_col = self.get_random_numeric_column()
        if not numeric_col:
            return

        threshold = self.get_random_threshold(numeric_col)
        if threshold is None:
            threshold = df[numeric_col].median()

        _filter_hint = HINT_E2_FILTER_HINT

        specs.append(
            {
                "title": f"Filter rows where {numeric_col} > {threshold:.2f}",
                "hint": _filter_hint,
                "correct_answer": f"df[df['{numeric_col}'] > {threshold:.2f}]",
            }
        )

        categorical_col = self.get_random_categorical_column()
        category_values = df[categorical_col].dropna().unique()
        category_choice = random.choice(category_values)
        specs.append(
            {
                "title": (
                    f"Filter rows where {categorical_col} == '{category_choice}'"
                ),
                "hint": _filter_hint,
                "correct_answer": f"df[df['{categorical_col}'] == '{category_choice}']",
            }
        )

        numeric_col2 = self.get_random_numeric_column()
        if numeric_col2 == numeric_col:
            numeric_cols_all = self.get_numeric_columns()
            if len(numeric_cols_all) > 1:
                numeric_col2 = random.choice(
                    [c for c in numeric_cols_all if c != numeric_col]
                )
        threshold2 = self.get_random_threshold(numeric_col2)
        if threshold2 is None:
            threshold2 = df[numeric_col2].median()
        specs.append(
            {
                "title": f"Filter rows where {numeric_col2} < {threshold2:.2f}",
                "hint": _filter_hint,
                "correct_answer": f"df[df['{numeric_col2}'] < {threshold2:.2f}]",
            }
        )

        threshold3 = self.get_random_threshold(numeric_col)
        if threshold3 is None:
            threshold3 = df[numeric_col].median()
        specs.append(
            {
                "title": f"Filter rows where {numeric_col} >= {threshold3:.2f}",
                "hint": _filter_hint,
                "correct_answer": f"df[df['{numeric_col}'] >= {threshold3:.2f}]",
            }
        )

        numeric_col3 = self.get_random_numeric_column()
        if numeric_col3 == numeric_col:
            numeric_cols_all = self.get_numeric_columns()
            if len(numeric_cols_all) > 1:
                numeric_col3 = random.choice(
                    [c for c in numeric_cols_all if c != numeric_col]
                )
        threshold4 = self.get_random_threshold(numeric_col)
        threshold5 = self.get_random_threshold(numeric_col3)
        if threshold4 is None:
            threshold4 = df[numeric_col].quantile(0.5)
        if threshold5 is None:
            threshold5 = df[numeric_col3].quantile(0.5)
        specs.append(
            {
                "title": (
                    f"Filter rows where {numeric_col} > {threshold4:.2f} AND "
                    f"{numeric_col3} > {threshold5:.2f}"
                ),
                "hint": HINT_E2_Q2,
                "correct_answer": (
                    f"df[(df['{numeric_col}'] > {threshold4:.2f}) & "
                    f"(df['{numeric_col3}'] > {threshold5:.2f})]"
                ),
            }
        )

        if categorical_col:
            category_values_list = list(category_values[:5])
            if len(category_values_list) >= 2:
                selected_values = random.sample(
                    category_values_list, min(3, len(category_values_list))
                )
                specs.append(
                    {
                        "title": (
                            f"Filter rows where {categorical_col} is one of: "
                            f"{selected_values}"
                        ),
                        "hint": HINT_E2_Q3,
                        "correct_answer": (
                            f"df[df['{categorical_col}'].isin({selected_values})]"
                        ),
                    }
                )

        numeric_cols = self.get_numeric_columns()
        col1, col2 = random.sample(numeric_cols, 2)
        specs.append(
            {
                "title": f"Calculate the correlation between '{col1}' and '{col2}' columns",
                "hint": HINT_E2_Q4,
                "correct_answer": f"df['{col1}'].corr(df['{col2}'])",
            }
        )

        col = self.get_random_numeric_column()
        specs.append(
            {
                "title": f"Create a box plot of the '{col}' column",
                "hint": HINT_E2_Q5,
                "correct_answer": f"df['{col}'].plot(kind='box')",
                "include_plotting": True,
            }
        )

        run_question_session(self, df, specs)

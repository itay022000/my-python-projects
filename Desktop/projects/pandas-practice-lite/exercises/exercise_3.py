"""Exercise 3: Sorting and column selection."""

import random

from exercise_session import run_question_session
from hints import (
    HINT_E3_Q1,
    HINT_E3_Q2,
    HINT_E3_Q3,
    HINT_E3_Q4,
    HINT_E3_Q5,
    HINT_E3_Q6,
    HINT_E3_Q7,
    HINT_E3_Q8,
)


class Exercise3Mixin:
    """Mixin for PandasPractice."""

    def exercise_3_sorting_and_selection(self):
        """Exercise: Sorting and column selection."""
        df = self.current_dataset
        specs: list[dict] = []

        sort_col = self.get_random_numeric_column()
        if not sort_col:
            return
        ascending = random.choice([True, False])
        order_text = "ascending" if ascending else "descending"
        specs.append(
            {
                "title": f"Sort the dataframe by {sort_col} in {order_text} order",
                "hint": HINT_E3_Q1,
                "correct_answer": f"df.sort_values('{sort_col}', ascending={ascending})",
            }
        )

        all_cols = df.columns.tolist()
        num_cols_to_select = min(random.randint(2, 4), len(all_cols))
        expected_cols = random.sample(all_cols, num_cols_to_select)
        cols_str = "', '".join(expected_cols)
        specs.append(
            {
                "title": f"Select only these columns: {expected_cols}",
                "hint": HINT_E3_Q2,
                "correct_answer": f"df[['{cols_str}']]",
            }
        )

        single_col = self.get_random_column()
        specs.append(
            {
                "title": f"Select only the '{single_col}' column (as a Series)",
                "hint": HINT_E3_Q3,
                "correct_answer": f"df['{single_col}']",
            }
        )

        numeric_cols = self.get_numeric_columns()
        if len(numeric_cols) >= 2:
            sort_col1 = random.choice(numeric_cols)
            sort_col2 = random.choice([c for c in numeric_cols if c != sort_col1])
            specs.append(
                {
                    "title": (
                        f"Sort by '{sort_col1}' (ascending), then by "
                        f"'{sort_col2}' (descending)"
                    ),
                    "hint": HINT_E3_Q4,
                    "correct_answer": (
                        f"df.sort_values(by=['{sort_col1}', '{sort_col2}'], "
                        f"ascending=[True, False])"
                    ),
                }
            )

        n_rows_iloc = random.randint(3, 8)
        specs.append(
            {
                "title": f"Select the first {n_rows_iloc} rows using iloc",
                "hint": HINT_E3_Q5,
                "correct_answer": f"df.iloc[:{n_rows_iloc}]",
            }
        )

        n_rows_select = random.randint(3, 6)
        n_cols_select = random.randint(2, 4)
        specs.append(
            {
                "title": (
                    f"Select first {n_rows_select} rows and first {n_cols_select} "
                    f"columns using iloc"
                ),
                "hint": HINT_E3_Q6,
                "correct_answer": f"df.iloc[:{n_rows_select}, :{n_cols_select}]",
            }
        )

        numeric_cols_list = self.get_numeric_columns()
        if numeric_cols_list:
            specs.append(
                {
                    "title": "Select only numeric columns from the dataframe",
                    "hint": HINT_E3_Q7,
                    "correct_answer": "df.select_dtypes(include=['int64', 'float64'])",
                }
            )

        sort_col3 = self.get_random_numeric_column()
        if sort_col3:
            n_top = random.randint(3, 7)
            specs.append(
                {
                    "title": (
                        f"Get the top {n_top} rows when sorted by '{sort_col3}' "
                        f"in descending order"
                    ),
                    "hint": HINT_E3_Q8,
                    "correct_answer": (
                        f"df.sort_values('{sort_col3}', ascending=False).head({n_top})"
                    ),
                }
            )

        run_question_session(self, df, specs)

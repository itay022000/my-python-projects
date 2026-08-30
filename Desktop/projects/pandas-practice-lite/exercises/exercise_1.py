"""Exercise 1: Basic Operations."""

import random

from exercise_session import run_question_session
from hints import (
    HINT_E1_Q1,
    HINT_E1_Q2,
    HINT_E1_Q3,
    HINT_E1_Q4,
    HINT_E1_Q5,
    HINT_E1_Q6,
    HINT_E1_Q7,
    HINT_E1_Q8,
)


class Exercise1Mixin:
    """Mixin for PandasPractice."""

    def exercise_1_basic_operations(self):
        """Exercise: Basic pandas operations."""
        df = self.current_dataset
        n_rows = random.randint(5, 15)
        n_rows_tail = random.randint(5, 15)
        numeric_cols = self.get_numeric_columns()
        col1, col2 = random.sample(numeric_cols, 2)

        specs = [
            {
                "title": f"Display the first {n_rows} rows",
                "hint": HINT_E1_Q1,
                "correct_answer": f"df.head({n_rows})",
            },
            {
                "title": "Get the shape of the dataframe",
                "hint": HINT_E1_Q2,
                "correct_answer": "df.shape",
            },
            {
                "title": "Display column names",
                "hint": HINT_E1_Q3,
                "correct_answer": "df.columns",
            },
            {
                "title": "Display the data types of all columns",
                "hint": HINT_E1_Q4,
                "correct_answer": "df.dtypes",
            },
            {
                "title": f"Display the last {n_rows_tail} rows",
                "hint": HINT_E1_Q5,
                "correct_answer": f"df.tail({n_rows_tail})",
            },
            {
                "title": "Get a statistical summary of the dataframe",
                "hint": HINT_E1_Q6,
                "correct_answer": "df.describe()",
            },
            {
                "title": f"Calculate the correlation between '{col1}' and '{col2}' columns",
                "hint": HINT_E1_Q7,
                "correct_answer": f"df['{col1}'].corr(df['{col2}'])",
            },
            {
                "title": f"Create a scatter plot of '{col1}' vs '{col2}'",
                "hint": HINT_E1_Q8,
                "correct_answer": f"df.plot(x='{col1}', y='{col2}', kind='scatter')",
                "include_plotting": True,
            },
        ]
        run_question_session(self, df, specs)

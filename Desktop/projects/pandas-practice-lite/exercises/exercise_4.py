"""Exercise 4: Data manipulation."""

import random

from exercise_session import run_question_session
from hints import (
    HINT_E4_Q1,
    HINT_E4_Q2,
    HINT_E4_Q3,
    HINT_E4_Q4,
    HINT_E4_Q5,
    HINT_E4_Q6,
    HINT_E4_Q7,
    HINT_E4_Q8,
)


class Exercise4Mixin:
    """Mixin for PandasPractice."""

    def exercise_4_data_manipulation(self):
        """Exercise: Basic data manipulation."""
        df = self.current_dataset
        specs: list[dict] = []

        col_to_rename = self.get_random_column()
        if not col_to_rename:
            return
        new_name = f"{col_to_rename}_new"
        specs.append(
            {
                "title": f"Rename column '{col_to_rename}' to '{new_name}'",
                "hint": HINT_E4_Q1,
                "correct_answer": f"df.rename(columns={{'{col_to_rename}' : '{new_name}'}})",
            }
        )

        numeric_cols = self.get_numeric_columns()
        col1, col2 = random.sample(numeric_cols, 2)
        operation = random.choice(["divide", "multiply", "add", "subtract"])
        name_token = {
            "divide": "div",
            "multiply": "times",
            "add": "plus",
            "subtract": "minus",
        }[operation]
        new_col_name = f"{col1}_{name_token}_{col2}"
        if operation == "divide":
            correct = f"df['{new_col_name}'] = df['{col1}'] / df['{col2}']"
            title = (
                f"Create a new column named '{new_col_name}' by dividing "
                f"'{col1}' by '{col2}'"
            )
        elif operation == "multiply":
            correct = f"df['{new_col_name}'] = df['{col1}'] * df['{col2}']"
            title = (
                f"Create a new column named '{new_col_name}' by multiplying "
                f"'{col1}' and '{col2}'"
            )
        elif operation == "add":
            correct = f"df['{new_col_name}'] = df['{col1}'] + df['{col2}']"
            title = (
                f"Create a new column named '{new_col_name}' by adding "
                f"'{col1}' and '{col2}'"
            )
        else:
            correct = f"df['{new_col_name}'] = df['{col1}'] - df['{col2}']"
            title = (
                f"Create a new column named '{new_col_name}' by subtracting "
                f"'{col2}' from '{col1}'"
            )
        specs.append(
            {
                "title": title,
                "hint": HINT_E4_Q2,
                "correct_answer": correct,
            }
        )

        col_to_drop = self.get_random_column()
        if col_to_drop:
            specs.append(
                {
                    "title": f"Drop the '{col_to_drop}' column from the dataframe",
                    "hint": HINT_E4_Q3,
                    "correct_answer": f"df.drop(columns=['{col_to_drop}'])",
                }
            )

        numeric_col = self.get_random_numeric_column()
        if numeric_col:
            specs.append(
                {
                    "title": f"Convert the '{numeric_col}' column to integer type",
                    "hint": HINT_E4_Q4,
                    "correct_answer": f"df['{numeric_col}'] = df['{numeric_col}'].astype('int64')",
                }
            )

        all_cols_list = df.columns.tolist()
        if len(all_cols_list) >= 3:
            reordered_cols = random.sample(all_cols_list, min(4, len(all_cols_list)))
            random.shuffle(reordered_cols)
            specs.append(
                {
                    "title": f"Reorder columns to: {reordered_cols}",
                    "hint": HINT_E4_Q5,
                    "correct_answer": f"df[{reordered_cols}]",
                }
            )

        numeric_col2 = self.get_random_numeric_column()
        if numeric_col2:
            new_col_name_sq = f"{numeric_col2}_squared"
            specs.append(
                {
                    "title": (
                        f"Create a new column '{new_col_name_sq}' with squared values "
                        f"of '{numeric_col2}'"
                    ),
                    "hint": HINT_E4_Q6,
                    "correct_answer": f"df['{new_col_name_sq}'] = df['{numeric_col2}'] ** 2",
                }
            )

        target_col = self.get_random_numeric_column()
        specs.append(
            {
                "title": f"Get correlations of all numeric columns with '{target_col}'",
                "hint": HINT_E4_Q7,
                "correct_answer": (
                    f"df.select_dtypes(include=['int64', 'float64']).corr()['{target_col}']"
                ),
            }
        )

        col = self.get_random_categorical_column()
        specs.append(
            {
                "title": f"Create a bar plot of value counts for the '{col}' column",
                "hint": HINT_E4_Q8,
                "correct_answer": f"df['{col}'].value_counts().plot(kind='bar')",
                "include_plotting": True,
            }
        )

        run_question_session(self, df, specs)

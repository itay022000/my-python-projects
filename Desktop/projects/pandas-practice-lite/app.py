"""
Pandas Practice - application class (B003 module split, B011 learner UI).
"""

from pathlib import Path
from typing import Optional

import session_common
import validators
from dataset import DatasetMixin
from exercises.exercise_1 import Exercise1Mixin
from exercises.exercise_2 import Exercise2Mixin
from exercises.exercise_3 import Exercise3Mixin
from exercises.exercise_4 import Exercise4Mixin
from exercises.exercise_5 import Exercise5Mixin
from menus import MenusMixin


class PandasPractice(
    DatasetMixin,
    MenusMixin,
    Exercise1Mixin,
    Exercise2Mixin,
    Exercise3Mixin,
    Exercise4Mixin,
    Exercise5Mixin,
):
    """Main class for the pandas learning application."""

    def __init__(self):
        self.data_dir = Path(__file__).parent / "data"
        self.current_dataset = None
        self.current_dataset_name = None
        self.fail_fast_if_no_dataset()

    def make_exact_checker(self, df, correct_answer: str, include_plotting: bool = False):
        def check(code: str) -> tuple[bool, Optional[str]]:
            if not validators.codes_match(code, correct_answer):
                return False, None
            _, error = self.execute_pandas_code(
                df, code, include_plotting=include_plotting
            )
            if error:
                return False, f"Error: {error}"
            return True, None

        return check

    def make_isnull_per_column_checker(self, df):
        def check(code: str) -> tuple[bool, Optional[str]]:
            expected = df.isnull().sum()
            valid, msg = self.is_valid_pandas_code(code)
            if not valid:
                return False, msg
            result, error = self.execute_pandas_code(df, code)
            if error:
                return False, f"Error: {error}"
            try:
                if hasattr(result, "equals") and result.equals(expected):
                    return True, None
                if hasattr(result, "index") and hasattr(result, "values"):
                    if all(result.index == expected.index) and all(
                        result.values == expected.values
                    ):
                        return True, None
            except Exception:
                pass
            return False, "Result doesn't match expected missing value counts"

        return check

    def run_exercise(self, exercise_num: int) -> None:
        """Run a specific pandas exercise with teach intro (B011)."""
        exercises = {
            1: self.exercise_1_basic_operations,
            2: self.exercise_2_filtering,
            3: self.exercise_3_sorting_and_selection,
            4: self.exercise_4_data_manipulation,
            5: self.exercise_5_data_cleaning,
        }

        if exercise_num not in exercises:
            print(f"Exercise {exercise_num} not found!")
            return

        title, background, session_line = session_common.EXERCISE_INTROS[exercise_num]
        session_common.print_exercise_intro(title, background, session_line)
        exercises[exercise_num]()

    def is_valid_pandas_code(self, code):
        return validators.is_valid_pandas_code(code)

    def execute_pandas_code(
        self, df, code, expected_result=None, description="", include_plotting=False
    ):
        return validators.execute_pandas_code(
            df, code, expected_result, description, include_plotting
        )

    def validate_head_result(self, result, df, n=10):
        return validators.validate_head_result(result, df, n)

    def validate_shape_result(self, result, df):
        return validators.validate_shape_result(result, df)

    def validate_columns_result(self, result, df):
        return validators.validate_columns_result(result, df)

    def validate_filter_result(self, result, df, condition_check):
        return validators.validate_filter_result(result, df, condition_check)

    def validate_filter_greater_than(self, result, df, column, threshold):
        return validators.validate_filter_greater_than(result, df, column, threshold)

    def validate_groupby_sum(self, result, df, group_col, agg_col):
        return validators.validate_groupby_sum(result, df, group_col, agg_col)

    def validate_merge_result(self, result, df1, df2, on_col):
        return validators.validate_merge_result(result, df1, df2, on_col)

    def validate_drop_duplicates(self, result, df):
        return validators.validate_drop_duplicates(result, df)

    def validate_handle_missing(self, result, df, method="fill", fill_value=None):
        return validators.validate_handle_missing(result, df, method, fill_value)

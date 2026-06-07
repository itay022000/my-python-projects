"""
Pandas Practice - application class (B003 module split).
"""

from pathlib import Path

import practice_common
import validators
from dataset import DatasetMixin
from exercises.exercise_1 import Exercise1Mixin
from exercises.exercise_2 import Exercise2Mixin
from exercises.exercise_3 import Exercise3Mixin
from exercises.exercise_4 import Exercise4Mixin
from exercises.exercise_5 import Exercise5Mixin
from menus import MenusMixin
from progress import ProgressMixin


class PandasPractice(
    ProgressMixin,
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
        self.progress_file = Path(__file__).parent / "progress.json"
        self.progress = self.load_progress()
        self.current_dataset = None
        self.current_dataset_name = None
        self.load_dataset("sales_data.csv", verbose=False)

    def handle_special_commands(self, code, correct_answer, explanation):
        return practice_common.handle_special_commands(code, correct_answer, explanation)

    def run_exercise(self, exercise_num):
        """Run a specific pandas exercise."""
        exercises = {
            1: self.exercise_1_basic_operations,
            2: self.exercise_2_filtering,
            3: self.exercise_3_sorting_and_selection,
            4: self.exercise_4_data_manipulation,
            5: self.exercise_5_data_cleaning,
        }

        if exercise_num in exercises:
            print(f"\n{'='*60}")
            print(f"📝 EXERCISE {exercise_num}")
            print(f"{'='*60}")
            exercises[exercise_num]()
        else:
            print(f"❌ Exercise {exercise_num} not found!")

    def is_valid_pandas_code(self, code):
        return validators.is_valid_pandas_code(code)

    def execute_pandas_code(self, df, code, expected_result=None, description="", include_plotting=False):
        return validators.execute_pandas_code(df, code, expected_result, description, include_plotting)

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

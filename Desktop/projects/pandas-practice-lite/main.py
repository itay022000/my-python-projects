"""
Pandas Practice - Interactive Learning Tool
A hands-on project to learn pandas through practical exercises and data analysis.
"""

import pandas as pd
import numpy as np
import os
import json
from pathlib import Path
from datetime import datetime
import random
import sys
import tty
import termios

class PandasPractice:
    """
    Main class for the pandas learning application.
    """
    
    def __init__(self):
        self.data_dir = Path(__file__).parent / "data"
        self.progress_file = Path(__file__).parent / "progress.json"
        self.progress = self.load_progress()
        self.current_dataset = None
        self.current_dataset_name = None
        # Automatically load the only dataset
        self.load_dataset("sales_data.csv")
    
    def wait_for_esc(self):
        """Wait for ESC key press to return to menu."""
        print("\n" + "-"*60)
        print("Press ESC to return to menu...")
        
        # Save terminal settings
        if sys.stdin.isatty():
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                while True:
                    char = sys.stdin.read(1)
                    # ESC key is ASCII 27
                    if ord(char) == 27:
                        break
            finally:
                # Restore terminal settings
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        else:
            # Fallback if not in a terminal
            input("Press Enter to return to menu...")
        
    def load_progress(self):
        """Load user progress from file."""
        if self.progress_file.exists():
            with open(self.progress_file, 'r') as f:
                data = json.load(f)
                # Migrate old format to new format
                if "exercises_completed" in data and "exercise_stats" not in data:
                    data["exercise_stats"] = {}
                    for ex in data.get("exercises_completed", []):
                        data["exercise_stats"][ex] = {"count": 1, "total_grade": 100.0, "grades": [100.0]}
                    if "exercises_completed" in data:
                        del data["exercises_completed"]
                return data
        return {
            "exercise_stats": {},
            "last_session": None
        }
    
    def save_progress(self):
        """Save user progress to file."""
        self.progress["last_session"] = datetime.now().isoformat()
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f, indent=2)
    
    def load_dataset(self, filename):
        """Load a dataset from the data directory."""
        filepath = self.data_dir / filename
        if not filepath.exists():
            print(f"❌ Dataset '{filename}' not found!")
            return None
        
        try:
            df = pd.read_csv(filepath)
            self.current_dataset = df
            self.current_dataset_name = filename
            self.save_progress()
            print(f"✅ Loaded dataset: {filename}")
            print(f"   Shape: {df.shape[0]} rows × {df.shape[1]} columns")
            return df
        except Exception as e:
            print(f"❌ Error loading dataset: {e}")
            return None
    
    def get_numeric_columns(self, df=None):
        """Get numeric columns from dataframe."""
        if df is None:
            df = self.current_dataset
        if df is None:
            return []
        return df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    
    def get_categorical_columns(self, df=None):
        """Get categorical/object columns from dataframe."""
        if df is None:
            df = self.current_dataset
        if df is None:
            return []
        return df.select_dtypes(include=['object', 'string']).columns.tolist()
    
    def get_random_numeric_column(self, df=None):
        """Get a random numeric column."""
        cols = self.get_numeric_columns(df)
        return random.choice(cols) if cols else None
    
    def get_random_categorical_column(self, df=None):
        """Get a random categorical column."""
        cols = self.get_categorical_columns(df)
        return random.choice(cols) if cols else None
    
    def get_random_column(self, df=None):
        """Get a random column of any type."""
        if df is None:
            df = self.current_dataset
        if df is None:
            return None
        return random.choice(df.columns.tolist())
    
    def get_random_value_from_column(self, column, df=None):
        """Get a random value from a column."""
        if df is None:
            df = self.current_dataset
        if df is None or column not in df.columns:
            return None
        values = df[column].dropna().unique()
        return random.choice(values) if len(values) > 0 else None
    
    def get_random_threshold(self, column, df=None, percentile=50):
        """Get a random threshold value from a numeric column."""
        if df is None:
            df = self.current_dataset
        if df is None or column not in df.columns:
            return None
        if df[column].dtype not in ['int64', 'float64']:
            return None
        return df[column].quantile(percentile / 100.0)
    
    def check_dataset_loaded(self):
        """Check if a dataset is loaded, prompt to load one if not."""
        if self.current_dataset is None:
            print("\n❌ No dataset loaded!")
            print("💡 The dataset should be automatically loaded. Please restart the program.")
            return False
        return True
    
    def handle_special_commands(self, code, correct_answer, explanation):
        """
        Handle special commands 'skip' and 'exit'.
        Returns: (is_skip, is_exit, should_continue)
        """
        code_lower = code.lower().strip()
        
        if code_lower == 'skip':
            print("\n" + "="*60)
            print("⏭️  Task skipped")
            print("="*60)
            print("📖 CORRECT ANSWER:")
            print("="*60)
            print(correct_answer)
            if explanation:
                print(f"\n💡 Explanation: {explanation}")
            return True, False, True  # is_skip, is_exit, should_continue
        
        elif code_lower == 'exit':
            return False, True, False  # is_skip, is_exit, should_continue
        
        return False, False, True  # No special command
    
    def explore_dataset(self, df=None):
        """Interactive dataset exploration."""
        if df is None:
            df = self.current_dataset
        
        if df is None:
            print("❌ No dataset loaded! The dataset should be automatically loaded. Please restart the program.")
            return
        
        
        while True:
            print("\n" + "="*60)
            print("📊 DATASET EXPLORATION MENU")
            print("="*60)
            print("1. View first few rows (head)")
            print("2. View last few rows (tail)")
            print("3. View dataset info")
            print("4. View basic statistics")
            print("5. View column names and data types")
            print("6. Check for missing values")
            print("7. View unique values in a column")
            print("8. Filter data by condition")
            print("9. Sort data")
            print("10. Return to main menu")
            
            choice = input("\nSelect an option (1-10): ").strip()
            
            if choice == "1":
                rows = input("How many rows? (default 5): ").strip()
                n = int(rows) if rows.isdigit() else 5
                print(f"\n📋 First {n} rows:")
                print(f"Dataset: {self.current_dataset_name}")
                print(df.head(n))
                self.wait_for_esc()
                
            elif choice == "2":
                rows = input("How many rows? (default 5): ").strip()
                n = int(rows) if rows.isdigit() else 5
                print(f"\n📋 Last {n} rows:")
                print(f"Dataset: {self.current_dataset_name}")
                print(df.tail(n))
                self.wait_for_esc()
                
            elif choice == "3":
                print("\n📋 Dataset Info:")
                print(f"Dataset: {self.current_dataset_name}")
                print(df.info())
                self.wait_for_esc()
                
            elif choice == "4":
                print("\n📊 Basic Statistics:")
                print(f"Dataset: {self.current_dataset_name}")
                print(df.describe())
                self.wait_for_esc()
                
            elif choice == "5":
                print("\n📋 Columns and Data Types:")
                print(f"Dataset: {self.current_dataset_name}")
                print(df.dtypes)
                self.wait_for_esc()
                
            elif choice == "6":
                print("\n🔍 Missing Values:")
                print(f"Dataset: {self.current_dataset_name}")
                missing = df.isnull().sum()
                if missing.sum() == 0:
                    print("✅ No missing values!")
                else:
                    print(missing[missing > 0])
                self.wait_for_esc()
                    
            elif choice == "7":
                col = input("Enter column name: ").strip()
                if col in df.columns:
                    print(f"\n📋 Unique values in '{col}':")
                    print(f"Dataset: {self.current_dataset_name}")
                    print(df[col].unique())
                    print(f"\nCount: {df[col].nunique()} unique values")
                    self.wait_for_esc()
                else:
                    print(f"❌ Column '{col}' not found!")
                    self.wait_for_esc()
                    
            elif choice == "8":
                col = input("Enter column name to filter: ").strip()
                if col in df.columns:
                    print(f"\nSample values in '{col}': {df[col].unique()[:5]}")
                    value = input(f"Enter value to filter by: ").strip()
                    try:
                        # Try numeric comparison
                        if df[col].dtype in ['int64', 'float64']:
                            value = float(value)
                            filtered = df[df[col] == value]
                        else:
                            filtered = df[df[col] == value]
                        print(f"\n📊 Filtered results ({len(filtered)} rows):")
                        print(f"Dataset: {self.current_dataset_name}")
                        print(filtered)
                        self.wait_for_esc()
                    except:
                        print("❌ Error filtering data. Check your input.")
                        self.wait_for_esc()
                else:
                    print(f"❌ Column '{col}' not found!")
                    self.wait_for_esc()
                    
            elif choice == "9":
                col = input("Enter column to sort by: ").strip()
                if col in df.columns:
                    order = input("Sort ascending? (yes/no, default yes): ").strip().lower()
                    ascending = order != 'no'
                    sorted_df = df.sort_values(by=col, ascending=ascending)
                    print(f"\n📊 Sorted data:")
                    print(f"Dataset: {self.current_dataset_name}")
                    print(sorted_df)
                    self.wait_for_esc()
                else:
                    print(f"❌ Column '{col}' not found!")
                    self.wait_for_esc()
                    
            elif choice == "10":
                break
            else:
                print("❌ Invalid choice!")

    def record_exercise_completion(self, exercise_name, tasks_completed, total_tasks):
        """Record exercise completion with grade."""
        if exercise_name not in self.progress["exercise_stats"]:
            self.progress["exercise_stats"][exercise_name] = {
                "count": 0,
                "total_grade": 0.0,
                "grades": []
            }
        
        grade = (tasks_completed / total_tasks) * 100.0
        self.progress["exercise_stats"][exercise_name]["count"] += 1
        self.progress["exercise_stats"][exercise_name]["total_grade"] += grade
        self.progress["exercise_stats"][exercise_name]["grades"].append(grade)
        self.save_progress()
    
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
        """Check if the code is actually pandas code, not just a literal value."""
        code_stripped = code.strip()
        
        # Reject if it's just a number (integer or float)
        try:
            float(code_stripped)
            return False, "Please enter pandas code, not just a number"
        except ValueError:
            pass
        
        # Reject if it's just a string literal
        if (code_stripped.startswith('"') and code_stripped.endswith('"')) or \
           (code_stripped.startswith("'") and code_stripped.endswith("'")):
            return False, "Please enter pandas code, not just a string"
        
        # Reject if it's just a boolean
        if code_stripped.lower() in ['true', 'false']:
            return False, "Please enter pandas code, not just a boolean"
        
        # Reject if it's just None
        if code_stripped.lower() == 'none':
            return False, "Please enter pandas code, not just None"
        
        # Check if it contains pandas operations (df, pd, or common pandas methods)
        if 'df' not in code_stripped and 'pd' not in code_stripped:
            # Allow some exceptions like print(), but generally require df or pd
            if not any(keyword in code_stripped for keyword in ['print', 'len', 'type', 'isinstance']):
                return False, "Please enter pandas code that uses 'df' or 'pd'"
        
        return True, None
    
    def execute_pandas_code(self, df, code, expected_result=None, description="", include_plotting=False):
        """Execute pandas code and verify results."""
        try:
            # Create a safe execution environment
            safe_dict = {"df": df, "pd": pd}
            if include_plotting:
                import matplotlib.pyplot as plt
                import matplotlib
                matplotlib.use('Agg')  # Use non-interactive backend
                safe_dict["plt"] = plt
                safe_dict["matplotlib"] = matplotlib
            
            # Check if code is an assignment statement
            # Assignment statements have '=' that is not part of comparison operators (==, !=, <=, >=)
            code_stripped = code.strip()
            has_equals = '=' in code_stripped
            
            if has_equals:
                # Check if '=' is part of a comparison operator
                # Replace comparison operators with placeholders to check for standalone '='
                temp_code = code_stripped.replace('==', 'XX').replace('!=', 'XX').replace('<=', 'XX').replace('>=', 'XX')
                has_standalone_equals = '=' in temp_code
                # Check if it looks like an assignment (has df[...] = or df. = pattern)
                looks_like_assignment = has_standalone_equals and ('df[' in code_stripped or 'df.' in code_stripped)
                is_assignment = looks_like_assignment
            else:
                is_assignment = False
            
            if is_assignment:
                # Use exec() for assignment statements
                # Make a copy of df to avoid modifying the original dataset
                df_copy = df.copy()
                safe_dict_copy = {"df": df_copy, "pd": pd}
                if include_plotting:
                    safe_dict_copy["plt"] = safe_dict.get("plt")
                    safe_dict_copy["matplotlib"] = safe_dict.get("matplotlib")
                exec(code, {"__builtins__": {}}, safe_dict_copy)
                return None, None  # Assignments don't return a value
            else:
                # Use eval() for expressions
                result = eval(code, {"__builtins__": {}}, safe_dict)
                return result, None
        except Exception as e:
            return None, str(e)
    
    def validate_head_result(self, result, df, n=10):
        """Validate that result shows first n rows."""
        if not hasattr(result, 'shape'):
            return False, "Result is not a DataFrame"
        expected_rows = min(n, df.shape[0])
        if result.shape[0] != expected_rows:
            return False, f"Expected {expected_rows} rows, got {result.shape[0]}"
        # Check if first row matches exactly
        try:
            if not result.iloc[0].equals(df.iloc[0]):
                return False, "First row doesn't match - this might not be the head"
            # Check if last row matches the expected last row of head
            if result.shape[0] > 1:
                expected_last_idx = min(n - 1, df.shape[0] - 1)
                if not result.iloc[-1].equals(df.iloc[expected_last_idx]):
                    return False, "Rows don't match - this might not be the head"
            # Check all columns match
            if not all(result.columns == df.columns):
                return False, "Column names don't match"
        except Exception as e:
            return False, f"Error validating: {str(e)}"
        return True, "Correct! You displayed the first rows correctly."
    
    def validate_shape_result(self, result, df):
        """Validate that result is the shape tuple."""
        if result == df.shape:
            return True, "Correct!"
        return False, f"Expected {df.shape}, got {result}"
    
    def validate_columns_result(self, result, df):
        """Validate that result contains column names."""
        try:
            if hasattr(result, 'tolist'):
                result_list = result.tolist()
            elif hasattr(result, 'values'):
                result_list = list(result.values)
            elif isinstance(result, (list, tuple)):
                result_list = list(result)
            elif hasattr(result, '__iter__') and not isinstance(result, str):
                result_list = list(result)
            else:
                return False, "Result is not a list or array of column names"
            
            expected = list(df.columns)
            # Check if we have the same columns (order doesn't matter for correctness)
            if set(result_list) == set(expected) and len(result_list) == len(expected):
                return True, "Correct! You got all the column names."
            elif len(result_list) != len(expected):
                return False, f"Expected {len(expected)} columns, got {len(result_list)}"
            else:
                missing = set(expected) - set(result_list)
                extra = set(result_list) - set(expected)
                if missing:
                    return False, f"Missing columns: {missing}"
                if extra:
                    return False, f"Extra columns that don't exist: {extra}"
                return False, "Column names don't match"
        except Exception as e:
            return False, f"Error validating: {str(e)}"
    
    def validate_filter_result(self, result, df, condition_check):
        """Validate filtering result."""
        if not hasattr(result, 'shape'):
            return False, "Result is not a DataFrame"
        # Check if all rows in result satisfy the condition
        # This is a simplified check - we'll validate based on the task
        return True, "Result looks like filtered data"
    
    def validate_filter_greater_than(self, result, df, column, threshold):
        """Validate that filter result contains only rows where column > threshold."""
        if not hasattr(result, 'shape'):
            return False, "Result is not a DataFrame"
        if column not in result.columns:
            return False, f"Column '{column}' not found in result"
        
        # Calculate expected result
        expected = df[df[column] > threshold]
        expected_count = len(expected)
        
        if len(result) == 0:
            if expected_count == 0:
                return True, "Correct! No rows satisfy the condition."
            return False, f"Result is empty, but {expected_count} rows should satisfy the condition"
        
        # Check that all values in result are greater than threshold
        if not (result[column] > threshold).all():
            invalid_count = (result[column] <= threshold).sum()
            return False, f"{invalid_count} rows don't satisfy the condition (should be > {threshold})"
        
        # Check that we have the correct number of rows
        if len(result) != expected_count:
            return False, f"Expected {expected_count} rows, got {len(result)}. You might be missing some rows or have extra ones."
        
        # Verify the actual rows match (check by index)
        try:
            result_indices = set(result.index)
            expected_indices = set(expected.index)
            if result_indices != expected_indices:
                missing = expected_indices - result_indices
                extra = result_indices - expected_indices
                if missing:
                    return False, f"Missing {len(missing)} rows that should be included"
                if extra:
                    return False, f"Have {len(extra)} extra rows that shouldn't be included"
        except:
            # If index comparison fails, at least we checked the count and condition
            pass
        
        return True, f"Correct! All {len(result)} rows satisfy the condition."
    
    def validate_groupby_sum(self, result, df, group_col, agg_col):
        """Validate groupby sum result."""
        if not hasattr(result, '__iter__'):
            return False, "Result should be a Series or DataFrame"
        
        # Calculate expected result
        try:
            expected = df.groupby(group_col)[agg_col].sum()
        except Exception as e:
            return False, f"Error calculating expected result: {str(e)}"
        
        try:
            # Handle if result is a DataFrame instead of Series
            if hasattr(result, 'shape') and result.shape[1] > 1:
                # If it's a DataFrame, try to extract the right column
                if agg_col in result.columns:
                    result_series = result[agg_col]
                elif len(result.columns) == 1:
                    result_series = result.iloc[:, 0]
                else:
                    return False, "Result is a DataFrame with multiple columns - should be a Series or single column"
            elif hasattr(result, 'values'):
                result_series = result
            else:
                return False, "Result format not recognized"
            
            # Check length
            if len(result_series) != len(expected):
                return False, f"Expected {len(expected)} groups, got {len(result_series)}"
            
            # Check index matches
            if not all(result_series.index == expected.index):
                missing = set(expected.index) - set(result_series.index)
                extra = set(result_series.index) - set(expected.index)
                if missing:
                    return False, f"Missing groups: {missing}"
                if extra:
                    return False, f"Extra groups: {extra}"
                return False, "Group indices don't match"
            
            # Check values match (with small tolerance for floating point)
            if hasattr(result_series, 'values') and hasattr(expected, 'values'):
                differences = abs(result_series.values - expected.values)
                max_diff = differences.max()
                if max_diff > 0.01:
                    return False, f"Values don't match. Max difference: {max_diff:.4f}"
                
                # Use equals for exact match if possible
                if hasattr(result_series, 'equals'):
                    if result_series.equals(expected):
                        return True, "Correct! Groupby sum is accurate."
                
                return True, "Correct! Groupby sum is accurate."
            else:
                return False, "Could not compare values"
        except Exception as e:
            return False, f"Error validating: {str(e)}"
    
    def validate_merge_result(self, result, df1, df2, on_col):
        """Validate merge result."""
        if not hasattr(result, 'shape'):
            return False, "Result is not a DataFrame"
        if on_col not in result.columns:
            return False, f"Merge column '{on_col}' not found in result"
        
        # Check that we have columns from both dataframes
        df1_cols = set(df1.columns)
        df2_cols = set(df2.columns)
        result_cols = set(result.columns)
        
        # Should have at least the merge column plus columns from both
        if not (df1_cols.issubset(result_cols) or df2_cols.issubset(result_cols)):
            # Check if we have columns from both (accounting for possible suffix additions)
            df1_cols_in_result = df1_cols.intersection(result_cols)
            df2_cols_in_result = df2_cols.intersection(result_cols)
            if len(df1_cols_in_result) == 0 or len(df2_cols_in_result) == 0:
                return False, "Merged dataframe should have columns from both original dataframes"
        
        # Check that merge column values are valid (exist in at least one original)
        if on_col in df1.columns and on_col in df2.columns:
            # Values in result should exist in at least one of the originals
            result_values = set(result[on_col].unique())
            df1_values = set(df1[on_col].unique())
            df2_values = set(df2[on_col].unique())
            valid_values = df1_values.union(df2_values)
            invalid = result_values - valid_values
            if invalid:
                return False, f"Merge column contains values not in either original: {list(invalid)[:5]}"
        
        # Basic sanity check - merged should have reasonable number of rows
        # (not more than cartesian product, not less than either original for inner)
        max_possible = len(df1) * len(df2)
        if result.shape[0] > max_possible:
            return False, f"Result has {result.shape[0]} rows, which is more than possible"
        
        return True, "Correct! Merge was performed successfully."
    
    def validate_drop_duplicates(self, result, df):
        """Validate drop_duplicates result."""
        if not hasattr(result, 'shape'):
            return False, "Result is not a DataFrame"
        if result.shape[0] > df.shape[0]:
            return False, "Result has more rows than original - duplicates weren't removed"
        
        # Check if there are actually duplicates in original
        original_dupes = df.duplicated().sum()
        removed = df.shape[0] - result.shape[0]
        
        if removed > original_dupes:
            return False, f"Removed {removed} rows, but only {original_dupes} duplicates exist"
        
        # Verify that result actually has no duplicates
        result_dupes = result.duplicated().sum()
        if result_dupes > 0:
            return False, f"Result still has {result_dupes} duplicate rows"
        
        # Verify that all rows in result exist in original
        try:
            # Check if result is a subset of original (by checking if we can find matches)
            # This is a simplified check - in practice, we'd need to compare row by row
            if result.shape[1] != df.shape[1]:
                return False, "Column count doesn't match - result might be modified incorrectly"
            
            # Check that we didn't accidentally remove non-duplicate rows
            # Count unique rows in original
            original_unique = df.drop_duplicates()
            if result.shape[0] < original_unique.shape[0]:
                return False, f"Removed {original_unique.shape[0] - result.shape[0]} unique rows that shouldn't have been removed"
        except:
            pass
        
        return True, f"Correct! Removed {removed} duplicate row(s)."
    
    def validate_handle_missing(self, result, df, method='fill', fill_value=None):
        """Validate missing value handling."""
        if not hasattr(result, 'shape'):
            return False, "Result is not a DataFrame"
        
        missing_after = result.isnull().sum().sum()
        missing_before = df.isnull().sum().sum()
        
        if method == 'drop':
            if missing_after >= missing_before:
                return False, f"Missing values weren't removed (had {missing_before}, still have {missing_after})"
            # Check that rows were actually removed (not just filled)
            if result.shape[0] >= df.shape[0]:
                return False, "No rows were removed - did you use dropna()?"
            # Verify that remaining rows have no missing values in the columns that had them
            cols_with_missing = df.columns[df.isnull().any()].tolist()
            if cols_with_missing:
                remaining_missing = result[cols_with_missing].isnull().sum().sum()
                if remaining_missing > 0:
                    return False, f"Still have {remaining_missing} missing values in columns that had them"
            return True, f"Correct! Removed rows with missing values. ({missing_before - missing_after} missing values removed)"
        
        elif method == 'fill':
            if missing_after >= missing_before:
                return False, f"Missing values weren't filled (had {missing_before}, still have {missing_after})"
            # Check that shape is the same (fillna doesn't remove rows)
            if result.shape[0] != df.shape[0]:
                return False, "Row count changed - fillna() should keep all rows"
            # Verify that the correct fill value was used
            if fill_value is not None:
                cols_with_missing = df.columns[df.isnull().any()].tolist()
                for col in cols_with_missing:
                    if df[col].isnull().any():
                        # Check if the filled values match the expected fill_value
                        filled_indices = df[df[col].isnull()].index
                        if len(filled_indices) > 0:
                            filled_values = result.loc[filled_indices, col]
                            # Check if all filled values match the expected fill_value
                            if not (filled_values == fill_value).all():
                                return False, f"Fill value incorrect! Expected all missing values to be filled with {fill_value}"
                return True, f"Correct! Filled missing values with {fill_value}. ({missing_before - missing_after} values filled)"
            else:
                return True, f"Correct! Filled missing values. ({missing_before - missing_after} values filled)"
        
        return True, "Result looks good!"
    
    def exercise_1_basic_operations(self):
        """Exercise: Basic pandas operations."""
        print("\n🎯 GOAL: Practice basic pandas operations")
        
        if not self.check_dataset_loaded():
            return
        
        df = self.current_dataset
        n_rows = random.randint(5, 15)  # Random number of rows to display
        tasks_completed = 0
        total_tasks = 8  # 8 tasks: 6 basic, 1 correlation, 1 plotting
        
        print("\n" + "="*60)
        print(f"TASK 1: Display the first {n_rows} rows")
        print("="*60)
        print(f"💡 Dataset: {self.current_dataset_name}")
        print("💡 Hint: There's a method to show the top rows of a dataframe")
        print("\nEnter your pandas code below:")
        
        task1_completed = False
        attempts = 0
        max_attempts = 3
        correct_answer = f"df.head({n_rows})"
        explanation = "The head() method displays the first n rows of a dataframe"
        while attempts < max_attempts:
            attempts += 1
            code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
            
            # Handle special commands
            is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
            
            if is_exit:
                self.record_exercise_completion("exercise_1", tasks_completed, total_tasks)
                grade = (tasks_completed / total_tasks) * 100.0
                print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                return
            
            if is_skip:
                break
            
            if not should_continue:
                continue
            
            if not code:
                print("❌ Please enter some code")
                attempts -= 1  # Don't count empty input as attempt
                continue
            
            # Check if answer matches exactly (normalizing whitespace)
            code_normalized = ' '.join(code.strip().split())
            correct_normalized = ' '.join(correct_answer.strip().split())
            
            if code_normalized == correct_normalized:
                # Exact match - execute and accept
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error executing code: {error}")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
                print(f"\n✅ Correct!")
                task1_completed = True
                tasks_completed += 1
                break
            else:
                # Not exact match - reject
                print("❌ Incorrect answer. Please enter the exact code.")
                if attempts < max_attempts:
                    print("💡 Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(correct_answer)
                    print(f"\n💡 Explanation: {explanation}")
                    break
                continue
        
        print("\n" + "="*60)
        print("TASK 2: Get the shape of the dataframe")
        print("="*60)
        print("💡 Hint: DataFrames have an attribute that returns (rows, columns)")
        print("\nEnter your pandas code below:")
        
        task2_completed = False
        attempts = 0
        max_attempts = 3
        correct_answer = "df.shape"
        explanation = "The shape attribute returns a tuple (rows, columns)"
        while attempts < max_attempts:
            attempts += 1
            code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
            
            # Handle special commands
            is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
            
            if is_exit:
                self.record_exercise_completion("exercise_1", tasks_completed, total_tasks)
                grade = (tasks_completed / total_tasks) * 100.0
                print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                return
            
            if is_skip:
                break
            
            if not should_continue:
                continue
            
            if not code:
                print("❌ Please enter some code")
                attempts -= 1
                continue
            
            # Check if answer matches exactly (normalizing whitespace)
            code_normalized = ' '.join(code.strip().split())
            correct_normalized = ' '.join(correct_answer.strip().split())
            
            if code_normalized == correct_normalized:
                # Exact match - execute and accept
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error executing code: {error}")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
                print(f"\n✅ Correct!")
                task2_completed = True
                tasks_completed += 1
                break
            else:
                # Not exact match - reject
                print("❌ Incorrect answer. Please enter the exact code.")
                if attempts < max_attempts:
                    print("💡 Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(correct_answer)
                    print(f"\n💡 Explanation: {explanation}")
                    break
                continue
        
        # TASK 3: Display column names
        print("\n" + "="*60)
        print("TASK 3: Display column names")
        print("="*60)
        print(f"💡 Dataset: {self.current_dataset_name}")
        print("💡 Hint: DataFrames have an attribute that contains all column names")
        print("\nEnter your pandas code below:")
        
        task3_completed = False
        attempts = 0
        max_attempts = 3
        correct_answer = "df.columns"
        explanation = "The columns attribute returns an Index object with all column names"
        while attempts < max_attempts:
            attempts += 1
            code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
            
            # Handle special commands
            is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
            
            if is_exit:
                self.record_exercise_completion("exercise_1", tasks_completed, total_tasks)
                grade = (tasks_completed / total_tasks) * 100.0
                print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                return
            
            if is_skip:
                break
            
            if not should_continue:
                continue
            
            if not code:
                print("❌ Please enter some code")
                attempts -= 1
                continue
            
            # Check if answer matches exactly (normalizing whitespace)
            code_normalized = ' '.join(code.strip().split())
            correct_normalized = ' '.join(correct_answer.strip().split())
            
            if code_normalized == correct_normalized:
                # Exact match - execute and accept
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error executing code: {error}")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
                print(f"\n✅ Correct!")
                task3_completed = True
                tasks_completed += 1
                break
            else:
                # Not exact match - reject
                print("❌ Incorrect answer. Please enter the exact code.")
                if attempts < max_attempts:
                    print("💡 Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(correct_answer)
                    print(f"\n💡 Explanation: {explanation}")
                    break
                continue
        
        # TASK 4: Display data types
        print("\n" + "="*60)
        print("TASK 4: Display the data types of all columns")
        print("="*60)
        print(f"💡 Dataset: {self.current_dataset_name}")
        print("💡 Hint: DataFrames have an attribute that shows data types")
        print("\nEnter your pandas code below:")
        
        task4_completed = False
        attempts = 0
        max_attempts = 3
        correct_answer = "df.dtypes"
        explanation = "The dtypes attribute returns a Series with data types for each column"
        while attempts < max_attempts:
            attempts += 1
            code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
            
            # Handle special commands
            is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
            
            if is_exit:
                self.record_exercise_completion("exercise_1", tasks_completed, total_tasks)
                grade = (tasks_completed / total_tasks) * 100.0
                print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                return
            
            if is_skip:
                break
            
            if not should_continue:
                continue
            
            if not code:
                print("❌ Please enter some code")
                attempts -= 1
                continue
            
            # Check if answer matches exactly (normalizing whitespace)
            code_normalized = ' '.join(code.strip().split())
            correct_normalized = ' '.join(correct_answer.strip().split())
            
            if code_normalized == correct_normalized:
                # Exact match - execute and accept
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error executing code: {error}")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
                print(f"\n✅ Correct!")
                task4_completed = True
                tasks_completed += 1
                break
            else:
                # Not exact match - reject
                print("❌ Incorrect answer. Please enter the exact code.")
                if attempts < max_attempts:
                    print("💡 Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(correct_answer)
                    print(f"\n💡 Explanation: {explanation}")
                    break
                continue
        
        # TASK 5: Display last n rows
        n_rows_tail = random.randint(5, 15)
        print("\n" + "="*60)
        print(f"TASK 5: Display the last {n_rows_tail} rows")
        print("="*60)
        print(f"💡 Dataset: {self.current_dataset_name}")
        print("💡 Hint: There's a method to show the bottom rows of a dataframe")
        print("\nEnter your pandas code below:")
        
        task5_completed = False
        attempts = 0
        max_attempts = 3
        correct_answer = f"df.tail({n_rows_tail})"
        explanation = "The tail() method displays the last n rows of a dataframe"
        while attempts < max_attempts:
            attempts += 1
            code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
            
            # Handle special commands
            is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
            
            if is_exit:
                self.record_exercise_completion("exercise_1", tasks_completed, total_tasks)
                grade = (tasks_completed / total_tasks) * 100.0
                print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                return
            
            if is_skip:
                break
            
            if not should_continue:
                continue
            
            if not code:
                print("❌ Please enter some code")
                attempts -= 1
                continue
            
            # Check if answer matches exactly (normalizing whitespace)
            code_normalized = ' '.join(code.strip().split())
            correct_normalized = ' '.join(correct_answer.strip().split())
            
            if code_normalized == correct_normalized:
                # Exact match - execute and accept
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error executing code: {error}")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
                print(f"\n✅ Correct!")
                task5_completed = True
                tasks_completed += 1
                break
            else:
                # Not exact match - reject
                print("❌ Incorrect answer. Please enter the exact code.")
                if attempts < max_attempts:
                    print("💡 Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(correct_answer)
                    print(f"\n💡 Explanation: {explanation}")
                    break
                continue
        
        # TASK 6: Get statistical summary
        print("\n" + "="*60)
        print("TASK 6: Get a statistical summary of the dataframe")
        print("="*60)
        print(f"💡 Dataset: {self.current_dataset_name}")
        print("💡 Hint: There's a method that provides descriptive statistics")
        print("💡 This shows count, mean, std, min, max, etc. for numeric columns")
        print("\nEnter your pandas code below:")
        
        task6_completed = False
        attempts = 0
        max_attempts = 3
        correct_answer = "df.describe()"
        explanation = "The describe() method provides descriptive statistics"
        while attempts < max_attempts:
            attempts += 1
            code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
            
            # Handle special commands
            is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
            
            if is_exit:
                self.record_exercise_completion("exercise_1", tasks_completed, total_tasks)
                grade = (tasks_completed / total_tasks) * 100.0
                print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                return
            
            if is_skip:
                break
            
            if not should_continue:
                continue
            
            if not code:
                print("❌ Please enter some code")
                attempts -= 1
                continue
            
            # Check if answer matches exactly (normalizing whitespace)
            code_normalized = ' '.join(code.strip().split())
            correct_normalized = ' '.join(correct_answer.strip().split())
            
            if code_normalized == correct_normalized:
                # Exact match - execute and accept
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error executing code: {error}")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
                print(f"\n✅ Correct!")
                task6_completed = True
                tasks_completed += 1
                break
            else:
                # Not exact match - reject
                print("❌ Incorrect answer. Please enter the exact code.")
                if attempts < max_attempts:
                    print("💡 Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(correct_answer)
                    print(f"\n💡 Explanation: {explanation}")
                    break
                continue
        
        # TASK 7: Correlation - Correlation between two specific columns
        numeric_cols = self.get_numeric_columns()
        if len(numeric_cols) < 2:
            print("\n⚠️  Not enough numeric columns for correlation task. Skipping task 7.")
        else:
            col1, col2 = random.sample(numeric_cols, 2)
            print("\n" + "="*60)
            print(f"TASK 7: Calculate the correlation between '{col1}' and '{col2}' columns")
            print("="*60)
            print(f"💡 Dataset: {self.current_dataset_name}")
            print("💡 Hint: Think about how to measure the relationship between two numeric columns")
            print(f"💡 Find the correlation coefficient between '{col1}' and '{col2}'")
            print("\nEnter your pandas code below:")
            
            task7_completed = False
            attempts = 0
            max_attempts = 3
            correct_answer = f"df['{col1}'].corr(df['{col2}'])"
            explanation = "corr() method on a Series calculates correlation with another Series"
            while attempts < max_attempts:
                attempts += 1
                code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
                
                # Handle special commands
                is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
                
                if is_exit:
                    self.record_exercise_completion("exercise_1", tasks_completed, total_tasks)
                    grade = (tasks_completed / total_tasks) * 100.0
                    print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                    return
                
                if is_skip:
                    break
                
                if not should_continue:
                    continue
                
                if not code:
                    print("❌ Please enter some code")
                    attempts -= 1
                    continue
                
                # Check if answer matches exactly (normalizing whitespace)
                code_normalized = ' '.join(code.strip().split())
                correct_normalized = ' '.join(correct_answer.strip().split())
                
                if code_normalized == correct_normalized:
                    # Exact match - execute and accept
                    result, error = self.execute_pandas_code(df, code)
                    if error:
                        print(f"❌ Error executing code: {error}")
                        if attempts < max_attempts:
                            print("💡 Try again.")
                        else:
                            print("\n" + "="*60)
                            print("📖 CORRECT ANSWER:")
                            print("="*60)
                            print(correct_answer)
                            print(f"\n💡 Explanation: {explanation}")
                            break
                        continue
                    print(f"\n✅ Correct!")
                    task7_completed = True
                    tasks_completed += 1
                    break
                else:
                    # Not exact match - reject
                    print("❌ Incorrect answer. Please enter the exact code.")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
        
        # TASK 8: Plotting - Create a scatter plot
        numeric_cols = self.get_numeric_columns()
        if len(numeric_cols) < 2:
            print("\n⚠️  Not enough numeric columns for plotting task. Skipping task 8.")
        else:
            col1, col2 = random.sample(numeric_cols, 2)
            print("\n" + "="*60)
            print(f"TASK 8: Create a scatter plot of '{col1}' vs '{col2}'")
            print("="*60)
            print(f"💡 Dataset: {self.current_dataset_name}")
            print("💡 Hint: Think about how to visualize the relationship between two numeric columns")
            print(f"💡 Create a scatter plot with '{col1}' on x-axis and '{col2}' on y-axis")
            print("💡 Note: The plot will be created but not displayed (non-interactive mode)")
            print("\nEnter your pandas code below:")
            
            task8_completed = False
            attempts = 0
            max_attempts = 3
            correct_answer = f"df.plot(x='{col1}', y='{col2}', kind='scatter')"
            explanation = "plot() with kind='scatter' creates a scatter plot, or use matplotlib directly"
            while attempts < max_attempts:
                attempts += 1
                code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
                
                # Handle special commands
                is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
                
                if is_exit:
                    self.record_exercise_completion("exercise_1", tasks_completed, total_tasks)
                    grade = (tasks_completed / total_tasks) * 100.0
                    print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                    return
                
                if is_skip:
                    break
                
                if not should_continue:
                    continue
                
                if not code:
                    print("❌ Please enter some code")
                    attempts -= 1
                    continue
                
                # Check if answer matches exactly (normalizing whitespace)
                code_normalized = ' '.join(code.strip().split())
                correct_normalized = ' '.join(correct_answer.strip().split())
                
                if code_normalized == correct_normalized:
                    # Exact match - execute and accept
                    result, error = self.execute_pandas_code(df, code, include_plotting=True)
                    if error:
                        print(f"❌ Error executing code: {error}")
                        if attempts < max_attempts:
                            print("💡 Try again.")
                        else:
                            print("\n" + "="*60)
                            print("📖 CORRECT ANSWER:")
                            print("="*60)
                            print(correct_answer)
                            print(f"\n💡 Explanation: {explanation}")
                            break
                        continue
                    print(f"\n✅ Correct!")
                    task8_completed = True
                    tasks_completed += 1
                    break
                else:
                    # Not exact match - reject
                    print("❌ Incorrect answer. Please enter the exact code.")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
        
        # Record exercise completion
        self.record_exercise_completion("exercise_1", tasks_completed, total_tasks)
        grade = (tasks_completed / total_tasks) * 100.0
        print(f"\n✅ Exercise 1 Complete! Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
        input("\nPress Enter to continue...")
    
    def exercise_2_filtering(self):
        """Exercise: Filtering data."""
        print("\n🎯 GOAL: Learn to filter data using pandas")
        
        if not self.check_dataset_loaded():
            return
        
        df = self.current_dataset
        tasks_completed = 0
        total_tasks = 8  # 8 tasks: 6 filtering, 1 correlation, 1 plotting
        
        # Get random numeric column and threshold
        numeric_col = self.get_random_numeric_column()
        if not numeric_col:
            print("❌ No numeric columns found in this dataset!")
            return
        
        threshold = self.get_random_threshold(numeric_col)
        if threshold is None:
            threshold = df[numeric_col].median()
        
        print("\n" + "="*60)
        print(f"TASK 1: Filter rows where {numeric_col} > {threshold:.2f}")
        print("="*60)
        print(f"💡 Dataset: {self.current_dataset_name}")
        print("💡 Hint: Think about how to select rows based on a condition")
        print(f"💡 The condition should check if '{numeric_col}' column values are greater than {threshold:.2f}")
        print("\nEnter your pandas code below:")
        
        task1_completed = False
        attempts = 0
        max_attempts = 3
        correct_answer = f"df[df['{numeric_col}'] > {threshold:.2f}]"
        explanation = "Boolean indexing filters rows where the condition is True"
        while attempts < max_attempts:
            attempts += 1
            code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
            
            # Handle special commands
            is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
            
            if is_exit:
                self.record_exercise_completion("exercise_2", tasks_completed, total_tasks)
                grade = (tasks_completed / total_tasks) * 100.0
                print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                return
            
            if is_skip:
                break
            
            if not should_continue:
                continue
            
            if not code:
                print("❌ Please enter some code")
                attempts -= 1
                continue
            
            # Check if answer matches exactly (normalizing whitespace)
            code_normalized = ' '.join(code.strip().split())
            correct_normalized = ' '.join(correct_answer.strip().split())
            
            if code_normalized == correct_normalized:
                # Exact match - execute and accept
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error executing code: {error}")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
                print(f"\n✅ Correct!")
                task1_completed = True
                tasks_completed += 1
                break
            else:
                # Not exact match - reject
                print("❌ Incorrect answer. Please enter the exact code.")
                if attempts < max_attempts:
                    print("💡 Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(correct_answer)
                    print(f"\n💡 Explanation: {explanation}")
                    break
                continue
        
        # Get random categorical column and value
        categorical_col = self.get_random_categorical_column()
        if not categorical_col:
            print("\n⚠️  No categorical columns found. Skipping task 2.")
            self.record_exercise_completion("exercise_2", tasks_completed, total_tasks)
            grade = (tasks_completed / total_tasks) * 100.0
            print(f"\n✅ Exercise 2 Complete! Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
            input("\nPress Enter to continue...")
            return
        
        category_values = df[categorical_col].dropna().unique()
        if len(category_values) == 0:
            print("\n⚠️  No values found in categorical column. Skipping task 2.")
            self.record_exercise_completion("exercise_2", tasks_completed, total_tasks)
            grade = (tasks_completed / total_tasks) * 100.0
            print(f"\n✅ Exercise 2 Complete! Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
            input("\nPress Enter to continue...")
            return
        
        category_choice = random.choice(category_values)
        expected = df[df[categorical_col] == category_choice]
        expected_count = len(expected)
        
        print("\n" + "="*60)
        print(f"TASK 2: Filter by a specific value in '{categorical_col}' column")
        print("="*60)
        print(f"💡 Dataset: {self.current_dataset_name}")
        print(f"💡 Available values in '{categorical_col}': {list(category_values[:10])}{'...' if len(category_values) > 10 else ''}")
        print(f"💡 Filter for: '{category_choice}'")
        print("💡 Hint: Think about how to filter rows that match a specific value")
        print(f"\nEnter your pandas code to filter for '{categorical_col}' == '{category_choice}':")
        
        task2_completed = False
        attempts = 0
        max_attempts = 3
        correct_answer = f"df[df['{categorical_col}'] == '{category_choice}']"
        explanation = "Use boolean indexing with == to filter for exact matches"
        while attempts < max_attempts:
            attempts += 1
            code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
            
            # Handle special commands
            is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
            
            if is_exit:
                self.record_exercise_completion("exercise_2", tasks_completed, total_tasks)
                grade = (tasks_completed / total_tasks) * 100.0
                print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                return
            
            if is_skip:
                break
            
            if not should_continue:
                continue
            
            if not code:
                print("❌ Please enter some code")
                attempts -= 1
                continue
            
            # Check if answer matches exactly (normalizing whitespace)
            code_normalized = ' '.join(code.strip().split())
            correct_normalized = ' '.join(correct_answer.strip().split())
            
            if code_normalized == correct_normalized:
                # Exact match - execute and accept
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error executing code: {error}")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
                print(f"\n✅ Correct!")
                task2_completed = True
                tasks_completed += 1
                break
            else:
                # Not exact match - reject
                print("❌ Incorrect answer. Please enter the exact code.")
                if attempts < max_attempts:
                    print("💡 Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(correct_answer)
                    print(f"\n💡 Explanation: {explanation}")
                    break
                continue
        
        # TASK 3: Filter with less than
        numeric_col2 = self.get_random_numeric_column()
        if numeric_col2 == numeric_col:
            numeric_cols_all = self.get_numeric_columns()
            if len(numeric_cols_all) > 1:
                numeric_col2 = random.choice([c for c in numeric_cols_all if c != numeric_col])
            else:
                numeric_col2 = numeric_col
        
        threshold2 = self.get_random_threshold(numeric_col2)
        if threshold2 is None:
            threshold2 = df[numeric_col2].median()
        
        print("\n" + "="*60)
        print(f"TASK 3: Filter rows where {numeric_col2} < {threshold2:.2f}")
        print("="*60)
        print(f"💡 Dataset: {self.current_dataset_name}")
        print("💡 Hint: Think about how to filter rows where values are less than a threshold")
        print(f"💡 Filter where '{numeric_col2}' is less than {threshold2:.2f}")
        print("\nEnter your pandas code below:")
        
        task3_completed = False
        attempts = 0
        max_attempts = 3
        correct_answer = f"df[df['{numeric_col2}'] < {threshold2:.2f}]"
        explanation = "Use < for less than comparison"
        while attempts < max_attempts:
            attempts += 1
            code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
            
            # Handle special commands
            is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
            
            if is_exit:
                self.record_exercise_completion("exercise_2", tasks_completed, total_tasks)
                grade = (tasks_completed / total_tasks) * 100.0
                print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                return
            
            if is_skip:
                break
            
            if not should_continue:
                continue
            
            if not code:
                print("❌ Please enter some code")
                attempts -= 1
                continue
            
            # Check if answer matches exactly (normalizing whitespace)
            code_normalized = ' '.join(code.strip().split())
            correct_normalized = ' '.join(correct_answer.strip().split())
            
            if code_normalized == correct_normalized:
                # Exact match - execute and accept
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error executing code: {error}")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
                print(f"\n✅ Correct!")
                task3_completed = True
                tasks_completed += 1
                break
            else:
                # Not exact match - reject
                print("❌ Incorrect answer. Please enter the exact code.")
                if attempts < max_attempts:
                    print("💡 Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(correct_answer)
                    print(f"\n💡 Explanation: {explanation}")
                    break
                continue
        
        # TASK 4: Filter with >= (greater than or equal)
        threshold3 = self.get_random_threshold(numeric_col)
        if threshold3 is None:
            threshold3 = df[numeric_col].quantile(0.25)
        
        print("\n" + "="*60)
        print(f"TASK 4: Filter rows where {numeric_col} >= {threshold3:.2f}")
        print("="*60)
        print(f"💡 Dataset: {self.current_dataset_name}")
        print("💡 Hint: Think about how to filter rows where values meet or exceed a threshold")
        print(f"💡 Filter where '{numeric_col}' is greater than or equal to {threshold3:.2f}")
        print("\nEnter your pandas code below:")
        
        task4_completed = False
        attempts = 0
        max_attempts = 3
        correct_answer = f"df[df['{numeric_col}'] >= {threshold3:.2f}]"
        explanation = "Use >= for greater than or equal comparison"
        while attempts < max_attempts:
            attempts += 1
            code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
            
            # Handle special commands
            is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
            
            if is_exit:
                self.record_exercise_completion("exercise_2", tasks_completed, total_tasks)
                grade = (tasks_completed / total_tasks) * 100.0
                print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                return
            
            if is_skip:
                break
            
            if not should_continue:
                continue
            
            if not code:
                print("❌ Please enter some code")
                attempts -= 1
                continue
            
            # Check if answer matches exactly (normalizing whitespace)
            code_normalized = ' '.join(code.strip().split())
            correct_normalized = ' '.join(correct_answer.strip().split())
            
            if code_normalized == correct_normalized:
                # Exact match - execute and accept
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error executing code: {error}")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
                print(f"\n✅ Correct!")
                task4_completed = True
                tasks_completed += 1
                break
            else:
                # Not exact match - reject
                print("❌ Incorrect answer. Please enter the exact code.")
                if attempts < max_attempts:
                    print("💡 Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(correct_answer)
                    print(f"\n💡 Explanation: {explanation}")
                    break
                continue
        
        # TASK 5: Filter with multiple conditions (AND)
        numeric_col3 = self.get_random_numeric_column()
        if numeric_col3 == numeric_col:
            numeric_cols_all = self.get_numeric_columns()
            if len(numeric_cols_all) > 1:
                numeric_col3 = random.choice([c for c in numeric_cols_all if c != numeric_col])
            else:
                numeric_col3 = numeric_col
        
        threshold4 = self.get_random_threshold(numeric_col)
        threshold5 = self.get_random_threshold(numeric_col3)
        if threshold4 is None:
            threshold4 = df[numeric_col].quantile(0.5)
        if threshold5 is None:
            threshold5 = df[numeric_col3].quantile(0.5)
        
        print("\n" + "="*60)
        print(f"TASK 5: Filter rows where {numeric_col} > {threshold4:.2f} AND {numeric_col3} > {threshold5:.2f}")
        print("="*60)
        print(f"💡 Dataset: {self.current_dataset_name}")
        print("💡 Hint: Think about how to combine multiple filtering conditions")
        print(f"💡 Filter where both '{numeric_col}' > {threshold4:.2f} AND '{numeric_col3}' > {threshold5:.2f}")
        print("\nEnter your pandas code below:")
        
        task5_completed = False
        attempts = 0
        max_attempts = 3
        correct_answer = f"df[(df['{numeric_col}'] > {threshold4:.2f}) & (df['{numeric_col3}'] > {threshold5:.2f})]"
        explanation = "Use & for AND, each condition must be in parentheses"
        while attempts < max_attempts:
            attempts += 1
            code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
            
            # Handle special commands
            is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
            
            if is_exit:
                self.record_exercise_completion("exercise_2", tasks_completed, total_tasks)
                grade = (tasks_completed / total_tasks) * 100.0
                print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                return
            
            if is_skip:
                break
            
            if not should_continue:
                continue
            
            if not code:
                print("❌ Please enter some code")
                attempts -= 1
                continue
            
            # Check if answer matches exactly (normalizing whitespace)
            code_normalized = ' '.join(code.strip().split())
            correct_normalized = ' '.join(correct_answer.strip().split())
            
            if code_normalized == correct_normalized:
                # Exact match - execute and accept
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error executing code: {error}")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
                print(f"\n✅ Correct!")
                task5_completed = True
                tasks_completed += 1
                break
            else:
                # Not exact match - reject
                print("❌ Incorrect answer. Please enter the exact code.")
                if attempts < max_attempts:
                    print("💡 Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(correct_answer)
                    print(f"\n💡 Explanation: {explanation}")
                    break
                continue
        
        # TASK 6: Filter with isin() for multiple values
        if categorical_col:
            category_values_list = list(category_values[:5])  # Take up to 5 values
            if len(category_values_list) >= 2:
                selected_values = random.sample(category_values_list, min(3, len(category_values_list)))
                print("\n" + "="*60)
                print(f"TASK 6: Filter rows where {categorical_col} is one of: {selected_values}")
                print("="*60)
                print(f"💡 Dataset: {self.current_dataset_name}")
                print("💡 Hint: Think about how to check if a value is in a list of options")
                print(f"💡 Filter where '{categorical_col}' is in {selected_values}")
                print("\nEnter your pandas code below:")
                
                task6_completed = False
                attempts = 0
                max_attempts = 3
                correct_answer = f"df[df['{categorical_col}'].isin({selected_values})]"
                explanation = "isin() checks if values are in a list"
                while attempts < max_attempts:
                    attempts += 1
                    code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
                    
                    # Handle special commands
                    is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
                    
                    if is_exit:
                        self.record_exercise_completion("exercise_2", tasks_completed, total_tasks)
                        grade = (tasks_completed / total_tasks) * 100.0
                        print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                        return
                    
                    if is_skip:
                        break
                    
                    if not should_continue:
                        continue
                    
                    if not code:
                        print("❌ Please enter some code")
                        attempts -= 1
                        continue
                    
                    # Check if answer matches exactly (normalizing whitespace)
                    code_normalized = ' '.join(code.strip().split())
                    correct_normalized = ' '.join(correct_answer.strip().split())
                    
                    if code_normalized == correct_normalized:
                        # Exact match - execute and accept
                        result, error = self.execute_pandas_code(df, code)
                        if error:
                            print(f"❌ Error executing code: {error}")
                            if attempts < max_attempts:
                                print("💡 Try again.")
                            else:
                                print("\n" + "="*60)
                                print("📖 CORRECT ANSWER:")
                                print("="*60)
                                print(correct_answer)
                                print(f"\n💡 Explanation: {explanation}")
                                break
                            continue
                        print(f"\n✅ Correct!")
                        task6_completed = True
                        tasks_completed += 1
                        break
                    else:
                        # Not exact match - reject
                        print("❌ Incorrect answer. Please enter the exact code.")
                        if attempts < max_attempts:
                            print("💡 Try again.")
                        else:
                            print("\n" + "="*60)
                            print("📖 CORRECT ANSWER:")
                            print("="*60)
                            print(correct_answer)
                            print(f"\n💡 Explanation: {explanation}")
                            break
                        continue
        
        # TASK 7: Correlation - Correlation between two numeric columns
        numeric_cols = self.get_numeric_columns()
        if len(numeric_cols) < 2:
            print("\n⚠️  Not enough numeric columns for correlation task. Skipping task 5.")
        else:
            col1, col2 = random.sample(numeric_cols, 2)
            print("\n" + "="*60)
            print(f"TASK 7: Calculate the correlation between '{col1}' and '{col2}' columns")
            print("="*60)
            print(f"💡 Dataset: {self.current_dataset_name}")
            print("💡 Hint: Think about how to measure the relationship between two numeric columns")
            print(f"💡 Find the correlation coefficient between '{col1}' and '{col2}'")
            print("\nEnter your pandas code below:")
            
            task5_completed = False
            attempts = 0
            max_attempts = 3
            correct_answer = f"df['{col1}'].corr(df['{col2}'])"
            explanation = "corr() method on a Series calculates correlation with another Series"
            while attempts < max_attempts:
                attempts += 1
                code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
                
                # Handle special commands
                is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
                
                if is_exit:
                    self.record_exercise_completion("exercise_2", tasks_completed, total_tasks)
                    grade = (tasks_completed / total_tasks) * 100.0
                    print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                    return
                
                if is_skip:
                    break
                
                if not should_continue:
                    continue
                
                if not code:
                    print("❌ Please enter some code")
                    attempts -= 1
                    continue
                
                # Check if answer matches exactly (normalizing whitespace)
                code_normalized = ' '.join(code.strip().split())
                correct_normalized = ' '.join(correct_answer.strip().split())
                
                if code_normalized == correct_normalized:
                    # Exact match - execute and accept
                    result, error = self.execute_pandas_code(df, code)
                    if error:
                        print(f"❌ Error executing code: {error}")
                        if attempts < max_attempts:
                            print("💡 Try again.")
                        else:
                            print("\n" + "="*60)
                            print("📖 CORRECT ANSWER:")
                            print("="*60)
                            print(correct_answer)
                            print(f"\n💡 Explanation: {explanation}")
                            break
                        continue
                    print(f"\n✅ Correct!")
                    task5_completed = True
                    tasks_completed += 1
                    break
                else:
                    # Not exact match - reject
                    print("❌ Incorrect answer. Please enter the exact code.")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
        
        # TASK 8: Plotting - Create a box plot
        numeric_cols = self.get_numeric_columns()
        if len(numeric_cols) < 1:
            print("\n⚠️  No numeric columns for plotting task. Skipping task 8.")
        else:
            col = random.choice(numeric_cols)
            print("\n" + "="*60)
            print(f"TASK 8: Create a box plot of the '{col}' column")
            print("="*60)
            print(f"💡 Dataset: {self.current_dataset_name}")
            print("💡 Hint: Think about how to visualize the distribution and outliers of a numeric column")
            print(f"💡 Create a box plot showing the distribution of '{col}'")
            print("💡 Note: The plot will be created but not displayed (non-interactive mode)")
            print("\nEnter your pandas code below:")
            
            task6_completed = False
            attempts = 0
            max_attempts = 3
            correct_answer = f"df['{col}'].plot(kind='box')"
            explanation = "plot() with kind='box' creates a box plot, or use matplotlib directly"
            while attempts < max_attempts:
                attempts += 1
                code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
                
                # Handle special commands
                is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
                
                if is_exit:
                    self.record_exercise_completion("exercise_2", tasks_completed, total_tasks)
                    grade = (tasks_completed / total_tasks) * 100.0
                    print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                    return
                
                if is_skip:
                    break
                
                if not should_continue:
                    continue
                
                if not code:
                    print("❌ Please enter some code")
                    attempts -= 1
                    continue
                
                # Check if answer matches exactly (normalizing whitespace)
                code_normalized = ' '.join(code.strip().split())
                correct_normalized = ' '.join(correct_answer.strip().split())
                
                if code_normalized == correct_normalized:
                    # Exact match - execute and accept
                    result, error = self.execute_pandas_code(df, code, include_plotting=True)
                    if error:
                        print(f"❌ Error executing code: {error}")
                        if attempts < max_attempts:
                            print("💡 Try again.")
                        else:
                            print("\n" + "="*60)
                            print("📖 CORRECT ANSWER:")
                            print("="*60)
                            print(correct_answer)
                            print(f"\n💡 Explanation: {explanation}")
                            break
                        continue
                    print(f"\n✅ Correct!")
                    task6_completed = True
                    tasks_completed += 1
                    break
                else:
                    # Not exact match - reject
                    print("❌ Incorrect answer. Please enter the exact code.")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
                    break
            
        # Exercise 2 complete - record completion
        self.record_exercise_completion("exercise_2", tasks_completed, total_tasks)
        grade = (tasks_completed / total_tasks) * 100.0
        print(f"\n✅ Exercise 2 Complete! Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
        input("\nPress Enter to continue...")
    
    def exercise_3_sorting_and_selection(self):
        """Exercise: Sorting and selecting columns."""
        print("\n🎯 GOAL: Learn to sort data and select specific columns")
        
        if not self.check_dataset_loaded():
            return
        
        df = self.current_dataset
        tasks_completed = 0
        total_tasks = 8  # 8 tasks: 6 core, 1 correlation, 1 plotting
        
        # Get random numeric column for sorting
        sort_col = self.get_random_numeric_column()
        if not sort_col:
            print("❌ No numeric columns found in this dataset!")
            return
        
        ascending = random.choice([True, False])
        order_text = "ascending" if ascending else "descending"
        
        print("\n" + "="*60)
        print(f"TASK 1: Sort the dataframe by {sort_col} in {order_text} order")
        print("="*60)
        print(f"💡 Dataset: {self.current_dataset_name}")
        print("💡 Hint: Think about how to arrange rows in a specific order")
        print(f"💡 You'll need to specify the column '{sort_col}' and order (ascending={ascending})")
        print("\nEnter your pandas code below:")
        
        task1_completed = False
        attempts = 0
        max_attempts = 3
        correct_answer = f"df.sort_values('{sort_col}', ascending={ascending})"
        explanation = f"sort_values() sorts by a column, ascending={ascending} for {order_text}"
        while attempts < max_attempts:
            attempts += 1
            code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
            
            # Handle special commands
            is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
            
            if is_exit:
                self.record_exercise_completion("exercise_3", tasks_completed, total_tasks)
                grade = (tasks_completed / total_tasks) * 100.0
                print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                return
            
            if is_skip:
                break
            
            if not should_continue:
                continue
            
            if not code:
                print("❌ Please enter some code")
                attempts -= 1
                continue
            
            # Check if answer matches exactly (normalizing whitespace)
            code_normalized = ' '.join(code.strip().split())
            correct_normalized = ' '.join(correct_answer.strip().split())
            
            if code_normalized == correct_normalized:
                # Exact match - execute and accept
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error executing code: {error}")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
                print(f"\n✅ Correct!")
                task1_completed = True
                tasks_completed += 1
                break
            else:
                # Not exact match - reject
                print("❌ Incorrect answer. Please enter the exact code.")
                if attempts < max_attempts:
                    print("💡 Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(correct_answer)
                    print(f"\n💡 Explanation: {explanation}")
                    break
                continue
        
        # Select random columns for task 2
        all_cols = df.columns.tolist()
        if len(all_cols) < 2:
            print("\n⚠️  Not enough columns for column selection task. Skipping.")
            self.record_exercise_completion("exercise_3", tasks_completed, total_tasks)
            grade = (tasks_completed / total_tasks) * 100.0
            print(f"\n✅ Exercise 3 Complete! Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
            input("\nPress Enter to continue...")
            return
        
        num_cols_to_select = min(random.randint(2, 4), len(all_cols))
        expected_cols = random.sample(all_cols, num_cols_to_select)
        
        print("\n" + "="*60)
        print("TASK 2: Select only specific columns from the dataframe")
        print("="*60)
        print(f"💡 Dataset: {self.current_dataset_name}")
        print("💡 Hint: Think about how to choose specific columns from a dataframe")
        print(f"💡 Select only these columns: {expected_cols}")
        print("\nEnter your pandas code below:")
        
        task2_completed = False
        attempts = 0
        max_attempts = 3
        cols_str = "', '".join(expected_cols)
        correct_answer = f"df[['{cols_str}']]"
        explanation = "Use double brackets to select multiple columns"
        while attempts < max_attempts:
            attempts += 1
            code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
            
            # Handle special commands
            is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
            
            if is_exit:
                self.record_exercise_completion("exercise_3", tasks_completed, total_tasks)
                grade = (tasks_completed / total_tasks) * 100.0
                print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                return
            
            if is_skip:
                break
            
            if not should_continue:
                continue
            
            if not code:
                print("❌ Please enter some code")
                attempts -= 1
                continue
            
            # Check if answer matches exactly (normalizing whitespace)
            code_normalized = ' '.join(code.strip().split())
            correct_normalized = ' '.join(correct_answer.strip().split())
            
            if code_normalized == correct_normalized:
                # Exact match - execute and accept
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error executing code: {error}")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
                print(f"\n✅ Correct!")
                task2_completed = True
                tasks_completed += 1
                break
            else:
                # Not exact match - reject
                print("❌ Incorrect answer. Please enter the exact code.")
                if attempts < max_attempts:
                    print("💡 Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(correct_answer)
                    print(f"\n💡 Explanation: {explanation}")
                    break
                continue
        
        # TASK 3: Select a single column (as Series)
        single_col = self.get_random_column()
        print("\n" + "="*60)
        print(f"TASK 3: Select only the '{single_col}' column (as a Series)")
        print("="*60)
        print(f"💡 Dataset: {self.current_dataset_name}")
        print("💡 Hint: Think about how to extract a single column from a dataframe")
        print(f"💡 Select the '{single_col}' column")
        print("\nEnter your pandas code below:")
        
        task3_completed = False
        attempts = 0
        max_attempts = 3
        correct_answer = f"df['{single_col}']"
        explanation = "Single brackets return a Series for one column"
        while attempts < max_attempts:
            attempts += 1
            code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
            
            # Handle special commands
            is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
            
            if is_exit:
                self.record_exercise_completion("exercise_3", tasks_completed, total_tasks)
                grade = (tasks_completed / total_tasks) * 100.0
                print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                return
            
            if is_skip:
                break
            
            if not should_continue:
                continue
            
            if not code:
                print("❌ Please enter some code")
                attempts -= 1
                continue
            
            # Check if answer matches exactly (normalizing whitespace)
            code_normalized = ' '.join(code.strip().split())
            correct_normalized = ' '.join(correct_answer.strip().split())
            
            if code_normalized == correct_normalized:
                # Exact match - execute and accept
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error executing code: {error}")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
                print(f"\n✅ Correct!")
                task3_completed = True
                tasks_completed += 1
                break
            else:
                # Not exact match - reject
                print("❌ Incorrect answer. Please enter the exact code.")
                if attempts < max_attempts:
                    print("💡 Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(correct_answer)
                    print(f"\n💡 Explanation: {explanation}")
                    break
                continue
        
        # TASK 4: Sort by multiple columns
        numeric_cols = self.get_numeric_columns()
        if len(numeric_cols) >= 2:
            sort_col1 = random.choice(numeric_cols)
            sort_col2 = random.choice([c for c in numeric_cols if c != sort_col1])
            print("\n" + "="*60)
            print(f"TASK 4: Sort by '{sort_col1}' (ascending), then by '{sort_col2}' (descending)")
            print("="*60)
            print(f"💡 Dataset: {self.current_dataset_name}")
            print("💡 Hint: Think about how to sort by multiple columns with different orders")
            print(f"💡 Sort first by '{sort_col1}' ascending, then by '{sort_col2}' descending")
            print("\nEnter your pandas code below:")
            
            task4_completed = False
            attempts = 0
            max_attempts = 3
            correct_answer = f"df.sort_values(by=['{sort_col1}', '{sort_col2}'], ascending=[True, False])"
            explanation = "Pass a list of columns and a list of boolean values for ascending"
            while attempts < max_attempts:
                attempts += 1
                code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
                
                # Handle special commands
                is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
                
                if is_exit:
                    self.record_exercise_completion("exercise_3", tasks_completed, total_tasks)
                    grade = (tasks_completed / total_tasks) * 100.0
                    print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                    return
                
                if is_skip:
                    break
                
                if not should_continue:
                    continue
                
                if not code:
                    print("❌ Please enter some code")
                    attempts -= 1
                    continue
                
                # Check if answer matches exactly (normalizing whitespace)
                code_normalized = ' '.join(code.strip().split())
                correct_normalized = ' '.join(correct_answer.strip().split())
                
                if code_normalized == correct_normalized:
                    # Exact match - execute and accept
                    result, error = self.execute_pandas_code(df, code)
                    if error:
                        print(f"❌ Error executing code: {error}")
                        if attempts < max_attempts:
                            print("💡 Try again.")
                        else:
                            print("\n" + "="*60)
                            print("📖 CORRECT ANSWER:")
                            print("="*60)
                            print(correct_answer)
                            print(f"\n💡 Explanation: {explanation}")
                            break
                        continue
                    print(f"\n✅ Correct!")
                    task4_completed = True
                    tasks_completed += 1
                    break
                else:
                    # Not exact match - reject
                    print("❌ Incorrect answer. Please enter the exact code.")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
                
                print(f"\n❌ Data is not sorted correctly by both columns")
                if attempts < max_attempts:
                    print(f"💡 Sort by [{sort_col1}, {sort_col2}] with ascending=[True, False]")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df.sort_values(by=['{sort_col1}', '{sort_col2}'], ascending=[True, False])")
                    print("\n💡 Explanation: Pass a list of columns and a list of boolean values for ascending")
                    break
        
        # TASK 5: Select rows using iloc
        n_rows_iloc = random.randint(3, 8)
        print("\n" + "="*60)
        print(f"TASK 5: Select the first {n_rows_iloc} rows using iloc")
        print("="*60)
        print(f"💡 Dataset: {self.current_dataset_name}")
        print("💡 Hint: Think about how to select rows by their position (not by label)")
        print(f"💡 Select rows 0 to {n_rows_iloc-1} (first {n_rows_iloc} rows)")
        print("\nEnter your pandas code below:")
        
        task5_completed = False
        attempts = 0
        max_attempts = 3
        correct_answer = f"df.iloc[:{n_rows_iloc}]"
        explanation = "iloc uses integer positions, [:n] selects first n rows"
        while attempts < max_attempts:
            attempts += 1
            code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
            
            # Handle special commands
            is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
            
            if is_exit:
                self.record_exercise_completion("exercise_3", tasks_completed, total_tasks)
                grade = (tasks_completed / total_tasks) * 100.0
                print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                return
            
            if is_skip:
                break
            
            if not should_continue:
                continue
            
            if not code:
                print("❌ Please enter some code")
                attempts -= 1
                continue
            
            # Check if answer matches exactly (normalizing whitespace)
            code_normalized = ' '.join(code.strip().split())
            correct_normalized = ' '.join(correct_answer.strip().split())
            
            if code_normalized == correct_normalized:
                # Exact match - execute and accept
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error executing code: {error}")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
                print(f"\n✅ Correct!")
                task5_completed = True
                tasks_completed += 1
                break
            else:
                # Not exact match - reject
                print("❌ Incorrect answer. Please enter the exact code.")
                if attempts < max_attempts:
                    print("💡 Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(correct_answer)
                    print(f"\n💡 Explanation: {explanation}")
                    break
                continue
        
        # TASK 6: Select specific rows and columns using iloc
        n_rows_select = min(5, df.shape[0])
        n_cols_select = min(3, df.shape[1])
        print("\n" + "="*60)
        print(f"TASK 6: Select first {n_rows_select} rows and first {n_cols_select} columns using iloc")
        print("="*60)
        print(f"💡 Dataset: {self.current_dataset_name}")
        print("💡 Hint: Think about how to select both specific rows and columns by position")
        print(f"💡 Select rows 0 to {n_rows_select-1} and columns 0 to {n_cols_select-1}")
        print("\nEnter your pandas code below:")
        
        task6_completed = False
        attempts = 0
        max_attempts = 3
        correct_answer = f"df.iloc[:{n_rows_select}, :{n_cols_select}]"
        explanation = "iloc[rows, columns] selects both rows and columns by position"
        while attempts < max_attempts:
            attempts += 1
            code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
            
            # Handle special commands
            is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
            
            if is_exit:
                self.record_exercise_completion("exercise_3", tasks_completed, total_tasks)
                grade = (tasks_completed / total_tasks) * 100.0
                print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                return
            
            if is_skip:
                break
            
            if not should_continue:
                continue
            
            if not code:
                print("❌ Please enter some code")
                attempts -= 1
                continue
            
            # Check if answer matches exactly (normalizing whitespace)
            code_normalized = ' '.join(code.strip().split())
            correct_normalized = ' '.join(correct_answer.strip().split())
            
            if code_normalized == correct_normalized:
                # Exact match - execute and accept
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error executing code: {error}")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
                print(f"\n✅ Correct!")
                task6_completed = True
                tasks_completed += 1
                break
            else:
                # Not exact match - reject
                print("❌ Incorrect answer. Please enter the exact code.")
                if attempts < max_attempts:
                    print("💡 Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(correct_answer)
                    print(f"\n💡 Explanation: {explanation}")
                    break
                continue
        
        # TASK 7: Select columns by data type
        numeric_cols_list = self.get_numeric_columns()
        if numeric_cols_list:
            print("\n" + "="*60)
            print("TASK 7: Select only numeric columns from the dataframe")
            print("="*60)
            print(f"💡 Dataset: {self.current_dataset_name}")
            print("💡 Hint: Think about how to filter columns based on their data type")
            print("💡 Select columns with numeric data types (int64, float64)")
            print("\nEnter your pandas code below:")
            
            task7_completed = False
            attempts = 0
            max_attempts = 3
            correct_answer = "df.select_dtypes(include=['int64', 'float64'])"
            explanation = "select_dtypes() filters columns by data type"
            while attempts < max_attempts:
                attempts += 1
                code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
                
                # Handle special commands
                is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
                
                if is_exit:
                    self.record_exercise_completion("exercise_3", tasks_completed, total_tasks)
                    grade = (tasks_completed / total_tasks) * 100.0
                    print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                    return
                
                if is_skip:
                    break
                
                if not should_continue:
                    continue
                
                if not code:
                    print("❌ Please enter some code")
                    attempts -= 1
                    continue
                
                # Check if answer matches exactly (normalizing whitespace)
                code_normalized = ' '.join(code.strip().split())
                correct_normalized = ' '.join(correct_answer.strip().split())
                
                if code_normalized == correct_normalized:
                    # Exact match - execute and accept
                    result, error = self.execute_pandas_code(df, code)
                    if error:
                        print(f"❌ Error executing code: {error}")
                        if attempts < max_attempts:
                            print("💡 Try again.")
                        else:
                            print("\n" + "="*60)
                            print("📖 CORRECT ANSWER:")
                            print("="*60)
                            print(correct_answer)
                            print(f"\n💡 Explanation: {explanation}")
                            break
                        continue
                    print(f"\n✅ Correct!")
                    task7_completed = True
                    tasks_completed += 1
                    break
                else:
                    # Not exact match - reject
                    print("❌ Incorrect answer. Please enter the exact code.")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
                    print("\n💡 Explanation: select_dtypes() filters columns by data type")
                    break
        
        # TASK 8: Get top N rows after sorting
        sort_col3 = self.get_random_numeric_column()
        if sort_col3:
            n_top = random.randint(3, 7)
            print("\n" + "="*60)
            print(f"TASK 8: Get the top {n_top} rows when sorted by '{sort_col3}' in descending order")
            print("="*60)
            print(f"💡 Dataset: {self.current_dataset_name}")
            print("💡 Hint: Think about how to combine sorting with selecting a subset of rows")
            print(f"💡 Sort by '{sort_col3}' descending, then get top {n_top} rows")
            print("\nEnter your pandas code below:")
            
            task8_completed = False
            attempts = 0
            max_attempts = 3
            correct_answer = f"df.sort_values('{sort_col3}', ascending=False).head({n_top})"
            explanation = "Chain sort_values() and head() methods"
            while attempts < max_attempts:
                attempts += 1
                code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
                
                # Handle special commands
                is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
                
                if is_exit:
                    self.record_exercise_completion("exercise_3", tasks_completed, total_tasks)
                    grade = (tasks_completed / total_tasks) * 100.0
                    print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                    return
                
                if is_skip:
                    break
                
                if not should_continue:
                    continue
                
                if not code:
                    print("❌ Please enter some code")
                    attempts -= 1
                    continue
                
                # Check if answer matches exactly (normalizing whitespace)
                code_normalized = ' '.join(code.strip().split())
                correct_normalized = ' '.join(correct_answer.strip().split())
                
                if code_normalized == correct_normalized:
                    # Exact match - execute and accept
                    result, error = self.execute_pandas_code(df, code)
                    if error:
                        print(f"❌ Error executing code: {error}")
                        if attempts < max_attempts:
                            print("💡 Try again.")
                        else:
                            print("\n" + "="*60)
                            print("📖 CORRECT ANSWER:")
                            print("="*60)
                            print(correct_answer)
                            print(f"\n💡 Explanation: {explanation}")
                            break
                        continue
                    print(f"\n✅ Correct!")
                    task8_completed = True
                    tasks_completed += 1
                    break
                else:
                    # Not exact match - reject
                    print("❌ Incorrect answer. Please enter the exact code.")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df.sort_values('{sort_col3}', ascending=False).head({n_top})")
                    print("\n💡 Explanation: Chain sort_values() and head() methods")
                    break
        
        # Record exercise completion
        self.record_exercise_completion("exercise_3", tasks_completed, total_tasks)
        grade = (tasks_completed / total_tasks) * 100.0
        print(f"\n✅ Exercise 3 Complete! Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
        input("\nPress Enter to continue...")
    
    def exercise_4_data_manipulation(self):
        """Exercise: Basic data manipulation."""
        print("\n🎯 GOAL: Learn to manipulate data in dataframes")
        
        if not self.check_dataset_loaded():
            return
        
        df = self.current_dataset
        tasks_completed = 0
        total_tasks = 8  # 8 tasks: 6 core, 1 correlation, 1 plotting
        
        # Get random column to rename
        col_to_rename = self.get_random_column()
        if not col_to_rename:
            print("❌ No columns found in this dataset!")
            return
        
        new_name = f"{col_to_rename}_new"
        
        print("\n" + "="*60)
        print("TASK 1: Rename a column in the dataframe")
        print("="*60)
        print(f"💡 Dataset: {self.current_dataset_name}")
        print("💡 Hint: Think about how to change a column's name")
        print(f"💡 Rename the '{col_to_rename}' column to '{new_name}'")
        print("\nEnter your pandas code below:")
        
        task1_completed = False
        attempts = 0
        max_attempts = 3
        correct_answer = f"df.rename(columns={{'{col_to_rename}' : '{new_name}'}})"
        explanation = "rename() with columns parameter renames specific columns"
        while attempts < max_attempts:
            attempts += 1
            code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
            
            # Handle special commands
            is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
            
            if is_exit:
                self.record_exercise_completion("exercise_4", tasks_completed, total_tasks)
                grade = (tasks_completed / total_tasks) * 100.0
                print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                return
            
            if is_skip:
                break
            
            if not should_continue:
                continue
            
            if not code:
                print("❌ Please enter some code")
                attempts -= 1
                continue
            
            # Check if answer matches exactly (normalizing whitespace)
            code_normalized = ' '.join(code.strip().split())
            correct_normalized = ' '.join(correct_answer.strip().split())
            
            if code_normalized == correct_normalized:
                # Exact match - execute and accept
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error executing code: {error}")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
                print(f"\n✅ Correct!")
                task1_completed = True
                tasks_completed += 1
                break
            else:
                # Not exact match - reject
                print("❌ Incorrect answer. Please enter the exact code.")
                if attempts < max_attempts:
                    print("💡 Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(correct_answer)
                    print(f"\n💡 Explanation: {explanation}")
                    break
                continue
        
        # Get two numeric columns for calculation
        numeric_cols = self.get_numeric_columns()
        if len(numeric_cols) < 2:
            print("\n⚠️  Not enough numeric columns for calculation task. Skipping.")
            self.record_exercise_completion("exercise_4", tasks_completed, total_tasks)
            grade = (tasks_completed / total_tasks) * 100.0
            print(f"\n✅ Exercise 4 Complete! Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
            input("\nPress Enter to continue...")
            return
        
        col1, col2 = random.sample(numeric_cols, 2)
        new_col_name = f"{col1}_per_{col2}"
        operation = random.choice(['divide', 'multiply', 'add', 'subtract'])
        op_symbol = {'divide': '/', 'multiply': '*', 'add': '+', 'subtract': '-'}[operation]
        op_text = {'divide': 'dividing', 'multiply': 'multiplying', 'add': 'adding', 'subtract': 'subtracting'}[operation]
        
        print("\n" + "="*60)
        print("TASK 2: Create a new column based on existing columns")
        print("="*60)
        print(f"💡 Dataset: {self.current_dataset_name}")
        print("💡 Hint: Think about how to add a new column with calculated values")
        print(f"💡 Create a new column '{new_col_name}' by {op_text} '{col1}' {op_symbol} '{col2}'")
        print("\nEnter your pandas code below:")
        
        task2_completed = False
        attempts = 0
        max_attempts = 3
        # Determine correct answer based on operation
        if operation == 'divide':
            correct_answer = f"df['{new_col_name}'] = df['{col1}'] / df['{col2}']"
        elif operation == 'multiply':
            correct_answer = f"df['{new_col_name}'] = df['{col1}'] * df['{col2}']"
        elif operation == 'add':
            correct_answer = f"df['{new_col_name}'] = df['{col1}'] + df['{col2}']"
        else:  # subtract
            correct_answer = f"df['{new_col_name}'] = df['{col1}'] - df['{col2}']"
        explanation = f"Create new columns by assigning calculated values ({operation})"
        while attempts < max_attempts:
            attempts += 1
            code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
            
            # Handle special commands
            is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
            
            if is_exit:
                self.record_exercise_completion("exercise_4", tasks_completed, total_tasks)
                grade = (tasks_completed / total_tasks) * 100.0
                print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                return
            
            if is_skip:
                break
            
            if not should_continue:
                continue
            
            if not code:
                print("❌ Please enter some code")
                attempts -= 1
                continue
            
            # Check if answer matches exactly (normalizing whitespace)
            code_normalized = ' '.join(code.strip().split())
            correct_normalized = ' '.join(correct_answer.strip().split())
            
            if code_normalized == correct_normalized:
                # Exact match - execute and accept
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error executing code: {error}")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
                print(f"\n✅ Correct!")
                task2_completed = True
                tasks_completed += 1
                break
            else:
                # Not exact match - reject
                print("❌ Incorrect answer. Please enter the exact code.")
                if attempts < max_attempts:
                    print("💡 Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(correct_answer)
                    print(f"\n💡 Explanation: {explanation}")
                    break
                continue
        
        # TASK 3: Drop a column
        col_to_drop = self.get_random_column()
        if col_to_drop:
            print("\n" + "="*60)
            print(f"TASK 3: Drop the '{col_to_drop}' column from the dataframe")
            print("="*60)
            print(f"💡 Dataset: {self.current_dataset_name}")
            print("💡 Hint: Think about how to remove a column from a dataframe")
            print(f"💡 Remove the '{col_to_drop}' column")
            print("\nEnter your pandas code below:")
            
            task3_completed = False
            attempts = 0
            max_attempts = 3
            correct_answer = f"df.drop(columns=['{col_to_drop}'])"
            explanation = "drop() with columns parameter removes specified columns"
            while attempts < max_attempts:
                attempts += 1
                code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
                
                # Handle special commands
                is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
                
                if is_exit:
                    self.record_exercise_completion("exercise_4", tasks_completed, total_tasks)
                    grade = (tasks_completed / total_tasks) * 100.0
                    print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                    return
                
                if is_skip:
                    break
                
                if not should_continue:
                    continue
                
                if not code:
                    print("❌ Please enter some code")
                    attempts -= 1
                    continue
                
                # Check if answer matches exactly (normalizing whitespace)
                code_normalized = ' '.join(code.strip().split())
                correct_normalized = ' '.join(correct_answer.strip().split())
                
                if code_normalized == correct_normalized:
                    # Exact match - execute and accept
                    result, error = self.execute_pandas_code(df, code)
                    if error:
                        print(f"❌ Error executing code: {error}")
                        if attempts < max_attempts:
                            print("💡 Try again.")
                        else:
                            print("\n" + "="*60)
                            print("📖 CORRECT ANSWER:")
                            print("="*60)
                            print(correct_answer)
                            print(f"\n💡 Explanation: {explanation}")
                            break
                        continue
                    print(f"\n✅ Correct!")
                    task3_completed = True
                    tasks_completed += 1
                    break
                else:
                    # Not exact match - reject
                    print("❌ Incorrect answer. Please enter the exact code.")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
        
        # TASK 4: Change data type of a column
        numeric_col = self.get_random_numeric_column()
        if numeric_col:
            print("\n" + "="*60)
            print(f"TASK 4: Convert the '{numeric_col}' column to integer type")
            print("="*60)
            print(f"💡 Dataset: {self.current_dataset_name}")
            print("💡 Hint: Use astype() method to convert data types")
            print(f"💡 Convert '{numeric_col}' to int64")
            print("\nEnter your pandas code below:")
            
            task4_completed = False
            attempts = 0
            max_attempts = 3
            correct_answer = f"df['{numeric_col}'] = df['{numeric_col}'].astype('int64')"
            explanation = "astype() converts column to specified data type"
            while attempts < max_attempts:
                attempts += 1
                code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
                
                # Handle special commands
                is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
                
                if is_exit:
                    self.record_exercise_completion("exercise_4", tasks_completed, total_tasks)
                    grade = (tasks_completed / total_tasks) * 100.0
                    print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                    return
                
                if is_skip:
                    break
                
                if not should_continue:
                    continue
                
                if not code:
                    print("❌ Please enter some code")
                    attempts -= 1
                    continue
                
                # Check if answer matches exactly (normalizing whitespace)
                code_normalized = ' '.join(code.strip().split())
                correct_normalized = ' '.join(correct_answer.strip().split())
                
                if code_normalized == correct_normalized:
                    # Exact match - execute and accept
                    result, error = self.execute_pandas_code(df, code)
                    if error:
                        print(f"❌ Error executing code: {error}")
                        if attempts < max_attempts:
                            print("💡 Try again.")
                        else:
                            print("\n" + "="*60)
                            print("📖 CORRECT ANSWER:")
                            print("="*60)
                            print(correct_answer)
                            print(f"\n💡 Explanation: {explanation}")
                            break
                        continue
                    print(f"\n✅ Correct!")
                    task4_completed = True
                    tasks_completed += 1
                    break
                else:
                    # Not exact match - reject
                    print("❌ Incorrect answer. Please enter the exact code.")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
        
        # TASK 5: Reorder columns
        all_cols_list = df.columns.tolist()
        if len(all_cols_list) >= 3:
            reordered_cols = random.sample(all_cols_list, min(4, len(all_cols_list)))
            random.shuffle(reordered_cols)
            print("\n" + "="*60)
            print(f"TASK 5: Reorder columns to: {reordered_cols}")
            print("="*60)
            print(f"💡 Dataset: {self.current_dataset_name}")
            print("💡 Hint: Think about how to rearrange columns in a specific order")
            print(f"💡 Reorder columns to match: {reordered_cols}")
            print("\nEnter your pandas code below:")
            
            task5_completed = False
            attempts = 0
            max_attempts = 3
            correct_answer = f"df[{reordered_cols}]"
            explanation = "Select columns in desired order using list"
            while attempts < max_attempts:
                attempts += 1
                code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
                
                # Handle special commands
                is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
                
                if is_exit:
                    self.record_exercise_completion("exercise_4", tasks_completed, total_tasks)
                    grade = (tasks_completed / total_tasks) * 100.0
                    print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                    return
                
                if is_skip:
                    break
                
                if not should_continue:
                    continue
                
                if not code:
                    print("❌ Please enter some code")
                    attempts -= 1
                    continue
                
                # Check if answer matches exactly (normalizing whitespace)
                code_normalized = ' '.join(code.strip().split())
                correct_normalized = ' '.join(correct_answer.strip().split())
                
                if code_normalized == correct_normalized:
                    # Exact match - execute and accept
                    result, error = self.execute_pandas_code(df, code)
                    if error:
                        print(f"❌ Error executing code: {error}")
                        if attempts < max_attempts:
                            print("💡 Try again.")
                        else:
                            print("\n" + "="*60)
                            print("📖 CORRECT ANSWER:")
                            print("="*60)
                            print(correct_answer)
                            print(f"\n💡 Explanation: {explanation}")
                            break
                        continue
                    print(f"\n✅ Correct!")
                    task5_completed = True
                    tasks_completed += 1
                    break
                else:
                    # Not exact match - reject
                    print("❌ Incorrect answer. Please enter the exact code.")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
        
        # TASK 6: Apply a function to a column
        numeric_col2 = self.get_random_numeric_column()
        if numeric_col2:
            print("\n" + "="*60)
            print(f"TASK 6: Create a new column '{numeric_col2}_squared' with squared values of '{numeric_col2}'")
            print("="*60)
            print(f"💡 Dataset: {self.current_dataset_name}")
            print("💡 Hint: Think about how to apply a mathematical operation to all values in a column")
            print(f"💡 Create new column with values from '{numeric_col2}' squared")
            print("\nEnter your pandas code below:")
            
            task8_completed = False
            attempts = 0
            max_attempts = 3
            new_col_name = f"{numeric_col2}_squared"
            correct_answer = f"df['{new_col_name}'] = df['{numeric_col2}'] ** 2"
            explanation = "Use ** for exponentiation"
            while attempts < max_attempts:
                attempts += 1
                code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
                
                # Handle special commands
                is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
                
                if is_exit:
                    self.record_exercise_completion("exercise_4", tasks_completed, total_tasks)
                    grade = (tasks_completed / total_tasks) * 100.0
                    print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                    return
                
                if is_skip:
                    break
                
                if not should_continue:
                    continue
                
                if not code:
                    print("❌ Please enter some code")
                    attempts -= 1
                    continue
                
                # Check if answer matches exactly (normalizing whitespace)
                code_normalized = ' '.join(code.strip().split())
                correct_normalized = ' '.join(correct_answer.strip().split())
                
                if code_normalized == correct_normalized:
                    # Exact match - execute and accept
                    result, error = self.execute_pandas_code(df, code)
                    if error:
                        print(f"❌ Error executing code: {error}")
                        if attempts < max_attempts:
                            print("💡 Try again.")
                        else:
                            print("\n" + "="*60)
                            print("📖 CORRECT ANSWER:")
                            print("="*60)
                            print(correct_answer)
                            print(f"\n💡 Explanation: {explanation}")
                            break
                        continue
                    print(f"\n✅ Correct!")
                    task8_completed = True
                    tasks_completed += 1
                    break
                else:
                    # Not exact match - reject
                    print("❌ Incorrect answer. Please enter the exact code.")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
        
        # TASK 7: Correlation - Correlation with a specific column
        numeric_cols = self.get_numeric_columns()
        if len(numeric_cols) < 2:
            print("\n⚠️  Not enough numeric columns for correlation task. Skipping task 7.")
        else:
            target_col = random.choice(numeric_cols)
            print("\n" + "="*60)
            print(f"TASK 7: Get correlations of all numeric columns with '{target_col}'")
            print("="*60)
            print(f"💡 Dataset: {self.current_dataset_name}")
            print("💡 Hint: Think about how to see relationships between one column and all others")
            print(f"💡 Find how all other numeric columns correlate with '{target_col}'")
            print("\nEnter your pandas code below:")
            
            task5_completed = False
            attempts = 0
            max_attempts = 3
            correct_answer = f"df.corr()['{target_col}']"
            explanation = "Get a column from the correlation matrix to see correlations with that column"
            while attempts < max_attempts:
                attempts += 1
                code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
                
                # Handle special commands
                is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
                
                if is_exit:
                    self.record_exercise_completion("exercise_4", tasks_completed, total_tasks)
                    grade = (tasks_completed / total_tasks) * 100.0
                    print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                    return
                
                if is_skip:
                    break
                
                if not should_continue:
                    continue
                
                if not code:
                    print("❌ Please enter some code")
                    attempts -= 1
                    continue
                
                # Check if answer matches exactly (normalizing whitespace)
                code_normalized = ' '.join(code.strip().split())
                correct_normalized = ' '.join(correct_answer.strip().split())
                
                if code_normalized == correct_normalized:
                    # Exact match - execute and accept
                    result, error = self.execute_pandas_code(df, code)
                    if error:
                        print(f"❌ Error executing code: {error}")
                        if attempts < max_attempts:
                            print("💡 Try again.")
                        else:
                            print("\n" + "="*60)
                            print("📖 CORRECT ANSWER:")
                            print("="*60)
                            print(correct_answer)
                            print(f"\n💡 Explanation: {explanation}")
                            break
                        continue
                    print(f"\n✅ Correct!")
                    task5_completed = True
                    tasks_completed += 1
                    break
                else:
                    # Not exact match - reject
                    print("❌ Incorrect answer. Please enter the exact code.")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
        
        # TASK 8: Plotting - Create a bar plot of value counts for a categorical column
        categorical_cols = self.get_categorical_columns()
        if not categorical_cols:
            print("\n⚠️  No categorical columns for plotting task. Skipping task 8.")
        else:
            col = random.choice(categorical_cols)
            print("\n" + "="*60)
            print(f"TASK 8: Create a bar plot of value counts for the '{col}' column")
            print("="*60)
            print(f"💡 Dataset: {self.current_dataset_name}")
            print("💡 Hint: Think about how to count values and visualize their frequencies")
            print(f"💡 Create a bar plot showing the frequency of each category in '{col}'")
            print("💡 Note: The plot will be created but not displayed (non-interactive mode)")
            print("\nEnter your pandas code below:")
            
            task6_completed = False
            attempts = 0
            max_attempts = 3
            correct_answer = f"df['{col}'].value_counts().plot(kind='bar')"
            explanation = "value_counts() gets frequencies, plot(kind='bar') creates a bar plot"
            while attempts < max_attempts:
                attempts += 1
                code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
                
                # Handle special commands
                is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
                
                if is_exit:
                    self.record_exercise_completion("exercise_4", tasks_completed, total_tasks)
                    grade = (tasks_completed / total_tasks) * 100.0
                    print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                    return
                
                if is_skip:
                    break
                
                if not should_continue:
                    continue
                
                if not code:
                    print("❌ Please enter some code")
                    attempts -= 1
                    continue
                
                # Check if answer matches exactly (normalizing whitespace)
                code_normalized = ' '.join(code.strip().split())
                correct_normalized = ' '.join(correct_answer.strip().split())
                
                if code_normalized == correct_normalized:
                    # Exact match - execute and accept
                    result, error = self.execute_pandas_code(df, code, include_plotting=True)
                    if error:
                        print(f"❌ Error executing code: {error}")
                        if attempts < max_attempts:
                            print("💡 Try again.")
                        else:
                            print("\n" + "="*60)
                            print("📖 CORRECT ANSWER:")
                            print("="*60)
                            print(correct_answer)
                            print(f"\n💡 Explanation: {explanation}")
                            break
                        continue
                    print(f"\n✅ Correct!")
                    task6_completed = True
                    tasks_completed += 1
                    break
                else:
                    # Not exact match - reject
                    print("❌ Incorrect answer. Please enter the exact code.")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
        
        # Exercise 4 complete - record completion
        self.record_exercise_completion("exercise_4", tasks_completed, total_tasks)
        grade = (tasks_completed / total_tasks) * 100.0
        print(f"\n✅ Exercise 4 Complete! Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
        input("\nPress Enter to continue...")
    
    def exercise_5_data_cleaning(self):
        """Exercise: Data cleaning."""
        print("\n🎯 GOAL: Learn data cleaning techniques")
        
        df = self.load_dataset("sales_data.csv")
        if df is None:
            return
        
        tasks_completed = 0
        total_tasks = 8  # 8 tasks: 6 core, 1 correlation, 1 plotting
        
        # TASK 1: Varied - randomly choose between per-column or total count
        task1_type = random.choice(['per_column', 'total_count'])
        
        if task1_type == 'per_column':
            print("\n" + "="*60)
            print("TASK 1: Find missing values per column")
            print("="*60)
            print(f"💡 Dataset: {self.current_dataset_name}")
            print("💡 Hint: Think about how to identify missing or null values")
            print("💡 You can then sum them to count missing values per column")
            print(f"\nDataset shape: {df.shape}")
            print("\nEnter your pandas code below:")
            
            expected = df.isnull().sum()
            task1_completed = False
            attempts = 0
            max_attempts = 3
            correct_answer = "df.isnull().sum()"
            explanation = "isnull() checks for null/NaN values, sum() counts them per column"
            while attempts < max_attempts:
                attempts += 1
                code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
                
                # Handle special commands
                is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
                
                if is_exit:
                    self.record_exercise_completion("exercise_5", tasks_completed, total_tasks)
                    grade = (tasks_completed / total_tasks) * 100.0
                    print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                    return
                
                if is_skip:
                    break
                
                if not should_continue:
                    continue
                
                if not code:
                    print("❌ Please enter some code")
                    attempts -= 1
                    continue
                
                result, error = self.execute_pandas_code(df, code)
                # Validate that it's actual pandas code, not just a literal value
                is_valid, error_msg = self.is_valid_pandas_code(code)
                if not is_valid:
                    print(f"❌ {error_msg}")
                    if attempts < max_attempts:
                        print("💡 You need to write pandas code, not just enter a value")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue

                if error:
                    print(f"❌ Error: {error}")
                    print("💡 Fix the error and try again")
                    if attempts >= max_attempts:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print("df.isnull().sum()")
                        print("\n💡 Explanation: isnull() checks for null/NaN values, sum() counts them per column")
                        break
                    continue
                
                print(f"\n📊 Result:")
                print(result)
                
                try:
                    if hasattr(result, 'equals'):
                        if result.equals(expected):
                            print("\n✅ Correct! You found all missing values per column!")
                            task1_completed = True
                            tasks_completed += 1
                            break
                    
                    if hasattr(result, 'index') and hasattr(result, 'values'):
                        if all(result.index == expected.index):
                            if all(result.values == expected.values):
                                print("\n✅ Correct! You found all missing values per column!")
                                task1_completed = True
                                tasks_completed += 1
                                break
                    
                    print("\n❌ Result doesn't match expected missing value counts")
                    if attempts < max_attempts:
                        print("💡 Your answer is not correct. Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print("df.isnull().sum()")
                        print("\n💡 Explanation: isnull() checks for null/NaN values, sum() counts them per column")
                        break
                except Exception as e:
                    print(f"\n❌ Error validating: {str(e)}")
                    if attempts >= max_attempts:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print("df.isnull().sum()")
                        print("\n💡 Explanation: isnull() checks for null/NaN values, sum() counts them per column")
                        break
                    print("💡 Make sure your code returns a Series with missing value counts per column")
                    continue
        else:
            # Total count
            print("\n" + "="*60)
            print("TASK 1: Count the total number of missing values in the entire dataframe")
            print("="*60)
            print(f"💡 Dataset: {self.current_dataset_name}")
            print("💡 Hint: Think about how to count missing values across the entire dataframe")
            print(f"\nDataset shape: {df.shape}")
            print("\nEnter your pandas code below:")
            
            expected_total = df.isnull().sum().sum()
            task1_completed = False
            attempts = 0
            max_attempts = 3
            correct_answer = "df.isnull().sum().sum()"
            explanation = "First sum() counts per column, second sum() totals all columns"
            while attempts < max_attempts:
                attempts += 1
                code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
                
                # Handle special commands
                is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
                
                if is_exit:
                    self.record_exercise_completion("exercise_5", tasks_completed, total_tasks)
                    grade = (tasks_completed / total_tasks) * 100.0
                    print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                    return
                
                if is_skip:
                    break
                
                if not should_continue:
                    continue
                
                if not code:
                    print("❌ Please enter some code")
                    attempts -= 1
                    continue
                
                # Check if answer matches exactly (normalizing whitespace)
                code_normalized = ' '.join(code.strip().split())
                correct_normalized = ' '.join(correct_answer.strip().split())
                
                if code_normalized == correct_normalized:
                    # Exact match - execute and accept
                    result, error = self.execute_pandas_code(df, code)
                    if error:
                        print(f"❌ Error executing code: {error}")
                        if attempts < max_attempts:
                            print("💡 Try again.")
                        else:
                            print("\n" + "="*60)
                            print("📖 CORRECT ANSWER:")
                            print("="*60)
                            print(correct_answer)
                            print(f"\n💡 Explanation: {explanation}")
                            break
                        continue
                    print(f"\n✅ Correct!")
                    task1_completed = True
                    tasks_completed += 1
                    break
                else:
                    # Not exact match - reject
                    print("❌ Incorrect answer. Please enter the exact code.")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
        
        print("\n" + "="*60)
        print("TASK 2: Remove duplicates")
        print("="*60)
        print(f"💡 Dataset: {self.current_dataset_name}")
        print(f"💡 Current shape: {df.shape}")
        print("💡 Hint: Think about how to eliminate duplicate rows")
        print("\nEnter your pandas code below:")
        
        task2_completed = False
        attempts = 0
        max_attempts = 3
        correct_answer = "df.drop_duplicates()"
        explanation = "drop_duplicates() removes duplicate rows from the dataframe"
        while attempts < max_attempts:
            attempts += 1
            code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
            
            # Handle special commands
            is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
            
            if is_exit:
                self.record_exercise_completion("exercise_5", tasks_completed, total_tasks)
                grade = (tasks_completed / total_tasks) * 100.0
                print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                return
            
            if is_skip:
                break
            
            if not should_continue:
                continue
            
            if not code:
                print("❌ Please enter some code")
                attempts -= 1
                continue
            
            # Check if answer matches exactly (normalizing whitespace)
            code_normalized = ' '.join(code.strip().split())
            correct_normalized = ' '.join(correct_answer.strip().split())
            
            if code_normalized == correct_normalized:
                # Exact match - execute and accept
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error executing code: {error}")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
                print(f"\n✅ Correct!")
                task2_completed = True
                tasks_completed += 1
                break
            else:
                # Not exact match - reject
                print("❌ Incorrect answer. Please enter the exact code.")
                if attempts < max_attempts:
                    print("💡 Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(correct_answer)
                    print(f"\n💡 Explanation: {explanation}")
                    break
                continue
        
        # TASK 3: Varied missing value handling - randomly choose method
        # Temporarily introduce some missing values if none exist, for educational purposes
        df_original = df.copy()
        missing_before = df.isnull().sum().sum()
        if missing_before == 0:
            # Introduce some missing values for this task
            # Randomly select a few cells to set as NaN
            num_missing = min(5, len(df) * len(df.columns) // 10)  # About 10% of cells, max 5
            for _ in range(num_missing):
                row_idx = random.randint(0, len(df) - 1)
                col_idx = random.randint(0, len(df.columns) - 1)
                df.iloc[row_idx, col_idx] = np.nan
            missing_before = df.isnull().sum().sum()
        
        if missing_before > 0:
            # Use fill_value method
            # Determine fill value based on dataset
            cols_with_missing = df.columns[df.isnull().any()].tolist()
            if cols_with_missing:
                numeric_cols_with_missing = [col for col in cols_with_missing if df[col].dtype in ['int64', 'float64']]
                string_cols_with_missing = [col for col in cols_with_missing if df[col].dtype == 'object']
                
                if numeric_cols_with_missing:
                    col_with_missing = random.choice(numeric_cols_with_missing)
                    fill_options = [0, round(df[col_with_missing].mean(), 2), round(df[col_with_missing].median(), 2)]
                    fill_value = random.choice(fill_options)
                elif string_cols_with_missing:
                    fill_value = "Unknown"
                else:
                    fill_value = 0
            else:
                fill_value = 0
            
            print("\n" + "="*60)
            print(f"TASK 3: Fill all missing values with {fill_value}")
            print("="*60)
            print(f"💡 Dataset: {self.current_dataset_name}")
            print("💡 Hint: Think about how to fill in missing values with a specific value")
            print(f"💡 Current missing values: {missing_before}")
            print(f"💡 Fill all missing values with {fill_value}")
            print("\nEnter your pandas code below:")
            
            task3_completed = False
            attempts = 0
            max_attempts = 3
            correct_answer = f"df.fillna({fill_value})"
            explanation = f"fillna({fill_value}) fills missing values with {fill_value}"
            while attempts < max_attempts:
                    attempts += 1
                    code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
                    
                    # Handle special commands
                    is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
                    
                    if is_exit:
                        self.record_exercise_completion("exercise_5", tasks_completed, total_tasks)
                        grade = (tasks_completed / total_tasks) * 100.0
                        print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                        return
                    
                    if is_skip:
                        break
                    
                    if not should_continue:
                        continue
                    
                    if not code:
                        print("❌ Please enter some code")
                        attempts -= 1
                        continue
                    
                    # Check if answer matches exactly (normalizing whitespace)
                    code_normalized = ' '.join(code.strip().split())
                    correct_normalized = ' '.join(correct_answer.strip().split())
                    
                    if code_normalized == correct_normalized:
                        # Exact match - execute and accept
                        result, error = self.execute_pandas_code(df, code)
                        if error:
                            print(f"❌ Error executing code: {error}")
                            if attempts < max_attempts:
                                print("💡 Try again.")
                            else:
                                print("\n" + "="*60)
                                print("📖 CORRECT ANSWER:")
                                print("="*60)
                                print(correct_answer)
                                print(f"\n💡 Explanation: {explanation}")
                                break
                            continue
                        print(f"\n✅ Correct!")
                        task3_completed = True
                        tasks_completed += 1
                        break
                    else:
                        # Not exact match - reject
                        print("❌ Incorrect answer. Please enter the exact code.")
                        if attempts < max_attempts:
                            print("💡 Try again.")
                        else:
                            print("\n" + "="*60)
                            print("📖 CORRECT ANSWER:")
                            print("="*60)
                            print(correct_answer)
                            print(f"\n💡 Explanation: {explanation}")
                            break
                        continue
        
        # TASK 4: Fill missing values with forward fill
        # Reintroduce missing values if task 3 removed them all
        missing_after_task3 = df.isnull().sum().sum()
        if missing_after_task3 == 0:
            # Reintroduce some missing values for this task
            num_missing = min(3, len(df) * len(df.columns) // 10)  # About 10% of cells, max 3
            for _ in range(num_missing):
                row_idx = random.randint(0, len(df) - 1)
                col_idx = random.randint(0, len(df.columns) - 1)
                df.iloc[row_idx, col_idx] = np.nan
        
        cols_with_nulls_ffill = [col for col in df.columns if df[col].isnull().any()]
        if cols_with_nulls_ffill:
            col_to_ffill = random.choice(cols_with_nulls_ffill)
            print("\n" + "="*60)
            print(f"TASK 4: Fill missing values in '{col_to_ffill}' column using forward fill")
            print("="*60)
            print(f"💡 Dataset: {self.current_dataset_name}")
            print("💡 Hint: Think about how to fill missing values by propagating the previous value forward")
            print(f"💡 Fill missing values in '{col_to_ffill}' by propagating the previous value forward")
            print("\nEnter your pandas code below:")
            
            task4_completed = False
            attempts = 0
            max_attempts = 3
            correct_answer = f"df['{col_to_ffill}'] = df['{col_to_ffill}'].fillna(method='ffill')"
            explanation = "Forward fill propagates the previous value forward"
            while attempts < max_attempts:
                attempts += 1
                code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
                
                # Handle special commands
                is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
                
                if is_exit:
                    self.record_exercise_completion("exercise_5", tasks_completed, total_tasks)
                    grade = (tasks_completed / total_tasks) * 100.0
                    print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                    return
                
                if is_skip:
                    break
                
                if not should_continue:
                    continue
                
                if not code:
                    print("❌ Please enter some code")
                    attempts -= 1
                    continue
                
                # Check if answer matches exactly (normalizing whitespace)
                code_normalized = ' '.join(code.strip().split())
                correct_normalized = ' '.join(correct_answer.strip().split())
                
                if code_normalized == correct_normalized:
                    # Exact match - execute and accept
                    result, error = self.execute_pandas_code(df, code)
                    if error:
                        print(f"❌ Error executing code: {error}")
                        if attempts < max_attempts:
                            print("💡 Try again.")
                        else:
                            print("\n" + "="*60)
                            print("📖 CORRECT ANSWER:")
                            print("="*60)
                            print(correct_answer)
                            print(f"\n💡 Explanation: {explanation}")
                            break
                        continue
                    print(f"\n✅ Correct!")
                    task4_completed = True
                    tasks_completed += 1
                    break
                else:
                    # Not exact match - reject
                    print("❌ Incorrect answer. Please enter the exact code.")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
        
        # TASK 5: Drop columns with missing values
        # Reintroduce missing values if previous tasks removed them all
        missing_after_task4 = df.isnull().sum().sum()
        if missing_after_task4 == 0:
            # Reintroduce some missing values for this task
            num_missing = min(3, len(df) * len(df.columns) // 10)  # About 10% of cells, max 3
            for _ in range(num_missing):
                row_idx = random.randint(0, len(df) - 1)
                col_idx = random.randint(0, len(df.columns) - 1)
                df.iloc[row_idx, col_idx] = np.nan
        
        cols_with_nulls = [col for col in df.columns if df[col].isnull().any()]
        if cols_with_nulls:
            col_to_drop = random.choice(cols_with_nulls)
            print("\n" + "="*60)
            print(f"TASK 5: Drop the '{col_to_drop}' column (it has missing values)")
            print("="*60)
            print(f"💡 Dataset: {self.current_dataset_name}")
            print("💡 Hint: Think about how to remove a column from a dataframe")
            print(f"💡 Remove the '{col_to_drop}' column")
            print("\nEnter your pandas code below:")
            
            task7_completed = False
            attempts = 0
            max_attempts = 3
            correct_answer = f"df.drop(columns=['{col_to_drop}'])"
            explanation = "drop(columns=[]) removes specified columns"
            while attempts < max_attempts:
                attempts += 1
                code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
                
                # Handle special commands
                is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
                
                if is_exit:
                    self.record_exercise_completion("exercise_5", tasks_completed, total_tasks)
                    grade = (tasks_completed / total_tasks) * 100.0
                    print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                    return
                
                if is_skip:
                    break
                
                if not should_continue:
                    continue
                
                if not code:
                    print("❌ Please enter some code")
                    attempts -= 1
                    continue
                
                # Check if answer matches exactly (normalizing whitespace)
                code_normalized = ' '.join(code.strip().split())
                correct_normalized = ' '.join(correct_answer.strip().split())
                
                if code_normalized == correct_normalized:
                    # Exact match - execute and accept
                    result, error = self.execute_pandas_code(df, code)
                    if error:
                        print(f"❌ Error executing code: {error}")
                        if attempts < max_attempts:
                            print("💡 Try again.")
                        else:
                            print("\n" + "="*60)
                            print("📖 CORRECT ANSWER:")
                            print("="*60)
                            print(correct_answer)
                            print(f"\n💡 Explanation: {explanation}")
                            break
                        continue
                    print(f"\n✅ Correct!")
                    task7_completed = True
                    tasks_completed += 1
                    break
                else:
                    # Not exact match - reject
                    print("❌ Incorrect answer. Please enter the exact code.")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
        
        # TASK 6: Drop rows where ALL columns are missing
        print("\n" + "="*60)
        print("TASK 6: Remove rows where ALL columns have missing values")
        print("="*60)
        print(f"💡 Dataset: {self.current_dataset_name}")
        print("💡 Hint: Think about how to remove rows only when all columns are missing")
        print("💡 Remove only rows where every column is missing (not rows with some missing values)")
        print("\nEnter your pandas code below:")
        
        task8_completed = False
        attempts = 0
        max_attempts = 3
        correct_answer = "df.dropna(how='all')"
        explanation = "how='all' removes rows only when all columns are missing"
        while attempts < max_attempts:
            attempts += 1
            code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
            
            # Handle special commands
            is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
            
            if is_exit:
                self.record_exercise_completion("exercise_5", tasks_completed, total_tasks)
                grade = (tasks_completed / total_tasks) * 100.0
                print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                return
            
            if is_skip:
                break
            
            if not should_continue:
                continue
            
            if not code:
                print("❌ Please enter some code")
                attempts -= 1
                continue
            
            # Check if answer matches exactly (normalizing whitespace)
            code_normalized = ' '.join(code.strip().split())
            correct_normalized = ' '.join(correct_answer.strip().split())
            
            if code_normalized == correct_normalized:
                # Exact match - execute and accept
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error executing code: {error}")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
                print(f"\n✅ Correct!")
                task8_completed = True
                tasks_completed += 1
                break
            else:
                # Not exact match - reject
                print("❌ Incorrect answer. Please enter the exact code.")
                if attempts < max_attempts:
                    print("💡 Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(correct_answer)
                    print(f"\n💡 Explanation: {explanation}")
                    break
                continue
        
        # TASK 7: Correlation - Correlation matrix
        numeric_cols = self.get_numeric_columns()
        if len(numeric_cols) < 2:
            print("\n⚠️  Not enough numeric columns for correlation task. Skipping task 7.")
        else:
            print("\n" + "="*60)
            print("TASK 7: Calculate the correlation matrix for all numeric columns")
            print("="*60)
            print(f"💡 Dataset: {self.current_dataset_name}")
            print("💡 Hint: Use corr() method to calculate correlations between all numeric columns")
            print("💡 This returns a matrix showing how each numeric column relates to others")
            print("\nEnter your pandas code below:")
            
            task5_completed = False
            attempts = 0
            max_attempts = 3
            correct_answer = "df.corr()"
            explanation = "corr() calculates pairwise correlations between all numeric columns"
            while attempts < max_attempts:
                attempts += 1
                code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
                
                # Handle special commands
                is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
                
                if is_exit:
                    self.record_exercise_completion("exercise_5", tasks_completed, total_tasks)
                    grade = (tasks_completed / total_tasks) * 100.0
                    print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                    return
                
                if is_skip:
                        break
        
                if not should_continue:
                    continue
                
                if not code:
                    print("❌ Please enter some code")
                    attempts -= 1
                    continue
                
                # Check if answer matches exactly (normalizing whitespace)
                code_normalized = ' '.join(code.strip().split())
                correct_normalized = ' '.join(correct_answer.strip().split())
                
                if code_normalized == correct_normalized:
                    # Exact match - execute and accept
                    result, error = self.execute_pandas_code(df, code)
                    if error:
                        print(f"❌ Error executing code: {error}")
                        if attempts < max_attempts:
                            print("💡 Try again.")
                        else:
                            print("\n" + "="*60)
                            print("📖 CORRECT ANSWER:")
                            print("="*60)
                            print(correct_answer)
                            print(f"\n💡 Explanation: {explanation}")
                            break
                        continue
                    print(f"\n✅ Correct!")
                    task5_completed = True
                    tasks_completed += 1
                    break
                else:
                    # Not exact match - reject
                    print("❌ Incorrect answer. Please enter the exact code.")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
                    
        # TASK 8: Get dataframe information
        print("\n" + "="*60)
        print("TASK 8: Get information about the dataframe")
        print("="*60)
        print(f"💡 Dataset: {self.current_dataset_name}")
        print("💡 Hint: There's a method that shows data types, non-null counts, and memory usage")
        print("💡 This is useful for understanding your cleaned data")
        print("\nEnter your pandas code below:")
        
        task8_completed = False
        attempts = 0
        max_attempts = 3
        correct_answer = "df.info()"
        explanation = "info() displays dataframe structure, data types, and non-null counts"
        while attempts < max_attempts:
            attempts += 1
            code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
            
            # Handle special commands
            is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)
            
            if is_exit:
                self.record_exercise_completion("exercise_5", tasks_completed, total_tasks)
                grade = (tasks_completed / total_tasks) * 100.0
                print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
                return
            
            if is_skip:
                break

            if not should_continue:
                continue
            
            if not code:
                print("❌ Please enter some code")
                attempts -= 1
                continue
            
            # Check if answer matches exactly (normalizing whitespace)
            code_normalized = ' '.join(code.strip().split())
            correct_normalized = ' '.join(correct_answer.strip().split())
            
            if code_normalized == correct_normalized:
                # Exact match - execute and accept
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error executing code: {error}")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(correct_answer)
                        print(f"\n💡 Explanation: {explanation}")
                        break
                    continue
                print(f"\n✅ Correct!")
                task8_completed = True
                tasks_completed += 1
                break
            else:
                # Not exact match - reject
                print("❌ Incorrect answer. Please enter the exact code.")
                if attempts < max_attempts:
                    print("💡 Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(correct_answer)
                    print(f"\n💡 Explanation: {explanation}")
                    break
                continue
        
        # Record exercise completion
        self.record_exercise_completion("exercise_5", tasks_completed, total_tasks)
        grade = (tasks_completed / total_tasks) * 100.0
        print(f"\n✅ Exercise 5 Complete! Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
        input("\nPress Enter to continue...")
    
    def reset_statistics(self):
        """Reset all learning statistics. Returns True if reset, False if cancelled."""
        while True:
            confirm = input("\n⚠️  Are you sure you want to reset all statistics? (yes/no): ").strip().lower()
            if confirm in ['yes', 'y']:
                self.progress["exercise_stats"] = {}
                self.progress["last_session"] = None
                self.save_progress()
                print("\n✅ Statistics reset successfully!")
                return True
            elif confirm in ['no', 'n']:
                print("\n❌ Reset cancelled.")
                return False
            else:
                print("❌ Invalid choice. Please enter 'yes', 'no', 'y', or 'n'.")
    
    def show_statistics(self):
        """Display learning statistics."""
        while True:
            print("\n" + "="*60)
            print("📊 YOUR LEARNING STATISTICS")
            print("="*60)
            
            exercise_names = {
                "exercise_1": "Exercise 1: Basic Operations",
                "exercise_2": "Exercise 2: Filtering Data",
                "exercise_3": "Exercise 3: Sorting and Selection",
                "exercise_4": "Exercise 4: Data Manipulation",
                "exercise_5": "Exercise 5: Data Cleaning"
            }
            
            stats = self.progress.get("exercise_stats", {})
            if not stats:
                print("No exercises completed yet.")
            else:
                print("\nExercise Statistics:")
                print("-" * 60)
                for ex_key, ex_name in exercise_names.items():
                    if ex_key in stats:
                        ex_stat = stats[ex_key]
                        count = ex_stat.get("count", 0)
                        total_grade = ex_stat.get("total_grade", 0.0)
                        avg_grade = total_grade / count if count > 0 else 0.0
                        print(f"\n{ex_name}:")
                        print(f"  Times Completed: {count}")
                        print(f"  Average Grade: {avg_grade:.2f}%")
                    else:
                        print(f"\n{ex_name}:")
                        print(f"  Times Completed: 0")
                        print(f"  Average Grade: N/A")
            
            if self.progress.get('last_session'):
                print(f"📅 Last Session: {self.progress['last_session']}")
            
            # Check if stats are already empty
            stats_empty = (
                not self.progress.get("exercise_stats", {}) and 
                not self.progress.get("last_session")
            )
            
            print("\n" + "="*60)
            print("Options:")
            if stats_empty:
                print("1. Back to Main Menu")
                choice = input("\nSelect option (1): ").strip()
                if choice == "1":
                    return
                else:
                    print("❌ Invalid choice! Please try again.")
                    continue
            else:
                print("1. Reset Statistics")
                print("2. Back to Main Menu")
                choice = input("\nSelect option (1-2): ").strip()
                if choice == "1":
                    was_reset = self.reset_statistics()
                    if was_reset:
                        # Reset was successful, go back to main menu
                        return
                    else:
                        # Reset was cancelled, show stats again (loop continues)
                        continue
                elif choice == "2":
                    return
                else:
                    print("❌ Invalid choice! Please try again.")
                    continue
    
    def main_menu(self):
        """Display and handle main menu."""
        while True:
            print("\n" + "="*60)
            print("🐼 PANDAS PRACTICE - Interactive Learning Tool")
            print("="*60)
            print("1. Explore Dataset")
            print("2. Run Exercise")
            print("3. View Learning Statistics")
            print("4. Exit")
            
            choice = input("\nSelect an option (1-4): ").strip()
            
            if choice == "1":
                self.explore_dataset()
            elif choice == "2":
                self.show_exercises()
            elif choice == "3":
                self.show_statistics()
            elif choice == "4":
                print("\nWe'll talk later! 👋")
                break
            else:
                print("❌ Invalid choice!")
    
    def list_datasets(self):
        """List available datasets."""
        if not self.data_dir.exists():
            print("❌ Data directory not found!")
            return
        
        datasets = list(self.data_dir.glob("*.csv"))
        if not datasets:
            print("❌ No datasets found in data directory!")
            return
        
        print("\n📁 Available Datasets:")
        for i, ds in enumerate(datasets, 1):
            print(f"  {i}. {ds.name}")
        
        while True:
            choice = input("\nEnter dataset number to load: ").strip()
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(datasets):
                    self.load_dataset(datasets[idx].name)
                    break
                else:
                    print(f"❌ Invalid number! Please enter a number between 1 and {len(datasets)}")
            except ValueError:
                print("❌ Invalid input! Please enter a valid number.")
    
    def show_exercises(self):
        """Show available exercises."""
        print("\n📝 Available Exercises:")
        print("1. Basic Operations")
        print("2. Filtering Data")
        print("3. Sorting and Column Selection")
        print("4. Data Manipulation")
        print("5. Data Cleaning")
        
        choice = input("\nSelect exercise (1-5): ").strip()
        try:
            self.run_exercise(int(choice))
        except:
            print("❌ Invalid choice!")


def main():
    """Main entry point."""
    app = PandasPractice()
    app.main_menu()


if __name__ == "__main__":
    main()
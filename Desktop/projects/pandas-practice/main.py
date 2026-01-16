"""
Pandas Practice - Interactive Learning Tool
A hands-on project to learn pandas through practical exercises and data analysis.
"""

import pandas as pd
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
            "datasets_explored": [],
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
            print("💡 Please load a dataset first from the main menu (option 1)")
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
            print("❌ No dataset loaded! Please load a dataset first.")
            return
        
        # Mark dataset as explored when entering exploration menu
        if self.current_dataset_name and self.current_dataset_name not in self.progress["datasets_explored"]:
            self.progress["datasets_explored"].append(self.current_dataset_name)
            self.save_progress()
        
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
            print("9. Group by and aggregate")
            print("10. Sort data")
            print("11. Return to main menu")
            
            choice = input("\nSelect an option (1-11): ").strip()
            
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
                group_col = input("Enter column to group by: ").strip()
                if group_col in df.columns:
                    agg_col = input("Enter column to aggregate: ").strip()
                    if agg_col in df.columns:
                        print("\nAvailable aggregations: sum, mean, count, min, max")
                        agg_func = input("Enter aggregation function: ").strip().lower()
                        try:
                            grouped = df.groupby(group_col)[agg_col].agg(agg_func)
                            print(f"\n📊 Grouped by '{group_col}', aggregated '{agg_col}' using {agg_func}:")
                            print(f"Dataset: {self.current_dataset_name}")
                            print(grouped)
                            self.wait_for_esc()
                        except Exception as e:
                            print(f"❌ Error: {e}")
                            self.wait_for_esc()
                    else:
                        print(f"❌ Column '{agg_col}' not found!")
                        self.wait_for_esc()
                else:
                    print(f"❌ Column '{group_col}' not found!")
                    self.wait_for_esc()
                    
            elif choice == "10":
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
                    
            elif choice == "11":
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
            
            result, error = self.execute_pandas_code(df, code)
            if error:
                print(f"❌ Error: {error}")
                print("💡 Fix the error and try again")
                if attempts >= max_attempts:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df.head({n_rows})")
                    print("\n💡 Explanation: The head() method displays the first n rows of a dataframe")
                    break
                continue
            
            print(f"\n📊 Result:")
            print(result)
            is_valid, message = self.validate_head_result(result, df, n_rows)
            if is_valid:
                print(f"\n✅ {message}")
                task1_completed = True
                tasks_completed += 1
                break
            else:
                print(f"\n❌ {message}")
                if attempts < max_attempts:
                    print("💡 Your answer is not correct. Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df.head({n_rows})")
                    print("\n💡 Explanation: The head() method displays the first n rows of a dataframe")
                    break
        
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
            
            result, error = self.execute_pandas_code(df, code)
            if error:
                print(f"❌ Error: {error}")
                print("💡 Fix the error and try again")
                if attempts >= max_attempts:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print("df.shape")
                    print("\n💡 Explanation: The shape attribute returns a tuple (rows, columns)")
                    break
                continue
            
            print(f"\n📊 Result: {result}")
            is_valid, message = self.validate_shape_result(result, df)
            if is_valid:
                print(f"\n✅ {message}")
                task2_completed = True
                tasks_completed += 1
                break
            else:
                print(f"\n❌ {message}")
                if attempts < max_attempts:
                    print("💡 Your answer is not correct. Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print("df.shape")
                    print("\n💡 Explanation: The shape attribute returns a tuple (rows, columns)")
                    break
        
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
            
            result, error = self.execute_pandas_code(df, code)
            if error:
                print(f"❌ Error: {error}")
                print("💡 Fix the error and try again")
                if attempts >= max_attempts:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print("df.columns")
                    print("\n💡 Explanation: The columns attribute returns the column names")
                    break
                continue
            
            print(f"\n📊 Result:")
            print(list(result) if hasattr(result, '__iter__') else result)
            is_valid, message = self.validate_columns_result(result, df)
            if is_valid:
                print(f"\n✅ {message}")
                task3_completed = True
                tasks_completed += 1
                break
            else:
                print(f"\n❌ {message}")
                if attempts < max_attempts:
                    print("💡 Your answer is not correct. Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print("df.columns")
                    print("\n💡 Explanation: The columns attribute returns an Index object with all column names")
                    break
        
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
            
            result, error = self.execute_pandas_code(df, code)
            if error:
                print(f"❌ Error: {error}")
                print("💡 Fix the error and try again")
                if attempts >= max_attempts:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print("df.dtypes")
                    print("\n💡 Explanation: The dtypes attribute returns a Series with data types for each column")
                    break
                continue
            
            print(f"\n📊 Result:")
            print(result)
            try:
                if hasattr(result, 'equals'):
                    if result.equals(df.dtypes):
                        print(f"\n✅ Correct! You displayed the data types correctly.")
                        task4_completed = True
                        tasks_completed += 1
                        break
                elif hasattr(result, 'index') and all(result.index == df.dtypes.index):
                    if all(result.values == df.dtypes.values):
                        print(f"\n✅ Correct! You displayed the data types correctly.")
                        task4_completed = True
                        tasks_completed += 1
                        break
            except:
                pass
            print(f"\n❌ Result doesn't match expected data types")
            if attempts < max_attempts:
                print("💡 Your answer is not correct. Try again.")
            else:
                print("\n" + "="*60)
                print("📖 CORRECT ANSWER:")
                print("="*60)
                print("df.dtypes")
                print("\n💡 Explanation: The dtypes attribute returns a Series with data types for each column")
                break
        
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
            
            result, error = self.execute_pandas_code(df, code)
            if error:
                print(f"❌ Error: {error}")
                print("💡 Fix the error and try again")
                if attempts >= max_attempts:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df.tail({n_rows_tail})")
                    print("\n💡 Explanation: The tail() method displays the last n rows of a dataframe")
                    break
                continue
            
            print(f"\n📊 Result:")
            print(result)
            expected = df.tail(n_rows_tail)
            if hasattr(result, 'shape') and result.shape == expected.shape:
                if result.reset_index(drop=True).equals(expected.reset_index(drop=True)):
                    print(f"\n✅ Correct! You displayed the last {n_rows_tail} rows!")
                task5_completed = True
                tasks_completed += 1
                break
            print(f"\n❌ Result doesn't match expected last {n_rows_tail} rows")
            if attempts < max_attempts:
                print("💡 Think about how to display the last rows of a dataframe")
                print("💡 Try again.")
            else:
                print("\n" + "="*60)
                print("📖 CORRECT ANSWER:")
                print("="*60)
                print(f"df.tail({n_rows_tail})")
                print("\n💡 Explanation: The tail() method displays the last n rows of a dataframe")
                break
        
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
            
            result, error = self.execute_pandas_code(df, code)
            if error:
                print(f"❌ Error: {error}")
                print("💡 Fix the error and try again")
                if attempts >= max_attempts:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print("df.describe()")
                    print("\n💡 Explanation: The describe() method provides descriptive statistics")
                    break
                continue
            
            print(f"\n📊 Result:")
            print(result)
            try:
                expected = df.describe()
                if hasattr(result, 'equals'):
                    if result.equals(expected):
                        print(f"\n✅ Correct! You got the statistical summary!")
                        task6_completed = True
                        tasks_completed += 1
                        break
                elif hasattr(result, 'shape') and result.shape == expected.shape:
                    if all(result.index == expected.index) and all(result.columns == expected.columns):
                        print(f"\n✅ Correct! You got the statistical summary!")
                        task6_completed = True
                        tasks_completed += 1
                        break
            except:
                pass
            print(f"\n❌ Result doesn't match expected statistical summary")
            if attempts < max_attempts:
                print("💡 Think about how to get summary statistics for numeric columns")
            else:
                print("\n" + "="*60)
                print("📖 CORRECT ANSWER:")
                print("="*60)
                print("df.describe()")
                print("\n💡 Explanation: The describe() method provides descriptive statistics")
                break
        
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
                
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error: {error}")
                    print("💡 Fix the error and try again")
                    if attempts >= max_attempts:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df['{col1}'].corr(df['{col2}'])")
                        print("\n💡 Explanation: corr() method on a Series calculates correlation with another Series")
                        break
                    continue
                
                print(f"\n📊 Result: {result}")
                
                # Validate correlation value
                try:
                    expected = df[col1].corr(df[col2])
                    if isinstance(result, (int, float)):
                        if abs(result - expected) < 0.0001:
                            print(f"\n✅ Correct! The correlation between '{col1}' and '{col2}' is {result:.4f}")
                            task7_completed = True
                            tasks_completed += 1
                            break
                        else:
                            print(f"\n❌ Expected correlation around {expected:.4f}, got {result:.4f}")
                    else:
                        print(f"\n❌ Result should be a number (correlation value), got {type(result).__name__}")
                    
                    if attempts < max_attempts:
                        print("💡 Think about how to calculate correlation between two Series")
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df['{col1}'].corr(df['{col2}'])")
                        print("\n💡 Explanation: corr() method on a Series calculates correlation with another Series")
                        break
                except Exception as e:
                    print(f"\n❌ Error validating: {str(e)}")
                    if attempts < max_attempts:
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df['{col1}'].corr(df['{col2}'])")
                        print("\n💡 Explanation: corr() method on a Series calculates correlation with another Series")
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
                
                result, error = self.execute_pandas_code(df, code, include_plotting=True)
                if error:
                    print(f"❌ Error: {error}")
                    print("💡 Fix the error and try again")
                    if attempts >= max_attempts:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df.plot(x='{col1}', y='{col2}', kind='scatter')")
                        print("\n💡 Explanation: plot() with kind='scatter' creates a scatter plot")
                        break
                    continue
                
                # Check if code contains plotting keywords
                code_lower = code.lower()
                has_plot = 'plot' in code_lower or 'scatter' in code_lower or 'plt.' in code_lower
                
                if has_plot and error is None:
                    print(f"\n✅ Correct! You created a scatter plot of '{col1}' vs '{col2}'!")
                    print("💡 Plot created successfully (running in non-interactive mode)")
                    task8_completed = True
                    tasks_completed += 1
                    break
                else:
                    print(f"\n❌ Your code should create a scatter plot")
                    if attempts < max_attempts:
                        print(f"💡 Think about how to visualize two columns as points on a graph")
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df.plot(x='{col1}', y='{col2}', kind='scatter')")
                        print("\n💡 Explanation: plot() with kind='scatter' creates a scatter plot")
                        break
        
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
            
            result, error = self.execute_pandas_code(df, code)
            if error:
                print(f"❌ Error: {error}")
                print("💡 Fix the error and try again")
                if attempts >= max_attempts:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df[df['{numeric_col}'] > {threshold:.2f}]")
                    print("\n💡 Explanation: Boolean indexing filters rows where the condition is True")
                    break
                continue
            
            if not hasattr(result, '__len__') or not hasattr(result, 'shape'):
                print("❌ Result is not a DataFrame")
                print("💡 Your code should return a filtered DataFrame")
                if attempts < max_attempts:
                    print("💡 Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df[df['{numeric_col}'] > {threshold:.2f}]")
                    print("\n💡 Explanation: Boolean indexing filters rows where the condition is True")
                    break
                continue
            
            print(f"\n📊 Filtered {len(result)} rows:")
            print(result.head(10) if len(result) > 0 else result)
            is_valid, message = self.validate_filter_greater_than(result, df, numeric_col, threshold)
            if is_valid:
                print(f"\n✅ {message}")
                task1_completed = True
                tasks_completed += 1
                break
            else:
                print(f"\n❌ {message}")
                if attempts < max_attempts:
                    print(f"💡 Your answer is not correct. Make sure you're filtering where {numeric_col} > {threshold:.2f}")
                    print("💡 Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df[df['{numeric_col}'] > {threshold:.2f}]")
                    print("\n💡 Explanation: Boolean indexing filters rows where the condition is True")
                    break
        
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
            
            result, error = self.execute_pandas_code(df, code)
            if error:
                print(f"❌ Error: {error}")
                print("💡 Fix the error and try again")
                if attempts >= max_attempts:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df[df['{categorical_col}'] == '{category_choice}']")
                    print("\n💡 Explanation: Use boolean indexing with == to filter for exact matches")
                    break
                continue
            
            if not hasattr(result, '__len__') or not hasattr(result, 'shape'):
                print("❌ Result is not a DataFrame")
                print("💡 Your code should return a filtered DataFrame")
                if attempts >= max_attempts:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df[df['{categorical_col}'] == '{category_choice}']")
                    print("\n💡 Explanation: Use boolean indexing with == to filter for exact matches")
                    break
                continue
            
            print(f"\n📊 Filtered {len(result)} rows:")
            print(result.head(10))
            
            # Validate that all rows have the selected value
            if categorical_col not in result.columns:
                print(f"\n❌ Result doesn't have '{categorical_col}' column")
                print("💡 Make sure you're filtering the original dataframe")
                if attempts < max_attempts:
                    print("💡 Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df[df['{categorical_col}'] == '{category_choice}']")
                    print("\n💡 Explanation: Use boolean indexing with == to filter for exact matches")
                    break
                continue
            
            if len(result) != expected_count:
                print(f"\n❌ Expected {expected_count} rows with {categorical_col} == '{category_choice}', got {len(result)}")
                print("💡 Check your filter condition")
                if attempts < max_attempts:
                    print("💡 Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df[df['{categorical_col}'] == '{category_choice}']")
                    print("\n💡 Explanation: Use boolean indexing with == to filter for exact matches")
                    break
                continue
            
            if not (result[categorical_col] == category_choice).all():
                invalid = (result[categorical_col] != category_choice).sum()
                print(f"\n❌ {invalid} rows don't have {categorical_col} == '{category_choice}'")
                print("💡 Make sure your filter condition is correct")
                if attempts < max_attempts:
                    print("💡 Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df[df['{categorical_col}'] == '{category_choice}']")
                    print("\n💡 Explanation: Use boolean indexing with == to filter for exact matches")
                    break
                continue
            
            # Verify we have the right rows
            result_indices = set(result.index)
            expected_indices = set(expected.index)
            if result_indices == expected_indices:
                print(f"\n✅ Correct! All {len(result)} rows have {categorical_col} == '{category_choice}'")
                task2_completed = True
                tasks_completed += 1
                break
            else:
                print(f"\n❌ Row indices don't match expected result")
                if attempts < max_attempts:
                    print("💡 You might have the right filter but wrong rows")
                    continue
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df[df['{categorical_col}'] == '{category_choice}']")
                    print("\n💡 Explanation: Use boolean indexing with == to filter for exact matches")
                    break
        
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
            
            result, error = self.execute_pandas_code(df, code)
            if error:
                print(f"❌ Error: {error}")
                print("💡 Fix the error and try again")
                if attempts >= max_attempts:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df[df['{numeric_col}'] > {threshold:.2f}]")
                    print("\n💡 Explanation: Boolean indexing filters rows where the condition is True")
                    break
                continue
            
            if not hasattr(result, 'shape'):
                print("❌ Result is not a DataFrame")
                if attempts >= max_attempts:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df[df['{numeric_col2}'] < {threshold2:.2f}]")
                    print("\n💡 Explanation: Use < for less than comparison")
                    break
                continue
            
            print(f"\n📊 Filtered {len(result)} rows:")
            print(result.head(10) if len(result) > 0 else result)
            expected = df[df[numeric_col2] < threshold2]
            if len(result) == len(expected) and len(result) > 0:
                if (result[numeric_col2] < threshold2).all():
                    print(f"\n✅ Correct! Filtered rows where {numeric_col2} < {threshold2:.2f}")
                    task3_completed = True
                    tasks_completed += 1
                    break
            print(f"\n❌ Expected {len(expected)} rows where {numeric_col2} < {threshold2:.2f}")
            if attempts < max_attempts:
                print("💡 Try again.")
            else:
                print("\n" + "="*60)
                print("📖 CORRECT ANSWER:")
                print("="*60)
                print(f"df[df['{numeric_col2}'] < {threshold2:.2f}]")
                print("\n💡 Explanation: Use < for less than comparison")
                break
        
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
            
            result, error = self.execute_pandas_code(df, code)
            if error:
                print(f"❌ Error: {error}")
                print("💡 Fix the error and try again")
                if attempts >= max_attempts:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df[df['{numeric_col}'] > {threshold:.2f}]")
                    print("\n💡 Explanation: Boolean indexing filters rows where the condition is True")
                    break
                continue
            
            if not hasattr(result, 'shape'):
                print("❌ Result is not a DataFrame")
                if attempts >= max_attempts:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df[df['{numeric_col}'] >= {threshold3:.2f}]")
                    print("\n💡 Explanation: Use >= for greater than or equal comparison")
                    break
                continue
            
            print(f"\n📊 Filtered {len(result)} rows:")
            print(result.head(10) if len(result) > 0 else result)
            expected = df[df[numeric_col] >= threshold3]
            if len(result) == len(expected) and len(result) > 0:
                if (result[numeric_col] >= threshold3).all():
                    print(f"\n✅ Correct! Filtered rows where {numeric_col} >= {threshold3:.2f}")
                    task4_completed = True
                    tasks_completed += 1
                    break
            print(f"\n❌ Expected {len(expected)} rows where {numeric_col} >= {threshold3:.2f}")
            if attempts < max_attempts:
                print("💡 Try again.")
            else:
                print("\n" + "="*60)
                print("📖 CORRECT ANSWER:")
                print("="*60)
                print(f"df[df['{numeric_col}'] >= {threshold3:.2f}]")
                print("\n💡 Explanation: Use >= for greater than or equal comparison")
                break
        
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
            
            result, error = self.execute_pandas_code(df, code)
            if error:
                print(f"❌ Error: {error}")
                print("💡 Fix the error and try again")
                if attempts >= max_attempts:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df[(df['{numeric_col}'] > {threshold4:.2f}) & (df['{numeric_col3}'] > {threshold5:.2f})]")
                    print("\n💡 Explanation: Use & for AND, each condition must be in parentheses")
                    break
                continue
            
            if not hasattr(result, 'shape'):
                print("❌ Result is not a DataFrame")
                if attempts >= max_attempts:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df[(df['{numeric_col}'] > {threshold4:.2f}) & (df['{numeric_col3}'] > {threshold5:.2f})]")
                    print("\n💡 Explanation: Use & for AND, each condition must be in parentheses")
                    break
                continue
            
            print(f"\n📊 Filtered {len(result)} rows:")
            print(result.head(10) if len(result) > 0 else result)
            expected = df[(df[numeric_col] > threshold4) & (df[numeric_col3] > threshold5)]
            if len(result) == len(expected):
                if len(result) == 0 or ((result[numeric_col] > threshold4).all() and (result[numeric_col3] > threshold5).all()):
                    print(f"\n✅ Correct! Filtered rows with both conditions")
                    task5_completed = True
                    tasks_completed += 1
                    break
            print(f"\n❌ Expected {len(expected)} rows matching both conditions")
            if attempts < max_attempts:
                print("💡 Remember: Use & for AND, and put each condition in parentheses")
            else:
                print("\n" + "="*60)
                print("📖 CORRECT ANSWER:")
                print("="*60)
                print(f"df[(df['{numeric_col}'] > {threshold4:.2f}) & (df['{numeric_col3}'] > {threshold5:.2f})]")
                print("\n💡 Explanation: Use & for AND, each condition must be in parentheses")
                break
        
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
                    
                    result, error = self.execute_pandas_code(df, code)
                    if error:
                        print(f"❌ Error: {error}")
                        print("💡 Fix the error and try again")
                        if attempts >= max_attempts:
                            print("\n" + "="*60)
                            print("📖 CORRECT ANSWER:")
                            print("="*60)
                            print(f"df[df['{categorical_col}'].isin({selected_values})]")
                            print("\n💡 Explanation: isin() checks if values are in a list")
                            break
                        continue
                    
                    if not hasattr(result, 'shape'):
                        print("❌ Result is not a DataFrame")
                        if attempts >= max_attempts:
                            print("\n" + "="*60)
                            print("📖 CORRECT ANSWER:")
                            print("="*60)
                            print(f"df[df['{categorical_col}'].isin({selected_values})]")
                            print("\n💡 Explanation: isin() checks if values are in a list")
                            break
                        continue
                    
                    print(f"\n📊 Filtered {len(result)} rows:")
                    print(result.head(10) if len(result) > 0 else result)
                    expected = df[df[categorical_col].isin(selected_values)]
                    
                    # Verify result matches expected
                    if len(result) == len(expected):
                        if len(result) == 0:
                            # Empty result is correct if expected is also empty
                            print(f"\n✅ Correct! Filtered rows where {categorical_col} is in the specified values")
                            task6_completed = True
                            tasks_completed += 1
                            break
                        else:
                            # Check that all values in result are in selected_values
                            result_values_in_list = result[categorical_col].isin(selected_values)
                            if result_values_in_list.all():
                                # Verify we have the correct rows
                                # Compare indices first (fastest check for exact match)
                                result_indices = set(result.index)
                                expected_indices = set(expected.index)
                                if result_indices == expected_indices:
                                    # Perfect match - indices and data both correct
                                    print(f"\n✅ Correct! Filtered rows where {categorical_col} is in the specified values")
                                    task6_completed = True
                                    tasks_completed += 1
                                    break
                                else:
                                    # Indices don't match - check if categorical column values match
                                    # This handles cases where user resets index or reorders rows
                                    result_cat_values = set(result[categorical_col].values)
                                    expected_cat_values = set(expected[categorical_col].values)
                                    
                                    if result_cat_values == expected_cat_values:
                                        # Categorical values match - data is correct even if indices differ
                                        print(f"\n✅ Correct! Filtered rows where {categorical_col} is in the specified values")
                                        task6_completed = True
                                        tasks_completed += 1
                                        break
                                    else:
                                        # Check if all expected values are present (even if count differs due to duplicates)
                                        # This handles cases where user might have duplicates or different ordering
                                        if len(result_cat_values) >= len(expected_cat_values) and expected_cat_values.issubset(result_cat_values):
                                            # All expected values are present
                                            print(f"\n✅ Correct! Filtered rows where {categorical_col} is in the specified values")
                                            task6_completed = True
                                            tasks_completed += 1
                                            break
                                        # Values don't match - incorrect result
                                        print(f"\n❌ The filtered rows don't match the expected result")
                                        if attempts < max_attempts:
                                            print("💡 Make sure you're filtering correctly")
                                            print("💡 Try again.")
                                            continue
                                        else:
                                            print("\n" + "="*60)
                                            print("📖 CORRECT ANSWER:")
                                            print("="*60)
                                            print(f"df[df['{categorical_col}'].isin({selected_values})]")
                                            print("\n💡 Explanation: isin() checks if values are in a list")
                                            break
                            else:
                                invalid_count = (~result_values_in_list).sum()
                                print(f"\n❌ {invalid_count} rows in result don't match the filter criteria")
                                if attempts < max_attempts:
                                    print("💡 Make sure all filtered rows have values in the specified list")
                                    print("💡 Try again.")
                                    continue
                                else:
                                    print("\n" + "="*60)
                                    print("📖 CORRECT ANSWER:")
                                    print("="*60)
                                    print(f"df[df['{categorical_col}'].isin({selected_values})]")
                                    print("\n💡 Explanation: isin() checks if values are in a list")
                                    break
                    else:
                        # Check if all values in result are correct, even if count differs
                        result_values_in_list = result[categorical_col].isin(selected_values)
                        if result_values_in_list.all() and len(result) > 0:
                            # All values are correct, might be a subset or have duplicates
                            result_cat_values = set(result[categorical_col].values)
                            expected_cat_values = set(expected[categorical_col].values)
                            if expected_cat_values.issubset(result_cat_values) or result_cat_values == expected_cat_values:
                                print(f"\n✅ Correct! Filtered rows where {categorical_col} is in the specified values")
                                task6_completed = True
                                tasks_completed += 1
                                break
                    
                    print(f"\n❌ Expected {len(expected)} rows matching the values")
                    if attempts < max_attempts:
                        print("💡 Think about how to check if a value is in a list")
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        values_str = str(selected_values).replace("'", "'")
                        print(f"df[df['{categorical_col}'].isin({selected_values})]")
                        print("\n💡 Explanation: isin() checks if values are in a list")
                        break
        
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
                
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error: {error}")
                    print("💡 Fix the error and try again")
                    if attempts >= max_attempts:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df['{col1}'].corr(df['{col2}'])")
                        print("\n💡 Explanation: corr() method on a Series calculates correlation with another Series")
                        break
                    continue
            
                print(f"\n📊 Result: {result}")
                
                # Validate correlation value
                try:
                    expected = df[col1].corr(df[col2])
                    if isinstance(result, (int, float)):
                        if abs(result - expected) < 0.0001:
                            print(f"\n✅ Correct! The correlation between '{col1}' and '{col2}' is {result:.4f}")
                            task5_completed = True
                            tasks_completed += 1
                            break
                        else:
                            print(f"\n❌ Expected correlation {expected:.4f}, got {result:.4f}")
                    else:
                        print(f"\n❌ Result should be a number (correlation coefficient), got {type(result).__name__}")
                    
                    if attempts < max_attempts:
                        print(f"💡 Think about how to calculate correlation between two Series")
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df['{col1}'].corr(df['{col2}'])")
                        print("\n💡 Explanation: corr() method on a Series calculates correlation with another Series")
                        break
                except Exception as e:
                    print(f"\n❌ Error validating: {str(e)}")
                    if attempts >= max_attempts:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df['{col1}'].corr(df['{col2}'])")
                        print("\n💡 Explanation: corr() method on a Series calculates correlation with another Series")
                        break
                    print("💡 Try again.")
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
                
                result, error = self.execute_pandas_code(df, code, include_plotting=True)
                if error:
                    print(f"❌ Error: {error}")
                    print("💡 Fix the error and try again")
                    if attempts >= max_attempts:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df['{col}'].plot(kind='box')")
                        print("\n💡 Explanation: plot() with kind='box' creates a box plot")
                        break
                    continue
                
                # Check if code contains plotting keywords
                code_lower = code.lower()
                has_plot = 'plot' in code_lower or 'box' in code_lower or 'plt.' in code_lower or 'seaborn' in code_lower or 'matplotlib' in code_lower
                
                # Check if column is referenced - be very flexible
                # Allow various ways to reference the column
                has_col = (
                    f"'{col}'" in code or 
                    f'"{col}"' in code or 
                    f"['{col}']" in code or
                    f'["{col}"]' in code or
                    f"[{col}]" in code or
                    f".{col}" in code or
                    f".{col}[" in code or
                    # Also check if result contains the column (for cases like df.iloc[:, 0])
                    (hasattr(result, 'columns') and col in result.columns) or
                    (hasattr(result, 'name') and result.name == col) or
                    # Check for iloc/iat references that might reference the column
                    ('iloc' in code_lower and 'df' in code_lower)
                )
                
                # For plotting tasks, the result might be None or an Axes object
                # If there's no error and plotting code is present, it's likely correct
                if has_plot and error is None:
                    # If plotting code is present and no error, accept it
                    # Column reference check is optional for plotting (user might use iloc or other methods)
                    if has_col or 'df' in code_lower:
                        print(f"\n✅ Correct! You created a box plot of '{col}'!")
                        print("💡 Plot created successfully (running in non-interactive mode)")
                        task6_completed = True
                        tasks_completed += 1
                        break
                
                print(f"\n❌ Your code should create a box plot of '{col}'")
                if attempts < max_attempts:
                    print(f"💡 Think about how to visualize distribution and outliers")
                    print("💡 Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df['{col}'].plot(kind='box')")
                    print("\n💡 Explanation: plot() with kind='box' creates a box plot")
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
            
            result, error = self.execute_pandas_code(df, code)
            if error:
                print(f"❌ Error: {error}")
                print("💡 Fix the error and try again")
                if attempts >= max_attempts:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df.sort_values('{sort_col}', ascending={ascending})")
                    print(f"\n💡 Explanation: sort_values() sorts by a column, ascending={ascending} for {order_text}")
                    break
                continue
            
            if not hasattr(result, 'shape'):
                print("❌ Result is not a DataFrame")
                print("💡 Your code should return a sorted DataFrame")
                if attempts >= max_attempts:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df.sort_values('{sort_col}', ascending={ascending})")
                    print(f"\n💡 Explanation: sort_values() sorts by a column, ascending={ascending} for {order_text}")
                    break
                continue
            
            print(f"\n📊 Result (first 10 rows):")
            print(result.head(10))
            
            # Validate sorting
            expected = df.sort_values(sort_col, ascending=ascending).reset_index(drop=True)
            try:
                result_reset = result.reset_index(drop=True)
                # Check if first row matches expected (handle NaN values)
                first_val_result = result_reset.iloc[0][sort_col]
                first_val_expected = expected.iloc[0][sort_col]
                first_matches = False
                if pd.isna(first_val_result) and pd.isna(first_val_expected):
                    first_matches = True
                elif not pd.isna(first_val_result) and not pd.isna(first_val_expected):
                    first_matches = abs(first_val_result - first_val_expected) < 0.01
                
                # Check if last row matches expected (handle NaN values)
                last_val_result = result_reset.iloc[-1][sort_col]
                last_val_expected = expected.iloc[-1][sort_col]
                last_matches = False
                if pd.isna(last_val_result) and pd.isna(last_val_expected):
                    last_matches = True
                elif not pd.isna(last_val_result) and not pd.isna(last_val_expected):
                    last_matches = abs(last_val_result - last_val_expected) < 0.01
                
                if first_matches and last_matches:
                    # Check if all rows are in correct order
                    if len(result_reset) > 1:
                        diffs = result_reset[sort_col].diff().dropna()
                        if len(diffs) > 0:  # Only check if there are non-NaN differences
                            if ascending:
                                if (diffs >= -0.01).all():  # Ascending: each value >= previous
                                    print(f"\n✅ Correct! Data is sorted by {sort_col} in {order_text} order!")
                                    task1_completed = True
                                    tasks_completed += 1
                                    break
                            else:
                                if (diffs <= 0.01).all():  # Descending: each value <= previous
                                    print(f"\n✅ Correct! Data is sorted by {sort_col} in {order_text} order!")
                                    task1_completed = True
                                    tasks_completed += 1
                                    break
                        else:
                            # All values are NaN or only one non-NaN value
                            print(f"\n✅ Correct! Data is sorted by {sort_col} in {order_text} order!")
                            task1_completed = True
                            tasks_completed += 1
                            break
                    else:
                        print("\n✅ Correct! Data is sorted!")
                        task1_completed = True
                        tasks_completed += 1
                        break
                
                print(f"\n❌ Data is not sorted correctly by {sort_col} in {order_text} order")
                if attempts < max_attempts:
                    print(f"💡 Make sure you're sorting by '{sort_col}' with ascending={ascending}")
                    print("💡 Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df.sort_values('{sort_col}', ascending={ascending})")
                    print(f"\n💡 Explanation: sort_values() sorts by a column, ascending={ascending} for {order_text}")
                    break
            except Exception as e:
                print(f"\n❌ Error validating: {str(e)}")
                if attempts >= max_attempts:
                    break
                print("💡 Try again.")
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
            
            result, error = self.execute_pandas_code(df, code)
            if error:
                print(f"❌ Error: {error}")
                print("💡 Fix the error and try again")
                if attempts >= max_attempts:
                    cols_str = "', '".join(expected_cols)
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df[['{cols_str}']]")
                    print("\n💡 Explanation: Use double brackets to select multiple columns")
                    break
                continue
            
            if not hasattr(result, 'shape'):
                print("❌ Result is not a DataFrame")
                print("💡 Your code should return a DataFrame with selected columns")
                if attempts >= max_attempts:
                    cols_str = "', '".join(expected_cols)
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df[['{cols_str}']]")
                    print("\n💡 Explanation: Use double brackets to select multiple columns")
                    break
                continue
            
            print(f"\n📊 Result (first 5 rows):")
            print(result.head(5))
            
            # Validate column selection
            try:
                result_cols = list(result.columns)
                if set(result_cols) == set(expected_cols) and len(result_cols) == len(expected_cols):
                    if result.shape[0] == df.shape[0]:
                        print("\n✅ Correct! You selected the right columns!")
                        task2_completed = True
                        tasks_completed += 1
                        break
                    else:
                        print("\n❌ Row count doesn't match - you might have filtered the data")
                        if attempts >= max_attempts:
                            break
                        continue
                else:
                    missing = set(expected_cols) - set(result_cols)
                    extra = set(result_cols) - set(expected_cols)
                    if missing:
                        print(f"\n❌ Missing columns: {missing}")
                    if extra:
                        print(f"\n❌ Extra columns: {extra}")
                    if attempts < max_attempts:
                        print(f"💡 Make sure you select exactly: {expected_cols}")
                        print("💡 Try again.")
                    else:
                        cols_str = "', '".join(expected_cols)
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df[['{cols_str}']]")
                        print("\n💡 Explanation: Use double brackets to select multiple columns")
                        break
            except Exception as e:
                print(f"\n❌ Error validating: {str(e)}")
                if attempts >= max_attempts:
                    break
                print("💡 Try again.")
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
            
            result, error = self.execute_pandas_code(df, code)
            if error:
                print(f"❌ Error: {error}")
                print("💡 Fix the error and try again")
                if attempts >= max_attempts:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df['{single_col}']")
                    print("\n💡 Explanation: Single brackets return a Series for one column")
                    break
                continue
            
            print(f"\n📊 Result (first 10 values):")
            print(result.head(10) if hasattr(result, 'head') else result[:10] if hasattr(result, '__getitem__') else result)
            
            try:
                expected = df[single_col]
                if hasattr(result, 'equals'):
                    if result.equals(expected):
                        print("\n✅ Correct! You selected the column correctly!")
                        task3_completed = True
                        tasks_completed += 1
                        break
                elif hasattr(result, 'values') and hasattr(result, 'index'):
                    if len(result) == len(expected) and all(result.values == expected.values):
                        print("\n✅ Correct! You selected the column correctly!")
                        task3_completed = True
                        tasks_completed += 1
                        break
            except:
                pass
            
            print(f"\n❌ Result doesn't match expected column selection")
            if attempts < max_attempts:
                print(f"💡 Make sure you select the '{single_col}' column using single brackets")
            else:
                print("\n" + "="*60)
                print("📖 CORRECT ANSWER:")
                print("="*60)
                print(f"df['{single_col}']")
                print("\n💡 Explanation: Single brackets return a Series for one column")
                break
        
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
                
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error: {error}")
                    print("💡 Fix the error and try again")
                    if attempts >= max_attempts:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df.sort_values(by=['{sort_col1}', '{sort_col2}'], ascending=[True, False])")
                        print("\n💡 Explanation: Pass a list of columns and a list of boolean values for ascending")
                        break
                    continue
                
                if not hasattr(result, 'shape'):
                    print("❌ Result is not a DataFrame")
                    if attempts >= max_attempts:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df.sort_values(by=['{sort_col1}', '{sort_col2}'], ascending=[True, False])")
                        print("\n💡 Explanation: Pass a list of columns and a list of boolean values for ascending")
                        break
                    continue
                
                print(f"\n📊 Result (first 10 rows):")
                print(result.head(10))
                
                try:
                    expected = df.sort_values(by=[sort_col1, sort_col2], ascending=[True, False]).reset_index(drop=True)
                    result_reset = result.reset_index(drop=True)
                    if len(result_reset) == len(expected):
                        # Check first few rows match
                        if result_reset.iloc[0][sort_col1] == expected.iloc[0][sort_col1]:
                            print("\n✅ Correct! Data is sorted by multiple columns!")
                            task4_completed = True
                            tasks_completed += 1
                            break
                except:
                    pass
                
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
            
            result, error = self.execute_pandas_code(df, code)
            if error:
                print(f"❌ Error: {error}")
                print("💡 Fix the error and try again")
                if attempts >= max_attempts:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df.iloc[:{n_rows_iloc}]")
                    print("\n💡 Explanation: iloc uses integer positions, [:n] selects first n rows")
                    break
                continue
            
            if not hasattr(result, 'shape'):
                print("❌ Result is not a DataFrame")
                if attempts >= max_attempts:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df.iloc[:{n_rows_iloc}]")
                    print("\n💡 Explanation: iloc uses integer positions, [:n] selects first n rows")
                    break
                continue
            
            print(f"\n📊 Result:")
            print(result)
            
            try:
                expected = df.iloc[:n_rows_iloc]
                if len(result) == len(expected) and result.shape[1] == expected.shape[1]:
                    if result.reset_index(drop=True).equals(expected.reset_index(drop=True)):
                        print("\n✅ Correct! You selected rows using iloc!")
                        task5_completed = True
                        tasks_completed += 1
                        break
            except:
                pass
            
            print(f"\n❌ Expected {n_rows_iloc} rows")
            if attempts < max_attempts:
                print(f"💡 Use iloc[:{n_rows_iloc}] to select first {n_rows_iloc} rows")
            else:
                print("\n" + "="*60)
                print("📖 CORRECT ANSWER:")
                print("="*60)
                print(f"df.iloc[:{n_rows_iloc}]")
                print("\n💡 Explanation: iloc uses integer positions, [:n] selects first n rows")
                break
        
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
            
            result, error = self.execute_pandas_code(df, code)
            if error:
                print(f"❌ Error: {error}")
                print("💡 Fix the error and try again")
                if attempts >= max_attempts:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df.iloc[:{n_rows_select}, :{n_cols_select}]")
                    print("\n💡 Explanation: iloc[rows, columns] selects both rows and columns by position")
                    break
                continue
            
            if not hasattr(result, 'shape'):
                print("❌ Result is not a DataFrame")
                if attempts >= max_attempts:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df.iloc[:{n_rows_select}, :{n_cols_select}]")
                    print("\n💡 Explanation: iloc[rows, columns] selects both rows and columns by position")
                    break
                continue
            
            print(f"\n📊 Result:")
            print(result)
            
            try:
                expected = df.iloc[:n_rows_select, :n_cols_select]
                if result.shape == expected.shape:
                    if result.reset_index(drop=True).equals(expected.reset_index(drop=True)):
                        print("\n✅ Correct! You selected rows and columns using iloc!")
                        task6_completed = True
                        tasks_completed += 1
                        break
            except:
                pass
            
            print(f"\n❌ Expected {n_rows_select} rows and {n_cols_select} columns")
            if attempts < max_attempts:
                print(f"💡 Use iloc[:{n_rows_select}, :{n_cols_select}]")
            else:
                print("\n" + "="*60)
                print("📖 CORRECT ANSWER:")
                print("="*60)
                print(f"df.iloc[:{n_rows_select}, :{n_cols_select}]")
                print("\n💡 Explanation: iloc[rows, columns] selects both rows and columns by position")
                break
        
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
                
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error: {error}")
                    print("💡 Fix the error and try again")
                    if attempts >= max_attempts:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print("df.select_dtypes(include=['int64', 'float64'])")
                        print("\n💡 Explanation: select_dtypes() filters columns by data type")
                        break
                    continue
                
                if not hasattr(result, 'shape'):
                    print("❌ Result is not a DataFrame")
                    if attempts >= max_attempts:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print("df.select_dtypes(include=['int64', 'float64'])")
                        print("\n💡 Explanation: select_dtypes() filters columns by data type")
                        break
                    continue
                
                print(f"\n📊 Result (first 5 rows):")
                print(result.head(5))
                
                try:
                    expected = df.select_dtypes(include=['int64', 'float64'])
                    if set(result.columns) == set(expected.columns) and len(result.columns) == len(expected.columns):
                        if result.shape[0] == df.shape[0]:
                            print("\n✅ Correct! You selected numeric columns!")
                            task7_completed = True
                            tasks_completed += 1
                            break
                except:
                    pass
                
                print(f"\n❌ Result doesn't match expected numeric columns")
                if attempts < max_attempts:
                    print("💡 Use select_dtypes(include=['int64', 'float64'])")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print("df.select_dtypes(include=['int64', 'float64'])")
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
                
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error: {error}")
                    print("💡 Fix the error and try again")
                    if attempts >= max_attempts:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df.sort_values('{sort_col3}', ascending=False).head({n_top})")
                        print("\n💡 Explanation: Chain sort_values() and head() methods")
                        break
                    continue
                
                if not hasattr(result, 'shape'):
                    print("❌ Result is not a DataFrame")
                    if attempts >= max_attempts:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df.sort_values('{sort_col3}', ascending=False).head({n_top})")
                        print("\n💡 Explanation: Chain sort_values() and head() methods")
                        break
                    continue
                
                print(f"\n📊 Result:")
                print(result)
                
                try:
                    expected = df.sort_values(sort_col3, ascending=False).head(n_top).reset_index(drop=True)
                    result_reset = result.reset_index(drop=True)
                    if result_reset.shape == expected.shape:
                        if abs(result_reset.iloc[0][sort_col3] - expected.iloc[0][sort_col3]) < 0.01:
                            print(f"\n✅ Correct! You got the top {n_top} rows sorted by {sort_col3}!")
                            task8_completed = True
                            tasks_completed += 1
                            break
                except:
                    pass
                
                print(f"\n❌ Expected top {n_top} rows sorted by {sort_col3} descending")
                if attempts < max_attempts:
                    print(f"💡 Sort by '{sort_col3}' descending, then use head({n_top})")
                else:
                    print("\n" + "="*60)
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
        correct_answer = f"df.rename(columns={{'{col_to_rename}': '{new_name}'}})"
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
            
            result, error = self.execute_pandas_code(df, code)
            if error:
                print(f"❌ Error: {error}")
                print("💡 Fix the error and try again")
                if attempts >= max_attempts:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df.rename(columns={{'{col_to_rename}': '{new_name}'}})")
                    print("\n💡 Explanation: rename() with columns parameter renames specific columns")
                    break
                continue
            
            if not hasattr(result, 'shape'):
                print("❌ Result is not a DataFrame")
                print("💡 Your code should return a DataFrame with renamed column")
                if attempts >= max_attempts:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df.rename(columns={{'{col_to_rename}': '{new_name}'}})")
                    print("\n💡 Explanation: rename() with columns parameter renames specific columns")
                    break
                continue
            
            print(f"\n📊 Result columns:")
            print(list(result.columns))
            
            # Validate column rename
            try:
                if new_name in result.columns and col_to_rename not in result.columns:
                    if result.shape[0] == df.shape[0] and result.shape[1] == df.shape[1]:
                        print(f"\n✅ Correct! Column '{col_to_rename}' was renamed to '{new_name}'!")
                        task1_completed = True
                        tasks_completed += 1
                        break
                    else:
                        print("\n❌ Row or column count changed - you might have done something else")
                        if attempts >= max_attempts:
                            print("\n" + "="*60)
                            print("📖 CORRECT ANSWER:")
                            print("="*60)
                            print(f"df.rename(columns={{'{col_to_rename}': '{new_name}'}})")
                            print("\n💡 Explanation: rename() with columns parameter renames specific columns")
                            break
                        continue
                else:
                    if new_name not in result.columns:
                        print(f"\n❌ Column '{new_name}' not found in result")
                    if col_to_rename in result.columns:
                        print(f"\n❌ Column '{col_to_rename}' still exists - it wasn't renamed")
                    if attempts < max_attempts:
                        print(f"💡 Make sure you rename '{col_to_rename}' to '{new_name}'")
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df.rename(columns={{'{col_to_rename}': '{new_name}'}})")
                        print("\n💡 Explanation: rename() with columns parameter renames specific columns")
                        break
            except Exception as e:
                print(f"\n❌ Error validating: {str(e)}")
                if attempts < max_attempts:
                    print("💡 Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df.rename(columns={{'{col_to_rename}': '{new_name}'}})")
                    print("\n💡 Explanation: rename() with columns parameter renames specific columns")
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
            
            # Store original df state before execution
            df_before = df.copy()
            
            result, error = self.execute_pandas_code(df, code)
            if error:
                print(f"❌ Error: {error}")
                print("💡 Fix the error and try again")
                if attempts >= max_attempts:
                    # Determine correct answer based on operation
                    if operation == 'divide':
                        expected_code = f"df['{new_col_name}'] = df['{col1}'] / df['{col2}']"
                    elif operation == 'multiply':
                        expected_code = f"df['{new_col_name}'] = df['{col1}'] * df['{col2}']"
                    elif operation == 'add':
                        expected_code = f"df['{new_col_name}'] = df['{col1}'] + df['{col2}']"
                    else:  # subtract
                        expected_code = f"df['{new_col_name}'] = df['{col1}'] - df['{col2}']"
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(expected_code)
                    print(f"\n💡 Explanation: Create new columns by assigning calculated values ({operation})")
                    break
                continue
            
            # Handle in-place modifications: if result is None, check df directly
            # Also handle case where result is a DataFrame (returned from expression)
            df_to_check = df if result is None or not hasattr(result, 'shape') else result
            
            if not hasattr(df_to_check, 'shape'):
                print("❌ Result is not a DataFrame")
                print("💡 Your code should create a new column in the dataframe")
                if attempts >= max_attempts:
                    # Determine correct answer based on operation
                    if operation == 'divide':
                        expected_code = f"df['{new_col_name}'] = df['{col1}'] / df['{col2}']"
                    elif operation == 'multiply':
                        expected_code = f"df['{new_col_name}'] = df['{col1}'] * df['{col2}']"
                    elif operation == 'add':
                        expected_code = f"df['{new_col_name}'] = df['{col1}'] + df['{col2}']"
                    else:  # subtract
                        expected_code = f"df['{new_col_name}'] = df['{col1}'] - df['{col2}']"
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(expected_code)
                    print(f"\n💡 Explanation: Create new columns by assigning calculated values ({operation})")
                    break
                continue
            
            print(f"\n📊 Result (first 5 rows, showing relevant columns):")
            if new_col_name in df_to_check.columns:
                if col1 in df_to_check.columns and col2 in df_to_check.columns:
                    print(df_to_check[[col1, col2, new_col_name]].head(5))
                else:
                    print(df_to_check.head(5))
            else:
                print(df_to_check.head(5))
            
            # Validate new column creation
            try:
                if new_col_name in df_to_check.columns:
                    # Calculate expected values based on operation using original df
                    if operation == 'divide':
                        expected_values = df_before[col1] / df_before[col2]
                        expected_code = f"df['{new_col_name}'] = df['{col1}'] / df['{col2}']"
                    elif operation == 'multiply':
                        expected_values = df_before[col1] * df_before[col2]
                        expected_code = f"df['{new_col_name}'] = df['{col1}'] * df['{col2}']"
                    elif operation == 'add':
                        expected_values = df_before[col1] + df_before[col2]
                        expected_code = f"df['{new_col_name}'] = df['{col1}'] + df['{col2}']"
                    else:  # subtract
                        expected_values = df_before[col1] - df_before[col2]
                        expected_code = f"df['{new_col_name}'] = df['{col1}'] - df['{col2}']"
                    
                    # Compare values - handle index alignment issues
                    result_col = df_to_check[new_col_name]
                    # Align indices for comparison
                    if len(result_col) == len(expected_values):
                        # Try direct comparison first
                        try:
                            diff = (result_col.values - expected_values.values).abs()
                            if diff.max() < 0.01:
                                print(f"\n✅ Correct! New column '{new_col_name}' created correctly!")
                                task2_completed = True
                                tasks_completed += 1
                                break
                        except:
                            # If direct comparison fails, try index alignment
                            pass
                        
                        # Try comparing by aligning indices
                        try:
                            # Reset indices for comparison if they differ
                            result_col_reset = result_col.reset_index(drop=True)
                            expected_values_reset = expected_values.reset_index(drop=True)
                            diff_aligned = (result_col_reset - expected_values_reset).abs()
                            if diff_aligned.max() < 0.01:
                                print(f"\n✅ Correct! New column '{new_col_name}' created correctly!")
                                task2_completed = True
                                tasks_completed += 1
                                break
                        except:
                            pass
                    
                    # If we get here, values don't match
                        print(f"\n❌ Values in '{new_col_name}' don't match expected ({col1} {op_symbol} {col2})")
                        if attempts < max_attempts:
                            print(f"💡 Make sure you {operation} '{col1}' {op_symbol} '{col2}'")
                            print("💡 Try again.")
                        else:
                            print("\n" + "="*60)
                            print("📖 CORRECT ANSWER:")
                            print("="*60)
                            print(expected_code)
                            print(f"\n💡 Explanation: Create new columns by assigning calculated values ({operation})")
                            break
                else:
                    print(f"\n❌ Column '{new_col_name}' not found")
                    if attempts < max_attempts:
                        print(f"💡 Make sure you create a column named '{new_col_name}'")
                        print("💡 Try again.")
                    else:
                        if operation == 'divide':
                            expected_code = f"df['{new_col_name}'] = df['{col1}'] / df['{col2}']"
                        elif operation == 'multiply':
                            expected_code = f"df['{new_col_name}'] = df['{col1}'] * df['{col2}']"
                        elif operation == 'add':
                            expected_code = f"df['{new_col_name}'] = df['{col1}'] + df['{col2}']"
                        else:
                            expected_code = f"df['{new_col_name}'] = df['{col1}'] - df['{col2}']"
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(expected_code)
                        print(f"\n💡 Explanation: Create new columns by assigning calculated values ({operation})")
                        break
            except Exception as e:
                print(f"\n❌ Error validating: {str(e)}")
                if attempts >= max_attempts:
                    break
                print("💡 Try again.")
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
                
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error: {error}")
                    print("💡 Fix the error and try again")
                    if attempts >= max_attempts:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df.drop(columns=['{col_to_drop}'])")
                        print("\n💡 Explanation: drop() with columns parameter removes specified columns")
                        break
                    continue
                
                if not hasattr(result, 'shape'):
                    print("❌ Result is not a DataFrame")
                    if attempts >= max_attempts:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df.drop(columns=['{col_to_drop}'])")
                        print("\n💡 Explanation: drop() with columns parameter removes specified columns")
                        break
                    continue
                
                print(f"\n📊 Result columns: {list(result.columns)}")
                
                if col_to_drop not in result.columns and result.shape[1] == df.shape[1] - 1:
                    print(f"\n✅ Correct! Column '{col_to_drop}' was dropped!")
                    task3_completed = True
                    tasks_completed += 1
                    break
                else:
                    if col_to_drop in result.columns:
                        print(f"\n❌ Column '{col_to_drop}' still exists")
                    if result.shape[1] != df.shape[1] - 1:
                        print(f"\n❌ Expected {df.shape[1] - 1} columns, got {result.shape[1]}")
                    if attempts < max_attempts:
                        print(f"💡 Use drop(columns=['{col_to_drop}'])")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df.drop(columns=['{col_to_drop}'])")
                        print("\n💡 Explanation: drop() with columns parameter removes specified columns")
                        break
        
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
                
                # Store original df state
                df_before = df.copy()
                
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error: {error}")
                    print("💡 Fix the error and try again")
                    if attempts >= max_attempts:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df['{numeric_col}'] = df['{numeric_col}'].astype('int64')")
                        print("\n💡 Explanation: astype() converts column to specified data type")
                        break
                    continue
                
                # Handle in-place modifications: check df if result is None
                df_to_check = df if result is None or not hasattr(result, 'shape') else result
                
                if not hasattr(df_to_check, 'shape'):
                    print("❌ Result is not a DataFrame")
                    if attempts >= max_attempts:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df['{numeric_col}'] = df['{numeric_col}'].astype('int64')")
                        print("\n💡 Explanation: astype() converts column to specified data type")
                        break
                    continue
                
                # Check if column exists and get its dtype
                if numeric_col not in df_to_check.columns:
                    print(f"\n❌ Column '{numeric_col}' not found in result")
                    if attempts < max_attempts:
                        print("💡 Make sure the column exists after your operation")
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df['{numeric_col}'] = df['{numeric_col}'].astype('int64')")
                        print("\n💡 Explanation: astype() converts column to specified data type")
                        break
                    continue
                
                print(f"\n📊 Data type of '{numeric_col}': {df_to_check[numeric_col].dtype}")
                
                # Check if dtype is integer (int8, int16, int32, int64, Int8, Int16, Int32, Int64)
                dtype_str = str(df_to_check[numeric_col].dtype).lower()
                if 'int' in dtype_str and 'float' not in dtype_str:
                    print(f"\n✅ Correct! Column '{numeric_col}' is now integer type!")
                    task4_completed = True
                    tasks_completed += 1
                    break
                else:
                    print(f"\n❌ Column is still {df_to_check[numeric_col].dtype}, expected int64")
                    if attempts < max_attempts:
                        print("💡 Think about how to convert a column's data type")
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df['{numeric_col}'] = df['{numeric_col}'].astype('int64')")
                        print("\n💡 Explanation: astype() converts column to specified data type")
                        break
        
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
                
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error: {error}")
                    print("💡 Fix the error and try again")
                    if attempts >= max_attempts:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df[{reordered_cols}]")
                        print("\n💡 Explanation: Select columns in desired order using list")
                        break
                    continue
                
                if not hasattr(result, 'shape'):
                    print("❌ Result is not a DataFrame")
                    if attempts >= max_attempts:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df[{reordered_cols}]")
                        print("\n💡 Explanation: Select columns in desired order using list")
                        break
                    continue
                
                print(f"\n📊 Result columns: {list(result.columns)}")
                
                if list(result.columns) == reordered_cols:
                    print(f"\n✅ Correct! Columns are reordered correctly!")
                    task5_completed = True
                    tasks_completed += 1
                    break
                else:
                    print(f"\n❌ Column order doesn't match. Expected: {reordered_cols}")
                    if attempts < max_attempts:
                        print("💡 Think about how to select columns in a specific order")
                        print("💡 Try again.")
                    else:
                        cols_str = str(reordered_cols).replace("'", "'")
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df[{reordered_cols}]")
                        print("\n💡 Explanation: Select columns in desired order using list")
                        break
        
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
                
                # Store original df state
                df_before_task6 = df.copy()
                
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error: {error}")
                    print("💡 Fix the error and try again")
                    if attempts >= max_attempts:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df['{new_col_name}'] = df['{numeric_col2}'] ** 2")
                        print("\n💡 Explanation: Use ** for exponentiation")
                        break
                    continue
                
                # Handle in-place modifications: check df if result is None
                df_to_check = df if result is None or not hasattr(result, 'shape') else result
                
                if not hasattr(df_to_check, 'shape'):
                    print("❌ Result is not a DataFrame")
                    if attempts >= max_attempts:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df['{new_col_name}'] = df['{numeric_col2}'] ** 2")
                        print("\n💡 Explanation: Use ** for exponentiation")
                        break
                    continue
                
                if new_col_name in df_to_check.columns:
                    expected_values = df_before_task6[numeric_col2] ** 2
                    result_col = df_to_check[new_col_name]
                    
                    # Compare values - handle index alignment
                    if len(result_col) == len(expected_values):
                        try:
                            # Try direct comparison
                            diff = (result_col.values - expected_values.values).abs()
                            if diff.max() < 0.01:
                                print(f"\n✅ Correct! New column '{new_col_name}' created with squared values!")
                                task8_completed = True
                                tasks_completed += 1
                                break
                        except:
                            pass
                        
                        # Try index-aligned comparison
                        try:
                            result_col_reset = result_col.reset_index(drop=True)
                            expected_values_reset = expected_values.reset_index(drop=True)
                            diff_aligned = (result_col_reset - expected_values_reset).abs()
                            if diff_aligned.max() < 0.01:
                                print(f"\n✅ Correct! New column '{new_col_name}' created with squared values!")
                                task8_completed = True
                                tasks_completed += 1
                                break
                        except:
                            pass
                    
                    # If we get here, values don't match
                        print(f"\n❌ Values in '{new_col_name}' don't match squared values")
                else:
                    print(f"\n❌ Column '{new_col_name}' not found")
                
                if attempts < max_attempts:
                    print("💡 Think about how to apply a mathematical operation to create a new column")
                    print("💡 Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df['{new_col_name}'] = df['{numeric_col2}'] ** 2")
                    print("\n💡 Explanation: Use ** for exponentiation")
                    break
        
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
                
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error: {error}")
                    print("💡 Fix the error and try again")
                    if attempts >= max_attempts:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df.corr()['{target_col}']")
                        print("\n💡 Explanation: Get a column from the correlation matrix to see correlations with that column")
                        break
                    continue
                
                print(f"\n📊 Result:")
                print(result)
                
                # Validate correlation series
                try:
                    expected = df.corr()[target_col]
                    if hasattr(result, 'equals'):
                        if result.equals(expected):
                            print(f"\n✅ Correct! You got all correlations with '{target_col}'!")
                            task5_completed = True
                            tasks_completed += 1
                            break
                    elif hasattr(result, 'index') and hasattr(result, 'values'):
                        if all(result.index == expected.index):
                            if all(abs(result.values - expected.values) < 0.0001):
                                print(f"\n✅ Correct! You got all correlations with '{target_col}'!")
                                task5_completed = True
                                tasks_completed += 1
                                break
                    
                    print(f"\n❌ Result doesn't match expected correlations with '{target_col}'")
                    if attempts < max_attempts:
                        print(f"💡 Think about how to extract one column from a correlation matrix")
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df.corr()['{target_col}']")
                        print("\n💡 Explanation: Get a column from the correlation matrix to see correlations with that column")
                        break
                except Exception as e:
                    print(f"\n❌ Error validating: {str(e)}")
                    if attempts >= max_attempts:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df.corr()['{target_col}']")
                        print("\n💡 Explanation: Get a column from the correlation matrix to see correlations with that column")
                        break
                    print("💡 Try again.")
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
                
                result, error = self.execute_pandas_code(df, code, include_plotting=True)
                if error:
                    print(f"❌ Error: {error}")
                    print("💡 Fix the error and try again")
                    if attempts >= max_attempts:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df['{col}'].value_counts().plot(kind='bar')")
                        print("\n💡 Explanation: value_counts() gets frequencies, plot(kind='bar') creates a bar plot")
                        break
                    continue
                
                # Check if code contains plotting keywords
                code_lower = code.lower()
                has_plot = 'plot' in code_lower or 'bar' in code_lower or 'plt.' in code_lower or 'seaborn' in code_lower
                has_value_counts = 'value_counts' in code_lower
                
                if has_plot and has_value_counts and error is None:
                    print(f"\n✅ Correct! You created a bar plot of value counts for '{col}'!")
                    print("💡 Plot created successfully (running in non-interactive mode)")
                    task6_completed = True
                    tasks_completed += 1
                    break
                elif has_plot and error is None:
                    # Accept if plotting code is present even without value_counts (user might do it differently)
                    print(f"\n✅ Correct! You created a bar plot of value counts for '{col}'!")
                    print("💡 Plot created successfully (running in non-interactive mode)")
                    task6_completed = True
                    tasks_completed += 1
                    break
                else:
                    print(f"\n❌ Your code should create a bar plot of value counts")
                    if attempts < max_attempts:
                        print(f"💡 Think about how to count values and then visualize them")
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df['{col}'].value_counts().plot(kind='bar')")
                        print("\n💡 Explanation: value_counts() gets frequencies, plot(kind='bar') creates a bar plot")
                        break
        
        # Exercise 4 complete - record completion
        self.record_exercise_completion("exercise_4", tasks_completed, total_tasks)
        grade = (tasks_completed / total_tasks) * 100.0
        print(f"\n✅ Exercise 4 Complete! Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
        input("\nPress Enter to continue...")
    
    def exercise_5_data_cleaning(self):
        """Exercise: Data cleaning."""
        print("\n🎯 GOAL: Learn data cleaning techniques")
        
        df = self.load_dataset("messy_data.csv")
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
                
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error: {error}")
                    print("💡 Fix the error and try again")
                    if attempts >= max_attempts:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print("df.isnull().sum().sum()")
                        print("\n💡 Explanation: First sum() counts per column, second sum() totals all columns")
                        break
                    continue
                
                print(f"\n📊 Result: {result}")
                
                try:
                    if result == expected_total:
                        print(f"\n✅ Correct! Found {result} total missing value(s)!")
                        task1_completed = True
                        tasks_completed += 1
                        break
                    else:
                        print(f"\n❌ Expected {expected_total} total missing values, got {result}")
                        if attempts < max_attempts:
                            print("💡 Think about how to count missing values across the entire dataframe")
                        else:
                            print("\n" + "="*60)
                            print("📖 CORRECT ANSWER:")
                            print("="*60)
                            print("df.isnull().sum().sum()")
                            print("\n💡 Explanation: First sum() counts per column, second sum() totals all columns")
                            break
                except Exception as e:
                    print(f"\n❌ Error validating: {str(e)}")
                    if attempts >= max_attempts:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print("df.isnull().sum().sum()")
                        print("\n💡 Explanation: First sum() counts per column, second sum() totals all columns")
                        break
                    print("💡 Make sure your code returns a single number (total count)")
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
            
            result, error = self.execute_pandas_code(df, code)
            if error:
                print(f"❌ Error: {error}")
                print("💡 Fix the error and try again")
                if attempts >= max_attempts:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print("df.drop_duplicates()")
                    print("\n💡 Explanation: drop_duplicates() removes duplicate rows from the dataframe")
                    break
                continue
            
            if not hasattr(result, 'shape'):
                print("❌ Result is not a DataFrame")
                print("💡 Your code should return a DataFrame with duplicates removed")
                if attempts >= max_attempts:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print("df.drop_duplicates()")
                    print("\n💡 Explanation: drop_duplicates() removes duplicate rows from the dataframe")
                    break
                continue
            
            print(f"\n📊 New shape: {result.shape}")
            removed = df.shape[0] - result.shape[0]
            print(f"   Removed {removed} duplicate rows")
            is_valid, message = self.validate_drop_duplicates(result, df)
            if is_valid:
                print(f"\n✅ {message}")
                task2_completed = True
                tasks_completed += 1
                break
            else:
                print(f"\n❌ {message}")
                if attempts < max_attempts:
                    print("💡 Your answer is not correct. Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print("df.drop_duplicates()")
                    print("\n💡 Explanation: drop_duplicates() removes duplicate rows from the dataframe")
                    break
        
        # TASK 3: Varied missing value handling - randomly choose method
        missing_before = df.isnull().sum().sum()
        if missing_before > 0:
            # Randomly choose between drop, fill with value, or backward fill
            method_options = ['drop', 'fill_value', 'bfill']
            method_choice = random.choice(method_options)
            
            if method_choice == 'drop':
                print("\n" + "="*60)
                print("TASK 3: Remove all rows that have ANY missing values")
                print("="*60)
                print(f"💡 Dataset: {self.current_dataset_name}")
                print("💡 Hint: Think about how to remove rows with missing values")
                print(f"💡 Current missing values: {missing_before}")
                print("💡 Remove rows that have at least one missing value")
                print("\nEnter your pandas code below:")
                
                task3_completed = False
                attempts = 0
                max_attempts = 3
                correct_answer = "df.dropna()"
                explanation = "dropna() removes rows with any missing values"
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
                    if error:
                        print(f"❌ Error: {error}")
                        print("💡 Fix the error and try again")
                        if attempts >= max_attempts:
                            print("\n" + "="*60)
                            print("📖 CORRECT ANSWER:")
                            print("="*60)
                            print("df.dropna()")
                            print("\n💡 Explanation: dropna() removes rows with any missing values")
                            break
                        continue
                    
                    if not hasattr(result, 'shape'):
                        print("❌ Result is not a DataFrame")
                        if attempts >= max_attempts:
                            print("\n" + "="*60)
                            print("📖 CORRECT ANSWER:")
                            print("="*60)
                            print("df.dropna()")
                            print("\n💡 Explanation: dropna() removes rows with any missing values")
                            break
                        continue
                    
                    print(f"\n📊 New shape: {result.shape}")
                    if result.isnull().sum().sum() == 0 and result.shape[0] < df.shape[0]:
                        print(f"\n✅ Correct! Removed rows with missing values!")
                        task3_completed = True
                        tasks_completed += 1
                        break
                    else:
                        print(f"\n❌ Expected rows with no missing values")
                        if attempts < max_attempts:
                            print("💡 Think about how to remove rows that have any missing values")
                            print("💡 Try again.")
                        else:
                            print("\n" + "="*60)
                            print("📖 CORRECT ANSWER:")
                            print("="*60)
                            print("df.dropna()")
                            print("\n💡 Explanation: dropna() removes rows with any missing values")
                            break
            
            elif method_choice == 'fill_value':
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
                    
                    result, error = self.execute_pandas_code(df, code)
                    if error:
                        print(f"❌ Error: {error}")
                        print("💡 Fix the error and try again")
                        if attempts >= max_attempts:
                            print("\n" + "="*60)
                            print("📖 CORRECT ANSWER:")
                            print("="*60)
                            print(f"df.fillna({fill_value})")
                            print(f"\n💡 Explanation: fillna({fill_value}) fills missing values with {fill_value}")
                            break
                        continue
                    
                    if not hasattr(result, 'shape'):
                        print("❌ Result is not a DataFrame")
                        if attempts >= max_attempts:
                            print("\n" + "="*60)
                            print("📖 CORRECT ANSWER:")
                            print("="*60)
                            print(f"df.fillna({fill_value})")
                            print(f"\n💡 Explanation: fillna({fill_value}) fills missing values with {fill_value}")
                            break
                        continue
                    
                    print(f"\n📊 New shape: {result.shape}")
                    missing_after = result.isnull().sum().sum()
                    print(f"   Missing values after: {missing_after}")
                    is_valid, message = self.validate_handle_missing(result, df, 'fill', fill_value)
                    if is_valid:
                        print(f"\n✅ {message}")
                        task3_completed = True
                        tasks_completed += 1
                        break
                    else:
                        print(f"\n❌ {message}")
                        if attempts < max_attempts:
                            print("💡 Think about how to replace missing values with a specific value")
                            print("💡 Try again.")
                        else:
                            print("\n" + "="*60)
                            print("📖 CORRECT ANSWER:")
                            print("="*60)
                            print(f"df.fillna({fill_value})")
                            print(f"\n💡 Explanation: fillna({fill_value}) fills missing values with {fill_value}")
                            break
            
            else:  # bfill
                cols_with_nulls_bfill = [col for col in df.columns if df[col].isnull().any()]
                if cols_with_nulls_bfill:
                    col_to_bfill = random.choice(cols_with_nulls_bfill)
                    print("\n" + "="*60)
                    print(f"TASK 3: Fill missing values in '{col_to_bfill}' column using backward fill")
                    print("="*60)
                    print(f"💡 Dataset: {self.current_dataset_name}")
                    print("💡 Hint: Think about how to fill missing values by propagating the next value backward")
                    print(f"💡 Fill missing values in '{col_to_bfill}' by propagating the next value backward")
                    print("\nEnter your pandas code below:")
                    
                    task3_completed = False
                    attempts = 0
                    max_attempts = 3
                    correct_answer = f"df['{col_to_bfill}'] = df['{col_to_bfill}'].fillna(method='bfill')  # or df['{col_to_bfill}'].bfill()"
                    explanation = "Backward fill propagates the next value backward"
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
                        if error:
                            print(f"❌ Error: {error}")
                            print("💡 Fix the error and try again")
                            if attempts >= max_attempts:
                                print("\n" + "="*60)
                                print("📖 CORRECT ANSWER:")
                                print("="*60)
                                print(f"df['{col_to_bfill}'] = df['{col_to_bfill}'].fillna(method='bfill')  # or df['{col_to_bfill}'].bfill()")
                                print("\n💡 Explanation: Backward fill propagates the next value backward")
                                break
                            continue
                        
                        if not hasattr(result, 'shape'):
                            print("❌ Result is not a DataFrame")
                            if attempts >= max_attempts:
                                print("\n" + "="*60)
                                print("📖 CORRECT ANSWER:")
                                print("="*60)
                                print(f"df['{col_to_bfill}'] = df['{col_to_bfill}'].fillna(method='bfill')  # or df['{col_to_bfill}'].bfill()")
                                print("\n💡 Explanation: Backward fill propagates the next value backward")
                                break
                            continue
                        
                        print(f"\n📊 Missing values in '{col_to_bfill}': {result[col_to_bfill].isnull().sum()}")
                        
                        expected = df[col_to_bfill].fillna(method='bfill')
                        if result[col_to_bfill].isnull().sum() < df[col_to_bfill].isnull().sum():
                            print(f"\n✅ Correct! Filled missing values using backward fill!")
                            task3_completed = True
                            tasks_completed += 1
                            break
                        
                        print(f"\n❌ Missing values not filled correctly with backward fill")
                        if attempts < max_attempts:
                            print("💡 Think about how to propagate the next value backward to fill missing values")
                            print("💡 Try again.")
                        else:
                            print("\n" + "="*60)
                            print("📖 CORRECT ANSWER:")
                            print("="*60)
                            print(f"df['{col_to_bfill}'] = df['{col_to_bfill}'].fillna(method='bfill')  # or df['{col_to_bfill}'].bfill()")
                            print("\n💡 Explanation: Backward fill propagates the next value backward")
                            break
        
        # TASK 4: Fill missing values with forward fill
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
            correct_answer = f"df['{col_to_ffill}'] = df['{col_to_ffill}'].fillna(method='ffill')  # or df['{col_to_ffill}'].ffill()"
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
                
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error: {error}")
                    print("💡 Fix the error and try again")
                    if attempts >= max_attempts:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df['{col_to_ffill}'] = df['{col_to_ffill}'].fillna(method='ffill')  # or df['{col_to_ffill}'].ffill()")
                        print("\n💡 Explanation: Forward fill propagates the previous value forward")
                        break
                    continue
                
                if not hasattr(result, 'shape'):
                    print("❌ Result is not a DataFrame")
                    if attempts >= max_attempts:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df['{col_to_ffill}'] = df['{col_to_ffill}'].fillna(method='ffill')  # or df['{col_to_ffill}'].ffill()")
                        print("\n💡 Explanation: Forward fill propagates the previous value forward")
                        break
                    continue
                
                print(f"\n📊 Missing values in '{col_to_ffill}': {result[col_to_ffill].isnull().sum()}")
                
                expected = df[col_to_ffill].fillna(method='ffill')
                if result[col_to_ffill].isnull().sum() < df[col_to_ffill].isnull().sum():
                    # Check if filled values match forward fill
                    if result[col_to_ffill].fillna(df[col_to_ffill]).equals(expected.fillna(df[col_to_ffill])):
                        print(f"\n✅ Correct! Filled missing values using forward fill!")
                        task4_completed = True
                        tasks_completed += 1
                        break
                
                print(f"\n❌ Missing values not filled correctly with forward fill")
                if attempts < max_attempts:
                    print("💡 Think about how to propagate the previous value forward to fill missing values")
                    print("💡 Try again.")
                else:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print(f"df['{col_to_ffill}'] = df['{col_to_ffill}'].fillna(method='ffill')  # or df['{col_to_ffill}'].ffill()")
                    print("\n💡 Explanation: Forward fill propagates the previous value forward")
                    break
        
        # TASK 5: Drop columns with missing values
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
                
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error: {error}")
                    print("💡 Fix the error and try again")
                    if attempts >= max_attempts:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df.drop(columns=['{col_to_drop}'])")
                        print("\n💡 Explanation: drop(columns=[]) removes specified columns")
                        break
                    continue
                
                if not hasattr(result, 'shape'):
                    print("❌ Result is not a DataFrame")
                    if attempts >= max_attempts:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df.drop(columns=['{col_to_drop}'])")
                        print("\n💡 Explanation: drop(columns=[]) removes specified columns")
                        break
                    continue
                
                print(f"\n📊 Columns: {list(result.columns)}")
                
                if col_to_drop not in result.columns and result.shape[1] == df.shape[1] - 1:
                    print(f"\n✅ Correct! Column '{col_to_drop}' was dropped!")
                    task7_completed = True
                    tasks_completed += 1
                    break
                else:
                    if col_to_drop in result.columns:
                        print(f"\n❌ Column '{col_to_drop}' still exists")
                    if attempts < max_attempts:
                        print(f"💡 Use drop(columns=['{col_to_drop}'])")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print(f"df.drop(columns=['{col_to_drop}'])")
                        print("\n💡 Explanation: drop(columns=[]) removes specified columns")
                        break
        
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
            
            result, error = self.execute_pandas_code(df, code)
            if error:
                print(f"❌ Error: {error}")
                print("💡 Fix the error and try again")
                if attempts >= max_attempts:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print("df.dropna(how='all')")
                    print("\n💡 Explanation: how='all' removes rows only when all columns are missing")
                    break
                continue
            
            if not hasattr(result, 'shape'):
                print("❌ Result is not a DataFrame")
                if attempts >= max_attempts:
                    print("\n" + "="*60)
                    print("📖 CORRECT ANSWER:")
                    print("="*60)
                    print("df.dropna(how='all')")
                    print("\n💡 Explanation: how='all' removes rows only when all columns are missing")
                    break
                continue
            
            print(f"\n📊 New shape: {result.shape}")
            expected = df.dropna(how='all')
            if result.shape[0] == expected.shape[0] and result.shape[1] == expected.shape[1]:
                # Check that rows with all missing are removed
                if result.shape[0] <= df.shape[0]:
                    print(f"\n✅ Correct! Removed rows where all columns are missing!")
                    task8_completed = True
                    tasks_completed += 1
                    break
            
            print(f"\n❌ Expected {expected.shape[0]} rows after removing rows with all missing values")
            if attempts < max_attempts:
                print("💡 Use dropna(how='all') to remove rows where all values are missing")
            else:
                print("\n" + "="*60)
                print("📖 CORRECT ANSWER:")
                print("="*60)
                print("df.dropna(how='all')")
                print("\n💡 Explanation: how='all' removes rows only when all columns are missing")
                break
        
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
                
                result, error = self.execute_pandas_code(df, code)
                if error:
                    print(f"❌ Error: {error}")
                    print("💡 Fix the error and try again")
                    if attempts >= max_attempts:
                            print("\n" + "="*60)
                            print("📖 CORRECT ANSWER:")
                            print("="*60)
                            print("df.corr()")
                            print("\n💡 Explanation: corr() calculates pairwise correlations between all numeric columns")
                            break
                    continue
                
                if not hasattr(result, 'shape'):
                    print("❌ Result is not a DataFrame")
                    if attempts >= max_attempts:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print("df.corr()")
                        print("\n💡 Explanation: corr() calculates pairwise correlations between all numeric columns")
                        break
                        continue
                    
                print(f"\n📊 Result:")
                print(result)
                
                # Validate correlation matrix
                try:
                    expected = df.corr()
                    test_passed = False
                    if result.shape == expected.shape:
                        if all(result.index == expected.index) and all(result.columns == expected.columns):
                            # Check a few correlation values
                            test_passed = True
                            for i in range(min(3, len(result.index))):
                                for j in range(min(3, len(result.columns))):
                                    if abs(result.iloc[i, j] - expected.iloc[i, j]) > 0.0001:
                                        test_passed = False
                                        break
                                if not test_passed:
                                    break
                            
                            if test_passed:
                                print(f"\n✅ Correct! You calculated the correlation matrix successfully!")
                                task5_completed = True
                            tasks_completed += 1
                            break
                    
                    if not test_passed:
                        print(f"\n❌ Result doesn't match expected correlation matrix")
                        if attempts < max_attempts:
                            print("💡 Think about how to calculate correlations between numeric columns")
                            print("💡 Try again.")
                        else:
                            print("\n" + "="*60)
                            print("📖 CORRECT ANSWER:")
                            print("="*60)
                            print("df.corr()")
                            print("\n💡 Explanation: corr() calculates pairwise correlations between all numeric columns")
                            break
                except Exception as e:
                    print(f"\n❌ Error validating: {str(e)}")
                    if attempts >= max_attempts:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print("df.corr()")
                        print("\n💡 Explanation: corr() calculates pairwise correlations between all numeric columns")
                        break
                    print("💡 Try again.")
                    continue
                    
        # TASK 8: Plotting - Create a heatmap of correlation matrix
        numeric_cols = self.get_numeric_columns()
        if len(numeric_cols) < 2:
            print("\n⚠️  Not enough numeric columns for plotting task. Skipping task 8.")
        else:
            print("\n" + "="*60)
            print("TASK 8: Create a heatmap of the correlation matrix")
            print("="*60)
            print(f"💡 Dataset: {self.current_dataset_name}")
            print("💡 Hint: Think about how to visualize a correlation matrix as a colored grid")
            print("💡 Create a heatmap showing correlations between all numeric columns")
            print("💡 Note: The plot will be created but not displayed (non-interactive mode)")
            print("\nEnter your pandas code below:")
            
            task6_completed = False
            attempts = 0
            max_attempts = 3
            correct_answer = "import seaborn as sns; sns.heatmap(df.corr(), annot=True)"
            explanation = "seaborn.heatmap() creates a heatmap visualization, or use matplotlib"
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
                
                result, error = self.execute_pandas_code(df, code, include_plotting=True)
                if error:
                    print(f"❌ Error: {error}")
                    print("💡 Fix the error and try again")
                    if attempts >= max_attempts:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print("import seaborn as sns; sns.heatmap(df.corr(), annot=True)")
                        print("\n💡 Explanation: seaborn.heatmap() creates a heatmap visualization")
                        break
                    continue
                
                # Check if code contains plotting keywords
                code_lower = code.lower()
                has_plot = 'heatmap' in code_lower or 'plot' in code_lower or 'plt.' in code_lower or 'sns.' in code_lower
                has_corr = 'corr' in code_lower
                
                if has_plot and has_corr and error is None:
                    print(f"\n✅ Correct! You created a heatmap of the correlation matrix!")
                    print("💡 Plot created successfully (running in non-interactive mode)")
                    task6_completed = True
                    tasks_completed += 1
                    break
                else:
                    print(f"\n❌ Your code should create a heatmap of the correlation matrix")
                    if attempts < max_attempts:
                        print("💡 Think about how to visualize a matrix as a colored grid")
                        print("💡 Try again.")
                    else:
                        print("\n" + "="*60)
                        print("📖 CORRECT ANSWER:")
                        print("="*60)
                        print("import seaborn as sns; sns.heatmap(df.corr(), annot=True)")
                        print("\n💡 Explanation: seaborn.heatmap() creates a heatmap visualization")
                        break
        
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
                self.progress["datasets_explored"] = []
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
            
            # Get list of available datasets and map to numbers
            datasets_explored = self.progress.get('datasets_explored', [])
            if self.data_dir.exists():
                all_datasets = sorted(list(self.data_dir.glob("*.csv")))
                dataset_numbers = {}
                for i, ds in enumerate(all_datasets, 1):
                    dataset_numbers[ds.name] = i
                
                explored_numbers = []
                for ds_name in datasets_explored:
                    if ds_name in dataset_numbers:
                        explored_numbers.append(dataset_numbers[ds_name])
                explored_numbers.sort()
                
                if explored_numbers:
                    numbers_str = ", ".join(map(str, explored_numbers))
                    print(f"\n📁 Datasets Explored: {len(datasets_explored)}/3 (Numbers: {numbers_str})")
                else:
                    print(f"\n📁 Datasets Explored: {len(datasets_explored)}/3")
            else:
                print(f"\n📁 Datasets Explored: {len(datasets_explored)}/3")
            
            if self.progress.get('last_session'):
                print(f"📅 Last Session: {self.progress['last_session']}")
            
            # Check if stats are already empty
            stats_empty = (
                not self.progress.get("exercise_stats", {}) and 
                not self.progress.get("datasets_explored", []) and
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
            if self.current_dataset is not None:
                print(f"📊 Current Dataset: {self.current_dataset_name} ({self.current_dataset.shape[0]} rows × {self.current_dataset.shape[1]} columns)")
            else:
                print("📊 Current Dataset: None (Please load a dataset)")
            print("="*60)
            print("1. Load Dataset")
            print("2. Explore Current Dataset")
            print("3. Run Exercise")
            print("4. View Learning Statistics")
            print("5. Exit")
            
            choice = input("\nSelect an option (1-5): ").strip()
            
            if choice == "1":
                old_dataset = self.current_dataset_name
                self.list_datasets()
                if self.current_dataset_name != old_dataset:
                    print(f"\n✅ Dataset changed! Exercises will now use: {self.current_dataset_name}")
                    print("💡 Each time you run an exercise, it will use random values from this dataset")
            elif choice == "2":
                self.explore_dataset()
            elif choice == "3":
                if self.current_dataset is None:
                    print("\n❌ No dataset loaded! Please load a dataset first (option 1)")
                else:
                    self.show_exercises()
            elif choice == "4":
                self.show_statistics()
            elif choice == "5":
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
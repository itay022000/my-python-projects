"""Exercise 5: Data cleaning."""

import random

import numpy as np
import practice_common


class Exercise5Mixin:
    """Mixin for PandasPractice."""

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
                if practice_common.codes_match(code, correct_answer):
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
            
            if practice_common.codes_match(code, correct_answer):
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
                row_idx = random.randrange(len(df))
                col_idx = random.randrange(len(df.columns))
                df.iat[row_idx, col_idx] = np.nan
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
                    if practice_common.codes_match(code, correct_answer):
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
                row_idx = random.randrange(len(df))
                col_idx = random.randrange(len(df.columns))
                df.iat[row_idx, col_idx] = np.nan
        
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
            correct_answer = f"df['{col_to_ffill}'] = df['{col_to_ffill}'].ffill()"
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
                if practice_common.codes_match(code, correct_answer):
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
                row_idx = random.randrange(len(df))
                col_idx = random.randrange(len(df.columns))
                df.iat[row_idx, col_idx] = np.nan
        
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
                if practice_common.codes_match(code, correct_answer):
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
            
            if practice_common.codes_match(code, correct_answer):
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
        correct_answer = "df.select_dtypes(include=['int64', 'float64']).corr()"
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
            if practice_common.codes_match(code, correct_answer):
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
            
            if practice_common.codes_match(code, correct_answer):
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

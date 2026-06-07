"""Exercise 4: Data manipulation."""

import random

import practice_common


class Exercise4Mixin:
    """Mixin for PandasPractice."""

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
        
        # Get two numeric columns for calculation
        numeric_cols = self.get_numeric_columns()
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
        
        # TASK 7: Correlation - Correlation with a specific column
        numeric_cols = self.get_numeric_columns()
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
        correct_answer = (
            f"df.select_dtypes(include=['int64', 'float64']).corr()['{target_col}']"
        )
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
        
        # TASK 8: Plotting - Create a bar plot of value counts for a categorical column
        categorical_cols = self.get_categorical_columns()
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
            if practice_common.codes_match(code, correct_answer):
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
    

"""Exercise 3: Sorting and column selection."""

import random

import practice_common


class Exercise3Mixin:
    """Mixin for PandasPractice."""

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
        
        # Select random columns for task 2
        all_cols = df.columns.tolist()
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
    

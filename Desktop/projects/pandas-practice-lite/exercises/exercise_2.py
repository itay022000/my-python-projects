"""Exercise 2: Filtering."""

import random
import practice_common


class Exercise2Mixin:
    """Mixin for PandasPractice."""

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
        
        # Get random categorical column and value
        categorical_col = self.get_random_categorical_column()
        category_values = df[categorical_col].dropna().unique()
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
        
        # TASK 7: Correlation - Correlation between two numeric columns
        numeric_cols = self.get_numeric_columns()
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
        
        # TASK 8: Plotting - Create a box plot
        numeric_cols = self.get_numeric_columns()
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
                break
        
        # Exercise 2 complete - record completion
        self.record_exercise_completion("exercise_2", tasks_completed, total_tasks)
        grade = (tasks_completed / total_tasks) * 100.0
        print(f"\n✅ Exercise 2 Complete! Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
        input("\nPress Enter to continue...")
    

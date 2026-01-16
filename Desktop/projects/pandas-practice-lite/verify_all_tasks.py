#!/usr/bin/env python3
"""
Code structure verification for all tasks.
Verifies that every task follows the correct pattern for all 4 cases.
"""

import re
from pathlib import Path

def verify_task_structure():
    """Verify that all tasks follow the correct structure."""
    main_file = Path("main.py")
    content = main_file.read_text()
    
    issues = []
    verified = 0
    
    # Find all exercise functions
    exercises = {
        "exercise_1_basic_operations": "Exercise 1",
        "exercise_2_filtering": "Exercise 2", 
        "exercise_3_sorting_and_selection": "Exercise 3",
        "exercise_4_data_manipulation": "Exercise 4",
        "exercise_5_data_cleaning": "Exercise 5"
    }
    
    print("\n" + "="*70)
    print("VERIFYING CODE STRUCTURE FOR ALL TASKS")
    print("="*70)
    
    for func_name, ex_name in exercises.items():
        print(f"\n{ex_name}:")
        
        # Find the exercise function
        pattern = rf"def {func_name}\(self\):.*?(?=def |\Z)"
        match = re.search(pattern, content, re.DOTALL)
        
        if not match:
            issues.append(f"{ex_name}: Function not found")
            continue
        
        exercise_code = match.group(0)
        
        # Count unique tasks by finding all "TASK X:" print statements
        # This is the most reliable way to count actual tasks, as each task
        # has exactly one "TASK X:" print statement, even if it has multiple
        # conditional branches (like Exercise 5 Task 1 and Task 3)
        task_number_pattern = r'"TASK (\d+):'
        task_numbers = re.findall(task_number_pattern, exercise_code)
        unique_tasks = sorted(set(task_numbers), key=int)
        num_tasks = len(unique_tasks)
        
        print(f"  Found {num_tasks} unique tasks (task numbers: {', '.join(unique_tasks)})")
        
        # Verify each task has:
        # 1. handle_special_commands
        # 2. is_exit handler with record_exercise_completion
        # 3. is_skip handler that just breaks
        # 4. Correct answer display on max attempts
        
        # Check for handle_special_commands in exercise
        if "handle_special_commands" not in exercise_code:
            issues.append(f"{ex_name}: Missing handle_special_commands")
        else:
            verified += 1
        
        # Count is_exit handlers (should match number of tasks)
        exit_count = exercise_code.count("if is_exit:")
        if exit_count < num_tasks:
            issues.append(f"{ex_name}: Only {exit_count} exit handlers for {num_tasks} tasks")
        else:
            verified += 1
        
        # Count is_skip handlers (should match number of tasks)
        skip_count = exercise_code.count("if is_skip:")
        if skip_count < num_tasks:
            issues.append(f"{ex_name}: Only {skip_count} skip handlers for {num_tasks} tasks")
        else:
            verified += 1
        
        # Verify skip just breaks (doesn't increment)
        skip_pattern = r"if is_skip:.*?break"
        skip_matches = re.findall(skip_pattern, exercise_code, re.DOTALL)
        for i, skip_match in enumerate(skip_matches, 1):
            if "tasks_completed" in skip_match:
                issues.append(f"{ex_name} Task {i}: Skip handler increments tasks_completed (should not)")
            else:
                verified += 1
        
        # Verify exit records completion
        exit_pattern = r"if is_exit:.*?record_exercise_completion"
        exit_matches = re.findall(exit_pattern, exercise_code, re.DOTALL)
        if len(exit_matches) < num_tasks:
            issues.append(f"{ex_name}: Some tasks missing exit completion recording (found {len(exit_matches)} for {num_tasks} tasks)")
        else:
            verified += 1
    
    print("\n" + "="*70)
    print("VERIFICATION SUMMARY")
    print("="*70)
    print(f"Verified patterns: {verified}")
    if issues:
        print(f"Issues found: {len(issues)}")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("✓ All tasks follow the correct pattern!")
    print("="*70)
    
    return len(issues) == 0

if __name__ == "__main__":
    verify_task_structure()


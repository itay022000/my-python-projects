# Test Failure Diagnostic Guide

When a test fails, you'll see a **DIAGNOSTIC** section that tells you exactly what to fix in `main.py`.

## Understanding Diagnostic Messages

Each diagnostic message includes:

1. **❌ ISSUE**: What went wrong
2. **📍 WHERE TO FIX**: Exact location in main.py (method name and approximate line numbers)
3. **🔧 HOW TO FIX**: Step-by-step instructions

## Common Issues and Fixes

### Issue: "Invalid dataset number was accepted"
**Location**: `list_datasets()` method (around line 200-250)

**Fix**:
1. Check the `while True` loop in `list_datasets()` method
2. Ensure it validates input: `if 0 <= idx < len(datasets)`
3. Verify it prints error message: `'❌ Invalid number! Please enter...'`
4. Make sure the loop continues until valid input is provided

**Code Pattern**:
```python
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
```

---

### Issue: "Correct answer shown X times instead of exactly once"
**Location**: Exercise methods - Task loops (around line 700-750 for Exercise 1, +600 per exercise)

**Fix**:
1. Check the `while attempts < max_attempts:` loop in the task
2. Ensure `'CORRECT ANSWER'` is printed only ONCE when `attempts >= max_attempts`
3. Look for duplicate print statements in the error handling block
4. Verify the answer is shown in the `else` block when `attempts >= max_attempts`
5. Check there's no duplicate answer display after the while loop ends
6. Make sure the `break` statement is after showing the answer

**Code Pattern**:
```python
while attempts < max_attempts:
    attempts += 1
    code = input(f"\nYour code (attempt {attempts}/{max_attempts}): ").strip()
    
    # ... validation ...
    
    if correct:
        tasks_completed += 1
        break
    elif attempts >= max_attempts:
        # Show answer ONCE here
        print("\n" + "="*60)
        print("📖 CORRECT ANSWER:")
        print("="*60)
        print(correct_answer)
        break
# NO duplicate answer display here!
```

---

### Issue: "Skip command not recognized"
**Location**: `handle_special_commands()` (line 156-177) and exercise methods

**Fix**:
1. Check `handle_special_commands()` method - verify it returns `(True, False, True)` for `'skip'`
2. Ensure it prints: `'⏭️  Task skipped'` and `'📖 CORRECT ANSWER:'`
3. In exercise methods, check: `if is_skip: break`
4. Verify `tasks_completed` is NOT incremented when skip is used
5. Make sure the task calls `handle_special_commands()` before processing code
6. Check that skip shows the answer but doesn't count toward grade (0%)

**Code Pattern**:
```python
# In handle_special_commands():
if code_lower == 'skip':
    print("\n" + "="*60)
    print("⏭️  Task skipped")
    print("="*60)
    print("📖 CORRECT ANSWER:")
    print("="*60)
    print(correct_answer)
    return True, False, True  # is_skip, is_exit, should_continue

# In exercise tasks:
is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)

if is_skip:
    break  # Skip task, don't increment tasks_completed
```

---

### Issue: "Exit command not recognized"
**Location**: `handle_special_commands()` (line 156-177) and exercise methods

**Fix**:
1. Check `handle_special_commands()` - verify it returns `(False, True, False)` for `'exit'`
2. In exercise methods, check: `if is_exit:` block
3. Verify it calls: `self.record_exercise_completion('exercise_X', tasks_completed, total_tasks)`
4. Ensure it prints: `'⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)'`
5. Make sure it returns immediately: `return` (not just `break`)
6. Check that the task calls `handle_special_commands()` before processing code

**Code Pattern**:
```python
# In handle_special_commands():
elif code_lower == 'exit':
    return False, True, False  # is_skip, is_exit, should_continue

# In exercise tasks:
is_skip, is_exit, should_continue = self.handle_special_commands(code, correct_answer, explanation)

if is_exit:
    self.record_exercise_completion("exercise_X", tasks_completed, total_tasks)
    grade = (tasks_completed / total_tasks) * 100.0
    print(f"\n⏹️  Exercise exited. Score: {tasks_completed}/{total_tasks} tasks ({grade:.1f}%)")
    return  # Exit immediately, not break!
```

---

### Issue: "Correct answer not recognized"
**Location**: Exercise methods - validation logic

**Fix**:
1. Check the exercise method's validation logic for correct answers
2. Verify it prints `'✅ Correct!'` or similar success message
3. Check that `tasks_completed` is incremented when answer is correct
4. Verify the code execution: `result, error = self.execute_pandas_code(df, code)`
5. Make sure validation checks the result correctly

**Code Pattern**:
```python
result, error = self.execute_pandas_code(df, code)
if error:
    # Handle error
    continue

# Validate result
if is_valid:
    print(f"\n✅ {message}")
    task_completed = True
    tasks_completed += 1  # Increment here
    break
```

---

## Finding Code Locations

The diagnostic messages provide approximate line numbers. To find the exact location:

1. **Search for method name**: Use your editor's search (Cmd+F / Ctrl+F)
2. **Search for function name**: e.g., `def exercise_1_basic_operations`
3. **Search for key strings**: e.g., `"CORRECT ANSWER"`, `"Task skipped"`, `"Exercise exited"`

## Quick Reference: Key Methods

- **`handle_special_commands()`**: Line ~156-177
- **`list_datasets()`**: Line ~200-250
- **`exercise_1_basic_operations()`**: Line ~670-1300
- **`exercise_2_filtering()`**: Line ~1300-2300
- **`exercise_3_sorting_and_selection()`**: Line ~2300-3300
- **`exercise_4_data_manipulation()`**: Line ~3300-4300
- **`exercise_5_data_cleaning()`**: Line ~4300-5300

## Still Stuck?

1. Read the diagnostic message carefully
2. Search for the method name in main.py
3. Compare your code with the code patterns above
4. Run the test again to see if the fix worked
5. Check for syntax errors or indentation issues


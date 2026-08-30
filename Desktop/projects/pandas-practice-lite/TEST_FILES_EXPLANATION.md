# Test Files Explanation

This document explains how each test file works and what it tests.

## Overview

All test files use the same basic approach:
1. **Subprocess Execution**: They run `main.py` as a subprocess
2. **Input Simulation**: They provide automated inputs via stdin
3. **Output Verification**: They check stdout/stderr for expected results
4. **Pass/Fail Reporting**: Each test clearly shows ✓ (pass) or ✗ (fail)

---

## 1. `test_simulation.py` - Basic Functionality Tests

### Purpose
Quick test suite for basic functionality (4 tests).

### What It Tests

#### Test 1: Dataset Loading Validation
- **What**: Tests that invalid dataset choices are caught
- **How**: 
  - Tries to load dataset with invalid number (5)
  - Verifies error message appears
  - Then loads with valid number (1)
- **Expected**: "Invalid" message appears, then dataset loads successfully
- **Output**: `[✓] Dataset loading validation: PASS` or `[✗] ... FAIL`

#### Test 2: Correct Answer Display (3 Failed Attempts)
- **What**: Tests that correct answer is shown exactly once after 3 wrong attempts
- **How**:
  - Loads dataset and starts Exercise 1
  - Provides 3 wrong answers for task 1
  - Counts occurrences of "CORRECT ANSWER" in output
- **Expected**: "CORRECT ANSWER" appears exactly once
- **Output**: `[✓] Correct answer display (3 failed attempts): PASS` or `[✗] ... FAIL`

#### Test 3: Skip Command
- **What**: Tests that 'skip' command works
- **How**:
  - Loads dataset and starts Exercise 1
  - Skips all 8 tasks using 'skip' command
  - Checks for "Task skipped" or "skipped" in output
- **Expected**: Skip command is recognized and tasks are skipped
- **Output**: `[✓] Skip command: PASS` or `[✗] ... FAIL`

#### Test 4: Exit Command
- **What**: Tests that 'exit' command works
- **How**:
  - Loads dataset and starts Exercise 1
  - Completes one task correctly
  - Types 'exit' during second task
  - Checks for "Exercise exited" in output
- **Expected**: Exercise exits immediately with grade calculation
- **Output**: `[✓] Exit command: PASS` or `[✗] ... FAIL`

### How to Run
```bash
python test_simulation.py
```

### Output Format
```
[TEST] Testing dataset loading validation...
[✓] Dataset loading validation: PASS
[TEST] Testing correct answer display (3 failed attempts)...
[✓] Correct answer display (3 failed attempts): PASS
...

TEST SUMMARY
============================================================
✓ Dataset validation: PASS
✓ Correct answer display: PASS
✓ Skip command: PASS
✓ Exit command: PASS

Total: 4/4 tests passed
```

---

## 2. `test_every_task.py` - Exercise Case Testing

### Purpose
Tests all 4 cases for each exercise (20 tests total: 5 exercises × 4 cases).

### What It Tests

For each exercise (1-5), it tests 4 cases:

#### Case 1: Correct Answer
- **What**: Verifies correct answers work
- **How**: 
  - For Exercise 1: Uses known correct answers (df.head(5), df.shape, etc.)
  - For others: Just verifies structure works
- **Expected**: Program accepts correct answers and moves forward
- **Output**: `[✓] Exercise X - Case 1: Correct answer` or `[✗] ... FAIL`

#### Case 2: 3 Wrong Answers
- **What**: Verifies answer shown exactly once after 3 wrong attempts
- **How**:
  - Provides 3 wrong answers for first task
  - Counts "CORRECT ANSWER" occurrences
- **Expected**: Exactly 1 occurrence of "CORRECT ANSWER"
- **Output**: `[✓] Exercise X - Case 2: 3 wrong answers` or `[✗] ... FAIL`

#### Case 3: Exit Command
- **What**: Verifies 'exit' works and calculates grade
- **How**:
  - Starts exercise and immediately types 'exit'
  - Checks for "Exercise exited", "Score", and grade format
- **Expected**: Exercise exits with grade shown (e.g., "0/8 tasks (0.0%)")
- **Output**: `[✓] Exercise X - Case 3: Exit command` or `[✗] ... FAIL`

#### Case 4: Skip Command
- **What**: Verifies 'skip' works and doesn't contribute to grade (0%)
- **How**:
  - Skips first task
  - For Exercise 1: Completes second task correctly, then exits
  - Checks for "skipped" message and grade calculation
- **Expected**: Skip is recognized, grade is calculated correctly
- **Output**: `[✓] Exercise X - Case 4: Skip command` or `[✗] ... FAIL`

### How to Run
```bash
python test_every_task.py
```

### Output Format
```
======================================================================
EXERCISE 1 - Testing All 4 Cases
======================================================================
[✓] Exercise 1 - Case 1: Correct answer
[✓] Exercise 1 - Case 2: 3 wrong answers
[✓] Exercise 1 - Case 3: Exit command
[✓] Exercise 1 - Case 4: Skip command

...

TEST SUMMARY
======================================================================
Total Tests: 20
✓ Passed: 20
✗ Failed: 0
Success Rate: 100.0%
```

---

## 3. `test_all_tasks.py` - First Task Testing

### Purpose
Tests the first task of each exercise for all 4 cases (20 tests total).

### What It Tests

Similar to `test_every_task.py`, but focuses on Task 1 of each exercise:
- Tests Case 1-4 for Exercise 1, Task 1
- Tests Case 1-4 for Exercise 2, Task 1
- ... and so on for all 5 exercises

### How to Run
```bash
python test_all_tasks.py
```

### Output Format
```
======================================================================
TESTING EXERCISE 1 - ALL TASKS (4 cases each)
======================================================================

Exercise 1 - Task 1:
  [✓] Case 1: Correct answer
  [✓] Case 2: 3 wrong answers
  [✓] Case 3: Exit command
  [✓] Case 4: Skip command

...

TEST SUMMARY
======================================================================
Total Tests: 20
✓ Passed: 20
✗ Failed: 0
Success Rate: 100.0%
```

---

## 4. `test_all_tasks_comprehensive.py` - Comprehensive Task Testing

### Purpose
Comprehensive testing that covers all tasks in each exercise (20 tests total).

### What It Tests

For each exercise, it tests all 4 cases but with more thorough coverage:

#### Case 1: Correct Answers
- **What**: Tests correct answers work across all tasks
- **How**: 
  - Skips first 7 tasks, then tests correct answer on last task
  - For Exercise 1: Uses known correct answer (df.describe())
- **Expected**: Correct answers are accepted

#### Case 2: 3 Wrong Answers
- **What**: Tests answer shown once after 3 wrong attempts
- **How**:
  - Provides 3 wrong answers for task 1
  - Skips remaining 7 tasks
  - Counts "CORRECT ANSWER" (should be 1 from wrong attempts + 7 from skips = 8 total)
- **Expected**: At least 1 "CORRECT ANSWER" from wrong attempts

#### Case 3: Exit Command
- **What**: Tests exit works from any task
- **How**:
  - Skips task 1, then exits from task 2
  - Verifies grade is calculated (should be 0/8 = 0%)
- **Expected**: Exit works, grade shown correctly

#### Case 4: Skip All Tasks
- **What**: Tests that skipping all tasks results in 0% grade
- **How**:
  - Skips all 8 tasks
  - Verifies grade shows 0/8 or 0.0%
- **Expected**: Grade is 0% when all tasks skipped

### How to Run
```bash
python test_all_tasks_comprehensive.py
```

### Output Format
```
======================================================================
EXERCISE 1 - Comprehensive Testing (All Tasks)
======================================================================
[✓] Exercise 1 - Case 1: Correct answer
[✓] Exercise 1 - Case 2: 3 wrong answers (answer shown once)
[✓] Exercise 1 - Case 3: Exit command
[✓] Exercise 1 - Case 4: Skip (0% contribution)

...

TEST SUMMARY
======================================================================
Total Tests: 20
✓ Passed: 20
✗ Failed: 0
Success Rate: 100.0%
```

---

## 5. `comprehensive_test.py` - Full Program Testing

### Purpose
Tests ALL functionalities of the entire program (17+ tests).

### What It Tests

#### Main Menu Tests
- Invalid choice handling

#### Dataset Loading Tests (3 tests)
- Invalid input validation (non-numeric, out of range)
- Error when trying exercises without dataset
- Error when trying exploration without dataset

#### Dataset Exploration Test (1 test)
- All 11 exploration menu options:
  1. View head
  2. View tail
  3. View info
  4. View statistics
  5. View columns/types
  6. Check missing values
  7. View unique values
  8. Filter data
  9. Group by and aggregate
  10. Sort data
  11. Return to menu

#### Statistics Tests (2 tests)
- View learning statistics
- Reset statistics (with confirmation)
- Cancel statistics reset

#### Exercise Menu Test (1 test)
- Access all 5 exercises
- Invalid exercise choice handling

#### Exercise Functionality Tests (4 tests)
- Correct answers work
- 3 failed attempts show answer exactly once
- Skip command works
- Exit command works

#### All Exercises Tests (5 tests)
- Exercise 1: All 8 tasks
- Exercise 2: All 8 tasks
- Exercise 3: All 8 tasks
- Exercise 4: All 8 tasks
- Exercise 5: All 8 tasks

### How to Run
```bash
python comprehensive_test.py
```

### Output Format
```
======================================================================
PANDAS PRACTICE - COMPREHENSIVE TEST SUITE
======================================================================

[TEST] Running: Main menu invalid choice
[✓] Main menu invalid choice

[TEST] Running: Dataset loading (invalid inputs)
[✓] Dataset loading validation

...

TEST SUMMARY
======================================================================
Total Tests: 17
✓ Passed: 17
✗ Failed: 0
Success Rate: 100.0%
```

---

## Common Patterns

### How Tests Work

1. **Input Preparation**: Each test creates a list of inputs (menu choices, answers, commands)
2. **Subprocess Launch**: Starts `main.py` as a subprocess
3. **Input Injection**: Sends all inputs via stdin
4. **Output Capture**: Captures stdout and stderr
5. **Verification**: Checks for expected strings/patterns in output
6. **Result Reporting**: Shows ✓ (pass) or ✗ (fail) with test name

### Example Test Flow

```python
inputs = [
    "1", "1",      # Load dataset: menu option 1, select dataset 1
    "3", "1",      # Run exercise: menu option 3, exercise 1
    "df.head(5)",  # Correct answer for task 1
    "exit",        # Exit exercise
    "5"            # Exit program
]

# Run simulation
success, stdout, stderr = run_simulation(inputs, "Test name")

# Verify
if "✅" in stdout:
    log("Test name", "PASS")
else:
    log("Test name", "FAIL")
```

### Pass/Fail Indicators

- `[✓]` = Test passed
- `[✗]` = Test failed
- `[TEST]` = Test in progress

---

## Which Test to Use?

- **Quick check**: `test_simulation.py` (4 basic tests)
- **Exercise cases**: `test_every_task.py` (20 tests, all 4 cases per exercise)
- **Task focus**: `test_all_tasks.py` (20 tests, first task of each exercise)
- **Comprehensive**: `test_all_tasks_comprehensive.py` (20 tests, thorough coverage)
- **Full program**: `comprehensive_test.py` (17+ tests, all features)

---

## Troubleshooting

If a test fails:
1. Check the test output for the specific failure message
2. Look for `[✗]` indicators to see which tests failed
3. Review the test code to understand what it's checking
4. Run `main.py` manually to verify the feature works
5. Check that datasets exist in the `data/` directory


# How to Run the Test Scripts

## Quick Start

### Basic Test Suite (4 tests)
```bash
python test_simulation.py
```

### Comprehensive Test Suite (17 tests - ALL functionalities)
```bash
python comprehensive_test.py
```

## What Gets Tested

### ✅ Comprehensive Test Suite Covers:

#### 1. Main Menu (1 test)
- Invalid choice handling

#### 2. Dataset Loading (3 tests)
- Invalid input validation (non-numeric, out of range)
- Error when trying exercises without dataset
- Error when trying exploration without dataset

#### 3. Dataset Exploration (1 test)
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

#### 4. Statistics (2 tests)
- View learning statistics
- Reset statistics (with confirmation)
- Cancel statistics reset

#### 5. Exercise Menu (1 test)
- Access all 5 exercises
- Invalid exercise choice handling

#### 6. Exercise Functionality (4 tests)
- Correct answers work
- 3 failed attempts show answer exactly once
- Skip command works
- Exit command works

#### 7. All Exercises (5 tests)
- Exercise 1: All 8 tasks
- Exercise 2: All 8 tasks
- Exercise 3: All 8 tasks
- Exercise 4: All 8 tasks
- Exercise 5: All 8 tasks

## Test Results

When you run the comprehensive test, you'll see:

```
======================================================================
PANDAS PRACTICE - COMPREHENSIVE TEST SUITE
======================================================================
Testing ALL functionalities of the application...

[✓] Main menu invalid choice
[✓] Dataset loading validation
[✓] Exercise without dataset
[✓] Explore without dataset
[✓] Explore dataset all options
[✓] Statistics view and reset
[✓] Statistics reset cancel
[✓] All exercises menu access
[✓] Exercise with correct answers
[✓] Exercise 3 failed attempts (answer shown 1x)
[✓] Exercise skip command
[✓] Exercise exit command
[✓] Exercise 1 all tasks
[✓] Exercise 2 all tasks
[✓] Exercise 3 all tasks
[✓] Exercise 4 all tasks
[✓] Exercise 5 all tasks

======================================================================
TEST SUMMARY
======================================================================
Total Tests: 17
✓ Passed: 17
✗ Failed: 0
Success Rate: 100.0%
```

## Understanding the Output

- **[✓]** = Test passed
- **[✗]** = Test failed
- **[TEST]** = Test in progress

## What the Tests Verify

1. **Correct Answer Display**: After 3 failed attempts, the correct answer is shown **exactly once** (not multiple times)

2. **Special Commands**: 
   - `skip` - Skips current task, shows answer, counts as incorrect
   - `exit` - Exits exercise immediately, calculates grade based on completed tasks

3. **Input Validation**: 
   - Invalid dataset numbers are caught
   - Invalid menu choices are handled
   - Non-numeric inputs are rejected

4. **All Functionalities**: Every menu option, every exercise, every task is tested

## Notes

- Tests run in non-interactive mode (automated)
- ESC key prompts automatically use Enter key fallback
- Some tests may take 1-3 minutes to complete
- Tests verify no errors occur during normal operation
- Tests verify all features work as expected

## Troubleshooting

If tests fail:
1. Ensure datasets exist: `ls data/*.csv`
2. Install dependencies: `pip install -r requirements.txt`
3. Test main program manually: `python main.py`
4. Check error messages in test output


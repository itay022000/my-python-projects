# Test Suite Instructions

## How to Run the Tests

### Quick Test (Basic Functionality)
```bash
python test_simulation.py
```

This runs 4 basic tests:
- Dataset loading validation
- Correct answer display (3 failed attempts)
- Skip command
- Exit command

### Comprehensive Test (All Functionalities)
```bash
python comprehensive_test.py
```

This runs **comprehensive tests covering ALL functionalities**:
- Main menu (invalid choices)
- Dataset loading (all validation scenarios)
- Dataset exploration (all 11 options)
- Statistics viewing and resetting
- All 5 exercises (all tasks)
- Exercise commands (skip, exit, correct answers, failed attempts)
- Error handling (no dataset loaded scenarios)

## What Gets Tested

### ✅ Main Menu
- Invalid choice handling
- All 5 menu options accessible

### ✅ Dataset Loading
- Invalid input (non-numeric)
- Invalid number (out of range)
- Valid selection
- Error when trying to use features without dataset

### ✅ Dataset Exploration (All 11 Options)
1. View first few rows (head)
2. View last few rows (tail)
3. View dataset info
4. View basic statistics
5. View column names and data types
6. Check for missing values
7. View unique values in a column
8. Filter data by condition
9. Group by and aggregate
10. Sort data
11. Return to main menu

### ✅ Statistics
- View learning statistics
- Reset statistics (with confirmation)
- Cancel statistics reset
- View datasets explored
- View exercise completion counts and grades

### ✅ All 5 Exercises
Each exercise is tested with:
- **Exercise 1**: Basic Operations (8 tasks)
- **Exercise 2**: Filtering Data (8 tasks)
- **Exercise 3**: Sorting and Selection (8 tasks)
- **Exercise 4**: Data Manipulation (8 tasks)
- **Exercise 5**: Data Cleaning (8 tasks)

### ✅ Exercise Functionality
For each exercise, the following are tested:
- **Correct answers**: Exercises accept correct answers
- **3 failed attempts**: Correct answer shown exactly once
- **Skip command**: Tasks can be skipped
- **Exit command**: Exercises can be exited early
- **All tasks**: All 8 tasks in each exercise are accessible

## Test Output

The test suite provides:
- ✓ Pass/Fail status for each test
- Summary with total passed/failed counts
- Success rate percentage
- Error messages if any tests fail

## Expected Results

When all tests pass, you should see:
```
Total Tests: 20+
✓ Passed: 20+
✗ Failed: 0
Success Rate: 100.0%
```

## Troubleshooting

If tests fail:
1. Make sure datasets exist in the `data/` directory
2. Ensure all dependencies are installed: `pip install -r requirements.txt`
3. Check that `main.py` runs without errors: `python main.py`
4. Review error messages in the test output

## Notes

- Tests run in non-interactive mode (subprocess)
- ESC key prompts fall back to Enter key
- Some tests may take longer (up to 2-3 minutes for comprehensive tests)
- Tests verify that correct answers are shown exactly once after 3 failed attempts
- Tests verify all special commands (skip, exit) work correctly


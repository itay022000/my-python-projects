# Quick Start: Running Tests

## Simplest Way to Run Tests

Open your terminal, navigate to the project directory, and run one of these commands:

### Option 1: Quick Test (Fastest - ~30 seconds)
```bash
python test_simulation.py
```
Tests basic functionality: dataset loading, skip/exit commands, correct answer display.

### Option 2: Comprehensive Test (Recommended - ~2-3 minutes)
```bash
python comprehensive_test.py
```
Tests **ALL functionalities** of your program including all exercises, dataset exploration, statistics, etc.

### Option 3: Task Testing (Tests all 4 cases for each exercise)
```bash
python test_all_tasks_comprehensive.py
```
Tests that all tasks correctly handle: correct answers, 3 wrong answers, skip, and exit commands.

## Step-by-Step Instructions

1. **Open Terminal** (or Command Prompt on Windows)

2. **Navigate to your project folder:**
   ```bash
   cd /Users/shanitiomkin/Desktop/projects/pandas-practice
   ```
   (Or wherever your project is located)

3. **Run a test:**
   ```bash
   python comprehensive_test.py
   ```

4. **Watch the output** - You'll see:
   - `[TEST]` messages showing what's being tested
   - `[✓]` for passed tests
   - `[✗]` for failed tests
   - A summary at the end

## Example Output

When you run a test, you'll see something like:

```
======================================================================
PANDAS PRACTICE - COMPREHENSIVE TEST SUITE
======================================================================
Testing ALL functionalities of the application...

[TEST] Running: Main menu invalid choice
[✓] Main menu invalid choice

[TEST] Running: Dataset loading validation
[✓] Dataset loading validation

...

======================================================================
TEST SUMMARY
======================================================================
Total Tests: 17
✓ Passed: 17
✗ Failed: 0
Success Rate: 100.0%
```

## Which Test Should I Run?

- **First time?** → Run `python comprehensive_test.py` (most thorough)
- **Quick check?** → Run `python test_simulation.py` (fastest)
- **Testing task behavior?** → Run `python test_all_tasks_comprehensive.py` (tests all 4 cases)

## Troubleshooting

**If you get "command not found":**
- Make sure you're in the project directory
- Try `python3` instead of `python`

**If tests fail:**
- Make sure you have datasets in the `data/` folder
- Check that `main.py` runs without errors first: `python main.py`

**If you see import errors:**
- Install dependencies: `pip install -r requirements.txt`


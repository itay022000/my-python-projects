# Pandas Practice Lite — Interactive Learning Tool

A hands-on Python CLI for practicing **pandas** on a real sales dataset: exploration, exercises, and progress tracking.

## Requirements

- **Python 3.10+** recommended (verified on **3.10.9** for maintenance brief B002)
- See `requirements.txt` (`pandas`, `numpy`; plotting tasks use `matplotlib` / `seaborn`)

## Installation

```bash
cd pandas-practice-lite
pip install -r requirements.txt
python create_datasets.py   # if data/sales_data.csv is missing
```

## Usage

```bash
python3 main.py
```

On startup the app loads **`data/sales_data.csv`** automatically.

### Main menu

| Option | Action |
|--------|--------|
| 1 | Explore dataset (head, tail, info, stats, filter, sort, …) |
| 2 | Run exercise (1–5) |
| 3 | View learning statistics |
| 4 | Exit |

### Exercises (option 2)

| # | Topic |
|---|--------|
| 1 | Basic Operations |
| 2 | Filtering Data |
| 3 | Sorting and Column Selection |
| 4 | Data Manipulation |
| 5 | Data Cleaning |

Each exercise has **8 tasks**. You type pandas code at the prompt. Many tasks require the **exact** expected code (whitespace is normalized). Special commands:

- **`skip`** — skip the current task (answer shown; task does not count toward score)
- **`exit`** — end the exercise and record your score

After **3 wrong attempts** on a task, the correct answer is shown once and the exercise moves on.

## Project layout

```text
main.py              # Entry: python3 main.py → main()
app.py               # PandasPractice class (wiring + run_exercise + validator delegates)
session_common.py    # Shared CLI helpers (skip/exit, intros, footers)
engine.py            # Question loop (ask_code_question)
hints.py             # Strike-1 hint strings
validators.py        # Sandbox, validate_*, normalize_code / codes_match
progress.py          # Progress JSON load/save, exercise stats, reset
dataset.py           # load_dataset, column/threshold helpers
menus.py             # Main menu, explore (1–9), statistics, wait_for_esc
exercises/
  exercise_1.py … exercise_5.py   # One module per exercise (8 tasks each)
create_datasets.py
data/sales_data.csv
progress.json        # Your stats (auto-created)
scripts/
  qa_regression_b002.py   # validators & helpers (40)
  qa_flow_b002.py          # exercises 5×8×4 (160)
  qa_menus_b002.py         # explore + statistics + plots (39)
tests/archive/       # Notes on legacy root test files
```

## Development / QA

Use a **project virtualenv** so QA does not pick up a broken Anaconda base (NumPy 2.x with old `numexpr` / `bottleneck` / `matplotlib` binaries is a common cause of `_ARRAY_API not found` spam or plot-task failures):

```bash
python3.10 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

From project root (with venv active):

```bash
python3 scripts/qa_regression_b002.py
python3 scripts/qa_flow_b002.py
python3 scripts/qa_menus_b002.py
```

Expect **238** passed total (40 + 160 + 38). If you must use Anaconda base, align versions (`pip install "numpy<2"` and upgrade `numexpr`, `bottleneck`, `matplotlib`) or create a dedicated conda env from `requirements.txt`.

## License

Learning project — use and modify freely.

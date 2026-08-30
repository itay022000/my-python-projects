# Matplotlib Pyplot Practice

An interactive command-line program for practicing **matplotlib.pyplot** across six exercise sequences: line plots, subplots, scatter plots, bar plots, histograms, and pie charts.

## Description

Run `main.py` to open a main menu. Each menu exercise contains **3 series**. Every series guides you step by step; you type Python/matplotlib code for each **question** (step). The program uses **exact matching** — only the precisely expected answer is accepted before you move on.

After a menu exercise, you see **three-bucket** statistics: **Completed**, **Completed (with help)**, and **Not completed**.

## Main menu

| Option | Sequence |
|--------|----------|
| 1 | Line Plot Exercise |
| 2 | Subplot Exercise |
| 3 | Scatter Plot Exercise |
| 4 | Bar Plot Exercise |
| 5 | Histogram Exercise |
| 6 | Pie Chart Exercise |
| 7 | Exit (type `7` or `exit` exactly) |

## During a menu exercise

1. **Teach intro** — short rules (python-basics style), then **Press Enter to start...**
2. **Tip** — `skip` skips the current series; `exit` / `quit` ends early → main menu
3. **Questions** — `STEP n: …` with **`Your code (attempt n/3):`**

### Special commands (any question)

| Input | Effect |
|--------|--------|
| **`skip` / `Skip`** | `Skipping series.` → next series (or stats); series = **Not completed** |
| **`exit` / `Exit`**, **`quit` / `Quit`** | Partial score → **main menu** |
| **Empty line** | Re-prompt; **no strike** |

### Strikes (per question)

| Attempt | On wrong |
|---------|----------|
| **1** | Hint (except final `plt.show()` step) + `Try again...` |
| **2** | No new hint + `Try again...` |
| **3** | Exact expected code line → **next question** (or stats if last question of last series) |

### Scoring (per series)

| Bucket | When |
|--------|------|
| **Completed** | All steps answered correctly (no strike-3 reveal) |
| **Completed (with help)** | Series finished all steps; ≥1 strike-3 reveal **and** ≥1 step answered correctly |
| **Not completed** | Series **skip**ped, **exit** before finish, or finished with **0** steps answered correctly (all revealed) |

## Features (all menu exercises)

- **Step-by-step prompts** with clear variable-name rules per step
- **Random exercise data** generated when each module loads (counts and rules are fixed per sequence type)
- **Three-strike rule per question** (not cumulative across a series)
- **Exact verification** of code strings (whitespace normalized; no alternate spellings)
- **Shared internals**: `engine.py` + `session_common.py` + `hints.py` (strikes, skip/exit, hints, three-bucket statistics)

## Sequence overview

| Module | Topic | Exercises | Notes |
|--------|-------|-----------|--------|
| `exercises/plot_exercises.py` | Line plots, labels, grid | 3 | Three variants: multi-line styling, titled axes, grid |
| `exercises/subplot_exercises.py` | `plt.subplot`, titles | 3 | 1×2 or 2×1 layouts; optional suptitle |
| `exercises/scatter_plot_exercises.py` | `plt.scatter` | 3 | Color arrays, sizes, numeric colors |
| `exercises/bar_plot_exercises.py` | `plt.bar` / `plt.barh` | 3 | Vertical bars, width, horizontal bars |
| `exercises/histogram_exercises.py` | `plt.hist` | 3 | `np.random.normal` then histogram |
| `exercises/pie_chart_exercises.py` | `plt.pie` | 3 | Proportions, colors, labels; optional explode, shadow, legend |

## Requirements

- **Python 3.10+** recommended (verified on 3.10.9 for maintenance brief B001)
- `numpy >= 1.20.0`
- `matplotlib >= 3.3.0`

See `requirements.txt`.

## Installation

```bash
cd matplotlib-practice
pip install -r requirements.txt
```

## Usage

```bash
python3 main.py
```

1. Choose a menu exercise (1–6), or exit with `7` or `exit` (exact, lowercase).
2. Read the teach intro; press Enter.
3. Complete each **question**; up to 3 attempts per question (see strikes above).
4. View three-bucket statistics at the end (or partial score on early exit).

## Verification rules (learners)

- Type answers as instructed (exact variable names: e.g. pie chart uses `x`, `c`, `lb`, `ex` where specified).
- Colors in arrays are **color name strings** (e.g. `"red"`), not RGB tuples, unless the step says otherwise.
- Only the shown correct pattern is accepted; extra spaces are normalized, but wrong names or values are rejected.

## Project layout

```text
main.py                 # Thin entry
app.py                  # Menu shell (MatplotlibPractice)
engine.py               # Series/step runner + normalize helpers
session_common.py       # Strike/skip/exit CLI helpers
hints.py                # Strike-1 hint strings
exercises/              # Six *_exercises.py series modules
requirements.txt
scripts/qa_regression_b001.py   # Validator regression (228 checks)
scripts/qa_flow_b008.py         # B008 flow: strikes, skip, exit, hints, stats
scripts/archive/                # Pre-B008 QA (historical)
```

## Development / QA

Regression check for validators (does not replace learner-facing manual practice):

```bash
python3 scripts/qa_regression_b001.py
python3 scripts/qa_flow_b008.py
```

Both must exit **0** before release.

## License / origin

Practice project for learning matplotlib pyplot interactively in the terminal.
